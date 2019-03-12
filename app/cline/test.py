#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class test(cline):
	"""
	Tests until error is encountered. No error means no problems!
	
	NOTE: This test suite is incomplete!
	"""
	def __init__(self):
		cline.__init__(self)
		print ("\n#\n# Test Report:\n#")
		print ("# * UNDER CONSTRUCTION *")
		print ("# - Tests until error is encountered.")
		print ("#   No error means no problems!")
		print ("# - Note: This test suite is incomplete!\n#\n")
		
		
		if self.args:
			trix.nmodule('test.%s' % '.'.join(self.args))
		else:
			trix.nmodule('test.testall', **self.kwargs)
		
		print ("\n#\n# Test concluded with no errors.\n#")
		print ("# Note: This test suite is under construction!")
		print ("#       Untested features may still be buggy.\n#")
		


