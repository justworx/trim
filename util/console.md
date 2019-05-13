

#### under construction - trying to convert list of dicts to a grid

    I'm trying to make a grid in Console that displays the status of
    all Runner objects. The goal is to eventually query and select
    Runner objects using the grid. Once selected, a Runner could be
    manipulated.
    
    Of course, the code below DOES NOT WORK	at the moment. Hopefully
    tomorrow I'll have enough brainpower to turn the whole thing into
    a propgrid.
    
    REM: I'll need a way to drill into the dict structure recursively
         to get (eg) encoding, errors, and bufsz into columns. Or,
         maybe those items should be flattened in the status dict.
         
         Can't think anymore tonight!


```python3

from trix.util.runner import *


kk = []                     # store all keys  (cols)
dd = []                     # store dict data (rows)


foo = Runner(name='foo').starts() # create runners
bar = Runner(name='bar').starts()


c = Console()
for o in c.OList:
  d = o.status()            # status dict of a Runner
  dd.append(d)              # store it
  keys = list(d.keys())     # get it's key list
  kk.extend(keys)           # add all keys together


kset = set(kk)              # unique set of keys
head = sorted(list(kset))   # sort the key set (column heading)


rows = []                   # storage for rows
for d in dd:                # dd = all runner status dicts
  row = []                  # storage for *this* row
  for col in head:          # col in head == field name
  	row.append(d.get(col))  # store each field in `row`
  rows.append(row)          # store each row in `rows`

```
