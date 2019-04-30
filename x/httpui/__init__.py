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
	Panel_Dir = "x/httpui/panel"
	
	
	def getpanel(self, panel_name):
		"""
		Pass the name of a panel from the httpui/www/panel directory. 
		(Do not include the '.html' suffix - just the panel name.)
		
		Reads and returns the html text of a panel html file.
		"""
		return trix.npath('%s/%s.html' % (self.Panel_Dir, panel_name)
			).reader(encoding=DEF_ENCODE).read()
	
	
	
	def generate_panel_list(self, **k):
		"""Respond with a JSON list of panels."""
		try:
			ls = trix.npath(self.Panel_Dir).ls
			files = ls.select(lambda p: p.set(p.split('.').v[0])).o
			self.dispatch_response(
				trix.formatter(f="JCompact").format(files)
			) 
		except Exception as ex:
			self.writeError("500", xdata())
			raise
	
	
	
	#
	# Override `generate_response` to handle commands
	#
	def generate_response(self, **k):
		"""
		Generate panel, panel list, or file response for display in trix 
		httpui interface.
		 * p=<PANELNAME>
		 * pp=<fnmatch-panel-list-query>; default *
		
		Otherwise, an html file's contents is returned.
		
		Note: More options are coming to this list. Ultimately ajax 
		      requests will also be processed here.		
		"""
		try:
			qdict = self.qdict
			if 'c' in qdict:
				self.generate_command_reply(qdict['c'][-1])
			elif 'p' in qdict:
				self.generate_panel(qdict['p'][-1])
			elif 'pp' in qdict:
				self.generate_panel_list(**k)
			else:
				# default... respond with specified file
				print ("ERR:", str(ex), xdata(panel_name=panel_name))
				HandleHttp.generate_response(self, **k)
			
		except BaseException as ex:
			self.writeError("500", xdata(qdict=qdict))
			raise
		
	
	
	def generate_panel(self, panel_name, **k):
		"""Load and return contents of an HTTP user interface panel."""
		try:
			p = self.getpanel(panel_name)
			self.dispatch_response(p)
		except Exception as ex:
			print ("ERR:", str(ex), xdata(panel_name=panel_name))
			self.writeError("500", xdata(panel_name=panel_name))
			#raise
	
	
	
	def generate_command_reply(self, command):
		"""Currently, no httpui commands are being handled."""
		try:
			r = {'c':command, 'e': None}
			if command=='foo':
				r["r"] = 'bar'
			else:
				r["r"] = 'error'
				r["e"] = 'unknown-command'
			self.dispatch_response(trix.formatter(f="JCompact").format(r))
		except Exception as ex:
			print ("ERR:", str(ex), xdata(command=command, r=r))
			self.writeError("500", str(ex), xdata(command=command, r=r))
			#raise












# 
# sunken (cursed) treasures
# 	
	
	"""
	def panel_list(self):
		try:
			return self.__panels
		except Exception as ex:
			print ("panel_list ERR1:", str(ex))
			try:
				self.__panels = trix.npath("x/httpui/panels").ls()
				return self.__panels
			except Exception as ex:
				print ("panel_list ERR2:", str(ex))
	"""			
	
	"""
	try:
		return self.__panel_dict[panel_name]
	except KeyError as ex:
		try:
			panel_n_path = 'x/httpui/%s' % panel_name
			self.__panel_dict[panel_name] = trix.npath(panel_n_path)
		except Exception as ex:
			print("ERR:", str(ex), str(xdata()))
			raise
	"""
