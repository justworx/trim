
#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


from .cix import *


class compenc(cix):
	"""
	Compression/Encoding.
	
	Call `compact` or `expand` from the command line.
	
	EXAMPLE:
	$
	$ python3 -m trix compenc compact "Test! This is a test."
	"eJxTCkktLlFUCMnILFYAokSFEiBfTwkAV30HSQ=="
	$
	$ python3 -m trix compenc expand eJxTCkktLlFUCMnILFYAokSFEiBfTwkAV30HSQ==
	"Test! This is a test."
	$
	
	"""
	
	def __init__(self):
		cix.__init__(self)
		
		# get the fmt.JCompact object
		JCompact = trix.nvalue('fmt', 'JCompact')
		value = JCompact().format(self.args[1])
		
		# see if there's an encoding kwarg; DEFALT: DEF_ENCODE
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
		
		# boil the json string down to an object
		value = self.jparse(value)
		
		#
		# DISPLAY THE RESULT
		#
		self.display(value)



