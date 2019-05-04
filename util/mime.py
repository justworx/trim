#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


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
		"""Returns `encoding` value ('compress', 'gzip', or None)."""
		return self.__enc
	
	@property
	def type(self):
		"""Return `type`."""
		return self.__type
	
	@property
	def subtype(self):
		"""Return `subtype`."""
		return self.__subtype
	
	
	# Does it work? Sure... it just doesn't... technically... fly.
	# @classmethod
	# def type2ext(cls, mimetype):
		# """
		# Classmethod. Utility; Returns the extension for a given mime type.
		# """
		# try:
			# return cls.__type2ext[mimetype]
		# except AttributeError:
			# maptypes = {}
			# mimetypes.init()
			# for k in mimetypes.types_map:
				# maptypes[mimetypes.types_map[k]] = k
			# cls.__type2ext = maptypes
			# return cls.__type2ext[mimetype]

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
			return maptypes




