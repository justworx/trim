
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

Here's a combination scenerio. The `each` method passes the Param
object and an enumeration of the offset and items of `self.v` so that 
each item in a list, dict, or sequence of any kind can be operated on 
individually.

```python3

from trix.data.param import *
p = Param(["Hello", "World"]) 

p.each(lambda p,i,v: p.setx(i, v.upper())) # set items to uppercase
p.each(lambda p,i,v: p.output([i,v])).null # print each, return None

```






