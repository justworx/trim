#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
from ....util.wrap import *


class scanner_extention(Wrap):
	"""Scanner extention base class."""

	def __init__(self, scanner_object):
		"""
		Pass a Scanner object.
		
		Adds this extention as a method to Scanner objects. Gives this
		extention access to all (non-private) Scanner properties and 
		methods.
		"""
		Wrap.__init__(self, scanner_object)
	

