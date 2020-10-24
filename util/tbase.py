#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .enchelp import *
from .tbase import *


class TBase(EncodingHelper):
	"""
	A useful base class that exposes a common interface for basic 
	needs, as well as methods that may be useful in the interpreter 
	and for debugging/development.
	"""
	
	def __init__(self, *a, **k):
		self.__a = a
		self.__k = k
	
	@property
	def a(self):
		"""For reference: Return any given args."""
		return self.__a
	
	@property
	def ax(self):
		"""
		For reference: Return any given args wrapped in propx().
		"""
		return trix.propx(self.__a)
	
	@property
	def k(self):
		"""
		For reference: Return any given keyword args.
		"""
		return self.__k
	
	@property
	def kx(self):
		"""
		For reference: Return any given keyword args wrapped in propx().
		"""
		return trix.propx(self.__k)
	
	@property
	def ekx(self):
		"""
		For reference: Return the contents of EncodingHelper data
		wrapped in a propx.
		"""
		return trix.propx(self.__k)
	
	@property
	def term(self, **k):
		"""Return a terminal."""
		return trix.ncreate('util.terminal.Terminal', **k)		
	
