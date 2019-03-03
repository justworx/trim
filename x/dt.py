#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *


class dt(object):
	"""
	Date/Time Utility.
	
	```python3
	
	from trix.x.dt import *
	dt().loc()
	dt().gmt()
	
	dt.sf("%Y-%m-%s")
	
	dt().gmt()
	
	dt().sf()                    # '2019-03-02'
	dt().sf("%Y-%m-%d %H:%M:%S") # '2019-03-02 22:35:32'
	dt().sf("%Y-%m-%d %H:%M:%S") # '2019-03-02 22:35:35'
	dt().sf("%Y-%m-%d %H:%M:%S") # '2019-03-02 22:35:38'
	
	d = trix.path()
	d.list.grid()
	
	#d.select(lambda p: p.setxx([2,3], lambda p,x: int(float(p.v[x])))
	
	```
	"""

	def __init__(self, dt=None):
		"""
		Pass `dt` as (float) seconds or timestruct. Default None sets
		this object's time to now().
		"""
		if dt:
			try:
				self.dt = float(dt)  # int/float
			except TypeError:
				self.dt = time.mktime(dt) # struct
		else:
			self.dt = time.time()
	
	@property
	def struct(self):
		"""Local time - struct."""
		return time.localtime(self.dt)
	
	@property
	def float(self):
		"""Local time - struct."""
		return time.localtime(self.dt)
		
	
	#
	# local time
	#
	def loc(self):
		"""Local time - struct."""
		return time.localtime(self.dt)
	
	def sf(self, fmt="%Y-%m-%d"):
		"""
		Pass strftime format string. Returns time struct for local time.
		"""
		return time.strftime(fmt, self.loc())
	
	#
	# gmt
	#
	def gmt(self):
		"""Return GMT time struct."""
		return time.gmtime(self.dt)
	
	def gsf(self, fmt="%Y-%m-%d"):
		"""Format GMT using strftime."""
		return time.strftime(fmt, self.gmt())
		
