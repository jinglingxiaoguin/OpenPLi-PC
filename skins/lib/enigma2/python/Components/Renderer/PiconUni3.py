# PiconUni
# Copyright (c) 2boom 2012-16
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# 25.06.2013 added resize picon
## 18.12.2013 added picon miltipath
# 27.12.2013 added picon reference
# 27.01.2014 added noscale parameter (noscale="0" is default, scale picon is on)
# 28.01.2014 code otimization
# 02.07.2014 small fix reference
# 09.01.2015 redesign code
# 02.05.2015 add path uuid device
# 22.08.2020 code optimization for Python2 & Python3

from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, resolveFilename
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.config import *
import os.path



class PiconUni3(Renderer):
	__module__ = __name__
	def __init__(self):
		Renderer.__init__(self)
		self.path = 'piconUni'
		self.scale = '0'
		self.nameCache = {}
		self.pngname = ''

	def applySkin(self, desktop, parent):
		attribs = []
		for (attrib, value,) in self.skinAttributes:
			if (attrib == "path"):
				self.path = value
			elif attrib == 'noscale':
				self.scale = value
			else:
				attribs.append((attrib, value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if (what[0] != self.CHANGED_CLEAR):
				sname = self.source.text
				sname = sname.upper()
				pngname = self.nameCache.get(sname, "")
				if (pngname == ""):
					pngname = self.findPicon(sname)
					if (pngname != ""):
						self.nameCache[sname] = pngname
			if (pngname == ""):
				pngname = self.nameCache.get("default", "")
				if (pngname == ""):
					pngname = self.findPicon("picon_default")
					if (pngname == ""):
						tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
						if os.path.exists(tmp):
							pngname = tmp
						else:
							pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
					self.nameCache["default"] = pngname
			if (self.pngname != pngname):
				if self.scale == '0':
					if pngname:
						self.instance.setScale(1)
						self.instance.setPixmapFromFile(pngname)
						self.instance.show()
					else:
						self.instance.hide()
				else:
					if pngname:
						self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname
				self.instance.setPixmapFromFile(self.pngname)

	def findPicon(self, serviceName):
		searchPaths = []
		if os.path.exists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if line.find("/dev/sd") > -1:
					searchPaths.append(line.split()[1].replace("\\040", " ") + "/%s/")
		searchPaths.append("/usr/share/enigma2/%s/")
		for path in searchPaths:
			pngname = (((path % self.path) + serviceName) + ".png")
			if os.path.exists(pngname):
				return pngname
		return ""
