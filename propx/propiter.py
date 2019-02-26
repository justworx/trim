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
		return trix.ncreate('util.xiter', self.o)
	
	
	@property
	def gen(self):
		"""Return a generator for self.o."""
		for x in self.o:
			yield(x)
	
	
	@property
	def sorted(self):
		"""Return a proplist with sorted content."""
		return propx(sorted(self.o))
	
	@property
	def reversed(self):
		"""Return a proplist with reversed content."""
		return propx(list(reversed(self.o)))
	
	#
	# These filters always behave as though in python3. Even when
	# running in python2 they use the matching itertools filter
	# so that behavior is consistent. Always use the python3 calling
	# convention for classmethods that match itertools methods.
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

	def filter(self, fn, iterable=None):
		# Call a filter function that behaves as it would in python3.
		try:
			return self.__filter(fn, iterable or self.o)
		except AttributeError:
			try:
				self.__filter = self.itertools('ifilter') #py 2
			except:
				self.__filter = filter #py3 `filter` = py2 `itertools.filter`
			
			return self.__filter(fn, iterable or self.o)
	
	
	def filterfalse(self, fn, iterable=None):
		try:
			return self.__filterfalse(fn, iterable or self.o)
		except:
			try:
				self.__filterfalse = self.itertool('filterfalse')
			except:
				self.__filterfalse = self.itertool('ifilterfalse')
			return self.__filterfalse(fn, iterable or self.o)
	
	
	#
	# ITER-TOOLS CLASSMETHODS
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
			
			return propx(cls.__map(fn(*a,**k), self.o))
	
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
	# As far as I can see, the remaining itertools objects are 
	# consistent in py2 and py3. If we find anymore, let's append them
	# to the "FILTERS THAT CHANGED" section above.
	#

