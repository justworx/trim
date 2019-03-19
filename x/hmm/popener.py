#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .enchelp import *
from ..propx import *


class POE(object):
	"""Custom Popen.communicate output manager."""
	
	def __init__(self, oe):
		self.__oe = oe
	
	@property
	def stderr(self):
		return self.__oe[1]
	
	@property
	def stdout(self):
		

class POpener(Popen):
	"""Custom Popen class. Overrides communicate."""
	
	def communicate(self, input=None, timeout=None):
		if input:
			self.stdin.write(input)
		else:
			return POE(Popen.communicate(self, input, timeout))



"""
class POpener(object):
	#
	# Potentially a new Popen manager, I guess. I need better features.
	#
	
	def __init__(self, cmd, *a, **k):
		
		try:
			m = cls.__sp
		except:
			m = cls.__sp = trix.module("subprocess")
		
		# set defaults and run the process
		k.setdefault("stdout", m.PIPE)
		k.setdefault("stderr", m.PIPE)
		try:
			self.__p = m.Popen(cmd, *a, **k)
		except FileNotFoundError:
			cmd = cmd.split()
			self.__p = m.Popen(cmd, *a, **k)


		
	def communicate(self, input=None, timeout=None):
		return self.communicate(input, timeout)


	
	def poll(self):
		return self.poll()
	
	def wait(self, timeout=None):
		return self.wait(timeout)
		
	def send_signal(self, signal):
		return self.send_signal(signal)
		
	def terminate(self):
		return self.terminate()
		
	def kill(self):
		return self.kill()
	
	
	@property
	def args(self):
		return self.args
	
	@property
	def stdin(self):
		return self.stdin
	
	@property
	def stdout(self):
		return self.stdout
	
	@property
	def stderr(self):
		return self.stderr
	
	@property
	def pid(self):
		return self.pid
	
	@property
	def returncode(self):
		return self.returncode
"""

