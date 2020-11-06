#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from ..util.loc import *
from datetime import *


class xLocale(Locale):
	"""
	An extension to Locale.
	"""
	
	AssetPath = '%s/assets/locale_json.tar.gz' % DEF_CACHE
	
	def __init__(self, loc_str):
		"""
		Pass a locale description string. Returns a dict containing
		locale format data.
		
		The `loc_str` argument must be a string in the following format:
		 * langcode_country.encoding
		 * Eg., "en_US.utf8"
		
		"""
		
		# Default is the current system locale.
		if not loc_str:
			loc_str = ".".join(trix.module("locale").getlocale())
		
		# VALIDATE THE LOCALE STRING
		self.__loc_str = loc_str = self.validate_locstr(loc_str)
		
		try:
			#
			# This will fail on first call, so will be handled below. On
			# subsequent calls, it will succeed here.
			# 
			BaseLocale.__init__(self, Locale.__qdict(loc_str))
		except:
			# here's why it will succeed on subsequent calls...
			try:
				# try to use asset locale data if possible...
				Locale.__qdict = Locale.query_asset_dict
			except:
				# otherwise, query the local system for locale data
				Locale.__qdict = Locale.query_locale_dict
			
			# here's the initialization for the first call
			
			BaseLocale.__init__(self, Locale.__qdict(loc_str))
	
	@property
	def loc(self):
		return self.__loc_str
	
	@classmethod
	def list(cls, pattern=None):
		"""
		Return a proplist containing all locales that match `pattern`.
		The default `pattern` is '*.utf8*, which returns the locale 
		signature for a complete set of language_country locales (with
		the exception of Gallcian Spain, which I've not yet been able to
		successfully download).
		
		```python3
		from trix import *
		trix.loc().list.table(w=6)
		trix.loc().list("en_*").table(w=6)
		trix.loc().list("*_IN*").table(w=6)
		
		```
		"""
		pattern = pattern or '*.utf8*'  # default search: "*.utf8*"
		p = trix.path('%s/assets/locale_json.tar.gz'%DEF_CACHE) #loc path
		a = p.wrapper(encoding='utf_8') # open archive
		return a.names.fnmatch(pattern)
		
	
	@classmethod
	def validate_locstr(self, loc_str):
		"""
		Converts a reasonably valid loc_str to the format in which locale 
		members are stored in the asset file, changing case and encoding
		values to match exactly. Eg., "En_Us.Utf-8" to "en_US.utf8", etc.
		
		>>> Locale.validate_locstr("AA_er.UTF-8@SAAHO")
    'aa_ER.utf8@saaho'

		"""
		s = trix.scan(loc_str)
		ll = s.splits("_.@")
		ll[0]=ll[0].lower()
		ll[1]=ll[1].upper()
		
		ln = len(ll)
		if ln<3:
			return "%s_%s" % ll
		
		#
		# If an encoding is included, make sure it matches member naming
		# conventions in the locale scheme.
		#
		eh = "util.enchelp.EncodingHelper"
		e = trix.ncreate(eh, encoding=ll[2]).encoding
		if e == 'utf_8':
			ll[2] = 'utf8'
		else:
			ll[2] = ll[2].lower()
		
		# if we get this far, there may be a remainder...
		rem = s.remainder()
		if rem:
			ll.append(rem.lower())
			return  "%s_%s.%s@%s" % tuple(ll)
		
		# otherwise, it's just the three basic elements
		else:
			return "%s_%s.%s" % tuple(ll)
	
	
	
	@classmethod
	def query_asset_dict(cls, loc_str):
		"""
		Query locale dict from assets.
		
		
		"""
		loc_str = cls.validate_locstr(loc_str)
		j = trix.path(cls.AssetPath).wrapper().read(loc_str)
		return trix.jparse(j)
	
	
	@classmethod
	def query_locale_dict(cls, loc_str):
		"""
		Query locale dict from system locale data.
		"""
		cline = "%s -m %s loc -c %s" % (
				sys.executable, trix.innerfpath(), loc_str
			)
		cx = trix.callx(cline)
		js = cx.reader().read()
		return trix.jparse(js)



	#
	#
	#
	#
	#
	# ---------------------------------------------------------------
	#
	#
	#
	#
	#
	
	
	#
	# DATE/TIME FORMATTING
	#  - This will have to be switched to use time.time() rather than
	#    the datetime struct because datetime doesn't resolve %R or %z,
	#    which are used by the locale formats.
	#
	def format_element(self, dt, element):
		"""
		Partial list of % code expansions for dates/times.
		"""
		
		#
		# DATE
		#
		if element == '%a':
			return self.abday[dt.tm_wday]
		
		elif element == '%A':
			return self.day[dt.tm_wday]
		
		elif element == '%b':
			return self.abmon[dt.tm_mday]
		
		elif element == '%B':
			return self.mon[dt.tm_mday]
		
		elif element == '%C':
			return str(dt.tm_year)
		
		#
		# %c? preferred date and time representation
		# %C? century number (the year divided by 100, range 00 to 99)
		# %D? same as %m/%d/%y
		#
		elif element == '%d':
			return str(dt.tm_mday)
		
		#
		# %e? day of the month (1 to 31)
		# %g - like %G, but without the century
		# %G - 4-digit year corresponding to the ISO week number (see %V).		#
		# %h - same as %b
		# %I - hour, using a 12-hour clock (01 to 12)
		# %j - day of the year (001 to 366)		
		#
		elif element == '%m':
			r = "0%i" % (dt.tm_mday)
			return r[-2:]
		
		elif element == '%w':
			return str(dt.tm_wday)
		
		elif element == '%x':
			return self.FMT_D
		
		elif element == '%y':
			r = "%i" % (dt.tm_year)
			return r[-2:]
		
		elif element == '%Y':
			return str(dt.tm_year)
		
		#
		# TIME
		#
		elif element == '%f':
			return self.day[dt.tm_wday]
		
		elif element == '%H':
			r = "0%i" % (dt.tm_hour)
			return r[-2:]
		
		elif element == '%I':
			h = dt.tm_hour
			r = "0%i" % (h-12 if h>12 else h)
			return r[-2:]
		
		elif element == '%M':
			r = "0%i" % (dt.tm_min)
			return r[-2:]
		
		elif element == '%p':
			return self.am if dt.tm_hour<12 else self.pm
		
		elif element == '%S':
			r = "0%i" % (dt.tm_min)
			return r[-2:]
		
		elif element == '%T':
			h = "0%i" % (dt.tm_hour)
			m = "0%i" % (dt.tm_min)
			s = "0%i" % (dt.tm_min)
			return "%s:%s:%s" % (h[-2:],m[-2:],s[-2:])
		
		elif element == '%y':
			return str(dt.tm_year)
		
		elif element == '%z':
			r = []
			r.append("0%i" % (dt.tm_hour))
			return r[-2:]
		
		#
		# I'll have to think about how to do these. Maybe a
		# recursive call would work...
		#
		#elif element == '%Z':
		#	return self.day[dt.xxx]
		#elif element == '%U':
		#	return self.day[dt.xxx]
		#elif element == '%W':
		#	return self.day[dt.xxx]
		#elif element == '%c':
		#	return self.day[dt.xxx]
		#elif element == '%x':
		#	return self.day[dt.xxx]
		#elif element == '%X':
		#	return self.day[dt.xxx]
		
		elif element == '%%':
			return "%"
		
		else:
			return element
	
	
	
	
	
	def getformat(self, ss):
		"""
		Return a formated date/time given a datetime struct...
		...or something.
		
		
		********* UNDER CONSTRUCTION *********
		
		I need to get the dict from the local data and find the key
		for the format I need.
		
		LIKE THIS:
		>>> ll = xLocale('en_US.utf8')
		>>> ll.locdata()["D_T_FMT"]
		'%a %d %b %Y %r %Z'
		>>> 
		>>> from datetime import *
		>>> dt = datetime.now()
		>>> dt.strftime( ll.locdata()["D_T_FMT"] )
		'Sun 01 Nov 2020 11:49:48 PM '
		>>> 
		
		
		REMEMBER THIS:
		>>> from trix.x.loc import *
		>>> ll = xLocale('en_US.utf8')
		>>> ll.locdata()["D_T_FMT"]
		'%a %d %b %Y %r %Z'
		>>> 
		
		BUGS!
		      
		      I'll have to rewrite the whole damned locale package
		      if I want this to work.
		      
		      Shouldn't be a problem.
		      
		      
		      Actually, it might not be.
		      The `format_element` method seems to be working with
		      data from the dict.
		      
		      I'll hit this again tomorrow when I'm not exhausted.
		      
		
		"""
		r = []
		#ss = trix.scan(self.D_T_FMT).split_space()
		ss = trix.scan(self.D_T_FMT).split_escape()
		for element in ss:
			r.append(self.format_element(dt_struct, element))
		
		return ''.join(r)
	
	
	
	
	
	def format(self, dt):
		"""
		Pass a date-time and a date string suitable to this locale is
		returned.
				
		"""
		
		
	
	
	
