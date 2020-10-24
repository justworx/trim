#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .output import * # trix, enchelp, sys
from .console import *
from .stream.buffer import *

DEF_SLEEP = 0.1


class Runner(Output):
	"""
	Start, manage, and stop a (possibly threaded) event loop. Override
	the `io` method in subclasses to define actions that must be taken 
	each pass through the loop.
	
	NOTE:
	 - Always use base-class `Output.output()` method to write data 
	   from within the `io()` method. This allows output written when 
	   in a pause state to be buffered and then printed later (when 
	   the pause state ends).
	"""
	
	# INIT
	def __init__(self, config=None, **k):
		"""Pass config and/or kwargs."""
		
		# add self to the console class-variable `OList`
		Console.oappend(self)
		
		# basic status
		self.__active = False
		self.__running = False
		self.__threaded = False
		self.__threadid = None
		
		# remote socket control
		self.__csock = None
		self.__cport = None
		self.__lineq = None
		self.__jformat = trix.ncreate('fmt.JCompact')
		
		# each subclass of Output must track its own pause status
		self.__pausestate = self.paused()
		
		try:
			#
			# CONFIG
			#  - If this object is a Runner subclass that's already set a 
			#    self.config value, then kwargs have already been merged
			#    into `config`.
			#
			config = self.config
		except:
			#
			#  - If not, we'll need to create the config from args/kwargs.
			#    Creating a config dict, then - regardless of whether 
			#    `config` is from an existing self.config property - update
			#    it with `k` (directly below).
			#
			config = config or {}
		
		#
		# UPDATE CONFIG WITH `k`
		#  - Runner can't take a URL parameter unless it's part of a class
		#    that converts URL (or whatever other `config` type) to a dict
		#    before calling Runner's __init__. 
		#  - Therefore... don't catch this error; let it raise immediately
		#    so the developer will know there's something wrong here.
		#  - BTW: What the developer needs to do is make sure the config
		#         passed here from a base class is given as a dict.
		#
		config.update(k)
		
		# 
		# CONFIG - COPY
		#  - Runner should work as a stand-alone class, so....
		#  - Keep a copy in case this Runner object is created as itself
		#    (rather than as a super of some other class).
		#
		self.__config = config
		
		# 
		# ENCODING HELPER
		#  - Encoding for decoding bytes received over socket connections.
		# 
		Output.__init__(self, config)
		
		
		#
		# running and communication
		#
		self.__sleep = self.config.get('sleep', DEF_SLEEP)
		
		# Let kwargs set the "name" property; otherwise name is generated
		# on request of property `self.name`.
		if 'name' in self.config:
			self.__name = str(self.config['name'])
		
		#
		# If CPORT is defined in config, connect to calling process.
		#
		if "CPORT" in self.config:
			#
			# Set up for communication via socket connection.
			#
			self.__lineq = trix.ncreate('util.lineq.LineQueue')
			self.__cport = p = self.config["CPORT"]
			self.__csock = trix.ncreate('util.sock.sockcon.sockcon', p)
			try:
				self.__csock.writeline("%i" % trix.pid())
			except Exception as ex:
				trix.log("csock-write-pid", trix.pid(), type(ex), ex.args)
				self.__csock = None
				self.__lineq = None
	
	
	
	# ----------------------------------------------------------------
	# DEL
	# ----------------------------------------------------------------
	def __del__(self):
		"""Stop. Subclasses override to implement stopping actions."""
		try:
			try:
				self.shutdown()
			except Exception as ex:
				trix.log(
						"err-runner-delete", "stop-fail", ex=str(ex), 
						args=ex.args, xdata=xdata()
					)
			
			#
			# EXPERIMENTAL 20190522
			# WTF. 20201023 - This self.__xthread: thing will cause an 
			#                 exception. There is no self.__xthread!
			#                 self.__xthread! What was I thinking?
			#
			#if self.__xthread:
			#	del(self.__xthread)
			#	self.__xthread = None
			#
			
			if self.__csock:
				try:
					self.__csock.shutdown(SHUT_RDWR)
				except Exception as ex:
					trix.log(
							"err-runner-csock", "shutdown-fail", ex=str(ex), 
							args=ex.args, xdata=xdata()
						)
			
			if self.active:
				self.close()
		
		except BaseException as ex:
			trix.log("err-delete-ex", "shutdown-fail", ex=str(ex), 
					args=ex.args, xdata=xdata()
				)
		
		finally:
			self.__csock = None
			Console.oremove(self)
	
	
	# ----------------------------------------------------------------
	#
	# PROPERTIES
	#  - Runner is often one of a set of multiple base classes that may
	#    fail (and deconstruct) during init, so its properties need to
	#    be available even if Runner.__init__ has not yet been called.
	#  - This helps prevent raising of irrelevant Exceptions that might
	#    mask the true underlying error.
	#
	# ----------------------------------------------------------------
	
	@property
	def active(self):
		"""True if open() has been called; False after close()."""
		try:
			return self.__active
		except:
			self.__active = False
			return self.__active
	
	@property
	def running(self):
		"""True if running."""
		try:
			return self.__running
		except:
			self.__running = None
			return self.__running
	
	@property
	def threaded(self):
		"""True if running in a thead after a call to self.start()."""
		try:
			return self.__threaded
		except:
			self.__threaded = None
			return self.__threaded
	
	@property
	def threadid(self):
		"""
		Returns thread id when running, else None. If not threaded, the
		main thread id is returned (but again, only when running).
		"""
		return self.__threadid
	
	@property
	def sleep(self):
		"""Sleep time per loop."""
		try:
			return self.__sleep
		except:
			self.__sleep = DEF_SLEEP
			return self.__sleep
	
	@sleep.setter
	def sleep(self, f):
		"""
		Set the amount of time this Runner should sleep after each pass 
		through the run loop.
		"""
		self.__sleep = f
	
	@property
	def name(self):
		"""
		Return the runner name, if one was provided to the constructor
		via kwarg "name". (Otherwise, a name will be generated using the
		pattern "<class_name>-<thread_ident>".)
		"""
		try:
			return self.__name
		except:
			self.__name = "Runner-%s" % str(self.__threadid)
			return self.__name
	
	@property
	def config(self):
		"""The configuration dict - for reference."""
		try:
			return self.__config
		except:
			self.__config = {}
			return self.__config
	
	@property
	def csock(self):
		"""
		Used internally when opened with trix.process(), or any time a
		keyword argument "CSOCK" is given. 
		"""
		try:
			return self.__csock
		except:
			self.__csock = None
			return self.__csock
	
	
	
	# ---- orisc -----
	
	# ----------------------------------------------------------------
	#
	# OPEN
	#
	# ----------------------------------------------------------------
	def open(self):
		"""
		The `open` method is called by run() if self.active is False.
		
		Override this method, adding any code that needs to execute in
		order for the subclass to work. 
		
		Call `open` from Subclasses! If you override the `open` method,
		be sure to call `Runner.open()` exactly after all opening actions
		are complete, so that the `Runner.active` flag will be set True.
		"""
		self.__active = True
	
	
	
	
	
	
	def wait(self, timeout=1, **k):
		"""
		Wait for `self.active` to become True (only when threaded).
		
		This method protects the main from trying to access member
		variables before threaded `open()` code can create them. 
		
		Calls to open() may take some time to complete. Always use 
		`wait(timeout)` to specify a maximum period to wait on `open`
		before timing out. Waiting ends when `self.active` becomes True
		and the method returns `self`.
		
		When `timeout` is exceeded, an exception is raised. Otherwise,
		`wait()` returns self.
		
		```python3
		client.starts().wait()  # default timeout: maximum 1 second.
		client.starts().wait(3) # allow up to 3 seconds timeout.
		```
		
		"""
		if self.threaded:
			trix.wait(timeout, lambda: self.active, runner=self.name, **k)
		return self
	
	
	
	
	
	
	# ----------------------------------------------------------------
	#
	# RUN
	#
	# ----------------------------------------------------------------
	def run(self):
		"""
		Loop while self.running is True, calling 	`urgent()` and `io()`,
		and `cio()` when a control port is specified.
		"""
		
		#
		# --------- PREPARE TO RUN ---------
		#
		
		# open()
		if not self.active:
			self.open()
		
		# mark object as running
		self.__running = True
		
		# Call self.cio() only in cases where event loop if a control 
		xio = [self.io]
		if self.csock:
			xio.append(self.cio)
		
		self.__threadid = thread.get_ident()
		
		
		#
		# --------- MAIN LOOP ---------
		#
		
		while self.__running:
			#
			# Call the `io()` method, and `self.cio()` if applicable.
			#
			for fn in xio:
				fn()
			
			#
			# Manage pause-state. This prints any data that was buffered
			# while the object was in the paused state.
			#
			ps = self.paused()
			if self.__pausestate != ps:
				
				with thread.allocate_lock() as alock:
					self.__pausestate = ps
					if ps:
						self.on_pause()
					else:
						self.flushbuffer()
						self.on_resume()
			
			#
			# sleep a little, now that we're out of the lock
			#
			time.sleep(self.sleep)
		
		
		
		#
		# I THINK THIS (BELOW) WAS A MISTAKE.
		# Like this, we can't stop a server briefly then start it 
		# running again. It's dead after it is stopped because of the
		# call to `self.shutdown` and setting csock to none.
		#
		# MAKE A BACKUP OF THIS AND...
		# Try using it a while without shutting down on `stop`. I think
		# shutting down on `stop` is against the rules. Use `shutdown` 
		# to permanently close out the whole runner-based object.
		#
		# NOTE: This may require some attention in `Process`, I'm really
		#       not sure. This should be looked into!
		#
		
		# Once processing is finished, `close()` and `stop()`.
		
		# BUT PROCESSING ISN'T NECESSARILY FINISHED HERE.
		# START CAN BE CALLED AFTER STOP. THAT SOCKET SHOULD
		# SIT THERE UNTIL I'M READY FOR IT AGAIN.
		#
		# COMMENTING: 20201023
		#
		# if self.active:
		# 	self.shutdown()
		# 	self.__csock = None
		 
	
	# ----------------------------------------------------------------
	#
	# IO 
	#  - This io() method must be overridden to perform the 
	#    functionality for which the subclass is intended.
	#
	# ----------------------------------------------------------------
		
	def io(self):
		"""
		For a Runner object, this method does absolutely nothing. All
		subclasses must override this method to perform repeating tasks
		once for each pass through `io()`.
		
		IMPORTANT: Never use `print()` to print output from the `io` 
		           method. Always use the `output` method. Output appends
		           self.newl by default - pass '' if you want to aviod
		           auto-appended CR and/or LF.
		"""
		pass
	
	
	# ----------------------------------------------------------------
	#
	# STOP
	#
	# ----------------------------------------------------------------
	def stop(self):
		"""Stop the run loop."""
		self.__running = False
		self.__threaded = False
	
	
	# ----------------------------------------------------------------
	#
	# CLOSE
	#
	# ----------------------------------------------------------------
	def close(self):
		"""
		This placeholder is called on object deletion. It may be called
		anytime manually, but you should probably call .stop() first if
		the object is running. 
		
		Subclasses may call `close()` from an overridden `stop()` method,  
		but `Runner` itself shouldn't. 
		
		In any case, it's very important to call Runner.close() from
		subclasses so that the active flag will be set to false.
		
		"""
		self.__active = False
	
	
	
	# ---- handle CPORT socket queries -----
	
	# ----------------------------------------------------------------
	# CPORT-IO
	# ----------------------------------------------------------------
	def cio(self):
		"""
		Control IO method. This is called each pass through the run loop,
		but only when this Runner is operating in a remote process 
		initiated by a controlling process. (That is, the main process
		spawned a new trix process in which this Runner is operating.)
		
		This is called regularly, regardless of pause-state, when a
		remote socket controls cport.
		"""
		
		# read the control socket and feed data to the line queue
		c = self.csock.read()
		self.__lineq.feed(c)
		
		# read and handle lines from controlling process
		q = self.__lineq.readline()
		while q:
			# get query response
			r = self.query(q)
			
			# package and send reply
			if not r:
				r = dict(query=q, reply=None, error='unknown-query')
			
			# write the query back to the caller
			self.csock.writeline(self.__jformat(r))
			
			# read another line (returns None when done)
			q = self.__lineq.readline()
		
	
	# QUERY
	def query(self, q):
		"""
		Answer a query from a controlling process. Responses are always
		sent as JSON dict strings.
		
		Override this method in subclasses that can run in an external
		process, adding commands your class should respond to.
		"""
		if q:
			q = q.strip()
			if q == 'ping':
				return dict(query=q, reply='pong')
			elif q == 'status':
				return dict(query=q, reply=self.status())
			elif q == 'shutdown':
				# shutdown, returning the new status
				self.shutdown()
				r = dict(query=q, reply=self.status())
				return r
	
	
	# ---- callbacks (for subclasses) -----
	
	def on_pause(self):
		pass
	
	def on_resume(self):
		pass
	
	
	# ---- utility -----
	
	# START
	def start(self):
		"""Start running in a new thread."""
		try:
			if not self.__threaded:
				trix.start(self.run)
				self.__threaded = True
		except Exception as ex:
			msg = "err-runner-except;"
			trix.log(msg, str(ex), ex.args, type=type(self), xdata=xdata())
			self.stop()
			raise
	
	# STARTS - Start and return self
	def starts(self):
		"""Start running in a new thread; returns self."""
		self.start()
		return self
	
	
	# SHUTDOWN
	def shutdown(self):
		"""Stop and close."""
		with thread.allocate_lock():
			try:
				self.stop()
				self.close()
			except Exception as ex:
				msg = "Runner.shutdown error;"
				trix.log(msg, str(ex), ex.args, type=type(self))
				raise
	
	
	# STATUS
	def status(self):
		"""Return a status dict."""
		#
		# I guess any class that can be managed by Console should
		# include this "cgroup" key in it's status. That's how we'll 
		# recognized classes that Console can manage.
		#
		# For now, of course, only Runner (and it's subclasses) may be
		# managed by Console.
		#
		return dict(
			cgroup   = "Runner",       # console grouping
			ek       = self.ek,        # encoding/errors
			active   = self.active,    # active state (true after 'open')
			running  = self.running,   # running state (true after 'run')
			threaded = self.threaded,  # threaded state (true after 'start')
			threadid = self.threadid,  # threadid, or None when not running
			sleep    = self.sleep,     # sleep time between calls to io
			config   = self.config,    # REMOVE THIS!
			cport    = self.__cport,   # control port for remote processes
			name     = self.name,      # name as given to constructor  
			paused   = self.paused(),  # True if Output paused, else False
			newl     = self.newl,      # Output new-line char(s)
			target   = self.target     # Output target stream
		)
	
	
	# DISPLAY
	def display(self):
		"""Print status in json display format."""
		trix.display(self.status())
	
	
	
	#
	# EXPERIMENTAL
	#  - Try a console
	#
	def console(self):
		"""
		Pause all output from the `Output` class and run a console session 
		that wraps this object by default.
		"""
		# REM: pause and resume are classmethods
		Console(wrap=self).console()

