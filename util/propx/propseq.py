#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


from .propiter import *


# -------------------------------------------------------------------
#
#
# PROP-LIST - Wrapping lists.
#
#
# -------------------------------------------------------------------

class propseq(propiter):
	"""
	Use this class to wrap objects that implement str, unicode, list, 
	tuple, bytearray, or buffer.
	"""
	
	def __repr__(self):
		try:
			return "<trix/%s %s len=%i>" % (
					self.T.__name__, self.To.__name__, len(self.o)
				) 
		except:
			return "<trix/%s %s>" % (
					self.T.__name__, self.To.__name__
				) 
		
	
	#
	#
	# GET ITEM
	#
	# Replace iter's weird getitem method with something appropriate
	# to sequence objects.
	#
	#
	def __getitem__(self, key):
		return type(self)(self.o[key])
	
	
	#
	#
	#  SET ITEM
	#
	#
	def __setitem__(self, key, v):
		self.o[key] = v
	
	
	#
	#
	#  LINES
	#
	#
	@property
	def lines(self):
		"""
		Generate string items (lines).
		"""
		for line in self.o:
			yield (str(line))
	
	
	#
	#
	#  PROP LIST
	#
	#
	@property
	def proplist(self):
		"""
		Return this object's sequence, self.o, as a list wrapped inside
		a `proplist` object.
		"""
		return trix.ncreate("util.propx.proplist.proplist", list(self.o))
	
	
	#
	#
	#  PROP GRID
	#
	#
	@property
	def propgrid(self):
		"""
		Return this object's sequence, self.o, as a list of lists wrapped
		inside a proplist object.
		"""
		ilen = len(self.o[0])
		for o in self.o:
			if len(o) != ilen:
				raise type(ex)(xdata(
					error='err-grid-fail', reason="not-a-grid",
					en="Grid rows must be of equal length."
				))
		
		return trix.ncreate('util.propx.proplist.propgrid', list(self.o))


