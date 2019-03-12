#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from .. import *  # trix


TEST_DIR = "%s/test" % DEF_CACHE


class test(object):
	def path(testpath=None):
		p = trix.path(TEST_DIR)
		return p(testpath) if testpath else p

# test file path
def testpath(testpath):
	#For creation of files within a test directory.
	return trix.path(TEST_DIR)(testpath).path


def banner(text):
	"""Pass text to display in a banner"""
	print("*\n* TESTING: %s" % text)

def report(text):
	"""Report success within a test module."""
	print ("  * %s" % text)

def footer():
	"""Report end of module testing."""
	print("* --> OK\n*\n")

