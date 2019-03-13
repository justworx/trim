#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .proplist import *


class propdict(propbase):
	"""
	Pass a dict or dict-like object.
	"""
	
	def __getitem__(self, key):
		return propx(self.o[key])
	
	def __setitem__(self, key, v):
		self.o[key] = v
	
	@property
	def keys(self):
		return proplist(list(self.o.keys()))
	
	
