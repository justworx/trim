#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ..util.output import *
from ..util.enchelp import *


# -------------------------------------------------------------------
#
#
#
# CHAIN
#
#
#
# -------------------------------------------------------------------

class Chain(object):
	"""
	Chain holds a value and provides methods to manipulate that value.
	
	>>>
	>>> from trix.data.param import *
	>>> p = Param(1)
	>>>
	>>> p.v == 1
	True
	>>>
	
	
	IMPORTANT:
	Chain is the base class for Param. The Chain class methods support
	the manipulation of data, `self.v`, but always return `self` 
	unless appended by the `null` property.
	
	Objects defined in subclass `Param` usually return a value other 
	than `self`. Calls to chain, however, always return self (unless 
	appended by the `null` property, which returns None).
	
	See the `set` method example, below.
	
	"""
	
	#
	#
	# INIT
	#
	#
	def __init__(self, v=None):
		"""Initialize `self.v`."""
		self.v = v
	
	
	#
	#
	# __CALL__
	#
	#
	def __call__(self, *a):
		"""
		Return a new Chain (or subclass) with given arguments.
		
		Calling Chein as a function causes a new copy of this object to 
		be created and returned.
		
		"""
		return type(self)(*a)
	
	
	#
	#
	# __GETITEM__
	#
	#
	def __getitem__(self, key):
		"""Return item `key` from `self.v`."""
		return self.v[key]
	
	
	#
	#
	# __SETITEM__
	#
	#
	def __setitem__(self, key, v):
		"""Set item `key` in `self.v`."""
		self.v[key] = v
	
	
	#
	#
	# PROPX
	#
	#
	@property
	def propx(self):
		"""
		Return a propx object wrapping `self.v`.
		
		SEE ALSO:
		>>> from trix.util.propx import *
		>>> help(propbase)
		"""
		return trix.propx(self.v)
	
	
	
	#
	#
	#
	# SETTING VALUES
	#
	#
	#
	
	#
	#
	# SET
	#
	#
	def set(self, v):
		"""
		Set `self.v` directly.
		
		>>> from trix.data.param import *
		>>> p = Param(1)
		>>> p.v
		1
		>>>
		>>> # Set `p.v` to a different value.
		>>> p.set(2)
		<trix.data.param.Param object at 0x7f5181044d68>
		>>> p.v
		2
		>>>
		>>> # This time, get rid of that icky repr.
		>>> p.set(3).null
		>>> p.v
		3
		>>>
		
		"""
		self.v = v
		return self
	
	
	#
	#
	# SETX
	#
	#
	def setx(self, key, value):
		"""
		Set list index (or dict key) `key` with value `value`.
		
		>>>
		>>> from trix.data.param import *
		>>> p = Param([0, 10, 20])
		>>> p.setx(1, "TEST").v
		>>>
		
		"""
		try:
			self.v[key] = value
			return self
		except BaseException as ex:
			raise type(ex)(xdata(po=self.v, key=key, value=value))
	
	
	#
	#
	# SETXX
	#
	#
	def setxx(self, items, fn, *a, **k):
		"""
		Alters a given set of `items` in a list or dict.
		
		Pass a list of item keys as `items`. The `items` arguments must 
		be a list of integers for setting list values. Each integer 
		must be the offset of an item in the list to alter.
		
		When operating on a dict, pass a list of key names.
		
		Each selected item's value is passed to callable `fn`, the 
		result replacing the corresponding item's current value.
		
		EXAMPLE:
		>>>
		>>> from trix.data.param import *
		>>> p = Param([0, 10, 20])
		>>> p.setxx([0,1,2], lambda item: item*100).v
		>>> p.setxx([0.1, 1.1, 2.3], lambda item: int(item)).v
				
		"""
		for item in items:
			val = fn(item)
			self.setx(item, val)
		return self	
	
	
	#
	#
	# CAST
	#
	#
	def cast(self, T):
		"""Type-cast self.v."""
		self.v = T(self.v)
		return self
	
	
	#
	#
	# CASTX
	#
	#
	def castx(self, x, T):
		"""Type-cast item `x` in `self.v` to type `T`."""
		self.v[x] = T(self.v[x])
		return self
	
	
	#
	#
	# JCAST
	#
	#
	def jcast(self):
		"""
		Alter string `self.v` to it's json-parsed value.
		
		EXAMPLE:
		>>> 
		>>> from trix.data.param import *
		>>> p = Param("[1,2,3]")
		>>> p.v
		'[1,2,3]'
		>>>
		>>> p.jcast().v
		[1, 2, 3]
		>>>
		>>> #
		>>> # NOTE ALSO: Calls return a param object, not the value!
		>>> #            Append .v (as above) to get the value.
		>>> #
		>>> p.jcast()
		<trix.data.param.Param object at 0x7f5178b830f0>
		>>> 
		
		"""
		v = self.v
		try:
			self.set(trix.jparse(self.v))
		except:
			self.set(self.v)
		return self
	
	
	#
	#
	# JCAST-X
	#
	#
	def jcastx(self, x):
		"""
		Typecast item `x` in `self.v` to its json-parsed value.
		
		EXAMPLE:
		>>> 
		>>> from trix.data.param import *
		>>> p = Param([1,"2",3]) # Notice item 1, the "2" in quotes.
		>>> p.jcastx(1).v
		[1, 2, 3]
		>>>
		
		"""
		self.setx(x, trix.jparse(self.v[x]))
		return self
	
	
	#
	#
	# JCAST-EACH
	#
	#
	def jcasteach(self):
		"""
		Alter each item in list `self.v` to its j-parsed value.
		
		EXAMPLE:
		>>> 
		>>> from trix.data.param import *
		>>> Param(['{"foo":"bar"}', "[1,2,3]"]).jcasteach().v
		[{'foo': 'bar'}, [1, 2, 3]]
		>>> 
		
		"""
		for x in range(len(self.v)):
			try:
				self.setx(x, trix.jparse(self.v[x]))
			except:
				pass
		return self
	
	
	
	#
	#
	#
	# CALLING RANDOM FUNCTIONS / CALLABLES
	#
	#
	#
	
	#
	#
	# PROC
	#
	#
	def proc(self, fn, *a, **k):
		"""
		Set this object's self.v to the result of the callable argument
		`fn`. All args and kwargs are passed on to the callable. Use this 
		when you want to set self.v to the callable's result.
		
		EXAMPLE:
		>>> 
		>>> from trix.data.param import *
		>>> p = Param(10)
		>>> p.proc(lambda x: x*2).v
		20
		>>> 
		
		"""
		self.v = fn(self.v, *a, **k)
		return self
	
	
	#
	#
	# PROCX
	#
	#
	def procx(self, item, fn, *a, **k):
		"""
		Set `item` in `self.v` to the result of `fn`.
		
		EXAMPLE:
		>>> 
		>>> from trix.data.param import *
		>>> p = Param([0, 10, 20])
		>>> p.procx(1, lambda x: x*2).v
		20
		>>> 
		
		"""
		newvalue = fn(self.v[item], *a, **k)
		self.setx(item, newvalue)
		return self
	
	
	#
	#
	# CALL
	#
	#
	def call(self, fn, *a, **k):
		"""
		This method allows the random calling of an executable object 
		with no forced ties to `self.v`. It may be useful in cases where
		the given values are operated on by an external callable.
		
		REM: You must pass `self.v` as an argument if you want it to be
		     altered.
		
		```
		def listbump(ls):
		  for i in range(0, len(ls)):
		    ls[i] = ls[i]+1
		
		p = Param([1,2,3])
		p.v                       # [1,2,3]
		p.call(listbump, p.v).v   # [2,3,4]

		```
		
		"""
		fn(*a, **k)
		return self	
	
	
	
	#
	#
	#
	# STRING OPS
	#
	#
	#
	
	#
	#
	# SPLIT
	#
	#
	def split(self, *a, **k):
		"""
		Split `self.v` by the string given as the first argument, or by
		the default, if no arguments are given. Keyword args are applied
		to the `str.split()` method.
		"""
		self.v = self.v.split(*a, **k)
		return self
	
	
	#
	#
	# JOIN
	#
	#
	def join(self, c=' ', *a):
		"""
		Join list items by character `c`. If no additional arguments are
		given, all items in list `self.v` are joined. If additional args
		are given, they must be integers that give offsets from self.v to 
		join.
		
		NOTE: All list values are cast as unicode before being joined.
		"""
		x = self.v
		u = unicode
		vv =  [u(x[i]) for i in a] if a else [u(v) for v in x]
		self.v = u(c).join(vv)
		return self
	
	
	#
	#
	# PAD
	#
	#
	def pad(self, mlen, val=''):
		"""
		Pad a sequence with `val` items to a minimum length of `mlen`.
		This method allows the expansion of string values to a minimum
		length (eg., for visual formatting of grids in a terminal).
		""" 
		val = val if len(str(val)) else ' '
		try:
			while len(self.v) < mlen:
				self.v.append(val)
		except AttributeError:
			while len(self.v) < mlen:
				self.v += val
			
		return self
	
	
	#
	#
	# STRIP
	#
	#
	def strip(self, c=None, alignment=0):
		"""
		Strip characters matching `c`, or whitespace, if c==None.
		If `alignment` < 0, only left-stripping is done using `lstrip()`. 
		If it's > 0, `rstrip()` is used. Default is 0, `strip()`
		"""
		if alignment < 0:
			self.v = self.v.lstrip(c)
		elif alignment > 0:
			self.v = self.v.rstrip(c)
		else:
			self.v = self.v.strip(c)
		return self
	
	
	
	#
	#
	#
	# OTHER/UTIL
	#
	#
	#
	
	#
	#
	# EACH
	#
	#
	def each(self, fn, *a, **k):
		"""
		Pass a callable `fn` that accepts Param object `p`, index (or 
		key) `i`, and the value of p[i], `v`. Callable `fn` is called,
		receiving the param object `p`, the offset/key `i`, and value `v`
		for each item.
		"""
		for x in enumerate(self.v):
			#
			# Here, self is this param object, x[0] is the index `i`, and
			# x[1] is the value, `v`, so... callable `fn` receives p,i,v.
			#
			fn(self, x[0], x[1], *a, **k)
		return self
	
	
	#
	#
	# OUTPUT
	#
	#
	def output(self, v=None, *a):
		"""Print `self.v`; for testing."""
		v = v or self.v
		Output().output(str(v))
		return self
	
	
	#
	#
	# WRITE
	#
	#
	def write(self, v=None, *a):
		"""Print `self.v`; for testing."""
		BaseOutput().output(str(v or self.v))
		return self
	
	
	#
	#
	# NULL
	#
	#
	@property
	def null(self):
		"""
		Tack this method to the end of a chain of calls to return None.
		Eg., Param("Hello, World").output().null
		"""
		return None



# -------------------------------------------------------------------
#
#
#
# PARAM
#
#
#
# -------------------------------------------------------------------

class Param(Chain):
	"""
	Param methods manipulate or evaluate data; usually the self.v value
	is involved. All methods work with either self.v or, in some cases,
	an optional second argument to use instead of self.v.
	
	Comparison methods eq, neq, gt, ge, lt, and le all require one
	argument and accept an optional second argument (which defaults to
	self.v).
	
	Methods inherrited from Chain always return `self`, so that calls 
	can be chained through a lambda, whereas Param methods typically, 
	if not always, return value resulting from the method. 
	
	Param doesn't come easy. There's a lot to learn but, once you get 
	it, it's a powerful tool for use in lambdas.
	
	"""
	def __init__(self, v=None, i=None):
		"""
		The constructor sets `self.v` and `self.i` to the given values. 
		Default for `i` is None.
		
		>>>
		>>>
		"""
		self.v = v
		self.i = i
	
	def __call__(self, *a):
		"""Return a new Param object with given arguments."""
		if len(a) < 1:
			return type(self)(self.v, self.i)
		elif len(a) < 2:
			return type(self)(a[0], self.i)
		else:
			return type(self)(*a)
	
	def __getitem__(self, key):
		return self.v[key]
	
	def __len__(self):
		return len(self.v)
	
	
	# PARAM INFO
	@property
	def iv(self):
		"""Return (index,value)"""
		return (self.i, self.v)
	
	@property
	def vi(self):
		"""Return (value,index)"""
		return (self.v, self.i)
	
	
	# VALUE INFO
	@property
	def type(self):
		"""Return the type of the current value."""
		return type(self.v)
	
	@property
	def len(self):
		"""Return the length of the current value."""
		return len(self.v)
	
	
	# reg-ex module access
	@property
	def re(self):
		"""Return the regular expression module `re`."""
		try:
			return self.__re
		except:
			self.__re = __import__('re')
			return self.__re
	
	
	# EVALUATION
	@property
	def true(self):
		return True
	
	@property
	def false(self):
		return False
	
	
	# BOOL
	def bool(self, v):
		return v
	
	# SKIP
	def skip(self, *a):
		"""
		Skip this item if the first given argument is True.
		
		Use this method at the end of a lambda to return True or False 
		based on the given argument's boolean evaluation.
		"""
		return len(a) and bool(a[0])


	# CONTAINS
	def contains(self, v, b=True):
		"""Return `b` (default True) if `v` exists in `self.v`."""
	
	
	#
	# COMPARISON
	#  - I'm thinking these are a really bad idea. I've never used them,
	#    and I'm looking at them now and thinking... WTH was I thinking?
	#  - I mean really... how often is self.v a scalar value? When would
	#    non-scalar types be able to make use of this?
	#  - I'm pretty sure these are not going to be here much longer.
	#
	def eq(self, v):
		"""Comparison: `v` equal to self.v"""
		return self.v == v
	
	def neq(self, v):
		"""Comparison: not equal to;"""
		return self.v != v
	
	def ge(self, v):
		"""Comparison: greater than/equal to;"""
		return self.v >= v 
	
	def le(self, v):
		"""Comparison: less than/equal to;"""
		return self.v <= v 
	
	def gt(self, v):
		"""Comparison: greater than;"""
		return self.v > v
	
	def lt(self, v):
		"""Comparison: less than;"""
		return self.v < v
	
