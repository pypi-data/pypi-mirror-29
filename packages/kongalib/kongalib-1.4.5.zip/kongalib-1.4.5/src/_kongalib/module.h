/** @file mga/module/module.h
 *
 *		Python MGA module global header file.
 *
 *		$Revision: 27427 $
 *		$Date: 2018-01-19 11:58:53 +0100 (ven, 19 gen 2018) $
 *		$Author: lillo $
 *
 */

#ifndef __MGA_MODULE_H__
#define __MGA_MODULE_H__

#include "Python.h"
#include "marshal.h"

#include "yajl/yajl_parse.h"
#include "yajl/yajl_gen.h"

#include <ebpr/types.h>
#include <ebpr/system.h>
#include <ebpr/decimal.h>
#include <ebpr/timestamp.h>
#include <ebpr/socket.h>
#include <ebpr/dispatcher.h>
#include <ebpr/cipher.h>

#include <konga_client/client.h>
#include <konga_client/common.h>

#include <ebpr/messages.h>
#include <konga_client/messages.h>


#if defined(__GNUC__) || defined(__clang__)
	#define EXPORT		__attribute__((__visibility__("default")))
#else
	#define EXPORT
#endif

#define STRING_EXPAND(x)					#x
#define TO_STRING(x)						STRING_EXPAND(x)


namespace MGA
{

/**
 *	\brief Small type managing an MGA client instance
 *
 *	Wraps #MGA_Client and its functionalities to allow accessing a remote MGA server via Python.
 */
typedef struct ClientObject
{
	PyObject_HEAD
	
	ClientObject();
	
	MGA_Client		*fClient;				/**< The #MGA_Client object doing the real work behind the scene. */
} ClientObject;


/**
 *
 */
typedef struct DeferredObject
{
	PyObject_HEAD
	
	DeferredObject(ClientObject *client, PyObject *userData, PyObject *success, PyObject *error, PyObject *progress, PyObject *idle);
	~DeferredObject();
	
	static DeferredObject *Allocate(ClientObject *client, PyObject *userData, PyObject *success = NULL, PyObject *error = NULL, PyObject *progress = NULL, PyObject *idle = NULL);
	
	ClientObject	*fClient;
	PyObject		*fSuccess;
	PyObject		*fError;
	PyObject		*fProgress;
	PyObject		*fIdle;
	PyObject		*fUserData;
	volatile bool	fAborted;
	volatile bool	fExecuted;
	CL_Condition	fCondition;
} DeferredObject;


/**
 *	\brief Type describing the Python MGA.Decimal object
 *
 *	Wraps around the functionalities of a #CL_Decimal object to represent a decimal value in Python.
 */
typedef struct DecimalObject
{
	PyObject_HEAD

	DecimalObject() {}

	static DecimalObject *Allocate();
	
	CL_Decimal		fValue;					/**< The #CL_Decimal object associated to this Python MGA.Decimal object. */
} DecimalObject;


/**
 *
 */
typedef struct JSONEncoderObject
{
	PyObject_HEAD
	
	JSONEncoderObject();
	
	yajl_gen		fHandle;
	string			fEncoding;
} JSONEncoderObject;


/**
 *
 */
typedef struct JSONDecoderObject
{
	PyObject_HEAD
	
	JSONDecoderObject();
	
	yajl_handle		fHandle;
	string			fEncoding;
	string			fFileName;
} JSONDecoderObject;



/**
 *
 */
typedef struct InterpreterObject
{
	PyObject_HEAD
	
	InterpreterObject();
	~InterpreterObject();
	
	CL_Job				*fJob;
	volatile bool		fRunning;
	volatile bool		fExecute;
	bool				fHasCode;
	string				fFileName;
	string				fScript;
	CL_Mutex			fLock;
	CL_Condition		fCond;
	CL_Condition		fReady;
	volatile uint32		fStartTime;
	uint32				fTimeOut;
	PyThreadState		*fState;
	CL_Array<string>	fArgv;
	CL_Array<string>	fPath;
} InterpreterObject;



extern CL_RecursiveMutex gThreadsLock;
extern CL_Dispatcher *gDispatcher;
extern PyObject *gIdleCB;
extern volatile bool gInitialized;

extern PyTypeObject ClientType;
extern PyTypeObject DeferredType;
extern PyTypeObject DecimalType;
extern PyTypeObject JSONEncoderType;
extern PyTypeObject JSONDecoderType;
extern PyTypeObject InterpreterType;


extern string translate(MGA_Status error);

extern PyObject *setException(MGA_Status error_code, const string& error_msg = "");
extern PyObject *setException(MGA_Status error_code, CLU_Table *output);
extern PyObject *setException(MGA::ClientObject *client, MGA_Status result);

extern bool trackClient(MGA::ClientObject *client);
extern void untrackClient(MGA::ClientObject *client);
extern void trackInterpreter(MGA::InterpreterObject *interpreter);
extern void untrackInterpreter(MGA::InterpreterObject *interpreter);

extern int ConvertString(PyObject *object, string *string);
extern int ConvertDecimal(PyObject *object, DecimalObject **decimal);
extern PyObject *List_FromCLU(CLU_List *list);
extern CLU_List *List_FromPy(PyObject *object);
extern PyObject *Table_FromCLU(CLU_Table *table);
extern CLU_Table *Table_FromPy(PyObject *object);

extern void InitUtilities();
extern void InitJSON();
extern void InitInterpreter();

};


#endif
