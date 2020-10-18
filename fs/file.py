#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import * # trix, mime, enchelp
from ..util.stream.reader import Reader
from ..util.stream.writer import Writer
from ..util.open import Opener



class File(FileBase):
	"""
	Access and manipulate plain files.
		
		EXAMPLE:
		>>> 
    >>> testfile = "~/test-%s.txt"%trix.value('time.time')()
		>>> 
		>>> from trix.fs.file import *
		>>> f = File(testfile, affirm="touch")
		>>> f.write("Hello, world!\n")
		>>> f.read()
		b'Hello, world!'
		>>> 
		>>> f.remove()
		>>> f.exists
		False
		>>>
	
	"""
	
	
	#
	#
	# OPEN
	#
	#
	def open(self, mode, **k):
		"""
		The `open` method opens a file.
		
		Pass `mode` as 'r', 'rb', 'w', or 'wb'.
		
		Valid keyword arguments include those accepted by stream 
		objects. Typically "encoding" and "errors". See help for 
		`trix.util.streams.Streams` for additional information.
	
		Providing an "encoding" specification causes reading and writing
		methods to translate the encoding to and from bytes as 
		appropriate. 
		
		The following table shows the type of data strings produced or 
		consumed given various combinations of "mode" and "encoding".
		
	    MODE  ENCODING      I/O      NOTE 
	    'r'                 unicode  decode with DEF_ENCODE
	    'r'   encoding=enc  unicode  decode with <enc>
	    'rb'                bytes    bytes are returned
	    'rb'  encoding=enc  unicode  bytes are decoded after reading
	    'w'                 unicode  encode with DEF_ENCODE
	    'w'   encoding=enc  unicode  encode with <enc>
	    'wb'                bytes    bytes are written
	    'wb'  encoding=enc  unicode  bytes are encoded before writing
		
		NOTE:
		Open and close are called automatically by all File-based 
		reading and writing methods. Unless an actual python file 
		pointer is needed as such, there's no reason to call `open` 
		directly.
		
		 * Use the `read` method to read full file contents.
		 * Use the `reader` method to read files line by line, character
		   by charactr, or in cases where you might want to seek various 
		   specific positions in the file.
		 * Use the `write` method to replace the full content of a file.
		 * Use the `writer` method to write to specific locations in a 
		   file.
		
		"""
		if not mode:
			raise Exception('err-open-fail', xdata(reason='mode-required'))
		if 'b' in mode:
			return Opener.open(self.path, mode, **self.sansEncoding(k))
		else:
			k.setdefault('encoding', DEF_ENCODE)
			return Opener.open(self.path, mode, **self.applyEncoding(k))
	
	
	#
	#
	# READ
	#
	#
	def read(self, mode=None, **k):
		"""
		Read complete file contents (from start).
		
		DEFAULTS:
		 * If mode is None and an encoding is given, mode defaults to 'r'.
		 * If mode is None and no encoding is given, mode defaults to 'rb'.
		 * Otherwise, `mode` is passed as given.
		
		"""
		
		#
		# MODE
		#  - Here we're building a "mode" to pass as a default keyword  
		#    argument to the `self.reader` method.
		#
		if not mode:
			if "encoding" in k:
				mode = "r"
			else:
				mode = "rb"
		
		#
		# apply default encoding and/or errors to the `ek` variable
		#
		ek = self.applyEncoding(k)
		
		#
		# PREPARE KWARGS FOR `Reader`.
		#
		# Set the given mode (if any) into a keyword arument. If the mode
		# is not given using the `mode` argument, 
		#
		k['mode'] = mode
		
		#
		# Use `Reader` to read the entire file contents.
		#
		with self.reader(**k) as r:
			return r.read()
	
	
	#
	#
	# WRITE
	#
	#
	def write(self, data, mode=None, **k):
		"""
		Write complete file contents.
		"""
		ek = self.applyEncoding(k)
		k['mode'] = mode or ('w' if ek else 'wb')
		
		with self.writer(**k) as w:
			i = w.write(data)
			w.flush()
			return i
	
	
	#
	#
	# READER
	#
	#
	def reader(self, **k):
		"""
		Return a `trix.util.stream.reader.Reader` object.
		
		Return a `Reader` object for this file. Pass keyword arguments
		"mode", "encoding", and "errors".
		
		SEE ALSO:
		>>> from trix.util.stream.reader import *
		>>> help(Reader)
		
		
		"""

		#
		# APPLY DEFAULT ENCODING (as given to File constructor)
		#  - encoding/errors in k, with self.ek applied as defaults
		#
		k = self.applyEncoding(k)
		
		#
		# MODE
		#  - If there's an encoding specification, let the default mode 
		#    for opening the stream be `self.rt`. Absent a specified 
		#    encoding, use as default mode `rb`.
		# 
		k.setdefault('mode', 'r' if k.get('encoding') else 'rb')
		
		#
		# GET STREAM
		#
		try:
			# if stream is given, send kwargs directly to constructor
			stream = k.pop('stream')
		except KeyError:
			# otherwise, a stream should be opened by this File object.
			stream = self.open(**k)
			
		return Reader(stream, **k)
	
	
	#
	#
	# WRITER
	#
	#
	def writer(self, **k):
		"""
		Return a Writer object.
		
		SEE ALSO:
		>>> from trix.util.stream.writer import *
		>>> help(Writer)
		
		"""
		
		k = self.applyEncoding(k)
		
		k.setdefault('mode', "w" if self.ek else "wb")
		k.setdefault('encoding', DEF_ENCODE)
		try:
			# if stream is given, send kwargs directly to Writer()
			return Writer(k.pop('stream'), **k)
		except KeyError:
			# ...else get stream from self.open()
			return Writer(self.open(**k), **k)

