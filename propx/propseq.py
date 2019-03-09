#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .propiter import *

#
# PROP-SEQ
#  - NOTE: be sure to check whether xrange should be wrapped with
#          propseq, propset, or propiter.
#
class propseq(propiter):
	"""
	Use this class to wrap objects that implement str, unicode, list, 
	tuple, bytearray, or buffer.
	"""
	
	def __getitem__(self, key):
		return type(self)(self.o[key])
	
	def __setitem__(self, key, v):
		self.o[key] = v
	
	#
	# EACH / SELECT
	#  - Use/selection of `self.o` data
	#
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
		Argument `fn` is a callable that selects/alters items one at
		a time.
		
		Returns an object of this type with the new dataset as `self.o`.
		
		```
		from trix.propx import *
		pl = proplist([1,2,3])
		pl.select(lambda o: o*9).o
		```
		"""
		r = []
		for v in self.o:
			r.append(fn(v, *a, **k))
		return self.T(r)

	
	
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
			return propstr(g.join(self.o))
	
	
	def proplist(self):
		return proplist(list(self.o))
	
	
	def propgrid(self):
		return propgrid(self.o)
		# try:
			# l = len(self.o[0])
			# self.each(lambda x: assert(len(x)==l)) # <-- windows blows up
			# return propgrid(self.o)
		# except BaseException as ex:
			# raise type(ex)(xdata(error='err-grid-fail', reason="not-a-grid"
					# english="Grid rows must be of equal lenght."
				# ))
