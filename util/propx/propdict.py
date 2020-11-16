#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .proplist import *


class propdict(propiter):
	"""
	Pass a dict or dict-like object.
	
	EXAMPLE
	>>> import trix
	>>> d = trix.propx({"a":1, "b":9, "c":4})
	>>> d.display()
	{
	  "a": 1,
	  "b": 9,
	  "c": 4
	}
	>>>	
	
	"""
	
	#
	#
	# GET-ITEM
	#
	#
	def __getitem__(self, key):
		"""
		Return an item by `key`.
		
		NOTE:
		All propx-based classes' `__getitem__` methods return a propx 
		object.
		
		EXAMPLE
		>>> import trix
		>>> d = trix.propx({"a":1, "b":9, "c":4})
		>>> d['b']
		<trix/propbase int>
		>>> d['b'].o
		9
		>>>	
		"""
		return propx(self.o[key])
	
	
	#
	#
	# SET-ITEM
	#
	#
	def __setitem__(self, key, v):
		"""
		Set an item by `key`.
		
		EXAMPLE
		>>> import trix
		>>> d = trix.propx({"a":1, "b":9, "c":4})
		>>> d['b'] = "nine"
		>>> d.display()
		{
		  "a": 1,
		  "b": "nine",
		  "c": 4
		}
		>>>
		
		"""
		self.o[key] = v
	
	
	#
	#
	# KEYS PROPERTY
	#
	#
	@property
	def keys(self):
		"""
		Returns a proplist with dict keys.
		
		EXAMPLE
		>>> import trix
		>>> pd = propdict({'a':1, 'p':'q'})
		>>> pd.keys.o
		['a', 'p']
		>>> 
		
		"""
		return propx(list(self.o.keys()))
	
	
	#
	#
	# VALUES PROPERTY
	#
	#
	@property
	def values(self):
		"""
		Returns a proplist with dict values.
		
		EXAMPLE
		>>> import trix
		>>> pd = trix.propx({'a':1, 'p':'q'})
		>>> pd.values()
		[1, 'q']
		>>> 
		"""
		return propx(list(self.o.values()))
	
	
	#
	#
	# PAIRS PROPERTY
	#
	#
	@property
	def pairs(self):
		"""
		Returns a proplist with key/value pairs from dict.
		
		EXAMPLE
		>>> import trix
		>>> pd = trix.propx({'a':1, 'p':'q'})
		>>> pd.pairs()
		[('a', 1), ('p', 'q')]
		>>> 
		>>> d = trix.propx({"a":1, "b":9, "c":4})
		>>> d.pairs()
		[('a', 1), ('b', 9), ('c', 4)]
		>>> 
		
		"""
		r = []
		for k in self.o.keys():
			r.append((k, self.o[k]))
		return propx(r)
	
	
	#
	#
	# RPAIRS PROPERTY
	#
	#
	@property
	def rpairs(self):
		"""
		Returns a proplist with key/value pairs reversed, making them
		value/key pairs.
		
		EXAMPLE 1
		>>> import trix
		>>> pd = trix.propx({'a':1, 'p':'q'})
		>>> pd.pairs()
		[(1, 'a'), ('q', 'p')]
		>>> 
		>>> d = trix.propx({"a":1, "b":9, "c":4})
		>>> d.rpairs()
		[(1, 'a'), (9, 'b'), (4, 'c')]
		>>> 
		
		"""
		r = []
		for k in self.o.keys():
			r.append((self.o[k], k))
		return propx(r)
	

