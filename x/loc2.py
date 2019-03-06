#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

import locale

class loc(object):
	
	def atoi(self, i):
		return locale.atoi(i)
	
	def atof(self, f):
		return locale.atof(i)
	
	def str(self, number):
		return locale.str(number)
	
	
	#
	# QUERIED INFO
	#
	def info(self, x):
		return locale.nl_langinfo(x)
	
	# characters
	def radix(self):
		"""Radix character, separating number from decimal places."""
		self.info(locale.RADIXCHAR)
	
	def thousep(self):
		"""Thousands separator."""
		self.info(locale.THOUSEP)
	
	def yes(self):
		"""Yes regex expression separator."""
		self.info(locale.YESEXPR)
	
	def no(self):
		"""No regex expression separator."""
		self.info(locale.NOEXPR)
	
	def cur(self):
		"""Currency symbol."""
		self.info(locale.CRNCYSTR)
	
	def era(self):
		"""Era expression."""
		self.info(locale.ERA)
	
	# formats
	def datetime(self):
		"""Local datetime format."""
		return self.info(locale.D_T_FMT)
	
	def date(self):
		return self.info(locale.D_FMT)
	
	def time(self):
		return self.info(locale.T_FMT)
	
	def ampm(self):
		return self.info(locale.T_FMT_AMPM)
	
	#
	# calendar
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


