#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#



from .. import *


class TX (object):
	
	def term(self):
		"""Returns the `util.terminal.Terminal` object."""
		try:
			return self.__term
		except:
			self.__term = trix.ncreate('util.terminal.Terminal')
			return self.__term

	def con(self):
		"""Opens the console."""
		try:
			self.__console.console()
		except:
			self.__console = trix.ncreate('util.console.Console')
			self.__console.console()
		return None

	def conf(self):
		"""Returns a Dir object to the config directory."""
		return trix.path(DEF_CONFIG)

	def cache(self):
		"""Returns a Dir object to the cache directory."""
		return trix.path(DEF_CACHE)

