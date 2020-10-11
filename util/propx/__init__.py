#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from ... import *

class propbase(object):
	"""
	Wraps objects with a set of methods convenitent for query, 
	display, and manipulation.
	
	The trix package can be of great use and, once you learn the 
	concepts, the propx package classes make working in code or in
	the terminal easy and fun.
	
	The `trix.util.propx` package defines a small set of classes that
	push results forward through dot notation and method calls. This
	allows a fun and intuitive way to gather, manipulate, and display
	data.
	
	
	# PROPX CLASS HIERARCHY
	All propx classes descend from propbase. The propiter class is the
	base for propdict, propseq, propstr, and proplist. The propgrid
	class is based on proplist.
	
    * propbase
    * |_ propiter
    *    |_propdict
    *    |_propseq
    *    |_propstr
    *    |_proplist
    *      |_propgrid
	
	
	To illustrate how propx objects work, let's take a look at a very
	simple example. The `trix.fs.Path` and its descendants make use of
	propx objects to (among other things) display directory listings.
	
	EXAMPLES: Directory Listing
	>>>
	>>> import trix
	>>> 
	>>> # sure this is fun...
	>>> trix.path('trix/util/propx').ls() 
	>>> 
	>>> # ...but isn't this nicer?
	>>> trix.path('trix/util/propx').ls.display()
	>>> 
	>>> # ...or this?
	>>> trix.path('trix/util/propx').list.grid()
	
	
	# EXPLANATION:
	So what is happening here?
	
	In the example above, the call to trix.path returns an `fs.Path` 
	object, (or an `fs.Dir` object, which is based on `fs.Path`). Many 
	of the properties of these methods return a propx object.
	
	When we call `trix.path('trix/util/propx').ls` property, a proplist
	object encapsulating the directory listing is returned. The default 
	behavior for calling a propx object as a function is to return the
	actual value held by the object. That is, the object's .o method: 
	the object `o` contained by the propx object. Therefore, calling
	`trix.path('trix/util/propx').ls()` returns a list containing the
	names of the items in the list (as provided to the proplist object's
	constructor.
	
	However, the __call__ method is only one of many methods available
	in `proplist.` The `proplist` class is based on propseq, which is
	based on propiter, and propbase, so a plethora of manipulation and
	display options are available here.
	
	  * propbase
    * |_propiter
    *   |_proplist
	
	In the "Directory Listing" examples, above, you will notice the 
	following calls:
	
	>>> trix.path('trix/util/propx').ls()          # ex 1
	>>> trix.path('trix/util/propx').ls.display()  # ex 2
	>>> trix.path('trix/util/propx').list.grid()   # ex 3
	
	In the first call, the `trix.path` method returns the default
	value from the proplist's __call__ method: A simple list of the
	names of files within the directory.
	
	The second example produces a proplist object, too, but instead of
	the retrieving the result of the `__call__()` method, the returned
	proplist object's display() method is called, printing a JSON 
	representation of the list of directory item names.
	
	In the third example, instead of calling `ls` for a simple list,
	the `list` method is called, producing a full directory listing with
	name, type, size, uid, gid, atime, mtime, and ctime.
	
	The `proplist` subclass, `propgrid`, is used to print the entire
	listing to the terminal.
	
	"""
	
	#
	# INIT
	#
	# There are two ways to create any propbase object:
	#  * Pass value, object, or callable `o`, plus args/kwargs needed 
	#    for the callable.
	#  * Pass an instance of the object the callback would have created.
	#
	#  The reason both these methods are needed is that sometimes it's
	#  more convenient to return a propbase subclass using a property.
	#  This allows the property to act like a method, returning the
	#  "normal" expected value, while still allowing the property to
	#  be called as a property to give access to the extra methods 
	#  propbase (and subclasses) provide. Eg., see `fs.Dir.list`.
	#
	#  ```
	#  trix.path().list()
	#  trix.path().list.table(width=3)
	#  ```
	#
	def __init__(self, o=None, *a, **k):
		"""
		Pass object `o`, a value, or a callable that returns a value.
		
		There are two ways to create propx object:
		 * Pass value, object, or callable `o`, plus args/kwargs needed 
		   for the callable.
		 * Pass an instance of the object the callable would have created.
		
		In the case `o` is a callable, pass also any args/kwargs required
		to execute that callable. When `self.o` is first accessed, the
		value will be calculated and stored as self.o (even if it's the
		first calling of property `self.o`).
		
		
		CALLING
		
		Until the final closing parentheses are added to an	expression, 
		dot-notation values continue producing propx objects.
		
		In the examples below, `trix.path()` produces an fs.Dir object 
		that manages, manipulates, and generally deals with directories.
		The `fs.Dir` class features several properties that produce propx
		object as results.
		
		The result returned by `trix.fs.path()` is a propx 
		object, which provides properties and methods related to file
		system paths.
		
		```
		#
		# trix.path() returns a propx object
		#
		>>> import trix
		>>> trix.path()
		>>> <trix.fs.dir.Dir '/home/nine' (d)>
		
		
		
		#
		# ls() returns a list for programatic
		#
		trix.path().ls()
		
		#
		# ls.table lets you take a peek at the data before using it
		#
		trix.path().ls.table(width=3)
		
		```
		
		"""
		self.__p = o
		self.__a = a
		self.__k = k
	
	
	
	def __repr__(self):
		return "<trix/%s %s>" % (self.T.__name__, self.To.__name__) 
	
	
	
	def __call__(self, *a, **k):
		"""
		On first call, sets the value for the `self.o` property. On
		subsequent calls, returns that value.
		
		The value of `self.o`, on the first call to this method, is
		undefined. If this object has been constructed given a callable
		as the first argument, it will be calculated here (given any
		additional constructor args/kwargs) and stored as a private
		member variable self.__o.
		
		On all calls, self.__o is returned.
		
		REMEMBER:
		The __call__ method *MUST NOT* be overridden by subclasses except
		to make necessary subclass-specific manipulations or additions
		before calling the superclass `__call__` method.
		
		"""
		try:
			return self.__o
		except:
			try:
				# if self.__p is callable...
				self.__o = self.__p(*a, **k)
			except TypeError:
				# otherwise, self.__p must be an object/value
				self.__o = self.__p
			
			return self.__o
	
	
	@property
	def o(self):
		"""
		Return this property's actual object value, as originally
		calculated by `self.__call__()`.
		"""
		try:
			return self.__o
		except:
			return self.__call__(*self.__a, **self.__k)
	
	@property
	def a(self):
		"""Returns arguments given to constructor."""
		return self.__a
	
	@property
	def k(self):
		"""Returns keyword args given to constructor."""
		return self.__k
	
	@property
	def T(self):
		"""Return the type of this `propbase` (or descendant) object."""
		return type(self)
	
	@property
	def To(self):
		"""Return the type of `self.o`."""
		return type(self.o)
	
	
	#
	#
	# UTILITY
	#
	#
	@property
	def compenc(self):
		"""
		Returns the compenc module on demand; Does not load the module 
		until first call to this property.
		
		NOTE: This is an internally used convenience more than a part of
		      the `propbase` feature set.
		"""
		try:
			return self.__compenc
		except:
			self.__compenc = trix.nmodule("util.compenc")
			return self.__compenc
	
	@property
	def jparse(self, **k):
		"""
		Return propx containing object parsed from json text. May be a
		proplist, propdict, propstr, etc...
		"""
		try:
			return propx(trix.jparse(str(self.o), **k))
		except Exception as ex:
			raise type(ex)(xdata(o=self.o, k=k))
	
	
	# ---- Methods that can handle pretty much any data type -----
	
	#
	#
	# DISPLAY
	#
	#
	def display(self, *a, **k):
		"""Display using trix.fmt. Default params: f='JDisplay'"""
		trix.display(self.o, *a, **k)
	
	
	#
	#
	# FORMATTING
	#
	#
	def json(self, *a, **k):
		"""
		Return self.o formatted as json text. Formatting may be specified.
		The default is standard JSON text.
		"""
		k.setdefault('f', 'JSON')
		return trix.formatter(*a, **k).format(self.o)
	
	
	def jcompact(self, *a, **k):
		"""Return self.o forced to jcompact text."""
		k['f'] = 'JCompact'
		return trix.formatter(*a, **k).format(self.o)
	
	
	#
	# DATA MANIPULATION
	# 
	def param(self, o=None):
		"""Returns arg `o` or `self.o` wrapped in a Param object."""
		try:
			return self.__Param(o or self.o)
		except:
			self.__Param = trix.nvalue("data.param", "Param")
			return self.__Param(o or self.o)
	
	# CURSOR
	def cursor(self, **k):
		"""
		Return a cursor containing self.o; any given keyword arguments
		are passed to the cursor's constructor.
		"""
		return trix.ncreate("data.cursor.Cursor", self.o, **k)
	
	# PDQ
	def pdq(self, **k):
		"""
		Return a python data Query object given self.o and any kwargs.
		"""
		return trix.ncreate("data.pdq.Query", self.o, **k)
	
	
	#
	# ENCODING , COMPRESSION
	#
	def b64(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base64."""
		k.setdefault('f','JCompact')
		return self.compenc.b64.encode(self.json(**k).encode(**k))
	
	def b64s(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base64."""
		k.setdefault('f','JCompact')
		return self.compenc.b64.sencode(self.json(**k).encode('utf8'))
	
	def b64u(self, **k):
		"""
		Return self.o as (compact) JSON bytes encoded to url-safe base64.
		"""
		k.setdefault('f','JCompact')
		return self.compenc.b64.uencode(self.json(**k).encode('utf8'))
	
	def b32(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base32."""
		k.setdefault('f','JCompact')
		return self.compenc.b32.encode(self.json(**k).encode(**k))
	
	def b16(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base16."""
		k.setdefault('f','JCompact')
		return self.compenc.b16.encode(self.json(**k).encode(**k))
	
	
	
	def compact(self, **k):
		"""
		Convert self.o to json, zlib-compress, and return base-64 bytes.
		Use trix.compenc.expand to revert to json.
		
		```
		from trix import *
		propx.compact("Hello, World!")
		
		```
		"""
		return self.compenc.compact(self.jcompact(**k).encode('utf8'))
	
	
	def expand(self, **k):
		"""
		Return propx containing data "expanded" from data that had
		previously been compressed by `util.compenc.compact` (such as by
		the propbase.compact() method).
		
		```
		from trix.util.propx import *
		pc = propx("Hello, World!").compact()
		propx(pc).expand().o.decode('utf8')
		
		```
		"""
		return propx(self.compenc.expand(self.o, **k))
	
	
	#
	#
	#
	#
  # Experimental
	#
	#
	#
	#
	
	#
	# CAST
	#
	def cast(self, T):
		"""
		Return a propx object given `self.o` cast as a different type.
		This would typically be used to cast an iterator as a list.
		"""
		return propx(T(self.o))
	
	
	#
	# OUTPUT - Print Contents
	#
	def output(self):
		"""
		The `output` method prints the object's contents, `self.o`.
		"""
		print (self.o)
	
	
	#
	# SPLITLINES - Bytes or Strings
	#
	def splitlines(self, *a, **k):
		"""
		Alter this propx-based object's contents by splitting bytes or
		strings.
		
		Applies only to bytes/text values. (I guess.)
		
		"""
		try:
			self.o = self.o.splitlines(**k)
		except:
			self.o = self.o.splitlines(self.o, **k)
	
	
	#
	# Maybe gather all the conversions here...? No, guess not.
	#
	
	# this one seems to work
	def propstr(self):
		return trix.ncreate("util.propx.propstr.propstr", str(self.o))
	
	# The rest will probably have to be specifically defined in the
	# appropriate classes.
	"""
	def propdict(self):
		return trix.ncreate("util.propx.propdict.propdict", self.o)
	
	def propiter(self):
		return trix.ncreate("util.propx.propiter.propiter", self.o)
	
	def proplist(self):
		return trix.ncreate("util.propx.proplist.proplist", list(self.o))
	
	def propseq(self):
		return trix.ncreate("util.propx.propseq.propseq", (self.o))
	"""
	








#
#
#
#
#
# CONVENIENCE
#  - Easy access to subclasses defined in other modules within
#    this package.
#
#
#
#


def propx(o, *a, **k):
	"""Try to calculate and return the correct wrapper."""
	
	#
	# ORDER IS IMPORTANT HERE
	#  - Checking keys/values for dict must come first.
	#  - Checking setitem must come before checking __getitem__,
	#    followed by __iter__ and generator.
	#
	
	try:
		if o.values and o.keys:
			return trix.ncreate("util.propx.propdict.propdict", o, *a, **k)
	except AttributeError as ex:
		pass
		
	try:
		o.encode
		return trix.ncreate("util.propx.propstr.propstr", o, *a, **k)
	except AttributeError as ex:
		pass
	
	try:
		o.__setitem__
		return trix.ncreate("util.propx.proplist.proplist", o, *a, **k)
	except AttributeError as ex:
		pass
	
	try:
		o.__getitem__
		return trix.ncreate("util.propx.propseq.propseq", o, *a, **k)
	except AttributeError as ex:
		pass
	
	try:
		if o.__iter__ or (type(o).__name__ == 'generator'):
			return trix.ncreate(
					"util.propx.propiter.propiter", iter(o), *a ,**k
				)
	except AttributeError as ex:
		pass
	
	
	# anything else...
	return propbase(o, *a, **k)

