
#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .cix import *


class compenc(cix):
	"""
	Compression/Encoding.
	
	$ python3 -m trix compenc compact Test! This is a test.
	
	"""
	
	def __init__(self):
		cix.__init__(self)
		
		# get the fmt.JCompact object
		JCompact = trix.nvalue('fmt', 'JCompact')
		value = JCompact().format(self.args[1])
		
		# see if there's an encoding kwarg
		kk = self.kwargs
		self.encoding = kk.get('encoding', kk.get('e', DEF_ENCODE))
		
		#
		# GET FUNCTION/METHOD
		#  - Use class.method or fn, as specified in command line...
		#    Eg., "compact", "b64.encode", etc...
		#
		xm = self.args[0].split('.')
		if len(xm) == 2:
			#
			# xm is "class.method", so split them up. Eg, if argument was
			# "b16.decode", split it into the "object-dot-method" string
			# and .append it to "util.compenc" and you get the full path,
			# "util.compenc.b16.encode", to create the method `fn`.
			#
			c, m = xm
			s = "util.compenc.%s" % c
			fn = trix.nvalue(s, m)
		
		else:
			#
			# xm is a function name - one item ("compact" or "expand"),
			# so just call nvalue the easy way without all the stirng
			# manipulation. 
			#
			fn = trix.nvalue("util.compenc", xm[0])

		
		try:
			value = fn(value)
		except TypeError as ex:
			value = value.encode(encoding=self.encoding)
			value = fn(value)
		
		
		#
		# DECODE
		#  - display as text, not b'text'
		#  - I guess we always want to decode from ascii since it'll be 
		#    ascii characters returned by the compenc functions, right?
		#    I mean... these are asci characters A-Z plus some others 
		#    that are also ascii - here we're just making sure they are
		#    not displayed with a "b'" in front of them.
		#  - So use ascii, actually, I guess. Yes.
		#
		try:
			value = value.decode('ascii') # changed from utf_8 to ascii
		except:
			pass
		
		try:
			# This gets rid of some extra slashes. This is kind of a hack,
			# but I'm not too sure how else to do it.
			while True:
				value = trix.jparse(value)
		except:
			pass
		
		#
		# DISPLAY THE RESULT
		#
		self.display(value)







"""
	def COMING_SOON(self):
		#~ I can't make this work right now. Can't even think of a name 
		#~ for the method!
		
		#~ I'll try to get to it soon! (Sooner or later.)
		
		
		# make sure arg is encoded to bytes
		arg = self.args[0]
		try:
			arg = arg.encode(enc)
		except:
			pass
		
		# encode
		if 'e' in self.flags:
			print ('base64: %s' % b64.encode(arg).decode(enc))
			print ('base32: %s' % b32.encode(arg).decode(enc))
			print ('base16: %s' % b16.encode(arg).decode(enc))
			print ('hex   : %s' % hex.encode(arg).decode(enc))
			print ('zlib  : %s' % zlib.encode(arg))
			print ('bz2   : %s' % bz2.encode(arg))
		
		# decode
		else:
			i=0
			try:
				print ('base64: %s' % b64.decode(arg).decode(enc))
				i += 1
			except:
				pass
			
			try:
				print ('base32: %s' % b32.decode(arg).decode(enc))
				i += 1
			except:
				pass
			
			try:
				print ('base16: %s' % b16.decode(arg).decode(enc))
				i += 1
			except:
				pass
			
			try:
				print ('hex   : %s' % hex.decode(arg).decode(enc))
				i += 1
			except:
				pass
			
			
			# I don't know what to do with these...
			try:
				print ('zlib: %s' % zlib.decode(arg))
				i += 1
			except:
				pass
			
			try:
				print ('bz2: %s' % bz2.decode(arg).decode(enc))
				i += 1
			except:
				pass
			
			
			#
			if not i:
				print ("No results.")
"""
		
