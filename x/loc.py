#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import locale

class loc(object):
	"""
	Wraps the `locale` module functionality.
	"""
	
	@property
	def locale(self):
		return locale.getlocale()
	
	
	def info(self, x):
		"""
		Low level method that returns values, format strings, or other
		data that corresponds to locale module code numbers. This is used
		by many of the following methods.
		"""
		return locale.nl_langinfo(x)
	
	
	#
	#
	# Conversion Methods
	#
	#
	def str(self, number):
		"""Converts numeric types (int, float) to string."""
		return locale.str(number)
	
	def ntoa(self, number):
		"""
		Converts numeric types (int, float) to string. This method is
		the same as `str`, but with a name similar to `atoi`, `atof`,
		etc...
		"""
		return locale.str(number)
	
	def atoi(self, i):
		"""Convert string `i` to integer."""
		return locale.atoi(i)
	
	def atof(self, f):
		"""Convert string `f` to float."""
		return locale.atof(i)
	
	def atob(self, YyNn):
		"""
		Pass a (case insensitive) character that indicates Yes or No for
		the locale. Returns boolean.
		"""
		return bool( re.match(self.yes(), YyNn) )
	
	def bool(self, YyNn):
		"""Alias for atob."""
		return bool( re.match(self.yes(), YyNn) )
		return bool( re.match(self.yes(), YyNn) )
	
	#def currency(self, f):
	#	c = self.str(f)
		
	
	#
	#
	# Localized Values
	#
	#
	def day(self, i):
		"""Pass int `i`, day of week, a value 1 through 7."""
		return self.info(self.DAY[i-1])
		
	def mon(self, i):
		"""Pass int `i`, month, a value 1 through 12."""
		return self.info(self.MON[i-1])
		
	def abday(self, i):
		"""Pass int `i`, abbreviated day of week, a value 1 through 7."""
		return self.info(self.ABDAY[i-1])
		
	def abmon(self, i):
		"""Pass int `i`, abbreviated month, a value 1 through 12."""
		return self.info(self.ABMON[i-1])

	
	
	#
	#
	# QUERIED INFO
	#
	#
	def radix(self):
		"""
		Returns radix character, separating number from decimal places.
		"""
		return self.info(locale.RADIXCHAR)
	
	def thousep(self):
		"""Thousands separator."""
		return self.info(locale.THOUSEP)
	
	def yes(self):
		"""Yes regex expression separator."""
		return self.info(locale.YESEXPR)
	
	def no(self):
		"""No regex expression separator."""
		return self.info(locale.NOEXPR)
	
	def curloc(self):
		"""
		Currency symbol placement indicator.
		 * Minus sign '-' indicates the currency symbol should be placed 
		   before the value.
		 * Plus sign '+' indicates the symbol should follow after the 
		   value.
		 * Period (dot) '.' indicates the symbol should replace the radix
		   character.
		"""
		return self.info(locale.CRNCYSTR)
	
	def era(self):
		"""Era expression."""
		return self.info(locale.ERA)

	
	#
	#
	# Formats
	#  - This section returns format strings
	#
	#
	def datetime(self):
		"""Localized datetime format string."""
		return self.info(locale.D_T_FMT)
	
	def date(self):
		"""Localized date format string."""
		return self.info(locale.D_FMT)
	
	def time(self):
		"""Localized time format string."""
		return self.info(locale.T_FMT)
	
	def ampm(self):
		"""Localized AM/PM strings."""
		return self.info(locale.T_FMT_AMPM)

		
	#
	# CONSTANT LISTS
	#  - These constants help make the above date-related methods easier
	#    to call.
	#
	DAY = [
		locale.DAY_1, locale.DAY_2, locale.DAY_3, locale.DAY_4,
		locale.DAY_5, locale.DAY_6, locale.DAY_7
	]
	
	ABDAY = [
		locale.ABDAY_1, locale.ABDAY_2, locale.ABDAY_3, locale.ABDAY_4,
		locale.ABDAY_5, locale.ABDAY_6, locale.ABDAY_7
	]
	
	MON = [
		locale.MON_1, locale.MON_2, locale.MON_3, locale.MON_4,
		locale.MON_5, locale.MON_6, locale.MON_7, locale.MON_8,
		locale.MON_9, locale.MON_10, locale.MON_11, locale.MON_12
	]
	
	ABMON = [
		locale.MON_1, locale.MON_2, locale.MON_3, locale.MON_4,
		locale.MON_5, locale.MON_6, locale.MON_7, locale.MON_8,
		locale.MON_9, locale.MON_10, locale.MON_11, locale.MON_12
	]
