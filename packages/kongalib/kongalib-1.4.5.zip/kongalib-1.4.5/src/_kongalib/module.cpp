/** @file mga/module/module.cpp
 *
 *		Main MGA Python module file.
 *
 *		$Revision: 27757 $
 *		$Date: 2018-02-22 11:04:43 +0100 (gio, 22 feb 2018) $
 *		$Author: lillo $
 *
 *		\defgroup mga_module MGA Python extension module
 *		The MGA Python extension module is a wrapper around the \ref mga_client and part of the \ref CL for Python.
 */

/*@{*/

#include "Python.h"

#define __DEFINE_DICTIONARY__
#include <konga_client/messages.h>
#undef __DEFINE_DICTIONARY__

#define __DEFINE_COMMANDS__
#include <konga_client/commands.h>
#undef __DEFINE_COMMANDS__

#include "module.h"

#include <list>
#include <algorithm>


CL_RecursiveMutex MGA::gThreadsLock;
CL_Dispatcher *MGA::gDispatcher;
PyObject *MGA::gIdleCB = NULL;
volatile bool MGA::gInitialized = false;

static long sMainThreadID;
static PyObject *sException;
static CL_Translator *sTranslator;
static CL_Mutex sTimerLock;
static std::list<MGA::DeferredObject *> sTimerList;
static std::list<MGA_Client *> sClientList, sFreeClientsList;
static std::list<MGA::InterpreterObject *> sInterpreterList;
static CL_AESCipher sCipher;


string
MGA::translate(MGA_Status error)
{
	return sTranslator->Get(error);
}


PyObject *
MGA::setException(MGA_Status error_code, const string& error_msg)
{
	std::string string = error_msg;
	if (string.empty())
		string = sTranslator->Get(error_code);
	PyObject *args = Py_BuildValue("is", error_code, (const char *)string.c_str());
	PyErr_SetObject(sException, args);
	Py_DECREF(args);
	return NULL;
}


/**
 *	Gets an error message from the server \a output and sets a Python exception accordingly.
 *	\param	error_code			Error code as returned by MGA_Client::Execute().
 *	\param	output				The server output #CLU_Table as returned by MGA_Client::Execute().
 *	\return						Always returns NULL.
 */
PyObject *
MGA::setException(MGA_Status error_code, CLU_Table *output)
{
	MGA_Status result = error_code;
	string error;
	
	if ((result == MGA_OK) && (output->Exists(MGA_OUT_ERRNO)))
		result = output->Get(MGA_OUT_ERRNO).Int32();
	if (result == MGA_OK) {
		result = error_code;
		error = sTranslator->Get(result);
	}
	else {
		if (output->Exists(MGA_OUT_ERROR))
			error = output->Get(MGA_OUT_ERROR).String();
		else
			error = sTranslator->Get(result);
	}
	return MGA::setException(result, error);
}


/**
 *	Gets an error message from the server \a output and sets a Python exception accordingly.
 *	\param	output				The server output #CLU_Table as returned by MGA_Client::Execute().
 *	\return						Always returns NULL.
 */
PyObject *
MGA::setException(MGA::ClientObject *client, MGA_Status result)
{
	return MGA::setException(result, sTranslator->Get(result));
}


bool
MGA::trackClient(MGA::ClientObject *client)
{
	CL_AutoLocker locker(&MGA::gThreadsLock);
	if (MGA::gInitialized) {
		if (sFreeClientsList.empty()) {
			client->fClient = CL_New(MGA_Client(MGA::gDispatcher));
			sClientList.push_back(client->fClient);
		}
		else {
			client->fClient = sFreeClientsList.back();
			sFreeClientsList.pop_back();
		}

		return true;
	}
	return false;
}


void
MGA::untrackClient(MGA::ClientObject *client)
{
	CL_AutoLocker locker(&MGA::gThreadsLock);
	if (MGA::gInitialized) {
		client->fClient->Disconnect();

		sFreeClientsList.push_front(client->fClient);
	}
}


void
MGA::trackInterpreter(MGA::InterpreterObject *interpreter)
{
	CL_AutoLocker locker(&MGA::gThreadsLock);
	if (MGA::gInitialized) {
		sInterpreterList.push_back(interpreter);
	}
}


void
MGA::untrackInterpreter(MGA::InterpreterObject *interpreter)
{
	CL_AutoLocker locker(&MGA::gThreadsLock);
	if (MGA::gInitialized) {
		std::list<MGA::InterpreterObject *>::iterator it = find(sInterpreterList.begin(), sInterpreterList.end(), interpreter);
		if (it != sInterpreterList.end())
			sInterpreterList.erase(it);
	}
}


MGA::DeferredObject::DeferredObject(ClientObject *client, PyObject *userData, PyObject *success, PyObject *error, PyObject *progress, PyObject *idle)
	: fClient(client), fSuccess(success), fError(error), fProgress(progress), fIdle(idle), fUserData(userData), fAborted(false), fExecuted(false)
{
	Py_XINCREF(client);
	Py_INCREF(userData);
	Py_XINCREF(success);
	Py_XINCREF(error);
	Py_XINCREF(progress);
	Py_XINCREF(idle);
}


MGA::DeferredObject::~DeferredObject()
{
	Py_XDECREF(fClient);
	Py_XDECREF(fSuccess);
	Py_XDECREF(fError);
	Py_XDECREF(fProgress);
	Py_XDECREF(fIdle);
	Py_DECREF(fUserData);
}


MGA::DeferredObject *
MGA::DeferredObject::Allocate(MGA::ClientObject *client, PyObject *userData, PyObject *success, PyObject *error, PyObject *progress, PyObject *idle)
{
	return new (DeferredType.tp_alloc(&DeferredType, 0)) DeferredObject(client, userData, success, error, progress, idle);
}


static void
Deferred_dealloc(MGA::DeferredObject *self)
{
	self->~DeferredObject();
	self->ob_type->tp_free((PyObject*)self);
}


static PyObject *
Deferred_cancel(MGA::DeferredObject *self, PyObject *args)
{
	if (!self->fAborted) {
		sTimerLock.Lock();
		self->fAborted = true;
		self->fCondition.Signal();
		sTimerLock.Unlock();
	}
	
	Py_RETURN_NONE;
}


static PyMethodDef Deferred_methods[] = {
	{	"cancel",			(PyCFunction)Deferred_cancel,				METH_NOARGS,					"Cancels this Deferred, setting 'aborted' attribute to True." },
	{	NULL,				NULL,										0,								NULL }
};


static PyObject *
Deferred_get_aborted(MGA::DeferredObject *self, void *data)
{
	if (self->fAborted)
		Py_RETURN_TRUE;
	else
		Py_RETURN_FALSE;
}


static PyObject *
Deferred_get_executed(MGA::DeferredObject *self, void *data)
{
	if (self->fExecuted)
		Py_RETURN_TRUE;
	else
		Py_RETURN_FALSE;
}


static PyGetSetDef Deferred_getset[] = {
	{	"aborted",				(getter)Deferred_get_aborted,			NULL,			"Aborted Deferred status", NULL },
	{	"executed",				(getter)Deferred_get_executed,			NULL,			"Executed Deferred status", NULL },
	{	NULL,					NULL,									NULL,			NULL, NULL }
};


/** Vtable describing the MGA.Deferred type. */
PyTypeObject MGA::DeferredType = {
	PyObject_HEAD_INIT(NULL)
    0,										/* ob_size */
    "_kongalib.Deferred",					/* tp_name */
    sizeof(MGA::DeferredObject),			/* tp_basicsize */
	0,										/* tp_itemsize */
	(destructor)Deferred_dealloc,			/* tp_dealloc */
	0,										/* tp_print */
	0,										/* tp_getattr */
	0,										/* tp_setattr */
	0,										/* tp_compare */
	0,										/* tp_repr */
	0,										/* tp_as_number */
	0,										/* tp_as_sequence */
	0,										/* tp_as_mapping */
	0,										/* tp_hash */
	0,										/* tp_call */
	0,										/* tp_str */
	0,										/* tp_getattro */
	0,										/* tp_setattro */
	0,										/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,						/* tp_flags */
	"Deferred objects",						/* tp_doc */
	0,										/* tp_traverse */
	0,										/* tp_clear */
	0,										/* tp_richcompare */
	0,										/* tp_weaklistoffset */
	0,										/* tp_iter */
	0,										/* tp_iternext */
	Deferred_methods,						/* tp_methods */
	0,										/* tp_members */
	Deferred_getset,						/* tp_getset */
};


class TimerJob : public CL_Job
{
public:
	TimerJob(uint32 timeout, MGA::DeferredObject *deferred)
		: CL_Job(), fTimeOut(timeout), fDeferred(deferred)
	{
		Py_INCREF(deferred);
		CL_AutoLocker _(&sTimerLock);
		sTimerList.push_back(fDeferred);
	}
	
	~TimerJob() {
		if ((Py_IsInitialized()) && (MGA::gInitialized)) {
			PyGILState_STATE gstate;
			gstate = PyGILState_Ensure();
			Py_DECREF(fDeferred);
			PyGILState_Release(gstate);
		}
	}
	
	virtual CL_Status Run() {
		sTimerLock.Lock();
		CL_Status status;
		if (fDeferred->fAborted)
			status = CL_ERROR;
		else
			status = fDeferred->fCondition.Wait(&sTimerLock, fTimeOut);
		sTimerLock.Unlock();
		
		if (status == CL_TIMED_OUT) {
// 			CL_AutoLocker locker(&MGA::gThreadsLock);
			if ((Py_IsInitialized()) && (MGA::gInitialized)) {
				PyGILState_STATE gstate;
				gstate = PyGILState_Ensure();
				
				if ((!fDeferred->fAborted) && (fDeferred->fSuccess)) {
					PyObject *result = PyObject_CallFunctionObjArgs(fDeferred->fSuccess, fDeferred->fUserData, NULL);
					Py_XDECREF(result);
					if (PyErr_Occurred()) {
						PyErr_Print();
						PyErr_Clear();
					}
					fDeferred->fExecuted = true;
				}
				PyGILState_Release(gstate);
			}
		}
		
		sTimerLock.Lock();
		std::list<MGA::DeferredObject *>::iterator it = find(sTimerList.begin(), sTimerList.end(), fDeferred);
		if (it != sTimerList.end())
			sTimerList.erase(it);
		sTimerLock.Unlock();
		
		return CL_OK;
	}
	
private:
	uint32					fTimeOut;
	MGA::DeferredObject		*fDeferred;
};


static PyObject *
start_timer(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "milliseconds", "callback", "userdata", NULL };
	int32 ms;
	PyObject *callback, *userdata = Py_None;
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "iO|O", kwlist, &ms, &callback, &userdata))
		return NULL;
	
	MGA::DeferredObject *deferred = MGA::DeferredObject::Allocate(NULL, userdata, callback, NULL, NULL);
	if (MGA::gInitialized)
		MGA::gDispatcher->AddJob(CL_New(TimerJob(CL_MAX(0, ms), deferred)), true);
	return (PyObject *)deferred;
}


/**
 *	Converts a dict object to an XML document and saves it inside an unicode string. The XML format is the same
 *	as the one returned via CLU_Table::SaveXML().
 *	\param	self				Unused.
 *	\param	args				Arguments tuple.
 *	\param	kwds				Supported argument keywords. Accepted keywords are:
 *								- \e dict: the Python dict object to be converted to XML.
 *	\return						An unicode string holding the XML document derived from \e dict.
 */
static PyObject *
save_xml(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "dict", NULL };
	CLU_Table *table = NULL;
	PyObject *dict, *result;
	CL_XML_Document doc;
	CL_Blob stream;
	string xml;
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!", kwlist, &PyDict_Type, &dict))
		return NULL;
	
	table = MGA::Table_FromPy(dict);
	if (PyErr_Occurred()) {
		CL_Delete(table);
		return NULL;
	}
	Py_BEGIN_ALLOW_THREADS
	doc.SetRoot(table->SaveXML());
	CL_Delete(table);
	doc.Save(stream);
	stream.Rewind();
	xml << stream;
	Py_END_ALLOW_THREADS
	result = PyUnicode_DecodeUTF8(xml.c_str(), xml.size(), NULL);
	
	return result;
}


/**
 *	Loads the contents of an XML document held in a string into a Python dict object. The XML format understood
 *	must be in the same form as accepted by CLU_Table::LoadXML(). If an error occurs while loading the XML data,
 *	a ValueError exception is raised.
 *	\param	self				Unused.
 *	\param	args				Arguments tuple.
 *	\param	kwds				Supported argument keywords. Accepted keywords are:
 *								- \e xml: an unicode string holding the XML document representing the dict.
 *	\return						A dict object representing the data held in the XML document in \e xml.
 */
static PyObject *
load_xml(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "xml", NULL };
	CLU_Table table;
	string xml;
	CL_XML_Document doc;
	CL_XML_Node *root;
	bool load;
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&", kwlist, MGA::ConvertString, &xml))
		return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	CL_Blob stream;
	stream << xml;
	stream.Rewind();
	load = doc.Load(stream);
	Py_END_ALLOW_THREADS
	if (!load) {
		PyErr_SetString(PyExc_ValueError, doc.GetError().c_str());
		return NULL;
	}
	
	root = doc.GetRoot();
	if ((!root) || (!table.LoadXML(root))) {
		PyErr_SetString(PyExc_ValueError, "malformed XML dictionary definition");
		return NULL;
	}
	
	return MGA::Table_FromCLU(&table);
}


/**
 *	Performs a forward or reverse DNS lookup, given an \e address on input. If \e address is an host name, a forward DNS
 *	lookup is performed and the function returns the associated IP in dotted numbers format. If \e address is in dotted
 *	numbers format, a reverse DNS lookup is performed and the function returns the associated host name. If lookup fails,
 *	the same input string is returned.
 *	\param	self				Unused.
 *	\param	args				Arguments tuple.
 *	\param	kwds				Supported argument keywords. Accepted keywords are:
 *								- \e address: an unicode string holding the IP or host name to be looked up.
 *	\return						An unicode string object holding the looked up address, or unmodified \e address on error.
 */
static PyObject *
host_lookup(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "address", NULL };
	string address;
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&", kwlist, MGA::ConvertString, &address))
		return NULL;
	
	Py_BEGIN_ALLOW_THREADS
	address = CL_NetAddress::Lookup(address);
	Py_END_ALLOW_THREADS
	
	return PyUnicode_DecodeUTF8(address.c_str(), address.size(), NULL);
}


static PyObject *
get_network_interfaces(PyObject *self, PyObject *args, PyObject *kwds)
{
	PyObject *result;
	CL_NetInterface IFs[32];
	uint32 i, numIFs;
	
	Py_BEGIN_ALLOW_THREADS
	numIFs = CL_NetInterface::Enumerate(IFs, 32);
	Py_END_ALLOW_THREADS
	result = PyTuple_New(numIFs);
	
	for (i = 0; i < numIFs; i++) {
		PyObject *entry = PyDict_New();
		PyObject *temp;
		CL_NetInterface *IF = &IFs[i];
		CL_NetAddress address;
		uint8 mac[6];
		
		temp = PyString_FromStringAndSize(IF->GetName(), strlen(IF->GetName()));
		PyDict_SetItemString(entry, "name", temp);
		Py_DECREF(temp);
		
		IF->GetMAC(mac);
		temp = PyString_FromStringAndSize((const char *)mac, 6);
		PyDict_SetItemString(entry, "mac", temp);
		Py_DECREF(temp);
		
		address = IF->GetAddress();
		temp = PyString_FromStringAndSize(address.GetIP().c_str(), address.GetIP().size());
		PyDict_SetItemString(entry, "address", temp);
		Py_DECREF(temp);
		
		address = IF->GetNetmask();
		temp = PyString_FromStringAndSize(address.GetIP().c_str(), address.GetIP().size());
		PyDict_SetItemString(entry, "netmask", temp);
		Py_DECREF(temp);
		
		address = IF->GetBroadcast();
		temp = PyString_FromStringAndSize(address.GetIP().c_str(), address.GetIP().size());
		PyDict_SetItemString(entry, "broadcast", temp);
		Py_DECREF(temp);
		
		temp = PyInt_FromLong(IF->GetFeatures());
		PyDict_SetItemString(entry, "features", temp);
		Py_DECREF(temp);
		
		PyTuple_SetItem(result, (Py_ssize_t)i, entry);
	}
	return result;
}


static PyObject *
get_machine_uuid(PyObject *self, PyObject *args, PyObject *kwds)
{
	string uuid = (const char *)MGA::GetComputerUUID();
	return PyUnicode_DecodeUTF8(uuid.c_str(), uuid.size(), NULL);
}


/**
 *	Obtains the hashed version of given plain password.
 *	\param	self				Unused.
 *	\param	args				Arguments tuple.
 *	\param	kwds				Supported argument keywords. Accepted keywords are:
 *								- \e password: an unicode string holding the unencrypted plain password.
 *	\return						An unicode string object holding the hashed password.
 */
static PyObject *
hash_password(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "password", NULL };
	string password;
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&", kwlist, MGA::ConvertString, &password))
		return NULL;
	
	password = MGA::GetPassword(password);
	return PyUnicode_DecodeUTF8(password.c_str(), password.size(), NULL);
}


static PyObject *
set_interpreter_timeout(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "timeout", NULL };
	PyObject *object = NULL;
	uint32 timeout, oldTimeout;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &object))
		return NULL;
	
	if ((!object) || (object == Py_None)) {
		timeout = 0;
	}
	else {
		timeout = PyInt_AsLong(object);
		if (PyErr_Occurred())
			return NULL;
	}
	CL_AutoLocker locker(&MGA::gThreadsLock);
	PyThreadState *current_tstate = PyThreadState_Get();
	for (std::list<MGA::InterpreterObject *>::iterator it = sInterpreterList.begin(); it != sInterpreterList.end(); it++) {
		MGA::InterpreterObject *interpreter = *it;
		if (interpreter->fState) {
			PyThreadState *tstate = PyInterpreterState_ThreadHead(interpreter->fState->interp);
			while (tstate) {
				if (tstate == current_tstate) {
					oldTimeout = interpreter->fTimeOut;
					interpreter->fTimeOut = timeout;
					interpreter->fStartTime = CL_GetTime();
					return PyInt_FromLong(oldTimeout);
				}
				tstate = PyThreadState_Next(tstate);
			}
		}
	}
	PyErr_SetString(PyExc_RuntimeError, "No parent Interpreter object for current context!");
	return NULL;
}


static PyObject *
lock(PyObject *self, PyObject *args)
{
	Py_BEGIN_ALLOW_THREADS
	MGA::gThreadsLock.Lock();
	Py_END_ALLOW_THREADS
	
	Py_RETURN_NONE;
}


static PyObject *
unlock(PyObject *self, PyObject *args)
{
	Py_BEGIN_ALLOW_THREADS
	MGA::gThreadsLock.Unlock();
	Py_END_ALLOW_THREADS
	
	Py_RETURN_NONE;
}


static PyObject *
_cleanup(PyObject *self, PyObject *args)
{
	if ((Py_IsInitialized()) && (MGA::gInitialized) && (PyThreadState_Get()->thread_id == sMainThreadID)) {
		{
			CL_AutoLocker locker(&MGA::gThreadsLock);
			MGA::gInitialized = false;
		}
		
		sTimerLock.Lock();
		for (std::list<MGA::DeferredObject *>::iterator it = sTimerList.begin(); it != sTimerList.end(); it++) {
			MGA::DeferredObject *deferred = *it;
			deferred->fAborted = true;
			deferred->fCondition.Signal();
		}
		sTimerLock.Unlock();
		
		for (std::list<MGA_Client *>::iterator it = sClientList.begin(); it != sClientList.end(); it++) {
			MGA_Client *client = *it;
			Py_BEGIN_ALLOW_THREADS
			client->Disconnect();
			Py_END_ALLOW_THREADS
		}
		
		for (std::list<MGA::InterpreterObject *>::iterator it = sInterpreterList.begin(); it != sInterpreterList.end(); it++) {
			MGA::InterpreterObject *interpreter = *it;
			interpreter->fRunning = false;
			interpreter->fCond.Signal();
		}
		
		Py_BEGIN_ALLOW_THREADS
		if (MGA::gDispatcher) {
			while (!MGA::gDispatcher->WaitForJobs(50)) {
				PyGILState_STATE gstate;
				gstate = PyGILState_Ensure();
				
				if ((MGA::gIdleCB) && (MGA::gIdleCB != Py_None)) {
					PyObject *result = PyObject_CallFunctionObjArgs(MGA::gIdleCB, NULL);
					if (!result) {
						PyErr_Print();
						PyErr_Clear();
					}
					else
						Py_DECREF(result);
				}
				PyGILState_Release(gstate);
			}
		}
		Py_END_ALLOW_THREADS
	}
	
	Py_RETURN_NONE;
}


static CL_Status
_power_callback(int state, void *param)
{
#ifdef WIN32
	if (state == CL_POWER_SLEEP) {
		CL_AutoLocker locker(&MGA::gThreadsLock);
		for (std::list<MGA_Client *>::iterator it = sClientList.begin(); it != sClientList.end(); it++) {
			MGA_Client *client = *it;
			client->Disconnect();
		}
	}
#endif
	return CL_OK;
}


static PyObject *
set_default_idle_callback(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "callback", NULL };
	PyObject *object;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &object))
		return NULL;
	
	Py_INCREF(object);
	Py_XDECREF(MGA::gIdleCB);
	MGA::gIdleCB = object;
	
	Py_RETURN_NONE;
}


static PyObject *
checksum(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "callback", NULL };
	PyObject *object;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &object))
		return NULL;
	
	CL_Blob data;
	if PyBuffer_Check(object) {
		const void *source;
		Py_ssize_t size;
		if (PyObject_AsReadBuffer(object, &source, &size))
			return 0;
		data.Set(source, (uint32)size);
	}
	else {
		Py_buffer view;
		if (PyObject_GetBuffer(object, &view, PyBUF_CONTIG_RO))
			return 0;
		data.Set((const char *)view.buf, (uint32)view.len);
		PyBuffer_Release(&view);
	}
	return PyInt_FromLong(data.CheckSum());
}


static PyObject *
get_application_log_path(PyObject *self, PyObject *args, PyObject *kwds)
{
	string name = CL_GetPath(CL_APPLICATION_PATH);
	string path = CL_GetPath(CL_USER_LOG_PATH);
	if (name.size() > 0)
		name = name.substr(0, name.size() - 1);
#ifdef __CL_WIN32__
	name = name.substr(name.rfind('\\') + 1) + "\\Log\\";
#else
	name = name.substr(name.rfind('/') + 1);
#ifdef __CL_DARWIN__
	name = name.substr(0, name.rfind('.'));
#endif
#endif
	path += name;

	return PyUnicode_DecodeUTF8(path.c_str(), path.size(), NULL);
}


static PyObject *
_aes_set_key(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "key", NULL };
	char *keyBuffer;
	int keyLen;

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#", kwlist, &keyBuffer, &keyLen))
		return NULL;

	CL_Blob key(keyBuffer, keyLen);
	key.Rewind();
	sCipher.SetKey(key);

	Py_RETURN_NONE;
}


static PyObject *
_aes_encrypt(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "data", NULL };
	char *dataBuffer;
	int dataLen;

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#", kwlist, &dataBuffer, &dataLen))
		return NULL;

	CL_Blob data(dataBuffer, dataLen);
	data.Rewind();
	sCipher.Encrypt(data, dataLen);

	return PyBytes_FromStringAndSize((const char *)data.GetData(), (Py_ssize_t)dataLen);
}


static PyObject *
_aes_decrypt(PyObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "data", NULL };
	char *dataBuffer;
	int dataLen;

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "s#", kwlist, &dataBuffer, &dataLen))
		return NULL;

	CL_Blob data(dataBuffer, dataLen);
	data.Rewind();
	sCipher.Decrypt(data, dataLen);

	return PyBytes_FromStringAndSize((const char *)data.GetData(), (Py_ssize_t)dataLen);
}


/** Vtable declaring MGA module methods. */
static PyMethodDef sMGA_Methods[] = {
	{	"host_lookup",					(PyCFunction)host_lookup,				METH_VARARGS | METH_KEYWORDS,	"host_lookup(str) -> str\n\nPerforms a forward or reverse DNS lookup given an IP/host name." },
	{	"get_network_interfaces",		(PyCFunction)get_network_interfaces,	METH_VARARGS | METH_KEYWORDS,	"get_network_interfaces() -> tuple\n\nReturns a list of dicts holding informations on all the available network interfaces." },
	{	"get_machine_uuid",				(PyCFunction)get_machine_uuid,			METH_NOARGS,					"get_machine_uuid() -> str\n\nGets machine unique UUID." },
	{	"save_xml",						(PyCFunction)save_xml,					METH_VARARGS | METH_KEYWORDS,	"save_xml(dict) -> str\n\nConverts given dictionary object in XML form and returns it as an (unicode) string." },
	{	"load_xml",						(PyCFunction)load_xml,					METH_VARARGS | METH_KEYWORDS,	"load_xml(str) -> dict\n\nLoads XML from given (unicode) string and returns a corresponding dictionary object." },
	{	"start_timer",					(PyCFunction)start_timer,				METH_VARARGS | METH_KEYWORDS,	"start_timer(seconds, callback, userdata) -> Deferred\n\nStarts a timer, so that callback gets called after specified amount of seconds. Returns a cancellable Deferred object." },
	{	"hash_password",				(PyCFunction)hash_password,				METH_VARARGS | METH_KEYWORDS,	"hash_password(password) -> str\n\nReturns the hashed version of given plain password." },
	{	"set_interpreter_timeout",		(PyCFunction)set_interpreter_timeout,	METH_VARARGS | METH_KEYWORDS,	"set_interpreter_timeout(timeout)\n\nSets timeout for current interpreter." },
	{	"lock",							(PyCFunction)lock,						METH_NOARGS,					"lock()\n\nAcquires the global MGA threads lock." },
	{	"unlock",						(PyCFunction)unlock,					METH_NOARGS,					"unlock()\n\nReleases the global MGA threads lock." },
	{	"_cleanup",						(PyCFunction)_cleanup,					METH_NOARGS,					"_cleanup()\n\nCleanup resources." },
	{	"set_default_idle_callback",	(PyCFunction)set_default_idle_callback,	METH_VARARGS | METH_KEYWORDS,	"set_default_idle_callback(callback)\n\nSets the default callback to be issued during client sync operations." },
	{	"checksum",						(PyCFunction)checksum,					METH_VARARGS | METH_KEYWORDS,	"checksum(buffer) -> int\n\nComputes a fast checksum of a buffer." },
	{	"get_application_log_path",		(PyCFunction)get_application_log_path,	METH_NOARGS,					"get_application_log_path() -> str\n\nReturns the user log path concatenated with the application name." },
	{	"_aes_set_key",					(PyCFunction)_aes_set_key,				METH_VARARGS | METH_KEYWORDS,	"_aes_set_key(key)\n\nSets AES cipher key." },
	{	"_aes_encrypt",					(PyCFunction)_aes_encrypt,				METH_VARARGS | METH_KEYWORDS,	"_aes_encrypt(data) -> data\n\nPerforms AES encryption on a block of data" },
	{	"_aes_decrypt",					(PyCFunction)_aes_decrypt,				METH_VARARGS | METH_KEYWORDS,	"_aes_decrypt(data) -> data\n\nPerforms AES decryption on a block of data." },
	{	NULL,							NULL,									0,								NULL }
};


/**
 *	Cleanup function to be called on module exit. Closes any connection to the MGA server previously enstablished.
 */
static void
MGA_Cleanup()
{
	{
		CL_AutoLocker locker(&MGA::gThreadsLock);
		MGA::gInitialized = false;
	}
	CL_Delete(sTranslator);
	sTranslator = NULL;
	CL_Dispatcher *dispatcher = MGA::gDispatcher;
	MGA::gDispatcher = NULL;
	if (Py_IsInitialized()) {
		Py_BEGIN_ALLOW_THREADS
		CL_Delete(dispatcher);
		Py_END_ALLOW_THREADS
	}
	else {
		CL_Delete(dispatcher);
	}
}


/**
 *	Main module initialization function. Automatically called by Python on module import.
 */
PyMODINIT_FUNC EXPORT
init_kongalib()
{
	PyObject *module;
	
	CL_Init();
	
	sTranslator = CL_New(CL_Translator);
	sTranslator->Load(CL_LANG_EN, sDefaultDictionary_CL_MESSAGES);
	sTranslator->Load(CL_LANG_EN, sDefaultDictionary_MGA_MESSAGES, false);
	
	MGA::gDispatcher = CL_New(CL_Dispatcher(1, 32));
	
	PyEval_InitThreads();
	Py_AtExit(&MGA_Cleanup);
	
	module = Py_InitModule3("_kongalib", sMGA_Methods,
		"MGA client module\n\n"
		"Allows to interact with an existing MGA server via TCP/IP.\n"
	);
	
	PyObject *parent = PyImport_AddModule("kongalib");
	sException = PyDict_GetItemString(PyModule_GetDict(parent), "Error");
	
	if (PyType_Ready(&MGA::DecimalType) < 0)
		return;
	Py_INCREF(&MGA::DecimalType);
	PyModule_AddObject(module, "Decimal", (PyObject *)&MGA::DecimalType);
	
	if (PyType_Ready(&MGA::ClientType) < 0)
		return;
	Py_INCREF(&MGA::ClientType);
	PyModule_AddObject(module, "Client", (PyObject *)&MGA::ClientType);
	
	if (PyType_Ready(&MGA::DeferredType) < 0)
		return;
	Py_INCREF(&MGA::DeferredType);
	PyModule_AddObject(module, "Deferred", (PyObject *)&MGA::DeferredType);
	
	if (PyType_Ready(&MGA::JSONEncoderType) < 0)
		return;
	Py_INCREF(&MGA::JSONEncoderType);
	PyModule_AddObject(module, "JSONEncoder", (PyObject *)&MGA::JSONEncoderType);
	
	if (PyType_Ready(&MGA::JSONDecoderType) < 0)
		return;
	Py_INCREF(&MGA::JSONDecoderType);
	PyModule_AddObject(module, "JSONDecoder", (PyObject *)&MGA::JSONDecoderType);
	
	if (PyType_Ready(&MGA::InterpreterType) < 0)
		return;
	Py_INCREF(&MGA::InterpreterType);
	PyModule_AddObject(module, "Interpreter", (PyObject *)&MGA::InterpreterType);
	
	MGA::InitJSON();
	MGA::InitInterpreter();
	MGA::InitUtilities();
	
	MGA::gInitialized = true;
	
	sMainThreadID = PyThreadState_Get()->thread_id;
	
	CL_AddPowerCallback(_power_callback);
}


/*@}*/
