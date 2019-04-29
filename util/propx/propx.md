
# propx

The propx package contains a set of modules defining classes that
each wraps suitable objects with a set of appropriate convinence
properties and methods.

The propx function, defined in propx.__init__.py, receives any object
and wraps it in the most suitable available subclass of `propbase`.
For example, list objects passed to `propx()` would be wrapped inside
a	`proplist` object, which provides methods and properties convenient
for querying, manipulation and display of list objects.



#### propx classes

The following modules/classes are currently available.

 * propbase - generic encoding, compression, and display methods. 
 * propiter - adds methods suitable to iterable objects
 * propseq  - methods suitable to any sequence item (based on propset) 
 * proplist - methods for list manipulation/display
   propgrid - proplist subclass for list of lists of equal length 
 * propdict - covers dict-like objects



#### propx use in the trix package

The propx objects are currently used by the fs.dir module to enhance
the return values of directory listings and search results.

The `dir.ls` member is now a property that returns a proplist object
with a __call__() method which returns the directory listing, but the
returned proplist object also provides a variety of other useful
methods as well.

For example:

```
python3

import trix
d = trix.path('trix') # <-- CREATE A `Dir` OBJECT

d.ls()                # <-- RETRIEVE THE STANDARD `ls` RESULT LIST

d.ls.table(width=4)   # <-- SHOW A TABULATED VERSION OF THE LIST

```


The long `dir.list` property's __call__() method works the same way, 
but provides the features of a grid rather than a list.

```
python3

import trix
d = trix.path('trix') # CREATE A `Dir` OBJECT
d.list()              # call as a function to return the list
d.list.grid()         # call as a property to access display methods

```



The root of sequence items is	`propiter`, which provides most of the
functionality for manipulation of lists.

```python3

from trix.util.propx.propiter import *

pi = propiter([]) 
list( pi.filter(lambda x: x<3, [1,2,3,4,5]) ) # FILTER

list( pi.filterfalse(lambda x: x<3, [1,2,3,4,5]) ) # FILTERFALSE

i = propiter([])
ii = i.zip('ABCD', 'xy') # ZIP
list(ii)

```



Use filters to select only the appropriate items...

```
from trix.util.propx.propiter import *

pi = propiter([]) 
list( pi.filter(lambda x: x<3, [1,2,3,4,5]) ) # FILTER

list( pi.filterfalse(lambda x: x<3, [1,2,3,4,5]) ) # FILTERFALSE

i = propiter([])
ii = i.zip('ABCD', 'xy') # ZIP
list(ii)

```


The propiter map and zip methods are designed to behave the same in 
both python 2.7.x and python 3.x. Always use python3 conventions
when passing parameters to propiter filtering methods.

```python3
from trix.util.propx.propiter import *
pi = propiter([]) 
list( pi.zip('ABCD', 'xy') )                   # ZIP
list( pi.zip(['ABCD', 'xy'], ["foo", "bar"]) ) # ZIP

```




## See doc

The propx package is fairly new and won't be fully documented until
all the kinks are worked out. For now, please see the python help
for more information on the individual classes and methods.




