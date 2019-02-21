

from ...util.encoded import *

tests = [
	b"Test stuff < charset = utf_8 > blah-blah",
	b'Test other < encoding= "utf_8" > blah-blah',
	b"Test blah  < encoding ='utf_8' > blah-blah"
]
for test in tests:
	assert(Encoded(test).detect()) == 'utf_8'



