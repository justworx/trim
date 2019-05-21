#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import textwrap
from . import terminfo
from .output import * # trix, enchelp, sys
from .event import *
from .xinput import *
from .wrap import *


#
# ---- CONSOLE -----
#

class Console(BaseOutput):
	"""
	Base class for an interactive command-line user interface.
	"""
	
	Debug = 1 #0
	
	@classmethod
	def oappend(cls, o):
		try:
			cls.__olist.append(o)
		except:
			cls.__olist = []
			cls.__olist.append(o)
	
	@classmethod
	def oremove(cls, o):
		try:
			cls.__olist.remove(o)
		except:
			cls.__olist = []
	
	
	
	
	
	def __init__(self, config=None, **k):
		
		config = config or {}
		config.update(k)
		
		#print ("k:", k)
		wrap = trix.kpop(k, 'wrap').get('wrap') # object to wrap (or None)
		#print ('wrap', wrap)
		
		
		BaseOutput.__init__(self, config)
		
		# debugging
		self.__debug = config.get('debug', self.Debug)
		
		# wrapper
		self.__wrap = Wrap(wrap) if wrap else None
		
		# formatting for textwrap
		jc = trix.jconfig(trix.npath('util/console.json').path)
		self.__text = jc.obj
		self.__textk = dict(initial_indent="  * ", subsequent_indent="    ")
		self.__textk.update(**k)
		self.__textw = terminfo.termsize()[1]
			
	
	
	def __del__(self):
		self.__wrap = None
	
	
	
	@property
	def debug(self):
		"""Debug setting."""
		return self.__debug
	
	@property
	def jformat(self):
		"""Object display format (default: JDisplay)."""
		try:
			return self.__jformat
		except:
			self.__jformat = trix.formatter(f='JDisplay')
			return self.__jformat
	
	@property
	def prompt(self):
		"""Console prompt."""
		return "> "
	
	
	@property
	def wrap(self):
		"""Current wrapped object."""
		return self.__wrap
	
	
	
	#
	# TEXT BLOCK
	#
	def _textblock(self, textkey):
		for line in self.__text[textkey]:
			tx = textwrap.wrap(line, width=self.__textw, **self.__textk)
			for line in tx:
				print (line)
	
	
	#
	# BANNER
	#
	def banner(self):
		print (self.__text['title'])
		self._textblock('banner')
		print ("\n")
	
	def about(self):
		for line in self.__text['about']:
			tx = textwrap.wrap(line, width=self.__textw, **self.__textk)
			for line in tx:
				print (line)
	
	
	
	#
	# CREATE EVENT
	#
	def create_event(self, commandLineText):
		"""Returns a TextEvent."""
		return LineEvent(commandLineText)
	
	
	
	#
	#
	# CONSOLE - Run the console (Loop)
	#
	#
	def console(self):
		"""Call this method to start a console session."""
		self.banner()
		self.__active = True
		while self.__active:
			e=None
			try:
				# get input, create Event
				line = xinput(self.prompt).strip()
				
				# make sure there's some text to parse
				if line:
					# get and handle event
					if line[0] == '/':
						# this is a command for the console object
						e = self.create_event(line[1:])
						self.handle_command(e)
					elif line[0] == '!':
						# this is a command for the wrapped object
						e = self.create_event(line[1:])
						self.handle_wrapper(e)
					else:
						e = self.create_event(line)
						self.handle_input(e)
			
			except (EOFError, KeyboardInterrupt) as ex:
				# Ctrl-C exits this prompt with EOFError; end the session.
				self.__active = False
				self.output("\n#\n# Console Exit\n#\n")
			
			except BaseException as ex:
				self.output('') # get off the "input" line
				self.output("#\n# %s: %s\n#" % (type(ex).__name__, str(ex)))
				if self.debug:
					if e and e.error:
						self.output(self.jformat(dict(event=e.dict,err=e.error)))
					self.output(self.jformat(xdata()))
					#self.output(self.newl.join(trix.tracebk()))
					self.output(self.jformat(trix.tracebk()))
	
	
	
	
	#
	#
	# ---- HANDLE INPUT, COMMANDS -----
	#
	#
	
	def handle_input(self, e):
		"""Send `e.text` to the target stream."""
		self.output(e.text)
	
	
	
	
	def handle_command(self, e):
		"""
		Handle input event `e`.
		"""
		if e.argvl[0] == 'about':
			self.about()
		
		elif e.argvl[0] == 'debug':
			if e.arg(1) is not None:
				self.__debug = bool(e.arg(1))
			else:
				self.output(str(bool(self.__debug)))
		
		# list
		elif e.argvl[0] == 'list':
			self.olist.table(w=3)
		
		# selected
		elif e.argvl[0] == 'selected':
			self.oselected()
		
		# select
		elif e.argvl[0] == 'select':
			try:
				objectName = e.argv[1]
				self.oselect(objectName)
			except IndexError:
				print("FAIL. Argument 'object name' required.")
		
		elif e.argvl[0] in ['wrap', 'wrapper']:
			wrap = type(self.__wrap.o).__name__
			self.output("%s: %s" % (wrap, self.__wrap.name))
		
		# exit the console session
		elif e.argvl[0] == 'exit':
			self.__active = False
	
	
	
	
	def handle_wrapper(self, e):
		"""
		Handle commands prefixed with the exclamation point '!' 
		character - wrapped object commands.
		
		NOTE: Wrapper commands are case-sensitive.
		"""		
		if self.__wrap:
			# wrapper commands are case-sensitive, so use e.arg(0)
			r = self.__wrap(e.arg(0), *e.argv[1:], **e.kwargs)
			if r:
				self.output(str(r))
	
	
	
	# -----------------------------------------------------------------
	
	def oselected(self):
		if self.__wrap:
			#print (self.__wrap)
			print(self.__wrap.name)
		else:
			print()
	
	def oselect(self, name):
		"""Select an object from the object list to wrap."""
		try:
			for o in self.__olist:
				if o.name == name:
					self.__wrap = Wrap(o)
		except Exception as ex:
			print (type(ex), ex.args)
			
	
	
	@property
	def olist(self):
		try:
			r = []
			for o in self.__olist:
				r.append(o.name)
		except:
			pass
		return trix.propx(r)
	
