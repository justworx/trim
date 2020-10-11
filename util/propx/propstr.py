#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .propseq import *


class propstr(propseq):
	"""
	Wrapping lots of cool features around text strings.
	"""
	
	@property
	def lines(self):
		"""
		Return a proplist object containing a list of the lines
		of text contained by this propstr object.
		
		EXAMPLE:
		>>> from trix.util.propx import *
		>>> px = propx("Hello, World!\nHow are you?\n")
		>>> px.lines.output()
		
		"""
		return trix.ncreate(
				"util.propx.proplist.proplist", self.o.splitlines()
			)
	
	
	def scan(self, **k):
		"""
		Return a data/Scanner object loaded with text `self.o`.
		
		>>> from trix.util.propx import *
		>>> px = propx("[1,2,3] means 'one, two, three'")
		>>> px.scan().splits()
		['[1,2,3]', 'means', "'one, two, three'"]
		>>>
		
		"""
		return trix.ncreate('data.scan.Scanner', self.o, **k)
	
	
	def pdq(self, *a, **k):
		"""
		Wrap a python data Query around this object's string.
		
		Returns the Query object.
		
		The pdq Query object is a bit outdated, but it can still be
		useful for exploring data, particularly value-separated text
		like csv or tab-separated values. It could be helpful in
		designing `trix.data.cursor.Cursor` callbacks.
		
		See: help(trix.data.pdq.Query)
		
		"""
		return trix.ncreate('data.pdq.Query', self.o, **k)
	
	
		
	#
	# needs a regex method
	#






