#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class cix(cline):
	"""
	Command-line plugin for subclasses that return text.
	
	FLAGS:
	 * c  = Pass flag -c to request that return values be presented in 
	        JCompact format - that is, with the minimum of whitespace 
	        in dict and list representations.
	 * x  = Flag -x indicates return values be presented (returned) in
	        `compenc.compact` format - that is, zlib-compressed in b64
	        encoding. See `trix.util.compenc.compact()` for details.
	        Use `trix.util.compenc.expand()` to retrieve the value.
	 * cx = Flag combination -cx combines the above, doing JCompact
	        first, then returning its result from compenc.compact. 
	 
	 * i  = Not yet implemented. Reserved for cix subclasses.
	"""
		
	
	def display(self, value):
		
		#print("\n # DBG: flags=%s\n" % ''.join(self.flags)), 
		
		jcompact = 'c' in self.flags
		xcompact = 'x' in self.flags
		
		if jcompact and xcompact:
			#print ("display: cx")
			c = trix.formatter(f="JCompact").format(value)
			#print ("c", c)
			x = trix.ncreate('util.compenc.compact', c)
			#print ("x", x)
			trix.display(x)
		
		elif jcompact:
			#print ("display: c")
			# if c flag is set, use JCompact on display data
			print(trix.formatter(f="JCompact").format(value))
	
		elif xcompact:
			#print ("display: x")
			# if x flag is set, compact the result using compenc.compact
			print(trix.ncreate('util.compenc.compact', value))
		
		else:
			#print ("display: None")
			# otherwise, just display as-is 
			cline.display(self, value)
