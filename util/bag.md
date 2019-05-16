
## trix.util.bag

The `trix.util.bag` module provides means for storing data as a 
dict-like selection of values.

The `trix` version of `Bag` is not like that of java. Here, `Bag` is 
used mainly to collect counts of named occurrences, or accumulate sets
of categorical values.

    NOTE:
    To avoid confusion, the name `Bag` may be changed before the
    final draft - if I can think of a better one that's not taken.


### Bag

Bag objects may hold/manipulate only a single object type. Create a 
Bag object by passing the relevant type object to the constructor.
Then, `put`, `add`, or `get` objects by name.


#### Preview Example

```python3

from trix.util.bag import *

b = Bag(str)
b.put("greeting", "Hello, World!") 

b.get("greeting")
b['greeting']

b.add("greeting", " ...and goodbye")
b.get("greeting")

```


##### `Bag.__init__()`

Pass a `type` object to the `Bag` constructor.


##### `Bag.put(category, x)`

Put object `x` to the `category` category. This will replace any 
existing value(s) in `category`.


##### `Bag.add(category, x)`

Add object `x` to the `category` category. Note that this method 
may only be used with data that can be added to using the addition 
operator.


##### `Bag.append(category, x)`

Append object `x` to the `category` category. Note that this method 
may only be used with data objects that support the `append` method.



#### More Examples

Explore Bag use with type `int`.

```python3

from trix.util.bag import *

b = Bag(int)
b.add("one", 1)
b.add("one", 1)

b.get("one")
b.dict() # {'one': 2}

b.put("one", 3)
b['one']

```


Explore the use of `list`.

```python3

from trix.util.bag import *

b = Bag(list)
b.add("stuff", 1)

b.get("one")
b.dict() # {'one': 2}

b.put("one", 3)
b['one']

```
