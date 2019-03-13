#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *
#from ...fmt import *


class compenc(cline):
	"""
	Compression/Encoding.
	
	$ python3 -m trix compenc compact Test! This is a test.
	"""
	
	def __init__(self):
		cline.__init__(self)
		
		JCompact = trix.nvalue('fmt', 'JCompact')
		value = JCompact().format(self.args[1])
		
		kk = self.kwargs
		self.encoding = kk.get('encoding', kk.get('e', DEF_ENCODE))
		
		# class.method or fn
		xm = self.args[0].split('.')
		if len(xm) == 2:
			# xm is a class.method - split them up
			c, m = xm
			s = "util.compenc.%s" % c
			fn = trix.nvalue(s, m)
		else:
			# xm is a function name - one item
			fn = trix.nvalue("util.compenc", xm[0])
		
		try:
			# i'm assuming this will always be bytes
			value = fn(value)
		except TypeError:
			# but if not...
			value = value.encode(encoding=self.encoding)
			value = fn(value)
	
		#
		# I guess we always want to decode to utf_8 since it'll be ascii
		# characters returned by the compenc functions... right?
		#
		# Need to think about this I guess. Sleepy now.
		#
		
		# display as text, not b'text'
		try:
			value = value.decode('UTF_8')
		except:
			pass
		
		self.write(value)
		
	
	def COMING_SOON(self):
		"""
		I can't make this work right now. Can't even think of a name 
		for the method!
		
		I'll try to get to it soon! (Sooner or later.)
		"""
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
			"""
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
			"""
			
			
			#
			if not i:
				print ("No results.")
		
