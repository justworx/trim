#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import sys, time, traceback, json
try:
	import thread
except:
	import _thread as thread


#
# VERSION
#  - The official version of the `trix` package is currently
#    "Version: zero; rough draft four; under construction".
#
VERSION = 0.0000

#
# AUTO_DEBUG
#  - Controls the formatting of raised Exceptions.
#  - The trix package is very complex, making it really hard to
#    track down bugs. This formatting of exceptions really helps.
#  - If you want exceptions the old-fashioned way, set it False.
#
AUTO_DEBUG = True

#
# DEF_ENCODE
#  - The default encoding for the trix package is now determined by
#    sys.getdefaultencoding(). I don't know if that method can fail,
#    but if it does, 'utf_8' is used as a backup.
#  - This change is experimental. DEF_ENCODE used to be set directly
#    to 'utf_8'. I don't expect this to cause any problems, but in
#    the event it does, I'll switch back to a hard-coded default of
#    'utf_8'.
#
DEF_ENCODE = sys.getdefaultencoding() or 'utf_8'

#
# DEF_NEWL
#  - The default newline sequence.
#
DEF_NEWL = '\r\n'

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
# DEFAULT INDENTATION
#  - Number of spaces to use when indenting formatted text, tab
#    replacement, etc...
#
DEF_INDENT = 2

#
# LOGLET FILE PATH/NAME
#
DEF_LOGLET = "./loglet"



#
# TRIX CLASS
#
class trix(object):
	"""Utility, debug, import; object, thread, and process creation."""
	
	__m  = __module__
	__mm = sys.modules
	
	Logging = 0 #-1=print; 0=None; 1=log-to-file
	
	
	# ---- object creation -----
	
	# INNER PATH	
	@classmethod
	def innerpath(cls, innerPath=None):
		"""
		Prefix `innerPath` with containing packages.
		
		Return a string path `innerPath` prefixed with any packages that
		contain this module. If the optional `innerPath` is None, the 
		path to (and including) this package is returned.
		
		>>> trix.innerpath("app.console")
		"""
		p = '.%s' % (innerPath) if innerPath else ''
		if cls.__m:
			return "%s%s" % (cls.__m, p)
		else:
			return innerPath
	
	
	# INNER F-PATH	
	@classmethod
	def innerfpath(cls, innerFPath=None):
		"""
		Return a file path from within the trix package.
		
		>>> trix.innerfpath('app/config/en.conf')
		"""
		ifp = cls.innerpath().split('.')
		if innerFPath:
			ifp.append(innerFPath)
		return "/".join(ifp)
	
	
	# MODULE
	@classmethod
	def module (cls, path):
		"""
		Returns a module given a string `path`. Specified module may be 
		external to the trix package. 
		
		>>> trix.nmodule('socket')
		"""
		try:
			return cls.__mm[path]
		except KeyError:
			__import__(path)
			return cls.__mm[path]
	
	
	# N-MODULE
	@classmethod
	def nmodule(cls, innerPath):
		"""
		Like `module`, but pass the inner path instead of full path.
		
		>>> trix.nmodule('fs.dir')
		"""
		return cls.module(cls.innerpath(innerPath))
	
	
	# CREATE
	@classmethod
	def create(cls, modpath, *a, **k):
		"""
		Create and return an object specified by argument `modpath`. 
		
		The dot-separated path must start with the path to the desired
		module. It must be suffixed with a name of a class defined in the
		specified module. (Eg, 'package.subpackage.module.ClassName')
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		
		>>> sock = trix.create("socket.socket")
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
					message = "cannnot-create-module"
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
		
	
	# N-CREATE - create an object given path from inside trix
	@classmethod
	def ncreate(cls, innerPath, *a, **k):
		"""
		Create and return an object specified by argument `innerPath`.
		The dot-separated path must start with the path to the desired
		module *within* this package (but NOT prefixed with the name of
		this package. It must be prefixed with a name of a class defined
		in the specified module. Eg, 'subpackage.theModule.TheClass
		
		Any additional arguments and keyword args will be passed to the
		class's constructor.
		
		USE: The ncreate() method is used from within this package. For 
		     normal (external) use, use the create() method.
		
		>>> trix.ncreate("app.console.Console")
		"""
		a = a or []
		k = k or {}
		return cls.create(cls.innerpath(innerPath), *a, **k)
	
	
	# VALUE - return a value (by name) from a module
	@classmethod
	def value(cls, pathname, *args, **kwargs):
		"""
		Returns an object as specified by `pathname` and additional args.
		
		Returns a module, class, function, or value, as specified by the
		string argument `pathname`. If additional *args are appended, 
		they must name a class, method, function, or value defined within 
		the object specified by first argument. A tupel is returned.
		
		>>> trix.value('socket',"AF_INET","SOCK_STREAM")
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
				# TO DO:
				# Make this work when `v` is a module. It does work if the
				# module `v` would specify is already loaded, but not if it's
				# not... which is inconsistent... which bothers me.
				raise
		
		# If one *args value was specified, return it. If more than one
		# was specified, return them as a tuple.
		if len(rr) == 1:
			return rr[0]
		return tuple(rr)
	
	
	# N-VALUE
	@classmethod
	def nvalue(cls, pathname, *a, **k):
		"""
		Like `value`, but pass the inner path instead of full path.
		
		>>> trix.nvalue("util.compenc.b64")
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
	
	
	# PATH
	@classmethod
	def path(cls, path=None, *a, **k):
		"""
		Return an fs.Path object at `path`.
		
		>>> p = trix.path().path
		>>> trix.path().dir().ls()
		>>> trix.path("trix/app/config/app.conf").reader().readline()
		"""
		try:
			return cls.__FPath(path, *a, **k)
		except:
			# requires full module path, so pass through innerpath()
			cls.__FPath = cls.module(cls.innerpath('fs')).Path
			return cls.__FPath(path, *a, **k)
	
	# N-PATH
	@classmethod
	def npath(cls, innerFPath=None, *a, **k):
		"""
		Return an fs.Path for a file-system object within the trix 
		directory.
		
		>>> e = 'UTF_8'
		>>> r = trix.npath("app/config/app.conf").reader(encoding=e)
		>>> r.readline()
		"""
		return cls.path(cls.innerfpath(innerPath), *a, **k)
	
	# DIR
	@classmethod
	def dir(cls, path=None, *a, **k):
		"""Like trix.path, but returns a Dir object."""
		return cls.path(path, *a, **k).dir()
	
	
	
	# ---- general utility -----
	
	
	# PROXIFY
	@classmethod
	def proxify(cls, obj):
		"""
		Return a proxy for `obj`. If `obj` is already a proxy, returns
		the proxy `obj` itself.
		
		>>> def test(): print("Testing 1 2 3");
		>>> prxy = trix.proxify(test)
		>>> prxy()
		>>> trix.proxify(prxy)
		"""
		try:
			return cls.create('weakref.proxy', obj)
		except BaseException:
			return obj

	
	# K-COPY
	@classmethod
	def kcopy(cls, d, keys):
		"""
		Copy `keys` from `d`; return in a new dict.
		
		Creates a subset of dict keys in order to select only desired (or 
		allowed) keyword args before passing to functions and methods. 
		Argument `keys` may be passed as a space-separated string, but 
		this won't work in all situations. It's much safer to pass the 
		`keys` as a list object.
		
		The original dict is never altered by `kcopy`.
		
		>>> d = dict(a=1, b=9, c=4)
		>>> trix.kcopy(d, "b")
		>>> trix.kcopy(d, ['a', 'c'])
		>>> d
		"""
		try:
			keys=keys.split()
		except:
			pass
		return dict([[k,d[k]] for k in keys if k in d])
	
	
	# K-POP
	@classmethod
	def kpop(cls, d, keys):
		"""
		Remove and return a set of `keys` from given dict. Missing keys 
		are ignored.
		
		Argument `keys` may be passed as a space-separated string, but 
		this won't work in all situations. It's much safer to pass the 
		`keys` as a list object.
		
		NOTE: The dict `d` that you pass to this method is affected.
		      Specified keys will be removed and returned in a separate
		      dict.
		
		>>> d = dict(a=1, b=9, c=4)
		>>> x = trix.kpop(d, "b")
		>>> print (x, d)
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
	
	
	
	# ---- display/debug -----
	
	
	# FORMATTER (default, JDisplay)
	@classmethod
	def formatter(cls, *a, **k):
		"""
		Return a fmt.FormatBase subclass described by keyword "f" (with
		"f" defaulting to "JDisplay"). Args and Kwargs are dependent on
		the "f" format value. See trix.fmt.* class doc to learn more 
		about how to control formats for various FormatBase subclasses.
		
		Call the returned object's `output` to display the output; Call 
		the `format` method to return a str value containing formatted 
		output.
		
		>>> j = trix.formatter(f="JCompact")
		>>> j.output(dict(a=1,b=9,c=4))
		>>>
		>>> f = trix.formatter(f="Lines")
		>>> f.format("Hello!", ff="title")
		>>> f.output("Hello!", ff="title")
		"""
		f = k.pop("f", "JDisplay")
		return cls.ncreate("fmt.%s"%f, *a, **k)
	
	
	# DISPLAY - Util. JSON is the main data format within the package.
	@classmethod
	def display(cls, data, *a, **k):
		"""
		Print python data (dict, list, etc...) in, by default, display 
		format. See `trix.formatter()` and various trix.fmt package doc
		for details on required and optional args/kwargs. 
		
		>>> trix.display({'a':1, 'b':9, 'c':4})
		"""
		cls.formatter(*a, **k).output(data)
	
	
	
	# DEBUG
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
	
	
	# X-DATA
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
# LOADER (and NLoader)
#

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


#
# COMPATABILITY
#

# common python 2/3 typedefs
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
	
	# Convence for development.
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



#
# This supports python versions before 2.6 when the bytes type was 
# introduced.
#
try:
	bytes
except:
	# this only happens pre-version 2.6
	bytes = str



#
# EXTENDED DEBUGGING
#  - This package provides extensive debugging information in raised
#    exceptions, so a little extra formatting is needed to help make
#    sense of some of the things that might go wrong.
#
class xdata(dict):
	"""Package extensive exception data into a dict."""

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
	
	with thread.allocate_lock():

		# catch errors in the debug hook and disable debugger
		try:
			
			# KEYBOARD ERROR
			if isinstance(v, KeyboardInterrupt):
				print ("\n", t, "\n\n")

			else:
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
				print ("# - Debug Hook Err: %s %s\n#" % (xxtype, str(xxval)))
			except:
				pass
			
			# turn off debugging and re-raise the exception
			debug(False)
			print ("# - Debug Hook is Disabled.")
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

