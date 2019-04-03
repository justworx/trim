#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .loc import *
import datetime


class dt(object):
	"""Simple Date/Time utility."""

	def __init__(self, dt=None, loc=None, **k):
		"""
		Date/Time formatting.
		
		Pass `dt` as (float) seconds or timestruct. Default None sets
		this object's time to time.time().
		
		Format strings default to locale-appropriate formats. Systems 
		that allow access to more than one locale may specify a locale
		string to access alternate format strings. (Does not work on 
		MS Windows systems.)
		"""
		
		if dt:
			try:
				# if time is given as a float
				self.__time = float(dt)
			except TypeError:
				try:
					# maybe it's a time struct
					self.__time = time.mktime(dt)
				except:
					# or maybe a datetime object
					self.__time = dt.timestamp()
		
		else:
			# if time's not given, use `time.time()`
			self.__time = time.time()
		
		# store the locale signature; the default is the system locale.
		self.__locsig = loc or ".".join(trix.module("locale").getlocale())
	
	
	def loc(self):
		"""A locale description for dt translation."""
		try:
			return self.__loc
		except:
			self.__loc = trix.loc(self.__locsig)
			return self.__loc
			
	
	def time(self):
		"""Time stored in this object, in float seconds."""
		return self.__time
	
	
	def datetime(self):
		"""A datetime object created from this object's structtime."""
		st = self.structtime()
		dt = list(st)[:7]
		return datetime.datetime(*dt)
		
	
	def localtime(self):
		"""A struct_time struct created from this object's self.time."""
		try:
			return self.__struct
		except:
			self.__struct = time.localtime(self.__time)
			return self.__struct
	
	
	def gmtime(self):
		"""Return UTC time struct created from this object's self.time."""
		return time.gmtime(self.__time)
	
	
	def fdatetime(self):
		self.loc().datetime(self.localtime())
	

