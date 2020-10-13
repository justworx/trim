#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


import tarfile, fnmatch
from .archive import *


class Tar(Archive):
	"""
	Tar file support.
	
	EXAMPLE:
	>>>
	>>> import trix
	>>>
	>>> #
	>>> # Create a path object to a test file
	>>> #
	>>> p = trix.path("~/test.tar.gz", affirm="touch", encoding="utf-8")
	>>>
	>>> #
	>>> # Get a tar file wrapper, `z`.
	>>> #
	>>> z = p.wrapper()
	>>> 
	>>> #
	>>> # Create a member passing member name, "Test1", and some text.
	>>> #
	>>> z.write("Test1", "This is a test.\n")
	>>> 
	>>> #
	>>> # Until the `Tar.flush` method is called, no changes take place
	>>> # in the file, so `z.members` returns an empty dict.
	>>> #
	>>> z.members
	{}
	>>>
	>>> #
	>>> # After calling `flush()`, the member is in the archive.
	>>> #
	>>> z.flush()
	>>> z.members
	{'Test1': <TarInfo 'Test1' at 0x7f420065d9a8>}
	>>>
	>>> #
	>>> # After calling `flush()`, the member is in the archive.
	>>> #
	>>> z.read("Test1", encoding='utf8')
	'This is a test.\n'
	>>> z.read("Test1")
	'This is a test.\n'
	>>> 
	
	"""
	
	__DEF_ENC = dict(gzip='gz', bzip2='bz2')
	
	def __init__(self, path, **k):
		
		#
		# Store the compression kwarg in case affirm=='touch', which would
		# mean Archive.__init__ would call self.touch(), which would need
		# to call the self.compression property, which would need to know
		# the value of the 'compression' kwarg, if given here.
		#
		self.__compressionk = k.get('compression')
		
		# Now it's safe to call Archive.__init__ even if affirm=='touch'
		Archive.__init__(self, path, **k)
	
	
	@property
	def openk(self):
		"""
		Return a dict of 'openk' keyword arguments.
		"""
		return dict(compression=self.compression)
	
	
	@property
	def names(self):
		"""
		Member names in a proplist. Call this property as a function to
		return the list of names.
		
		>>> arch = trix.path("my_archive.tar.gz")
		>>> arch.names()                             # returns list
		>>> arch.wrapper.names.sorted.table(width=2) # displays member paths
		
		SEE ALSO:
		>>> from trix.propx.proplist import *
		>>> help(proplist)
		>>>
		
		```
		"""
		with self.archopen('r|*') as f:
			self.__names = f.getnames()
		return propx(self.__names)
	
	
	@property
	def compression(self):
		"""
		Return the compression string, 'gz', 'bz2', or ''
		"""
		#
		# This weirdness is because the touch() method, which may be 
		# called by Archive.__init__, needs to know the compression.
		# When affirm != 'touch', compression must be calculated here.
		# When affirm == 'touch', the touch() method must calculate the
		# compression value before touching.
		#
		try:
			return self.__compression
		except:
			# if compression is given as a kwarg, use that
			if self.__compressionk != None:
				if not self.__compressionk:
					self.__compression = ''
				else:
					self.__compression = self.__compressionk
				
				# this one is a parameter, so needs to be checked
				if not (self.__compression in ['', 'gz', 'bz2']):
					raise ValueError('err-init-fail', xdata(
							require1[None, '', False, 'gz', 'bz2']
						))
			
			# try to get compression from mime type's 'encoding'
			elif self.mime.enc in ['gzip', 'bzip2']:
				self.__compression = self.__DEF_ENC[self.mime.enc]
			
			# try to get it from the last element of the extention
			else:
				self.__compression = self.path.split(".")[:-1]
				if self.__compression == 'tgz':
					self.__compression = "gz"
			
			# Store compression (or an empty string, if none is specified)
			return self.__compression
	
	
	@property
	def members(self):
		"""
		Returns a dict with member name : member file info.
		"""
		rr = {}
		with self.archopen('r|*') as f:
			mm = f.getmembers()
			for m in mm:
				rr[m.name] = m
			return rr
	
	
	@property
	def memberinfo(self):
		"""
		Return member info listing.
		
		>>>
		>>> #
		>>> # The memberinfo property returns a propdict object.
		>>> # Call as a method to get the actual dict object.
		>>> #
		>>> myTarFile.memberinfo()
		>>>
		>>> # For easier reading in a terminal, try this:
		>>> myTarFile.memberinfo.display()
		>>> 
		
		Returns a propx object containing a dict with member names as 
		keys; each value is a dict containing information on the 
		corresponding member.
    
		SEE ALSO:
    >>> from trix.util.propx.propdict import *
    >>> help(propdict)
		
		"""
		rr = {}
		with self.archopen('r|*') as f:
			mm = f.getmembers()
			for m in mm:
				rr[m.name] = dict(
					name = m.name,
					size = m.size,
					mtime = m.mtime,
					mode = m.mode,
					type = m.type,
					linkname = m.linkname,
					uid = m.uid,
					gid = m.gid,
					uname = m.uname,
					gname = m.gname #,pax = m.pax_headers	
				)
						
		return trix.propx(rr)
	
	
	#
	# TOUCH
	#
	def touch(self, times=None):
		"""
		Touch the file to create and/or alter times.
		"""
		# be sure not to overwrite the file when it already exists!
		if not self.exists():
			# touch and create
			mode = 'w:%s' % self.compression
		else:
			# file exists. just touch.
			mode = 'a'
		
		# create as a tar file (if mode = w) or just open and close
		with self.archopen(mode) as z:
			z.close()
		
		# now put the time on it
		Path.touch(self, times)
	
	
	#
	# ARCH STORE (internal use)
	#
	def archstore(self, memgen, **k):
		"""Write member data from the `memgen` iterable."""
		
		ek = self.extractEncoding(k)
		mode = "w:%s" % self.compression
		with tarfile.open(self.path, mode) as fp:
			for item in memgen:
				# create TarInfo
				bufr = item['buffer']                  # the buffer
				bufr.seekend()                         # find buffer size
				info = tarfile.TarInfo(item['member']) # archive member name
				info.size = bufr.tell()
				info.mtime = time.time()
				
				bufr.seek(0)
				fp.addfile(tarinfo=info, fileobj=bufr.stream)
		
			# do i need to do this?
			fp.close()
	
	
	#
	# ARCH READ (internal use)
	#
	def archread(self, member, **k):
		return self.archopen("r:*").extractfile(member).read()
	
	
	#
	# ARCH OPEN (internal use)
	#
	def archopen(self, mode, **k):
		"""Open the tarfile; return the TarFile object."""
		try:
			return tarfile.open(self.path, mode, **k)
		except Exception as ex:
			raise type(ex)('tar-open-fail', xdata(path=self.path, k=k, 
					mode=mode, exists=self.exists(), mime=self.mime.guess
				))



