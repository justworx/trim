#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ..util.propx.proplist import *   # trix, propgrid, et al
import sqlite3, re


class DBGrid(object):
	"""
	Add and query a set of named, in-memory sqlite3 tables.
	
	EXAMPLE:
	>>> from trix.data.dbgrid import *
	>>> g = DBGrid()
	>>> g.add('four', [[1,2], [3,4]], columns=['left','right'])
	>>> g("select * from four").grid()
	>>>
	
	EXAMPLE 2:
	>>>
	>>> import trix
	>>> g = trix.path("~/trix").list.propgrid.dbgrid('lg')
	>>>
	
	UNDER CONSTRUCTION!
	This class is under construction. I can't leave it out of  
	the trix package because it's too useful for sorting grids.
	Meanwhile, development continues.
	
	"""
	
	def __init__(self, **k):
		"""
		Initialize grid database. See the `add()` method for details on
		how to create tables.
		"""
		
		type(self).re_columns = re.compile("^[_A-Za-z0-9]*$")
		
		self.con = sqlite3.connect(":memory:")
		
		# maintain a table list
		self.__T = []
		
	
	#
	# CALL
	#
	def __call__(self, sql, *a, **k):
		"""
		WARNING:
		THIS CURRENTLY ONLY WORKS FOR SELECT STATEMENTS!
		Running updates, deletions, etc... will cause a failure.
		I'm working on a plan to make this more flexible. We'll see 
		how that goes.
		
		For now, use `DBGrid.execute()` to update/delete/etc...
		
		Shortcut for `select()`. Returns a DataGrid containing results
		of valid sqlite3 queries.
		"""
		try:
			return self.select(sql, *a, **k)
		except BaseException as ex:
			raise type(ex)("dbgrid-select-error", xdata(
						sql=sql, a=a, k=k
					)
				)
	
	@property
	def tables(self):
		"""
		Return the names of tables that have been added to this dbgrid.
		"""
		return list(self.__T)
	
	
	
	
	def add(self, table_name, grid, columns=None):
		"""
		Pass a table name and a grid (list of lists of equal length).
		Column names must be either prepended to the grid or specified 
		as a list using the optional `columns` argument.
		
		>>>
		>>> from trix.data.dbgrid import *
		>>> t = DBGrid()
		>>> t.add('four', [[1,2],[3,4]], columns=["L","R"])
		>>> t('select * from four')
		<trix/propgrid list len=2>
		>>> t('select * from four').grid()
		L  R
		1  2
		3  4
		>>>
		>>> t.execute('delete from four where R = "4"')
		>>> t.execute('delete from four where R = "4"')
		>>>
		
		"""
		
		#
		# SET UP THE INITIAL DATABASE IN MEMORY
		#  - Copy `grid` (a list of lists) into a :memory: database.
		#    This init method
		#
		
		# get setup values
		if columns:
			cols = columns
			rows = grid
		else:
			cols = grid[0]
			rows = grid[1:]
		
		#
		# generate list of valid sqlite3 column names from `columns`
		#
		i = 0
		valid_cols = []
		for columnName in cols:
			valid_chars = []
			for c in columnName:
				if type(self).re_columns.match(c):
					valid_chars.append(c)
			if valid_chars:
				valid_cols.append("".join(valid_chars))
			else:
				valid_cols.append("COLUMN_%i" % i)
				i+=1
		
		self.cols = cols = valid_cols
		
		#
		# create memory database
		#
		sql = "create table %s (%s)" % (table_name, ','.join(cols))
		try:
			self.con.execute(sql)
		except:
			raise Exception("dbgrid.add", xdata(
					columns=cols, row_ct=len(rows), sql=sql, table=table_name
				))
		
		# get the cursor
		self.cur = self.con.cursor()
		
		# populate database
		qms = ",".join("?"*len(cols))
		sql = "insert into %s values (%s)" % (table_name, qms)
		self.cur.executemany(sql, iter(rows))
		
		# add tablename
		self.__T.append(table_name)
	
	
	
	
	def remove(self, tableName):
		"""
		Remove table `tableName` from the temporary database.
		
		WARNING: Do not use "DROP TABLE <tablename>" to remove tables 
		         or the table list will not be updated to reflect the 
		         removed table.
		"""
		if tablename in self.__T:
			self.execute('drop table %s'%tablename)
			del(self.T[tablename]) 
	
	
	
	
	def execute(self, sql, *a):
		"""
		Execute an sql query on the grid data. Returns an sqlite3 cursor.
		"""
		try:
			return self.cur.execute(sql, *a)
		except sqlite3.OperationalError as ex:
			raise type(ex)(xdata(sql=sql, a=a, cols=self.cols, 
					tables=self.__T
				)
			)
	
	
	
	
	def query(self, sql, *a):
		"""
		Execute an sql query on the grid data. Returns a list of lists 
		(grid) matching the query result.
		"""
		cc = self.execute(sql, *a)
		if cc:
			return cc.fetchall()
	
	
	
	
	def select(self, sql, *a, **k):
		"""
		THIS CURRENTLY ONLY WORKS FOR SELECT STATEMENTS!
		See: __call__(), above.
		
		Execute select query `sql`.	Returns a propgrid loaded with the
		query result. A column name list is prepended by default, unless
		you pass the kwarg header=False.
		
		NOTE: Passing an statement that does not select data will return
		      a propgrid containing an empty list.
		"""
		newgrid = self.query(sql, *a)
		if k.get('h', k.get('header', True)):
			try:
				r = [self.get_column_names()]
				r.extend(newgrid)
				return propgrid(r)
			except BaseException as ex:
				print ("TEMP DEBUG: %s" % str(ex))
				return []
		else:
			return propgrid(newgrid)
	
	
	
	
	def get_column_names(self):
		"""Returns the list of columns from the most recent query."""
		try:
			colnames = []
			for x in self.cur.description:
				colnames.append(x[0])
			return colnames
		except:
			raise
	
	#
	# ALIASES
	#  - Helpful for use in lambda callbacks.
	#  - Note that the alias for select is the `__call__()` method
	#
	q = query
	tt = tables
	rm = remove
	ex = execute
