#
# Copyright 2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import os


#
# Screen size to use if all else fails.
#
DEFAULT_HW = [24,80]

#
# Keeping this to False may save some processor cycles.
#
DEFAULT_DBG = False    


class Terminal(BaseClass):
	"""
	The `Terminal` class provides methods for determinining the terminal
	size and for clearing the screen.
	
	"""
	
	def __init__(self, **k):
		"""
		Returns the size of the current terminal as [height,width].
		
		Pass optional keyword arguments for a default size as a list of 
		two integers. This is not usually necessary unless you're on a 
		system that does not support one of the methods (defined in the 
		`size` method) for detecting the terminal width.
		
		Keyword argument "default_hw"=[24,80] sets the default, which will
		be returned by the `size` method if all other options for finding
		the terminal size fail.
		
		EXAMPLE
		>>> from trix.util.terminal import *
		>>> t = Terminal()
		>>> t.size()
		[25, 94]
		>>>
		
		"""
		BaseClass.__init__(self, **k)
		
		#
		# This is set on the first call to `Terminal.size`.
		# It will be one of:
		#  * _os_terminal_size (use os.terminal_size)
		#  * _sh_terminal_size (use shellx to determine terminal size)
		#  * _sp_terminal_size (use subprocess to determine terminal size)
		#
		self.__size_fn = None
		
		self.default_hw_list = k.get('default_hw', DEFAULT_HW)
		self.debugging       = k.get("debugging", DEFAULT_DBG)
		self.debughard       = k.get("debughard", False) # raise errors
		self.__log           = []
	
	
	#
	# DEBUG
	#
	@property
	def debug(self):
		"""
		Returns a `propdict` object containing debug information.
		
		EXAMPLE
		>>> from trix.util.terminal import *
		>>> t = Terminal(debugging=True)
		>>> t.size()
		>>> t.debug.display()
		
		NOTES:
		It's sometimes nice to have a bit of information on what's 
		happening inside. Pass the keyword argument `debugging=True` to 
		access debugging information.
		
		As for the "debughard" keyword argument, it's only for use in
		development. It might be commented out in future versions. It is
		*ONLY* for busting bugs, and will definitely prevent the object 
		from determining the screen size.
		
		"""
		return trix.propx({
			"__size_fn"       : str(self.__size_fn),
			"default_hw_list" : self.default_hw_list,
			"debugging"       : self.debugging,
			"debughard"       : self.debughard,
			"logging"         : self.__log
		})
		
	
	#
	#
	# TERMINAL SIZE
	#
	#
	def size(self):
		"""
		Return terminal height/width as a set.
		"""
		#
		# If the self.__size_fn has already been list, use it.
		#
		try:
			return self.__size_fn()
		except BaseException as ex:
			if self.debugging:
				self.__log.append({
					'method'   : 'size',
					'error'    : str(ex),
					'function' : str(self.__size_fn)
				})
			if self.debughard:
				raise
		
		#
		# If not yet set, call the most recent methods first, progressing
		# to methods used in older versions of python.
		#
		
		# Try the most recent, the os.terminal_size method.
		try:
			return self._os_terminal_size()
		except BaseException as ex:
			if self.debugging:
				self.__log.append({
					'method'   : 'size',
					'option'   : '_os_terminal_size',
					'error'    : str(ex),
					'function' : str(self.__size_fn)
				})
			if self.debughard:
				raise
		
		# Try the shell.terminal_size() method.
		try:
			return self._sh_terminal_size()
		except BaseException as ex:
			if self.debugging:
				self.__log.append({
					'method'   : 'size',
					'option'   : '_sh_terminal_size',
					'error'    : str(ex),
					'function' : str(self.__size_fn)
				})
			if self.debughard:
				raise
		
		# Try the subprocess.terminal_size() method.
		try:
			return self._sp_terminal_size()
		except BaseException as ex:
			if self.debugging:
				self.__log.append({
					'method'   : 'size',
					'option'   : '_sp_terminal_size',
					'error'    : str(ex),
					'function' : str(self.__size_fn)
				})
			if self.debughard:
				raise
		
		#
		# Fallback on caller-settable default.
		#
		if self.default_hw_list:
			return self.default_hw_list
	
	
	
	#
	#
	# OS_TERMINAL_SIZE
	#  - Set direct to __size_fn
	#  - This is the most recent terminal size function
	#
	def _os_terminal_size(self):
		"""
		Try using os module. If it works, set the self.__size_fn member
		to use `os.get_terminal_size` every time.
		
		On earlier systems, this may fail. In this case, older methods
		for determining terminal dimensions will be tried.
		
		"""
		try:
			#
			# This is the part that prepares the call to self.__size_fn,
			# which will be used in subsequent calls without having to pass
			# through this process of loading a trix.value, etc...
			#
			self.__size_fn = trix.value("os.get_terminal_size")
			self.__term_sz = self._os__tsize 
			
			# It goes through the whole process first time, but next time
			# self.__term_sz() will be called 
			return self.__term_sz()
		except BaseException as ex:
			self.__size_fn = None
			if self.debugging:
				raise
			if self.debughard:
				raise
	
	def _os__tsize(self):
		try:
			return list(self.__size_fn())
		except BaseException as ex:
			if self.debugging:
				raise
			if self.debughard:
				raise
	
	
	#
	#
	# SHELL_GET_TERMINAL_SIZE
	#  - Needs a secondary method, _sp__tsize
	#
	#
	def _sh_terminal_size(self):	
		try:
			self.__term_sz = trix.value("shutil.get_terminal_size")
			self.__size_fn = self._sh__tsize
			return list(self.__term_sz())
		except BaseException as ex:
			if self.debugging:
				raise
			if self.debughard:
				raise
			self.__size_fn = None
	
	def _sh__tsize(self):
		try:
			#
			# This is where we actually calculate the shutil method of
			# getting terminal sizes.
			#
			
			# The self.__term_sz function is "shutil.get_terminal_size".
			# Now self.__term_sz() needs to return
			fn = self.__term_sz()
			hw = fn(['stty', 'size'])
			hw.decode().split()
			return [int(hw[0]), int(hw[1])]
		except BaseException as ex:
			self.__size_fn = None
			if self.debugging:
				raise
			if self.debughard:
				raise
	
	
	#
	#
	# SUBPROCESS_GET_TERMINAL_SIZE
	#  - Needs a secondary method, _sp__tsize
	#
	#
	def _sp_terminal_size(self):
		try:
			self.__term_sz = trix.value("subprocess.check_output")
			self.__size_fn = self._sp__tsize
			return (self.__size_fn())
		except BaseException as ex:
			if self.debugging:
				raise
			if self.debughard:
				raise
	
	def _sp__tsize(self):
		fn = self.__term_sz
		hw = fn(['stty', 'size']).decode().split()
		return [int(hw[0]), int(hw[1])]
	
	
	
	
	#
	#
	# CLEAR
	#
	#
	def clear(self):
		"""Clear the terminal."""
		os.system('cls' if os.name=='nt' else 'clear')
	
	
	def cls(self):
		"""Clear the terminal. Alias for `clear()`."""
		self.clear()
	    
