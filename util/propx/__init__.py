#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from ..enchelp import *


# -------------------------------------------------------------------
#
#
# PROP-BASE - Basic utilities for propx subclasses.
#
#
# -------------------------------------------------------------------

class propbase(EncodingHelper):
	"""
	Wraps objects with a set of methods convenitent for query, 
	display, and manipulation.
	
	The propx package can be of great use and, once you learn the 
	concepts, the propx package classes make working in code or in
	the terminal easy and fun.
	
	The `trix.util.propx` package defines a small set of classes that
	push results forward through dot notation and method calls. This
	allows a fun and intuitive way to gather, manipulate, and display
	data.
	                                             
	# PROPX CLASS HIERARCHY                         
	All propx classes descend from propbase.         propbase  
	The propiter class is the base for propdict,     |_propiter  
	propseq, propstr, and proplist. The propgrid       |_propdict
	class is based on proplist.                        |_propseq
	                                                   |_propstr
	To illustrate how propx objects work, let's        |_proplist  
	take a look at a very simple example. The            |_propgrid
	`trix.fs.Path` and its descendants make use of
	propx objects to (among other things) display 
	directory listings.
	
	EXAMPLE: Directory Listing
	>>>
	>>> import trix
	>>> 
	>>> #
	>>> # Sure this is fun...
	>>> #
	>>> trix.npath('util/propx').ls() 
	['__init__.py', 'propstr.py', 'propiter.py', 'propdict.py', 
	'proplist.py', '_propall.py', 'propseq.py']
	>>> 
	>>> #
	>>> # ...but isn't this a nicer view?
	>>> #
	>>> trix.npath('util/propx').ls.display()
	[
	  "__init__.py",
	  "propstr.py",
	  "propiter.py",
	  "propdict.py",
	  "proplist.py",
	  "_propall.py",
	  "propseq.py"
	]
	>>> 
	>>> #
	>>> # ...or this?
	>>> #
	>>> trix.npath('util/propx').list.grid()
	name         type size  uid  gid  atime      mtime      ctime     
	__init__.py  f    13362 1000 1000 1602791711 1602791711 1602791711
	propstr.py   f    1438  1000 1000 1602739773 1602625146 1602625146
	propiter.py  f    7583  1000 1000 1602789805 1602789708 1602789708
	propdict.py  f    1301  1000 1000 1602739773 1602625146 1602625146
	proplist.py  f    7873  1000 1000 1602791475 1602790478 1602790478
	_propall.py  f    370   1000 1000 1602739773 1602625146 1602625146
	propseq.py   f    1677  1000 1000 1602744617 1602744125 1602744125
	>>>
	
	
	# EXPLANATION:
	So what is happening up there?
	
	Because "trix/util/propx" is a directory, the call to `trix.path`
	returns an `fs.Dir` object (based on `fs.Path`). Many properties of
	`fs.Dir` (including `list` and `ls`) return a propx object.
	
	When we call `trix.npath('util/propx').ls`, a proplist object 
	encapsulating the directory listing is returned.
	
	The default behavior for calling a propx object *as a function* is 
	to return the actual value held by the object. It is an alias for
	the object's .o property.
	
	>>>
	>>> trix.npath('util/propx').ls.o 
	['__init__.py', 'propstr.py', 'propiter.py', 'propdict.py', 
	'proplist.py', '_propall.py', 'propseq.py']
	>>>
	>>> trix.npath('util/propx').ls() 
	['__init__.py', 'propstr.py', 'propiter.py', 'propdict.py', 
	'proplist.py', '_propall.py', 'propseq.py']
	>>> 
	
	Therefore, despite that `Path.ls` is a property, calling 
	`trix.path('trix/util/propx').ls()` returns a  list containing the
	directory listing.
	
	
	#
	# A PLETHORA OF FEATURES
	#
	The __call__ method is only one of many methods made available by 
	`proplist.` The `proplist` class is based on propiter, and propbase,
	so a plethora of manipulation and display options are available.
	
	  * propbase
    * |_propiter
    *   |_proplist
    *     |_propgrid
	
	In the "Directory Listing" examples, above, you will notice the 
	following calls:
	
	>>> trix.npath('util/propx').ls()          # ex 1
	>>> trix.npath('util/propx').ls.display()  # ex 2
	>>> trix.npath('util/propx').list.grid()   # ex 3
	
	In the first call, the `trix.npath` method returns the default
	value from the proplist's __call__ method: A simple list of the
	names of files within the directory.
	
	The second example produces a proplist object, too, but instead of
	the retrieving the result of the `__call__()` method, the returned
	proplist object's `display()` method is called, printing a JSON 
	representation of the list of directory item names.
	
	In the third example, instead of calling `ls` for a simple list,
	the `list` method is called, producing a full directory listing with
	name, type, size, uid, gid, atime, mtime, and ctime.
	
	The `proplist` subclass, `propgrid`, is used to print the entire
	listing to the terminal. The `propgrid` class includes a method for
	returning a `trix.data.dbgrid.DBGrid` object wrapping the directory
	results in a temporary sqlite3 table, so results may be sorted or
	otherwise adjusted as necessary using sql statements.
		
	EXAMPLE
	>>> import trix
	>>> 
	>>> # Get a `trix.fs.dir.Dir` object.
	>>> d = trix.npath('util/propx').list
	>>>
	>>> # Get a dbgrid object naming the table 'tb'.
	>>> dg = d.propgrid.dbgrid("tb")
	>>>
	>>> # Run a query and check out the results.
	>>> dg("select type, size, uid from tb order by size").grid()
	>>>
	>>> # Massage the data as needed, then get the modified object.
	>>> dg("select type, size, uid from tb order by size").o
	[['type', 'size', 'uid'], ['f', 370, 1000], ['f', 1510, 1000], 
	 ['f', 1771, 1000], ['f', 1990, 1000], ['d', 4096, 1000], 
	 ['f', 10166, 1000], ['f', 12629, 1000], ['f', 22159, 1000]]
	>>> 	
	
		
	SEE ALSO:
	>>> from trix.data.dbgrid import *
	>>> help(DBGrid)
	>>>
	>>> from trix.util._propall import *
	>>> help(propgrid)
	>>>
	
	"""
	
	#
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
		
		In the examples below, `trix.path()` produces an `fs.Dir` object 
		that manages, manipulates, and generally deals with directories.
		The `fs.Dir` class features several properties that produce propx
		object as results.
		
		The result returned by `fs.dir.ls()` is a propx 
		object, which provides properties and methods related to file
		system paths.
		
		
		```
		#
		# trix.path() returns an fs.Path or fs.Dir object
		#
		>>> import trix
		>>> trix.path()
		<trix.fs.dir.Dir '/home/me' (d)>
		>>> 		
		
		#
		# The `fs.ls()` method returns a proplist. Calling `ls()` as a
		# function returns the raw data. So would `ls.o`.
		#
		trix.path().ls()
		
		#
		# However, the ls method returns a propx object, which may be
		# used to take a peek at the data before using it.
		#
		trix.npath().ls.table(width=3)
		
		```
		
		"""
		#
		# The `self.__p` value is set to a value, object, or callable.
		# It won't be calculated until the `self.o` property is called,
		# at which time self.__o will be added to the object's private
		# member variables.
		#
		
		k.setdefault("encoding", DEF_ENCODE)
		k.setdefault("errors", DEF_ERRORS)
		
		self.__p = o
		self.__a = a
		self.__k = k
		
		# init the base class
		EncodingHelper.__init__(self, **k)


	#
	#
	#  REPR
	#  - This is "terminal" because it terminates the object's "repr".
	#
	#
	def __repr__(self):
		return "<trix/%s %s>" % (self.T.__name__, self.To.__name__) 
	
	
	#
	#
	#  CALL
	#   - This method is terminal because it returns the value held 
	#     by this propx object.
	#
	#
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




	# -----------------------------------------------------------------
	#
	#
	#
	# TERMINATING PROPERTIES/METHODS (TERMINAL)
	#  - This section's property and method results are *NOT* wrapped 
	#    in propx objects.
	#  - These properties are mostly used internally, but are useful
	#    as terminals, and when debugging.
	#
	#
	#
	# -----------------------------------------------------------------
	
	
	#
	#
	#  O (OBJECT)
	#   - This method is terminal because it returns the value held 
	#     by this propx object.
	#
	#
	@property
	def o(self):
		"""
		Return this property's actual object value, as originally
		calculated by `self.__call__()`.
		"""
		try:
			return self.__o
		except:
			self.__o = self.__call__(*self.__a, **self.__k)
			return self.__o
	
	
	#
	#
	# A - Args given to constructor
	#   - This method is terminal because it returns a python list
	#     containing any arguments passed to this object's constructor.
	#
	#
	@property
	def a(self):
		"""Returns arguments given to constructor."""
		return self.__a
	
	
	#
	#
	# K - Keyword-args given to constructor
	#   - This method is terminal because it returns a python list
	#     containing any keyword arguments passed to this object's 
	#     constructor.
	#
	#
	@property
	def k(self):
		"""Returns keyword args given to constructor."""
		return self.__k
	
	
	#
	#
	# T - Type of Propbase Object
	#   - This method is terminal because it returns the type of 
	#     this object.
	#
	#
	@property
	def T(self):
		"""Return the type of this propbase-based object."""
		return type(self)
	
	
	#
	#
	# TO - Type of Object
	#   - This method is terminal because it returns the type of 
	#     the object passed to this object's constructor.
	#
	#
	@property
	def To(self):
		"""Return the type of `self.o`."""
		return type(self.o)
	
	
	
	
	
	#
	#
	# PARSER
	#
	#
	def parser(self, **k):
		try:
			return self.__parser
		except:
			self.__parser = trix.ncreate("util.parse.Parser", **k)
			return self.__parser
			#
			# I *THINK* this will be fine because the lifespan of any
			# propx object is only one use. I can't see a way that the
			# encoding/errors values would change through the course
			# of manipulating parsed objects, unless maybe someone were
			# passing an array or dict with strings encoded in different
			# encodings.
			# 
			# KEEP AN EYE ON THIS, THOUGH! 
			# I keep finding the unexpected in the propx subpackage!
			#
	
	
	
	#
	#
	# COMP-ENC
	#   - This method is terminal because it returns the `util.compenc`
	#     module.
	#
	#
	@property
	def compenc(self):
		"""
		Returns the `compenc` module on demand; Does not load the module 
		until first call to this property.
		
		TERMINAL!
		This method does not return a propx object.
		
		NOTE: This is an internally used convenience more than a part of
		      the `propbase` feature set. It implements all the base-x
		      methods, as well as compact and expand.
		      
		"""
		try:
			return self.__compenc
		except:
			self.__compenc = trix.nmodule("util.compenc")
			return self.__compenc
	
	
	
	
	
	#
	#
	# CURSOR
	#  - This is "terminal" because it terminates the chain of propx
	#    objects by returning a `data.cursor.Cursor` object.
	#
	#
	def cursor(self, **k):
		"""
		Return a cursor containing `self.o`.
		
		Any given keyword arguments are passed to the cursor's 
		constructor.
		
		TERMINAL!
		This method does not return a propx object.
		
		"""
		return trix.ncreate("data.cursor.Cursor", self.o, **k)
	
	
	#
	#
	# DATA MANIPULATION
	#  - This is "terminal" because it terminates the chain of propx
	#    objects by returning a Param object.
	#
	# 
	def param(self, o=None):
		"""
		Returns arg `o` or `self.o` wrapped in a `data.param.Param` 
		object.
		
		TERMINAL!
		This method does not return a propx object.
		
		SEE ALSO:
		>>> from trix.data.param import *
		>>> help(Param)
		
		"""
		try:
			return self.__Param(o or self.o)
		except:
			self.__Param = trix.nvalue("data.param", "Param")
			return self.__Param(o or self.o)
	
	
	#
	#
	# PDQ
	#  - This is "terminal" because it terminates the chain of propx
	#    objects by returning a `data.pdq.Query` object.
	#  - HOWEVER: The `data.pdq.Query` object has some interesting
	#             methods. It's worth a look sometime,
	#
	#
	def pdq(self, **k):
		"""
		Return a python data Query object given self.o and any kwargs.
	  
	  This is "terminal" because it terminates the chain of propx
    objects by returning a `data.pdq.Query` object.
		
		TERMINAL!
		This method does not return a propx object.
	   
	  SEE ALSO:
	  >>> from trix.data.pdq import *
		>>> help(Query)
		>>>
		 
		"""
		return trix.ncreate("data.pdq.Query", self.o, **k)
	
	
	#
	#
	# DISPLAY
	#
	# 
	def display(self, *a, **k):
		"""
		Display the current `self.o`.
		
		TERMINAL!
		This method does not return a propx object.
		
		EXAMPLE
		>>> import trix
		>>> trix.propx("['1', 'two']").parse().display()
		>>>
		
		"""
		trix.display(self.o)
	
	
	
	
	# -----------------------------------------------------------------
	#
	#
	#
	# NON-TERMINAL METHODS
	#  - This section's method results are wrapped in propx objects.
	#  - Methods that do not return a propx are called "terminal."
	#  - Methods that return a propx are "non-terminal."
	#
	#
	# -----------------------------------------------------------------


	#
	#
	# PARSE
	#
	#
	def parse(self, **k):
		"""
		Return propx containing the object parsed from json text. It may
		be a proplist, propdict, propstr, etc... depending on the content.
		
		EXAMPLES
		>>> import trix
		>>> trix.propx("['1', 'two']").parse().o
		['1', 'two']
		>>> trix.propx('["1", "two"]').parse().o
		['1', 'two']
		>>> trix.display(['1', 'two'])
		
		"""
		return propx(self.parser(**k).parse(self.o, **k))
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# FORMAT METHODS
	#  - These return a new propx object containing data from the caller
	#    that has been reformatted to the available formats.
	#  - See the `trix.fmt` modules for full details.
	#
	#
	# -----------------------------------------------------------------
	
	#
	#
	# FORMAT
	#
	#
	def format(self, *a, **k):
		"""
		Return a new propx object containing the data from `self.o` 
		formatted as specified by any given arguments and keyword 
		arguments. 
		
		The default is standard JSON text.
		
		To manipulate results, pass args and kwargs as specified by the
		`trix.format` classmethod's doc.
		
		
		EXAMPLES
		>>> import trix
		>>> x = trix.propx([1,2,3,4])
		>>> x.format(f='Table', width=2).o
		'1  2\n3  4'
		>>>
		>>> from trix.x.propx.proplist import *
		>>> x = proplist([1,2,3,4]).format(f="Table", w=2)
		>>> x.o
		'1  2\n3  4'
		>>>
		>>> from trix.x.propx import *
		>>> x = propx([1,2,3,4])
		>>> y = x.format(f="Table", width=2)
		'1  2\n3  4'
		>>>
		
		SEE ALSO:
		>>> from trix.fmt import *
		>>> help(Format)
		>>>
		
		"""
		k.setdefault('f', 'JSON')
		return propx(trix.formatter(*a, **k).format(self.o))
	
	
	#
	#
	# JSON
	#
	# 
	def json(self, **k):
		"""
		Return a propx object containing a copy of `self.o` converted
		to json text.
		
		This method ignores attempts to format in anything other than 
		json format.
		
		EXAMPLE 1
		>>> trix.propx([ [1, 2], [3, 4] ]).json(f="JCompact").o
		'[[1,2],[3,4]]'
		>>>
		
		EXAMPLE 2
		>>> trix.propx([ [1, 2], [3, 4] ]).json().o
		
		"""
		k['f'] = 'JSON'
		
		#
		# Remember, formatter returns an altered copy of `self.o`, but 
		# it is wrapped in a `propx` object, so this method is not
		# "terminal."
		#
		return self.format(**k) # format returns a new propx
	
	
	#
	#
	# JCOMPACT
	#
	# 
	def jcompact(self, **k):
		"""
		Return a propx object containing a copy of self.o forced to 
		jcompact text.
		
		EXAMPLE
		>>> trix.propx([ [1, 2], [3, 4] ]).format(f="JCompact").o
		
		"""
		k['f'] = 'JCompact'
		return self.format(**k) # format returns a new propx
	
	
	#
	#
	# JDISPLAY
	#
	# 
	def jdisplay(self, **k):
		"""
		Return a propx object containing a copy of self.o forced to 
		jcompact text.
		
		EXAMPLE
		>>> trix.propx([ [1, 2], [3, 4] ]).format(f="JCompact").o
		'[\n  [\n    1,\n    2\n  ],\n  [\n    3,\n    4\n  ]\n]'
		>>>
		>>> trix.propx([ [1, 2], [3, 4] ]).format(f="JDisplay").output()
		[
		  [
		    1,
		    2
		  ],
		  [
		    3,
		    4
		  ]
		]
		>>>
		
		"""
		k['f'] = 'JDisplay'
		
		#
		# Remember, formatter returns an altered copy of `self.o`, but 
		# it is wrapped in a `propx` object, so this method is not
		# "terminal."
		#
		return self.format(**k).format(self.o)
	
	
	#
	#
	# OUTPUT - Print Contents
	#
	#
	def output(self):
		"""
		The `output` method prints the object's contents, `self.o`.
		"""
		print (self.o)
	
	
	
	
	
	# -----------------------------------------------------------------
	#
	#
	# ENCODING , COMPRESSION
	#
	#
	# -----------------------------------------------------------------

	
	#
	#
	# COMPACT
	#
	#
	def compact(self, **k):
		"""
		Convert self.o to json, zlib-compress, and return base-64 bytes.
		Use trix.compenc.expandexpand to revert to json.
		
		```
		from trix import *
		propx.compact("Hello, World!")
		
		```
		"""
		try:
			r = self.compenc.compact(self.o)
		except:
			# if self.o is a list or something, better use a json string
			c = self.jcompact(**k).encode('utf8') # json must be utf8
			r = self.compenc.compact(c)
		
		return propx(r)
	
	
	#
	#
	# EXPAND
	#
	#
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
	# CAST
	#
	#
	def cast(self, T):
		"""
		Return a propx object given `self.o` cast as a different type.
		This might be used to cast an iterator as a list.
		"""
		return propx(T(self.o))
	
	
	#
	#
	# SPLITLINES - Bytes or Strings
	#
	#
	def splitlines(self, *a, **k):
		"""
		Alter this propx-based object's contents by splitting bytes or
		strings.
				
		"""
		o = self.o.splitlines(self.o, **k)
		return propx(o)
	
	
	#
	#
	#  PROP-STR
	#
	#
	def propstr(self):
		"""
		Returns a propstr object, converting the packaged data to its
		string representation.
		"""
		return trix.ncreate("util.propx.propstr.propstr", str(self.o))
	









#
#
#
# CONVENIENCE
#  - Easy access to subclasses defined in other modules within
#    this package.
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
		
		try:
			LIST = trix.ncreate("util.propx.proplist.proplist", o, *a, **k)
			ITEMS = LIST.o
			
			try:
				ILEN = len(ITEMS[0])
			except IndexError:
				return LIST
			
			
			#
			# [ [1,2], [3,4] ] # that's a grid
			# [ [1],   [2]   ] # also a grid
			# [ [1]          ] # still a grid
			# [ [12],  [3,4] ] # NOT a grid
			#
			for x in ITEMS:
				if len(x) != ILEN:
					# 
					# NOT A GRID!
					# 
					if ILEN > 1:
						return LIST
		
		except TypeError as ex:
			#print (ex)
			return trix.ncreate("util.propx.proplist.proplist", o, *a, **k)
		
		#
		# If list items' lengths are equal, return propgrid.
		#
		return trix.ncreate("util.propx.proplist.propgrid", o, *a, **k)
			
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

