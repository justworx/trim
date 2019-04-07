#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import platform, os


class xplat(object):
	"""
	Methods for cross-platform compatability.
	"""
	def __init__(self):
		self.__sys = platform.system()
		if self.__sys == "Windows":
			self.__xplat = xplat_windows()
		else:
			self.__xplat = xplat_linux()
	
	def clear_screen(self):
		"""Clear terminal screen."""
		self.__xplat.clear_screen()



class xplat_linux(object):
	def clear_screen(self):
		os.system("clear")
	
class xplat_windows(object):
	def clear_screen(self):
		os.system("cls")


