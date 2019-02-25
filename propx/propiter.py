#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class propiter(propbase):
	"""
	Superclass for iterable subclasses.
	
	NOTE: I'm pretty sure this class isn't needed. These functions
	      probably belong in propseq, and will move there if/when I 
	      discover there's no use for an iterator without a sequence.
	"""
	
	def __iter__(self):
		"""Return an iterator this object's list."""
		return trix.ncreate('util.xiter', self.gen)
	
	@property
	def gen(self):
		for x in self.o:
			yield(x)
	

