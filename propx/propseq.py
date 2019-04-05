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
	
	
	@property
	def sorted(self):
		"""
		Return a proplist with sorted content.
		"""
		return type(self)(sorted(self.o))
	
	@property
	def reversed(self):
		"""Return a proplist with reversed content."""
		return type(self)(list(reversed(self.o)))
	
	@property
	def lines(self):
		"""Generate string items (lines)."""
		for line in self.o:
			yield (str(line))
	
	
	"""
	#
	# This seems like it should be pretty easy, but I can't figure it
	# out. I guess we can't convert bytes to unicode... what? In some
	# particular situation that's occuring.............. # HERE...?
	#
	# WTH am i missing? For some reason 
	#
	def text(self, glue=None, **k):
		#
		# Join list items into lines of text. Pass optional `glue` value, 
		# the char(s) on which to join list items (Default: '').
		#
		
		try:
			g = glue or ''
			txt = g.join(self.o)
		except TypeError:
			try:
				g = glue or b''
				print ("<DEBUG>")
				print(".")
				print("self.o -> ", bytes(self.o))
				print(".")
				print("bytes(self.o) -> ", bytes(self.o))
				print(".")
				print ("type(self.o) ->", type(self.o))
				print(".")
				print ("type(self.o[0]) ->", type(self.o[0]))
				print ("self.o[0] ->", self.o[0])
				print(".")
				print ("</DEBUG>")
				txt = g.join(self.o)                   # <--- HERE
				txt = txt.decode(**k)
			except Exception as ex:
				raise type(ex)(xdata(g=g, o0=self.o[0], To0=type(self.o[0])))
		return trix.ncreate('propx.propstr', txt)
	"""
	
	@property
	def proplist(self):
		return trix.ncreate("propx.proplist.proplist", list(self.o))
	
	@property
	def propgrid(self):
		ilen = len(self.o[0])
		for o in self.o:
			if len(o) != ilen:
				raise type(ex)(xdata(
					error='err-grid-fail', reason="not-a-grid",
					english="Grid rows must be of equal length."
				))
		return trix.ncreate('propx.proplist.propgrid', self.o)

