#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import curses, time
#from curses import wrapper


class BaseScreen(object):
	"""Basic screen control via curses."""
	
	def __init__(self, *a, **k):
		try:
			self.__a
		except:
			self.__a = a
			self.__k = k
	
	
	def main(self, stdscr):
		try:
			self.__ss
			raise Exception("Main may be called only once.")
		except:
			self.__ss = stdscr
			self.run()
	
	
	def start(self):
		"""
		Call this to start running the screen.
		"""
		curses.wrapper(self.main)
	
	
	def run(self):
		"""
		This is the actual running of a started screen. It calls 
		`self.prepare()` then loops calling `self.io()`.
		"""
		self.prepare()
		self.__running = True
		try:
			while self.__running:
				self.io()
				time.sleep(0.1)
		except KeyboardInterrupt:
			pass
	
	
	def prepare(self):
		"""
		Override this to handle any preparation for operation of this 
		object.
		"""
		self.__ss.clear()
		print ("Screen started. Ctrl-c to exit.\r")
	
	
	def io(self):
		"""Override this to do something frequently."""
		pass
	
	
	def stop(self):
		"""Sets private self.__running variable to False."""
		self.__running = False




class Screen(BaseScreen):
	"""
	This class should extend BaseScreen with features for the handling
	of screen display/updates.
	"""
	pass

