#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .enchelp import *
from .tbase import *


class TBase(EncodingHelper):
	"""
	EXPERIMENTAL
	
	A useful base class that exposes a common interface for basic 
	needs, as well as methods that may be useful in the interpreter 
	and for debugging/development.
	
	...Or, at least, that's what I'm hoping for.
	
	"""
	
	def __init__(self, *a, **k):
		
		k.setdefault('encoding', DEF_ENCODE)
		k.setdefault('errors', DEF_ERRORS)
		
		self.__a = a
		self.__k = k
		
		EncodingHelper.__init__(self, *a, **k)
	
	
	@property
	def a(self):
		"""
		Returns arguments given to the `TBase` constructor, wrapped in a 
		proplist.
		
		If you call this property as a method it returns the original
		arguments as a list.
		
		"""
		return trix.propx(list(self.__a))
	
	
	@property
	def k(self):
		"""
		Returns keyword arguments given to the TBase constructor, wrapped
		in a proplist.
		
		If you call this property as a method, it returns the original
		arguments as a list.
		
		For reference: Return any given keyword args.
		"""
		return trix.propx(self.__k)
	
	
	@property
	def ee(self):
		"""
		For reference: Return the contents of EncodingHelper data
		wrapped in a propx.
		"""
		return trix.propx(self.ek)
	
	
	@property
	def term(self, **k):
		"""
		Return the terminal object.
		"""
		try:
			return self.__term
		except:
			self.__term = trix.ncreate('util.terminal.Terminal', **k)
			return self.__term	
	
