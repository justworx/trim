#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *


#
# --- PREP FOR TESTING --- 
#

from ...data.database import *

def remove_test_databases():
	# Remove any existing database test files
	try:
		path = testpath("dbtest.sqlite3")
		trix.path(path).wrapper().remove()
	except OSError, FileNotFoundError:
		pass
	except BaseException as ex:
		raise type(ex)(ex.args, xdata(path=path))
	
	try:
		path = testpath("dbtest2.sqlite3")
		trix.path(path).wrapper().remove()
	except OSError, FileNotFoundError:
		pass
	except BaseException as ex:
		raise type(ex)(ex.args, xdata(path=path))


# initial cleanup
remove_test_databases()
time.sleep(0.1)


#
# --- TEST SIMPLE FEATURES ---
#

# create/open a database
db1 = Database(testpath("dbtest.sqlite3"))
db1.open()

assert(db1.active)

db1.execute("create table test1 (a, b, c)")
db1.execute("insert into test1 values ('A','B','C')")

c = db1.execute("select * from test1")
assert(c.fetchone() == ("A", "B", "C"))

db1.close()
assert(db1.active == False)



# --- TEST COMPLEX FEATURES ---

# test creation of Database with a config dict
from trix.data.database import *

config = {
	"path" : testpath("dbtest2.sqlite3"),
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




#
# --- CLEANUP, REPORT --- 
#
remove_test_databases()
report("database: OK")



