#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *
import os, glob, fnmatch


class Dir(Path):
	"""Directory query/access/manipulation."""
	
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
		Returns proplist containing names of files in this directory.
		
		When called as though it were a method, this property returns
		the list of items in this directory.
		
		```Dir().ls() # returns list of items in this directory```
		
		This property actually returns a proplist containing the 
		directory listing. See `help(Dir().ls)` for more options.
		"""
		return trix.propx(self.listshort())
	
	
	@property
	def list(self):
		"""
		Returns proplist containing extended information on items in this
		directory.
		
		When called as though it were a method, this property returns
		a list of lists - the items in this directory.
		
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
		return trix.propx(self.listlong())
	
	
	@property
	def paths(self):
		"""
		Return proplist containing the fullpath of each item in this
		directory.
		"""
		return trix.propx(list(self.pathgen()))
	
	
	
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
	def search(self, query=None, **k):
		"""
		Search directories recursively starting at this directory path. 
		Return list of all paths, or matching `query` results if given.
		See `searchgen` for query options.
		"""
		return trix.propx(list(self.searchgen(query, **k)))
	
	
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
		
		return trix.propx(rr)
	
	
	
	#
	# --- Raw Data Generation ----------------------------------------- 
	#
	
	# LIST SHORT
	def listshort(self, path=None):
		"""Returns a python list of directory entries at `path`."""
		return os.listdir(self.merge(path))
	
	
	# LIST LONG
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
	
	
	#
	# GENERAOTRS (for paths and searches)
	#
	
	def pathgen(self):
		"""Generator; Yields full filepaths within this directory."""
		for item in self.listshort():
			yield (self.merge(item))
	
	
	def searchgen(self, query=None, **k):
		"""
		Walk the directory path yielding results as specified by the
		`query` argument.
		
		Valid results are yielded as a dict containing:
		 - d  : current dir path;
		 - dd : list of directories in `d`;
		 - ff : list of files in `d`;
		
		Result set depends on the value of `query`:
		 * When `query` is None, all file system objects contained in the
		   `self.path` directory are yielded.
		 * When `query` is an `fnmatch` pattern string, only results 
		   matching the filepath pattern are included in the 'files' list.
		 * When `query` is a callable, the d, dd, and ff arguments are 
		   passed for each file system object, and yielded if callable
		   returns a result that evaluates to True.
		
		NOTE ALSO: 
		When query is an fnmatch pattern string and keyword argument 
		`matchcase` is True, fnmatchcase is used instead of fnmatch, so
		selection of results will be case sensitive.
		
		"""
		path = self.path
		query = query or '*.*'
		rlist = []
		
		if not query:
			#
			# NO QUERY
			#  - If no `query` is provided, all files/directories within
			#    self.path are returned.
			#
			for d, dd, ff in os.walk(path):
				yield {'dir':d, 'dirs': dd, 'files':ff}
		
		elif callable(query):
			#
			# CALLABLE QUERY
			#  - If `query` is callable, selection criteria can be much more
			#    precise, using `d`, `dd`, and `ff` arguments to select both 
			#    directories and/or files to be part of the result set.
			#
			# NOTE that the callable query selection function may be used  
			# to select results based on any available criteria - just wrap 
			# each path in a `Path` object to select based on, for example,
			# modification date, file modes, file content, etc...
			#
			for d, dd, ff in os.walk(path):
				if query(d, dd, ff):
					yield {'dir':d, 'dirs': dd, 'files':ff}
		
		else:
			#
			# FN-MATCH QUERY
			#  - If `query` is a fnmatch pattern string, all subdirectories 
			#    are scanned, but only [files within those directories] that
			#    match the fnmatch pattern are selected. This is a simpler 
			#    way to select, based only on filepath patterns.
			#
			if k.get('matchcase') :
				fnmatchx = fnmatch.fnmatchcase
			else:
				fnmatchx = fnmatch.fnmatch
			
			for d, dd, ff in os.walk(path):
				files = []
				for fpath in ff:
					if fnmatchx(os.path.join(d, fpath), query):
						files.append(fpath)
				yield {'dir':d, 'dirs': dd, 'files':files}

