#
# Copyright 2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from trix.util.xiter import *
import os


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
	
	def __init__(self, path=None, **k):
		
		self.__k = k
		
		# start with some cleanup
		if not path:
			path = trix.innerfpath()
		
		self.__path = path
		self.__item = ()
		self.__count= 0
		self.__dir = trix.path(path) # returns an fs.Dir!
		
		xiter.__init__(self, os.walk(path))
	
	
	#
	#
	# __NEXT__
	#
	#
	def __next__(self):
		try:
			self.__item = xiter.__next__(self)	
		except BaseException as ex:
			raise type(ex)('err-search-fail', xdata(
				path=self.__path, item=self.__item, k=self.__k
			))
	
	
	#
	#
	# PATH
	#
	#
	def path(self):
		return self.__dir[0]
	
	
	#
	#
	# BASEPATH
	#
	#
	def basepath(self):
		return self.__path # Dir[0] is the path to the directory itself
	
	
	# -----------------------------------------------------------------
	#
	#
	# RESULTS
	#
	#
	# -----------------------------------------------------------------
	
	#
	#
	# ITEM
	#
	#
	def item(self):
		return self.__item
	
	
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
	# DIR
	#
	#
	def dir(self):
		return self.__item[0]
	
	
	#
	#
	# DIRS
	#
	#
	def dirs(self):
		return self.__item[1]
	
	
	#
	#
	# FILES
	#
	#
	def files(self):
		return self.__item[2]

	
