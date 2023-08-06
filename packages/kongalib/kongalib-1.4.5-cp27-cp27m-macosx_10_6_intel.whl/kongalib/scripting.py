# -*- coding: utf-8 -*-
#
#	Konga Client library
#
#		Scripting support
#

from kongalib import InterpreterTimeout, Error, start_timer
from _kongalib import Interpreter, get_application_log_path, set_interpreter_timeout

import __builtin__
import sys
import os
import atexit
import io
import threading
import multiprocessing.connection
import logging



class ProxyLocker(object):
	def __init__(self):
		self.timeout = 0
		self.lock = threading.RLock()
	def __enter__(self):
		try:
			self.timeout = set_interpreter_timeout(0)
		except:
			self.timeout = 0
		self.lock.acquire()
	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.lock.release()
		try:
			set_interpreter_timeout(self.timeout)
		except:
			pass



class Proxy(object):
	def __init__(self):
		self.__conn = None
		self.__lock = ProxyLocker()

	def _initialize(self):
		conn_type = str(sys.argv.pop(1))
		address = str(sys.argv.pop(1))
		if conn_type == 'AF_INET':
			colon = address.rfind(':')
			address = (address[:colon], int(address[colon+1:]))
		logger.debug("[Proxy] init: %s" % repr(address))
		try:
			self.__conn = multiprocessing.connection.Client(address, conn_type)
		except:
			import traceback
			logger.error("[Proxy] init error: %s" % traceback.format_exc())
			raise
		logger.debug("[Proxy] connection established")
	
	def close(self):
		if self.__conn is not None:
			sys.stdout.flush()
			sys.stderr.flush()
			self.__conn.close()
			self.__conn = None
	
	def __getattr__(self, name):
		return MethodHandler(self.__conn, self.__lock, name)


proxy = Proxy()
def close_proxy():
	try:
		proxy.close()
	except:
		pass
atexit.register(close_proxy)
logger = logging.getLogger("script")


def timeout_handler():
	if proxy.builtin.handle_timeout():
		raise InterpreterTimeout



def init_interpreter(init_logging=True):
	if init_logging:
		logger.setLevel(logging.DEBUG)
		try:	os.makedirs(get_application_log_path())
		except:	pass
		formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s", datefmt='%a, %d %b %Y %H:%M:%S')
		handler = logging.FileHandler(os.path.join(get_application_log_path(), 'script.log'), 'w')
		handler.setLevel(logging.DEBUG)
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		logger.propagate = False
	logger.debug('init_interpreter')

	proxy._initialize()
	sys.stdout = ProxyStdOut()
	sys.stderr = ProxyStdErr()
# 	sys.stdout = io.TextIOWrapper(ProxyStdOut(), 'utf-8', line_buffering=True)
# 	sys.stderr = io.TextIOWrapper(ProxyStdErr(), 'utf-8', line_buffering=True)
	sys.stdin = ProxyStdIn()
	sys.prefix, sys.exec_prefix = proxy.builtin.get_prefixes()
	sys.is_kongalib_interpreter = True

	def excepthook(type, value, tb):
		import traceback
# 		sys.__stdout__.write('EXCEPTHOOK:\n%s' % '\n'.join(traceback.format_exception(type, value, tb)))
		tb = traceback.extract_tb(tb)
		def do_filter(entry):
			filename = entry[0].replace('\\', '/')
			if filename.endswith('kongalib/scripting.py') or filename.endswith('__script_host__.py'):
				return False
			return True
		tb = filter(do_filter, tb)
		proxy.builtin.print_exception(type.__name__, str(value), tb)
	sys.excepthook = excepthook



def exit_interpreter():
	logger.debug('exit_interpreter')
	# proxy.close()



class ProxyStdIn(io.StringIO):
	def readline(self, size=-1):
		return proxy.builtin.read_line()



class ProxyStdOut(io.StringIO):
	def write(self, text):
		proxy.builtin.write_stdout(str(text))
		return len(text)

	def flush(self):
		proxy.builtin.flush_stdout()



class ProxyStdErr(io.StringIO):
	def write(self, text):
		sys.__stderr__.write(str(text))
		try:
			proxy.builtin.write_stderr(str(text))
		except:
			pass
		return len(text)

	def flush(self):
		proxy.builtin.flush_stderr()



class MethodHandler(object):
	def __init__(self, conn, lock, name):
		self._conn = conn
		self._lock = lock
		self._name = name
	
	def __getattr__(self, name):
		return Method(self, name)



class Method(object):
	def __init__(self, handler, name):
		self.handler = handler
		self.name = name
	
	def __call__(self, *args, **kwargs):
		with self.handler._lock:
			# logger.debug('[Proxy] call: %s' % str((self.handler._name, self.name, args, kwargs)))
			self.handler._conn.send((self.handler._name, self.name, args, kwargs))
			# logger.debug('[Proxy] waiting reply: %s' % str((self.handler._name, self.name)))
			e, result = self.handler._conn.recv()
			# logger.debug('[Proxy] got reply: %s' % str((self.handler._name, self.name, result)))
			if e is None:
				return result
			errmsg, errno = e
			if errno is None:
				raise RuntimeError(e)
			else:
				raise Error(errno, errmsg)



class ServerProxy(object):
	CACHE = []
	LOCK = threading.RLock()

	def __init__(self):
		self.ready = threading.Event()
		self.quit = False
		self.handlers = {}
		# try:
		# 	self.listener = multiprocessing.connection.Listener(family='AF_INET')
		# except:
		self.listener = multiprocessing.connection.Listener()
	
	def start(self):
		self.quit = False
		self.ready.clear()
		start_timer(0, lambda dummy: self.run())

	def stop(self):
		self.quit = True
		self.ready.wait()
		with ServerProxy.LOCK:
			ServerProxy.CACHE.append(self)

	def run(self):
		logger.debug("[ServerProxy] run")
		try:
			conn = self.listener.accept()
			logger.debug("[ServerProxy] got proxy")
			while not self.quit:
				if conn.poll(0.1):
					data = conn.recv()
					handler, name, args, kwargs = data
					# logger.debug("[kongaprint:%s] %s(%s)" % (handler, name, ', '.join([ repr(arg) for arg in args ] + [ '%s=%s' % (key, repr(value)) for key, value in kwargs.iteritems() ])))
					func = getattr(self.handlers[handler], name)
					try:
						result = (None, func(*args, **kwargs))
					except Exception, e:
						import traceback
						logger.error("[ServerProxy] method error: %s" % traceback.format_exc())
						# sys.__stderr__.write('SCRIPTING EXCEPTION:\n%s\n' % traceback.format_exc())
						if isinstance(e, Error):
							errno = e.errno
						else:
							errno = None
						result = ((str(e), errno), None)
					finally:
						conn.send(result)
		except IOError:
			import traceback
			logger.error("[ServerProxy] IOError: %s" % traceback.format_exc())
		except EOFError:
			pass
		finally:
			logger.debug("[ServerProxy] exiting")
			self.ready.set()

	@classmethod
	def create(cls, handlers):
		with cls.LOCK:
			if len(cls.CACHE) == 0:
				ServerProxy.CACHE.append(ServerProxy())
			proxy = ServerProxy.CACHE.pop()
			proxy.handlers = handlers
			return proxy




class BuiltinHandler(object):
	def __init__(self):
		self.__interpreter = None
	
	def _set_interpreter(self, interpreter):
		self.__interpreter = interpreter
	
	def _get_interpreter(self):
		return self.__interpreter
	
	def write_stdout(self, text):
		sys.__stdout__.write(text)
	
	def write_stderr(self, text):
		sys.__stderr__.write(text)

	def flush_stdout(self):
		pass

	def flush_stderr(self):
		pass
	
	def read_line(self):
		sys.__stdin__.readline()
	
	def get_prefixes(self):
		return os.getcwd(), os.getcwd()
	
	def format_exception(self, type, value, tb):
		import traceback
		text = [ 'Traceback (most recent call last):\n' ] + traceback.format_list(tb) + traceback.format_exception_only(type, value)
		return ''.join(text)
	
	def print_exception(self, type, value, tb):
		print self.format_exception(type, value, tb)
	
	def get_time_left(self):
		if self.__interpreter is not None:
			return self.__interpreter.get_time_left()
		return 0
	
	def set_timeout(self, timeout=0):
		if self.__interpreter is not None:
			return self.__interpreter.set_timeout(timeout)
	
	def handle_timeout(self):
		raise InterpreterTimeout
	
	def noop(self):
		pass



def execute(script=None, filename=None, argv=None, path=None, timeout=0, handlers=None, interpreter=None):
	if (script is None) and (filename is None):
		raise ValueError('Either script or filename must be specified')
	logger.debug("[ServerProxy] launching...")
	if filename is None:
		filename = '__script__'
	if argv is None:
		argv = [ filename ]
	if interpreter is None:
		interpreter = Interpreter()
	logger.debug("[ServerProxy] instantiating ServerProxy")
	_handlers = { 'builtin': BuiltinHandler() }
	_handlers.update(handlers or {})
	_handlers['builtin']._set_interpreter(interpreter)
	p = ServerProxy.create(_handlers)
	logger.debug("[ServerProxy] listener address is: %s" % repr(p.listener.address))

	conn_type = multiprocessing.connection.address_type(p.listener.address)
	if conn_type == 'AF_INET':
		address = '%s:%d' % tuple(p.listener.address)
	else:
		address = p.listener.address
	argv.insert(1, conn_type)
	argv.insert(2, address)
	p.start()
	logger.debug("[ServerProxy] waiting proxy: %s" % repr(argv))

	try:
# 		import time
# 		start = time.time()
		interpreter.execute(script, filename, argv, path or [], timeout)
# 		print "Script execution time:", time.time() - start
	except Exception, e:
		import traceback
		logger.debug("[ServerProxy] execute exception: %s" % traceback.format_exc())
		raise
	finally:
		logger.debug("[ServerProxy] done")
		p.stop()
		_handlers['builtin']._set_interpreter(None)

