#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

#from trix import *
from ...net.handler.hhttp import *


class HttpUi(HandleHttp):
	"""HTTP user interface to trix features."""
	
	# HTTPUI CONTENT PATH
	WebContent = trix.innerfpath("x/httpui/www")
	
	
	#
	# HANDLE DATA
	#
	def handledata(self, data, **k):
				
		self.request = httpreq(data)
		try:
			self.__test
		except:
			self.__test=""
			trix.display(self.request.dict) #
		
		HandleHttp.handledata(self, data, **k)
