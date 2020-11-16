#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *
import itertools


# -------------------------------------------------------------------
#
#
# PROP-LIST - Wrapping lists.
#
#
# -------------------------------------------------------------------

class propiter(propbase):
	"""
	The propiter class is a sort of intermediary between propbase,
	which exposes a set of data utility methods, and its subclasses,
	which wrap more complex objects such as lists, dicts, etc.
	
	Propiter methods wrap itertools functions that, for practical 
	purposes, work the same in both python2.7.x and python3.
	
	IMPORTANT:
	Always use python3 calling conventions when calling propiter's
	corresponding itertools methods, even when running python2.7.x.
	
	"""
	
	#
	#
	#  GET ITEM
	#
	#
	def __getitem__(self, key):
		"""
		Get a slice from remaining items.
		
		Note that once an item has been passed, it can no longer be 
		accessed.
		
		Repeatedly calling propiter[0] will return items one at at time
		until the iterator is exhausted.
		
		EXAMPLE:
		>>> 
		>>> import trix
		>>> x = trix.propx(([1,2],[3,4]))
		>>> x[0]
		<trix/propseq list len=2>
		>>> 
		>>> #
		>>> # Dot-o returns the value
		>>> #
		>>> x[0].o
		[1, 2]
		>>> 
		>>> #
		>>> # Calling as a method returns the value
		>>> #
		>>> x[0]()
		[1, 2]
		>>> 
		>>> 
		>>> #
		>>> # __getitem__ is implemented
		>>> #
		>>> x[:1]
		<trix/propseq tuple len=1>
		>>> 
		>>> x[:1].o
		([1, 2],)
		>>> 
		>>> x[:2].o
		([1, 2], [3, 4])
		>>> 
		>>> 
		>>> #
		>>> # The propiter object always works from its current position 
		>>> # in the stream, so repeatedly calling propiter[0:4] will 
		>>> # return the next four items until the iterator is exhausted.
		>>> #
		>>> ii = propiter(iter(range(0,100)))
		>>> ii[0:4].o
		[0, 1, 2, 3]
		>>> ii[0:4].o
		[4, 5, 6, 7]
		>>>
		
		"""
		try:
			return self.T(list(
					itertools.islice(self.o, key.start, key.stop, key.step)
				))
		except Exception as ex:
			raise type(ex)(xdata(
					start=key.start, stop=key.stop, step=key.step
				))
	
	
	#
	#
	#  ITER
	#
	#
	def __iter__(self):
		"""
		Return an iterator.
		
		To facilitate support for both python3 and python2.7.x, the 
		`trix.util.iter.iter` iterator is used by propiter.
		
		"""
		return trix.ncreate('util.xiter.xiter', self.o)
	
	
	#
	#
	#  GEN - Generator
	#
	#
	@property
	def gen(self):
		"""
		Return a generator for self.o.
		
		This property is here for internal use, but (obviously) it could
		come in handy in situations this particular class can't help with.
		
		"""
		for item in self.o:
			yield(item)
	
	
	#
	#
	#  SORTED
	#
	#
	@property
	def sorted(self):
		"""
		Return a proplist with sorted content.
		"""
		return self.T(sorted(self.o))
	
	
	#
	#
	#  REVERSED
	#
	#
	@property
	def reversed(self):
		"""
		Return a proplist with reversed content.
		"""
		return self.T(reversed(list(self.o)))
	
		
	#
	#
	#  EACH-X
	#
	#
	def eachx(self, x, *a, **k):
		"""
		Run callable `x` on each item in this object.
		
		EXAMPLE
		>>> #
		>>> # Here is a list of tuples.
		>>> #
		>>> ps = trix.propx([(0,1),(2,3)])
		>>>
		>>> #
		>>> # Convert its items to lists.
		>>> #
		>>> ps.eachx(list).o
		[[0, 1], [2, 3]]
		>>>
		
		"""
		L = []
		for item in self.o:
			L.append(x(item, *a, **k))
		return trix.propx(L)
	
	
	#
	#
	#  SELECT
	#
	#
	def select (self, fn, *a, **k):
		"""
		Argument `fn` is a callable that selects/alters items one at a 
		time, storing each in an xprop wrapper and returning the result.
		
		"""
		rr = []
		for v in self.o:
			pm = self.param(v)
			fn(pm, *a, **k)
			rr.append(pm.v)
		
		return propx(rr)
	
	
	#
	#
	#  GRID, LIST, TABLE
	#
	#
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
	
	
	
	# -----------------------------------------------------------------
	#
	# FILTERS THAT CHANGED
	#  - These filters always behave as though in python3. Even when
	#    running in python2 they use the matching itertools filter
	#    so that behavior is consistent. Always use the python3 calling
	#    convention for filtering methods that match itertools methods.
	#
	# -----------------------------------------------------------------
	
	#
	#
	#  MAP
	#
	#
	def map(self, fn, *iterables):
		"""
		The "map" filteR.
		
		Call this method using python3 conventions (even when running
		under python 2.7.x).
		
		"""
		try:
			return propx(self.T.__map(fn, iterables or self.o))
		except AttributeError:
			try:
				self.T.__map = itertools.imap #py 2
			except:
				self.T.__map = map #py3
			
			return propx(self.T.__map(fn, iterables or self.o))
	
	
	#
	#
	#  ZIP
	#
	#
	def zip(self, *iterables):
		"""
		The "zip" filter - call using python3 conventions (even from py2).
		
		EXAMPLE
		>>> from trix.util.propx.propiter import *
		>>> i = propiter([])
		>>> ii = i.zip('ABCD', 'xy') # ZIP
		>>> list(ii)
		[('A', 'x'), ('B', 'y')]
		>>> 
		
		"""
		try:
			return propx(self.T.__zip(*iterables or self.o))
		except AttributeError:
			try:
				self.T.__zip = itertools.izip #py 2.7+
			except:
				self.T.__zip = zip #py 3+
			
			return propx(self.T.__zip(*iterables or self.o))
	
	
	
	# -----------------------------------------------------------------
	#
	# ITER-TOOLS
	#  - These operate on self *or* given `iterable` object.
	#
	# -----------------------------------------------------------------
	
	#
	#
	#  FILTER
	#
	#
	def filter(self, fn, iterable=None):
		"""
		Call this filter method using python3 convention even in python2.
		
		EXAMPLE
		>>> from trix.util.propx.propiter import *
		>>> pi = propiter([]) 
		>>> list( pi.filter(lambda x: x<3, [1,2,3,4,5]) ) # FILTER
		[1, 2]
		>>>
		
		"""
		try:
			iterable = iterable or self.o
			return propx(self.__filter(fn, iterable))
		except AttributeError:
			try:
				self.T.__filter = itertools.ifilter #py 2
			except:
				# NOTE: py3.filter == py2.itertools.ifilter
				self.T.__filter = filter 
			
			return propx(self.T.__filter(fn, iterable or self.o))
	
	
	#
	#
	#  FILTER-FALSE
	#
	#
	def filterfalse(self, fn, iterable=None):
		"""
		Filter elements from iterable returning only those for which 
		the predicate is False.
		
		EXAMPLE 1: Result based on self.o value.
		>>> 
		>>> from trix.util.propx.propiter import *
		>>> piter = propiter([1,2,3,4,5])
		>>> list(piter.filterfalse(lambda x: x<3))
		[3, 4, 5]
		>>> 

		EXAMPLE 2: Populate based on a given iterable.
		>>> 
		>>> from trix.util.propx.propiter import *
		>>> pi = propiter([]) 
		>>> list( pi.filterfalse(lambda x: x<3, [1,2,3,4,5]) )
		[3, 4, 5]
		>>>
		 
		"""
		
		iterable = iterable or self.o
		try:
			return propx(self.__filterfalse(fn, iterable))
		except:
			try:
				self.T.__filterfalse = itertools.filterfalse
			except:
				self.T.__filterfalse = itertools.ifilterfalse
			return propx(self.T.__filterfalse(fn, iterable))
	
	
	
	# -----------------------------------------------------------------
	#
	# ACCEPT ITERABLES OR NONE
	#
	# Here are some methods that accept optional `*iterables` or None,
	# which defaults to the iterable being `self.o`.
	#
	# -----------------------------------------------------------------
	
	#
	#
	#  CHAIN
	#
	#
	def chain(self, *iterables):
		"""
		Pass one or more iterables to chain together. If no iterables 
		are given, `self.o` must provide only iterables or an error is
		raised.
		
		EXAMPLE
		>>> from trix.util.propx.propiter import *
		>>> list(pi.chain([1,2],[3,4,5]).o)
		[1, 2, 3, 4, 5]
		>>>
		
		"""
		itrs = iterables or self.o
		return propx(itertools.chain(*itrs))
	
	
	#
	#
	#  CYCLE
	#
	#
	def cycle(self, iterable=None):
		"""
		Cycle through `iterable`, if given, else `self.o`.
		
		EXAMPLE
		>>> from trix.util.propx.propiter import *
		>>> for x in range(1,15):
		>>> 	pi.cycle([1, 9, 10])
		>>>
		"""
		return propx(itertools.chain(iterable or self.o))
	
	
	# -----------------------------------------------------------------
	#
	# FUNCTION FILTERS
	#
	# For the rest here, the first argument is always a function (or
	# some kind of scalar argument) while the second argument is always
	# an optional iterable with default being `self.o`, making for a
	# lot of extended functionality to propseq and proplist.
	#
	# -----------------------------------------------------------------
	
	#
	#
	#  ACCUMULATE
	#
	#
	def accumulate(self, fn=None, iterable=None):
		"""
		Pass an accumulation function (default: operator.add) and,
		optionally, an iterable to replace `self.o`.
		
		NOTE: This method is *not* available in python2.
		
		"""
		fn = fn or trix.module('operator').add
		return propx(itertools.accumulate(iterable or self.o, fn))
	
	
	#
	#
	#  DROP-WHILE
	#
	#
	def dropwhile(self, fn, iterable=None):
		"""
		Drops elements from the iterable as long as the callable `fn` 
		returns True.
		"""
		return propx(itertools.dropwhile(iterable or self.o, fn))
	
	
	#
	#
	#  PERMUTATIONS
	#
	#
	def permutations(self, r, iterator=None):
		"""
		Pass r-length (and, optionally, an iterator to replace `self.o`).
		"""
		return propx(itertools.permutations(r, iterable or self.o))
	
	
	#
	#
	#  STARMAP
	#
	#
	def starmap(self, fn, iterable=None):
		"""
		Pass a function to receive arguments. This will fail if self.o 
		(or replacement `iterable`) doesn't produce tuples.
		"""
		return propx(itertools.permutations(r, iterable or self.o))
	
	
	#
	#
	#  TAKE-WHILE
	#
	#
	def takewhile(self, fn, iterable=None):
		"""
		Returns an iterator that returns elements from the iterable as 
		long as the predicate is True.
		
		EXAMPLE
		>>> from trix.util.propx.propiter import *
		>>> px = propx([1,2,3,4])
		>>> 
		>>> list(px.takewhile(lambda x: x<3))
		[1, 2]
		>>> list(px.takewhile(lambda x: x<=3))
		>>>
		 		
		"""
		return propx(itertools.takewhile(fn, iterable or self.o))
	
	
	# -----------------------------------------------------------------
	#
	# OTHER SELECTORS
	#
	# The fnmatch and fnmatchcase may be useful in this context.
	# They're here if you need them!
	#
	# -----------------------------------------------------------------
	
	#
	#
	#  FN-MATCH
	#
	#
	def fnmatch(self, pattern): # , iterable=None <-- do this
		"""
		Select items using (case-insensitive) Unix shell-style wildcards. 
		The special characters used in shell-style wildcards are:
		
			PATTERN   MEANING
			*         matches everything
			?         matches any single character
			[seq]     matches any character in seq
			[!seq]    matches any character not in seq	
		
		EXAMPLE
		>>> import trix
		>>> d = trix.path( trix.innerfpath() )
		>>> d.ls.fmnatch("*.py")
		>>>
		['__init__.py', '__main__.py']
		>>>
			 
		"""
		try:
			try:
				m = self.T.__match
				return self.T(m.filter(iter(self.o), pattern))
			except AttributeError:
				m = self.T.__match = trix.module('fnmatch')
				return self.T(m.filter(iter(self.o), pattern))
		except IndexError:
			return self.T(iter([]))
	
	#
	#
	#  FN-MATCH-CASE
	#
	#
	def fnmatchcase(self, pattern):
		"""
		Select items using (case-sensitive) Unix shell-style wildcards. 
		The special characters used in shell-style wildcards are:
		
			PATTERN   MEANING
			*         matches everything
			?         matches any single character
			[seq]     matches any character in seq
			[!seq]    matches any character not in seq	
		
		EXAMPLE
		>>> import trix
		>>> d = trix.path( trix.innerfpath() )
		>>> d.ls.fmnatchcase("*.py")
		>>>
		['__init__.py', '__main__.py']
		>>>
			 
		"""
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
	
	
