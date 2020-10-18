#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

#
#   === Looks like this class can be removed completely ===
#   ===    It adds/removes/changes nothing from File.   ===
#

from .file import *


class BFile(File):
	"""
	BFile wraps python file classes that accept and produce only bytes.
	
	The `BFile` class supports descendents that don't allow the 'r' 
	mode. In other words, classes which accept only bytes for writing, 
	and which read back only bytes. This includes python's gzip and 
	bzip classes as well as the members of python's tar and zip class 
	objects.
	
	Pass optional defaults for encoding and errors as keyword
	arguments. These will be stored for use with the reading and 
	writing methods (but internally, the file opening object will 
	always open for reading bytes).
	
	NOTE:
	The purpose of `BFile` is *NOT* to prevent file reads from being 
	returned as unicode, but in fact to allow it, so as to make itself 
	(and its subclasses) part of set of classes that facilitate a common 
	system of calling conventions.
	
	If an encoding is provided, unicode may be passed to the write
	method and received from the read method.
	
	If mode 'r' is specified but no encoding is specified, the 
	`trix.DEF_ENCODE` value will be used for conversion to and from
	bytes as necessary.
	
	This allows files thought of as being "bytes only" to respond in 
	the same way as other file class wrappers when given the same set 
	of arguments.
	
	EXAMPLE:
	>>> from trix.fs.bfile import *
	>>> bf1 = BFile("~/test/bfile1.txt", affirm='touch')
	>>> bf1.write("Here's some unicode.", encoding='utf8')
	>>> bf1.read()
	b"Here's some unicode."
	>>> bf1.read(encoding="utf8")
	"Here's some unicode."
	>>> bf1.remove()
	>>> 
	
	"""
	
	#
	#
	# INIT
	#
	#
	def __init__(self, path, **k):
		"""
		Base files that accept and produce only bytes.
		"""
		#
		# REM: Mode is passed by keyword argument to the writer and reader
		#      methods. It's passed as an argument to read() and write().
		#
		File.__init__(self, path, **k)
	
	
	#
	#
	# WRITER
	#
	#
	# def writer(self, **k):
		# """
		# Return a writer given `path` and keyword arguments, but opened in 
		# bytes mode.
		
		# If a default encoding was given to the constructor, that will be
		# used to encode unicode text to be writen to the file.
		
		# NOTE:
		# Keyword argument `encoding` given to the `writer` method would 
		# override potential encodings provided to the constructor.
		
		# """
		# self.applyEncoding(k)
		# k.setdefault('mode', "w" if k.get('encoding') else "wb")
		
		# return File.writer(self, stream=self.open("wb"), **k)
	
	
	#
	#
	# READ
	#
	# 
	# def read(self, mode=None, **k):
		# """
		# Read and return complete file contents (from start).
		# """
		# #
		# # If mode is 'r', the trix.DEF_ENCODE value will be used to decode
		# # bytes to unicode before the result is returned.
		# #
		
		# self.applyEncoding(k)
		
		# if not mode:
			# if self.encoding:
				# mode = 'r'
			# else:
				# mode = 'rb'
		
		# #k.setdefault('mode', mode or "r" if k.get('encoding') else "rb")
		
		
		# return self.reader(**k).read()
	
	
	#
	#
	# READER
	#
	# 
	# def reader(self, **k):
		# """
		# Return a reader with given params, but opened in bytes mode.
		
		# If an encoding is given by keyword argument, it will be used to
		# convert results to unicode, overriding the same encoding value (if any) that had been passed to the constructor.
		
		# NOTE:
		# This may seem silly, but it does provide one potentially useful
		# benefit: The full range of encodings could be iterated through
		# one by one and eyeballed, eventually leading to the discovery of
		# an encoding that looks right.
		
		# In any case, it is consistent with calling conventions for all
		# File-based classes.
		
		# """
		# #
		# # "Given params" means encoding passed to constructor, overridden
		# # by any encoding passed to this method.
		# #
		# # It also means a 'mode' keyword specified by keyword args. To 
		# # prevent errors, the default for BFile-based objects is 'rb'
		# # unless there's an encoding - in which case it's 'r'.
		# #
		# # For BFile subclasses, the file stream itself is always opened in
		# # binary mode. Any conversion to unicode happens in the reader (if
		# # indicated by mode and encoding params).
		# #
		
		# # First, apply `self.ek` to `k` as defaults
		# self.applyEncoding(k)
		
		# # Then, calculate a default "mode" value
		# k.setdefault("mode", "r" if k.get('encoding') else "rb")
		
		# # Finally, return the reader that reads binary and converts it to
		# # unicode if appropriate.
		# return File.reader(self, stream=self.open("rb"), **k)
