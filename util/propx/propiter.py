#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *
import itertools


class propiter(propbase):
	"""Base for iterable subclasses. Pass an iterable object."""
	
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
		#return self.T(list(self.islice(key.start,key.stop,key.step)))
		try:
			return self.T(list(
					itertools.islice(self.o, key.start,key.stop,key.step)
				))
		except Exception as ex:
			raise type(ex)(xdata(
					start=key.start, stop=key.stop, step=key.step
				))
		
	
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
		
		This method is not intended to alter self.o, nor to return any
		altered value; it exists only to facilitate operations external 
		to this object.
		
		Returns `self`.
		"""
		for v in self.o:
			fn(self.param(v), *a, **k)
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
		rr = []
		for v in self.o:
			pm = self.param(v)
			fn(pm, *a, **k)
			rr.append(pm.v)
		
		return propx(rr)
	
	
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
	
	def map(self, fn, *iterables):
		"""
		The "map" filter - call using python3 conventions (even from py2).
		"""
		try:
			return propx(self.T.__map(fn, iterables or self.o))
		except AttributeError:
			try:
				self.T.__map = itertools.imap #py 2
			except:
				self.T.__map = map #py3
			
			return propx(self.T.__map(fn, iterables or self.o))
	
	
	def zip(self, *iterables):
		"""
		The "zip" filter - call using python3 conventions (even from py2).
		"""
		try:
			return propx(self.T.__zip(fn, iterables or self.o))
		except AttributeError:
			try:
				self.T.__zip = itertools.izip #py 2
			except:
				self.T.__zip = zip #py3
			
			return propx(self.T.__zip(fn, iterables or self.o))
	
	
	
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
				self.T.__filter = itertools.ifilter #py 2
			except:
				self.T.__filter = filter #py3.filter == py2.itertools.ifilter
			
			#return self.T(type(iterable)(self.__filter(fn, iterable)))
			return propx(self.T.__filter(fn, iterable or self.o))
	
	
	def filterfalse(self, fn, iterable=None):
		iterable = iterable or self.o
		try:
			return propx(self.__filterfalse(fn, iterable))
		except:
			try:
				self.T.__filterfalse = itertools.filterfalse
			except:
				self.T.__filterfalse = itertools.ifilterfalse
			return propx(self.T.__filterfalse(fn, iterable))
	
	
	
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
		return propx(itertools.chain(*itrs))
	
	
	def cycle(self, iterable=None):
		"""Cycle through `iterable`, if given, else `self.o`."""
		return propx(itertools.chain(iterable or self.o))
	
	
	
	#
	# For the rest here, the first argument is always a function (or
	# some kind of scalar argument) while the second argument is always
	# an optional iterable with default being `self.o`, making for a
	# lot of extended functionality to propseq and proplist.
	#
	
	def accumulate(self, fn=None, iterable=None):
		fn = fn or trix.module('operator').add
		return propx(itertools.accumulate(iterable or self.o, fn))
	
	
	def dropwhile(self, fn, iterable=None):
		return propx(itertools.dropwhile(iterable or self.o, fn))
	
	
	def permutations(self, r, iterator=None):
		"""
		Pass r-length (and, optionally, an iterator to replace `self.o`).
		"""
		return propx(itertools.permutations(r, iterable or self.o))
	
	
	def starmap(self, fn, iterable=None):
		"""
		Pass a function to receive arguments. This will fail if self.o 
		(or replacement `iterable`) doesn't produce tuples.
		"""
		return propx(itertools.permutations(r, iterable or self.o))
	
	
	def takewhile(self, fn, iterable=None):
		return propx(itertools.takewhile(fn, iterable or self.o))
	
	
	# other selectors
	
	def fnmatch(self, pattern): # , iterable=None <-- do this
		try:
			try:
				m = self.T.__match
				return self.T(m.filter(iter(self.o), pattern))
			except AttributeError:
				m = self.T.__match = trix.module('fnmatch')
				return self.T(m.filter(iter(self.o), pattern))
		except IndexError:
			return self.T(iter([]))
	
	
	def fnmatchcase(self, pattern):
		try:
			try:
				m = self.T.__match
				x = [n for n in self.o if m.fnmatchcase(n,pattern)]
				return self.T(x)
			except AttributeError:
				m = self.T.__match = trix.module('fnmatch')
				x = [n for n in self.o if m.fnmatchcase(n,pattern)]
				return self.T(x)
		except IndexError:
			return self.T([])
		
