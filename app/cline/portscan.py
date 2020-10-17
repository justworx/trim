#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


from .cix import *
import time


class portscan(cix):
	"""
	Scan local ports and displays results. 
	
	This command may take several seconds to complete.
	
	EXAMPLE
	$
	$ python3 -m trix portscan
	{
	  "active-ports": [
	    139,
	    445
	  ],
	  "scan-time:": 6.7197747230529785
	}	
	$
	
	"""
	
	def __init__(self):
		cix.__init__(self)
		
		t = time.time()
		n = trix.ncreate('util.network.Host')
		r = n.portscan() 
		self.display({
			'active-ports' : r,
			'scan-time:'   : time.time()-t
		})
