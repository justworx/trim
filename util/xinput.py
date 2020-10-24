#
# Copyright 2018-2020 justworx
# This file is part of the trix project, distributed under 
# the terms of the GNU Affero General Public License.
#


from .. import *
import unicodedata as ud


XINPUT_PROMPT="--> "


def xinput(prompt=XINPUT_PROMPT):
	"""
	Common text input interface for p2/p3. Normalizes result (NFC).
	Returns text exactly as entered.
	"""
	
	e = None
	try:
		r = input(prompt) # python3
	except NameError:
		import sys, locale # python2
		e = sys.stdin.encoding or locale.getpreferredencoding(True)
		r = raw_input(prompt).decode(e)
	
	# return normalized string input
	try:
		return ud.normalize('NFC', r)
	except Exception as ex:
		raise type(ex)("err-normalize-fail", xdata(e=e, text=r))
