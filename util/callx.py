#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from .. import *
import shlex


class callx(object):
	"""
	Creates and handles Popen calls.
	"""
	
	@classmethod
	def cline(cls, cmd, **k):
		"""
		Pass a cline handler name and args, plus optional kwargs. Returns
		a callx object.
		"""
		try:
			a = shlex.split(cmd)
		except:
			a = cmd
		
		args = [sys.executable, '-m', trix.innerpath()]
		args.extend(a)
		
		return cls(args, **k)
	
	
	
	def __init__(self, cmd=None, **k):
		"""
		Makes a system call and returns the response.
		
		Pass argument `cmd`, which may be one of the following:
		 * a string containing a command line, to be split with shlex
		 * a list containing the exact arguments to pass to popen
		
		ALTERNATELY:
		Pass a keyword argument specifying a cline command.
		
		
		# Example 1 - Call a system command.
		The following line of code creates a callx object to gather text
		describing currently running processes.
		
		>>>
		>>> from trix.util.callx import *
		>>>
		>>> callx('ps').text.display()
		"  PID TTY          TIME CMD\n 3405 pts/2    00:00:00 bash\n 
		4094 pts/2    00:00:00 python3\n 4134 pts/2    00:00:00 ps\n"
		>>>
		>>> trix.callx('ps').list()
		
		
		>>>
		>>> # Example 2 - Call a command line handler (cline).
		>>>
		>>> from trix.util.callx import *
		>>> 
		
		
		
		"""
		
		#print ("CMD: %s" % cmd)
		#print ("KRG: %s" % k)
		
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
					en="Command line argument or a cline keyword argument required."
				)
			)
				
			
			
	
	
	def __repr__(self):
		C = " ".join(self.a)
		E = "..." if len(C)>45 else ""
		return "<trix/%s \"%s%s\">" % (type(self).__name__, C[:45], E) 
	
	
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
	
	
	
	
	def reader(self):
		try:
			return self.__reader
		except:
			self.__buffer = trix.ncreate(
				"util.stream.buffer.Buffer", 
				self.x.stdout.read(), **self.__rk
			)
			self.__reader = self.__buffer.reader()
			return self.__reader
	
	
	
	
	@property
	def a(self):
		"""Returns args, as given to constructor."""
		return self.__a
	
	@property
	def k(self):
		"""Returns kwargs, as given to constructor."""
		return self.__k
	
	@property
	def x(self):
		"""Returns the executable object."""
		try:
			return self.__x
		except:
			self.__call__() # self.__call__() sets `self.__x`
			return self.__x
	
	@property
	def text(self):
		"""
		Returns a propx object covering the text. Call this property like
		a function to return the text received from the called process.
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
		return self.data.lines
			
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

