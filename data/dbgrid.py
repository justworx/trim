#
# Copyright 2019-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from trix import *
from .database import *
from ..util.propx.proplist import *   # trix, propgrid, et al
import sqlite3, re, time
import atexit


class DBGrid(Database):
	"""
	Query a set of named, in-memory sqlite3 tables.
	
	EXAMPLE:
	>>>
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
	
	"""
	
	PATHLIST = []
	
	#
	#
	# INIT
	#
	#
	def __init__(self, **k):
		"""
		Create a database for manipulation of grids
		
		A `grid` is a list containing a set of lists of equal length.
		
		NOTES:
		 * DBGrid database files are always sqlite3.
		 * DBGrid database files are always temporary. Their names are
		   always auto-generated.
		 * The temporary database files are stored in DEF_CACHE, 
		   and are deleted by the class destructor.
		 
		USAGE NOTES:
		 * See the `add()` method for details on how to create tables.
		 * It seems that once you've closed a DBGrid, you can't open it 
		   again. I'm not sure if that's a bug or a feature. It doesn't
		   seem to conflict with the purpose of this class.
		
		 
		"""
		
		self.__cache = trix.path(DEF_CACHE).path
		
		#
		# Generate time-based filename in DEF_CACHE.
		#
		f='%s/dbgrid/dbgrid.%s.sqlite3' % (
				DEF_CACHE, str(time.time())
			)
		self.__fpath = f
		
		
		#
		# List of files to delete on exit.
		#
		type(self).PATHLIST.append(self.__fpath)
		
		
		#
		# Initialize the base class, Database.
		#
		Database.__init__(self, self.__fpath)
		
		#
		# Set up a class value containing a regex that validates
		# and (if necessary) deletes characters sqlite3 can't use
		# as column names.
		#
		self.__T = type(self)
		self.__T.re_columns = re.compile("^[_A-Za-z0-9]*$")
	
		
		#
		# Open the database immediately (unless autoopen=False).
		# I can't imagine that ever being the case, but what do
		# I know?
		#
		self.__autoopen = k.get('autoopen', True)
		if self.__autoopen:
			self.open()
	
	
	#
	#
	# DEL
	#
	#
	def __del__(self):
		"""
		Delete the temp file.
		"""
		try:
			self.close()
		except BaseException as ex:
			print ("DBGrid __del__ Error: " + ex)
	
	
	#
	#
	# CALL METHOD - Returns result of `self.execute`.
	#
	#
	def __call__(self, sql, *a):
		"""
		Execute an sql query on the grid data.
		
		 * Pack the data (and hopefully headers) into a DBGrid.
		 * In the event of an error, the connection is rolled back.
		
		>>>
		>>> from trix.data.dbgrid import *
		>>> 
		>>> # make a dbgrid
		>>> t = DBGrid()
		>>> 
		>>> #
		>>> # Add the tablename `lr`, the columns (left and right),
		>>> # and the data.
		>>> #
		>>> t.add("lr", [ ['left', 'right'], [1,2], [3,4] ])
		>>> 
		>>> #
		>>> pl = t("select * from lr")
		>>> pl()
		[(1, 2), (3, 4)]
		>>> 
		>>> #
		>>> t('insert into lr values (5,6)')
		>>> t.commit()
		>>> 
		>>> #
		>>> t("select * from lr order by left").grid()
		1  2
		3  4
		5  6
		>>> 
				
		"""
		try:
			c = self.cur.execute(sql, *a)
			try:
				ca = c.fetchall()
				if ca:
					#print ('debug ca', ca)
					
					cal = list(ca)
					#print ('debug cal', cal)
					
					# prepend column names
					cal.insert(0, self.cols)
					#print ('debug cal.insert', cal)
					
					return trix.propx(cal)
			except:
				raise
			
		except sqlite3.OperationalError as ex:
			#
			# If there was an error, rollback and rethrow the exception.
			#
			self.con.rollback()
			raise type(ex)(xdata(
					sql=sql, a=a
				)
			)
	
	
	
	@property
	def fpath(self):
		"""Return the file path to this sqlite3 file."""
		return self.__fpath
	
	
	
	@property
	def tables(self):
		"""
		Return a propx object containing the names of tables added to
		this object.
		
		If you want a straight python list, call this property as though
		it were a method.
		
		Otherwise, all the proplist features are available.
		
		EXAMPLE:
		>>> from trix.data.dbgrid import *
		>>> g = DBGrid()
		>>> g.add('four', [[1,2], [3,4]], columns=['left','right'])
		>>> g("select * from four").grid()
		left  right
		1     2    
		3     4 
		>>>   
		>>> g.tables()
		['four']
		
		
		EXAMPLE 2: 
		#
		# All on one line (sort of).
		#
		trix.npath().list.dbgrid('lgrid').x(
			'select * from lgrid order by size').grid()

		"""
		
		i = 0
		tableList = []
		while True:
			try:
				tableList.append(self.master()[i][1])
				i+=1
			except:
				pass
			
			return trix.propx(tableList)
	
	
	
	#
	#
	# ADD - It converts the grid to a real table.
	#
	#
	def add(self, table_name, grid, columns=None):
		"""
		Add a table to this dbgrid.
		
		To add a table, pass the following arguments to the `DBGrid.add`
		method:
		
		 * table_name: a string value, the name of the table to add 
		   into this dbgrid.
		   
				>>>
				>>> dg = DBGrid()
				>>>
				
		 * grid: a list of lists.
				
				>>>
				>>> #
				>>> # Here, there is no `columns` argument, so the
				>>> # first list is taken to be the column headings.
				>>> #
				>>> dg.add("oh_my_grid", [ ['left','right'], [1,2], [3,4] ])
				>>> 
		 	
				OR
		 	
				If you pass a `grid` with `columns` specified, do not pass 
				the column names in the list of lists.
				
				>>> #
				>>> # Here, there IS a third (`columns`) argument, so the
				>>> # column names should NOT be prepended to the second
				>>> # argument's list.
				>>> #
				>>> dg.add("oh_my_grid", [[1,2],[3,4]], columns)
				>>> 
		
		REMEMBER: When you pass your grid without a `columns` specifier,
		          the first list in the grid is taken as a list of column
		          names.
		
		>>>
		>>> from trix.data.dbgrid import *
		>>> t = DBGrid()
		>>> t.add('four', [[1,2],[3,4]], columns=["left","right"])
		>>> t('select * from four')
		<trix/propgrid list len=2>
		>>> t('select * from four').grid()
		left  right
		1     2
		3     4
		
		"""
		
		#
		# If a columns value was specified, it will be set directly
		# into the `cols` value, and rows will be separated into 
		# the `rows` variable.
		#
		if columns:
			cols = columns
			rows = grid
		
		#
		# If a columns value is NOT specified, the first list in the
		# grid is taken to be the heading, providing column names.
		#
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
				if self.__T.re_columns.match(c):
					valid_chars.append(c)
			if valid_chars:
				valid_cols.append("".join(valid_chars))
			else:
				valid_cols.append("COLUMN_%i" % i)
				i+=1
		
		#
		# Set the validated columns in `self.cols`.
		#
		self.cols = cols = valid_cols
		
		#
		# Create a table in the temporary database.
		#
		sql = "create table %s (%s)" % (table_name, ','.join(self.cols))
		try:
			self.con.execute(sql)
		except:
			raise Exception("dbgrid.add", xdata(
					columns=self.cols, row_ct=len(rows), sql=sql, table=table_name
				))
		
		# get the cursor
		self.cur = self.con.cursor()
		
		# populate database
		qms = ",".join("?"*len(self.cols))
		sql = "insert into %s values (%s)" % (table_name, qms)
		self.cur.executemany(sql, iter(rows))
		
		return self
	
	
	
	#
	#
	# EXECUTE - returns a cursor
	#
	#
	def execute(self, sql, *a):
		"""
		Execute an sql query on the grid data. Returns an sqlite3 cursor.
		In the event of an error, the connection is rolled back.
		
		Returns a cursor.
		
		"""
		try:
			return Database.execute(self, sql, *a)
		
		except sqlite3.OperationalError as ex:
			#
			# If there was an error, rollback and rethrow the exception.
			#
			self.con.rollback()
			raise type(ex)(xdata(
					sql=sql, a=a, cols=self.cols, tables=self.__T
				)
			)
	
	
	
	def x(self, *a, **k):
		"""
		Execute an sql statement returning any selected values.
		"""
		return trix.propx(self.__call__(*a, **k))
	
	
	
	def close(self):
		try:
			Database.close(self)
		except BaseException as ex:
			pass
		try:
			trix.path(self.fpath).wrapper().remove()
		except BaseException as ex:
			pass
	
	
	
	
	# AT EXIT
	@classmethod
	def _at_exit(cls):
		for path in cls.PATHLIST:
			w = trix.path(path).wrapper()
			try:
				w.close()
				w.remove()
			except:
				try:
					w.remove()
				except:
					pass


#
# Close and clean up temp files when program terminates.
#
atexit.register(DBGrid._at_exit)

