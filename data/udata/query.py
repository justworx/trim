#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..scan import *


def query(**k):
	"""
	Display tabulated query results.
	
	EXAMPLE:
	>>> from trix.data.udata import *
	>>> udata.query(
	...   blocks=['Basic Latin', "Gothic"], 
	...   where=lambda ci: ci.num != None
	... )

	BLOCK       ORD     CHAR BIDI BRACKET CAT NUM   NAME
	Basic Latin 0x30    '0'  EN   None    Nd  0.0   DIGIT ZERO
	Basic Latin 0x31    '1'  EN   None    Nd  1.0   DIGIT ONE
	Basic Latin 0x32    '2'  EN   None    Nd  2.0   DIGIT TWO
	Basic Latin 0x33    '3'  EN   None    Nd  3.0   DIGIT THREE
	Basic Latin 0x34    '4'  EN   None    Nd  4.0   DIGIT FOUR
	Basic Latin 0x35    '5'  EN   None    Nd  5.0   DIGIT FIVE
	Basic Latin 0x36    '6'  EN   None    Nd  6.0   DIGIT SIX
	Basic Latin 0x37    '7'  EN   None    Nd  7.0   DIGIT SEVEN
	Basic Latin 0x38    '8'  EN   None    Nd  8.0   DIGIT EIGHT
	Basic Latin 0x39    '9'  EN   None    Nd  9.0   DIGIT NINE
	Gothic      0x10341 '𐍁'  L    None    Nl  90.0  GOTHIC LETTER NINETY
	Gothic      0x1034A '𐍊'  L    None    Nl  900.0 GOTHIC LETTER NINE HUNDRED
	qtime: 0.176986
	>>>
	
	SEE ALSO:
	>>> from trix.data.udata import charinfo
	>>> help(charinfo)
	
	"""
	ScanQuery(**k).table(**k)




class ScanQuery(Scanner):
	"""
	Select unicode data properties.
	
	The `ScanQuery` class is the workhorse behind the `query` function,
	defined above.
	
	EXAMPLE
	>>> from trix.data.udata.query import *
	>>> sq = ScanQuery(blocks=['Basic Latin', "Gothic"],
	...                where=lambda ci: ci.num != None)
	>>> result = sq.format()
	
	# -----------------------------------------------------------------
	#
	#
	# DARN. This doesn't work right. It's not limiting the
	#       results to numbers. I can't see how it works
	#       for `query` but not for `format`.
	#
	#
	# -----------------------------------------------------------------
	
	"""
	
	# default fields to query
	Titles = 'block ord char bidi bracket cat num name'
	
	# default limit when block=='*'
	ALimit = 0x3399
	
	@classmethod
	def chargen(cls, **k):
		limit = k.get('limit') or 0
		blocks = udata.blocks()
		bnames = k.get('blocks') or udata.blocknames()
		
		#
		# CHECK LIMIT
		#  - Limit is a stop-gap measure to prohibit CJK (0x3400 and 
		#    beyond).
		#  - This makes it more practical to set the 'blocks' keyword
		#    argument default to '*'.
		#
		if (bnames=='*'):
			limit = limit or cls.ALimit
			bnames = udata.blocknames()
			#print (limit)
			
		# Loop through blocks...
		for block in bnames:
			rng = blocks[block]
			try:
				# yield all codepoints in the current block...
				for c in range(rng[0], rng[1]+1):
					yield (unichr(c))
				
				# ...check limit AFTER each block.
				if limit and (c >= limit):
					raise StopIteration()
			
			except ValueError:
				if c > 0x10FFFF:
					raise StopIteration()
				else:
					raise
	
	
	def __init__(self, **k):
		"""Pass text to query, or None (the contents of each block)."""
		text = k.get('text') or self.chargen(**k)
		Scanner.__init__(self, text)
	
	
	def query(self, **k):
		"""
		Pass keyword args to match. Eg., category='Po', etc...
		"""
		
		# select clause - a space-separated string listing titles
		titles = k.get('select', self.Titles).upper()
		
		# where clause - a lambda or other callable
		fn = k.get('where')
		
		tt = [] # title list
		rr = [] # result lists
		
		# titles are taken from the select clause, but all-caps
		rr.append(titles.split())
		
		# fallback in case of error before being set
		c = t = None
		
		titles = titles.lower().split()
		try:
			while True:
				if (self.cc and (not fn)) or fn(self.c):
					r = []
					
					for t in titles:
						#
						# TO DO:
						#  - There must be a better way to handle this...
						#    ...happening every time might make it slow :-/
						#
						c = self.c.c
						if t in ['char','c']:
							if (self.c.cat=='Mc'):
								x = "' " + str(c) + "'"
							else:
								x = repr(c)
							r.append(x)
						elif t == 'block':
							r.append(self.c.block)
						elif t in ['bidi', 'bidirectional']:
							r.append(self.c.bidirectional)
						elif t == 'bracket':
							r.append(self.c.bracket)
						elif t in ['cat', 'category']:
							r.append(self.c.category)
						elif t in ['decomp', 'decomposition']:
							r.append(self.c.decomposition)
						elif t in ['mirrored']:
							r.append(self.c.mirrored)
						
						elif t in ['num', 'numeric']:
							r.append(self.c.numeric)
						elif t in ['dec', 'decimal']:
							r.append(self.c.decimal)
						elif t in ['dig', 'digit']:
							r.append(self.c.digit)
						
						elif t == 'name':
							if self.c.name:
								r.append(self.c.name)
							else:
								r.append('')
						elif t in ['props', 'properties']:
							r.append(" ".join(self.c.props))
						
						elif t in ['br', 'linebreak']:
							r.append(self.c.br)
						elif t in ['brname']:
							r.append(self.c.brname)
						
						elif t == 'bidiname':
							r.append(self.c.bidiname)
						elif t == 'catname':
							r.append(self.c.catname)
						
						elif t == 'ord':
							r.append(self.c.ord)
						
						else:
							raise ValueError('err-unknown-property', xdata(
									prop=t
								))
					
					# add the row to results
					rr.append(r)
					
		except StopIteration:
			return rr
		
		except Exception:
			raise Exception(xdata(c=self.c.c, t=t))
	
	
	
	def format(self, **k):
		rr = self.query(**k)
		return trix.ncreate('fmt.Grid').format(rr)
	
	
	def table(self, **k):
		t = time.time()
		rr = self.query(**k)
		tt = time.time()-t
		hd = k.get('heading', '')
		if hd != None:
			print(hd)
		trix.ncreate('fmt.Grid').output(rr)
		print ('qtime: %f' % tt)


