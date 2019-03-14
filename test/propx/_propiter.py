#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix.propx import *

ii = propx(range(1,999))

assert (ii.T == "<class 'trix.propx.propseq.propseq'>")
assert (repr(ii.To) == "<class 'range'>")

assert(ii[0:9].o == range(1,10))
assert(ii[0:9].o == range(1,10))

ii[0:9].o
