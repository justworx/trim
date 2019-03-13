#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *


from ...fmt import *


# FORMAT
f = Format('{0}, {1}, {2}')
assert(f.format("bob's", "your", "Uncle!")=="bob's, your, Uncle!")

compact_bytes = f.compact("bob's", "your", "Uncle!")
assert(compact_bytes == b"eJxLyk9SL9ZRqMwvLdJRCM1LzklVBABAAgZN")

expanded_bytes = f.expand(b"eJxLyk9SL9ZRqMwvLdJRCM1LzklVBABAAgZN")
assert(expanded_bytes == b"bob's, your, Uncle!")

report("Format: OK")


# JSON
d = {'a':1, 'b':9, 'c':4}
k = dict(sort_keys=True) # <------------------------------ SORTED!
assert(JSON(**k).format(d) == '{"a": 1, "b": 9, "c": 4}')
assert(JCompact(**k).format(d)=='{"a":1,"b":9,"c":4}')


#
# UNFORTUNATELY...
#  - This needs a check of python version...
#
if sys.version_info[0] == 3:
	assert(JDisplay(**k).format(d)=='{\n  "a": 1,\n  "b": 9,\n  "c": 4\n}')
else:
	assert(JDisplay(**k).format(d)=='{\n  "a": 1, \n  "b": 9, \n  "c": 4\n}')

report("JSON suite: OK")


#LIST/GRID/TABLE
assert(List().format("a b c".split()) == '1  a\n2  b\n3  c')
assert(Grid().format([[1,2],[3,4]]) == '1  2\n3  4')
assert(Table(width=2).format([1,2,3,4,5])=='1  2\n3  4\n5   ')

report("List/Grid/Table: OK")




report("fmt package: OK")

