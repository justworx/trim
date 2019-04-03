#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *


class split_escape(object):
	
	def __call__(self, char="%"):
		"""
		Return a list of escape characters + the following char, with
		any unescaped segments split by spaces.
		
		Default `char` is "%s".
		
		```
		s = Scanner()
		s.split_escape("%m/%d/%y") --> ["%m", "/", "%d", "/", "%y"]
		
		```
		"""
		
		r = []
		try:
			
			# These are the characters we're looking for - escape sequences.
			xchars = '%s '%char
			
			# Loop through the text...
			while True:
				
				# collect anything that comes before the first escape sequence
				r.append(self.collect(lambda ci: ci.c not in xchars))
				
				# parse the (two-character) escape sequence
				if self.char == char:
					
					# we know the first part is % (or whatever char is)
					cchar = self.cc.c
					
					# now we need to make sure the next char isn't ' ' space
					if cchar.strip():
						# if it's not, add it to the return list as %<x>
						r.append("%s%s" % (char, cchar))
						self.cc
					
					else:
						# what to do if percent is followed by whitespace?
						r.append("%") # just use %, i guess.
						r.append(cchar)
				
				elif self.c.white:
					r.append(self.collect(lambda ci: ci.white))
				
				else:
					r.append(self.collect(lambda ci: ci.c not in xchars))
			
		except StopIteration:
			self.__eof = True
		return r

