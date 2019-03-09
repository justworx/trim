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
