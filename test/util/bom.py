

# UTIL.BOM
from ...util.bom import *
assert(testbom("abc".encode("utf32")).startswith('utf_32'))
assert(testbom("abc".encode("utf16")).startswith('utf_16'))
assert(testbom("abc".encode("utf_8_sig")) == "utf_8_sig")


