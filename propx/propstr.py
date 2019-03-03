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
	
	splitlines = self.o.splitlines
	
	@property
	def lines(self):
		return proplist([self.glines])
	
	@property
	def glines(self):
		for x in self.o.splitlines():
			yield (x)
	
	def scanner(self, **k):
		return trix.ncreate('data.scan.Scanner', self.o, **k)
	






