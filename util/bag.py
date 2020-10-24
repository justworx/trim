#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *


class Bag(object):
	"""
	A selection of values, sorted by name.
	
	Bag objects always store values in a defaultdict dict. Pass the key
	to set
	
	EXAMPLE
	>>> from trix.util.bag import *
	>>> b = Bag(int)
	>>> b.put("one", 1)
	>>> b.get("one")
	1
	>>> b.get("two")
	0
	>>> 
	
	#
	# TO DO:
	#  * There should be an option to enforce type.
	#  * There should be an option to force type conversion.
	#  * There should be an option to attempt type conversion.
	#
	
	"""
	
	def __init__(self, T):
		"""
		Pass the type of object this bag holds.
	
		EXAMPLE
		>>> from trix.util.bag import *
		>>> b = Bag(int)
		>>>
		"""
		try:
			self.__d = Bag.defaultdict(T)
		except:
			Bag.defaultdict = trix.value("collections.defaultdict")
			self.__d = Bag.defaultdict(T)
	
	
	def __getitem__(self, key):
		"""
		Get Bag item.
	
		EXAMPLE
		>>> from trix.util.bag import *
		>>> b = Bag(int)
		>>> b.put("one", 1)
		>>> b[0]
		1
		>>>
		"""
		return self.__d[key]
	
	
	def __len__(self):
		return len(self.__d)
	
	
	
	#
	#
	# DICT
	#
	#
	@property
	def dict(self):
		"""
		Return the current dict value wrapped in a propx object.
		Call this property as a function to get the resulting dict.

		EXAMPLE
		>>> b = Bag(int)
		>>> b.put("one", 1)
		>>> b.put("two", 2)
		>>> b.dict.display()
		{
		  "one": 1,
		  "two": 2
		}
		>>> 
			
		"""
		return propx(dict(self.__d))
	
	
	#
	#
	# LIST
	#
	#
	@property
	def list(self):
		"""
		Return the current list value wrapped in a propx object.
		Call this property as a function to get the resulting dict.
		
		>>> from trix.util.bag import *
		>>> b = Bag(list)
		>>> b.add("numbers", [1])
		>>> b.add("numbers", [3])
		>>> b.get('numbers')
		[1, 3]
		>>> b.get.display()
		>>>
		
		"""
		return propx(self.__d)
	
	
	#
	#
	# GET
	#
	#
	def get(self, key):
		"""
		Get value of key. 
		
		Default may not be specified - it's always the empty value of the 
		object's type.
		
		"""
		return self.__d[key]
	
	
	#
	#
	# PUT
	#
	#
	def put(self, key, value):
		"""Set or change a key/value pair."""
		self.__d[key] = value
	
	
	#
	#
	# ADD
	#
	#
	def add(self, key, x):
		"""
		Add `x` to key value.
		
		EXAMPLE 1
		>>> b = Bag(int)
		>>> b.put("one", 1)
		>>> b.add("one", 1)
		>>> b.dict()
		{'one': 2}
		
		Addition of items to a list bag appends the item.
		
		EXAMPLE 2
		>>> b.add("one", [1])
		>>> b.add("one", [3])
		>>> b.dict()
		{'one': [1, 3]}
		>>> 
		
		If unset, set key's value to `x`. This allows the summation of
		Bag entries to be handled in a loop using only the `add` method,
		instead of forcing the use of `put` for the first addition.
		
		EXAMPLE 3
		>>> b = Bag(int)
		>>> b.add("one", 1)
		>>> b.add("one", 1)
		>>> b.dict()
		{'one': 2}
		>>> 
		
		Note that this also works with strings.
		
		EXAMPLE 4
		>>> b.add('one', "foo")
		>>> b.add('one', "bar")
		>>> b.add('two', "to")
		>>> b.add('two', "too")
		>>> b.dict()
		{'one': 'foobar', 'two': 'totoo'}
		
		"""
		try:
			self.__d[key] += x
		except KeyError:
			self.__d[key] = x


