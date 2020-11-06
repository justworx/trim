#
# Copyright 2020 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

#
# NOTE: This code appears in several places throughout the trix
#       package. I want them all to turn here for the ability to
#       parse ast and/or json.
#


from .enchelp import *
import ast


class Parser(EncodingHelper):
	"""
	Parse json or ast text to an object, eg., dict, list, etc.
	
	The Parser class is based on EncodingHelper, so pass encoding
	and/or errors keyword arguments.
	"""
	
	def __init__(self, **k):
		"""
		Parse JSON or AST text.
		
		Pass encoding (default: DEF_ENCODE),
		and  errors   (default: DEF_ERRORS)
		
		Call `parse()` passing JSON or AST parsable text.
		
		Returns the corresponding python object.
		
		"""
		k.setdefault("encoding", DEF_ENCODE)
		k.setdefault("errors", DEF_ERRORS)
		EncodingHelper.__init__(self, **k)
	
	
	def parse(self, text):
		"""
		Pass the text to parse.
		
		EXAMPLE
		>>> from trix.util.parse import *
		>>> p = Parser()
		>>> t = "['1','9', '10']"
		>>> p.parse(t)
		"""
		
		#
		# REM: This is EncodingHelper's decode method, so it won't
		#      break if the text is already unicode.
		#
		text = self.decode(text)
		try:
			try:
				#
				# check in python2 to see if this is necessary
				# (and put in a try/except if it is!)
				#
				#txt = EncodingHelper(**k).decode()
				#
				return ast.literal_eval(text)
			except:
				# this should cause a exception that gives a line number
				compile(text, text, 'eval')
				raise # if not, raise anyway
		
		except BaseException as ast_ex:
			# ast failed - try json
			try:
				return json.loads(text)
			except BaseException as json_ex:
				raise Exception ("parse-error", xdata(text=text, 
					json = {"type" : type(json_ex), "args" : json_ex.args},
					ast  = {"type" : type(ast_ex),  "args" : ast_ex.args}
				))
