#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import weakref
from ..util.stream.buffer import *
from ..util.propx import *
from .file import * # trix, stream, enchelp

class Archive(FileBase):
	"""
	The base class Zip and Tar files.
	
	The `trix.fs.archive.Archive` class is the base class for archive
	file system objects tar and zip. This class defines the methods used
	to write to and read from members, to list members and names, and to
	delete members.
	
	EXAMPLE:
	>>>
	>>> Create an archive; write and read memebers.
	>>>
	# 
	# Create a path object to a test archive
	# 
	p = trix.path("~/test.tar.gz", affirm="touch")
	
	# 
	# Get a tar file wrapper, `z`.
	# 
	z = p.wrapper()
	
	# 
	# Create a member passing member name, "Test1", and some text.
	# 
	z.write("Test1", "This is a test.")
	
	# 
	# Until you call the `Tar.flush` method, no changes take place
	# in the file, so `z.members` returns an empty dict.
	# 
	z.members
	
	# 
	# After calling `flush()`, the member is in the archive.
	# 
	z.flush()
	z.members
	
	# 
	# After calling `flush()`, the member is in the archive.
	# 
	z.read("Test1")
	
	
	READING AND WRITING:
	See the `read`, `reader`, `write`, and `writer` method documentation
	for a description of how to "mode" and "encoding" keyword arguments
	to maintain strict control of how data is read from and written to
	archive members.
	
	"""
	
	#
	#
	# INIT
	#
	#
	def __init__(self, path, **k):
		"""
		Pass archive file path and kwargs relevant to file type.
		"""
		
		#
		# Keep changed members in __writers dict. Each key is an archive 
		# member's name, and its value is a Buffer object with the text
		# to be stored when this archive is flushed - rewritten into a
		# new archive with removals excluded, changed and unchanged (but
		# not removed) members.
		#
		self.__writers = {}
		self.__readers = {}
		self.__deleted = []
		self.__openk = k
		
		FileBase.__init__(self, path, **k)
	
	
	
	#
	#
	# DEL
	#
	#
	def __del__(self):
		try:
			if self.__writers or self.__deleted:
				self.flush()
		except:
			pass
	
	@property
	def openk(self):
		return dict(self.__openk)
	
	@property
	def deleted(self):
		return self.__deleted
	
	@property
	def writers(self):
		return self.__writers.keys()
	
	
	
	#
	#
	#
	# ABSTRACT PROPERTIES AND METHODS
	#  - All classes based on Archive must implement these.
	#
	#
	#
	
	
	#
	#
	# MEMBERS
	#
	#
	@property
	def members(self):
		"""The member objects within the archive."""
		raise NotImplementedError("abstract-property-required", 'members')
	
	
	#
	#
	# NAMES
	#
	#
	@property
	def names(self):
		"""List of the names of member objects in this archive."""
		raise NotImplementedError("abstract-property-required", 'names')
	
	
	#
	#
	# ARCH-READ
	#
	#
	def archread(self, member, **k):
		"""Read a single member from the archive."""
		raise NotImplementedError("abstract-method-required", 'archread')
	
	
	#
	#
	# ARCH-STORE
	#
	#
	def archstore(self, membergen, **k):
		"""Write all non-deleted members to the new archive."""
		raise NotImplementedError("abstract-method-required", 'archstore')
	
	
	
	#
	#
	#
	#
	# ARCHIVE METHODS
	#
	#
	#
	#
	
	#
	#
	# SEARCH - UNDER CONSTRUCTION
	#
	#
	def search(self, fnmatch_pattern, **k):
		"""
		Search member names in this path using fnmatch.
		
		Pass keyword argument `remove=True` to delete matching members.
		 
		NOTE: You must flush the archive before removed members are
		      actually deleted. Until flushed, removed members will 
		      still appear in listings.
		
		"""
		
		nn = self.names.fnmatch(fnmatch_pattern)
		if k.get('remove'):
			for n in nn:
				self.delete(n)
		
		return trix.propx(nn)		
	
	
	
	#
	#
	# READ
	#
	#
	def read(self, member, **k):
		"""
		Return the entire contents of the member. Use "mode", "encoding",
		and "errors" keyword arguments to tailor the result type.
		
    MODE  ENCODING      I/O      NOTE 
    'r'                 unicode  decode with DEF_ENCODE
    'r'   encoding=enc  unicode  decode with <enc>
    'rb'                bytes    bytes are returned
    'rb'  encoding=enc  unicode  bytes are decoded after reading
    
		SEE ALSO:
    >>> from trix.util.reader import *
    >>> help(Stream)
    >>> help(Reader)
    
		"""
		return self.reader(member, **k).read()
	
	
	#
	#
	# READER
	#
	#
	def reader(self, member, **k):
		"""
		Return a Buffer.reader() to read the given member. Pass Reader
		kwargs to specify how data should be read. Stream kwargs are also
		accepted, but are only applicable on the first call for any given
		member.
		
    MODE  ENCODING      I/O      NOTE 
    'r'                 unicode  decode with DEF_ENCODE
    'r'   encoding=enc  unicode  decode with <enc>
    'rb'                bytes    bytes are returned
    'rb'  encoding=enc  unicode  bytes are decoded after reading
    
		SEE ALSO:
    >>> from trix.util.reader import *
    >>> help(Stream)
    >>> help(Reader)
		
		"""
		if 'encoding' in k:
			k.setdefault('mode', "r")
		
		if member in self.__writers:
			b = self.__writers[member]
		elif member in self.__readers:
			b = self.__readers[member]
		else:
			bk = trix.kpop(k, 'max_size mode encoding')
			b = Buffer(**bk)
			b.write(self.archread(member, **k))
			self.__readers[member] = b
		
		b.seek(0)
		return weakref.proxy(b.reader(**k))
	
	
	
	#
	#
	# WRITE
	#
	#
	def write(self, member, data, **k):
		"""
		Write the new contents of the member.
		
		Pass member name string argument `member`, and any `data` that
		needs to be written.
		
		Keyword arguments will be passed to a `trix.util.stream.writer`
		object's constructor. The mode and encoding arguments default to:
		 
		MODE  ENCODING      I/O      NOTE 
		'w'                 unicode  encode with DEF_ENCODE
		'w'   encoding=enc  unicode  encode with <enc>
		'wb'                bytes    bytes are written
		'wb'  encoding=enc  unicode  bytes are encoded before writing
		
		EXAMPLE:
		>>> from trix.fs.tar import *
		>>> testfile = "~/test-%s.tar.gz"%trix.value('time.time')()
		>>> f = Tar(testfile, affirm="touch")
		>>> f.write("Test1", "This is a test.")
		>>> f.write("Test2", "This is a another.")
		>>> f.members()
		{}
		>>> f.flush()
		>>> f.members.display()
		
		
		SEE ALSO:
    >>> from trix.util.reader import *
    >>> help(Stream)
    >>> help(Writer)
		
		"""
		self.writer(member, **k).write(data)
	
	
	#
	#
	# WRITER
	#
	#
	def writer(self, member, **k):
		"""
		Return a Buffer.writer() to write to the given member. Pass Writer
		kwargs to specify how data should be read. Buffer kwargs are also
		accepted, but are only applicable on the first call (when the 
		buffer is first created).
		
    MODE  ENCODING      I/O      NOTE 
    'w'                 unicode  encode with DEF_ENCODE
    'w'   encoding=enc  unicode  encode with <enc>
    'wb'                bytes    bytes are written
    'wb'  encoding=enc  unicode  bytes are encoded before writing
    
		SEE ALSO:
    >>> from trix.util.reader import *
    >>> help(Stream)
    >>> help(Writer)
		
		"""
		
		if 'encoding' in k:
			k.setdefault('mode', "w")
		
		# a buffer already writable
		if member in self.__writers:
			b = self.__writers[member]
		
		# a buffer that was a reader, now becomes a writer
		elif member in self.__readers:
			b = self.__readers[member]
			del(self.__readers[member])
		
		else:
			mxsz = k.pop('max_size', None)
			b = Buffer(mxsz, **k)
			try:
				# an existing member not yet read or written to
				b.write(self.archread(member, **k))
			except KeyError:
				# A new buffer not in the archive (which will be written (to
				# a new archive file) when flush() is called.
				pass
		
		# store the member's buffer
		self.__writers[member] = b
		
		# if this member name has been deleted, undelete it (or it won't
		# get written when it's supposed to!)
		if member in self.__deleted:
			self.__deleted.remove(member)
		
		# start at the beginning; return a proxy to the buffer's writer
		b.seek(0)
		return weakref.proxy(b.writer(**k))
	
	
	
	#
	#
	# DELETE
	#
	#
	def delete(self, member):
		"""
		Mark the given member for deletion on the next flush.
		"""
		self.__deleted.append(member)
		if member in self.__readers:
			del(self.__readers[member])
		if member in self.__writers:
			del(self.__writers[member])
	
	
	
	#
	#
	# UNDO CHANGES
	#
	#
	def undelete(self, member):
		"""
		Remove a member from the deletion list.
		"""
		if member in self.__deleted:
			self.__deleted.remove(member)
	
	def unwrite(self, member):
		"""Remove all changes to member since the last flush."""
		if member in self.__writers:
			del(self.__writers[member])
	
	def revert(self, member=None):
		"""
		If member is specified, undelete/undo any writes. Otherwise, undo
		all writes/deletes since the last flush.
		"""
		if member:
			self.undelete(member)
			self.unwrite(member)
		else:
			self.__writers={}
			self.__deleted=[]
	
	
	
	#
	#
	# MEM-GEN
	#
	#
	def memgen(self):
		"""Used internally by subclasses to write archive members."""
		# 
		# BUILD NAME LIST
		#  - Build a list of names to be checked and, if appropriate,
		#    written to the ARCHNEW file.
		#
		names = []                           # start with blank list
		names.extend(self.names)             # add all archive names
		names.extend(self.__writers.keys())  # add all writer names
		names = set(names)                   # make the list unique
		
		for name in names:
			# Copy existing files and write new self.__writers buffers
			# to the new (`archnew`) archive.
			if not (name in self.__deleted):
				if name in self.__writers:
					b = self.__writers[name]
				elif name in self.__readers:
					b = self.__readers[name]
				else:
					# copy unedited members
					b = Buffer()
					b.write(self.archread(name))
				
				# seek start and yield a dict
				b.seek(0)
				d = dict(member=name, buffer=b)
				yield (d)
	
	
	#
	#
	# FLUSH
	#
	#
	def flush(self):
		"""
		Flush changes to archive members' contents.
		
		Flush is called automatically when an Archive object is destroyed.
		If any changes are buffered, the archive will be rewritten to
		reflect the current members and their content.
		
		""" 
		
		#
		# Don't do anything unless there are write buffers present.
		# If there are no writers, there are no changes.
		#
		if self.__writers or self.__deleted:
			
			# store self.path
			TRUEPATH = self.path
			TYPE = type(self) # either Zip or Tar
			try:
				#
				# ARCHNEW
				#  - create the new archive object using a temporary name,
				#    "#PATH#/#FILENAME#.new". EG, 'myArchive.tar.gz.new'.
				#
				ARCHNEW = "%s.new" % TRUEPATH
				krgs = self.openk
				krgs['affirm'] = 'touch'
				archnew = TYPE(ARCHNEW, **krgs)
				
				# write all undeleted members to the ARCHNEW file
				archnew.archstore(iter(self.memgen()))
				
				#
				# HANDLE THE BACKUP FILE
				#  - If there's an older backup file, remove it so we can 
				#    replace it with the current file.
				#
				BACKUP = "%s/.%s.bu" % (Path(TRUEPATH).parent, self.name)
				x = FileBase(BACKUP)
				if x.exists():
					x.remove()
				
				#
				# RENAME THIS FILE
				#  - Rename the current file to ".#FILENAME#.bu"
				#  - Remember: `rename` resets self.path automatically, so 
				#    this file's internal self.path is now ".#FILENAME#.bu",
				#    which has just been removed.
				#
				self.rename(BACKUP)
				
				#
				# RENAME THE NEW FILE
				#  - Rename the newly-written archive to the name this object
				#    previously held. Again, `rename` resets self.path 
				#    automatically.
				#  - However, that's the new file object, not THIS object, so
				#    there's one more step to make the new file the property
				#    of this object...
				#
				archnew.rename(TRUEPATH)
				
				#
				# CHANGE INTERNAL FILE PATH
				#  - Make the new version of the archive the property of this
				#    object.
				#  - The old archive object `archnew` is done when this method
				#    exits. This object will now have its path.
				#
				Path.setpath(self, TRUEPATH)
				
				# clear all the buffers
				self.__writers={}
				self.__readers={}
				self.__deleted=[]
				
				# Now that there's been no exception, it's time to delete
				# the backup file.
				x = FileBase(BACKUP)
				if x.exists():
					x.remove()
				
			except BaseException as ex:
				#
				# I'm not too sure what needs to be done in the case of an
				# exception. I guess... 
				#  1. rename this file to whatever.restore
				#  2. rename the archnew file to this archive's real name
				#  3. reset self.path to the original file's path
				#
				# I guess I need to think some more on this. So far, there's
				# been no exception to help me see what might go wrong. I'm
				# not sure whether to hope for some errors! The whole thing's
				# pretty simple - maybe this catch isn't really needed. I do
				# need to think some more about this. TODO: Think some more!
				#
				raise type(ex)("err-archive-flush", xdata(path=self.path))
