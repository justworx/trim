
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
 * propdict - covers dict-like objects - UNDER CONSTRUCTION

#### propx use in the trix package

The propx objects are currently used by the fs.dir module to enhance
the return values of directory listings and search results.

```
python3

import trix
d = trix.path('trix') # <-- CREATE A `Dir` OBJECT

d.ls()                # <-- RETRIEVE THE STANDARD `ls` RESULT LIST

d.ls.table(width=4)   # <-- SHOW A GRID-FORMATTED VERSION OF THE LIST

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



Try in both python (2.7) and python3...

python
python3

The root of sequence items is	`propiter`, which provides most of the
functionality for manipulation of lists.

```
from trix.propx.propiter import *

# FILTER
pi = propiter([])
list( pi.filter(lambda x: x<3, [1,2,3,4,5]) )

# FILTERFALSE
list( propiter.filterfalse(lambda x: x<3, [1,2,3,4,5]) )

# ZIP
i = propiter([])
ii = i.zip('ABCD', 'xy')
list(ii)

```












Get some data to play with...

```python3

from trix.data.dbgrid import *

q = DBGrid(trix=trix.path('trix').list()) # get the trix dir list
pp = q('select * from trix')              # returns proplist

```


Here's a proplist `pp` with lots of fun and helpful methods.

```
pp.grid()

```


See how there are some problems. First, the rows are really wide for
display in a skinny terminal window, so I'd like to turn those time
values to integers. Second... to do that, we need to operate only on
the data rows, not the column headers.

```

pd = pp[1:] # param data rows only, no heading 
pd.grid()

```

Creating and viewing a new proplist, `pd`, with all but the first 
row, the list of column names, solves the second problem. However,
the remaining rows each consist of a set of values (rather than a
list) and so they can't be altered in place.

What's needed next is a way to convert those sets to lists.



Here I'll try to loop through each object turning it into a list.
First I'll just print each object.

Remember that proplist.each loops through the lines, not the values
of any given line.

```

pp.update(lambda x: list(x))

```



#### Moving to `trix.util`

Though far from complete, I'm moving `trix.propx` to util and 
delaying any further development there for now. The classes that
currently return propx objects will continue to do so, but until
the current bugs are fixed (and a proper test suite is complete)
I'll hold off adding anymore to the propx package.







