#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from . import *
import locale

class loc(cline):
	"""
	Return a locale conversion dict for the given language.
	
	```
	python3 -m trix loc en_CA.UTF_8
	
	```
	"""
	
	def __init__(self):
		
		cline.__init__(self)
		
		xsig = sig = self.args[0]
		try:
			LC,Enc = sig.split(".")
			LS = LC.split("_")
			LC = "%s_%s" % (LS[0].lower(), LS[1].upper())
			Enc = trix.ncreate("util.enchelp.EncodingHelper", encoding=Enc)
			sig = "%s.%s" % (LC, Enc.encoding)
		except Exception as ex:
			raise ValueError("Invalid Signature", xdata(pyerr=str(ex),
					original_signature=xsig, sig=sig
				))
		
		locale.setlocale(locale.LC_ALL, sig)
		
		rdict = {}
		
		# think about joining all these dicts into one...
		rdict['locale'] = sig
		rdict['loconv'] = locale.localeconv()
		rdict['format'] = {
			"datetime" : locale.nl_langinfo(locale.D_T_FMT),
			"date" : locale.nl_langinfo(locale.D_FMT),
			"time" : locale.nl_langinfo(locale.T_FMT),
			"ampm" : locale.nl_langinfo(locale.T_FMT_AMPM),
			"era" : locale.nl_langinfo(locale.ERA)
		}
		
		trix.display(rdict)
		
