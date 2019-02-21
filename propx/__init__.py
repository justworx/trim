#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .. import *

class propx(object):
	"""
	Wraps objects with a set of methods convenitent for manipulation,
	query, display, and compression.
	"""
	
	#
	# INIT
	#  - Pass value or callback `o`, plus args/kwargs needed for 
	#    callback.
	#
	def __init__(self, o=None, *a, **k):
		"""
		Pass object `o`, a value or callable that returns a value.
		
		In the case `o` is a callable, pass also any args/kwargs required
		to execute that callable. When `self.o` is first accessed, the
		value will be calculated and stored as self.o (even if it's the
		first calling of property `self.o`).
		"""
		self.p = o
		self.a = a
		self.k = k
	
	
	def __call__(self, *a, **k):
		"""
		On first call, sets the value for the `self.o` property. On
		subsequent calls, returns that value.
		
		The value of `self.o` is, on the first call to this method,
		undefined. If this object has been constructed given a callable
		as the first argument, it will be calculated here (given any
		additional constructor args/kwargs) and stored as a private
		member variable self.__o.
		
		On all calls, self.__o is returned.
		"""
		try:
			return self.__o
		except:
			try:
				# if self.p is callable...
				self.__o = self.p(*a, **k)
			except TypeError:
				# or, self.p must be an object/value
				self.__o = self.p
			
			return self.__o
	
	
	@property
	def o(self):
		"""
		Return this property's actual object value (as calculated
		by `self.__call__()`).
		"""
		try:
			return self.__o
		except:
			self.__o = self.__call__(*self.a, **self.k)
			return self.__o
	
	@property
	def compenc(self):
		"""Loads and returns the compenc module."""
		try:
			return self.__compenc
		except:
			self.__compenc = trix.nmodule("util.compenc")
			return self.__compenc
	
	#
	#
	# Methods that can handle pretty much any data type
	#
	#
	
	# DISPLAY
	def display(self, *a, **k):
		"""Display using trix.fmt; default: f='JDisplay'"""
		trix.display(self.o, *a, **k)
	
	
	# FORMATTING
	def json(self, *a, **k):
		"""
		Return self.o as json text. Default format is compact json. 
		Note: Use the `display()` method for JSON in display format. 
		"""
		k.setdefault('f', 'JCompact')
		return trix.formatter(*a, **k).format(self.o)
	
	
	#
	# CURSOR, PDQ
	#
	def cursor(self, **k):
		"""
		Return a cursor containing self.o; any given keyword arguments
		are passed to the cursor's constructor.
		"""
		return trix.ncreate("data.cursor.Cursor", self.o, **k)
	
	def pdq(self, **k):
		"""
		Return a python data Query object given self.o and any kwargs.
		"""
		return trix.ncreate("data.pdq.Query", self.o, **k)
	



#
# STRING or BYTES
#
class propseq(propx):

	#
	# ENCODING / COMPRESSION
	#
	def b64(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base64."""
		return self.compenc.b64.encode(self.json(**k).encode(**k))
	
	def b64s(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base64."""
		return self.compenc.b64.sencode(self.json(**k).encode('utf8'))
	
	def b64u(self, **k):
		"""
		Return self.o as (compact) JSON bytes encoded to url-safe base64.
		"""
		return self.compenc.b64.uencode(self.json(**k).encode('utf8'))
	
	def b32(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base32."""
		return self.compenc.b32.encode(self.json(**k).encode(**k))
	
	def b16(self, **k):
		"""Return self.o as (compact) JSON bytes encoded to base16."""
		return self.compenc.b16.encode(self.json(**k).encode(**k))
	
	def compact(self, **k):
		"""
		Convert self.o to json, zlib-compress, and return base-64 bytes.
		Use trix.compenc.expand to revert to json.
		"""
		return self.compenc.compact(self.json(**k).encode('utf8'))
	





#
#
# PROP-LIST
#
#
class proplist(propx):
	"""
	Wrap objects in a proplist to provide a variety of useful features
	for manipulation and display.
	"""
	
	def __getitem__(self, key):
		return self.o[key]
	
	
	@property
	def sorted(self):
		"""Return a proplist with sorted content."""
		return type(self)(sorted(self.o))
	
	@property
	def reversed(self):
		"""Return a proplist with reversed content."""
		return type(self)(reversed(self.o))
	
	@property
	def lines(self):
		"""Generate string items (lines)."""
		for line in self.o:
			yield (str(line))
	
	
	#def datagrid(self):
	#	"""Return a DataGrid object loaded with self.o."""
	#	return trix.ncreate('data.datagrid.DataGrid', self.o)
	
	
	def each(self, fn, *a, **k):
		"""
		For each item in self.o execute callable `fn` given the item
		and any specified args/kwargs.
		"""
		for item in self.o:
			fn(item, *a, **k)
	
	
	def filter(self, fn, *a, **k):
		"""
		Pass callable `fn` that returns False for items that should not
		be selected. Optional args/kwargs are received by fn.
		
		Returns filter object.
		"""
		return filter(fn, self.o, *a, **k)
	
	
	def filtered(self, fn, *a, **k):
		"""
		Return a proplist containing results filtered by function `fn`.
		
		Eg.
		d = trix.path('~').dir()
		d.list.filtered(lambda x: x[1]=='f').o
		"""
		return proplist(list(self.filter(fn,*a,**k)))
	
	
	def text(self, glue=None):
		"""
		Join list items into lines of text. Pass optional `glue` value, 
		the char(s) on which to join list items (Default: '').
		"""
		try:
			g = glue or ''
			return g.join(self.o)
		except TypeError:
			g = glue or b''
			return g.join(self.o)
	
	
	#
	# DISPLAY
	#  - Display lists as json or in grids/tables/lists
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



