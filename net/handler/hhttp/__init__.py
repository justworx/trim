#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#

from time import gmtime, strftime
from ....util import urlinfo, mime
from ....net.handler import *
from ....net.httpreq import *


#
# HANDLE-HTTP
#
class HandleHttp(Handler):
	"""
	Replies with the default HTTP content handler - a message about 
	this class and how to customize it to suit your needs.
	"""
	
	#
	# DEFAULT CONTENT PATH
	#
	WebContent = trix.innerfpath("net/handler/hhttp/example/")
	
	
	#
	#
	# INIT
	#
	#
	def __init__(self, sock, **k):
		
		# inits
		self.__request = None
		
		# make root dir configurable
		self.__rootdir = k.get('rootdir')
		
		# set default path to the example content files (if necessary)
		if not self.__rootdir:
			self.__rootdir = self.WebContent
		
		Handler.__init__(self, sock, **k)
		
		# webroot is an fs.Path object
		self.__webroot = trix.path(self.__rootdir)
		
		# configurable header items
		self.__server = k.get("Server", "trix/%s" % str(VERSION))
		self.__connection = k.get("Connection", "keep-alive")
	
	
	@property
	def request(self):
		"""
		Current request's `request` object, or None if no request is
		in progress.
		"""
		return self.__request
	
	@property
	def rootdir(self):
		"""String; The root directory containing content files."""
		return self.__rootdir
	
	@property
	def webroot(self):
		"""An `fs.Dir` object wrapping `self.rootdir`."""
		return self.__webroot
	
	
	#
	#
	# HANDLE DATA
	#  - Override the net.handler `handledata` method returning web
	#    content.
	#
	#
	def handledata(self, data, **k):
		"""
		Receive a web request; process and return reply.
		"""
		
		self.parse_request(data, **k)
		self.generate_response(**k)
	
	
	
	def parse_request(self, data, **k):
		"""
		Parse request; Set internal variables:
		 - self.request: the net/httpreq object
		 - self.uinfo  : the util/urlinfo object
		 - self.qdict  : the urlinfo query dictionary Eg: ?a=1 -> {'a':1}
		 - self.reqpath: the path to a requested file
		"""
		#
		# Parse Headers
		#
		self.__request = httpreq(data)
		
		# Parse URL
		self.uinfo = urlinfo.urlinfo(self.__request.reqpath)
		self.qdict = self.uinfo.qdict
		
		# Get full path string to requested document...
		reqpath = self.webroot.merge(self.uinfo.path)
		
		# ...and a path object
		self.reqpath = trix.path(reqpath)
	
	
	
	def generate_response(self, **k):
		"""
		Calls `generate_file_response()` dto generate content based on 
		request url path.  
		
		Override to implement custom content generation.
		"""
		self.generate_file_response(**k)
	
	
	
	def generate_file_response(self, **k):
		"""
		Read and return the file specified by `self.reqpath`.
		"""
		try:
			# apply default file (index.html)
			if self.reqpath.isdir():
				sReqPath = self.reqpath.merge('index.html')
			else:
				sReqPath = self.reqpath.path
			
			# Check mime type
			self.contentType = mime.Mime(sReqPath).mimetype
			
			# Load File Content
			content = trix.path(sReqPath).reader(encoding="utf_8").read()
			
			self.dispatch_response(content)
			
		except BaseException as ex:
			self.writeError("500", xdata())
			raise
	
	
	
	
	def dispatch_response(self, response_content):
			
		try:
			# Generate Headers
			clength = len(response_content.encode('utf_8'))
			
			# Write the response header and...
			head = self.head('200', clength)
			
			# ...send End Bytes.
			self.write(head + "\r\n\r\n" + response_content + "\r\n\r\n")
			
		except BaseException as ex:
			self.writeError("500", xdata())
			raise
	
	
	
	#
	# HEAD - Generate head text.
	#
	def head(self, result, clength):
		"""Generate and return the response header text."""
		
		#
		# TEMPORARY MEASURE
		#  - we need a way to insure contentType is set.
		#
		try:
			content_type = self.contentType or "text/html"
		except:
			content_type = "text/html"
		
		gmt = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		head = "\r\n".join([
			"HTTP/1.1 %s OK"     % result, 
			"Date: %s"           % (gmt),
			"Connection: %s"     % (self.__connection),
			"Server: %s"         % (self.__server),
			"Accept-Ranges: bytes",
			"Content-Type: %s"   % content_type,
			"Content-Length: %i" % (clength),
			"Last-Modified: %s"  % (gmt) # this should be the file mod date
		])
		
		return head
	
	
	
	#
	# WRITE-ERROR - Writes error page to client.
	#
	def writeError(self, errcode, xdata=None):
		"""
		Write an error response given `errcode` and optional `xdata`.
		"""
		try:
			b = trix.ncreate('util.stream.buffer.Buffer', encoding='utf_8')
			w = b.writer()
			
			w.write("<html><head>\r\n")
			w.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n')
			w.write("<title>Error</title>\r\n")
			w.write("</head><body>\r\n")
			
			if errcode == '404':
				w.write("<h1>404 File Not Found Error</h1>\r\n")
			else:
				w.write("<h1>500 Internal Server Error</h1>\r\n")
			w.write("<pre>\r\n")			
			
			if xdata:
				# gotta make entities out of gt & lt...
				xdatae = trix.formatter(f='JDisplay').format(xdata)
				xdatae = xdatae.replace(">", "&gt;")
				xdatae = xdatae.replace("<", "&lt;")
				#print (xdatae)
				w.write(xdatae)
			w.write("</pre>\r\n</body></html>\r\n\r\n")
			
			# SEND the error page.
			head = self.head(errcode, w.tell())
			self.write("%s\r\n\r\n" % (head.encode('utf_8')))
			
			# read the response from the Buffer, b
			self.write(b.read())
		
		except Exception as ex:
			pass
			# debug message
			#print ("\n\n\n\n\nERROR HANDLING EXCEPTION!\n\n\n\n", str(ex))
			#raise

