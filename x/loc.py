#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class BaseLocale(object):
	"""Base for Locale and AltLoc subclasses."""
	
	#
	# This should provide a common interface so that using AltLoc
	# is the same as using Locale (though Locale will, for a while,
	# have several extra features - that is until I can figure out
	# how to reproduce them in AltLoc). I don't want to have two
	# versions of the documentation.
	#

class AltLoc(BaseLocale):
	"""
	AltLocale allows data formatting expected in other locales. Many 
	AltLocale objects may be created, used, and discarded during the
	lifespan of any given application process.
	"""
	
	__locales = {}
	
	def __init__(self, loc):
		self.__loc = loc
		try:
			self.__fmt = self.__locales[loc]
		except:
			self.__locales[loc] = self.query_locale_dict(loc)
			self.__fmt = self.__locales[loc]
		
		self.locale = self.__fmt['locale']
		
		#print (self.__fmt)
		self.day = self.__fmt['day']
		self.abday = self.__fmt['abday']
		self.mon = self.__fmt['mon']
		self.abmon = self.__fmt['abmon']
		
		# format
		self.time = self.__fmt['format'].get('time')
		self.date = self.__fmt['format'].get('date')
		self.datetime = self.__fmt['format'].get('time')
		self.era = self.__fmt['format'].get('era')
		self.ampm = self.__fmt['format'].get('ampm')
		
		self.ERA = self.__fmt['ERA']
		self.ERA_D_FMT = self.__fmt['ERA_D_FMT']
		self.ERA_D_T_FMT = self.__fmt['ERA_D_T_FMT']
		self.ERA_T_FMT = self.__fmt['ERA_T_FMT']
		
		# money
		self.CRNCYSTR = self.__fmt['CRNCYSTR'] #"-$"
		
		self.loconv = self.__fmt["loconv"]
		self.int_frac_digits = self.loconv['int_frac_digits']
		self.frac_digits = self.loconv['frac_digits']
		self.mon_decimal_point = self.loconv['mon_decimal_point']
		self.positive_sign = self.loconv['positive_sign']
		self.n_sign_posn = self.loconv['n_sign_posn']
		self.mon_thousands_sep = self.loconv['mon_thousands_sep']
		self.p_sign_posn = self.loconv['p_sign_posn']
		self.negative_sign = self.loconv['negative_sign']
		self.n_cs_precedes = self.loconv['n_cs_precedes']
		self.mon_grouping = self.loconv['mon_grouping']
		self.p_cs_precedes = self.loconv['p_cs_precedes']
		self.grouping = self.loconv['grouping']
		self.n_sep_by_space = self.loconv['n_sep_by_space']
		self.thousands_sep = self.loconv['thousands_sep']
		self.int_curr_symbol = self.loconv['int_curr_symbol']
		self.p_sep_by_space = self.loconv['p_sep_by_space']
		self.decimal_point = self.loconv['decimal_point']
		
		# yes/no
		self.YESEXPR = self.__fmt['YESEXPR']
		self.NOEXPR = self.__fmt['NOEXPR']
		
		# numerics
		self.radix = self.__fmt['radix']
		self.thousep = self.__fmt['thousep']
	


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
