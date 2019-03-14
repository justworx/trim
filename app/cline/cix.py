#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class cix(cline):
	"""
	Command-line plugin for subclasses that output text.
	
	FLAGS:
	 * c  = Pass flag -c to request that return values be presented in 
	        JCompact format - that is, with the minimum of whitespace 
	        in dict and list representations.
	 * x  = Flag -x indicates return values be presented (returned) in
	        `compenc.compact` format - that is, zlib-compressed in b64
	        encoding. See `trix.util.compenc.compact()` for details.
	        Use `trix.util.compenc.expand()` to retrieve the value.
	        NOTE: x will convert non-string values (dict, list, float,
	              etc.) to JSON before compacting.
	 * cx = Flag combination -cx combines the above, doing JCompact
	        first, then returning its result from compenc.compact. This
	        is the way to explicitly convert string values to JSON
	        before compacting and returning them. 
	 
	 * i  = Not yet implemented. Reserved for cix subclasses.
	"""
		
	
	def display(self, value):
		"""
		I think display should be used to display json only and plain
		text strings only. If it's some kind of compressed or otherwise-
		encoded string (Eg, from `b64.encode` or `compact`) it should 
		just be written as bytes,
		"""
		
		#print("\n # DBG: flags=%s\n" % ''.join(self.flags)), 
		
		jcompact = 'c' in self.flags
		xcompact = 'x' in self.flags
		
		if xcompact:
			
			c = trix.formatter(f="JCompact").format(value)
			x = trix.ncreate('util.compenc.compact', c)
			
			# output for any value that's 
			try:
				print(x.decode("UTF_8"))
			except:
				print(x)
		
		elif jcompact:
			o = trix.formatter(f="JCompact").format(value)
			try:
				print(o.decode('UTF_8'))
			except:
				print(o)
				
		else:
			try:
				value.decode
				print(value.decode('UTF_8'))
			except:
				trix.display(value)
