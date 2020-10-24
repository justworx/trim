#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..util.sock.sockcon import *


CONNECT_DEFAULT_TIMEOUT = 1.5
CONNECT_DEFAULT_WAITTIME = 0.2




class Connect(sockcon):
	"""
	A simple connection class with config and socket properties.
	
	EXAMPLE
	>>> from trix.net.connect import *
	>>> from trix.net.server import *
	>>> s=Server(9955).starts()
	>>> c=Connect(9955)
	>>> c.write("This will work!")
	15
	>>> c.read()
	'This will work!'
	>>> 

	"""
	
	def read(self, sz=None, **k):
		"""
		Read data from server.
		"""		
		 
		t_timeout  = k.get('timeout', CONNECT_DEFAULT_TIMEOUT)
		t_waittime = k.get('waittime', CONNECT_DEFAULT_WAITTIME)
		t_out_when = time.time() + t_timeout
		
		while True:
			
			rdata = sockwrap.read(self, sz, **k)
			if rdata:
				return rdata 
			
			# if timeout is exceeded, break, and an exception is raised.
			if time.time() > t_out_when:
				raise Exception("Connect:read-timeout", xdata(
						k=k, config=self.config, timeout_time=t_out_when,
						timeout_period=t_timeout, current_time=time.time()
					))
			else:
				time.sleep(t_waittime)
			
