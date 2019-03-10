#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class Locale(object):
	"""Stores formatting values and strings for the given locale."""
	
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
		
		d = self.__dict
		self.__day   = d['day']
		self.__abday = d['abday']
		self.__mon   = d['mon']
		self.__abmon = d['abmon']
	
	
	
	#
	# Now I want to redo this so that there are a lot of properties
	#
	
	# info strings come first
	@property 
	def locale(self):
		return self.__locale
	
	
	# FORMAT STRINGS
	@property
	def fdatetime(self):
		return self.__fmt['datetime']
	
	@property
	def fdate(self):
		return self.__fmt['date']
	
	@property
	def ftime(self):
		return self.__fmt['time']
	
	@property
	def fampm(self):
		return self.__fmt['ampm']
	
	@property
	def fera(self):
		return self.__fmt['era']
	
	
	# DAY/MONTH NAMES/ABBREVIATIONS
	@property
	def day(self):
		"""Zero-based list of day names."""
		return self.__dict['day']
	
	@property
	def abday(self):
		"""Zero-based list of abbreviated day names."""
		return self.__dict['abday']
	
	@property
	def month(self):
		"""Zero-based list of month names."""
		return self.__dict['mon']
	
	@property
	def abmonth(self):
		"""Zero-based list of abbreviated month names."""
		return self.__dict['abmon']
	
	
	# GENERAL
	@property
	def radix(self):
		return self.__dict['radix']
	
	@property
	def thousep(self):
		return self.__dict['thousep']
	
	@property
	def radix(self):
		return self.__dict['YESEXPR']
	
	@property
	def yes(self):
		"""Regex expression matching single-char Yes/No responses.""" 
		return self.__dict['radix']
	
	@property
	def no(self):
		"""Regex expression matching single-char Yes/No responses.""" 
		return self.__dict['radix']
	
	@property
	def curstr(self):
		"""CRNCYSTR"""
		return self.__dict['CRNCYSTR']
	
	@property
	def fera(self):
		"""DateTime Era string. (Usually blank.)"""
		return self.__dict['ERA']
	
	@property
	def fera(self):
		"""DateTime Era string. (Usually blank.)"""
		return self.__dict['ERA']
	
	@property
	def feradt(self):
		"""DateTime Era string. (Usually blank.)"""
		return self.__dict['ERA_D_T_FMT']
	
	@property
	def ferad(self):
		"""DateTime Era string. (Usually blank.)"""
		return self.__dict['ERA_D_FMT']
 	
	@property
	def ferat(self):
		"""Era Time string. (Usually blank.)"""
		return self.__dict['ERA_T_FMT']
	
	# NUMERIC
	def decimal(self):
		return self.__loconv['decimal_point']
	
	def decimal(self):
		return self.__loconv['']
	
	def decimal(self):
		return self.__loconv['']
	
	
	#
	# We'll put classmethods at the bottom for now. Looks like there
	# are a few more coming.
	#
	@classmethod
	def query_locale_dict(cls, locale=None):
		"""
		Pass a locale string, eg., "en_US.UTF_8", etc... Returns a new
		`trix.x.loc` object containing locale format methods and data.
		"""
		locmod = trix.module("locale")
		locstr = locale or ".".join(locmod.getlocale())
		py_ver = sys.executable
		cline = "%s -m %s loc %s" % (py_ver, trix.innerfpath(), locstr)
		
		proc = trix.popen(cline)
		jsonb = proc.communicate()[0]
		jsons = jsonb.decode("UTF_8")
		
		return trix.jparse(jsons)
		#return trix.ncreate("x.loc.Locale", trix.jparse(jsons))
	
	
