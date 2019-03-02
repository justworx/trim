#
# Copyright 2019 justworx
# This file is part of the trix project, distributed under the terms 
# of the GNU Affero General Public License.
#

from ...fs import *


d = Path(trix.innerpath()).dir()
assert("LICENSE" in d.ls())



