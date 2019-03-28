#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


#
# EXPERIMENTAL - EXPLORATORY
#  - I'm pursuing something like propx here, but to be used with
#    executables rather than values.
# 

from ..propx import *
import shlex


class callx(object):
	"""Creates and handles Popen calls."""
	
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
	
	
	
	
	def __init__(self, cmd, **k):
		"""
		Pass argument `cmd`, which may be one of the following:
		 * a string containing a command line, to be split with shlex
		 * a list containing the exact arguments to pass to popen
		"""
		
		# pop kwargs meant for reader
		self.__rk = trix.kpop(k, "encoding errors mode max_size")
		self.__rk.setdefault('encoding', DEF_ENCODE)
		
		# remaining kwargs must be for Popen.
		self.__k = k
		
		# get the command-line arguments
		try:
			self.__a = shlex.split(cmd)
		except:
			self.__a = cmd
	
	
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
		"""Returns the text received from the called process."""
		try:
			return propx(self.__text)
		except:
			r = self.reader()
			r.seek(0)
			self.__text = r.read()
			return propx(self.__text)
			
	@property
	def data(self):
		"""
		Returns a propx object. Treat `read` like a function, or explore
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
				self.__data = propx(data)
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

