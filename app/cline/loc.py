+#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *
import locale

class loc(cline):
	"""
	Return a locale conversion dict for the given language.
	
	```
	python3 -m trix loc en_CA.UTF_8
	
	```
	"""
	
	def __init__(self):
		cline.__init__(self)
		locale.setlocale(locale.LC_ALL, self.args[0])
		
		rdict = {}
		rdict['convert'] = locale.localeconv()
		rdict['format'] = {
			"datetime" : locale.nl_langinfo(locale.D_T_FMT),
			"date" : locale.nl_langinfo(locale.D_FMT),
			"time" : locale.nl_langinfo(locale.T_FMT),
			"ampm" : locale.nl_langinfo(locale.T_FMT_AMPM),
			"era" : locale.nl_langinfo(locale.ERA)
		}
		trix.display()

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
