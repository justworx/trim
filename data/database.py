#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
# 

from .. import *


SAMPLE_CONFIG_DICT = {
	"path" : "~/sample.db",
	"sql" : {
		"create" : [
			"create table foo ('bar','baz')",
			"insert into 'foo' values ('barnone', 'baz00kas')"
		],
		"op" : {
			"getfoo" : "select * from foo"
		}
	}
}



class Database(object):
	"""
	Wrapper for DB-API 2.0 database access, plus additional features.
	
	EXAMPLE 1:
	#
	# Simple use of the Database class:
	#
	>>> from trix.data.database import *
	>>> db = Database("test-simple.db")
	>>> db.open()
	>>> d.execute("create table fos (food, fools, folly)")
	>>> d.execute("insert into fos values ('spam','dorks','python')")
	>>> c = d.execute("select * from fos")
	>>> c.fetchone()
	
	EXAMPLE 2:
	#
	# Create database using a config file (or dict).
	#
	>>> from trix.data.database import *
	>>> db = Database("test-config.db", sql=SAMPLE_CONFIG_DICT)
	>>> db.open()
	>>> db.create()
	>>> c = db.execute("select * from foo")
	>>> c.fetchall()
	[('barnone', 'baz00kas')]
	>>> 
	
	EXAMPLE 3:
	>>> # 
	>>> # USING 'ops' with `Database.opq`.
	>>> # 
	>>> from trix.data.database import *
	>>> db = Database("test-config.db", sql=SAMPLE_CONFIG_DICT)
	>>> db.open()
	>>> db.opq('getfoo')
	[('barnone', 'baz00kas')]
	>>> 
	
	"""
	
	LOADERR = []
	CONFTYPE = ''
	CONFUSED = None
	
	# read-conf
	def __readconf(self, config, *a, **k):
		"""
		#
		# TODO (Maybe)
		#
		if 'nconfig' in k:
			config = trix.nconfig(k['nconfig'])
		
		As this is passed only by keyword argument, I guess (in keeping
		with the theme) it should take precedence over the others. I'll
		have to put it in a try block before the first one, below.
		
		I'm not sure it would be useful, but there may come to be many
		packages that provide useful databases - probably in a set of
		plugin objects.
		
		I'll probably wait until that comes to pass before adding the
		nconfig option.
		
		"""
		
		config = config or {}
		errors = []
		
		try:
			# try to read config as a dict
			config.update(k)
			self.CONFUSED = 1
			self.CONFTYPE = str(type(c))
			return config
		except BaseException as ex:
			self.CONFTYPE = None
			self.CONFUSED = 0
			pass
			#print ("Not a dict. " + str(ex))
			#self.LOADERR.append(xdata(ex=str(ex)))
		
		try:
			# try to load config as a config file
			c = trix.config(config, **k)
			c.update(k)
			self.CONFUSED = 2
			self.CONFTYPE = str(type(c))
			return c
		except BaseException as ex:
			self.CONFTYPE = None
			self.CONFUSED = 0
			pass
			#print ("Not a config file. " + str(ex))
			#self.LOADERR.append(xdata(ex=str(ex)))
		
		try:
			# config must be a file path directly to the database file
			c = {'path':config}
			c.update(k)
			self.CONFTYPE = str(type(c))
			self.CONFUSED = 3
			return c
		except BaseException as ex:
			self.CONFTYPE = None
			self.CONFUSED = 0
			pass
			#print ("Not a file path. " + str(ex))
			#self.LOADERR.append(xdata(ex=str(ex)))
	
	
	#
	#
	# __INIT__
	#
	#
	def __init__(self, config=None, *a, **k):
		
		#
		# READ CONFIG
		#  - Config always comes back as a dict (even if empty)
		#
		self.__config = self.__readconf(config, **k)
		self.__path   = self.__config.get('path')
		
		#
		# ARGS:
		#  - Store args for opening database. These args
		#    are held until it's time to open the db file.
		#
		self.__args = a = list(a)
		
		#
		# PATH
		#  - Some databases need a `path`, some don't.
		#  - If there's a path, insert it as the first item in args.
		#  - If there's a path, expand it to a full path and make sure 
		#    its containing directory exists.
		#  - In any case, store the given path.
		#
		if self.__path:
			path = trix.path(self.__path, affirm='makepath').path
			self.__args.insert(0, path)
		
		# Store the path. Note: It might be None for some dbms.
		#self.__path = path
		
		# Initialize runtime values.
		self.__con = None
		self.__inited = None
		
		#
		# MODULE
		#  - The module may be given by name, or by passing the module
		#    class as the module keyword, or in a dict a `module` key.
		#
		mod = self.__config.get('module', 'sqlite3')
		try:
			self.__mod = trix.module(mod)
			self.__modname = mod
		except:
			self.__mod = mod
			self.__modname = type(self.__mod).__name__
		
		#
		# SQL
		#  - An 'sql' key may be included in the config spec. If `auto`
		#    is True, the "create" key in the "sql" specification dict
		#    will be used to initialize tables.
		#  - An "op" dict may also be included in the "sql" dict. If
		#    present, queries there may be 
		#
		sql = self.__config.get('sql', {})
		try:
			# string path to sql file
			rdr = trix.path(sql).reader()
			sql = trix.jparse(rdr.read())
		except:
			sql = sql
		
		# sql/op
		self.__sql = self.__config.get('sql', {})
		self.__op = self.__sql.get('op', {})
		
		#
		# AUTO-INIT
		#  - If autoinit is set to true, the first call to open will try
		#    to create the new database by executing the queries defined
		#    in the `sql` parameter's content.
		#  - An `sql` value must exist, or autoinit will remain False.
		#
		self.__autoinit = self.__sql and self.__config.get('auto', False)
		
	
	#	
	#	
	# __DEL__
	#	
	#	
	def __del__(self):
		"""
		On deletion of the Database object, close the database (if open).
		"""
		try:
			self.close()
		except:
			pass	
	
	
	#	
	#	
	# ACTIVE
	#	
	#	
	@property
	def active (self):
		"""Returns True if the database is open/connected."""
		return True if self.__con else False
	
	
	#	
	#	
	# CONFIG
	#	
	#	
	@property
	def config(self):
		"""
		Get/Display config.
		
		The config property returns a propx object containing the 
		configuration.
		
		Call this property as a method to receive the actual config dict,
		or use the propdict properties to display config nicely in the
		terminal.
		
		>>> from trix.data.database import *
		>>> db = Database(SAMPLE_CONFIG_DICT)
		>>> db.config.display()
		{
		  "sql": {
		    "create": [
		      "create table foo ('bar','baz')",
		      "insert into 'foo' values ('barnone', 'baz00kas')"
		    ],
		    "op": {
		      "getfoo": "select * from foo"
		    }
		  }
		}
		>>>
		
		SEE ALSO:
		>>> from trix.util.propx.propdict import *
		>>> help(propdict)
		
		"""
		return trix.propx(self.__config)
	
	
	#	
	#	
	# CON
	#	
	#	
	@property
	def con (self):
		"""
		Return the DB connection object.
		"""
		return self.__con
	
	
	#	
	#	
	# MASTER
	#	
	#	
	@property
	def master(self):
		"""
		The master property returns a propx object containing information
		on objects in this database.
		
		Call the property as a function to return the actual list, or 
		use the propx features to display the information.
		
		EXAMPLE
		>>> from trix.data.database import *
		>>> db = Database("~/foo.json")
		>>> db.open()
		>>> db.master.display()
		[
		  [
		    "table",
		    "foo",
		    "foo",
		    2,
		    "CREATE TABLE foo ('bar','baz')"
		  ],
		  [
		    "table",
		    "__meta",
		    "__meta",
		    3,
		    "CREATE TABLE __meta (k,v)"
		  ]
		]
		>>> 
		
		SEE ALSO:
		>>> from trix.util.propx.proplist import *
		>>> help(proplist)
		
		"""
		
		try:
			con = self.con
			with con:
				cur = con.cursor()
				cur.execute("SELECT * FROM sqlite_master")
				return trix.propx(cur.fetchall())
		except BaseException as ex:
			raise type(ex)('err-master-fail', xdata(active=self.active,
					en="If `db.active` is False, the database is not open."
				)
			)
	
	#	
	#	
	# MOD
	#	
	#	
	@property
	def mod (self):
		"""
		Return the DB module object.
		"""
		return self.__mod
	
	
	#	
	#	
	# MODNAME
	#	
	#	
	@property
	def modname (self):
		"""Return the DB module name."""
		return self.__modname
	
	
	#	
	#	
	# PATH
	#	
	#	
	@property
	def path (self):
		"""
		Return the database file path. For some DBMS, it may be None. 
		"""
		return self.__path
	
	
	#	
	#	
	# SQL
	#	
	#	
	@property
	def sql(self):
		"""
		Return the full config sql dict wrapped in a propx.
		
		Call this property as a method to return the resulting dict, or
		use the propx features to display data nicely in the terminal.
		
		EXAMPLE
		>>> from trix.data.database import *
		>>> db = Database("~/foo.json")
		>>> db.open()
		>>> db.sql.display()
		{
		  "create": [
		    "create table foo ('bar','baz')",
		    "insert into 'foo' values ('barnone', 'baz00kas')"
		  ],
		  "op": {
		    "getfoo": "select * from foo"
		  }
		}
		>>>
		
		NOTE:
		The Database class allows specification of a text configuration 
		file (or dict) that as shown in the SAMPLE_CONFIG_DICT and in 
		the example code in the Database class comments, above.
		
		SEE ALSO:
		>>> from trix.util.propx.propdict import *
		>>> help(propdict)
		
		"""
		return trix.propx(self.__sql)
	
	
	#	
	#	
	# SOP
	#	
	#	
	@property
	def sop(self):
		"""
		Return the preconfigured SQL Operations dict `op`.
		"""
		return self.__op
	
	
	#	
	#
	# CAT
	#
	#	
	def cat(self, cat):
		"""
		Returns the named SQL query category as a list or a dict as 
		defined in configuration: Queries in the 'create' category are
		list; those in 'op' are dict.
		
		>>> db.cat('op')
		{'getfoo': 'select * from foo'}
		>>> 
		
		"""
		return self.__sql[cat]
	
	
	#
	#
	# CREATE
	#
	#	
	def create(self):
		"""
		Initialize the database.
		
		Initialize database using the "create" category of the sql dict
		defined in config. The "create" category is a list of statements
		intended to define tables and indices, and to populate tables
		if needed.
		
		NOTE:
		This method also creates a __meta table with one field whose
		value is set to the current __meta version, 3.
		
		"""
		cr = self.cat("create")
		if cr:
			self.qlist(cr)
		
		self.query("create table __meta (k,v)")
		self.query("insert into __meta values ('version', 3)")
		self.commit()
	
	
	#	
	#
	# OPEN
	#
	#	
	def open(self, **k):
		"""
		Open database using preconfigured arguments and optional kwargs.
		"""
		if self.active:
			raise Exception(
					'db-open-fail', self.xdata(reason='already-open',
					item=1
				))
		elif not self.mod:
			raise Exception('db-open-fail', self.xdata(
					reason='module-not-specified', item=2
				))
		
		try:
			self.__con = self.mod.connect(*self.__args, **k)
		except BaseException as ex:
			raise type(ex)('db-open-fail', self.xdata(
				python=str(ex), args=self.__args, kwargs=k, item=3
			))
		
		# auto-init
		if not self.__autoinit:
			self.__inited = True
		
		elif not self.__inited:
			try:
				cc = self.query('select v from __meta where k="version"')
				self.__inited = True if cc.fetchone() else False
			except Exception as ex:
				self.create()
				cc = self.query('select v from __meta where k="version"')
				self.__inited = True if cc.fetchone() else False
				if not self.__inited:
					raise Exception('db-autoinit-fail', self.xdata())
			finally:
				self.__autoinit = False
	
	
	#	
	#	
	# OPENS (open, return self)
	#	
	#	
	def opens(self, **k):
		"""Open database connection; return self."""
		self.open(**k)
		return self
	
	
	#	
	#	
	# CLOSE
	#	
	#	
	def close(self):
		"""Close the database connection."""
		try:
			if self.__con and self.active:
				self.__con.close()
		finally:
			self.__con = None
	
	
	#	
	# 
	# EXEC
	#	
	#
	def execute(self, *a):
		"""Execute a query with given args. Returns a cursor."""
		return self.__con.execute(*a)
	
	
	#	
	#	
	# EXECUTEMANY
	#	
	#	
	def executemany(self, *a):
		"""Execute multiple queries with given args. Returns a cursor."""
		return self.__con.executemany(*a)
	
	
	#	
	#	
	# CURSOR
	#	
	#	
	def cursor(self):
		"""Returns a cursor."""
		return self.__con.cursor()
	
	
	#	
	#	
	# COMMIT
	#	
	#	
	def commit(self):
		"""
		Commit a transaction.
		
		IMPORTANT:
		The calling code is responsible for commiting transactions.
		
		If insert queries are not showing up, make sure db.commit() is 
		being called at all the appropriate places.
		
		"""
		self.__con.commit()
	
	
	#	
	#	
	# ROLLBACK
	#	
	#	
	def rollback(self):
		"""
		Rollback a transaction.
		"""
		self.__con.rollback()
	
	
	#	
	#	
	# ERROR ROLLBACK
	#	
	#	
	def __rollback(self):
		#
		#Used only in except clauses, in case the database was not open
		#(or some other error not related to the sql itself). This keeps
		#the wrong error from being raised.
		#
		try:
			self.rollback()
		except:
			pass
	
	
	# ----------------------------------------------------------------
	#
	#
	# OPERATIONS
	#  - handle queries defined in the 'sql' config.
	#
	#
	# ----------------------------------------------------------------
	
	#	
	#	
	# QUERY
	#	
	#	
	def query(self, sql, *a):
		"""
		Execute query with given args; Rollback on error.
		
		NOTE:
		On success, the calling code must commit (if/when appropriate).
		
		"""
		try:
			return self.execute(sql, *a)
		except BaseException as ex:
			if not self.active:
				raise type(ex)('db-inactive', self.xdata())
			self.__rollback()
			raise type(ex)('db-query-err', self.xdata(sql=sql))
	
	
	#	
	#	
	# Q-MANY
	#	
	#	
	def qmany(self, sql, *a):
		"""
		Just like `self.query`, but uses executemany.
		
		NOTE:
		On success, the calling code must commit (if/when appropriate).
		"""
		try:
			return self.executemany(sql, *a)
		except BaseException as ex:
			if not self.active:
				raise type(ex)('db-inactive', self.xdata())
			self.__rollback()
			raise type(ex)('db-query-err', self.xdata(sql=sql, args=a))
	
	
	#	
	#	
	# Q-LIST
	#	
	#	
	def qlist(self, queries, cursor=None):
		"""
		Execute list of query strings. On error, rollback.
		
		NOTE:
		On success, the calling code must commit (if/when appropriate).
		"""
		try:
			cc = cursor if cursor else self.cursor()
			qn=0
			for sql in queries:
				cc.execute(sql)
				qn += 1
			return cc
		except BaseException as ex:
			self.__rollback()
			raise type(ex)('db-query-err', self.xdata(sql=sql, qitem=qn,
				qlist=queries
			))
	
	
	#	
	#	
	# OPQ - Op Query
	#	
	#	
	def opq (self, qname, *a):
		"""
		Pass query name as defined in config in the 'op' section, and 
		any arguments required by the query; Executes the query and 
		returns a cursor.
		
		NOTE:
		On success, your code must do the commit (if/when appropriate).
		"""
		return self.query(self.__op[qname], *a)
	
	
	#	
	#	
	# OPS - Op Query List
	#	
	#	
	def ops (self, qname, *a):
		"""
		Execute a list of queries specified by an op name. This only 
		applies to op values that are lists of queries to execute.
		On error, rollback.
		
		NOTE:
		On success, your code must do the commit (if/when appropriate).
		
		"""
		#
		# Transaction opening is automatic so if there's an exception,
		# self.query() will do the rollback for all.
		#
		# I guess it's best to stick to the principle that the caller 
		# always does the commit. I need to document that and post some
		# reminders in comments everywhere it's necessary.
		#
		try:
			xq = len(self.__op[qname])
			xa = len(a)
			xsql = self.__op[qname]
			for i in range(0, xq):
				sql = xsql[i]
				if (i<xa) and (a[i]):
					self.query(sql, a[i])
				else:
					self.query(sql)
					
		except BaseException as ex:
			raise type(ex)(self.xdata(qname=qname, args=a))
	
	
	#	
	#	
	# XDATA
	#	
	#	
	def xdata(self, **k):
		"""
		Return a dict containing debug information.
		
		This method is called in the event of any exception. It packages
		relevant data into the exception to assist with the debugging of
		problems in code or queries.
		
		"""
		d = dict(dbmodule=self.__modname, dbactive=self.active)
		if self.path:
			d['path'] = self.path
		return xdata(d, **k)
	
	
	#	
	#	
	# FETCHN
	#	
	#	
	@classmethod
	def fetchn(cls, cursor, n=None):
		"""
		This classmethod returns a list of `n` number of rows from 
		`cursor`, starting at its current position. If value is None, 
		all rows are returned.
		"""
		if n == None:
			return cursor.fetchall()
		else:
			r = []
			while n > 0:
				r.append(cursor.fetchone())
			return r
	
	
	#	
	#	
	# CDESC
	#	
	#	
	def cdesc(self, c):
		"""
		Returns a description of the cursor; names of fields selected.
		"""
		desc = map(lambda x: x[0], c.description)
		return list(desc)
	
