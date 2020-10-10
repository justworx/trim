#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import sys, time, traceback, locale, json #, threading
try:
	import thread
except:
	import _thread as thread


#
# VERSION
#  - The official version of the `trix` package is currently
#    "Version: zero; rough draft five; under construction".
#
VERSION = 0.0000

#
# AUTO_DEBUG
#  - Controls the formatting of raised Exceptions.
#  - The trix package is very complex, making it really hard to
#    track down bugs. This formatting of exceptions helps a lot.
#  - If you want exceptions the old-fashioned way, set it False.
#
AUTO_DEBUG = True #True/False

#
# CONFIG / CACHE
#  - Default root directory for storage of config and cache files.
#  - These are the defaults for many *nix systems, and should work
#    for Windows. I'm hoping, though, that I'll learn of better
#    values for Windows before too much longer. 
#
DEF_CONFIG = "~/.config/trix"
DEF_CACHE  = "~/.cache/trix"

#
# LOGLET FILE PATH/NAME
#
DEF_LOGLET = "./loglet"

#
# DEF_LOCALE - Under Construction
#  - This default locale setting is here for any strange and unusual
#    cases in which it might need to be switched to a specific value.
#    The default specified below causes trix to use the locale set as 
#    the default for the system on which this software is running. 
#    For most cases, unless you *really* know what you're doing, it's
#    probably best to leave it set to ''.
#
#  - IMPORTANT: Many trix features make use of threading, so typically
#               `locale.setlocale` must not be reset over the life of 
#               the process. However, a thread-safe system for getting
#               alternate locale data is under construction. We'll see
#               how that goes. (See: `trix.loc()`, below.)
#
DEF_LOCALE = ''

# Set the locale as specified above.
locale.setlocale(locale.LC_ALL, DEF_LOCALE)


#
# DEF_ENCODE
#  - The default encoding for the trix package is now determined by
#    the locale module. I don't know if that method can fail,
#    but if it does, 'utf_8' is used as a backup.
#  - This change is experimental. DEF_ENCODE used to be set directly
#    to 'utf_8'. I don't expect this to cause any problems, but in
#    the event it does, I'll switch back to a hard-coded default of
#    'utf_8'.
#

DEF_ENCODE = locale.getpreferredencoding() or 'utf_8'

try:
	DEF_LANG = locale.getlocale()[0].split('_')[0]
except:
	DEF_LANG = 'en'


#
# DEF_NEWL
#  - The default newline sequence.
#
DEF_NEWL = '\r\n'


#
# DEFAULT INDENTATION
#  - Number of spaces to use when indenting formatted text, tab
#    replacement, etc...
#
DEF_INDENT = 2




#
#
#
# TRIX CLASS
#
#
#
class trix(object):
	"""Utility, debug, import; object, thread, and process creation."""
	
	# USER CLASS VARS
	Logging = 0 #-1=print; 0=None; 1=log-to-file
	
	
	# PRIVATE CLASS VARS
	__m = __module__
	__mm = sys.modules
	__od = {}
	#__tid = threading.current_thread().ident
	#__tname = threading.current_thread().name


	
	# -----------------------------------------------------------------
	#
	#
	# OBJECT CREATION
	#  - This section defines a set of trix methods that create objects,
	#    or support the creation of objects in general as specified by
	#    classmethod arguments, and utilities which support the creation
	#    of objects.
	#
	#
	# -----------------------------------------------------------------
	
	#
	#
	# INNER PATH (Independent of subpackages)
	#
	#
	@classmethod
	def innerpath(cls, innerPath=None):
		"""
		Returns `innerPath` prefixed with containing packages.
		
		If `innerPath` is not specified, the string "trix" is returned,
		prefixed by any containing directories.
		
		If the `trix` package is contained in superordinate packages, 
		they will be dot-prefixed in the order correct for import.
		
		When an `innerPath` string value is specified, it is appended to
		the resulting value.
		
		EXAMPLES:
		>>> #
		>>> # Calling trix.innerpath with no containing pacakges and no 
		>>> # argument:
		>>> #
		>>> trix.innerpath()
		'trix'
		>>>
		>>> #
		>>> # Calling trix.innerpath from a containing package named
		>>> # 'myproject':
		>>> #
		>>> myproject.trix.innerpath()
		'myproject.trix'
		>>>
		>>> #
		>>> # Calling trix.innerpath with a containing package and an
		>>> # argument:
		>>> #
		>>> myproject.trix.innerpath('fs.dir')
		'myproject.trix.fs.dir'
		>>>
		
		This classmethod exists stand-alone as a basic utility. It is 
		part of a larger set of classmethods within the trix class.
		
		NOTE:
		Specifying a non-existent subpackage or module will return the
		path. No checking is done to cause an exception in such cases.
		Use of other import methods such as `trix.module`, `trix.nmodule`,
		`trix.value`, `trix.nvalue`, `trix.create`, or `trix.ncreate`,
		will raise an appropriate exception if the existing module, 
		object, or class does not exist.
		
		"""
		p = '.%s' % (innerPath) if innerPath else ''
		if cls.__m:
			return "%s%s" % (cls.__m, p)
		else:
			return innerPath
	
	
	#
	#
	# MODULE (Independent)
	#
	#
	@classmethod
	def module (cls, path):
		"""
		Returns a module given a string `path`. The specified module may
		be external to the trix package.
		
		This methods exists mainly to support the `trix.nmodule` method,
		described below, but could be of use in any project as a way to
		“load on demand,” which may be especially useful in cases
		where such values as may be needed are only rarely needed.
		
		Additionally, the trix.module method might be of use in cases 
		where more than one module may be selected as a choice. For 
		example, python provides a variety of database classes, and the 
		trix.data.database class allows use of config files to determine
		the DBMS for use.
		
		#
		# EXAMPLE:
		#
		>>> import trix
		>>> dbms = trix.module("sqlite3")
		>>> dbms
		<module 'sqlite3' from '/usr/lib/python...>
		>>>
		
		"""
		try:
			return cls.__mm[path]
		except KeyError:
			__import__(path)
			return cls.__mm[path]
	
	
	#
	#
	# N-MODULE (Independent)
	#
	#
	@classmethod
	def nmodule(cls, innerPath):
		"""
		Like `module`, but pass the inner path instead of full path.
		
		Use `trix.nmodule` to import items from within the `trix` package
		only when you need to import objects by their inner paths.
		
		The `trix.nmodule` method works like `trix.module`, but it must
		be given the path to a module *within* the trix package. Do not 
		prefix the string `path` with the dot-separated path of containing
		any packages, or the operation will fail.
		
		Likewise, prepending `trix` would also cause the operation to 
		fail. The `innerPath` string argument must be a dot-separated path 
		starting within the `trix` package.
		
		#
		# EXAMPLES:
		#
		>>> #
		>>> # Calling trix.nmodule when trix is the root package
		>>> #
		>>> import trix
		>>> trix.nmodule('fs.dir')
		<module 'trix.fs.dir' from '/home/ME/trix/...>
		>>>
		>>> #
		>>> # Calling trix.nmodule where the trix package is subordinate
		>>> # to a containing package called `myproject`.
		>>> #
		>>> from mypackage.trix import *
		>>> trix.nmodule('fs.dir')
		<module 'mypackage.trix.fs.dir' from '/home/ME/mypackage/...>
		>>>
		
		The `trix.nmodule` method provides an easy way to import modules 
		from the trix package without worrying about the depth or 
		ordering of potential superordinate packages.
		
		When you import modules from trix using the `trix.nmodule` 
		method, the trix.innerpath() method prefixes any containing 
		package names. Changes to the names of containing packages,
		would cause no problems for calls to trix.nmodule().
		
		"""
		return cls.module(cls.innerpath(innerPath))
	
	
	#
	#
	# VALUE (Independent)
	#
	#
	@classmethod
	def value(cls, pathname, *args, **kwargs):
		"""
		Returns an object as specified by `pathname` and arguments.
		
		Returns a module, class, function, or value, as specified by the
		string argument `pathname`. If additional *args are appended, 
		they must name a class, method, function, or value defined within 
		the object specified by first argument. A tupel is returned.
		
		>>> trix.value('socket',"AF_INET","SOCK_STREAM")
		(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>)
		>>>
		
		"""
		
		try:
			return __builtins__[pathname](*args, **kwargs)
		except:
			pass
		
		try:
			mm = mc = cls.module(pathname)
		except:
			# If `pathname` points to a module or function, split it and 
			# load its containing module.
			pe = pathname.split('.')
			
			# only pop the last item if there's more than one element
			nm = pe.pop() if len(pe) > 1 else None
			
			# get the module
			mm = cls.module('.'.join(pe))
			
			# Get the last object specified by `pathname`; This object must
			# be either a module or a class, not a function or other value.
			# If no other args are specified, this is the final result.
			mc = mm.__dict__[nm] if nm else mm
		
		# If there are no *args, return the last [module or class] object
		# specified by `pathname`.
		if not args:
			return mc
		
		# if args are specified, forget about the mod/cls item and just
		# return any requested values from it.
		rr = []
		for v in args:
			try:
				rr.append(mc.__dict__[v])
			except KeyError:
				if 'default' in kwargs:
					return kwargs['default']
				return ()
			except NameError:
				raise
		
		# If one *args value was specified, return it. If more than one
		# was specified, return them as a tuple.
		if len(rr) == 1:
			return rr[0]
		return tuple(rr)
	
	
	#
	#
	# N-VALUE (Independent)
	#
	#
	@classmethod
	def nvalue(cls, pathname, *a, **k):
		"""
		Like `trix.value`, but pass the inner path instead of full path.
		
		The `trix.nvalue` classmethod is a shortcut for obtaining objects
		from a trix subpackage given a path to the object.
		
		#
		# EXAMPLE
		#
		>>> #
		>>> # Load a base-64 encoder/decoder into variable `b64` and use
		>>> # it to encode bytes, then decode them again.
		>>> #
		>>> b64 = trix.nvalue("util.compenc.b64")
		>>> b64.encode(b"A")
		b'QQ=='
		>>> b64.decode(b'QQ==')
		b'A'
		>>>
		
		"""
		
		try:
			return cls.value(cls.innerpath(pathname), *a, **k)
		except KeyError as kex:
			try:
				return __builtins__[pathname]
			except Exception as ex:
				raise type(ex)(ex.args, 'err-nvalue-fail', xdata(
						pathname=pathname
					))
	
	
	#
	#
	# CREATE (Independent)
	#  - This method is thechnically independent of subpackages, but 
	#    is only ever used to create objects from subclasses. In this
	#    sense, it could be viewed as being "Dependent." However, as
	#    the classmethod itself depends on no subordinate packages, 
	#    it is technically independent.
	#
	#
	@classmethod
	def create(cls, modpath, *a, **k):
		"""
		Create and return an object specified by argument `modpath`. 
		
		The dot-separated path must start with the path to the desired
		module. It must be suffixed with the name of a class defined in 
		the specified module. (Eg, 'package.subpackage.module.ClassName')
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		
		>>> sock = trix.create("socket.socket")
		>>> sock
		<socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>
		>>>
		
		"""
		
		p = modpath.split(".")
		m = p[:-1] # module
		o = p[-1]  # object
		
		try:
			T = None
			if m:
				mm = cls.module(".".join(m))
				T  = mm.__dict__[o]
			else:
				T = __builtins__[o]
		
		except KeyError as ex:
			try:
				otype = type(trix.value(modpath)).__name__
				if otype == 'module':
					reason = "invalid-create-type"
					message = "cannot-create-module"
				raise TypeError("Can't trix.create a module.")
			except TypeError:
				raise TypeError('create-fail', xdata(path=modpath, 
						otype=otype, mod=".".join(m), obj=o, T=T, 
						error="err-create-fail", reason=reason, message=message
					))
			except KeyError:
				reason=message=otype = "Unknown"
				raise KeyError('create-fail', xdata(path=modpath, 
						otype=otype, mod=".".join(m), obj=o, T=T, 
						error="err-create-fail", reason=reason, message=message
					))
		
		try:
			return T(*a, **k)
		except BaseException as ex:
			raise type(ex)(
					xdata(path=modpath, a=a, k=k, obj=o, T=type(o)
				))
	
	
	#
	#
	# N-CREATE  (Independent)
	#  - Create an object given path from trix subpackages.
	#  - This method is thechnically independent of subpackages, but 
	#    is only ever used to create objects from subclasses. In this
	#    sense, it could be viewed as being "Dependent." However, as
	#    the ncreate classmethod itself depends on no subordinate
	#    packages it is, technically, independent.
	#
	#
	@classmethod
	def ncreate(cls, innerPath, *a, **k):
		"""
		Create and return an object specified by argument `innerPath`.
		The dot-separated path must start with the path to the desired
		module *within* this package (but NOT prefixed with the name of
		this package). It must be prefixed with a name of a class defined
		in the specified module. Eg, 'subpackage.theModule.TheClass'
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		
		USE: The ncreate() method is used from within this package. For 
		     normal (external) use, use the create() method.
		
		>>> trix.ncreate("util.console.Console").console()
		
		"""
		a = a or []
		k = k or {}
		return cls.create(cls.innerpath(innerPath), *a, **k)
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# FILE SYSTEM FEATURES
	#  - This section defines a small set of features that facilitate
	#    file system operations.
	#  - The `path` classmethod, in particular, exposes all of the
	#    trix file system operations in one place consistent interface.
	#    Reading and writing files, compressed files, and archives has
	#    never been easier.
	#  
	#
	# -----------------------------------------------------------------
	
	
	#
	#
	# INNER F-PATH (Independent)
	#
	#
	@classmethod
	def innerfpath(cls, innerFPath=None):
		"""
		Return a full file path from within the trix package.
		
		>>> import trix
		>>> trix.innerfpath('app/config/en.conf')
		'trix/app/config/en.conf'
		>>> 
		
		"""
		ifp = cls.innerpath().split('.')
		if innerFPath:
			ifp.append(innerFPath)
		return "/".join(ifp)
	
	
	#
	#
	# PATH (Dependent)
	#
	#
	@classmethod
	def path(cls, path=None, *a, **k):
		"""
		Return the `trix.fs.Path` object for `path`.
		
		The `trix.fs.Path` class wraps a file system objects, providing
		a reasonably consistent interface to information and access to
		content, though tar and zip files contain an additional layer
		of features to facilitate their needs. For gzip and bzip files,
		the interface to their content is the same as for text files.
		All other file types are stored and accessed as bytes.
		
		EXAMPLE 1:
		>>> #
		>>> # Create a path object; Create a file reader from that
		>>> # object.
		>>> # 
		>>> import trix
		>>> r = trix.path("trix/LICENSE").reader()
		>>> r.readline()
		b'                    GNU AFFERO GENERAL PUBLIC LICENSE\n'
		>>> r.readline()
		b'                       Version 3, 19 November 2007\n'
		>>> 
		
		
		If argument `path` points to a directory, a `trix.fs.Dir` object 
		(which is based on fs.Path) is returned instead.

		EXAMPLE 2:
		>>> #
		>>> # Create a path object that wraps a directory.
		>>> # 
		>>> import trix
		>>> trixpath = trix.path(trix.innerpath())
		>>> d = trix.path(trixpath)
		>>> d.ls()

		EXAMPLE 3:
		>>> #
		>>> # A shortcut for the above...
		>>> #
		>>> import trix
		>>> trix.path(trix.innerpath()).ls()
		['util', 'app', '__init__.py', 'NOTES', 'fmt', 'x', 'fs', 'data', 
		'scripts', 'net', 'README.md', 'LICENSE', 'test', '__pycache__', 
		'.gitignore', '__main__.py', '.git']
		>>>
		
		"""
		try:
			p = cls.__FPath(path, *a, **k)
		except:
			# requires full module path, so pass through innerpath()
			cls.__FPath = cls.module(cls.innerpath('fs')).Path
			p = cls.__FPath(path, *a, **k)
		
		return p.dir() if p.isdir() else p
	
	
	#
	#
	# N-PATH (Dependent)
	#
	#
	@classmethod
	def npath(cls, innerFPath=None, *a, **k):
		"""
		Return a `trix.fs.Path` for a file-system object within the trix 
		directory.
		
		>>> #
		>>> # Create a reader and read a line.
		>>> #
		>>> r = trix.npath("app/config/app.conf").reader(encoding='utf8')
		>>> r.readline()
		'#\n'
		>>> 
		
		"""
		return cls.path(cls.innerfpath(innerFPath), *a, **k)
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# THREADS, PROCESSES
	#  - This section defines a set of features that facilitate working
	#    with threads, 
	#  - The `path` classmethod, in particular, exposes all of the
	#    trix file system operations in one place consistent interface.
	#    Reading and writing files, compressed files, and archives has
	#    never been easier.
	#  
	#
	# -----------------------------------------------------------------
	
	
	#
	#
	# START (Independent)
	#
	#
	@classmethod
	def start (cls, x, *a, **k):
		"""
		Start callable object `x` in a new thread, passing any given 
		*args and **kwargs.
		
		EXAMPLE:
		>>>
		>>> def test():
		...   print("Testing 1 2 3");
		>>>
		>>> thread_id = trix.start(test)
		Testing 1 2 3
		>>>
		
		The `trix.start` method is provided as a low-level convenience. 
		It is used by the `trix.util.runner.Runner` class, a higher-level
		class with many more features. See the `trix.util.runner` module.
		
		The `trix.start` method returns the thread ID.
		
		"""
		try:
			return thread.start_new_thread(x, a, k)
		except:
			pass
	
	
	
	#
	#
	# PID (Independent)
	#
	#
	@classmethod
	def pid(cls):
		"""
		Return the id for this process.
		
		>>> trix.pid()
		15231
		>>>
		
		"""
		try:
			return cls.__pid
		except:
			import os
			cls.__pid = os.getpid()
			return cls.__pid
	
	
	#
	#
	# POPEN (Dependent)
	#
	#
	@classmethod
	def popen (cls, cmd, *a, **k):
		"""
		Open a subprocess and return a Popen object created with the given
		args and kwargs. This functions exactly as would calling the popen
		function directly, except that stdout and stderr are enabled by 
		default.
		
		The return value is a Popen object. Use its communicate() method
		to read results of the command.
		
		KWARGS REFERENCE:
		bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, 
		preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None,
		universal_newlines=False, startupinfo=None, creationflags=0
		
		>>> import trix
		>>> tp = trix.popen("ps").communicate()
		>>> print(tp[0].decode(trix.DEF_ENCODE))
		  PID TTY          TIME CMD
		13766 pts/4    00:00:00 bash
		15259 pts/4    00:00:00 python3
		15261 pts/4    00:00:00 ps
		>>>
		
		"""
		
		try:
			m = cls.__sp
		except:
			m = cls.__sp = cls.module("subprocess")
		
		# set defaults and run the process
		k.setdefault("stdout", m.PIPE)
		k.setdefault("stderr", m.PIPE)
		try:
			return m.Popen(cmd, *a, **k)
		except FileNotFoundError:
			
			try:
				cmd = cls.__shlex.split(cmd)
			except:
				cls.__shlex = cls.module('shlex')
				cmd = cls.__shlex.split(cmd)
			
			#cmd = cmd.split()
			
			return m.Popen(cmd, *a, **k)
	
	
	#
	#
	# PROCESS
	#
	#
	@classmethod
	def process(cls, path, *a, **k):
		"""
		Launch and use an independent process.
		
		Pass a dot-separated string, `path`, specifying a class to be 
		instantiated and run within a separate process. Specify any 
		arguments and/or keyword arguments needed for the creation and 
		operation of the object.
		
		Calling `trix.process` is much like calling `trix.ncreate`. Pass 
		the object's full dot-separated python path, appending arguments 
		and keyword args as required or needed.
		
		A `trix.util.process.Process` object will be returned to the
		calling process (the terminal or python script from which the 
		remote process is being launched).
		
		Store the return value so that you may control the remote process and receive any data which may result of its operation.
		
				>>> p = trix.process("trix.net.server.Server", 9999)
		
		
		Pass a class `path` and any needed args/kwargs. An object of type 
		`trix.util.process.Process` is returned. Call the returned Process 
		object's `launch` method passing a method name (string) and any 
		additional args/kwargs (or no params, if the constructor of the
		object contained in the remote process starts processing on its 
		own).
		
				>>> p.launch('run')
		
		
		The trix.process() method supports trix.nprocess(), which accepts
		the same arguments (but, of course, with the path leading to a
		module in the set of trix subpackages, specifying a full path to 
		the required class definition.
		
		#
		# EXAMPLE:
		# It is important to note that the trix.net.server.Server class
		# defaults to an "echo" server. Unless overridden, whatever data 
		# is transmitted to the Server will be immediately echoed back to 
		# the sender.
		# 
		>>> #
		>>> # Start by defining a process that runs a basic echo server.
		>>> # The `Server` class requires specification of a port argument
		>>> # on which it will listen for requests. (In this case, 9999.)
		>>> #
		>>> p = trix.process("trix.net.server.Server", 9999)
		>>>
		>>> #
		>>> # Launch the process, calling the `Server` object's `run`
		>>> # method.
		>>> #
		>>> p.launch('run')
		>>>
		>>> #
		>>> # Create a `Connect` object to transmit data to the Server
		>>> # on port 9999, then write to the server.
		>>> #
		>>> c = trix.create("trix.net.connect.Connect", 9999)
		>>> c.write("Test")
		>>>
		>>> # read the response
		>>> c.read()
		>>>
		>>> # end the remote process
		>>> p.stop()
		>>>
		
		REFERENCE:
		The Process class is comlicated, and is packed with features. See 
		the `trix.util.process.Process` module's help for more detailed 
		documentation.
		
		>>> from trix.util.process import *
		>>> help(Process)
		
		"""
		#
		# REM! `path` is the module.class to launch within the `Process`.
		#  - In the code below, the ncreate call creates and returns a
		#    Process object that has not yet been "launched," or rather,
		#    the process won't begin operation until the p.launch() method
		#    has been called.
		#
		return cls.ncreate("util.process.Process", path, *a, **k)
	
	
	#
	#
	# N-PROCESS
	#
	#
	@classmethod
	def nprocess(cls, innerPath, *a, **k):
		"""
		Launch and use an independent process.
		
		This method works exactly like `process` (above), but given the
		remote object's "inner path," rather than its full path. That is
		to say, the `innerPath` arg is expanded to be the full dot
		separated path that to the object that will be launched by 
		`cls.process()`.
		
		#
		# SPECIFICALLY:
		#
		When calling `trix.process`, the full dot-separated path to the 
		object being run in the remote process is given:
		
				>>> p = trix.process("trix.net.server.Server", 9999)
		
		Here, though, in `trix.nprocess`, only the inner path should be
		specified:

				>>> p = trix.nprocess("net.server.Server", 9999)
		
		#
		# EXAMPLE
		#
		>>>
		>>> # Create a "local" process object pointer `p`.
		>>> p = trix.nprocess("net.server.Server", 9999).launch('run')
		>>>
		>>> # Check the local Process object's condition
		>>> p.display()
		>>>
		>>> # Check the remote Process object's condition
		>>> p.rdisplay() # remote display
		>>>
		>>> # TEST: Connect, to transmit data to the Server
		>>> c = trix.ncreate("net.connect.Connect", 9999)
		>>> c.write("Test")
		4
		>>>
		>>> # read the response
		>>> c.read()
		'Test'
		>>>
		>>> # when finished, end the remote process
		>>> p.stop() # end the remote process
		"""
		#
		# The `innerPath` arg is expanded to be the full module.class 
		# path that will be launched by `cls.process()`.
		#
		return cls.process(cls.innerpath(innerPath), *a, **k)
	
	
	#
	#
	# CALL-X
	#
	#
	@classmethod
	def callx (cls, cmd=None, **k):
		"""
		Call a system executable.
		
		The `callx` module makes it easy to retrieve the results of calls
		to system executables and provides result manipulation and display
		by returning the result in the most appropriate propx object.
		
		There are two ways to use callx to open: 
		 * call system executables directly
		 * call a trix cline handler using the "cline" keyword argument
		
		EXAMPLE:
		>>>
		>>> from trix import *
		>>> ps = trix.callx("ps")
		>>>
		>>> #
		>>> # Get the result text:
		>>> #
		>>> ps.text() 
		'  PID TTY          TIME CMD\n13766 pts/4    00:00:00 bash\n16203 pts/4    00:00:00 python3\n16205 pts/4    00:00:00 ps\n'
		
		MORE:
		More documentation is available in the `callx` module.
		>>>
		>>> from trix.util.callx import *
		>>> help(callx)
		>>>
		
		"""
		return cls.ncreate('util.callx.callx', cmd, **k)
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# CONFIGURATION / JSON
	#  - This section defines a set of features that facilitate working
	#    configuration files, which can be read as JSON or ast-parsable
	#    text files.
	#  
	#
	# -----------------------------------------------------------------
	
	
	#
	#
	# CONFIG
	#
	#
	@classmethod
	def config(cls, config=None, **k):
		"""
		Read and return a config file or dict.
		
		The `config` classmethod is the simplest of a set of methods that
		make it easy to generate, retrieve, and store configuration data.
		
		If `config` is given as a dict, the dict is updated with any 
		given keyword arguments and returned immediately.
		
		EXAMPLE:
		>>>
		>>> # Return a simple configuration by passing a dict and,
		>>> # optionally, keyword arguments.
		>>>
		>>> import trix
		>>> trix.config()
		{}
		>>> 
		>>> trix.config({'a':1, 'b':9, 'c':4})
		{'a': 1, 'b': 9, 'c': 4}
		>>> 
		>>> trix.config({'a':1, 'b':9, 'c':4}, d="Light")
		{'a': 1, 'b': 9, 'c': 4, 'd': 'Light'}
		>>> 

		
		If `config` is the path to a JSON or ast-parsable text file, the
		file is parsed and the resulting structure is returned as a dict.
		
		NOTE: In this case, any keyword args are passed to the JConfig 
		      constructor.
		
		EXAMPLE:
		>>>
		>>> # Return a configuration stored within a file.
		>>>
		>>> trix.config("~/trix/app/config/example.conf")
		{'A': 'Alpha', 'B': 'Bet'}
		>>> 
		>>> # 
		>>> # NOTE:
		>>> #  - Keyword args are passed to the JConfig constructor.
		>>> #    Pass only file-related keyword arguments when loading  
		>>> #    config from a file.
		>>> #  - Inappropriate keyword arguments could cause invalid
		>>> #    results, or damage to existing config files.
		>>> # 
		>>> 
		>>> import trix
		>>> trix.config(None, x=9)
		{'x': 9}
		>>> 
		>>> trix.config(x=9)
		{'x': 9}
		>>> 
		>>> trix.config({'y':'x'}, y="X") # kwargs replace dict keys
		{'y': 'X'}
		>>> 
		
		"""
		if config == None:
			return dict(k)
		try:
			# by dict 
			config.update(**k)
		except AttributeError:
			# by path...
			jconf = cls.jconfig(config, **k)
			config = jconf.obj
		return config
	
	
	#
	#
	# N-CONFIG (Dependent)
	#
	#
	@classmethod
	def nconfig(cls, config=None, **k):
		"""
		Read and return a config file or dict.
		
		The `trix.nconfig` classmethod works the same as `trix.config`,
		but file paths must be given as partial paths starting within the
		trix package directory.
		
		>>> # 
		>>> # See trix.config, above, for more usage examples.
		>>> # 
		>>> import trix
		>>> trix.nconfig("app/config/example.conf")
		>>>
		
		"""
		if config == None:
			return dict(k)
		if isinstance(config, dict):
			config.update(k)
			return config
		return cls.config(trix.innerfpath(config), **k)
	
	
	#
	#
	# J-CONFIG
	#
	#
	@classmethod
	def jconfig(cls, filepath, **k):
		"""
		Pass string `filepath` to a JSON (or ast-parsable) config file.
		 
		Optional `default` kwarg identifies file path containing default 
		contents for a new config file in case no file exists at 
		`filepath`. Use `ndefault` kwarg instead for the internal path
		(within the trix directory) to a default file.
		
		A `util.JConfig` object is returned.
		
		NOTES:
		 * The default path should point to a static default config file
		   (in ast or json format).
		 * If default path is given, affirm defaults to "touch".
		 * Be careful that your default filepath is not unintentionally
		   set to the same path as the `filepath` argument, or your
		   original default file may be overwritten.
		
		EXAMPLE:
		>>>
		>>> import trix
		>>> jc = trix.jconfig(trix.innerfpath("app/config/example.conf"))
		>>> print (jc.config)
		{'A': 'Alpha', 'B': 'Bet'}
		>>>
		
		"""
		default = k.get('default', cls.npath(k.get('ndefault')).path)
		k['default'] = default
		
		#
		# This should protect against unintentional overwriting of the 
		# default file.
		#
		if default and (default == filepath):
			raise ValueError("Matching target and default paths.", xdata(
					default=default, filepath=filepath, k=k
				))
		
		m = cls.nmodule("util.jconfig")
		return m.JConfig(filepath, **k)
	
	
	#
	#
	# J-PARSE
	#
	#
	@classmethod
	def jparse(cls, jsonstr, **k):
		"""
		Parse json to object.
		
		>>> import trix
		>>> trix.jparse('{"a": 1, "b": 9, "c": 4}')
		{'a': 1, 'b': 9, 'c': 4}
		>>>
		
		"""
		try:
			return json.loads(jsonstr)
		except TypeError:
			k.setdefault('encoding', DEF_ENCODE)
			return json.loads(jsonstr.decode(**k))
	
	
	#
	#
	# ---- GENERAL UTILITY --------------------------------------------
	#
	#
	
	#
	#
	# K-COPY
	#
	#
	@classmethod
	def kcopy(cls, d, keys):
		"""
		Copy `keys` from `d`; return in a new dict.
		
		Creates a subset of dict keys in order to select only desired 
		keyword args before passing to functions and methods. 
		
		Argument `keys` may be passed as a space-separated string, but 
		this won't work in all situations. It's safer to pass the `keys` 
		as a list object.
		
		The original dict is never altered by `kcopy`.
		
		EXAMPLE:
		>>> 
		>>> import trix
		>>> d = dict(a=1, b=9, c=4)
		>>> trix.kcopy(d, "b")
		{'b': 9}
		>>> trix.kcopy(d, ['a', 'c'])
		{'a': 1, 'c': 4}
		>>> d
		{'a': 1, 'b': 9, 'c': 4}
		>>> 
		
		"""
		
		try:
			keys=keys.split()
		except:
			pass
		return dict([[k,d[k]] for k in keys if k in d])
	
	
	#
	#
	# K-POP
	#
	#
	@classmethod
	def kpop(cls, d, keys):
		"""
		Remove and return a set of `keys` from given dict. Missing keys 
		are ignored.
		
		Argument `keys` may be passed as a space-separated string, but 
		this won't work in all situations. It's much safer to pass the 
		`keys` as a list object.
		
		NOTE: The dict `d` that you pass to this method *IS* affected.
		      Specified keys will be removed and returned in a separate
		      dict.
		
		EXAMPLE:
		>>> 
		>>> import trix
		>>> d = dict(a=1, b=9, c=4)
		>>> x = trix.kpop(d, "b")
		>>> print (x, d)
		{'b': 9} {'a': 1, 'c': 4}
		>>> 
		
		"""
		
		try:
			keys=keys.split()
		except AttributeError:
			pass
		r = {}
		for k in keys:
			if k in d:
				r[k] = d[k]
				del(d[k])
		return r
	
	
	#
	#
	# PROXIFY
	#
	#
	@classmethod
	def proxify(cls, obj):
		"""
		Return a proxy for `obj`. If `obj` is already a proxy, returns
		the proxy `obj` itself.
		
		>>> 
		>>> # 
		>>> # An example of an object to "proxify."
		>>> # 
		>>> def test(): print("Testing 1 2 3");
		... 
		>>> # 
		>>> # Create a proxy of the "test" function.
		>>> # 
		>>> prxy = trix.proxify(test)
		>>> 
		>>> # 
		>>> # Run the "test" function by calling its proxy.
		>>> # 
		>>> prxy()
		Testing 1 2 3
		>>> 
		>>> # 
		>>> # Show that calling proxify on proxy `prxy` returns the same
		>>> # proxy object.
		>>> # 
		>>> trix.proxify(prxy)
		<weakproxy at 0x7ff017e7e3b8 to function at 0x7ff017e546a8>
		>>> 
		>>> prxy
		<weakproxy at 0x7ff017e7e3b8 to function at 0x7ff017e546a8>
		>>>		
		
		"""
		try:
			return cls.create('weakref.proxy', obj)
		except BaseException:
			return obj
	
	
	#
	#
	# PROPX
	#
	#
	@classmethod
	def propx(cls, *a, **k):
		"""
		Return a propx for given args/kwargs.
		
		The propx objects wrap dicts, iterators, lists, sequences, and
		strings. They provide a variety of interesting and useful methods
		that can be used to view, restructure, and manipulate data. 

		The following modules/classes are currently available. They are
		defined in the `trix.util.propx` package.
		
		 * propbase - generic encoding, compression, and display methods. 
		 * propiter - adds methods suitable to iterable objects
		 * propseq  - methods suitable to any sequence items 
		 * proplist - methods for list manipulation/display
		   propgrid - proplist subclass for list of lists of equal length 
		 * propdict - covers dict-like objects
		
		The set of `propx` classes can be found in the `trix.util.propx`
		package. The scope of propx functionality is too large to be
		presented here. Instead, a short demonstration will be provided
		as a teaser to show where and how a few of the propx features may
		be used to produce amazing results.
		
		EXAMPLE 1:
		>>>
		>>> import trix
		>>> trix.path( trix.innerpath() ).ls.grid()
		util         app      __init__.py  NOTES        fmt       
		x            fs       data         scripts      net       
		README.md    LICENSE  test         __pycache__  .gitignore
		>>>
		
		EXAMPLE 2:
		>>>
		>>> from trix import *
		>>> ps = trix.callx("ps")
		>>>
		>>> #
		>>> # Get the result text:
		>>> #
		>>> ps.text() 
		'  PID TTY          TIME CMD\n13766 pts/4    00:00:00 
		bash\n16203 pts/4    00:00:00 python3\n16205 pts/4    00:00:00 
		ps\n'
		>>>
		>>> #
		>>> # Split the result text into a list of lines:
		>>> #
		>>> ps.text.lines()
		['  PID TTY          TIME CMD', '13766 pts/4    00:00:00 bash', 
		 '16203 pts/4    00:00:00 python3', '16205 pts/4    00:00:00 ps']
		>>>
		>>> #
		>>> # Display the lines as a formatted list
		>>> #
		>>> ps.text.lines.list()
		1    PID TTY          TIME CMD    
		2  13766 pts/4    00:00:00 bash   
		3  16203 pts/4    00:00:00 python3
		4  16205 pts/4    00:00:00 ps     
		>>>
		
		The examples here barely scratch the surface of all the propx
		module can do.
		
		SEE ALSO:
		More documentation is available in the `propx` objects. It's 
		currently sparse, but (we should hope) will be improved overtime.
		>>>
		>>> from trix.util.propx import *
		>>> help(propbase)
		>>> help(propiter)
		>>> help(propseq)
		>>> help(proplist)
		>>> help(propgrid)
		>>> help(propdict)
		>>>
		
		"""
		return trix.ncreate("util.propx.propx", *a, **k)
	
	
	#
	#
	# SCAN - Returns a scanner.
	#
	#
	@classmethod
	def scan(cls, *a, **k):
		"""
		Returns a scanner created with given args/kwargs.
		
		The `trix.scan` classmethod calls on the `trix.data.scan` module
		to help with the parsing of text data.
		
		EXAMPLES:
		>>> trix.scan('[1, 2, 3] frog {"x" : "stream"}').split()
		['[1, 2, 3]', 'frog', '{"x" : "stream"}']
		
		The `trix.data.scan.Scanner` class is complicated, and relies on
		many subpackages.
		
		SEE ALSO:
		>>> from trix.data.scan import *
		>>> help(Scanner)
		>>> help(charinfo)

		"""
		return trix.ncreate('data.scan.Scanner', *a, **k)
	
	
	
	#
	#
	# ---- DISPLAY/DEBUG ----------------------------------------------
	#
	#
	
	
	#
	#
	# FORMATTER (default, JDisplay)
	#
	#
	@classmethod
	def formatter(cls, *a, **k):
		"""
		Return a fmt.FormatBase subclass described by keyword "f" (with
		"f" defaulting to "JDisplay"). Args and Kwargs are dependent on
		the "f" format value.
		
		Call the returned object's `output` to display the output; Call 
		the `format` method to return a str value containing formatted 
		output.
		
		EXAMPLE:
		>>> #
		>>> # Create a formatter for compact json strings.
		>>> #
		>>> j = trix.formatter(f="JCompact")
		>>> j.output(dict(a=1,b=9,c=4))
		{"a":1,"b":9,"c":4}
		>>>
		>>> #
		>>> # Create a formatter for a welcoming banner.
		>>> #
		>>> f = trix.formatter(f="Lines")
		>>> 
		>>> # 'format' generates the string
		>>> f.format("Hello!", ff="title")
		'#\n# Hello!\n#'
		>>>
		>>> # 'output' formats and prints the string
		>>> f.output("Hello!", ff="title")
		#
		# Hello!
		#
		>>>
		
		Available Format Classes:
		 * Format   - Formatted using the python 'format' features.
		 * JCompact - Json with no unnecessary spaces.
		 * JDisplay - An easy-to-read JSON display output.
		 * JSON     - Normal json string.
		 * Grid     - A rudimentary grid display for terminals or files.
		 * List     - A list of items (much like the one you're reading).
		 * Lines    - Formatting of text for display.
		 * Table    - Tabulated data.
		 
		See `trix.fmt.*` class doc to learn more how to use formats for 
		various FormatBase subclasses.
		
		"""
		f = k.pop("f", k.pop('format', "JDisplay"))
		return cls.ncreate("fmt.%s"%f, *a, **k)
	
	
	#
	#
	# DISPLAY - Util. JSON is the main data format within the package.
	#
	#
	@classmethod
	def display(cls, data, *a, **k):
		"""
		Print python data (dict, list, etc...) in, by default, display 
		format. See `trix.formatter()` and various trix.fmt package doc
		for details on required and optional args/kwargs. 
		
		EXAMPLE:
		>>> 
		>>> # Format readable JSON
		>>> trix.display({'a':1, 'b':9, 'c':4})
		{
		  "a": 1,
		  "b": 9,
		  "c": 4
		}
		>>>
		>>> # Format some equal-length lists in a grid
		>>> trix.display([[1,2],[3,4]], f="Grid")
		1  2
		3  4
		>>>
		>>> trix.display([1,2,3,4,5,6,7,8,9], f="Table", width=3)
		1  2  3
		4  5  6
		7  8  9
		>>> 

		
		"""
		cls.formatter(*a, **k).output(data)
	
	
	
	#
	#
	# DEBUG
	#
	#
	@classmethod
	def debug(cls, debug=True, showtb=True):
		"""
		Enable/disable debugging/traceback. This should pretty much be
		left alone. The trix code is too convoluted to debug without it.
		However, it's available if you want to turn it off. If debug is
		set to False, normal python excpetion format is displayed (and
		tracebacks won't be duplicated). When `debug` is on but `showtb`
		is False, the extended exception format is still shown but the
		trailing traceback is ignored.
		"""
		Debug.debug(debug,showtb)

	
	# TRACE-BK
	@classmethod
	def tracebk(cls):
		"""Return current exception's traceback as a list."""
		tb = sys.exc_info()[2]
		if tb:
			try:
				return list(traceback.extract_tb(tb))
			finally:
				del(tb)
	
	
	#
	#
	# X-DATA
	#
	#
	@classmethod
	def xdata(cls, data=None, **k):
		"""
		Package extensive exception data into a dict. This is a utility
		for the trix package; it helps generate extensive exception data
		for use by the debug handler. That doesn't mean it's not still
		useful for other purposes.
		
		>>> xdata(a=1, b=9, c=4)
		"""
		return xdata(cls, data, **k)
	
	
	#
	#
	# LOG
	#
	#
	@classmethod
	def log(cls, *a, **k):
		"""
		Returns Loglet for this process. Pass args/kwargs to log. The
		trix.Logging class variable determines the output:
		
		 * 1  = Log to file
		 * 0  = Logging turned off (the default)
		 * -1 = Print log entries to the terminal
		
		Calling this method with trix.Logging set to 1 generates a log 
		file named for the process ID. This is helpful for debugging 
		multi-process situations.
		
		#
		# Check your working directory for log files after this example!
		# They can really fill up a directory quickly if you forget.
		#
		>>> trixc = trix.trixc()
		>>> dbg = trixc.Logging
		>>> trixc.Logging = 1
		>>> trixc.log('a', 'b', 'c', x=1)
		>>> trixc.Logging = dbg
		
		#
		# NOTE: 
		#  - The `trix.trixc()` method is necessary here because this 
		#    example must get and set the trix.Logging class variable,
		#    while `trix` may refer either to the trix class or the trix
		#    module.
		#    
		#    While this may seem a silly distinction, it serves to make
		#    this example work regardless of how you imported trix.
		#    
		#    One of the primary goals of the trix project is ease of use
		#    from the python interpreter. With `trix.trixc()`, we need
		#    never suffer an error because we typed `import trix` rather
		#    than `from trix import *` (or vice-versa).
		#
		"""
		if cls.Logging < 0:
			with thread.allocate_lock():
				a = list(a)
				a.append(k)
				cls.display(a)
		elif cls.Logging > 0:
			with thread.allocate_lock():
				try:
					cls.__log(*a, **k)
				except:
					cls.__log = cls.ncreate('util.loglet.Loglet', cls.__m)
					cls.__log(*a, **k)
	
	
	#
	#
	# TRIX-C
	#
	#
	@classmethod
	def trixc(cls):
		"""
		Returns the trix class.
		
		This may be necessary when scripting outside the library in a 
		situation where you don't know whether the trix library was 
		imported as "import trix" or "from trix import *".
		
		This method exists mostly to make sure that example code won't
		fail regardless of how trix was imported.
		
		"""
		return cls
	
	
	
	
	# ---- unsorted classmethods --------------------------------------
	
	#
	#
	# SIGNALS
	#
	#
	@classmethod
	def signals(cls):
		"""
		Manage the handling of signals. 
		
		* Call classmethod `add` passing int `signal` and a function,
		  method, or other callable to be triggered when the specified
		  `signal` is detected.
		* Use classmethod `rmv` to remove the signal when the target 
		  should no longer receive notification of this signal.
		
		```
		def on_interrupt(signum, stackframe):
			print ("Signal %i!" % signum)
		
		SIGINT = 2
		trix.signals().add(SIGINT, lambda i,sf: on_interrupt(i,sf))
			
		```
		
		See `trix.util.signals` for more information.
		
		URGENT: SIGNALS MUST BE ADDED *ONLY* FROM THE MAIN THREAD!
		
		"""
		try:
			return cls.__signals
		except:
			cls.__signals = trix.nvalue("util.signals.Signals")
			return cls.__signals
	
	
	#
	#
	# LOC
	#
	#
	@classmethod
	def loc(cls, locale=None):
		"""
		Pass a locale string, eg., "en_US.UTF_8"; Default is the current
		system default locale values.
		
		Returns a new object that's a subclass of `util.loc.BaseLocale`
		containing locale data and format strings.
		
		EXAMPLE 1:
		>>> import trix
		>>> L = trix.loc("en_US.UTF_8")
		>>> L.display()
		
		The example above should display a dict containing all locale 
		data for "en_US.UTF_8".
		
		NOTE:
		Use `L.locdata` to retrieve a dict containing the information 
		displayed above.
		
		NOTE ALSO:
		The `trix.loc` method is not limited to retrieving data for
		only one locale. By gathering loc data through remote processes,
		any or all locales can be queried at any time.
		
		EXAMPLE 2:
		>>> L = trix.loc("fr_FR.utf8")
		>>> L.display()
		
		"""
		
		# Default is the current system locale.
		if not locale:
			locale = ".".join(trix.module("locale").getlocale())
		
		# If a `locale` argument is specified, that locale will be used.
		return trix.ncreate("util.loc.Locale", locale)






# -------------------------------------------------------------------
#
#
# CONVENIENCE
#  - Trix should be imported in one of two ways:
#    >>> import trix
#    >>> from trix import *
#
#  Because these variables are set to the values of the trix methods
#  and classmethods, there's no chance that the annoyance of not
#  having chosen the correct import statement will interfere with
#  one's work.
#
#  Importing by the first method, `import trix` is tighter, and gives
#  access to all of trix features. 
#
#  Importing by the second method, `from trix import *`, allows access
#  to the variables below by name.
#
#  >>> from trix import *
#  >>> loc('fr')
#
# -------------------------------------------------------------------

callx      = trix.callx
config     = trix.config
create     = trix.create
debug      = trix.debug
display    = trix.display
innerpath  = trix.innerpath
innerfpath = trix.innerfpath
formatter  = trix.formatter
jconfig    = trix.jconfig
jparse     = trix.jparse
kcopy      = trix.kcopy
kpop       = trix.kpop
loc        = trix.loc
log        = trix.log
module     = trix.module
nconfig    = trix.nconfig
ncreate    = trix.ncreate
nmodule    = trix.nmodule
nprocess   = trix.nprocess
nvalue     = trix.nvalue
npath      = trix.npath
path       = trix.path
pid        = trix.pid
popen      = trix.popen
process    = trix.process
propx      = trix.propx
proxify    = trix.proxify
scan       = trix.scan
signals    = trix.signals
start      = trix.start
tracebk    = trix.tracebk
trixc      = trix.trixc
value      = trix.value



# -------------------------------------------------------------------
#
#
# LOADER (and NLoader)
#  - The Loader class prepares for loading modules without actually 
#    bringing them into memory.
#
#
# -------------------------------------------------------------------

class Loader(object):
	"""Intended for internal use."""
	
	def __init__(self, module, value=None, loader=trix.module):
		#
		#Pass module name (string) and function name (string). Loading of
		#module is deferred until the first call.
		#
		self.__L = loader
		self.__M = module
		self.__V = value
	
	def __repr__(self):
		T = type(self)
		aa = (
			T.__name__, self.__L.__name__, self.__M, repr(self.__V)
		)
		return "<%s trix.%s('%s', %s)>" % aa
	
	@property
	def module(self):
		# Return the module object as specified to construcor.
		try:
			return self.__module
		except AttributeError:
			self.__module = self.__L(self.__M) # use loader
			return self.__module
	
	@property
	def value(self):
		# Return the value specified to construcor.
		try:
			return self.__value
		except AttributeError:
			self.__value = self.module.__dict__[self.__V]
			return self.__value

	def __call__(self, *a, **k):
		# Load the specified method/function and return its result.
		self.__call__ = self.value
		return self.__call__(*a, **k)

	def __getitem__(self, x):
		# Get any member (function, value, etc...) from the module.
		return self.module.__dict__[x]


# N-LOADER
class NLoader(Loader):
	"""Intended for internal use."""
	def __init__(self, module, value=None):
		# Init loader with the trix.nmodule loader."""
		Loader.__init__(self, module, value, loader=trix.nmodule)


# -------------------------------------------------------------------
#
#
# COMPATABILITY
#  - Ensures the existence of common python 2/3 typedefs.
#
#
# -------------------------------------------------------------------


try:
	basestring
except:
	#
	# The following are defined if basestring is undefined (before 
	# python 2.3, and for python 3 and higher). These values make the
	# important distinction between unicode and byte values/strings.
	# These designations are important in some rare cases.
	#
	basestring = unicode = str
	unichr = chr
	
	# Convence for development. Selects an import lib suitable to 
	# the running version of python.
	# 
	if AUTO_DEBUG:
		try:
			try:
				from importlib import reload
			except:
				from imp import reload
		except:
			pass



#
# For implementations with unicode support compiled without wide 
# character support, this allows comparison of wide characters. 
# This should solve many problems on pre-python3 Windows systems.
#
try:
	unichr(0x10FFFF) # check wide support
except:
	import struct
	def unichr (i):
		return struct.pack('i', i).decode('utf-32')



"""
#
# This supports python versions before 2.6 when the bytes type was 
# introduced.
#
try:
	bytes
except:
	#
	# TO DO:
	#  - This only happens pre-version 2.6 and trix only supports 2.7+,
	#    so I need to deprecate and remove it... after testing.
	#
	bytes = str
"""


# Define FileNotFoundError for earlier systems that need it.
try:
	FileNotFoundError
except:
	class FileNotFoundError(NameError):
		pass


#
# I'm not sure how useful this is. There may be a better (existing) 
# exception to use instead.
#
try:
	wt = WaitTimeout
except:
	class WaitTimeout(Exception):
		"""Raise this when an operation times out."""
		pass



# -------------------------------------------------------------------
#
# EXTENDED DEBUGGING
#  - This package provides extensive debugging information in raised
#    exceptions, so a little extra formatting is needed to help make
#    sense of some of the things that might go wrong.
#
# -------------------------------------------------------------------

class xdata(dict):
	"""
	Package extensive exception data into a dict.
	
	Pass optional data and keyword arguments. A
	"""

	def __init__(self, data=None, **k):

		# argument management
		data = data or {}
		data.update(k)

		# create and populate the return dict
		self['xdata'] = data
		self.setdefault('xtime', time.time())

		# If this is a current exception situation,
		# record its values
		try:
			tblist = None
			xtype, xval = sys.exc_info()[:2]
			tblist = trix.tracebk()
			if xtype or xval or tblist:
				self['xtype'] = xtype
				self.__xtype  = xtype
				self['xargs'] = xval.args
				if tblist:
					self['xtracebk'] = list(tblist)
		finally:
			if tblist:
				del(tblist)
				tblist = None



#
# DEBUG HOOK
#
def debug_hook(t, v, tb):
	"""
	# ARGS:
	t  = Type      - eg, <class 'Exception'>
	v  = Value     - the arguments (probably packed into xdata)
	tb = Traceback 
	
	"""
	
	with thread.allocate_lock():
		
		#
		#if isinstance(v, KeyboardInterrupt):
		#	trix.module('os').kill(trix.pid(), 2)
		#
		# KEYBOARD INTERRUPT
		#if isinstance(v, KeyboardInterrupt):
		#	#print ("\n", t, v, tb, "\n\n")
		#	raise KeyboardInterrupt()
		#	#print ("\n", t, "\n\n")
		#
		# JUST KIDDING
		#  - It turns out there's no way to re-throw a KeyboardInterrupt
		#    if you want to capture and custom-display errors as trix
		#    does.
		#  - In fact, this is good - SIGINT should be handled by a signal
		#    handler anyway, because trix is into threading in a big way
		#    and there's no way to use that KeyboardInterrupt to directly
		#    (determinately) influence the operation of threads.
		#  - USE specialized signal installer `output.InstallPauseSignal`
		#    to enable pause/resume in Runner output, or...
		#  - USE trix.signals().add(2, some_callable) to install your own
		#    custom SIGINT handler.
		#  - Otherwise, KeyboardInterrupt is just going to "pass".
		#
		
		if isinstance(v, KeyboardInterrupt):
			pass
		
		
		#
		# ------- ALL OTHERS --------------------------------------------
		#
		else:
			# catch errors in the debug hook and disable debugger
			try:
				print (t)
				
				# SYNTAX ERROR
				if isinstance(v, SyntaxError):
					print(" ->", str(type(v)))
				
				#
				# DISPLAY ARGS
				#
				if v.args:
					try:
						trix.display(list(v.args), sort_keys=1)
					except Exception:
						args = [str(a) for a in v.args]
						print ("[")
						if len(v.args)==1:
							print (" ", str(v.args))
						else:
							for a in v.args:
								try:
									print("  %s" % str(a))
								except:
									print ("  ", a)
						print ("]")
				
				
				#
				# TRACEBACK
				#  - show traceback, if enabled
				#
				if tb and Debug.showtb():
					print ("Traceback:")
					traceback.print_tb(tb)
				print ('')
			
			#
			# EXCEPTION IN EXCEPTION HANDLER
			#
			except BaseException:
				print ("\n#\n# DEBUG HOOK FAILED!")
				try:
					xxtype, xxval = sys.exc_info()[:2]
					print ("# - Debug Hook Err: %s %s\n#"%(xxtype, str(xxval)))
				except:
					pass
				
				# turn off debugging and re-raise the exception
				debug(False)
				print ("# - Debug Hook is Disabled.\n#\n")
				raise
			finally:
				if tb:
					del(tb)
					tb = None


#
# DEBUG
#
class Debug(object):
	__DEBUG = False
	__TRACE = False
	__SYSEX = sys.excepthook
	
	@classmethod
	def debug(cls, debug=True, showtb=False, **k):
		cls.__DEBUG = bool(debug)
		cls.__TRACE = bool(showtb)
		if cls.__DEBUG:
			sys.excepthook = debug_hook
		else:
			sys.excepthook = cls.__SYSEX
	
	@classmethod
	def debugging(cls):
		return cls.__DEBUG
	
	@classmethod
	def showtb(cls):
		return cls.__TRACE



if AUTO_DEBUG:
	Debug.debug(1,1)

