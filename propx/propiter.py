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
		return self.T(list(self.islice(key.start,key.stop,key.step)))
	
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
	
	def each (self, fn, *a, **k):
		"""
		Argument `fn` is a callable that operates on items from `self.o` 
		in place, one item at a time. 
		
		Returns `self`.
		"""
		for v in self.o:
			fn(v, *a, **k)
		return self
	
	
	def select (self, fn, *a, **k):
		"""
		Argument `fn` is a callable that selects/alters  items one at a 
		time, storing them in an xprop wrapper and returning the result.
		
		```
		from trix.propx import *
		pl = proplist([1,2,3])
		pl.select(lambda o: o*9)
		
		```
		"""
		r = []
		for v in self.o:
			r.append(fn(v, *a, **k))
		return propx(r)
	
	
	def grid(self, *a, **k):
		"""Display as Grid."""
		k['f'] = 'Grid'
		trix.display(self.o, *a, **k)
	
	def list(self, *a, **k):
		"""Display as List."""
		k['f'] = 'List'
		trix.display(self.o, *a, **k)
	
	def table(self, *a, **k):
		"""Display as Table. Pass keyword argument 'width'."""
		k['f'] = 'Table'
		trix.display(self.o, *a, **k)
	
	
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
			
			return propx(cls.__map(fn(*a,**k), self.o))
	
	@classmethod
	def zip(cls, *iterables):
		try:
			return propx(cls.__zip(*iterables))
		except AttributeError: #, NameError:
			try:
				cls.__zip = cls.itertool('izip')
			except Exception as ex:
				cls.__zip = zip
			return propx(cls.__zip(*iterables))
	
	
	
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
			#return self.T(type(iterable)(self.__filter(fn, iterable)))
			return propx(self.__filter(fn, iterable))
		except AttributeError:
			try:
				self.__filter = self.itertools('ifilter') #py 2
			except:
				self.__filter = filter #py3.filter == py2.itertools.ifilter
			
			#return self.T(type(iterable)(self.__filter(fn, iterable)))
			return propx(self.__filter(fn, iterable or self.o))
	
	
	def filterfalse(self, fn, iterable=None):
		iterable = iterable or self.o
		try:
			return propx(self.__filterfalse(fn, iterable))
		except:
			try:
				self.__filterfalse = self.itertool('filterfalse')
			except:
				self.__filterfalse = self.itertool('ifilterfalse')
			return propx(self.__filterfalse(fn, iterable))
	
	
	
	#
	# Here are some methods that accept optional `*iterables` or None,
	# which defaults to the iterable being `self.o`.
	#
	def chain(self, *iterables):
		"""
		Pass one or more iterables to chain together. If no iterables 
		are given, `self.o` must provide only iterables or an error is
		raised.
		"""
		itrs = iterables or self.o
		return propx(self.itertool('chain')(*itrs))
	
	def cycle(self, iterable=None):
		"""Cycle through `iterable`, if given, else `self.o`."""
		return propx(self.itertool('chain')(iterable or self.o))
	
	
	
	#
	# For the rest here, the first argument is always a function (or
	# some kind of scalar argument) while the second argument is always
	# an optional iterable with default being `self.o`, making for a
	# lot of extended functionality to propseq and proplist.
	#
	
	def accumulate(self, fn=None, iterable=None):
		fn = fn or trix.module('operator').add
		return propx(self.itertool('accumulate')(iterable or self.o, fn))
	
	
	def dropwhile(self, fn, iterable=None):
		return propx(self.itertool('dropwhile')(iterable or self.o, fn))
	
	
	def permutations(self, r, iterator=None):
		"""
		Pass r-length (and, optionally, an iterator to replace `self.o`).
		"""
		return propx(self.itertool('permutations', r,iterable or self.o))
	
	
	
	
	def starmap(self, fn, iterable=None):
		"""
		Pass a function to receive arguments. This will fail if self.o 
		(or replacement `iterable`) doesn't produce tuples.
		"""
		return propx(self.itertool('permutations',r, iterable or self.o))
	
	
	def takewhile(self, fn, iterable=None):
		return propx(self.itertool('takewhile', fn, iterable or self.o))
	
	
	
	"""
	#
	# I don't understand this one - need to work on it a bit
	#
	def groupby(self, iterable, key=None):
		pass
	
	
	
	#
	# I'm not too sure how to implement these for propiter. I'll have
	# to think about it for a while.
	#
	
	def product(self, repeat=1, *iterables):
		#	
		#	product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
		#	product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
		#	
		#	Pass integer `repeat`.... then what? How would this apply to
		#	the propiter class?
		#
		pass

	def repeat(self, object[, times]):
		#
		# How to use this when `object` is an iterator? Maybe this one
		# could go into propseq or proplist. Maybe some of the others
		# here, too, could belong to propseq.
		#
		pass
	
	def tee(self, iterable, n=2):
		pass
	
	def zip_longest(self, *iterables, fillvalue=None):
		pass
	
	def combinations(self, iterable, r):
		pass
	
	def combinations_with_replacement(self, iterable, r):
		pass
	
	
	
	#
	# I don't think i'll include this one - it's not really applicable
	# to this class.
	#
	def count(self, start=0, step=1):
		pass
	"""


