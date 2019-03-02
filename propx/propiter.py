#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class propiter(propbase):
	"""
	Base for iterable subclasses. Pass an iterator or iterable object.
	"""
	
	def __iter__(self):
		"""Return an iterator this object's list."""
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
		"""Loads the itertools on demand and returns  object `name`."""
		try:
			return cls.__itools(name)
		except:
			itertools = trix.module('itertools')
			cls.__wrap = trix.nvalue('util.wrap', 'Wrap')
			cls.__itools = cls.__wrap(itertools)
			return cls.__itools(name)
	
	#
	# ITER-TOOLS CLASSMETHODS
	#  - classmethod filters should NOT wrap return value in type(self)
	#
	
	@classmethod
	def map(cls, fn, *iterables, **k):
		try:
			return propx(cls.__map(fn, *iterables))
		except AttributeError:
			try:
				cls.__map = cls.itertools('imap') #py 2
			except:
				cls.__map = map #py3 `filter`; py2 `itertools.ifilter`
			
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
	
	
	#
	#
	# ITER-TOOLS
	#  - These operate on self *or* given `iterable` object.
	#
	#
	
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
	# As far as I can see, the remaining itertools objects are 
	# consistent in py2 and py3. If we find anymore, let's append them
	# to the "FILTERS THAT CHANGED" section above.
	#
	
	#
	# I think the above filtering methods could be simplified greatly.
	# I don't like the way this is done. Have to think about this.....
	# 
	# The itertool() classmethod is OK, but everything below it - to
	# this point, is way overcomplicated. I don't think the likely
	# number of times each of these would be called warrants the
	# creation of a new class variable for each method. These objects
	# will probably turn out to be very shortlived, in most cases.
	#
	# It might be interesting, however, to develop a class that handles
	# this sort of thing - something that could be coded as a property
	# returning a __call__ method that holds the variable. WAIT... 
	# don't Loader and NLoader do this? They'd keep the speed of stored
	# method calls while reducing the code complexity quite well. Maybe
	# something to consider. The name of the object to load would be
	# the only real variable in this. OH.. and it's module path.
	#

