#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *
from ..util.propx.proplist import *
import os, glob


class Dir(Path):
	"""
	Directory functionality.
	"""
	
	def __init__(self, path=None, **k):
		"""
		Pass an optional file system path. Default is '.'. Kwargs apply 
		as to Path.expand().
		"""
		p = k.get('dir', path)
		if not 'affirm' in k:
			k['affirm'] = 'checkdir'
		try:
			Path.__init__(self, p, **k)
		except Exception:
			raise ValueError('fs-invalid-dir', xdata(path=p)) 
		
		# requires py 2.6+
		self._walk = os.walk
	
	
	# GET ITEM - retrieve item path (string) by offset in directory.
	def __getitem__(self, key):
		"""
		Retrieve item path (string) by offset in directory.
		
		Dir objects can act as lists of the full path to the items inside
		the directory to which they point; Dir()[0] returns the full path
		to the first item in its directory listing.
		"""
		return self.merge(self.ls()[key])
	
	
	#
	# --- Multi-feature Properties -----------------------------------
	#
	@property
	def ls(self):
		"""
		When called as though it were a method, this property returns
		the list of items in this directory.
		
		```Dir().ls() # returns list of items in this directory```
		
		This property actually returns a proplist containing the 
		directory listing. See `help(Dir().ls)` for more options.
		"""
		return proplist(self.listshort)
	
	
	@property
	def list(self):
		"""
		When called as though it were a method, this property returns
		a list of lists, items  in this directory.
		
		```
		dir_list = trix.list()
		```
		
		When called as a property, it returns a propgrid object that
		features additional properties and methods for manipulating and
		displaying data from the directory listing.
		
		```
		plist = trix.path(trix.innerfpath()).list
		plist.grid()
		```
		
		See `help(Dir().ls)` for more details.
		
		"""
		return propgrid(self.listlong)
	
	
	#
	# --- Navigation -------------------------------------------------
	#
	
	def cd(self, path):
		"""Change directory the given path."""
		p = self.merge(path)
		if not os.path.isdir(p):
			raise Exception ('fs-not-a-dir', xdata(path=p))
		self.path = p
	
	
	#
	# --- Directory Manipulation -------------------------------------
	#
	
	def mkdir(self, path, *a):
		"""
		Create a directory described by path. If appended, additional 
		argument (mode) is passed on to os.makedirs().
		"""
		os.makedirs(self.merge(path), *a)
	
	
	# selection/action by pattern matches...
	
	# MV (move) 
	def mv(self, pattern, dst):
		"""
		Select contents of this directory that match `pattern` and 
		move to `dst`.
		"""
		for src in self.match(pattern):
			shutil.move(src, self.merge(dst))
	
	# RM (remove)
	def rm(self, pattern):
		"""
		Select contents of this directory that match `pattern` for 
		removal.
		"""
		for px in self.match(pattern):
			if os.path.isdir(px):
				shutil.rmtree(px)
			else:
				os.remove(px)
	
	
	# Directory manipulation features - applied to self.
	
	def copy(self, dst, symlinks=False, ignore=None):
		"""Use shutil.copytree to copy this directory."""
		shutil.copytree(self.path, dst, symlinks, ignore)
	
	def move(self, dst):
		"""Move this directory to path `dst`."""
		shutil.move(self.path, self.merge(dst))
	
	def rename(self, name):
		"""
		Rename this directory. Parents and contents remain unchanged.
		"""
		newname = self.merge("../%s" % name)
		self.move(newname)
		self.setpath(newname)
	
	
	
	#
	# --- Content Selection ------------------------------------------
	#
	
	
	#
	# MATCH
	#  - Select and return contents of this directory that match 
	#    `pattern`.
	#
	def match(self, pattern):
		"""Return matching directory items for the given pattern."""
		return glob.glob(self.merge(pattern))
	
	
	#
	# THIS NEEDS TO BE SPLIT UP
	#  - search() returns results
	#  - each() does actions
	#
	@property
	def search(self, pattern=None, **k):
		"""
		Search directories recursively starting at this directory path. 
		Return list of all paths unless matching `pattern`; default: *.*
		
		KEYWORD ARGUMENT:
		If `fn` keyword is specified, its value must be callable; this 
		callable will be called once for each result path. If args 
		keyword exists, it must be an array of values to be passed as 
		individual additional arguments to fn.
		
		WARNING: There is no 'confirm' or 'undo' when passing a 'fn'.     
		         ALWAYS CHECK the search results *without a function* 
		         BEFORE using it with a function.
		"""
		
		return proplist(self.listsearch, pattern, **k)
	
	
	#
	# --- Directory content access -----------------------------------
	#
	
	# READ - file/archive text
	def read(self, path, **k):
		"""
		Reads a file or archive member and returns full text.
		
		Keyword argument 'member' required for archive files (tar, zip).
		Optional encoding-related kwargs default to encoding='utf_8'.
		"""
		w = Path(self.merge(path)).wrapper(**k)
		return w.reader(**k).read()
	
	
	# HEAD - file/archive head 
	def head(self, path=None, **k):
		"""
		Return the initial lines of the given file. See help for 
		the Dir.headlines() method for details.
		
		Pass kwarg "lines" to specify the number of lines (default: 9)
		"""
		return self.headlines(path, **k).text()
	
	
	# HEAD LINES
	def headlines(self, path=None, **k):
		"""
		Returns a proplist containing the top lines from given file path,
		which may be a full path or relative to this directory.
		
		Keyword argument 'member' required for archive files (tar, zip).
		Optional encoding keyword argument defaults to DEF_ENCODE.
		Optional kwarg 'lines' specifies number of lines (default: 9).
		"""
		# make it text
		k.setdefault('encoding', DEF_ENCODE)
		
		p = Path(self.merge(path)) if path else self
		w = p.wrapper(**k)
		r = w.reader(**k)
		
		ct = k.get('lines', 9)
		rr = []
		for x in range(0, ct):
			line = r.readline()
			if not line:
				break
			rr.append(line)
		
		return proplist(rr)
	
	
	#
	# Raw Data Generation
	#
	def listshort(self, path=None):
		"""Returns a python list of directory entries at `path`."""
		return os.listdir(self.merge(path))
	
	
	def listlong(self, path=None, **k):
		"""
		Return extended directory listing as a list of lists, each
		containing name, type, size, uid, gid, atime, mtime, and ctime.
		"""
		h = ['name','type','size','uid','gid','atime','mtime','ctime']
		d = Path(self.merge(path)) if path else self
		
		# create result variable
		rr = []
		
		# append heading (if not forbidden by titles=False)
		if k.get('h', k.get('head', True)):
			rr.append(h)
		
		for item in d.ls():
			# get status
			x = Path(d.merge(item))
			stat = x.stat()
			
			# append item record
			rr.append([
				x.name,
				x.pathtype,
				stat.st_size,
				stat.st_uid,
				stat.st_gid,
				stat.st_atime,
				stat.st_mtime,
				stat.st_ctime,
			])
		
		return rr

	
	def listsearch(self, pattern=None, **k):
		
		path = self.path
		pattern = pattern or '*.*'
		
		#
		# Walk the directory path collecting results.
		# At each step:
		#  - d = current dir path;
		#  - dd = contained dir;
		#  - ff = contained files;
		#
		rlist = []
		
		#
		# NOTE: Replace with something like this to prevent os from 
		#       being loaded until necessary:
		# ```
		# walker = trix.create('os.walk')
		# for d,dd,ff in walker(pattern, **k)...
		# ```
		#
		for d, dd, ff in self._walk(path):
			rlist.extend(self.match(os.path.join(d, pattern)))
		
		# Handle action provided by kwarg `fn` (see WARNING above!)
		if 'fn' in k:
			fn = k['fn']
			for fpath in rlist:
				rr = {}
				aa = k.get('args', [])
				fn(fpath, *aa)
		
		# or, if no function was provided, just return the list.
		else:
			return rlist
