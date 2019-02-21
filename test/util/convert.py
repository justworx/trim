

# UTIL.CONVERT
from ...util.convert import *
assert(Convert().temp('f', 'c', 0) == 32)
assert(Convert().temp('c', 'f', 32) == 0)


