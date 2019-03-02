#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *


#
# VECTOR
#

class vector(object):
	
	def __init__(self, x={}):
		#
		# Pass `x`, a dict that contains keys (int, item-offset) for 
		# non-zero item values.
		#
		self.__d = 0   # default node value: 0
		self.__mx = 0  # current maximum vector length
		
		# set nodes values defined in argument dict `x`.
		self.__v = None
		self.set(x)
		
	
	@property
	def width(self):
		return self.__mx+1
	
	@property
	def row(self):
		return list(self.gen)
	
	@property
	def gen(self):
		for ii in range(0, self.__mx+1):
			try:
				yield (self.__v[ii])
			except KeyError:
				yield (0)
	
	
	def range(self):
		return range(0, self.__mx+1)
	
	
	def __getitem__(self, i):
		#
		# Return a node object with __getitem__ and get methods the results
		# of which are taken from a copy of the containing vector.
		#
		try:
			return self.__v[i]
		except BaseException as e:
			return 0
	
	
	def __setitem__(self, i, v):
		#
		# Set item `i` with value `v`.
		#
		self.__v[i] = v
		if i > self.__mx:
			self.__mx = i
	
	
	def get(self):
		# Return the vector value (should be a dict)
		return self.__v
	
	
	def set(self, values):
		"""
		Set values for this matrix. The constructor calls this method
		passing the given argument constructor argument.
		
		Valid arguments are either:
		 * a dict with integer keys paired to any non-zero value. Any
		   unspecified integer key defaults to zero.
		 * or, a normal python list containing all values contained in
		   this vector.
		
		Vector (list) length is determined by the longest resulting row.
		"""
		d = {}
		try:
			values.keys
			self.__v = values
		except:
			mx = 0
			for i in range(0, len(values)):
				if values[i]:
					self.__v[i] = values[i]
		
		# store the largest key value
		self.__mx = max(self.__v.keys())





"""
#
# ELEMENT (node)
#  - I'm not too sure whether this will be of any valid use. I'm
#    thinking not. However, I'll hold it here, commented, until I've
#    given it some thought.
#

class node(object):
	def __init__(self, vector, i):
		#
		# The point of node is to make a live node object with member 
		# variables that reflect updates made to the owning vector.
		#
		self.__v = trix.proxify(vector) # proxy to a vector object
		self.__i = i                    # key to value in vector dict
	
	@property
	def v(self):
		return self.__v[self.__i]
	
	@property
	def vector(self):
		return self.__v
	
	def get(self):
		try:
			return self.__v[self.__i] # remember self.__v is a dict
		except KeyError:
			return self.__v.defvalue
	
	def set(self, i, x):
		self.__v[i] = x
"""


