#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .cix import *


class echo(cix):
	"""
	Debug/Testing utility. Explore results with various flags.
	
	Echo args as a string. Flag -d for display, otherwise write is
	used to echo the arguments.
	
	```
	python3 -m trix echo '"Hello, World!"'
	```
	
	Echo can accept one keyword argument, "format", which must be the
	name of a class based on fmt.Format - usually JCompact, JSON, or
	JDisplay. Any kwargs that apply to such objects may also be passed
	as keyword arguments.
	
	"""
	
	def __init__(self):
		cix.__init__(self)
		
		#print (self.args)
		#print (self.kwargs)
		
		if 'd' in self.flags:
			trix.display(self.args, **self.kwargs)
		else:
			self.write(self.args)
		
		# maybe show the kwargs, too
		if 'k' in self.flags:
			print("KWARGS:")
			self.display(self.kwargs)
		
		"""
		try:
			a_out = " ".join(self.args)
		except:
			try:
				a_out = b" ".join(self.args)
			except Exception as ex:
				#print ("self.args:", self.args)
				raise type(ex)(xdata(args=self.args, kwargs=self.kwargs))
		
		if 'd' in self.flags:
			self.display(a_out)
		else:
			self.write(a_out)
		"""
	
