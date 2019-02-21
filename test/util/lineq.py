

# UTIL.LINEQ
from ...util.lineq import *

q = LineQueue(encoding='utf_8')
q.feed("Abcd\r\n123")

assert(q.q.get() == "Abcd\r\n")
assert(q.fragment == '123')

