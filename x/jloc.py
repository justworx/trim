#
# Copyright 2018-2019 justworx
# This file is part of the trix project, distributed under
# the terms of the GNU Affero General Public License.
#


from ..util.loc import *


class Loc(BaseLocale):
	"""A Locale class that accesses asset data."""
	
	def __init__(self, loc_str):
		self.__path = self._find_loc_assets()
		self.__archive = self.__path.wrapper()
	
	
	@property
	def _asset_path(self):
		"""Return the path to the locale_json archive file."""
		return self.__path	
	
	
	@property
	def locales(self):
		"""
		Return list of available locale descriptors wrapped in a propx()
		object. (Call this as a function. See propx() help.)
		"""
		return trix.propx(self.__archive.names())
	
	
	@classmethod
	def _find_loc_assets(cls):
		
		asset_paths = [
			"%s/locale_json.tar.gz" % DEF_CACHE, 
			"%s/locale_json.zip" % DEF_CACHE,
			"assets/locale_json.tar.gz", "assets/locale_json.zip"
		]
		for apath in asset_paths:
			if trix.path(apath).exists():
				return trix.path(apath)
			"""
			try:
				return trix.path("%s/locale_json.tar.gz" % DEF_CACHE)
			except:
				pass
			"""
		
		raise ValueError("Assets not found.", xdata(error='no-such-path',
				reason="assets-not-found", suggest="download-assets",
				url="https://github.com/justworx/assets/README.md"
			))
	
		
