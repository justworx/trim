


from ...propx import *

# test propx creation types
assert(type(propx([1,2])).__name__  == "proplist")
assert(type(propx("1,2")).__name__  == "propstr")
assert(type(propx(b"1,2")).__name__  == "propseq")
assert(type(propx((1,2))).__name__  == "propseq")
assert(type(propx(tuple([1,2]))).__name__  == "propseq")
assert(type(propx(iter([1,2]))).__name__  == "propiter")


#test propiter
ii = propx(iter([1,5,3,2,7]))
ii.sorted()



