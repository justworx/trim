#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ..propx import *
import sqlite3


class DBGrid(object):
	"""Add and query a set of named, in-memory sqlite3 tables."""
	
	def __init__(self, **k):
		"""
		Initialize grid database.
		"""
		self.con = sqlite3.connect(":memory:")
		self.__T = []
		
		# experimental
		for table in k:
			self.add(table, k[table])
	
	
	def __call__(self, sql=None, *a, **k):
		"""
		Shortcut for `select()`. Returns a DataGrid containing results.
		"""
		return self.select(sql, *a, **k)
	
	
	@property
	def tables(self):
		"""
		Return the names of tables that have been added to this dbgrid.
		"""
		return list(self.__T)
	
	
	def add(self, table_name, grid, columns=None):
		"""
		Pass a table name and a grid (list of lists of equal length). As
		with DataGrid, column names must be either prepended to the grid
		or specified as a list using the optional `columns` argument.
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
		
		self.cols = columns
		
		# create memory database
		sql = "create table %s (%s)" % (table_name, ','.join(cols))
		try:
			self.con.execute(sql)
		except:
			raise Exception("dbgrid.add", xdata(
					columns=cols, row_ct=len(rows), sql=sql, table=table_name
				))
		
		# get the cursor
		cur = self.cur = self.con.cursor()
		
		# populate database
		qms = ",".join("?"*len(cols))
		sql = "insert into %s values (%s)" % (table_name, qms)
		cur.executemany(sql, iter(rows))
		
		# add tablename
		self.__T.append(table_name)
	
	
	def rmv(self, tableName):
		"""
		Remove table `tableName` from the temporary database.
		
		NOTE: Do not use "DROP TABLE <tablename>" to remove tables or
		      the table list will not be updated to reflect the removed
		      table.
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
			raise type(ex)(xdata(sql=sql))
	
	
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
		Execute select query `sql`.	Returns a proplist loaded with the
		query result. A column name list is prepended by default, unless
		you pass the kwarg header=False.
		
		NOTE: Passing an statement that does not select data will return
		      a proplist containing an empty list.
		"""
		newgrid = self.query(sql, *a)
		if k.get('h', k.get('header', True)):
			r = [self.get_column_names()]
			r.extend(newgrid)
			return proplist(r)
		else:
			return proplist(newgrid)
	
	
	def get_column_names(self):
		"""Returns the list of columns from the most recent query."""
		try:
			colnames = []
			for x in self.cur.description:
				colnames.append(x[0])
			return colnames
		except:
			raise
