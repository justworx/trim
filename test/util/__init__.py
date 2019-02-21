#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


#
#	TEST ALL
#  - Test all available modules from each of the trix
#    subpackages.
#

#
# load the test.enchelp module, which tests trix.util.enchelp
#
from . import bag
from . import bom
from . import compenc
from . import convert
from . import dq
from . import enchelp
from . import encoded


#
# Skipping testing of form, jenc, linedbg,
# but loading them to make sure they'll compile.
#
from ...util import form, jenc, linedbg

#
# back to actual tests...
#
from . import lineq
from . import matheval
from . import mime
from . import runner



#
# END TEST
#
print("* Module `trix.util` : OK")




#
# NOTES:
#
"""
#
#
# -------- TEMPORARILY OR PERMANENTLY UN-TESTABLE --------
#
#

#
# UTIL.LOGLET
#
from . import loglet

#
# UTIL.FORM
# - I can't think of a way to automatically test Form.
#
from . import form

#
# UTIL.NETWORK
# - I can't think of a way to automatically test this one, either.
#

#
# UTIL.OPEN 
#  - This will be tested by the fs set of tests. The module itself
#    probably really isn't even necessary since the earliest possible
#    syntax is 2.7, where `io` is available.
#  - Need to consider getting rid of util.open.
#

#
# SAK
#  - This one's more of a debug tool; something you'd have to eyeball
#    test, anyway.
#

#
# X-INPUT
#  - Due to its nature, this is not prone to automated testing.
#

#
# X-INSPECT
#  - The testing of this will be part of the 'util.wrap' testing,
#    or vice-versa. Some testing of Wrap/Inspect functionality is
#    implicit in the util_runner test... it's incomplete, though.
#

#
# X-ITER
#  - Testing of this alone is impossible as its implementation is
#    tied to whatever object it's covering.
#  - It will certainly be tested with data.scan and udata.query.
#

#
# X-JSON
#  - Too generic and ubiquitous to be "stand-alone" tested.
#

#
# X-QUEUE
#  - just a simple pair of import statement for py2/3 compatibility.
#


#
# ---------- TESTING OF UTIL.SOCK and UTIL.STREAM ----------
#
# The util.sock and util.stream modules are (or will soon be) used
# almost exclusively as support for implementation of a large set
# of classes. Their testing will be tied completely to the testing
# of those other classes.
#


"""

