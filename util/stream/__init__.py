#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ..enchelp import * # trix


#
#
#
#
# STREAM
#
#
#
#
class Stream(EncodingHelper):
	"""
	The purpose of streams is to provide a common interface for dealing
	with objects that read and write data.
	
	Stream-based objects hold their stream, manage their encoding-related
	issues, provide a set of features for reading, writing, and working
	with stream data.
	
	They clean themselves up when finished.
	
	Stream use is divided into two areas: Read data with a `Reader` and
	write data with a `Writer`. Both these classes are based on 
	`Stream`, so properties `stream` and `mode` give access to the 
	contained stream (or other producer/consumer of data), and the 
	mode (bytes or unicode) that the stream produces/consumes.
	
	The Stream object is based on EncodingHelper, so the `ek` property 
	and other methods for applying, extracting, and otherwise using any
	encoding-related keyword arguments (as provided to the Stream 
	object's constructor) are available.

	Providing an "encoding" specification causes Writer and Reader 
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
	
	"""

	#
	#
	#
	# INIT
	#
	#
	#
	def __init__(self, stream, **k):
		"""
		Pass argument `stream`, a stream.
		
		Valid keyword arguments are:
		 * Anything EncodingHelper accepts. (See: trix.util.enchelp)
		 * A specific mode using keyword argument "mode". (See above)
		
		NOTE:
		In some situations `stream` will be an object that shares its
		source stream with a container object, which would need to be 
		held in this object's memory for this object's lifespan. In such
		cases, it is passed here as keyword argument "source".
		
		"""
		
		EncodingHelper.__init__(self, **k)
		self.__mode = k.get('mode')
		self.__stream = stream
		if k.get('keepopen'):
			self.close = self.keepopen
		
		#
		# In some situations `stream` will be an object that shares its
		# source stream with a container object, which would need to be 
		# held in this object's memory for this object's lifespan. In such
		# cases, it is passed here as keyword argument "source".
		#
		self.__source = k.get('source')

	
	#
	#
	#
	# DEL
	#
	#
	#
	def __del__(self):
		"""
		Flush and close the contained stream (if open).
		"""
		#
		# REMEMBER: Some subclasses may not call `Stream.__init__()` 
		#           immediately, so it IS possible that self.__stream
		#           may remain unset for a while (eg, until the first
		#           write or read).
		#
		#           Further, a stream may be detached from this object
		#           in a valid way, so an error here would be misleading.
		#
		try:
			# Don't try to close if self.__stream was never set.
			self.__stream
		except AttributeError:
			self.__stream = None
		
		# Close without hiding meaningful errors that might be raised if
		# self.__stream were undefined.
		self.close()
		#
		# REMEMBER: Some subclasses may need to have close() called even
		#           if this class doesn't.
		#
	
	
	#
	#
	#
	# ENTER/EXIT
	#
	#
	#
	def __enter__(self):
		return self
	
	def __exit__(self, *args):
		self.close()
	
	
	@property
	def stream(self):
		"""The contained stream."""
		return self.__stream
	
	@property
	def mode(self):
		"""Return `mode` as given to constructor."""
		return self.__mode
	
	
	#
	#
	#
	# CLOSE
	#
	#
	#
	def close(self):
		"""Closes the stream (unless keepopen is True)."""
		self.forceclose()
	
	
	#
	#
	#
	# KEEP OPEN (NO CLOSE)
	#
	#
	#
	def keepopen(self, **k):
		"""Ignore attempt to close stream."""
		pass
	
	
	#
	#
	#
	# FORCE CLOSE
	#
	#
	#
	def forceclose(self):
		"""
		Closes the `self.__stream` stream object. Subclasses that do not
		work with stream objects should replace this method with cleanup
		suitable to their own non-stream "producer".
		"""
		
		# don't raise an exception here if the stream was never set
		try:
			self.__stream
		except:
			return
		
		# Leave the actual closing of the stream out here so that errors
		# will not be caught.
		if self.__stream:
			self.__stream.close()
		
		# If there happens to be a source object being held, release it.
		try:
			del(self.__source)
		except:
			pass
	
	
	#
	#
	#
	# SEEK
	#
	#
	#
	def seek(self, *a, **k):
		"""
		Performs seek on the contained stream using any given args and
		kwargs. (Seekable streams only!)
		"""
		# first, make sure self.__stream is set
		self.__stream
		
		#
		# The seek method MUST NOT be replaced by self.__stream.seek 
		# because subclasses need to reset the `lines` property after 
		# each seek.
		#
		try:
			self.__stream.seek(*a, **k)
		except Exception as ex:
			raise type(ex)('err-seek-fail', ex.args, xdata(
					streamtype=type(self.__stream)
				))
	
	
	#
	#
	#
	# SEEKEND
	#
	#
	#
	def seekend(self):
		"""Move pointer to the end of the stream."""
		return self.seek(0,2)
	
	
	#
	#
	#
	# TELL
	#
	#
	#
	def tell(self):
		"""Return current pointer position in the stream."""
		return self.__stream.tell()

	
	#
	#
	#
	# DETACH
	#
	#
	#
	def detach(self):
		"""
		Return a good copy of this stream, nullifying the internal copy.
		"""
		try:
			return self.__stream
		finally:
			self.__stream = None

