#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .. import *
import mimetypes


MIME_STRICT = False


class Mime(object):
	"""
	Detect/store mime type info. Properties are set in the constructor.
	"""
	def __init__(self, url, strict=MIME_STRICT):
		"""
		Pass a url (a file name will do). Optional `strict` argument
		limits results to IANA specifications; default is MIME_STRICT,
		False, which (unless changed) allows well-known file-type results.
		"""
		self.__url = url # the file name will do
		self.__strict = strict
		
		r = mimetypes.guess_type(url, strict)
		self.__guess = r
		self.__mimet = r[0]
		self.__enc = r[1]
		
		t,st = self.__mimet.split('/') if self.__mimet else (None,None)
		self.__type = t
		self.__subtype = st
	
	def __str__(self):
		return "<Mime %s%s>" % (
				str(self.__guess, " strict" if self.__strict else '')
			)
	
	@property
	def guess(self):
		"""Return (type/subtype,enc)."""
		return self.__guess
	
	@property
	def strict(self):
		"""
		Return True if `strict` was specified True to the constructor.
		
		If strict, limits results to IANA specifications. Otherwise,
		"well-known" file types are allowed, too.
		"""
		return self.__strict
	
	@property
	def mimetype(self):
		"""Return mime type."""
		return self.__mimet
	
	@property
	def enc(self):
		"""
		Returns the (guess) `encoding` value ('compress', 'gzip', None).
		"""
		return self.__enc
	
	@property
	def type(self):
		"""Return the (guess) `type`."""
		return self.__type
	
	@property
	def subtype(self):
		"""Return the (guess) `subtype`."""
		return self.__subtype
	
	
	@property
	def extension(self):
		"""Return the (guess) extension."""
		return mimetypes.guess_extension(self.guess[0])
	
	@property
	def extensions(self):
		"""Return a list of possible extensions for this mimetype."""
		return mimetypes.guess_all_extensions(self.guess[0])
	
	
	
	# -----------------------------------------------------------------
	# class methods providing mime data structures wrapped in propdict
	# objects.
	# -----------------------------------------------------------------
	
	@classmethod
	def type2ext(cls, mimetype):
		"""
		Classmethod. Utility; Returns the extension for a given mime type.
		"""
		return cls.maptypes()[mimetype]

	@classmethod
	def maptypes(cls):
		try:
			return cls.__maptypes
		except AttributeError:
			maptypes = {}
			mimetypes.init()
			for k in mimetypes.types_map:
				maptypes[mimetypes.types_map[k]] = k
			cls.__maptypes = maptypes
			return trix.propx(maptypes)
	
	# -----------------------------------------------------------------
	
	@classmethod
	def common_types(self):
		"""A propdict containing "common" extension:mimetype pairs."""
		return trix.propx(mimetypes.common_types)
	
	@classmethod
	def encodings_map(self):
		"""A propdict containing extension:encoding."""
		return trix.propx(mimetypes.encodings_map)
	
	@classmethod
	def suffix_map(self):
		"""
		Returns propdict mapping short suffix to long. Eg, "tgz":"tar.gz".
		"""
		return trix.propx(mimetypes.suffix_map)
	
	@classmethod
	def types_map(self):
		"""Returns propdict contianing existing {ext:mimetype} values."""
		return trix.propx(mimetypes.types_map)
		



