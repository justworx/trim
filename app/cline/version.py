#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *

class version(cline):
	"""
	Print version information.
	"""
	def __init__(self):
		version = dict(
			version   = VERSION,
			copyright = COPYRIGHT,
			license   = 'agpl-3.0'
		)
		trix.display(version)
	
