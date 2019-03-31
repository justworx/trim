
# new plan for udata.query

I'm going to put an sqlite3 database in .cache which contains all
unicode data tables. This saves me writing an sql-like query parser
and (I'm betting) it will probably speed up the querying process.


