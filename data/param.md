
# Param Facts

The `Param` class, defined in `trix.data.param`, is what's typically
sent by the trix package as arguments to callback methods.


#### Param constructor

Param's `self.v` member variable starts as the value given to the 
consructor. There's also an optional `self.i` member that's set by 
iterating classes such as `Cursor` and pdq.Query. Default is `None`.


```python3

from trix.data.param import *
p = Param(["Hello", "World"])

print ("--> p.v = %s" % str(p.v))
print ("--> p.i = %s" % str(p.i))

```



#### Param Methods

Param has a set of methods that operate on the `v` member variable.


```python3

from trix.data.param import *
p = Param(["Hello", "World"]) 

p.v

p.join() # NOTE: Param manipulation methods usually return `self`.

print ("--> p.v = %s"    % str(p.v))    # join p.v into a string

print ("--> p[0:3] = %s" % str(p[0:3])) # access items in p.v string

p.split()                               # split it back into a list

print ("--> p.v = %s" % str(p.v))       # p.v is now a list

print ("--> p[0] = %s" % str(p[0]))     # access items in p.v
print ("--> p[1] = %s" % str(p[1]))     # access items in p.v


```


###### Using `set()` and `setx()`

Use the `set` method within your callback to change the entire value
of `self.v`.

Use `setx()` to change a specific item in `self.v`.


```python3

from trix.data.param import *
p = Param(["Hello", "World"])  # Create Param with Hello World list

p.set(["Goodbye", "World"]).v  # Set `self.v` directly.
p.setx(0, "Hello again,").v    # (append .v to print the result)

```


###### Manipulate Each Item

Here's a combination scenerio. The `each` method passes `p` the Param
object and an enumeration of the offset and items of `self.v` so that 
each item in a list, dict, or sequence of any kind can be operated on 
individually.

```python3

from trix.data.param import *
p = Param(["Hello", "World"]) 

p.each(lambda p,i,v: p.setx(i, v.upper())) # set items to uppercase
p.each(lambda p,i,v: p.output([i,v])).null # print each, return None

```


###### Manipulate Portions of Each Item

```python3

from trix.data.param import *

d = trix.path('trix') # create and show a long directory listing
d.list.grid()         # notice the float time values

for x in d.list[1:]:
  
  # get rid of the micro-milli-billi-seconds
  p = Param(d.list()) 
  p.setxx([5,6,7], lambda p,x: int(float(p.v[x])))
  
```

Change a directory listing's floats to ints (for brevity).

```
dlist = ['trix', 'd', '1551543158.9558208', '1551543136.5832613']
p = Param(dlist)
p.setxx([2,3], lambda p,x: int(float(p.v[x])))

```



###### process callx results

```
import trix
cx = trix.callx('ps -aux')      # call for process listing
plist = cx.text.lines.proplist  # get a proplist of the lines

xs = plist.select(lambda p: p.split(maxsplit=10)) # split each line
xs.proplist.select(lambda p: p.jcasteach())       # parse each field
xs.grid()                                         # display grid

db = xs.propgrid.dbgrid('ps')
db.select('select * from ps order by mem desc').grid()

```

Looks like dbgrid still doesn't "order by" properly - probably because
the SQL table definitions aren't including column types. Maybe I can
pass types from the first row and generate a better table def.

Maybe tomorrow. Brain Needs Sleeeeeeep.



