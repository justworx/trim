#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix.x.vector import *

v = vector({1:11, 4:44})
assert(v.row == [0, 11, 0, 0, 44])
assert(v.width == 5)

#
# This isn't actually in trix.data yet, it's in trix.x - however,
# I wanted to build the test file while developing the classes.
#

#
# ALSO: This filename may change to "matrix.py", or it may become
#       a `data.matrix` package with various files.
#

