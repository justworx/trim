#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .bfile import *


class Gzip(BFile):
	"""
	Access and manipulate gzip files.
	
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
		>>>
		>>> import trix
		>>>
		>>> #
		>>> # Create a test file name and make a Path object
		>>> #
		>>> filename = "~/test-%s.gz"%trix.value('time.time')()
		>>> p = trix.path(filename, affirm="touch")
		>>>
		>>> #
		>>> # Create a file wrapper.
		>>> #
		>>> w = p.wrapper()
		>>> w.write("Hello, world!\n", encoding='utf8')
		>>> w.read()
		>>> #
		>>> #  Because an encoding is specified to neither the wrapper 
		>>> #  nor the `read` method, the result is returned as bytes.
		>>> #
		b'Hello, world!\n'
		>>>
		>>> #
		>>> # This time we'll specify an encoding to the wrapper.
		>>> #
		>>> w = p.wrapper(encoding='utf8')
		>>> w.write("Hello, world!\n")
		>>> w.read()
		'Hello, world!\n'
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
	
	# GZ OPEN
	def open(self, mode=None, **k):
		"""
		Return a gzip file pointer.
		
		Optional keyword argument `compresslevel` defaults to 9.
		
		"""
		ok = trix.kcopy(k, "compresslevel")
		return trix.create("gzip.GzipFile", self.path, mode, **ok)
	
	# TOUCH
	def touch(self, times=None):
		"""Make sure file exists. If `times` is set, touch."""
		if not self.exists():
			with self.open("a") as fp:
				fp.write(b'')
				fp.flush()
				fp.close()
		
		# apply timestamp
		if times:
			BFile.touch(self, times)


