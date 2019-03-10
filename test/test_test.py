
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
db = Database(config, auto=True)

#test
db.open()
assert(db.active)

db.opq("addanimal", ("mares", "oats"))
db.opq("addanimal", ("does", "oats"))
db.opq("addanimal", ("lambs", "ivy"))

db.commit()

c = db.execute("select * from animals")
r = sorted(list(c.fetchall()))
assert(r == [('does', 'oats'), ('lambs', 'ivy'), ('mares', 'oats')])

