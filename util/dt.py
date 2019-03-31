#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *
from .loc import *


class dt(object):
	"""Date/Time utility."""

	def __init__(self, dt=None, loc=None):
		"""
		Date/Time formatting.
		
		Pass `dt` as (float) seconds or timestruct. Default None sets
		this object's time to now().
		
		Format strings default to locale-appropriate formats. Systems 
		that allow access to more than one locale may specify a locale
		string to access alternate format strings. (Does not work on 
		MS Windows systems.)
		"""
		if dt:
			try:
				self.__time = float(dt)  # int/float
			except TypeError:
				self.__struct = dt
				self.__time = time.mktime(dt) # struct
		else:
			self.__time = time.time()
		
		self.__locsig = loc
	
	
	@property
	def loc(self):
		"""A locale description for dt translation."""
		try:
			return self.__loc
		except:
			self.__loc = trix.loc(self.__locsig)
			return self.__loc
			
	
	@property
	def float(self):
		"""
		Time stored in this object, in float seconds (ala time.time()).
		"""
		return self.__time
	
	@property
	def struct(self):
		"""A DateTime struct created from this object's self.time."""
		try:
			return self.__struct
		except:
			self.__struct = time.localtime(self.__time)
			return self.__struct
	
	def format(self, fmt=None):
		"""Format using strftime."""
		return time.strftime(fmt, self.struct)
	
	def datetime(self, fmt=None):
		"""Format using locale-specific format string."""
		return self.format(fmt or self.loc.D_T_FMT)
	
	def date(self, fmt=None):
		"""Format using locale-specific format string. """
		return self.format(fmt or self.loc.D_FMT)
	
	def time(self, fmt=None):
		"""Format using locale-specific format string."""
		return self.format(fmt or self.loc.T_FMT)
	
	def ampm(self, fmt=None):
		"""
		Format using locale-specific format string. Returned time string
		will present with AM/PM specification for locales where that is
		possible, else with the 24-hour clock time for other locales.
		
		NOTE: As far as I can tell, `time` and `ampm` are exactly the
		      same. I'll leave them here in case there are situations I'm
		      unaware of in which the distinction is significant.
		"""
		if fmt:
			return self.format(fmt)
		else:
			return self.format(self.loc.T_FMT_AMPM) or self.time()


