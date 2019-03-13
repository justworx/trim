#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .cix import *


class echo(cix):
	"""
	Debug/Testing utility. Explore results with various flags.
	"""
	
	def __init__(self):
		"""
		Echo args as a string. Flag -d for display, otherwise write is
		used to echo the arguments.
		"""
		cix.__init__(self)
	
		try:
			a_out = " ".join(self.args)
		except:
			a_out = b" ".join(self.args)
		
		if 'd' in self.flags:
			self.display(a_out)
		else:
			self.write(a_out)
	
	
