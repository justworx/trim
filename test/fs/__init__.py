#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *
from ...fs import *


#
# Get the Path to the TEST_DIR directory
#
p = trix.path(TEST_DIR, affirm="makedirs")

#
# Next, get a list of the files in TEST_DIR.
# This line puts the list of files into `pso`.
#
pso = p.search().o[0].get('files', [])

#
# Now loop through the files, removing each.
#
for f in pso:
	trix.path(f).wrapper(encoding=DEF_ENCODE).remove()

#
# The above for-loop should have cleared the TEST_DIR
# directory of all files.
#




# TXT
d = Path(trix.innerpath()).dir()
try:
	assert("LICENSE" in d.ls())
except:
	raise Exception("Trix Package LICENSE file is missing!")


# check path.exists false
assert (test.path("foo.txt").exists()==False)

# make a file and assert it exists
w = test.path("foo.txt").wrapper(affirm='touch')
assert (w.exists() == True)

# write some content and affirm read matches
T = b"This is a test!\n"
w.write(T)
assert (w.read() == T)

# do it again with encoding
w = test.path("foo.txt").wrapper(affirm='touch', encoding="utf_8")
T = "This is a test!\n"
w.write(T)
assert (w.read() == T)

# now remove the file
w.remove()
assert(w.exists()==False)



# BZIP
bz = test.path("foo.bz2").wrapper(affirm='touch')
T = b"B-zip-ity doo dah..."
bz.write(T)
assert(bz.read() == T)

bz.remove()
assert(bz.exists()==False)



# GZIP
gz = test.path("foo.gzip").wrapper(affirm='touch', encoding='utf8')
T = "G-zip-ity doo dah..."
gz.write(T)
assert(gz.read() == T)

gz.remove()
assert(gz.exists()==False)



# ZIP
z = test.path("foo.zip").wrapper(affirm='touch')
M = "testmember"
T = b"Zip-ity doo dah\nZiping is fun!\n"
z.write(M, T)

# The content is there before flush but the name isn't because only
# existing names are read into the names property.
assert(z.read(M) == T)
assert(z.names() == [])

z.flush()
assert(z.read(M) == T)
assert(z.names() == [M])

z.remove()
assert(z.exists()==False)



# TAR.GZ
t = test.path("foo.tar.gz").wrapper(affirm='touch')
M = "testmember"
T = b"I'm gettin' tar'd...\n...of writing test scripts.\n"

t.write(M, T)
assert(t.read(M) == T)
assert(t.names() == [])

t.flush()
assert(t.read(M) == T)
assert(t.names() == [M])

t.remove()
assert(t.exists()==False)


