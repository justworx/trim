

from trix.x.callx import *
c = callx("python3 -m trix echo 'Hello, World!'")
c.data


from trix.x.callx import *
cx = callx.trix("echo Phoo Bear!")
cx.text
cx.data()


from trix.x.callx import *
cx = callx.trix("loc en_CA.utf_8")
cx.data.display()


#
# external
#

python3
from trix.x.callx import *
ps = callx("ps")
ps.data.lines[:-1]

callx("ps -u").data.lines.o
callx("ps -u").data.lines.select(lambda x: x.split(maxsplit=10)).o
callx("ps -u").data.lines.select(lambda x: x.split(maxsplit=10)).grid()

px = callx("ps -aux").data.lines.select(lambda x: x.split(maxsplit=10))
pg = px.propgrid()



#
```python3

from trix.x.callx import *
px = callx("ps -aux").data.lines.select(lambda x: x.split(maxsplit=10))
pg = px.propgrid()
dg = pg.cast().dbgrid("ps")
dg.select("select * from ps").grid()
pd('select * from ps order by MEM desc').grid()


```
