#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .cix import *
import time


class portscan(cix):
	"""Scan local ports. This may take several seconds."""
	
	def __init__(self):
		cix.__init__(self)
		
		t = time.time()
		n = trix.ncreate('util.network.Host')
		r = n.portscan() 
		self.display({
			'active-ports' : r,
			'scan-time:'   : time.time()-t
		})
