#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ..udata.charinfo import *
from ...util.stream.buffer import *


class Analyses(object):
	"""A group of analyses within a single Analysis."""
	
	def __init__(self):
		self.aa = {}

class Analysis(Analyses):
	"""A single analysis datum, and a grouping of analysis data."""
	
	def __init__(self):
		Analyses.__init__(self):
			self.a = None



