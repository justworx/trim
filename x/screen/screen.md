


# The `Screen` Class

This is an attempt to create an easy-to-use screen-controling object.
I don't really know much about curses, so it'll probably be a while
before it becomes useful. However, it's fascinating and fun, so I'm
going to spend some time on it now and then.


#### Where are we?

The BaseScreen class lays out the basic structure for operation. 
Any given args/kwargs are stored, but the object does nothing until
`start()` is called. Subclasses may override `prepare()`, which is 
called once before the main loop begins calling `io()` repeatedly.
When the main loop exits, `cleanup()` is called.

The Screen class currently has nothing to add to BaseScreen. The
intention is to add configuration to Screen, leaving BaseScreen as
a helpful starting point for unusually structured subclasses. Screen
should be useful for more typically needed features such as:
 
 * selecting items from a menu
 * displaying and/or entering text
 * presenting data in some kind of report format
 * viewing/manipulating grids/tables
 * entering complex form data


```python3

from trix.x.screen import *
s = Screen()
s.start()

```


#### Some Examples

I'll try to put some examples here - maybe that will help guide
forward progress. 

The following examples (until this notice is removed) come in 
reverse order so the simplest will be at the bottom.



###### Screen/Window Dimensions

```python3

from trix.x.screen import *
class ScreenDim(Screen):
	"""Show some dimensions - always y/x, the curses way."""
	
	termsize = trix.nvalue("util.terminfo.termsize")
	
	def prepare(self):
		curses.curs_set(0)
	
	def io(self):
		self.ss.clear()
		
		yx = self.ss.getyx()
		maxyx = self.ss.getmaxyx()
		paryx = self.ss.getparyx()
		cyx = [curses.LINES, curses.COLS]
		trmyx = self.termsize()
		
		self.ss.addstr(1, 1, '   yx = %s' % str(yx))
		self.ss.addstr(2, 1, 'maxyx = %s' % str(maxyx))
		self.ss.addstr(3, 1, 'paryx = %s' % str(paryx))
		self.ss.addstr(4, 1, 'curyx = %s' % str(cyx))
		self.ss.addstr(5, 1, 'trmyx = %s' % str(trmyx))
		
		self.ss.refresh()


s = ScreenDim()
s.start()

```




###### A UnixTime Seconds Counter


```python3

from trix.x.screen import *

class UnixTime(Screen):
	
	def prepare(self):
		curses.curs_set(0)
	
	def io(self):
		# clear
		self.ss.clear()
		
		# print the current time.time()
		self.ss.addstr(1, 1, 'Time: %s' % str(time.time()))
		
		# refresh the screen
		self.ss.refresh()

s = UnixTime()
s.start()

```










###### Crazy, Broken IO Events Test/Dev Thing

This may be a bit tentative. I'm mostly using it as a stepping-stone
for figuring out how to handle events (getch) generically.

It doesn't work - I'm keeping it here in case I decide to play more
with it later.

```python3

from trix.x.screen import *
class ScreenEvents(Screen):
	def __init__(self):
		self.edict = {}
		event = trix.nconfig("x/screen/eventdesc.json")
		cwrap = trix.ncreate("util.wrap.Wrap", curses)
		for e in event:
			try:
				e.append(cwrap(e[0]))
				self.edict[e[0]] = e
			except KeyError:
				# skip KEY_Fn
				pass
	
	def on_event(self, e):
		try:
			L = self.edict[e] # get a list from the dict
			print("%s: %s # %s" % (str(e), str(L[0]), str(L[1])))
		except Exception as ex:
			print("%s: ERROR %s" % (str(e), str(ex)))


s = ScreenEvents()
s.start()

```




