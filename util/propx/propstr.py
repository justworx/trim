#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .propseq import *


class propstr(propseq):
	"""
	Wrapping lots of cool features around text strings.
	"""
	
	@property
	def lines(self):
		return trix.ncreate(
				"util.propx.proplist.proplist", self.o.splitlines()
			)
	
	def scan(self, **k):
		"""
		Return a data/Scanner object loaded with text `self.o`.
		"""
		return trix.ncreate('data.scan.Scanner', self.o, **k)
	
	#
	# needs a regex method
	#






