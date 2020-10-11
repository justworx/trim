#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .proplist import *


class propdict(propiter):
	"""
	Pass a dict or dict-like object.
	"""
	
	def __getitem__(self, key):
		return propx(self.o[key])
	
	def __setitem__(self, key, v):
		self.o[key] = v
	
	
	@property
	def keys(self):
		"""
		Returns a proplist with dict keys.
		
		EXAMPLE
		>>>
		>>> pd = propdict({'a':1, 'p':'q'})
		>>> pd.keys.o
		['a', 'p']
		>>> 
		
		"""
		return proplist(list(self.o.keys()))
	
	@property
	def values(self):
		"""
		Returns a proplist with dict values.
		"""
		return proplist(list(self.o.values()))
	
	@property
	def pairs(self):
		"""
		Returns a proplist with key/value pairs from dict.
		
		EXAMPLE
		>>>
		>>> pd = propdict({'a':1, 'p':'q'})
		>>> pd.pairs()
		[('a', 1), ('p', 'q')]
		>>> 
		
		"""
		r = []
		for k in self.o.keys():
			r.append((k, self.o[k]))
		return proplist(r)
	
	@property
	def rpairs(self):
		"""
		Returns a proplist with key/value pairs reversed, making them
		value/key pairs.
		
		EXAMPLE
		>>>
		>>> pd = propdict({'a':1, 'p':'q'})
		>>> pd.pairs()
		[(1, 'a'), ('q', 'p')]
		>>> 
		"""
		r = []
		for k in self.o.keys():
			r.append((self.o[k], k))
		return proplist(r)
	

