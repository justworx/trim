#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


# -------------------------------------------------------------------
#
# TRIX -> test trix class methods
#
# -------------------------------------------------------------------

# import trix
from .. import *


# Test nmodule() [ + module(), innerpath() ] 
test = trix.nmodule('util.enchelp')

match = "<module 'trix.util.enchelp'"
assert(repr(test)[:27] == match)

# Test nvalue() [ + value() ]
test = repr(trix.nvalue('util.enchelp', 'EncodingHelper'))
match = "<class 'trix.util.enchelp.EncodingHelper'>"
assert(test == match)

# Test ncreate() [ + create() ]
test = trix.ncreate('util.enchelp.EncodingHelper', encoding='utf_8')
match = "<trix.util.enchelp.EncodingHelper"
assert(repr(test)[:33] == match)



# Test proxify()
class TestP(object):
	def __init__(self, v):
		self.v = v

tp = TestP(9)
assert(trix.proxify(tp).v == tp.v)


# Test kcopy, kpop
assert(trix.kpop(dict(a=1,b=9,c=4), 'a c') == dict(a=1,c=4))
assert(trix.kpop(dict(a=1,b=9,c=4), ['a', 'c']) == dict(a=1,c=4))
assert(trix.kcopy(dict(a=1,b=9,c=4), 'b') == dict(b=9))
assert(trix.kcopy(dict(a=1,b=9,c=4), ['b']) == dict(b=9))

raise Exception("GOOD!")

# -------------------------------------------------------------------
#
# TEST TRIX SUB-PACKAGES
#
# -------------------------------------------------------------------

#
# Load the test.util init module, which tests all available 
# trix.util modules.
#
"""
trix.nmodule('test.util')

"""








