#
# Copyright 2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from trix.util.xiter import *
import os, fnmatch


# -------------------------------------------------------------------
#
#
# SEARCH
#
#
# -------------------------------------------------------------------

class Search(xiter):
	"""
	UNDER CONSTRUCTION!
	
	A file searching class.
	
	This `Search` class is the workhorse for a `search` classmethod,
	coming soon, which will execute full file searches based on fmatch
	patterns, returning selected results.
	
	EXAMPLE
	>>> from trix.fs.search import *
	>>> s = Search("trix/fs")
	>>> s.next()
	>>> s.dict()
	{
	  "dir": "trix/fs",
	  "dirs": [
	    "__pycache__"
	  ],
	  "files": [
	    "__init__.py",
	    "archive.py",
	    "bzip.py",
	    "dir.py",
	    "file.py",
	    "gzip.py",
	    "search.py",
	    "strings.json",
	    "tar.py",
	    "zip.py"
	  ]
	}
	>>>
	
	"""				
	
	
	#
	#
	# 
	#
	#
	def __init__(self, path=None, **k):
		"""
		Search for files.
		
		The `Search` class uses `os.walk` to find files based on fnmatch
		patterns. Walk the list one by one, or pass a pattern keyword
		argument and call `search()` to receive a list of file paths that
		match the given pattern. 
		
		EXAMPLE:
		>>> from trix.fs.search import *
		>>> s = Search(trix.npath().path, p="*.conf")
		>>> s.search().display()
		[
		  "/home/nine/trix/app/config/example.conf",
		  "/home/nine/trix/app/config/app.conf",
		  "/home/nine/trix/app/config/console.conf",
		  "/home/nine/trix/app/config/service/en.service.conf"
		]
		>>> 
		
		"""
		
		self.__k = k
		
		# start with some cleanup
		if not path:
			path = trix.path("~/").path
		
		self.__path = path
		self.__item = ()
		self.__count= 0
		self.__dir = trix.path(path) # returns an fs.Dir!
		
		self.__pattern = k.get('p', k.get('pattern'))
		if self.__pattern:
			self.search = self.__search
			self.__matches = []
			self.__next__ = self.__next_pat
		else:
			self.__next__ = self.__next 
		
		xiter.__init__(self, os.walk(path))


	
	#
	#
	# __NEXT
	#
	#
	def __next(self):
		"""
		This is the ultimate iterator. It can not be replaced. It provides
		content for the various "next" methods, below.
		
		"""
		try:
			self.__item = xiter.__next__(self)
			self.__count += 1
			
		except BaseException as ex:
			raise type(ex)('err-search-fail', xdata(
				path=self.__path, item=self.__item, k=self.__k
			))
	
	
	#
	#
	# __NEXT_PAT
	#
	#
	def __next_pat(self):
		"""
		Filter by pattern.
		
		EXAMPLE
		>>> from trix.fs.search import *
		>>> s = Search("trix/fs", pattern="*.py")
		>>> s.next()
		>>> s.item.display()
	
		"""
		#
		# Calling `next` is going to give the full dict.
		#
		self.__next()
		
		#
		# Filter the files, then add them to `self.__matches`.
		#
		results = fnmatch.filter(self.files(), self.__pattern)
		
		for r in results:
			
			# Matches are given as a full file path.
			self.__matches.append("%s/%s" % (self.__item[0], r))
	
	
	#
	#
	# __SEARCH
	#
	#
	def __search(self):
		"""
		Loop until StopIteration.
		
		All files matching `pattern` will be returned as file paths
		stored in the self.matches proplist.
		"""
		try:
			while True:
				self.next()			
		except StopIteration:
			return self.matches
	
	
	#
	#
	# NEXTS
	#
	#
	def nexts(self):
		"""
		Calls the current `self.__next__` (whether __next or __next_pat)
		and then returns self. This is to allow call-chaining. It's most
		useful for debugging.
		"""
		self.__next__()
		return self
	
	
	#
	#
	# MATCHES
	#
	#
	@property
	def matches(self):
		"""
		Returns proplist containing `k` matches.
		
		This list will be populated only if a pattern keyword argument
		was specified to the constructor.
		"""
		try:
			return trix.propx(self.__matches)
		except:
			return None
	
	
	#
	#
	# K - Keyword Argument dict
	#
	#
	@property
	def k(self):
		"""Returns propdict containing `k`. Call as a method."""
		return trix.propx(self.__k)
	
	
	#
	#
	# PATH
	#
	#
	def path(self):
		"""
		Returns the path at the current point of iteration - the most
		recent call to `next`.
		"""
		return self.__dir[0]
	
	
	#
	#
	# BASEPATH
	#
	#
	def basepath(self):
		"""
		Returns the path given to the constructor
		"""
		return self.__path
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# RESULTS
	#
	#
	# -----------------------------------------------------------------
	
	#
	#
	# DICT
	#
	#
	@property
	def dict(self):
		itm = self.__item
		return trix.propx({
			"dir": itm[0],
			"dirs": sorted(itm[1]),
			"files": sorted(itm[2])
		})
	
	
	#
	#
	# ITEM
	#
	#
	@property
	def item(self):
		return trix.propx(self.__item)
	
	
	#
	#
	# DIR
	#
	#
	@property
	def dir(self):
		return trix.propx(self.__item[0])
	
	
	#
	#
	# DIRS
	#
	#
	@property
	def dirs(self):
		return trix.propx(self.__item[1])
	
	
	#
	#
	# FILES
	#
	#
	@property
	def files(self):
		return trix.propx(self.__item[2])
