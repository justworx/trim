#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import zipfile, weakref
from .archive import *

DEF_COMPRESS = zipfile.ZIP_DEFLATED
DEF_ALLOW64  = False


class Zip(Archive):
	"""
	Read/write Zip files.
	
	"""
	
	#	
	#	
	# INIT
	#	
	#	
	def __init__(self, path, **k):
		"""
		Pass path to file. Optional arguments include:
		 * compression - default is ZIP_DEFLATED
		 * allowZip64  - allow zipfile size > 2GB; default: True
		
		Keywords apply as to Path.expand().
		"""
		Archive.__init__(self, path, **k)
		
		if 'pwd' in k:
			k['pwd'] = self.encode(k['pwd'])
		
		# open kwargs
		self.__openk = trix.kcopy(k, "compression allowZip64 pwd")
		self.__openk.setdefault('compression', DEF_COMPRESS)
		self.__openk.setdefault('allowZip64', DEF_ALLOW64)
	
	
	#	
	#	
	# OPEN-K
	#	
	#	
	@property
	def openk(self):
		return dict(self.__openk)
	
	
	#	
	#	
	# NAMES
	#	
	#	
	@property
	def names(self):
		"""
		Member names in a proplist. Returns only the names of members
		currently existing in the archive.
		
		Call this property as a function to return the list of names. 
		See `trix.propx.proplist` for more calling options.
		
		```
		arch = trix.path("my_archive.zip")
		arch.names()                       # returns list
		arch.names.sorted.table(width=2)   # display member paths
		
		```
		"""
		with self.archopen() as z:
			try:
				nlist = z.namelist()
				return propx(nlist)
			finally:
				z.close()
	
	
	#	
	#	
	# MEMBERS
	#	
	#	
	@property
	def members(self):
		"""
		{'filename':ZipInfo}
		"""
		r = {}
		for x in self.zipinfo():
			r[x.filename] = x
		return propx(r)
	
	
	@property
	def zipinfo(self):
		"""
		Return a list of zipinfo objects as provided by python's zipfile
		module.
		"""
		with self.archopen() as z:
			try:
				return propx(z.infolist())
			finally:
				z.close()
	
	
	
	#
	# TEST
	#
	def test(self):
		"""Test zip file's integrity."""
		with self.open() as z:
			try:
				return z.testzip()
			finally:
				z.close()
	
	
	#
	# TOUCH
	#
	def touch(self, times=None):
		"""Touch zip file, initing the zip format for the file."""
		with self.archopen(mode='a') as z:
			z.close()
		Path.touch(self, times)
	
	
	#
	# ARCH READ
	#  * Kwargs for ZipFile - Defaults from constructor
	#    - compression 
	#    - allowZip64
	#  * Kwargs for z.read():
	#    - pwd = optional password
	#    - mode = 'r', 'U'; default: 'rU'
	#
	def archread(self, member, **k):
		"""Read directly from zip file."""
		
		kz = dict(self.openk)
		kz.update(k)
		
		# pwd
		ko = trix.kpop(kz, 'pwd') # pop before ZipFile()
		if 'pwd' in ko:
			# encode the password using `self.ek`
			ko['pwd'] = self.encode(ko['pwd'])
		
		# Create ZipFile, open file pointer, read/return, and close.
		with zipfile.ZipFile(self.path, "r", **kz) as z:
			return z.read(member, **ko)
	
	
	#
	# ARCH STORE
	#  * Kwargs for ZipFile - Defaults from constructor
	#    - compression 
	#    - allowZip64
	#
	def archstore(self, memgen, **k):
		"""
		Write member data from the `memgen` iterable to the zipfile.
		
		"""
		
		kz = dict(self.__openk)
		kz.update(k)
		kz.pop('pwd', None)
		
		with zipfile.ZipFile(self.path, "a", **kz) as z:
			try:
				for d in iter(memgen):
					z.writestr(d['member'], d['buffer'].read())
			finally:
				z.close()
	
	
	#
	# ARCH OPEN
	#
	def archopen(self, mode='r', **kz):
		"""Return an open file pointer - for utility purposes, mainly."""
		return zipfile.ZipFile(self.path, mode, **kz)


