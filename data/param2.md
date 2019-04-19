

# trix.data.param

The `data.param` module provides a set of methods that make data 
manipulation easier. It's particularly useful for commonly needed 
features found in callback methods. Param objects are used mostly by  
the data module's `Cursor` object and by propx objects, but can be 
used anywhere, as the following examples should make clear.

Param objects always contain a value `v`, which is the value this
object represents. 

Param objects often contain an optional `i` value, representing the
item's offset, when used by such as the `data.cursor.Cursor` object.


#### setting param values

The `set`, `setx`, and `setxx` methods allow direct setting of all,
one, or some items in `self.v`.

```
from trix.data.param import *
Param([1,2,3]).set(['0',99]).v
Param([1,2,3]).setx(0,99).v
#Param([1,2,3]).setxx([0,2],[99,33].remove).v


```



#### typecasting

The `cast` Param method lets you force values into alternate types
where appropriate. The alternate form, `castx` is for use on only
specified values in `self.v`.

```
from trix.data.param import *

Param([1,2,3]).cast(str).v       # '[1, 2, 3]'
Param([1,2,3]).castx(1, str).v   # [1, '2', 3]

```

The job of jcast is to recast values into their natural type - as 
they'd be parsed by javascript. For example, parsing the string 
representation to a list, as is shown below using `jcast`, or by
casting individual items in a list as needed, as shown using the
`jcastx` method.

The `jcasteach` method automatically casts each item in a list of
values to it's natural javascript form, relieving us of the need
to cast each item individually using `jcastx`.

```
from trix.data.param import *

Param("[1,2,3]").jcast().v                # [1, 2, 3]
Param([1.1,"2.1","3.1"]).jcastx(1).v      # [1.1, 2.1, '3.1']
Param([1.0, "2", "three"]).jcasteach().v  # [1.0, 2, 'three']

```


#### manipulation

The `proc` and `procx` methods operate on the value of `self.v`.

```
from trix.data.param import *

p = Param([1,2,3])
p.proc(sum, p.v).v

from trix.data.param import *
Param([1,2,3]).procx(1, lambda p: p.v[1]*3).v

```
