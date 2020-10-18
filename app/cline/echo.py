#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .cix import *


class echo(cix):
	"""
	Debug/Testing utility. Echos given arguments, by default as JSON.
	
	Echo can accept one keyword argument, "format", which must be the
	name of a class based on fmt.Format - usually JCompact, JSON, or
	JDisplay. Any kwargs that apply to such objects may also be passed
	as keyword arguments.
	
	```
	python3 -m trix echo '"Hello, World!"'
	python3 -m trix echo '{"a":1, "b":9, "c":4}'
	
	```
	
	"""
	
	def __init__(self):
		cix.__init__(self)
		args = []
		try:
			for a in self.args:
				args.append(trix.jparse(a))
		except:
			args = self.args	
		trix.display(args)



