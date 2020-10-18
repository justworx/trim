#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .file import *


class Gzip(File):
	"""
	Access and manipulate gzip files.
		
		EXAMPLE:
		>>> 
		>>> from trix.fs.gzip import *
		>>> testfile = "~/test-%s.gz"%trix.value('time.time')()
		>>> 
		>>> f = Gzip(testfile, affirm="touch")
		>>> f.exists()
		True
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
		
	"""
	
	# 
	# 
	# GZ OPEN
	# 
	# 
	def open(self, mode=None, **k):
		"""
		Returns a gzip file pointer.
		
		Optional keyword argument `compresslevel` defaults to 9.
		
		"""
		k.setdefault("compresslevel", 9)
		ok = trix.kcopy(k, "compresslevel")
		return trix.create("gzip.GzipFile", self.path, mode, **ok)
	
	
	# 
	# 
	# TOUCH
	# 
	# 
	def touch(self, times=None):
		"""
		Make sure file exists. If `times` is set, touch.
		"""
		if not self.exists():
			with self.open("a") as fp:
				fp.write(b'')
				fp.flush()
				fp.close()
		
		# apply timestamp
		if times:
			File.touch(self, times)


