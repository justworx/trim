#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .. import *
from curses import wrapper
from curses import panel
from curses import textpad
import curses


class Screen(object):
	"""
	Manages a curses window screen in a terminal window/tab.
	
	EXPERIMENTAL! UNDER CONSTRUCTION - LEARNING - JUST GETTING STARTED.
	"""
	
	def __init__(self, *a, **k):
		"""
		Prepare and start the screen.
		 - Store args in self.a
		 - Store kwargs in self.k
		 - use `wrapper` to call main, which loops calling `io()`.
		
		Note that self.s will be set to the stdscr as soon as wrapper
		calls `self.main()`.
		"""
		# store args/kwargs for use below
		self.__a = a     # args
		self.__k = k     # kwargs
		self.__ss = None # stdscr
		
		self.__sleep = k.get('sleep', 0.1)
	
	
	def a(self):
		return self.__a
	
	def k(self):
		return self.__k
	
	def ss(self):
		return self.__ss
	
	def sleep(self):
		return self.__sleep
	
	
	#
	# Start running the screen
	#
	def run(self):
		self.__ss = wrapper(self.main)
		return self.__ss
	
	
	def main(self, stdscr):
		"""
		Clear the screen, set self.s=stdscr, call prepare, then start 
		calling the `io()` loop method, with a short sleep between calls.
		"""
		#store stdscr, clear the screen, and call prepare
		self.__ss = stdscr
		
		# clear the screen
		stdscr.clear()
		
		# setup; draw initial content
		self.prepare()
		
		# once prepared, start calling io every `self.sleep` second
		sleep = self.sleep
		while True:
			self.io()
			time.sleep(sleep)
			
	
	
	def prepare(self):
		pass
	
	
	
	def io(self):
		
		self.s.addstr(1, 0, "LINES: %s\r" % str(curses.LINES))
		self.s.addstr(2, 0, "COLS : %s\n\r" % str(curses.COLS))
		
		self.s.refresh()
		
		curses.doupdate()
	
	
	
	
	
	def termsize(self):
		"""
		There must be a better way to get this info - I just haven't
		found it yet.
		"""
		return termsize()




