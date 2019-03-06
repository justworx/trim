#
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
		trix.display(locale.localeconv())

