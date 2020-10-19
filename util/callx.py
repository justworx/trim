#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *
import shlex


class callx(BaseClass):
	"""
	Creates and handles Popen calls.
	"""
	
	#
	#
	# C-LINE - Runs a trix command-line handler.
	#
	#
	@classmethod
	def cline(cls, cmd, **k):
		"""
		Pass a cline handler name and args, plus optional kwargs. Returns
		a callx object.
		
		The `cline` handler modules are defined in the `trix.app.cline`
		subpackage. See the help for each module to learn more about its
		use.

		"""
		try:
			a = shlex.split(cmd)
		except:
			a = cmd
		
		args = [sys.executable, '-m', trix.innerpath()]
		args.extend(a)
		
		return cls(args, **k)
	
	
	#
	#
	# INIT
	#
	#
	def __init__(self, cmd=None, **k):
		"""
		Make a system call and return the response.
		
		Pass argument `cmd`, which may be one of the following:
		 * a string containing a command line, to be split with shlex
		 * a list containing the exact arguments to pass to popen
		
		Keyword Argument Options:
		 * encoding, errors, mode, max_size
		
		ALTERNATELY:
		Call a command line handler (cline). Pass a keyword argument 
		specifying a cline command. Command line handlers are available 
		for review in the `trix.app.cline` module.
		
		IN RESULTS:
		  * The `callx.reader` method returns a `Buffer` object containing 
		    the text generated by the system call. The Buffer class is
		    based on `trix.util.stream.Stream`, and provides methods for
		    reading returned data.
		  * The `callx.text` property returns a `propstr` object which
		    contains the full text.
		  * The `callx.data` property returns
		
		EXAMPLE 1:
		>>> #
		>>> # Gather text describing currently running processes.
		>>> #
		>>>  
		>>> from trix.util.callx import *
		>>> cx.text.output()
		  PID TTY          TIME CMD
		 3313 pts/2    00:00:00 bash
		 5092 pts/2    00:00:00 python3
		 5094 pts/2    00:00:00 ps
		>>> 
		>>> cx.text.lines()
		['{', '  "version": 0.0,', '  "copyright": "Copyright (C) 2018-2020 justworx",', '  "license": "agpl-3.0"', '}']
		>>>		
		
		EXAMPLE 2: `callx.data`
		>>> #
		>>> # Call a command line handler (cline).
		>>> #
		>>>  
		>>> from trix.util.callx import *
		>>> ver = trix.callx(cline='version')
		>>> ver.data.display()
		{
		  "version": 0.0,
		  "copyright": "Copyright (C) 2018-2020 justworx",
		  "license": "agpl-3.0"
		}
		>>> 
		>>> ver.data()
		{'version': 0.0, 'copyright': 'Copyright (C) 2018-2020 justworx', 'license': 'agpl-3.0'}
		>>> 
		
		SEE ALSO:
		>>> from trix.app.cline import *
		>>> help(callx)
		>>> 
		>>> 
		
		"""
		BaseClass.__init__(self, [cmd], **k)
		
		# pop kwargs meant for reader
		self.__rk = trix.kpop(k, "encoding errors mode max_size")
		self.__rk.setdefault('encoding', DEF_ENCODE)
		
		# remaining kwargs must be for Popen.
		self.__k = k
		
		# get the command-line arguments
		if cmd:
			try:
				args = shlex.split(cmd)
			except:
				args = cmd
		
		else:
			# if command line args are None, check for "cline" kwarg.
			if 'cline' in k:
				args = [sys.executable, '-m', trix.innerpath()]
				try:
					a = shlex.split(k.get('cline'))
				except:
					a = k.get('cline')
				args.extend(a)
				
				#
				# Get rid of the cline kwarg so it can't interfere with any
				# other method calls.
				#
				trix.kpop(k, 'cline')
		
		# Finally, set self.__a to the generated arg list	
		try:
			self.__a = args
		except Exception as ex:
			en = "Command line argument or cline keyword argument required."
			raise type(ex)(xdata(
					error="cline-args-required", en=en
				)
			)
	
	
	#
	#
	# X
	#
	#
	@property
	def x(self):
		"""
		Returns the `subprocess.Popen` object.
		"""
		try:
			return self.__x
		except:
			self.__call__() # self.__call__() sets `self.__x`
			return self.__x
	
	
	#
	#
	# DATA
	#
	#
	@property
	def data(self):
		"""
		Returns a propx object. Treat `data` like a function, or explore
		the extra propx features.
		
		"""
		try:
			return self.__data
		except:
			# If possible, convert text to json data.
			try:
				#
				# If the text does parse to json, we need to set self.__data
				# to the appropriate propbase subclass by calling propx().
				#
				data = trix.jparse(self.text())
				self.__data = trix.propx(data)
				return self.__data
			except:
				pass
			
			#
			#
			# TO DO:
			#  - There may be other ways to convert text to data.
			#    If so, try them here.
			#
			#
			
			# If nothing above works, just set the text as the data.
			self.__data = trix.propx(self.__text)
			return self.__data
	
	
	#
	#
	# TEXT
	#
	#
	@property
	def text(self):
		"""
		Returns a propx object covering the text. Call this property like
		a function to return the text received from the called process.
		
		>>>  
		>>> from trix.util.callx import *
		>>>
		>>> callx('ps').text.display()
		"  PID TTY          TIME CMD\n 3405 pts/2    00:00:00 bash\n 
		4094 pts/2    00:00:00 python3\n 4134 pts/2    00:00:00 ps\n"
		>>>
		>>> trix.callx('ps').list()
		>>>
		
		"""
		try:
			return trix.propx(self.__text)
		except:
			r = self.reader() # no args here; the reader property does them.
			r.seek(0)
			self.__text = r.read()
			return trix.propx(self.__text)
	
	
	#
	#
	# READER
	#
	#
	def reader(self):
		"""
		Get a reader for the buffered results.
		"""
		try:
			return self.__reader
		except:
			self.__buffer = trix.ncreate(
				"util.stream.buffer.Buffer", 
				self.x.stdout.read(), **self.__rk
			)
			self.__reader = self.__buffer.reader()
			return self.__reader

