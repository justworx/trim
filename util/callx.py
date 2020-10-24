#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .tbase import * # trix, EncodingHelper, TBase
import shlex


class callx(TBase):
	"""
	Creates and handles Popen calls.
	
	The `callx` class may be called like a function, passing a command
	and any additional flags and arguments.
	
	Pass keyword cline="<cline-script> to trigger cline scripts.
	
	"""
	
	@classmethod
	def cline(cls, cmd, **k):
		"""
		Pass a cline handler name and any required arguments. 
		Returns a callx object.
		
		EXAMPLE
		>>> from trix.util.callx import *
		>>> callx.cline("version").text.output()
		{
			"version": 0.0,
		  "copyright": "Copyright (C) 2018-2020 justworx",
		  "license": "agpl-3.0"
		}
		>>>
		
		SEE ALSO:
		
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
		Makes a system call and returns the response.
		
		Pass argument `cmd`, which may be one of the following:
		 * a string containing a command line, to be split with shlex
		 * a list containing the exact arguments to pass to popen
		
		EXAMPLE
		>>> from trix.util.callx import *
		>>>
		>>> # create a callx object calling the unix "ps" program.
		>>> cx = callx('ps')
		>>>
		>>> cx.text()
		"  PID TTY          TIME CMD\n 3405 pts/2    00:00:00 bash\n 
		4094 pts/2    00:00:00 python3\n 4134 pts/2    00:00:00 ps\n"
		>>>
		>>> # view the results
		>>> cx.text.output()
		  PID TTY          TIME CMD
		 5242 pts/0    00:00:00 bash
		 5381 pts/0    00:00:00 python3
		 6241 pts/0    00:00:00 ps
		
		>>> cx.data()
		'  PID TTY          TIME CMD\n 5242 pts/0    00:00:00 bash\n 5381 
		pts/0    00:00:00 python3\n 6241 pts/0    00:00:00 ps <defunct>\n 
		6267 pts/0    00:00:00 ps\n'
		>>> 
		
		
		ALTERNATELY:
		Pass a keyword argument specifying a cline command. See below.
		
		"""
		TBase.__init__(self, cmd=None, **k)
		
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
			if 'cline' in self.k:
				args = [sys.executable, '-m', trix.innerpath()]
				try:
					a = shlex.split(self.k.get('cline'))
				except:
					a = self.k.get('cline')
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
			raise type(ex)(xdata(
					error="cline-args-required",
					en="Command line argument or a cline keyword argument " + 
						"required."
				)
			)
	
	
	#
	#
	# REPR
	#
	#
	def __repr__(self):
		C = " ".join(self.a)
		E = "..." if len(C)>45 else ""
		return "<trix/%s \"%s%s\">" % (type(self).__name__, C[:45], E) 
	
	
	#
	#
	# CALL
	#
	#
	def __call__(self):
		try:
			self.__x
			return self
		except:
			pass
		
		try:
			m = type(self).__sp
		except:
			m = type(self).__sp = trix.module("subprocess")
		
		# set defaults and run the process
		self.__k.setdefault("stdout", m.PIPE)
		self.__k.setdefault("stderr", m.PIPE)
		try:
			self.__x = m.Popen(self.__a, **self.__k)
		except FileNotFoundError:
			cmd = cmd.split()
			self.__x = m.Popen(self.__a, **self.__k)
		
		return self
	
	
	#
	#
	# READER
	#
	#
	def reader(self):
		"""
		Returns a buffer reader 
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
	
	
	#
	#
	#
	#
	#
	@property
	def x(self):
		"""Returns the executable object."""
		try:
			return self.__x
		except:
			self.__call__() # self.__call__() sets `self.__x`
			return self.__x
	
	
	#
	#
	#
	#
	#
	@property
	def text(self):
		"""
		Returns a propx object covering the text.
		
		Call this property like a function to return the text received 
		from the called process.
		
		Call it as a property to receive a proptext object.
		"""
		try:
			return trix.propx(self.__text)
		except:
			r = self.reader() # no args here; the reader property does them.
			r.seek(0)
			self.__text = r.read()
			return trix.propx(self.__text)
			
	@property
	def lines(self):
		"""Returns text lines as proptext."""
		return trix.propx(self.data.lines)
			
	@property
	def data(self):
		"""
		Returns a propx object. Treat `data` like a function, or explore
		the extra propx features.
		
		EXAMPLE 1
		>>> callx('ps').data.output()
		['  PID TTY          TIME CMD', ' 8212 pts/0    00:00:00 bash',
		 ' 8392 pts/0    00:00:00 python3', ' 8411 pts/0    00:00:00 ps']
		>>>
		
		EXAMPLE 2
		>>> callx('ps').data.output()
		  PID TTY          TIME CMD
		 8212 pts/0    00:00:00 bash
		 8392 pts/0    00:00:00 python3
		 8403 pts/0    00:00:00 ps
		>>>
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
			# There may be other ways to convert text to data...
			# if so, try them here.
			#
			
			# If nothing above works, just set the text as the data.
			self.__data = trix.propx(self.__text)
			return self.__data

