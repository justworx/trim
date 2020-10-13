#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .bfile import *
import bz2


class Bzip(BFile):
	"""
	Access and manipulate bz2 files.
	
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
		>>> filename = "~/test-%s.bz2"%trix.value('time.time')()
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
		>>> w.read()
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
	
	# OPEN
	def open(self, mode=None, **k):
		"""
		Pass `mode` 'rb' or 'wb'. Optional compression level (1-9)
		defaults to 9. Optional encoding kwargs are used by the reader() 
		and writer() methods.
		"""
		ok = trix.kcopy(k, "compresslevel")
		return bz2.BZ2File(self.path, mode, **ok)
	
	# TOUCH
	def touch(self, times=None):
		"""Make sure file exists. If `times` is set, touch."""
		if not self.exists():
			with bz2.BZ2File(self.path, 'w'):
				pass
		if times:
			with bz2.BZ2File(self.path, 'a'):
				os.utime(self.path, times)
