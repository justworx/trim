

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

Param([1,2,3]).set(['0',99]).v                      # ['0', 99]

Param([1,2,3]).setx(0,99).v                         # [99, 2, 3]
Param([1,2,3]).setx(1,99).v                         # [1, 99, 3]
Param([1,2,3]).setx(2,99).v                         # [1, 2, 99]

p = Param([1.1, 2.2, 3.3])
p.setxx([0,2], lambda p,x: int(p.v[x]) ).v          # [1, 2.2, 3]

p = Param([1.1, 2.2, 3.3])
p.setxx(range(0,3), lambda p,x: int(p.v[x]) ).v     # [1, 2, 3]


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


#### calling functions/procedures

The `proc` and `procx` methods operate by setting the value of 
`self.v` to the return value of a given callable object.

Use `proc` to operate on the entire value `self.v`. Use `procx` to
operate on the individual value of item `x`.

```
from trix.data.param import *

p = Param([1,2,3])
p.proc(sum, p.v).v                             # 6

Param([1,2,3]).procx(1, lambda p: p.v[1]*3).v  # [1, 6, 3]

```

The use of `call` is more like a pascal procedure that has no
return value. Use `call` when the callable `fn` operates directly
on the structure being passed.

Note that `call` does not pass `self.v`. This is intentional. Pass
`self.v` explicitly in the argument position required by the callable.

```
from trix.data.param import *

def listbump(ls):
  for i in range(0, len(ls)):
    ls[i] = ls[i]+1

p = Param([1,2,3])
p.call(listbump, p.v).v        # [2, 3, 4]
p.call(listbump, p.v).v        # [3, 4, 5]
p.call(listbump, p.v).v        # [4, 5, 6]

```



#### string ops

Here are some string operations for convenience.

```
from trix.data.param import *

Param("crash boom bam!").split().v          # ['crash','boom','bam!']
Param(['crash','boom','bam!']).join(' ').v  # 'crash boom bam!'

Param("Hello!").pad(15, "!").v              # 'Hello!!!!!!!!!!'
Param("Hello!").pad(15, "!").pad(16,' ').v  # 'Hello!!!!!!!!!! '

Param("  Hello!  ").strip().v               # 'Hello!'
Param("  Hello!  ").strip(None, -1).v       # 'Hello!  '
Param("  Hello!  ").strip(None, 1).v        # '  Hello!'
Param("x  Hello!  x").strip('x').v          # '  Hello!  '
Param("x  Hello!  x").strip('x', -1).v      # '  Hello!  x'


```



#### other/util

The `Param.write` writes argument `v` (which defaults to `self.v`)
to the stdout stream, so that it the output will appear from within
a lambda even in python 2.7.x.

The `Param.each` method calls each object in `self.v` passing the
object, its enumeration (integer offset or dict key), and the item 
value.

The `Param.null` property returns None (rather than `self`.)

```
from trix.data.param import *
Param([1,2,3]).each(lambda p,i,v: p.write(v))
Param([1,2,3]).each(lambda p,i,v: p.write(v)).null

```


