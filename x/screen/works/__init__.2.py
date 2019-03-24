#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from ... import * # trix
from ...util.wrap import * # trix
import curses


class BaseScreen(object):
	"""
	*** EXPERIMENTAL - EXPLORATORY - UNDER CONSTRUCTION ***
	
	Basic screen control via curses. Create a BaseScreen object (or
	subclass) then call the `start()` method to prepare and display
	the screen and then begin looping through calls to `io()`.
	
	```
	s = Screen()
	s.start()
	
	```
	
	The stop method may be called to end the io loop programatically.
	
	
	After stopping, the `cleanup()` method is called. Override the
	`prepare()` and `cleanup()` methods as necessary.
	"""
	
	def __init__(self, *a, **k):
		try:
			self.__a
		except:
			self.__a = a
			self.__k = k
			
	
	@property
	def ss(self):
		"""Return stdscr, or None if `start()` hasn't been called."""
		try:
			return self.__ss
		except AttributeError as ex:
			raise type(ex)(xdata(error="err-unstarted-screen",
					reason="screen-not-started", suggest="call-screen.start",
					en="Call `Screen.start()` before using Screen object."
				))
	
	
	def start(self):
		"""Call this to start running the screen."""
		curses.wrapper(self.__main)
	
	
	def prepare(self):
		"""
		Override this to handle any preparation for operation of this 
		object.
		"""
		print ("Screen started. Ctrl-c to exit.\r")
		self.__ss.clear()
	
	
	def run(self):
		"""
		Calls `self.prepare()` then loops calling `self.io()`. Finally,
		calls `self.cleanup()`.
		"""
		self.__run()
	
	
	def io(self):
		"""Override this to implement screen display."""
		pass
	
	
	def stop(self):
		"""Stop the `io()` event loop."""
		self.__running = True
	
	
	def cleanup(self):
		"""
		Apply any finishing touches. I'm not even sure this is necessary,
		but it feels symetrical, so I'm going to include it for now.
		"""
		pass
	
	
	
	#
	# PRIVATE METHODS
	#
	
	def __run(self):
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
		finally:
			self.__running = False
			self.cleanup()
	
	
	def __main(self, stdscr):
		#
		# I'm not sure this try block is really necessary anymore.
		#
		try:
			self.__ss
			#raise Exception("Main may be called only once.")
		except:
			self.__ss = stdscr
			self.run()





#
#
#  SCREEN
#   - Screen will implement some conveniences I want.
#
#
class Screen(BaseScreen):
	"""
	This class should extend BaseScreen with features for the handling
	of screen display/updates.
	"""
	
	def __init__(self, config=None, **k):
		"""Pass a config dict, updated by optional kwargs."""
		config = config or {}
		config.update(k)
		
























