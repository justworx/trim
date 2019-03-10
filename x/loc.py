#
# Copyright 2018 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#

from .. import *
import locale


class BaseLocale(object):
	"""Base for Locale and AltLocale subclasses."""
	

class Locale(BaseLocale):
	"""
	Locale wraps the locale module's features. It's intended for use
	when generating output expected by the user of *this* application.
	There should be only one Locale object in any given application; it
	should be created when the application starts and persist through
	the process runtime.
	
	To generate output strings in this app that contain formmatting for
	other locales, use AltLocal.
	"""


class AltLocal(BaseLocale):
	"""
	AltLocale allows data formatting expected in other locales. Many 
	AltLocale objects may be created, used, and discarded during the
	lifespan of any given application process.
	"""
	
	
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
		locmod = trix.module("locale")
		locstr = locale or ".".join(locmod.getlocale())
		py_ver = 'python3' if sys.version_info[0]==3 else "python"
		cline = "%s -m %s loc %s" % (py_ver, trix.innerfpath(), locstr)
		
		proc = trix.popen(cline)
		jsonb = proc.communicate()[0]
		jsons = jsonb.decode("UTF_8")
		
		return trix.jparse(jsons)
		#return trix.ncreate("x.loc.Locale", trix.jparse(jsons))
