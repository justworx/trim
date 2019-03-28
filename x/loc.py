#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class BaseLocale(object):
	"""Base for Locale and AltLoc subclasses."""
	pass
		

class AltLoc(BaseLocale):
	"""
	AltLoc allows data formatting expected in other locales. AltLoc
	object data is retrieved in such a way that the threading issues
	involved with changing locale are not a concern. Many AltLocale 
	objects may be created, used, and discarded during the lifespan  
	of any given application process.
	
	The AltLoc class contains member variables that typically match
	the naming from the locale module. The exception to this is that
	the DAY_*, ABDAY_*, MON_*, and AB_* values are presented as lists
	with lowercase names. Eg., `AltLoc(L).abday` returns an ordered
	list of abbreviated day names for locale `L`.
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
		
		#print (self.__fmt)
		self.day = self.__fmt['day']
		self.abday = self.__fmt['abday']
		self.mon = self.__fmt['mon']
		self.abmon = self.__fmt['abmon']
		
		# format - these need to go...
		#self.time = self.__fmt['format'].get('time')
		#self.date = self.__fmt['format'].get('date')
		#self.datetime = self.__fmt['format'].get('datetime')
		#self.ampm = self.__fmt['format'].get('ampm')
		
		self.D_FMT = self.__fmt['D_FMT']
		self.T_FMT = self.__fmt['T_FMT']
		self.D_T_FMT = self.__fmt['D_T_FMT']
		self.T_FMT_AMPM = self.__fmt['T_FMT_AMPM']
		
		self.ERA = self.__fmt['ERA']
		self.ERA_D_FMT = self.__fmt['ERA_D_FMT']
		self.ERA_D_T_FMT = self.__fmt['ERA_D_T_FMT']
		self.ERA_T_FMT = self.__fmt['ERA_T_FMT']
		
		# other
		self.CRNCYSTR = self.__fmt['CRNCYSTR']   #"-$"
		self.RADIXCHAR = self.__fmt['RADIXCHAR'] #"."
		self.THOUSEP = self.__fmt['THOUSEP']     #","
		self.YESEXPR = self.__fmt['YESEXPR']     #"Yy"
		self.NOEXPR = self.__fmt['NOEXPR']       #"Nn"
		
		
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
		self.decimal_point = self.loconv['decimal_point']
		self.grouping = self.loconv['grouping']
		self.thousands_sep = self.loconv['thousands_sep']
	


#class Locale(BaseLocale):
	#"""
	# --- NOT YET IMPLEMENTED! ---
	#Locale wraps the locale module's features. It's intended for use
	#when generating output expected by the user of this app instance.
	#There should be only one Locale object in any given process; it
	#should be created when the application starts and persist through
	#the process runtime.
	
	#To generate output strings in this app that contain formmatting 
	#for other locales, use AltLocal.
	#"""
	
	#def __init__(self):
		#pass
		
		
	@classmethod
	def query_locale_dict(cls, locale):
		"""
		Pass a locale string, eg., "en_US.UTF_8", etc... Returns a new
		`trix.x.loc` object containing locale format methods and data.
		"""
		cline = "%s -m %s loc -c %s" % (
				sys.executable, trix.innerfpath(), locale
			)
		
		cx = trix.callx(cline)
		js = cx.reader().read()
		
		return trix.jparse(js)
