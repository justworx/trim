#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

import textwrap, atexit
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
	An interactive command-line user interface.
	
	Console is under construction, but is useful for debugging.
	It provides a measure of control over objects based on the 
	`util.runner.Runner` class.
	
	EXAMPLE:
	>>> from trix.util.console import *
	>>> Console().console()
	
	"""
	
	Debug = False
	
	# need to make these defaults for `config`
	ConsoleCmdKey  = '/'
	ConsoleWrapKey = '!'
	ConsolePrompt  = "trix.Console:"
	ConsoleConfig  = "app/config/assets/console.%s" % DEF_LANG
	
	#
	# 
	#
	TextK_Updates  = ["width", "expand_tabs", "tabsize", 
		"replace_whitespace", "drop_whitespace", "initial_indent", 
		"subsequent_indent", "fix_sentence_endings", "break_long_words",
		"break_on_hyphens", "max_lines", "placeholder"]
	
	
	#
	# Store all consolable objects here	
	#
	__olist = []

	
	#
	#
	# INIT
	#
	#
	def __init__(self, config=None, **k):
		"""
		Create a `Console` object.
		
		Though config and keyword arguments may be provided, it probably
		is best, for now, to open the console using defaults.
		
		
		
		"""
		config = config or {}
		config.update(k)
		
		# init superclass
		BaseOutput.__init__(self, config)
		
		# set debugging
		self.__debug = config.get('debug', self.Debug)
		
		# plugins
		#self.__plugins = {}
		#plugin_config = trix.config(DEF_CACHE
		
		self.__plugins = {}
		self.__plugins['calc'] = trix.ncreate(
				"app.plugin.calc.Calc", "calc", self, {}
			)
		self.__plugins['dir'] = trix.ncreate(
				"app.plugin.dir.Dir", "dir", self, {}
			)
		
		#
		#
		# wrapper
		#
		#  - what's going on here?
		#  - it's failing in wrap
		#  - transport endpoint is not connected
		#  - but the endpoint i want isn't the server socket
		#  - i want it going to output
		#  - should output be using classmethods?
		#
		#
		wrap = trix.kpop(config, 'wrap').get('wrap')
		self.__wrap = Wrap(wrap) if wrap else None
		
		# set wrapper name
		wrapname = self.__wrap.name if self.__wrap else None # was "None"
		
		# formatting for textwrap
		jc = trix.jconfig(trix.npath(self.ConsoleConfig).path)
		self.__text = jc.obj
		
		# constructor kwargs for textwrapping
		tk = trix.kcopy(k, self.TextK_Updates)
		tk.setdefault("initial_indent", "  * ")
		tk.setdefault("subsequent_indent", " "*4)
		self.__textk = tk
		
		# store terminal width
		self.__textw = terminfo.termsize()[1]
		
		
		# prompt
		self.__prompt = jc.obj.get('prompt') or self.ConsolePrompt
		#ConsoleCmdKey  = '/'
		#ConsoleWrapKey = '!'
		#ConsolePrompt  = "trix.Console:"
		
		
		#
		# TEXTBLOCK ARGS
		#  - textblock arguments must be sent from the `about`, `help`, 
		#    and console method to the `__textblock()` method as keyword 
		#    arguments.
		#  - The value of self.wrap may change through the course of a
		#    console session, so that one must be set in `__textblock()`.
		#
		try:
			targname = self.target.name
		except:
			targname = repr(self.target)
		
		self.__textblock_kwargs = dict(
				wrapper_name = wrapname,
				target_strm = targname,
				console_cmd = self.ConsoleCmdKey,
				wrapper_cmd = self.ConsoleWrapKey
			)
	
	
	#
	#
	# __DEL__
	#
	#
	def __del__(self):
		self.__wrap = None
	
	
	#
	#
	# DEBUG
	#
	#
	@property
	def debug(self):
		"""Debug setting."""
		return self.__debug
	
	
	#
	#
	# JFORMAT
	#
	#
	@property
	def jformat(self):
		"""Object display format (default: JDisplay)."""
		#
		# TO-DO: Use this (rather than `display`) to output structures!
		#
		try:
			return self.__jformat
		except:
			self.__jformat = trix.formatter(f='JDisplay')
			return self.__jformat
	
	
	#
	#
	# PROMPT
	#
	#
	@property
	def prompt(self):
		"""Console prompt."""
		return "%s " % self.__prompt
	
	
	#
	#
	# WRAP
	#
	#
	@property
	def wrap(self):
		"""Currently selected "wrapped" object."""
		return self.__wrap
	
	
	#
	#
	# PLUGINS
	#
	#
	@property
	def plugins(self):
		"""Return plugins dict."""
		return self.__plugins
	
	
	#
	#
	# __TEXTBLOCK - (banner, about, help)
	#
	#
	def __textblock(self, textkey, **k):
		
		#trix.display (["self.text", self.__text])
		
		# read each line from the specified text
		for line in self.__text[textkey]:
			
			# wrap the line to fit the current terminal width
			self.__textk.setdefault('width', self.__textw)
			tx = textwrap.wrap(line, **self.__textk)
			
			#trix.display (["tx", tx])
			self.__textblock_kwargs.setdefault('wrapper_name', "None")
			try:
				for lx in tx:
					print (lx.format(**self.__textblock_kwargs))
			except Exception as ex:
				raise type(ex)(xdata(line=line, tx=tx, lx=lx, 
						tbkwargs=self.__textblock_kwargs
					))
	
	
	#
	#
	# ABOUT
	#
	#
	def about(self):
		print (self.__text['title_about'])
		self.__textblock('about')
		print("")
	
	
	#
	#
	# BANNER
	#
	#
	def banner(self):
		print (self.__text['title'])
		self.__textblock('banner')
		print("")
	
	
	#
	#
	# HELP
	#
	#
	def help(self):
		print (self.__text['title_help'])
		self.__textblock('help')
		print("")
		#print("Help is not yet available.")
	
	
	#
	#
	# CREATE_EVENT
	#
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
		"""
		Call this method to start a console session.
		
		What happens?
		 * A banner is displayed.
		 * A prompt is displayed.
		 * Prompt commands are executed.
		 
		"""
		self.banner()
		self.__active = True
		while self.__active:
			e=None
			try:
				# get input, create Event
				line = xinput(self.prompt).strip()
				
				# Make sure there's some text to parse.
				if line:
					#
					# Get and handle whatever text was entered.
					#
					
					#
					# SEND TO HANDLE-COMMAND: /
					#  - If the first character on the (stripped) line is a
					#    slash '/', this is a command for the console.
					#
					if line[0] == self.ConsoleCmdKey:
						e = self.create_event(line[1:])
						self.handle_command(e)
					
					#
					# SEND TO HANDLE-WRAPPER: !
					#  - If the first character on the (stripped) line is a
					#    bang '!', this is a command for the currently "wrapped"
					#    object (which can be selected by /wrap <object name>).
					#
					elif line[0] == self.ConsoleWrapKey:
						e = self.create_event(line[1:])
						self.handle_wrapper(e)
					
					#
					# SEND TO HANDLE-INPUT:
					#  - When the first character on the (stripped) line is 
					#    neither bang '!' nor slash '/', the command is handled
					#    differently.
					#
					else:
						e = self.create_event(line)
						self.handle_input(e)
			
			
			except (EOFError, KeyboardInterrupt) as ex:
				# Ctrl-C exits this prompt with EOFError; end the session.
				self.__active = False
				print("\n#\n# Console Exit (%s)\n#\n" % str(type(ex)))
			
			except BaseException as ex:
				print('') # get off the "input" line <---- KEEP PRINT HERE?
				print("#\n# %s: %s\n#" % (type(ex).__name__, str(ex)))
				if self.debug:
					if e and e.error:
						print(self.jformat(dict(event=e.dict,err=e.error)))
					print(self.jformat(xdata()))
					#print(self.newl.join(trix.tracebk()))
					print(self.jformat(trix.tracebk()))
	
	
	
	
	#
	#
	# ---- HANDLE INPUT, COMMANDS -----
	#
	#
	
	
	#
	#
	# HANDLE_INPUT
	#
	#
	def handle_input(self, e):
		"""
		Send `e.text` to the target stream.
		"""
		if e.text:
			try:
				self.plugins['calc'].handle(e)
			except BaseException as ex:
				self.output(str(ex)) # comment this ( debugging )sin
				pass
			
			x = self.plugins['dir']
			
			#
			# The Dir plugin publishes its command list in a class variable.
			# This is a good idea to remember for plugins that have only
			# commands (as opposed to calc, which watches every line for
			# a chance to do its thing.
			#
			if e.text in x.COMMANDS:
				x.handle(e)
			
			if e.reply:
				self.output(e.reply)
			
		if self.debug:
			e.display()
	
	
	#
	#
	# HANDLE_COMMAND
	#
	#
	def handle_command(self, e):
		"""
		Handle input event `e`.
		
		The `handle_command` method is called when `ConsoleCmdKey` is the 
		first character in a given command line. (Default: "/".)
		
		FOR EXAMPLE:
		/help causes the help banner to be displayed
		
		EXAMPLE
		trix.Console: /help
		Console commands/descriptions
		  * about    : Print the 'about' message
		  * banner   : Print the console startup banner
		  * help     : Print (this) help message
		  * list     : List Runners by name
		  * select   : Select a Runner by name
		  * selected : Display name of currently selected Runner
		  * exit     : Exit the console.
		
		SEE ALSO:
		>>> from trix.util.runner import *
		>>> help(Runner)
		
		NOTE ALSO:
		Objects in this process that are based on `util.runner.Runner` 
		automatically show up in the /list results. Use /select to select
		a object by name. The /selected command displays the currently 
		selected object.
		
		Use !<command> feature to query `Runner.display` and other 
		methods.
		
		"""		
		
		#
		# UNDOCUMENTED COMMANDS
		#
		if e.argvl[0] == 'plugins':
			trix.display(self.plugins)
		
		elif e.argvl[0] == 'prompt':
			self.__prompt = e.argv[1]
		
		elif e.argvl[0] == 'clear':
			trix.tx.cls
		
		
		#
		# DOCUMENTED COMMANDS
		#
		elif e.argvl[0] == 'about':
			self.about()

		elif e.argvl[0] == 'banner':
			self.banner()
		
		elif e.argvl[0] == 'help':
			self.help()
		
		elif e.argvl[0] == 'debug':
			if e.arg(1) is not None:
				self.__debug = bool(e.arg(1))
			else:
				print(str(bool(self.__debug)))
		
		# list
		elif e.argvl[0] == 'list':
			self.olist.table(w=3)
		
		# selected
		elif e.argvl[0] == 'selected':
			o = self.oselected()
			if o:
				print(repr(o))
				print()
		
		# select
		elif e.argvl[0] == 'select':
			try:
				objectName = e.argv[1]
				self.oselect(objectName)
				wrapper_name = self.wrap.name if self.wrap else "None"
				self.__textk['wrapper_name'] = wrapper_name

			except IndexError:
				print("FAIL. Argument <object-name> required.")
		
		elif e.argvl[0] in ['wrap', 'wrapper']:
			if self.__wrap:
				wrap = type(self.__wrap).__name__
				print("%s: %s" % (wrap, self.__wrap.name)+"\r")
			else:
				print()
		
		# exit the console session
		elif e.argvl[0] == 'exit':
			self.__active = False
	
	
	#
	#
	# HANDLE_WRAPPER
	#
	#
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
				print(str(r)+"\r")
	
	
	#
	#
	# OSELECTED
	#  - List, select, or [query for the selected] Runner
	#
	#
	def oselected(self):
		if self.__wrap:
			#print (self.__wrap)
			print(self.__wrap.name)
		else:
			print()
	
	
	#
	#
	# OSELECT
	#
	#
	def oselect(self, name):
		"""Select an object from the object list to wrap."""
		try:
			self.__wrap = None
			for o in type(self).__olist:
				if o.name == name:
					self.__wrap = Wrap(o)
			if not self.__wrap:
				raise ValueError(xdata(error="err-select-fail", 
						reason="no-such-name", name=name
					))
		except Exception as ex:
			print (type(ex), ex.args)
			if self.debug:
				raise
	
	
	#
	#
	# OLIST
	#
	#
	@property
	def olist(self):
		try:
			r = []
			for o in type(self).__olist:
				r.append(o.name)
			
			return trix.propx(r)
		
		except BaseException as ex:
			print (type(ex), ex.args)
			if self.debug:
				raise
	
	
	#
	#
	# OAPPEND
	#  - Classmethods used by runner to add/remove self
	#
	#
	@classmethod
	def oappend(cls, o):
		try:
			cls.__olist.append(o)
		except:
			raise
			cls.__olist = []
			cls.__olist.append(o)
	
	
	#
	#
	# OREMOVE
	#
	#
	@classmethod
	def oremove(cls, o):
		try:
			cls.__olist.remove(o)
		except:
			raise
			cls.__olist = []
	
	
	#
	#
	# AT EXIT
	#
	#
	@classmethod
	def _at_exit(cls):
		for obj in cls.__olist:
			obj.shutdown()

#
# Make all runners shutdown when the program terminates.
#
atexit.register(Console._at_exit)


