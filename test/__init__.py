#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from .. import *


def banner(text):
	"""Pass text to display in a banner"""
	print("\n*\n*\n* TESTING: %s\n*" % text)

def footer():
	print("* --> OK\n*\n*\n")


banner("Module: `trix`")
from . import trix
footer()

banner("Package: `app`")
from . import app
footer()

banner("Package: `data`")
from . import data
footer()

banner("Package: `fmt`")
from . import fmt
footer()

banner("Package: `fs`")
from . import fs
footer()

banner("Package: `net`")
from . import net
footer()

banner("Package: `propx`")
from . import net
footer()

banner("Package: `util`")
from . import util
footer()

