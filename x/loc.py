#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class Locale(object):
	"""Stores formatting values and strings for the given locale."""
	
	@classmethod
	def query_locale_dict(cls, locale=None):
		"""
		Pass a locale string, eg., "en_US.UTF_8", etc... Returns a new
		`trix.x.loc` object containing locale format methods and data.
		"""
		locmod = trix.module("locale")
		locstr = locale or ".".join(locmod.getlocale())
		py_ver = 'python3' if sys.version_info[0]==3 else "python"
		cline = "%s -m %s loc %s" % (py_ver, trix.innerfpath(), locstr)
		
		proc = trix.popen(cline)
		jsonb = proc.communicate()[0]
		jsons = jsonb.decode("UTF_8")
		
		return trix.jparse(jsons)
		#return trix.ncreate("x.loc.Locale", trix.jparse(jsons))
	
	
	def __init__(self, locinfo=None):
		"""
		Pass argument `locinfo` as a locale signature string (Eg.,
		"en_US.UTF8") or as a dict containing the full set of key/value
		pairs required to support this object's operation.
		"""
		
		try:
			#
			# If locinfo has a getkeys method, it's a dict and should be
			# stored directly in `self.__dict`.
			#
			locinfo.getkeys
			self.__dict = locinfo
		
		except:
			#
			# Otherwise, locinfo must be a locale signature string in the
			# required format. Eg., "en_US.UTF8". In this case, the string
			# is passed to the `Locale.query_locale_dict` classmethod and
			# a new locinfo dict will be generated (in a subprocess so as
			# to avoid any potential quirks of python's `locale` module.) 
			#
			self.__dict = self.query_locale_dict(locinfo)
		
		#
		# Store loc data as member variables
		#
		
		# info
		self.__locale = self.__dict['locale']
		
		# formats
		self.__loconv = dict(self.__dict['loconv'])
		self.__fmt = fmt = dict(self.__dict['format'])
		
		self.__f_dt = fmt["datetime"]
		self.__f_d  = fmt["date"]
		self.__f_t  = fmt["time"]
		self.__fapm = fmt['ampm']
		self.__fera = fmt['era']
		
		
		#
		# COMING SOON...
		#  - values (days of week/month, and alts)
		#
	
	
	
	@property
	def locale(self):
		return self.__locale
	
	@property
	def format(self):
		return self.__fmt
	
	@property
	def conv(self):
		return self.__loconv
	
	
	# formats
	def datetime(self, f=None):
		return strftime(f or self.__f_dt)
	
	def date(self, f=None):
		return strftime(self.__f_d)
	
	def time(self, f=None):
		return strftime(self.__f_t)
	
	def ampm(self, f=None):
		return strftime(self.__fapm)
	
	def era(self, f=None):
		return strftime(self.__fera)
	
