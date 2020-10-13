#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..util import mime
from ..util.enchelp import *
import shutil, os, os.path as ospath

VALID_AFFIRM = ['touch','makedirs','makepath','checkdir','checkfile',
								'checkpath']


class Path(object):
	"""
	Objects of class `Path` represent a file system path.
	
	The `trix.fs.Path` class is the base for all trix subclasses that
	deal with file system objects. Path provides a common interface
	for accessing information about paths such as:
	 
	 * the file name, size, path, pathtype, mime info, parent directory
	 * useful data like md5, sha256 and sha512 hashes, reasonable 
	   values for blocksizes
	 * the files `stat`, and whether it `exists`.
	
	Path also provides methods for manipulation and access of files.
	
	 * the `touch` method makes it easy to update file dates 
	 * the `dir` method returns a Dir object.
	
	"""
	
	
	#
	#
	# INIT
	#
	#
	def __init__(self, path=None, **k):
		"""
		Pass optional `path` argument. Default is the current working 
		directory.
		
		Pass optional keyword arguments accepted by the expand() method.
		
		Keyword 'affirm' lets you assign (or restrict) actions to be
		taken if the given path does not exist.
		
		 * checkpath - default; raise if parent path does not exist.
		 * checkfile - raise if `path` doesn't specify an existing file.
		 * checkdir - raise if full given path does not exist.
		 * makepath - create parent path as directory if none exists.
		 * makedirs - create full path as directory if none exists.
		 * touch - create a file at the given path if none exists.
		
		REMEMBER:
		The default 'affirm' keyword argument value is "checkpath".
		To ignore all validation, you must pass affirm=None.
		
		EXAMPLE:
		>>> 
		>>> from trix.fs import *
		>>> p = Path("~/tests/myTest.txt", affirm="touch")
		>>> 
		>>> #
		>>> # Note that the `p` object created above points to a file, so 
		>>> # the `p.dir()` call must be directed outward to the enclosing 
		>>> # directory so that we can call the `ls()` method to list the 
		>>> # file.
		>>> # 
		>>> p.dir("..").ls()
		['myTest.txt']
		>>> 
		
		"""
		self.sep = os.sep
		self.__p = self.expand(k.get('path', path or '.'), **k)
		
		
		try:
			self.__n = ospath.normpath(self.__p).split(self.sep)[-1]
		except TypeError:
			if isinstance(self.sep, unicode):
				self.sep = self.sep.encode()
			else:
				self.sep = self.sep.decode()
				self.__n = ospath.normpath(self.__p).split(self.sep)[-1]
		
	
	#
	#
	# CALL - Shortcut for creating new Path and Dir objects based 
	#        on the path of this (self) object.
	#
	#
	def __call__(self, mergepath=None, **k):
		"""
		A shortcut for creating new Path and Dir objects.
		
		When you call the Path object as a function a new Path or Dir
		object will be returned based on the type of file system object
		that is selected.
		
		#
		# Calling With no Argument:
		#
		If you call this method as a function without passing an argument,
		a Dir object will be returned if the target file system object is
		a directory. Otherwise, a Path object will be returned
		
		EXAMPLE:
		>>>
		>>> from trix.fs import *
		>>> trixpath = trix.innerfpath()
		>>> p = Path(trixpath)
		>>> p()
		<trix.fs.dir.Dir '/home/nine/trix' (d)>
		>>>
		>>> # 
		>>> # you can use the result as a temporary object
		>>> #
		>>> p().ls.sorted.table(width=6)
		.git         .gitignore   LICENSE  NOTES  README.md  __init__.py
		__main__.py  __pycache__  app      data   fmt        fs         
		net          scripts      test     util   x                     
		>>> 
		
		#
		# Calling with Arguments:
		#
		If you pass a partial file path to this method it will be merged
		into a new Path or Dir object, depending on the type of file 
		system object being encapsulated.
		
		EXAMPLE:
		>>>
		>>> from trix.fs import *
		>>>
		>>> p('data').ls()
		['__init__.py', 'database.py', 'cursor.py', 'param.py', 'udata',   
		 'pdq.py','dbgrid.py', 'param.md', 'scan.py']
		>>> 

		"""
		
		# If a merge path is given, merge it to this object's path.
		if mergepath:
			
			# Get the new object's path.
			mpath = self.merge(mergepath)
			
			# If the target file system object is a directory, wrap it in a
			# Dir object and return it.
			if self.isdir(mpath):
				return self.dir(mpath, **k)
			
			# If it's something else, wrap it in a path object.
			else:
				return Path(mpath, **k)
		
		# OTHERWISE: Just make a Path or Dir from this object's self.path
		else:
			if self.isdir(self.path):
				return self.dir(self.path, **k)
			else:
				return Path(self.path, **k)	
	
	
	#
	#
	# ENTER/EXIT
	#
	#
	def __enter__(self):
		"""
		There's really no reason for this except to make it available
		to people who like to write code this way.
		"""
		return self
	
	def __exit__(self, *args):
		"""
		There's really no reason for this except to make it available
		to people who like to write code this way.
		"""
		pass
	
	
	#
	#
	# GET-ITEM
	#
	#
	def __getitem__(self, i):
		"""
		Return the path to an item from a directory by its integer index.
		
		The purpose of this method is to facilitate the iteration through 
		path elements in a full file path.
		
		EXAMPLE:
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath() )
		>>>
		>>> p[0] # on linux, the zero path element is always ''
		''
		>>> p[1]
		'home'
		
		"""
		return self.path.split(self.sep)[i]
	
	
	#
	#
	# REPR
	#
	#
	def __repr__(self):
		"""
		Returns a representation string specifying:
		 * full class path
		 * full file path
		 * file system object's type, abbreviated:
		     f = file
		     d = directory
		     l = link
		     m = mount
		
		EXAMPLE:
		>>> 
		>>> from trix.fs import *
		>>> repr(p())
		"<trix.fs.dir.Dir '/home/nine/trix' (d)>"
		>>> 
		"""
		return "<%s.%s '%s' (%s)>" % (
				str(type(self).__module__),
				str(type(self).__name__), self.path, self.pathtype
			)
	
	
	#
	#
	# STR
	#
	#
	def __str__(self):
		"""
		Returns the path as a string.
		
		>>> from trix.fs import *
		>>> str( p() )
		>>> 
		"""
		return self.path
	
	
	#
	#
	# UNICODE
	#
	#
	def __unicode__(self):
		"""The path as a unicode string (for python 2 support)."""
		return unicode(self.path)
	
	
	#
	#
	# PROPERTIES
	#
	#
	@property
	def mime(self):
		"""
		Return a Mime object for this object's path.
		
		The `Path.mime` method is a utility that supports several features
		in the `trix.fs` package. However, it can certainly be used when
		needed for other purposes.
		
		#
		# EXAMPLE:
		#
		>>> import trix
		>>> p = trix.path(trix.innerpath("__init__.py"))
		>>> p.mime.guess
		('text/x-python', None)
		>>> p.mime.type
		'text'
		>>> p.mime.subtype
		'x-python'
		>>> p.mime.mimetype
		'text/x-python'
		>>>
		
		#
		# MORE INFO:
		#
		>>> import trix.util.mime
		>>> help(trix.util.mime)
		
		"""
		return trix.ncreate('util.mime.Mime', self.path)
	
	@property
	def parent(self):
		"""
		Return the path to this path's parent directory.
		
		#
		# EXAMPLE:
		#
		>>> import trix
		>>> p = trix.path(trix.innerfpath("__init__.py"))
		>>> p.parent
		'/home/<USER>/trix'
		>>>
		
		"""
		return ospath.dirname(self.path)
	
	@property
	def name(self):
		"""
		Return current path's last element.
		
		#
		# EXAMPLE:
		#
		>>> import trix
		>>> p = trix.path(trix.innerfpath("__init__.py"))
		>>> p.name
		'__init__.py'
		>>>
		"""
		return self.__n
	
	@property
	def path(self):
		"""Return or set this path."""
		return self.getpath()
	
	@path.setter
	def path(self, path):
		self.setpath(path)
	
	@property
	def pathtype(self):
		"""
		Return the type of this object's target file system object.
		
		  f = file
		  d = directory
		  l = link
		  m = mount
		
		"""
		if self.isfile():
			return 'f' #file'
		elif self.isdir():
			return 'd' #dir'
		elif self.islink():
			return 'l' #link'
		elif self.ismount():
			return 'm' #mount'
		else:
			return '?'
	
	
	#
	# METHODS
	#
	
	# GET/SET PATH
	def getpath(self):
		"""Return this object's path."""
		return self.__p
	
	def setpath(self, path):
		"""
		INTERNAL USE ONLY!
		Sets the path to which this object points.
		
		WARNING:
		This method is intended for ONLY for internal use. 
		
		DANGER:
		Path.setpath does NOT move file system objects - other classes 
		handle that kind of thing. The `setpath` method is used ONLY to 
		reset an object's path once such a move has been made.
		
		NOTE ALSO:
		I'll probably rename it to _setpath to conform to pythonic
		conventions. If I remember correctly, we're supposed to treat
		identifiers prefixed with an underscore as though they were
		"protected" members.
		
		"""
		self.__p = path
		self.__n = ospath.normpath(path).split(self.sep)[-1]
	
	#
	# PATH TYPES
	#
	def isfile(self, path=None):
		"""True if path is a file."""
		return ospath.isfile(self.merge(path))
	
	def isdir(self, path=None):
		"""True if path is a directory."""
		return ospath.isdir(self.merge(path))
	
	def islink(self, path=None):
		"""True if path is a symbolic link."""
		return ospath.islink(self.merge(path))
	
	def ismount(self, path=None):
		"""True if path is a mount point."""
		return ospath.ismount(self.merge(path))
	
	
	#
	#
	# TOUCH
	#
	#
	def touch(self, mergepath=None, times=None):
		"""
		Touch a file.
		
		Typical usage is to call Path.touch() with no arguments. This 
		will reset the file to the current times.
		
		>>>
		>>> from trix.fs import *
		>>>
		>>> #
		>>> # Take a file's time back to yesterday
		>>> #
		>>> import time
		>>> h_minus_24 = time.time() - 60*60*24
		>>> p = Path(trix.innerfpath('README.md'))
		>>> p.stat()
		>>> p.touch(h_minus_24, h_minus_24)
		>>>
		
		If a "mergepath" keyword argument is specified, it will be 
		merged with this Path object's current path. This allows Path 
		objects that contain a directory to be called multiple times 
		for the purpose of altering some or all files within the 
		directory to the same `utime` values.
		
		>>> 
		>>> from trix.fs import *
		>>> p = Path(trix.innerfpath('README.md'))
		>>> p.touch(times)
		>>>
		
		If a "times" keyword argument is passed, it must consist of a
		tupel containing (atime, mtime), where each member is an int or
		float expressing seconds.
		
		#
		# TO DO:
		#
		Trix does not currently support the nanosecond parameter. This 
		is on the to-do list, but will have to wait for now. I need a
		way to safely catch excptions for pre-3.6 and pre-3.3 systems so
		that older systems can still make use of the method.

		"""
		try:
			p = self.merge(mergepath)
		except Exception as ex:
			raise type(ex)('touch-fail', xdata(
					p         = p,         # same as mergepath
					path      = self.path, 
					mergepath = mergepath, Tmergepath = type(mergepath),
					times     = times,     Ttimes     = type(times)
				))
		
		try:
			if times:
				with self.wrapper(p) as w:
					w.touch(times)
			else:
				w.touch()
				
		except:
			with open(p, 'a'):
				os.utime(p, times)
	
	
	#
	#
	# MERGE
	#
	#
	def merge(self, path):
		"""
		Return the given path relative to self.path.
		
		Build a new path based on the `path` string argument.
		
		EXAMPLE:
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath('net/server.py') )
		>>> p.merge( "../connect.py" )
		'/home/<USER>/trix/net/connect.py'
		>>>
		>>> p.merge( ".." )
		'/home/<USER>/trix/net'

		"""
		if not path:
			return self.path
		
		p = ospath.expanduser(path)
		if ospath.isabs(p):
			return ospath.normpath(p)
		
		else:
			p = ospath.join(self.path, p)
			return ospath.abspath(ospath.normpath(p))
	
	
	#
	#
	# HASH
	#
	#
	def hash(self, algo, blocksize=None):
		"""
		Hash this file given string `algo` for the hashing algorithm, and
		an optional blocksize.
		
		Hash the file at self.path using the given algo; optional argument
		`blocksize` defaults to value returned by self.blocksizer().
		
		Example:
		>>> from trix.fs import *
		>>> p = Path(trix.innerfpath('LICENSE'))
		>>> p.hash('sha256')
		'8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef'
		>>>
		 
		"""
		blocksize or self.blocksizer()
		try:
			h = hashlib.new(algo)
		except:
			import hashlib
			h = hashlib.new(algo)
		
		with open(self.path, 'rb') as f:
			b = f.read(blocksize)
			while len(b) > 0:
				h.update(b)
				b = f.read(blocksize)
		return h.hexdigest()
	
	
	#
	#
	# MD5
	#
	#
	def md5(self, blocksize=None):
		"""
		Hash using md5 algo.
		
		Example:
		>>> 
		>>> p = Path(trix.innerfpath('LICENSE'))
		>>> p.md5()
		'4ae09d45eac4aa08d013b5f2e01c67f6'
		>>> 
			
		"""
		return self.hash('md5', blocksize or self.blocksizer())
	

	#
	#
	# SHA-256
	#
	#
	def sha256(self, blocksize=None):
		"""
		Hash using sha256 algo.
		
		Example:
		>>> 
		>>> p.sha256()
		'8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef'
		>>> 

		"""
		return self.hash('sha256', blocksize or self.blocksizer())
	

	#
	#
	# SHA-512
	#
	#
	def sha512(self, blocksize=None):
		"""
		Hash using sha512 algo.
		
		Example:
		>>> 
		>>> p.sha512()
		
		"""
		return self.hash('sha512', blocksize or self.blocksizer())
	
	
	#
	#
	# BLOCK-SIZER
	#
	#
	def blocksizer(self, path=None):
		"""
		Recommended block size (4K-16M), based on size of file.
		
		This method is overwhelmingly for internal use. The algorithm is
		completely based on my own intuition, and on some trial and error
		experiments. It's intended to provide the fastest hashing results
		with the minimum use of memory.
		
		EXAMPLE:
		>>> 
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath() )
		>>> p('__main__.py').blocksizer() # 215 bytes
		1024
		>>> p('LICENSE').blocksizer()     # 34.5k
		65536
		>>> 
		
		"""
		sz = ospath.getsize(path or self.path)
		for x in [10,11,12,13,14,16,17,20,22]:
			blocksize = 2**x
			if sz < blocksize:
				return blocksize
		return 2**24 # max
	
	
	#
	#
	# SIZE
	#
	#
	def size(self, mergepath=None):
		"""
		Return the size of the file at this object's path.
		
		EXAMPLE:
		>>> 
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath("README.md") )
		
		"""
		p = self.merge(mergepath)
		return ospath.getsize(p)
	
	
	#
	#
	# STAT
	#
	#
	def stat(self, mergepath=None):
		"""
		Return file stat in a proplist.
		
		EXAMPLE:
		>>>
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath("README.md") )
		>>> p.stat()
		>>>
		
		"""
		merged_path = self.merge(mergepath)
		try:
			if self.pathtype == 'l':
				st = os.lstat(merged_path)
			else:
				st = os.stat(merged_path)
				
		except FileNotFoundError:
			raise FileNotFoundError(xdata(
					err="file-not-found", path=mergepath
				))
		
		# return status
		return st
	
	
	#
	#
	# STAT DICT
	#
	#
	@property
	def statd(self):
		"""
		Return a propdict containing stats.
		"""
		
		if self.pathtype == 'l':
			x = trix.propx.proplist(os.lstat(self.p))
		else:
			x = os.stat()
		
		return trix.ncreate("util.propx.propdict.propdict", dict(
				st_mode  = x.st_mode,
				st_ino   = x.st_ino,
				st_dev   = x.st_dev,
				st_uid   = x.st_uid,
				st_gid   = x.st_gid,
				st_size  = x.st_size,
				st_atime = x.st_atime,
				st_mtime = x.st_mtime,
				st_ctime = x.st_ctime,
				pathtype = self.pathtype
			)
		)
	
	
	#
	#
	# EXISTS
	#
	#
	def exists(self, mergepath=None):
		"""
		Returns `True` if path exists.

		Pass `mergepath` string to append string aditional path elements.
		
		Example:
		>>> 
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath() )
		>>> p.exists()
		True
		>>> p.exists("fs")
		True
		>>> 
		
		"""
		return ospath.exists(self.merge(mergepath))
			

	#
	#
	# DIR
	#
	#
	def dir(self, mergepath=None):
		"""
		Return an `fs.dir.Dir` object for the given path. 

		Pass `mergepath` string to append string aditional path elements.
		
		Example:
		>>> 
		>>> from trix.fs import *
		>>> p = Path( trix.innerfpath() )
		>>> p.dir("fs")
		<trix.fs.dir.Dir '/home/nine/trix/fs' (d)>
		>>> 
		
		"""
		return trix.ncreate('fs.dir.Dir', self.merge(mergepath))
	
	
	#
	#
	# WRAPPER
	#
	#
	def wrapper(self, **k):
		"""
		Returns a File-based object wrapping the fs object at this
		path. The default for files whose mime type can't be matched 
		here is fs.file.File.
		
		EXAMPLE 1:
		>>> 
		>>> from trix.fs import *
		>>> x = Path( trix.innerfpath('README.md') ).wrapper()
		>>> r = x.reader(encoding='utf-8')
		>>> r.readline()
		>>> r.readline()
		>>> r.readline()
		>>> r.read()
		>>> 
		
		"""
		
		# MIME, VALIDATION
		if self.isdir() or self.ismount():
			raise Exception('open-fail', xdata(
				path=self.path, reason='file-required', k=k
			))
		
		mm = self.mime
		
		# Application
		if mm.type == 'application':
			
			# tar, tar.bz2, tar.gz, tgz
			if mm.subtype == 'x-tar':
				return trix.ncreate('fs.tar.Tar', self.path, **k)
			
			# zip
			elif mm.subtype == 'zip':
				return trix.ncreate('fs.zip.Zip', self.path, **k)
			
			# xlsx - for now, use zip, but there may be room for improvement
			elif mm.subtype == 'vnd.openxmlformats-officedocument.spreadsheetml.sheet':
				return trix.ncreate('fs.zip.Zip', self.path, **k)
	
		# encoded
		elif mm.enc == 'bzip2':
			return trix.ncreate('fs.bzip.Bzip', self.path, **k)	
		
		# gzip
		elif mm.enc == 'gzip':
			return trix.ncreate('fs.gzip.Gzip', self.path, **k)
		
		#
		# Default - for plain text or, as a default, any kind of file
		#
		return trix.ncreate('fs.file.File', self.path, **k)
	
	
	#
	#
	# READER
	#
	#
	def reader(self, **k):
		"""
		Return an object of class `trix.util.stream.reader.Reader`.
		
		Return a Reader for this object's path based on the mime type of
		the file there. If this Path object points to a tar or zip file,
		a member keyword must specify the member to read. In such cases,
		the returned Reader object will be suitable to the mime type of
		the specified member (as far as is supported by the fs package).
		
		Encoding-related kwargs are extracted and sent to the reader when
		it's created. All other (not encoding-related) kwargs are used to
		create any wrappers that may be needed to create this reader. 
		
		NOTE: Do not specify a 'mode'; this method must always rely on
		      the default mode for the type of wrapper that represents 
		      the file at this path.
		"""
		
		# Files with members will need to create a different kind of
		# object from what gets returned. Pop that key out of kwargs
		# before calling `wrapper`.
		member = k.pop('member', None)
		
		# now get the file wrapper object and return a reader
		wrapper = self.wrapper(**k)
		
		
		# -- container wrapper handling (tar/zip) --
		
		# If member is passed, it is required; the file type wrapper must
		# have a 'names' property.
		if member:
			try:
				wrapper.names
			except Exception as ex:
				raise type(ex)('fs-reader-fail', xdata(k=k, path=self.path,
						reason='fs-non-container', member=member, wrapper=wrapper
					))
			
			# make sure the specified member exists in the tar/zip file
			if not member in wrapper.names:
				raise KeyError('fs-reader-fail', xdata(k=k, path=self.path,
						reason='fs-non-member', member=member, wrapper=wrapper
					))
			
			# get correct file class by calling wrapper on member
			try:
				mpath = Path(member, affirm=None)
				
				# get a wrapper suitable to the member's filename
				mwrap = mpath.wrapper()
			except:
				# default is plain File
				mwrap = ncreate('fs.file.File')
			
			# get the original 'owner' stream for the memberwrapper to use
			ownerstream = wrapper.reader(member=member).detach()
			
			# create the member's wrapper
			try:
				rr = mwrap.reader(stream=ownerstream, **k)
			except BaseException as ex:
				raise type(ex)("err-reader-fail", ex.args, xdata(
						mpath=mpath, mwrap=mwrap, member=member,
						ownerstream=ownerstream
					))
			
			return rr
		
		# -- non-contaner handling --
		return wrapper.reader(**k)
	
	
	@classmethod
	def expand(cls, path=None, **k): # EXPAND
		"""
		Returns an absolute path.
		
		Keyword 'affirm' lets you assign (or restrict) actions to be
		taken if the given path does not exist. 
		 * checkpath - default; raise if parent path does not exist.
		 * checkfile - raise if `path` doesn't specify an existing file.
		 * checkdir - raise if full given path does not exist.
		 * makepath - create parent path as directory if none exists.
		 * makedirs - create full path as directory if none exists.
		 * touch - create a file at the given path if none exists.
		
		To ignore all validation, pass affirm=None.
		
		"""
		
		if 'affirm' in k:
			if k['affirm'] not in VALID_AFFIRM:
				raise ValueError("invalid-expand-selector", xdata(
					affirm  = k.get('affirm'),
					message = "Invalid keyword argument.",
					detail  = "`trix.fs.Path.expand`",
					__doc__ = cls.expand.__doc__
				))
		
		OP = ospath
		if path in [None, '.']:
			path = os.getcwd()
		
		if not OP.isabs(path): # absolute
			path = OP.expanduser(path)
			if OP.exists(OP.dirname(path)): # cwd
				path = OP.abspath(path)
			else:
				path = OP.abspath(OP.normpath(path))
		
		v = k.get('affirm', "checkpath")
		if (v=='checkfile') and (not OP.isfile(path)):
			raise ValueError('not-a-file', {'path' : path})
		elif (v=='checkpath') and (not OP.exists(OP.dirname(path))):
			raise ValueError('no-such-path', {'path' : OP.dirname(path)})
		if v:
			if OP.exists(path):
				if (v=='checkdir') and (not OP.isdir(path)):
					raise ValueError('not-a-directory', {'path' : path})
			else:
				if (v=='checkdir'):
					raise ValueError('no-such-directory', {'path' : path})
				elif v in ['makepath', 'touch']:
					if not OP.exists(OP.dirname(path)):
						os.makedirs(OP.dirname(path))
					if v == 'touch':
						Path(path).wrapper().touch()
				elif (v=='makedirs'):
					os.makedirs(path)
		
		return path




# -------------------------------------------------------------------
#
#
# FILE BASE
#
#
# -------------------------------------------------------------------

class FileBase(Path, EncodingHelper):
	"""
	Common methods `fs.file.File` and subclasses will need.
	
	This object provides the most basic needs for the system of
	subclasses that implement the opening of various types of files.
	
	FileBase can create, touch, move, rename, and remove files, and 
	provides the bases of these actions to subclasses. Apart from a
	utility "dir" method, that returns the directory in which a file
	is contained, that's about the extent of it.
	
	However, being based on Path, all the Path class methods are 
	available to FileBase and its subclasses. The only exception is
	that the Path.setpath method is disabled, since use of the `setpath` 
	method would corrupt the object's integrity.
	
	"""
	
	#
	# INIT
	#
	def __init__(self, path=None, **k):
		"""Pass file path with optional keyword arguments."""
		
		#
		# If `affirm` is "touch", prepare for its handling after Path is
		# initialized. By resetting the affirm value to 'makepath', the
		# way is clear for this object to call it's class-specific
		# `touch` method after Path is initialized here.
		#
		touch = (k.get('affirm') == 'touch')
		if touch:
			k['affirm'] = 'makepath'
		
		# init superclasses
		EncodingHelper.__init__(self, **k)
		Path.__init__(self, path, **k)
		
		# handle touch, if necessary
		if touch and not self.exists():
			self.touch()
	
	
	#
	# DIR
	#
	def dir(self, path=None):
		"""
		Return a dir.Dir object for the directory containing this file. 
		Pass path string (default None) to merge from the directory
		containing this file.
		"""
		return trix.ncreate('fs.dir.Dir', self.merge('..')).dir(path)
	
	
	#
	# SET PATH - prevent changing path
	#
	def setpath(self, path):
		"""Prevents changing of this file wrapper's path. """
		raise ValueError('fs-immutable-path', xdata())

	
	#
	# TOUCH - touch file without possibility of "merging" the path.
	#
	def touch(self, times=None):
		"""
		Touch the file at this path.
		
		Unlike the `Path.touch` method, which can touch files within a 
		directory path, the FileBase `touch` method can touch only itself.
		
		
		"""
		with open(self.path, 'a'):
			os.utime(self.path, times)  
	
	
	#
	# COPY
	#
	def copy(self, dest, **k):
		"""Copy this file to string path `dest`."""
		src = self.path
		dst = self.dir().merge(dest)
		try:
			shutil.copyfile(src, dst)
			if k.get('stat'):
				shutil.copystat(src, dst)
			if k.get('mode'):
				shutil.copymode(src, dst)
		except Exception as ex:
			raise type(ex)(ex.args, xdata(src=src, dst=dst, dest=dest, k=k))
	

	#
	# MOVE
	#
	def move(self, dest):
		"""Move this file from it's current location to path `dest`."""
		src = self.path
		dst = self.expand(self.dir().merge(dest))
		try:
			shutil.move(src, dst)
			Path.setpath(self, dst)
		except Exception as ex:
			raise type(ex)(ex.args, xdata(src=src, dst=dst, dest=dest))
	

	#
	# RENAME
	#
	def rename(self, dest):
		"""Rename this file (moving it, if appropriate)."""
		src = self.path
		dst = self.dir().merge(dest)
		try:
			os.rename(src, dst)
			Path.setpath(self, dst)
		except Exception as ex:
			raise type(ex)(ex.args, xdata(src=src, dst=dst, dest=dest))
	

	#
	# REMOVE
	#
	def remove(self):
		"""Delete this file."""
		os.remove(self.path)





