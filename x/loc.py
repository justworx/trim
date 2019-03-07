#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import locale


class Locale(object):
	"""
	Stores value for formatting based on locale.
	"""
	
	def __init__(self, locale_info_dict):
		self.__dict = locale_info_dict
		
		fmt = self.__dict['format']
		self.__f_dt = fmt["datetime"]
		self.__f_d  = fmt["date"]
		self.__f_t  = fmt["time"]
		self.__fapm = fmt['ampm']
		self.__fera = fmt['era']
	
	
	# formats
	def datetime(self):
		return strftime(self.__f_dt)
	
	def date(self):
		return strftime(self.__f_dt)
	
	def time(self):
		return strftime(self.__f_dt)
	
	def ampm(self):
		return strftime(self.__f_dt)
	