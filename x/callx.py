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

from .. import *
import shlex


class ProcessHandler(object):
	"""Creates and handles Popen calls."""
	
	def __init__(self, cmd, **k):
		"""
		Pass argument `cmd`, which may be one of the following:
		 * a string containing a command line, to be split with shlex
		 * a list containing the exact arguments to pass to popen
		"""
		
		# pop kwargs meant for reader
		self.__rk = trix.kpop(k, "encoding errors mode max_size")
		
		# remaining kwargs must be for Popen.
		self.__k = k
		
		# get the command-line arguments
		try:
			self.__a = shlex.split(cmd)
		except:
			self.__a = cmd
	
	
	
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
	def read(self):
		"""
		Returns a propx object. Treat `read` like a function, or explore
		the extra propx features.
		"""
		try:
			return trix.propx(self.__data)
		except:
			r = self.reader()
			r.seek(0)
			self.__data = r.read()
			return trix.propx(self.__data)




""" NO...
class Caller(object):
	def __init__(self, cpath, *a, **k):
		self.a = a
		self.k = k
		self.w = Wrapper(trix.create(cpath))
	
	def __call__(
"""
