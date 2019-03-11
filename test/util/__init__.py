#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *

#
#	TEST ALL
#  - Test all testable modules from `trix.util`.
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

report("Testable Util Modules: OK")


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
from . import urlinfo




#
# X-ITER
#  - Testing of this alone is very limited, as its implementation is
#    typically tied to whatever object it's covering.
#  - It will certainly be tested with data.scan and udata.query.
#
from ...util.xiter import *
ii = xiter([1,2])
assert (ii.next()==1)
# 
# try:
# 	next(ii)
# except NameError:
# 	# could be a version of python2 that doesn't support the next(ii)
# 	# calling convention... I'm not sure about this - I'll have to
#   # do some checking to see whether all python 2.7 versions support
#   # it.
# 

#
# -------- TEMPORARILY OR PERMANENTLY UN-TESTABLE --------
#
# The following can't really be tested, but should be loaded to make
# sure there are no compile errors.
#

#
# UTIL.LOGLET
#
from ...util import loglet

#
# UTIL.FORM
# - I can't think of a way to automatically test Form.
#
from ...util import form

#
# UTIL.NETWORK
# - I can't think of a way to automatically test this one, either.
#
from ...util import network

#
# UTIL.OPEN 
#  - This will be tested by the fs set of tests. The module itself
#    probably really isn't even necessary since the earliest possible
#    syntax is 2.7, where `io` is available.
#  - Need to consider getting rid of util.open.
#
from ...util import open

#
# SAK
#  - This one's more of a debug tool; something you'd have to eyeball
#    test, anyway.
#
from ...util import sak

#
# X-INPUT
#  - Due to its nature, this is not prone to automated testing.
#
from ...util import xinput

#
# X-INSPECT
#  - The testing of this will be part of the 'util.wrap' testing,
#    or vice-versa. Some testing of Wrap/Inspect functionality is
#    implicit in the util_runner test... it's incomplete, though.
#
from ...util import xinspect

#
# X-JSON
#  - Too generic and ubiquitous to be "stand-alone" tested.
#
from ...util import xjson

#
# X-QUEUE
#  - just a simple pair of import statement for py2/3 compatibility.
#
from ...util import xqueue


#
# ---------- TESTING OF UTIL.SOCK and UTIL.STREAM ----------
#
# The util.sock and util.stream modules are (or will soon be) used
# almost exclusively as support for implementation of a large set
# of classes. Their testing will be tied completely to the testing
# of those other classes.
#


report("Untestable util modules: Loaded.")


