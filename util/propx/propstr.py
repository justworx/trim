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
	
	def scanner(self, **k):
		return trix.ncreate('data.scan.Scanner', self.o, **k)
	






