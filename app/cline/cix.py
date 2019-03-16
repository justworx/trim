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
	 
	 * i  = Replace all arguments (and, optionally, kwargs) with a
	        compact json dict containing keys 'a' for an argument list
	        and 'k' for a keyword argument dict.
	        
	        When the -i flag is set, this compact json dict may be the
	        only argument. However, keyword args passed via the command
	        line will override any kwargs defined in the compact json
	        dict.
	        
	        ```
	        cargs = trix.formatter().compact({'a':'Hello, World!'})
	        trix.popen('python3 -m trix echo -i %s' % cargs)
	        
	        ```
	"""
	
	def __init__(self):
		
		cline.__init__(self)
		if "i" in self.flags:
			if len(self.args) > 1:
				raise ValueError("Mode -i; pass one compressed argument.")
		
			# cargs
			print ("cix.__init__ - self.args", self.args)
			cargs = trix.formatter().expand(self.args[0])    # <-- to json
			print ("cix.__init__ - cargs", cargs)
			
			cargs = cargs.decode(DEF_ENCODE)
			print ("cix.__init__ - cargs decoded", cargs)
			
			cargs = trix.jparse(cargs)# <-- encode
			print ("cix.__init__ - cargs jparsed", cargs)
		
			# args
			self.args = cargs.get('a') # reset self.args
		
			# kwargs given on command line override kwargs given in cargs
			krgs = cargs.get('k', {})
			for k in krgs:
				krgs[k] = self.kwargs[k]
		
			# reset self.kwargs
			self.kwargs = krgs
	
		
	
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
