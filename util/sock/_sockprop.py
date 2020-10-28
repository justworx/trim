#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#


from ... import * # trix
import socket


class sockprop(object):
	"""
	Stores the real socket; exposes socket proxy and properties.
	"""
	
	#
	#
	# INIT
	#
	#
	def __init__(self, socket):
		"""
		Pass the true socket object, not a proxy.
		"""
		
		#
		# STORING THE SOCKST
		#  - The `sock` parameter is either a proxy to an object stored by
		#    a subclass or its the socket itself. Either way, it's safe to
		#    store it here as itself because it's deleted by the __del__
		#    method when this object's released.
		# 
		self.__realsock = socket
		
		#
		# HERE IS THE WORKING COPY
		#  - This is the proxy that should be shared via the self.socket
		#    property.
		#  - The `self.__realsock` object should never be shared outside
		#    this object.
		#
		#    REMEMBER...
		#  - DO NOT STORE the actual socket object anywhere but HERE!
		#
		self.__socket = trix.proxify(socket)
	
	
	#
	#
	# DEL
	#
	#
	def __del__(self):
		"""
		Shutdown the socket; Set member variables to None
		"""
		
		try:
			self.shutdown()
		except:
			pass
		
		try:
			self.__realsock.shutdown()
		except:
			pass
		
		self.__realsock = None # Destroy the real socket.
		self.__socket = None   # Destroy the proxy, too.
	
	
	#
	#
	# SOCKET
	#
	#
	@property
	def socket(self):
		"""
		Return this object's socket as a proxy.
		"""
		try:
			return self.__socket
		except BaseException as ex:
			return None
	
	
	#
	#
	# TIMEOUT
	#
	#
	@property
	def timeout(self):
		"""Returns timeout value."""
		try:
			return self.socket.gettimeout()
		except BaseException as ex:
			return None
	
	
	
	#
	#
	# TIMEOUT (SET)
	#
	#
	@timeout.setter
	def timeout(self, f):
		"""Set timeout value."""
		try:
			self.socket.settimeout(f)
		except BaseException as ex:
			return None
		
	
	
	#
	#
	# ADDR
	#
	#
	@property
	def addr(self):
		"""
		Returns local address as tupel (addr,port).
		"""
		try:
			return self.socket.getsockname()
		except BaseException as ex:
			return None
		
	
	
	#
	#
	# PEER
	#
	#
	@property
	def peer(self):
		"""
		Returns remote address as tupel (addr,port).
		"""
		try:
			return self.socket.getpeername()
		except BaseException as ex:
			return None
	
	
	
	#
	#
	# PORT
	#
	#
	@property
	def port(self):
		"""
		Return this socket's port.
		"""
		try:
			return self.addr[1]
		except BaseException as ex:
			return None
	
	
	#
	#
	# SHUTDOWN
	#
	#
	def shutdown(self):
		"""
		Shutdown the socket.
		"""
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
		except:
			pass
		finally:
			self.__socket = None


