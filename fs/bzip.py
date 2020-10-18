#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .file import *
import bz2


class Bzip(File):
	"""
	Access and manipulate bz2 files.
		
		EXAMPLE:
		>>> from trix.fs.bzip import *
		>>> testfile = "~/test-%s.bz2"%trix.value('time.time')()
		>>> 
		>>> f = Bzip(testfile, affirm="touch")
		>>> f.exists()
		True
		>>> 
		>>> f.write("Hello, world!\n")
		>>> f.read()
		b'Hello, world!\n'
		>>> 
		>>> f.read(encoding='utf8')
		'Hello, world!\n'
		>>> 
		>>> f.read('r')
		'Hello, world!\n'
		>>> 
		>>> f.remove()
		>>> f.exists()
		False
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
