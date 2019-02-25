

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

pd.update(lambda x: list(x))

```


# No... #q = pd.each(lambda p,i,v: p.setx(i, list(v)))



```python3

from trix.data.dbgrid import *

q = DBGrid(trix=trix.path('trix').list()) # get the trix dir list
pp = q('select * from trix')              # returns proplist

pp.grid()

pd = pp[1:] # param data rows only, no heading 
pd.grid()

pd.each(lambda o: 


```











# FAIL

use=lambda p:Param(p.v).cast(list).setx(5,int(p.v)).v if p.i else None
c = p.create('data.cursor.Cursor', pp.o, use=use)

#pp[1:].each(lambda p,i,v: p.setx(i, int(v)))

from trix.data.dbgrid import *
q = DBGrid(trix=trix.path('trix').list())
pp = q('select * from trix')

pp.grid()

pp.pdq().update(
		lambda p: p.setx(5, int(p.v[5])) , 
		
		where=lambda p: p.i > 1

	)





# more stuff

from trix.data.dbgrid import *

q = DBGrid(trix=trix.path('trix').list())
pp = q('select * from trix') # returns proplist

pp.param(pp.o[1:])[0]

















