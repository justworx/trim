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
	
	Providing an "encoding" specification causes `Writer` and `Reader` 
	stream objects to translate the encoding from and to bytes before 
	returning or writing them to the contained stream. The following 
	table shows the type of data strings produced or consumed with 
	various combinations of "mode" and "encoding".

    MODE  ENCODING      I/O      NOTE 
    'r'                 unicode  decode with DEF_ENCODE
    'r'   encoding=enc  unicode  decode with <enc>
    'rb'                bytes    bytes are returned
    'rb'  encoding=enc  unicode  bytes are decoded after reading
    'w'                 unicode  encode with DEF_ENCODE
    'w'   encoding=enc  unicode  encode with <enc>
    'wb'                bytes    bytes are written
    'wb'  encoding=enc  unicode  bytes are encoded before writing
	
    EXAMPLE:
    
    import trix
    >>>
    >>> #
    >>> # Create a test file name and make a Path object
    >>> #
    >>> filename = "~/test-%s.txt"%trix.value('time.time')()
    >>> p = trix.path(filename, affirm="touch")
    >>>
    >>> #
    >>> # Create a file wrapper.
    >>> #
    >>> w = p.wrapper()
    >>> w.write("Hello, world!", encoding='utf8')
    14
    >>>
    >>> #
    >>> #  Because an encoding is specified to neither the wrapper 
    >>> #  nor the `read` method, the result is returned as bytes.
    >>> #
    >>> w.read()
    b'Hello, world!'
    >>>
    >>> #
    >>> # This time we'll specify an encoding to the wrapper.
    >>> #
    >>> w = p.wrapper(encoding='utf8')
    >>> w.write("Hello, world!")
    14
    >>> #
    >>> # Because wrapper `w` was constructed with a given encoding,
    >>> # that encoding is used as the default in calls to w.read()
    >>> # which lack a given encoding specification. The result will
    >>> # be returned as unicode text.
    >>> #
    >>> w.read()
    'Hello, world!'
    >>>
    >>> #
    >>> # Finally, we should clean up the test file.
    >>> #
    >>> w.remove()
    >>> 
    
    SEE ALSO:
    >>> from trix.util.reader import *
    >>> help(Stream)
    >>> help(Reader)
    
    SEE ALSO:
    >>> from trix.util.writer import *
    >>> help(Writer)
	
	""" 
	
	#
	#
	# OPEN
	#
	#
	def open(self, mode, **k):
		"""
		Return a file pointer fitting `mode`, kwargs, and default encoding
		as provided to this object's constructor.
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
		"""
		ek = self.applyEncoding(k) # apply default encoding
		k['mode'] = mode or ('r' if ek else 'rb')
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
		
		#
		# --------------- start here -----------------------
		#
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
		"""Return a Reader object."""

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
		"""Return a Writer object."""
		
		k = self.applyEncoding(k)
		
		k.setdefault('mode', "w" if self.ek else "wb")
		k.setdefault('encoding', DEF_ENCODE)
		try:
			# if stream is given, send kwargs directly to Writer()
			return Writer(k.pop('stream'), **k)
		except KeyError:
			# ...else get stream from self.open()
			return Writer(self.open(**k), **k)

