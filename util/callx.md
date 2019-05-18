
# trix.util.callx

The `callx` module makes it easy to retrieve the results of calls to 
system executables and provides result manipulation and display by
returning the result in the most appropriate propx object.


## callx class

Create a callx object using the trix.callx() method, or by importing
`trix.util.callx` and creating a `callx()` object the normal way.

There are two ways to use callx to open: 
 * call system executables directly
 * call a trix cline handler using the "cline" keyword argument


#### examples

Here's a simple example of the use of the `callx` class to query a
system executable.

```python3

from trix import *
ps = trix.callx("ps")
ps.text()              # Get the result text
ps.text.lines()        # OR, split the result text into lines
ps.text.lines.list()   # OR, display the lines as a formatted list

```

In the example above, callx queries the (Linux) operating system for 
a list of running processes, and gives examples of how to use the
result, `ps`, to view and massage result data using the `ps` object's
methods.



#### callx with trix command-line handlers

Pass arguments using kwarg "cline" to easily access trix command
line handler results.

```python3

from trix import *
cx = trix.callx(cline="echo Phoo Bear!")
cx.text()
cx.data()

```

In the example above, the "echo" command line handler returns the
text "Phoo Bear!". Calling the `cx` result object's data property as
a method returns a list containing the (json-parsed) result of the 
query.

Most callx methods return propx obects, Eg., proplist, propstr,
propdict, etc... These objects may be strung along from one to the
next, providing an easy way to massage data as needed. 



# more complex callx queries

```python3

from trix import *
ps = trix.callx("ps")
ps.data.lines.o

trix.callx("ps -u").data.lines.o
trix.callx("ps -u").data.lines.select(lambda x: x.split(maxsplit=10)).o
trix.callx("ps -u").data.lines.select(lambda x: x.split(maxsplit=10)).grid()

px = trix.callx("ps -aux").data.lines.select(lambda x: x.split(maxsplit=10))
pg = px.propgrid()

```

The propx objects provide a powerful set of methods which, once you've
learned their use, can really speed up the process of massaging data 
to get just the results you need.


```python3

from trix import *
px = trix.callx("ps -aux").data.lines.select(lambda x: x.split(maxsplit=10))
px.propgrid.dbgrid('ps').select("select * from ps order by TIME desc").grid()

```

For more information on propx results, see:
 * [how-to-use-propx](https://github.com/justworx/trix/wiki/how-to-use-propx)

