#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from .. import *
from ..util.terminfo import *
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
		self.a = a
		self.k = k
		
		wrapper(self.main)
	
	
	#
	# MAIN LOOP
	#
	def main(self, stdscr):
		"""
		Clear the screen, set self.s=stdscr, call prepare, then start 
		calling the `io()` loop method, with a short sleep between calls.
		"""
		#store stdscr, clear the screen, and call prepare
		self.s = stdscr
		stdscr.clear()
		self.prepare()
		
		# once prepared, start calling io every 1/10th second
		while True:
			self.io()
			time.sleep(0.1)
	
	
	def prepare(self):
		"""
		Override this method to prepare for handling the event "io" loop.
		"""
		# seems print works, but you gotta put in your own CR
		print("I need some better doc!")
		print("\r")
		
		# this didn't do what the doc said it would
		#curses.echo()
		
		# experimenting
		#self.s.addstr(self.s, 3, 3,"Hello, World!")
		#curses.doupdate()
	
	
	def io(self):
		pass
	
	
	
	
	
	def termsize(self):
		"""
		There must be a better way to get this info - I just haven't
		found it yet.
		"""
		return termsize()




