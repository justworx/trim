#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from trix.x.vector import *

v = vector({1:11, 4:44})
assert(v.row == [0, 11, 0, 0, 44])
assert(v.width == 5)


m = matrix([{1:11, 4:44}, {2:22}, {3:33}])
