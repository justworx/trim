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
	
	def __repr__(self):
		return "<trix/%s %s len=%i>" % (
				self.T.__name__, self.To.__name__, len(self.o)
			) 
	
	
	# Replace iter's weird getitem method with something appropriate
	# to sequence objects.
	def __getitem__(self, key):
		return type(self)(self.o[key])
	
	def __setitem__(self, key, v):
		self.o[key] = v
	
	
	# propiter does this
	# ~ @property
	# ~ def sorted(self):
		# ~ """
		# ~ Return a proplist with sorted content.
		# ~ """
		# ~ return type(self)(sorted(self.o))
	
	# ~ @property
	# ~ def reversed(self):
		# ~ """Return a proplist with reversed content."""
		# ~ return type(self)(list(reversed(self.o)))
	
	@property
	def lines(self):
		"""Generate string items (lines)."""
		for line in self.o:
			yield (str(line))
	
	@property
	def proplist(self):
		return trix.ncreate("util.propx.proplist.proplist", list(self.o))
	
	@property
	def propgrid(self):
		ilen = len(self.o[0])
		for o in self.o:
			if len(o) != ilen:
				raise type(ex)(xdata(
					error='err-grid-fail', reason="not-a-grid",
					english="Grid rows must be of equal length."
				))
		return trix.ncreate('util.propx.proplist.propgrid', self.o)

