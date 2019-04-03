#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...data.udata.charinfo import *
from ...util.stream.buffer import *
from ...util.wrap import *


class Scanner(object):
	"""
	Try something new with scanner.
	"""
	
	Escape = "\\"
	BufSize = 2048
	
	def __init__(self, iterable_text, **k):
		"""Pass anything iterable that produces unicode characters."""
		self.__k = k
		self.__escape = k.get('escape', self.Escape)
		self.__bufsz = k.get('bufsz', self.BufSize)
		self.__itext = iter(iterable_text)
		
		# flag set to True on StopIteration
		self.__eof = False
	
	
	# CHARACTERS
	@property
	def c(self):
		"""Return current character info object."""
		if self.eof:
			raise StopIteration()
		try:
			return self.__cinfo
		except AttributeError:
			return ''
	
	@property
	def cc(self):
		"""Move forward one and return the character info object."""
		try:
			return self.__cinfo.next()
		except AttributeError:
			self.__cinfo = charinfo(self.__itext)
			return self.__cinfo.next()
		except StopIteration:
			self.__eof = True
	
	@property
	def char(self):
		"""Return the current character."""
		return self.c.c
	
	
	# STATUS
	@property
	def eof(self):
		"""False until end of text is reached."""
		return self.__eof
	
	
	# CONFIG PROPERTIES
	@property
	def bufsz(self):
		"""
		The size of a buffer used to scan text. The default is 2048, but
		scans will not fail if that is exceeded (though they may be a 
		bit slower). If you expect larger scan chunks, it may improve
		performance if you specify a larger buffer size integer via the
		bufsz keyword argument. (I haven't tested this - it may be just
		the same or worse.)
		"""
		return self.__bufsz
	
	@property
	def escape(self):
		"""The escape character. Default: '\' (backslash)."""
		return self.__escape
	
	#
	# COLLECT
	#
	def collect(self, fn):
		"""
		Collect each character that matches the criteria of `fn`. The 
		pointer is left directly after the last matching character.
		
		>>> s = Scanner("Abc 123")
		>>> s.char                          # 'A'
		>>> s.collect(lambda ci: ci.alpha)  # 'Abc'
		>>> s.char                          # ' '
		>>> s.cc                            # '1'
		>>> s.collect(lambda ci: ci.numeric)# '123'
		
		"""
		if self.eof:
			raise StopIteration()
		
		b = Buffer(mode='r', max_size=self.__bufsz)
		w = b.writer()
		try:
			while fn(self.c):
				if self.c.c != self.__escape:
					w.write(self.c.c)
				else:
					w.write(self.cc.c) # it IS an escape char; get next char.
				self.cc
		except StopIteration:
			self.__eof = True
		
		# read/return the whole buffer
		return b.read()
	
	
	#
	# IGNORE
	#
	def ignore(self, fn):
		"""
		Pass all characters for which executable `fn` returns True. The
		iterator stops on the first character following ignored text.
		
		NOTE: If the current character doesn't match what `fn` is looking
		      for, the pointer is not moved.
		"""
		
		# Calling self.c will raise StopIteration if self.eof is set.
		a = fn(self.c)
		try:
			while a:
				a = fn(self.cc)
		except StopIteration:
			self.__eof = True
	
	
	
	#
	# DEV
	#
	@classmethod
	def _load_scanner(self, scanner_name):
		inner_path = 'x.xscan.%s' % scanner_name
		return trix.ncreate(inner_path, self)
