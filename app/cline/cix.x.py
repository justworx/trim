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
	 * cx = Flag combination -cx combines the above.
	 * i  = Flag -i indicates that input should be expected a compact
	        format. Use `trix.fmt.compact()` to pack all arguments into
	        a compacted json list. (There must be exactly one argument
	        when using the -i flag.) This list will be automatically 
	        expanded by the cix-based ojbect and used to perform its
	        task. Flag -i will be useful when large amounts of data
	        must be sent to a cix-based object for processing.
	        
	        NOTE: I probably need to figure out how to use stdin for
	              this rather than sending huge compacted strings via
	              the command line. 
	              
	              Put that on the TODO list.
	
	Finally, -cix indicates all of the above: The input must be given
	in compact format - again, that's `trix.util.compenc.compact()` -
	and output will be returned (printed) in compact format as well, so
	must be "expanded" using `trix.util.compenc.expand()`.
	"""
	
	"""
	def __init__(self):
		cline.__init__(self)
		if 'i' in self.flags:
			#
			# Can't seem to make this work, and I'm not even sure it's
			# a good idea, anyway.
			#
			print ("TESTING", self.args)
			print (trix.ncreate('util.compenc.expand', self.args[0]))
			print (".\n")
			
			EH = trix.nvalue('util.enchelp.EncodingHelper')
			arg0 = EH(encoding="utf8").encode(self.args[0])
			self.args[0] = trix.ncreate('util.compenc.expand', arg0)
			
			EH = trix.nvalue('util.enchelp.EncodingHelper')
			args = EH(encoding="utf8").encode(self.args[0])
			self.args[0]=trix.ncreate('fmt.Format').expand(args)
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
