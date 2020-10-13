#
# Copyright 2018-2020 justworx
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
	
	# INIT
	def __init__(self, path, **k):
		"""
		Pass path to file.
		
		Optional Zip-related keyword arguments include:
		 * compression - default is ZIP_DEFLATED
		 * allowZip64  - allow zipfile size > 2GB; default: True
		
		Keyword arguments that apply as to `fs.Path.expand`:
		 * affirm (eg, affirm='touch')
		
		EXAMPLE:
		>>>
		>>> from trix.fs.zip import *
		>>> p = trix.path("~/test.zip", affirm="touch", encoding="utf8")
		>>> w = p.wrapper()
		>>> w.write("Test1", "This is a zip file test.\n")
		>>>
		"""
		Archive.__init__(self, path, **k)
		
		if 'pwd' in k:
			k['pwd'] = self.encode(k['pwd'])
		
		# open kwargs
		self.__openk = trix.kcopy(k, "compression allowZip64 pwd")
		self.__openk.setdefault('compression', DEF_COMPRESS)
		self.__openk.setdefault('allowZip64', DEF_ALLOW64)
	
	
	
	@property
	def openk(self):
		return dict(self.__openk)
	
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
	
	@property
	def members(self):
		"""
		Returns a list containing ZipInfo on each member.
		
		"""
		with self.archopen() as z:
			try:
				return z.infolist()
			finally:
				z.close()
	
	@property
	def memberinfo(self):
		"""
		Return a proplist with accessible member info in individual dicts.
		This is more for display than actual use. It can be helpful in
		assessing what's there.
		"""
		
		memdict = {}
		
		for item in self.members:
			itemdict = dict(
				is_dir         = item.is_dir(),
				filename       = item.filename,
				date_time      = item.date_time,
				compress_type  = item.compress_type,
				comment        = item.comment,
				extra          = item.extra,
				create_system  = item.create_system,
				create_version = item.create_version,
				reserved       = item.reserved,
				flag_bits      = item.flag_bits,
				volume         = item.volume,
				internal_attr  = item.internal_attr,
				external_attr  = item.external_attr,
				header_offset  = item.header_offset,
				CRC            = item.CRC,
				file_size      = item.file_size
			)
			
			memdict[item.filename] = itemdict
			
		return trix.propx(memdict)
		
		
	
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
	#
	# ARCH READ (Internal Use)
	#
	#  * Kwargs for ZipFile - Defaults from constructor
	#    - compression 
	#    - allowZip64
	#  * Kwargs for z.read():
	#    - pwd = optional password
	#    - mode = 'r', 'U'; default: 'rU'
	#
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
		"""Write member data from the `memgen` iterable."""
		
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


