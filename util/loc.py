#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class BaseLocale(object):
	"""Base for AltLoc subclass and, potentially, future variants."""
	pass
		

class AltLoc(BaseLocale):
	"""
	AltLoc allows data formatting expected in other locales. AltLoc
	object data is retrieved in such a way that the threading issues
	involved with changing locale are not a concern. Many AltLoc 
	objects may be created, used, and discarded during the lifespan  
	of any given process.
	
	The AltLoc class contains member variables that typically match
	the naming from the locale module. The exception to this is that
	the DAY_*, ABDAY_*, MON_*, and AB_* values are presented as lists
	with lowercase names. Eg., `AltLoc(L).abday` returns an ordered
	list of abbreviated day names for locale `L`.
	
	AltLoc provides no formatting methods. The intention is to provide
	formatting strings in any locale available to the system. 
	
	BE AWARE:
	AltLoc can NOT access locale data that is not available to the
	system. Check your Settings/Preferences to determine which locale
	datasets are available.
	
	WINDOWS USERS:
	Unfortunately, MS Windows seems to allow access to only the locale
	dataset that is specified in preferences. I hope to create a set
	of locale json files that can be downloaded for use on any system
	so that Windows users may access alternate locales, too, but that
	is in the future.
	"""
	
	__locale_cache = {}
	
	def __init__(self, loc):
		"""
		Pass a locale signature in the form [lang_countrycode.encoding],
		Eg., "en_CA.UTF_8", etc...
		
		Returns AltLoc, a subclass of BaseLocale containing all the data
		for a given locale. Member variables match the naming conventions
		of the python 'locale' module, but format strings are expanded so
		there's no need to pass them through locale.info().
		"""
		try:
			self.__fmt = self.__locale_cache[loc]
		except:
			self.__locale_cache[loc] = self.query_locale_dict(loc)
			self.__fmt = self.__locale_cache[loc]
		
		self.locale = self.__fmt['locale']
		self.loconv = self.__fmt["loconv"]
		
		#
		# DATE/TIME
		#
		self.day = self.__fmt['day']
		self.mon = self.__fmt['mon']
		self.abday = self.__fmt['abday']
		self.abmon = self.__fmt['abmon']
		
		self.D_FMT = self.__fmt['D_FMT']
		self.T_FMT = self.__fmt['T_FMT']
		self.D_T_FMT = self.__fmt['D_T_FMT']
		self.T_FMT_AMPM = self.__fmt['T_FMT_AMPM']
		
		self.ERA = self.__fmt['ERA']
		self.ERA_D_FMT = self.__fmt['ERA_D_FMT']
		self.ERA_T_FMT = self.__fmt['ERA_T_FMT']
		self.ERA_D_T_FMT = self.__fmt['ERA_D_T_FMT']
		
		#
		# LC_MONETARY
		#
		self.int_curr_symbol = self.loconv['int_curr_symbol']
		self.currency_symbol = self.loconv['currency_symbol']
		self.p_cs_precedes = self.loconv['p_cs_precedes']
		self.n_cs_precedes = self.loconv['n_cs_precedes']
		self.n_sep_by_space = self.loconv['n_sep_by_space']
		self.p_sep_by_space = self.loconv['p_sep_by_space']
		self.mon_decimal_point = self.loconv['mon_decimal_point']
		self.frac_digits = self.loconv['frac_digits']
		self.int_frac_digits = self.loconv['int_frac_digits']
		self.mon_thousands_sep = self.loconv['mon_thousands_sep']
		self.mon_grouping = self.loconv['mon_grouping']
		self.positive_sign = self.loconv['positive_sign']
		self.negative_sign = self.loconv['negative_sign']
		self.n_sign_posn = self.loconv['n_sign_posn']
		self.p_sign_posn = self.loconv['p_sign_posn']
		
		#
		# LC_NUMERIC
		#
		self.grouping = self.loconv['grouping']
		self.decimal_point = self.loconv['decimal_point']
		self.thousands_sep = self.loconv['thousands_sep']
		
		# other
		self.CRNCYSTR = self.__fmt['CRNCYSTR']   #"-$"
		self.RADIXCHAR = self.__fmt['RADIXCHAR'] #"."
		self.THOUSEP = self.__fmt['THOUSEP']     #","
		self.YESEXPR = self.__fmt['YESEXPR']     #"Yy"
		self.NOEXPR = self.__fmt['NOEXPR']       #"Nn"
		
		
	@classmethod
	def query_locale_dict(cls, loc_str):
		"""
		Pass a locale description string. Returns a dict containing
		locale format data.
		
		The `loc_str` argument must be a string in the following format:
		 * langcode_country.endocing
		 * Eg., "en_US.utf_8"
		
		"""
		cline = "%s -m %s loc -c %s" % (
				sys.executable, trix.innerfpath(), loc_str
			)
		
		cx = trix.callx(cline)
		js = cx.reader().read()
		
		return trix.jparse(js)
