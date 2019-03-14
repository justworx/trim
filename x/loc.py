#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class BaseLocale(object):
	"""Base for Locale and AltLoc subclasses."""
	
	#
	# This should provide a common interface so that using AltLoc
	# is the same as using Locale (though Locale will, for a while,
	# have several extra features - that is until I can figure out
	# how to reproduce them in AltLoc). I don't want to have two
	# versions of the documentation.
	#
	


class Locale(BaseLocale):
	"""
	Locale wraps the locale module's features. It's intended for use
	when generating output expected by the user of this app instance.
	There should be only one Locale object in any given process; it
	should be created when the application starts and persist through
	the process runtime.
	
	To generate output strings in this app that contain formmatting for
	other locales, use AltLocal.
	"""
	
	def __init__(self):
		pass



class AltLoc(BaseLocale):
	"""
	AltLocale allows data formatting expected in other locales. Many 
	AltLocale objects may be created, used, and discarded during the
	lifespan of any given application process.
	"""
	
	__locales = {}
	
	
	def __init__(self, loc):
		self.__loc = loc
		try:
			self.__fmt = self.__locales[loc]
		except:
			self.__locales[loc] = query_locale_dict(loc)
			self.__fmt = self.__locales[loc]
	
	
	
	#
	# We'll put classmethods at the bottom for now. Looks like there
	# are a few more coming.
	#
	@classmethod
	def query_locale_dict(cls, locale=None):
		"""
		Pass a locale string, eg., "en_US.UTF_8", etc... Returns a new
		`trix.x.loc` object containing locale format methods and data.
		"""
		
		cline = "%s -m %s loc -cx %s" % (
				sys.executable, trix.innerfpath(), locale
			)
		
		proc = trix.popen(cline)
		jsonx = proc.communicate()[0]
		print(jsonx)
		
		"""
		jsonb = trix.ncreate('util.compenc.expand', jsonx)
		jsons = jsonb.decode("UTF_8")
		
		return trix.jparse(jsons)
		"""
		#return trix.ncreate("x.loc.Locale", trix.jparse(jsons))
