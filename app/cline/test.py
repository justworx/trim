#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from . import *


class test(cline):
	"""
	Tests until error is encountered. No error means no problems!
	
	This command calls on the `trix.test` package, in which many of the
	trix package classes and methods apply at least cursory levels of
	testing.
	
	EXAMPLE
	$
	$ python3 -m trix test
	
	#
	# Test Report:
	#
	# * UNDER CONSTRUCTION *
	# - Tests until error is encountered.
	#   No error means no problems!
	# - Note: This test suite is incomplete!
	#
	
	*
	* TESTING: Module: `trix`
	* --> OK
	*
	
	*
	* TESTING: Package: `util`
	  * Testable Util Modules: OK
	  * Untestable util modules: Loaded.
	* --> OK
	*
	
	*
	* TESTING: Package: `fmt`
	  * Format: OK
	  * JSON suite: OK
	  * List/Grid/Table: OK
	  * fmt package: OK
	* --> OK
	*
	
	*
	* TESTING: Package: `propx`
	* --> OK
	*
	
	*
	* TESTING: Package: `fs`
	* --> OK
	*
	
	*
	* TESTING: Package: `data`
	  * database: OK
	* --> OK
	*
	
	*
	* TESTING: Package: `net`
	* --> OK
	*
	
	*
	* TESTING: Package: `app`
	* --> OK
	*
	
	#
	# Test concluded with no errors.
	#
	# Note: This test suite is under construction!
	#       Untested features may still be buggy.
	#
	$
	
	
	NOTE: This test suite far from complete! Additional tests will be 
	      added as time permits. There's still a long way to go before
	      comprehensive test results can gathered.
	
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
		


