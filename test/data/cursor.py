#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ...data.cursor import *

c = Cursor([[1,2], [3,4]])

assert (c.fetch() == [1,2])
assert (c.fetch.i == 0)

assert (c.fetch() == [3,4])
assert (c.fetch.i == 1)



#
# Test the `use` kwarg.
#
c = Cursor([[1,2], [3,4]], use=lambda p: p.v[0] == 3)

fetched = c.fetch()

assert (fetched != [1,2])
assert (fetched == [3,4])


# need to test each param method next


