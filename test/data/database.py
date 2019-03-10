#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ...data.database import *

try:
	trix.path("~/.cache/trix/test/dbtest.sqlite3").wrapper().remove()
except:
	pass

try:
	trix.path("~/.cache/trix/test/dbtest2.sqlite3").wrapper().remove()
except:
	pass

time.sleep(0.1)


# --- SIMPLE TEST FIRST ---

# create/open a database
db1 = Database("~/.cache/trix/test/dbtest.sqlite3")
db1.open()

assert(db1.active)

db1.execute("create table test1 (a, b, c)")
db1.execute("insert into test1 values ('A','B','C')")

c = db1.execute("select * from test1")
assert(c.fetchone() == ("A", "B", "C"))

db1.close()
assert(db1.active == False)


# --- TEST COMPLEX FEATURES ---

# test with a config dict
from trix.data.database import *

# test with a config dict
config = {
	"path" : "~/.cache/trix/test/dbtest2.sqlite3",
	"sql" : {
		"create" : ["create table animals (animal, food)"],
		"op" : {
			"addanimal" : "insert into animals values (?, ?)",
			"getfeed" : "select food from animals where animal = ?"
		}
	}
}

# create db with config (and auto-create set)
db2 = Database(config, auto=True)

#test
db2.open()
assert(db2.active)

db2.opq("addanimal", ("mares", "oats"))
db2.opq("addanimal", ("does", "oats"))
db2.opq("addanimal", ("lambs", "ivy"))

db2.commit()

c = db2.execute("select * from animals")
r = sorted(list(c.fetchall()))
assert(r == [('does', 'oats'),('lambs', 'ivy'),('mares', 'oats')])


try:
	db1.close()
except:
	pass
try:
	trix.path("~/.cache/trix/test/dbtest.sqlite3").wrapper().remove()
except:
	pass

try:
	db2.close()
except:
	pass
try:
	trix.path("~/.cache/trix/test/dbtest2.sqlite3").wrapper().remove()
except:
	pass
"""
"""
