
from .. import *
import os

class Terminal(BaseClass):
	
	def __init__(self, **k):
		"""
		Pass optional keyword arguments for a default size as a list of 
		two integers. This is not usually necessary unless you're on a 
		system that does not support one of the methods (defined in the 
		`size` method) for detecting the terminal width.
		"""
		BaseClass.__init__(self, **k)
		
		#
		# This is set on the first call to `Terminal.size`.
		# It will be one of:
		#  * _os_terminal_size
		#  * _os_terminal_size
		#
		self.__size_fn = None
		
		# A default, which is stupid, but I guess necessary.
		self.default_hw_list = k.get('default_hw', [24,80])
		self.debugging       = k.get("debugging", True)
		self.logging         = []
	
	
	##
	## DEBUGGING
	##
	def debug(self):
		"""Call as a function. Returns propdict."""
		return trix.propx({
			"__size_fn"       : self.__size_fn,
			"default_hw_list" : self.default_hw_list,
			"debugging"       : self.debugging,
			"logging"         : self.self.logging,
			"x"               : "The End."
		})
		
	
	#
	#
	# TERMINAL SIZE
	#
	#
	def size(self):
		#
		# If the self.__size_fn has already been set, use it.
		#
		try:
			return self.__size_fn()
		except BaseException as ex:
			#print ("SIZE Passed")
			pass
			#if self.debugging:
			#	raise
		
		#
		# If not yet set, call the most recent methods first, progressing
		# to methods used in older versions of python.
		#
		
		# try the most recent, the os.terminal_size method
		
		# THIS ONE WORKS
		try:
			return self._os_terminal_size()
		except BaseException as ex:
			if self.debugging:
				raise
		
		# try the shell.terminal_size() method
		try:
			return self._sh_terminal_size()
		except BaseException as ex:
			if self.debugging:
				raise
		
		# try the subprocess.terminal_size() method
		try:
			return self._sp_terminal_size()
		except BaseException as ex:
			if self.debugging:
				raise
		
		#
		# fallback on caller-settable default; k=default_hw
		#
		if self.default_hw_list:
			return self.default_hw_list
	
	
	
	# ----------------------------------------------------------------
	
	
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
	
	def _os__tsize(self):
		try:
			return list(self.__size_fn())
		except BaseException as ex:
			if self.debugging:
				raise
			
	
	
	# ----------------------------------------------------------------
	
	
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
	    
