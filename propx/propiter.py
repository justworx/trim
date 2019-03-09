#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class propiter(propbase):
	"""
	Base for iterable subclasses. Pass an iterable object.
	"""
	
	def __getitem__(self, key):
		"""
		Get a slice of the remaining items.
		Note that once an item has been passed, it can no longer be 
		accessed.
		
		Repeatedly calling propiter[0] will return items one at at time
		until the iterator is exhausted.
		
		```
		ii = propiter(iter(range(0,100)))
		ii[1:5] # [1, 2, 3, 4]
		ii[95:]
		"""
		# this is probably a bad idea...
		return type(self)(list(self.islice(key.start,key.stop,key.step)))
	
	def __iter__(self):
		"""Return an iterator."""
		return trix.ncreate('util.xiter.xiter', self.o)
	
	@property
	def gen(self):
		"""Return a generator for self.o."""
		for x in self.o:
			yield(x)
	
	@property
	def sorted(self):
		"""Return a proplist with sorted content."""
		return self.T(sorted(self.o))
	
	@property
	def reversed(self):
		"""Return a proplist with reversed content."""
		return self.T(reversed(self.o))
	
	#
	# FILTERS THAT CHANGED
	#  - These filters always behave as though in python3. Even when
	#    running in python2 they use the matching itertools filter
	#    so that behavior is consistent. Always use the python3 calling
	#    convention for filtering methods that match itertools methods.
	#
	
	@classmethod
	def itertool(cls, name):
		#Loads the itertools on demand and returns  object `name`.
		try:
			return cls.__itools(name)
		except:
			itertools = trix.module('itertools')
			cls.__wrap = trix.nvalue('util.wrap', 'Wrap')
			cls.__itools = cls.__wrap(itertools)
			return cls.__itools(name)
	
	#
	# ITER-TOOLS CLASSMETHODS
	#  - classmethod filters must NOT wrap return value in type(self)
	#
	
	@classmethod
	def map(cls, fn, *iterables, **k):
		try:
			return propx(cls.__map(fn, *iterables))
		except AttributeError:
			try:
				cls.__map = cls.itertools('imap') #py 2
			except:
				cls.__map = map #py3
			
			return cls.__map(fn(*a,**k), self.o)
	
	@classmethod
	def zip(cls, *iterables):
		try:
			return cls.__zip(*iterables)
		except AttributeError: #, NameError:
			try:
				cls.__zip = cls.itertool('izip')
			except Exception as ex:
				cls.__zip = zip
			return cls.__zip(*iterables)
	
	
	# -----------------------------------------------------------------
	#
	# ITER-TOOLS
	#  - These operate on self *or* given `iterable` object.
	#
	# -----------------------------------------------------------------
	
	def filter(self, fn, iterable=None):
		# Call a filter function that behaves as it would in python3.
		try:
			iterable = iterable or self.o
			return self.T(type(iterable)(self.__filter(fn, iterable)))
		except AttributeError:
			try:
				self.__filter = self.itertools('ifilter') #py 2
			except:
				self.__filter = filter #py3 `filter` = py2 `itertools.filter`
			
			return self.T(type(iterable)(self.__filter(fn, iterable)))
			#return self.T(self.__filter(fn, iterable or self.o))
	
	
	def filterfalse(self, fn, iterable=None):
		iterable = iterable or self.o
		try:
			return self.T(type(iterable)(self.__filterfalse(fn, iterable)))
		except:
			try:
				self.__filterfalse = self.itertool('filterfalse')
			except:
				self.__filterfalse = self.itertool('ifilterfalse')
			return self.T(type(iterable)(self.__filterfalse(fn, iterable)))
	
	
	#
	# I think the rest of the itertools can be included here pretty
	# cheaply. Going to think about this - maybe later. I have some 
	# other stuff to figure out first.
	#
	"""
	def accumulate(self, iterable=None, func=operator.add):
		return self.itertool('accumulate')(iterable or self.o, func)
	
	def chain(self, *iterables):
		return self.chain(*iterables)
	
	def combinations(self, iterable, r):
		pass
	
	def combinations_with_replacement(self, iterable, r):
		pass
	
	def compress(self, data, selectors):
		pass
	
	def count(self, start=0, step=1):
		pass
	
	def cycle(self, iterable):):
		pass
	
	def dropwhile(self, predicate, iterable):
		pass
	
	def groupby(self, iterable, key=None):
		pass
	
	def permutations(self, iterable, r=None):
		pass
	
	def product(self, *iterables, repeat=1):
		pass
	
	def repeat(self, object[, times]):
		pass
	
	def starmap(self, function, iterable):
		pass
	
	def takewhile(self, predicate, iterable):
		pass
	
	def tee(self, iterable, n=2):
		pass
	
	def zip_longest(self, *iterables, fillvalue=None):
		pass
	
	
	
	
	"""
	
	
	


