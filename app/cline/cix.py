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
	 
	 * i  = When the -i flag is set, only one argument may be passed -
	        a JSON string processed by the `compenc.compact` method.
	        (Additional flags and kwargs are ok.)
	        
	        This flag is intended for special use by cline handlers
	        that need to receive a large data structure for processing
	        of some kind. Any cline handler that accepts this data
	        should document well the exact format required.
	        
	        ```
	        cargs = trix.formatter().compact({'greet':'Hello, World!'})
	        cline = 'python3 -m trix echo -i %s' % cargs.encode()
	        p = trix.popen(cline)
	        print (p.stdout.decode())
	        
	        ```
	"""
	
	def __init__(self):
		
		# set up the original args values
		cline.__init__(self)
		
		# if the -i flag is set, input is compact and must be expanded
		if "i" in self.flags:
			if len(self.args) > 1:
				raise ValueError("Flag -i allows only one argument.")
		
			cargs = trix.formatter().expand(self.args[0])    # <-- to json
			cargs = cargs.decode(DEF_ENCODE)
			cargs = trix.jparse(cargs) # convert to object
			self.args = [cargs]
	
		
	
	def display(self, value):
		"""
		JSON display, for returning json. This should be the default
		so we can see results nice and pretty in the terminal.
		
		Use the -cx flag combination when calling via popen, for slightly
		more compressed results (of potentially large return values) to 
		be expanded/used programatically via `popen.communicate()`. When
		-x is used, results must be expanded using `compenc.expand()`.
		"""
		jcompact = 'c' in self.flags
		xcompact = 'x' in self.flags
		
		if xcompact:
			
			c = trix.formatter(f="JCompact").format(value)
			x = trix.ncreate('util.compenc.compact', c)
			
			# output for any value that can
			try:
				print(x.decode(trix.DEF_ENCODE))
			except:
				print(x)
		
		elif jcompact:
			o = trix.formatter(f="JCompact").format(value)
			try:
				print(o.decode(trix.DEF_ENCODE))
			except:
				print(o)
				
		else:
			try:
				value.decode
				print(value.decode(trix.DEF_ENCODE))
			except:
				trix.display(value)
