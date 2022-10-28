import os
from io       import open as ioOpen
from json      import loads as jLoads, dumps as iDumps
from glob      import glob as iGlob
from re       import match as iMatch, escape as iEscape
from re       import sub as iSub, subn as iSubn, split as iSplit
from re       import search as iSearch, compile as iCompile
from re       import findall as iFindall, finditer as iFinditer
from re       import IGNORECASE
from math      import floor as iFloor, ceil as iCeil, log as iLog
from time      import localtime, mktime, strftime, time as iTime
from time      import sleep as iSleep
from threading     import Thread as iThread, enumerate as iEnumerate
from datetime     import datetime, timedelta
from base64      import b64encode, b64decode
from skin      import parseColor
from Tools.Directories   import fileExists, pathExists, crawlDirectory
from Tools.Directories   import resolveFilename, SCOPE_PLUGINS
from Plugins.Plugin    import PluginDescriptor
from Screens.Screen    import Screen
from Screens.ChannelSelection import ChannelContextMenu
from Screens.ChannelSelection import service_types_tv, service_types_radio
from Screens.InfoBar   import InfoBar
from Tools.BoundFunction  import boundFunction as BF
from Tools.LoadPixmap   import LoadPixmap
from Components.PluginComponent import plugins as iPlugins
from Components.Harddisk  import harddiskmanager
from Components.Label   import Label
from Components.ScrollLabel  import ScrollLabel
from Components.Button   import Button
from Components.MenuList  import MenuList
from Components.ActionMap  import ActionMap
from Components.Pixmap   import Pixmap
from Components.MultiContent import MultiContentEntryText
from Components.NimManager  import nimmanager
from Components.Slider   import Slider
from enigma      import getDesktop, ePoint, eSize, gFont, eRect
from enigma      import eTimer, eDVBDB, fontRenderClass
from enigma      import iServiceInformation
from enigma      import eServiceReference, eServiceCenter
from enigma      import eListboxPythonMultiContent
from enigma      import RT_HALIGN_LEFT as LEFT
from enigma      import RT_HALIGN_CENTER as CENTER
from enigma      import RT_VALIGN_CENTER
from Components.ConfigList  import ConfigListScreen
from Components.config   import config, ConfigSubsection, configfile
from Components.config   import getConfigListEntry, ConfigDirectory
from Components.config   import ConfigYesNo, ConfigElement, ConfigText
from Components.config   import ConfigSelection, ConfigSelectionNumber
from Components.config   import ConfigSubList, ConfigInteger
import importlib
try:  import tarfile as iTar
except: iTar = None
try:  import zipfile as iZip
except: iZip = None
try: from xml.etree import ElementTree as iElem
except: iElem = None
try: from shutil import move as iMove, copyfile as iCopyfile
except: iMove = iCopyfile = None
try:
 from urllib.request import Request as iRequest, urlopen as iUrlopen, build_opener, install_opener, HTTPPasswordMgrWithDefaultRealm, HTTPDigestAuthHandler, HTTPHandler
 from urllib.error import URLError as iURLError
 from urllib.parse import unquote as iUnquote, quote as iQuote
 from urllib.parse import urlparse as iUrlparse, parse_qs as iUrlparse_qs
except:
 try:
  from urllib.request import Request as iRequest, urlopen as iUrlopen, build_opener, install_opener, HTTPPasswordMgrWithDefaultRealm, HTTPDigestAuthHandler, HTTPHandler
  from urllib.error import URLError as iURLError
  from urllib.parse import unquote as iUnquote, quote as iQuote, urlparse as iUrlparse, parse_qs as iUrlparse_qs
 except:
  iRequest = iUrlopen = iURLError = iUnquote = iQuote = iUrlparse = build_opener = install_opener = HTTPPasswordMgrWithDefaultRealm = HTTPDigestAuthHandler = HTTPHandler = None
PLUGIN_NAME    = "AJPanel"
PLUGIN_DESCRIPTION  = "Enigma2 Tools"
VV73TT   = "v7.1.0"
VVNDdR    = "20-09-2022"
EASY_MODE    = 0
VV8FUX   = 0
VVaEAu   = 0
VV9VaA  = resolveFilename(SCOPE_PLUGINS, base="Extensions/")
VVuVce  = resolveFilename(SCOPE_PLUGINS, base="SystemPlugins/")
VVCnD5    = "/media/usb/"
VVzIQa    = "/usr/share/enigma2/picon/"
VVhyQq = "/etc/enigma2/blacklist"
VV609C   = "/etc/enigma2/"
VVJNDG  = "ajpanel_update_url"
VV0A4Z   = "AJPan"
VVXLG3  = "AUTO FIND"
VV1nAS  = "Custom"
VVDZkF    = ""
VVFwML    = "Regular"
VVZ1aI      = "-" * 80
VVm77t    = ("-" * 100, )
VVyQYx    = ""
VVrML3   = " && echo 'Successful' || echo 'Failed!'"
VVwFJG    = []
VVCYwM  = "Cannot continue (No Enough Memory) !"
VVF5vz  = False
VVPJLC  = False
VVe9cu = False
VVoxS0     = 0
VVJ7n1    = 1
VV7ebZ    = 2
VVSzFu   = 3
VVEgON    = 4
VVCyHa    = 5
VVhfwD = 6
VV0L7B = 7
VVm2aL  = 8
VVV9ui   = 9
VV3nyh  = 10
VVOdhH  = 11
VV4ccg    = 12
VVbZAe   = 13
VV4yep   = 14
VV1GIX    = 15
VVmOpB    = 16
VVnacN  = 17
VVw3Mn   = 0
VV72id   = 1
VVtPPw   = 2
def FFBl25():
 fList = None
 try:
  from enigma import getFontFaces
  return set(getFontFaces())
 except:
  try:
   from skin import getFontFaces
   return set(getFontFaces())
  except:
   pass
 return [VVFwML]
config.plugins.AJPanel = ConfigSubsection()
CFG = config.plugins.AJPanel
CFG.showInMainMenu    = ConfigYesNo(default=False)
CFG.showInExtensionMenu   = ConfigYesNo(default=True)
CFG.showInChannelListMenu  = ConfigYesNo(default=True)
CFG.EventsInfoMenu    = ConfigYesNo(default=True)
CFG.keyboard     = ConfigSelection(default="v", choices=[ ("v", "Virtual Keyboard"), ("s", "System Default") ])
CFG.FileManagerExit    = ConfigSelection(default="d", choices=[ ("d", "Directory Up"), ("e", "Exit File Manage") ])
CFG.hotkey_signal    = ConfigSelection(default="lesc", choices=[ ("off", "Disabled"), ("lok", "Long-OK"), ("lesc", "Long-Exit"), ("lred", "Long-Red") ])
CFG.epgLanguage     = ConfigSelection(default="off", choices=[ ("off", "Original"), ("en", "English"), ("ar", "Arabic") ])
CFG.iptvAddToBouquetRefType  = ConfigSelection(default="4097", choices=[ ("1", "1 (DVB Stream)"), ("4097", "4097 (servicemp3)"), ("5001", "5001 (GST Player)"), ("5002", "5002 (Ext-3 EPlayer)"), ("8192", "8192 (HDMI input)"), ("8193", "8193 (eServiceUri)") ])
CFG.autoResetFrozenIptvChan  = ConfigYesNo(default=True)
CFG.hideIptvServerAdultWords = ConfigYesNo(default=False)
CFG.hideIptvServerChannPrefix = ConfigYesNo(default=False)
CFG.iptvHostsMode    = ConfigDirectory(default=VVXLG3, visible_width=45)
CFG.iptvHostsDirs    = ConfigText(default="")
CFG.MovieDownloadPath   = ConfigDirectory(default="/media/hdd/movie/", visible_width=45)
CFG.PIconsPath     = ConfigDirectory(default=VVzIQa, visible_width=45)
CFG.backupPath     = ConfigDirectory(default=VVCnD5, visible_width=45)
CFG.packageOutputPath   = ConfigDirectory(default="/tmp/", visible_width=45)
CFG.downloadedPackagesPath  = ConfigDirectory(default="/tmp/", visible_width=45)
CFG.exportedTablesPath   = ConfigDirectory(default="/tmp/", visible_width=45)
CFG.exportedPIconsPath   = ConfigDirectory(default="/tmp/", visible_width=45)
CFG.browserStartPath   = ConfigText(default="/")
CFG.browserBookmarks    = ConfigText(default="/tmp/,/")
CFG.browserSortMode    = ConfigInteger(default=0, limits=(0, 5))
CFG.browserSortMix    = ConfigYesNo(default=False)
CFG.signalPos     = ConfigInteger(default=5, limits=(1, 9))
CFG.playerPos     = ConfigInteger(default=0, limits=(0, 1))
CFG.signalSize     = ConfigInteger(default=3, limits=(1, 13))
CFG.mixedColorScheme   = ConfigInteger(default=4, limits=(0, 4))
CFG.checkForUpdateAtStartup  = ConfigYesNo(default=False)
CFG.playerJumpMin    = ConfigInteger(default=5, limits=(1, 10))
CFG.downloadAutoResume   = ConfigYesNo(default=True)
CFG.downloadMonitor    = ConfigYesNo(default=False)
CFG.lastTerminalCustCmdLineNum = ConfigInteger(default=0)
CFG.lastSharePickerDvbRow  = ConfigInteger(default=0)
CFG.lastSharePickerIptvRow  = ConfigInteger(default=0)
CFG.lastFileManFindPatt   = ConfigText(default="")
CFG.lastFileManFindSrt   = ConfigText(default="/media/")
CFG.lastFindTerminal   = ConfigText(default="")
CFG.lastFindServers    = ConfigText(default="")
CFG.lastFindIptv    = ConfigText(default="")
CFG.lastFindSubtitle   = ConfigText(default="")
CFG.lastFindPackages   = ConfigText(default="")
CFG.lastFindServices   = ConfigText(default="")
CFG.lastFindSatName    = ConfigText(default="")
CFG.lastFindContextFind   = ConfigText(default="")
CFG.lastFindEditor    = ConfigText(default="")
CFG.lastFindGeneral    = ConfigText(default="")
tmp = [("srt", "From SRT File"), ("#FFFFFF", "White"), ("#C0C0C0", "Silver"), ("#808080", "Gray"), ("#000000", "Black"), ("#FF0000", "Red"), ("#800000", "Maroon"), ("#FFFF00", "Yellow"), ("#808000", "Olive"), ("#00FF00", "Lime"), ("#008000", "Green"), ("#00FFFF", "Aqua"), ("#008080", "Teal"), ("#0000FF", "Blue"), ("#000080", "Navy"), ("#FF00FF", "Fuchsia"), ("#800080", "Purple")]
CFG.subtDelaySec    = ConfigSelectionNumber(default=0, stepwidth=1, min=-600, max=600, wraparound=False)
CFG.subtBGTransp    = ConfigSelectionNumber(default=100, stepwidth=10, min=0, max=100, wraparound=False)
CFG.subtTextFg     = ConfigSelection(default="#FFFFFF", choices=tmp)
CFG.subtTextFont    = ConfigSelection(default=VVFwML, choices=[ (x,  x) for x in FFBl25() ])
CFG.subtTextSize    = ConfigSelectionNumber(default=50, stepwidth=5, min=30, max=100, wraparound=False)
CFG.subtTextAlign    = ConfigSelection(default="1", choices=[ ("0", "Left"), ("1", "Center"), ("2", "Right") ])
CFG.subtShadowColor    = ConfigSelection(default="#000080", choices=tmp[1:])
CFG.subtShadowSize    = ConfigSelectionNumber(default=5, stepwidth=1, min=0, max=10, wraparound=False)
CFG.subtVerticalPos    = ConfigSelectionNumber(default=90, stepwidth=1, min=0, max=100, wraparound=False)
del tmp
def FFMT5Y():
 mode = CFG.mixedColorScheme.getValue()
 if mode == 4:
  VVDz1F  = 0 == os.system("if which systemctl > /dev/null 2>&1; then exit 0; else exit 1; fi")
  VVOXAJ = 0 == os.system("if grep -q 'open.*vision' /etc/issue; then exit 0; else exit 1; fi")
  if  VVDz1F  : return 0
  elif VVOXAJ : return 1
  else    : return 3
 else:
  return max(min(3, mode), 0)
COLOR_SCHEME_NUM = FFMT5Y()
VVjrAG = VVkXS4 = VVzZva = VVMmz2 = VVU8eD = VVTdoW = VVYje8 = VVhR0y = VV9cEK = VVk6tE = VVdWFT = VVoTT6 = VVpHwQ = VVNTmM = VVyFMl = VVZgqQ = ""
def FFqRzv()  : FFr6Fa(FFWSwj())
def FFq5Ar()  : FFr6Fa(FFQo1C())
def FFMqnp(tDict): FFr6Fa(iDumps(tDict, indent=4, sort_keys=True))
def FFSKu7(*args): FFAYnq(True, False, *args)
def FFr6Fa(*args) : FFAYnq(True , True , *args)
def FFgOVc(*args): FFAYnq(False, True , *args)
def FFAYnq(addSep=True, oneLine=True, *args):
 if VV8FUX:
  sep = (">>>> %s\n" % ("#" * 80)) if addSep else ""
  txt = sep
  if oneLine:
   cr = "\n" if addSep else ""
   txt += ">>>> %s%s" % (" , ".join(list(map(str, args))), cr)
  else:
   for item in args:
    if isinstance(item, list) or isinstance(item, tuple):
     txt += ">>>> LIST START <--\n"
     for itm in item:
      txt += ".... %s\n" % str(itm)
     txt += ">>>> LIST END <--\n"
    else:
     txt += "---> %s\n" % str(item)
  txt += sep.replace("#", "-")
  os.system("cat << '_EOF' \n" + str(txt) + "\n_EOF")
def FFPrk0(txt, isAppend=True, ignoreErr=False):
 if VV8FUX:
  tm = FFdyoU()
  err = ""
  if not ignoreErr:
   err = FFQo1C()
  fileName = "/tmp/ajpanel_log.txt"
  with open(fileName, "a" if isAppend else "w") as f:
   if err:
    f.write(err)
   f.write("%s >> %s\n" % (tm, str(txt)))
  if err:
   FFr6Fa(err)
  FFr6Fa("Output Log File : %s" % fileName)
def FFQo1C():
 try:
  from traceback import format_exc, format_stack
  trace = format_exc()
  if trace and len(trace) > 5:
   tm = FFdyoU()
   stack = format_stack()[:-1]
   sep = "*" * 70
   err = "\n%s\n*** %s\n%s\n\n" % (sep, tm, sep)
   err += "%s\n\n%s\n%s\n" % ("".join(stack), trace, sep)
   return err
 except:
  return "Cannot Trace !"
def FFWSwj():
 import inspect
 lst = []
 for ndx, f in enumerate(inspect.stack()):
  if ndx > 0:
   lst.append("%s >> %s" % (os.path.basename(f[1]), f[3]))
 return "Last Fncs:\n" + "\n".join(lst)
VVaRWp = 0
def FFm8xK():
 global VVaRWp
 VVaRWp = iTime()
def FF5X2v(txt=""):
 FFr6Fa(">>>>>> Elapsed : %s sec\t%s" % (("%.6f" % (iTime() - VVaRWp)).rstrip("0"), txt))
VVwFJG = []
def FFqx5h(win):
 global VVwFJG
 if not win in VVwFJG:
  VVwFJG.append(win)
def FFSJQP(*args):
 global VVwFJG
 for win in VVwFJG:
  try:
   win.close()
  except:
   pass
 VVwFJG = []
def FFYLWi():
 BT_SCALE = BT_KEEP_ASPECT_RATIO = None
 try:
  from enigma import BT_SCALE, BT_KEEP_ASPECT_RATIO
 except:
  try  : from enigma import BT_SCALE, BT_FIXRATIO as BT_KEEP_ASPECT_RATIO
  except : pass
 if BT_SCALE and BT_KEEP_ASPECT_RATIO: return BT_SCALE | BT_KEEP_ASPECT_RATIO
 else        : return None
VVlTBS = FFYLWi()
def getDescriptor(fnc, where, name=PLUGIN_NAME, descr="", needsRestart=False):
 w = getDesktop(0).size().width()
 if w and w < 1920 : icon="icon.png"
 else    : icon="iconhd.png"
 if not descr: descr = PLUGIN_DESCRIPTION
 else  : descr = "%s %s" % (PLUGIN_NAME, descr)
 return PluginDescriptor(fnc=fnc, where=where, needsRestart=needsRestart, name=name, description=descr, icon=icon)
def FFN09A()     : return PluginDescriptor(fnc=FFBZFC, where=[PluginDescriptor.WHERE_SESSIONSTART] , needsRestart=True   , description="AJPanel Startup")
def FFhBib()      : return getDescriptor(FFwCZt   , [ PluginDescriptor.WHERE_PLUGINMENU  ] , needsRestart=True)
def FF0Yba()       : return getDescriptor(FFGJCR  , [ PluginDescriptor.WHERE_MENU    ] , PLUGIN_NAME     , descr="Main Menu")
def FFoK0z()   : return getDescriptor(FFTcrJ , [ PluginDescriptor.WHERE_EXTENSIONSMENU ] , "AJ File Manager"   , descr="File Maneger")
def FFoLGY(): return getDescriptor(FFNjPC , [ PluginDescriptor.WHERE_EXTENSIONSMENU ] , "AJ Signal/Player"  , descr="Signal Monitor / Player")
def FFhLkM()  : return getDescriptor(FFqswZ  , [ PluginDescriptor.WHERE_EXTENSIONSMENU ] , "AJ IPTV"     , descr="IPTV Menu")
def FFpzdz()     : return getDescriptor(FF6tDv , [ PluginDescriptor.WHERE_EVENTINFO  ] , "AJ Info."    , descr="Service Info")
def Plugins(**kwargs):
 result = [ FFhBib() , FF0Yba() , FFN09A() ]
 if CFG.showInExtensionMenu.getValue():
  result.append(FFoK0z())
  result.append(FFoLGY())
  result.append(FFhLkM())
 if CFG.EventsInfoMenu.getValue():
  result.append(FFpzdz())
 return result
def FFBZFC(reason, **kwargs):
 if reason == 0:
  FFIfnO()
  if "session" in kwargs:
   session = kwargs["session"]
   FFyn0O(session)
   CCoAK5(session)
def FFGJCR(menuid, **kwargs):
 if menuid == "mainmenu" and CFG.showInMainMenu.getValue():
  return [(PLUGIN_NAME, FFwCZt, PLUGIN_NAME, 45)]
 else:
  return []
def FFwCZt(session, **kwargs):
 session.open(Main_Menu)
def FFTcrJ(session, **kwargs):
 session.open(CC7ujK)
def FFNjPC(session, **kwargs):
 FF3bCE(session, isFromSession=True)
def FFqswZ(session, **kwargs):
 session.open(CCqQHV)
def FF6tDv(session, **kwargs):
 session.open(CCARMv, fncMode=CCARMv.VVTlHJ)
def FFnm9f():
 FFbqIb(CFG.showInExtensionMenu.getValue(), iPlugins.getPlugins(PluginDescriptor.WHERE_EXTENSIONSMENU), [ FFoK0z(), FFoLGY(), FFhLkM() ])
 FFbqIb(CFG.EventsInfoMenu.getValue(), iPlugins.getPlugins(PluginDescriptor.WHERE_EVENTINFO), [ FFpzdz() ])
def FFbqIb(setVal, pluginList, dList):
 try:
  if setVal:
   for item in dList:
    if not item in pluginList:
     iPlugins.addPlugin(item)
  else:
   for item in dList:
    if item in pluginList:
     iPlugins.removePlugin(item)
 except:
  pass
VVRoZ5 = None
def FFIfnO():
 try:
  global VVRoZ5
  if VVRoZ5 is None:
   VVRoZ5    = ChannelContextMenu.__init__
  ChannelContextMenu.__init__   = FFk8QX
  ChannelContextMenu.FFhwN1 = FFhwN1
 except:
  pass
def FFk8QX(SELF, session, csel):
 from Components.ChoiceList import ChoiceEntryComponent
 VVRoZ5(SELF, session, csel)
 if CFG.showInChannelListMenu.getValue():
  title1 = PLUGIN_NAME + " - Find"
  title2 = PLUGIN_NAME + " - Channels Tools"
  SELF["menu"].list.insert(0, ChoiceEntryComponent(key=" ", text=(title2 , BF(SELF.FFhwN1, title2, csel, isFind=False))))
  SELF["menu"].list.insert(0, ChoiceEntryComponent(key=" ", text=(title1 , BF(SELF.FFhwN1, title1, csel, isFind=True))))
def FFhwN1(self, title, csel, isFind):
 refCode = servName = bouquetRoot = ""
 try:
  currSel  = csel.getCurrentSelection()
  bouquetRoot = csel.getRoot().toString()
  refCode  = currSel.toString()
  servName = FFy0JC(refCode)
 except:
  pass
 self.session.open(BF(CC7Gx2, title=title, csel=csel, refCode=refCode, servName=servName, bouquetRoot=bouquetRoot, isFind=isFind))
 self.close()
def FFyn0O(session):
 hk = ActionMap(["KeyMap_HK"])
 hk.execBegin()
 hk.actions['longOK']  = BF(FFSCE9, session, "lok")
 hk.actions['longCancel'] = BF(FFSCE9, session, "lesc")
 hk.actions['longRed']  = BF(FFSCE9, session, "lred")
def FFSCE9(session, key):
 if CFG.hotkey_signal.getValue() == key:
  try:
   if CCWsdR.VVlcTS:
    CCWsdR.VVlcTS.close()
   if not CCppdx.VVKGP0:
    CCppdx.VVgElN(session, isFromExternal=True)
  except:
   pass
def FFnT3A(confItem, val):
 confItem.setValue(val)
 confItem.save()
 configfile.save()
def FFJd2Z(SELF, title="", addLabel=False, addScrollLabel=False, VV625J=None, addCloser=False):
 Screen.__init__(SELF, SELF.session)
 if title == "" : title = FFNUl9()
 else   : title = "  %s  " % title
 SELF["myTitle"] = Label(title)
 SELF["myBody"] = Label()
 SELF["myInfoFrame"] = Label()
 SELF["myInfoBody"] = Label()
 SELF["myInfoFrame"].hide()
 SELF["myInfoBody"].hide()
 btnMode = SELF.skinParam["topRightBtns"]
 if btnMode in (1, 2): SELF["keyMenu"] = Pixmap()
 if btnMode in (2, 3): SELF["keyInfo"] = Pixmap()
 if SELF.skinParam["barHeight"] > 0:
  SELF["myBar"]  = Label()
  SELF["myLine"]  = Label()
  SELF["keyRed"]  = Label()
  SELF["keyGreen"] = Label()
  SELF["keyYellow"] = Label()
  SELF["keyBlue"]  = Label()
  SELF["keyRed"].hide()
  SELF["keyGreen"].hide()
  SELF["keyYellow"].hide()
  SELF["keyBlue"].hide()
 if addLabel:
  SELF["myLabel"] = Label()
 if addScrollLabel:
  SELF["myLabel"] = CC3sIb(SELF)
 if VV625J:
  SELF["myMenu"] = MenuList(VV625J)
  SELF["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : SELF.VVmz9T        ,
   "cancel" : SELF.close        ,
  }, -1)
 if addCloser:
  SELF["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : SELF.close ,
   "cancel"  : SELF.close ,
   "red"   : SELF.close
  }, -1)
def FFCMLR(SELF, tableObj, colNum=0):
 SELF.keyPressed = -1
 SELF["myActionMap"].actions.update({
  "0" : BF(FFjECD, SELF, "0") ,
  "1" : BF(FFjECD, SELF, "1") ,
  "2" : BF(FFjECD, SELF, "2") ,
  "3" : BF(FFjECD, SELF, "3") ,
  "4" : BF(FFjECD, SELF, "4") ,
  "5" : BF(FFjECD, SELF, "5") ,
  "6" : BF(FFjECD, SELF, "6") ,
  "7" : BF(FFjECD, SELF, "7") ,
  "8" : BF(FFjECD, SELF, "8") ,
  "9" : BF(FFjECD, SELF, "9")
 })
 from Tools.NumericalTextInput import NumericalTextInput
 SELF.numericalTextInput = NumericalTextInput(nextFunc=BF(FFvprW, SELF, tableObj, colNum))
 SELF.numericalTextInput.setUseableChars('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
def FFjECD(SELF, key):
 SELF.keyPressed = SELF.numericalTextInput.getKey(int(key))
 for group in [ "1", "2ABC", "3DEF", "4GHI", "5JKL", "6MNO", "7PQRS", "8TUV", "9WXYZ", "0" ]:
  if SELF.keyPressed in group:
   if VVZgqQ:
    txt = " ".join(group)
    txt = txt.replace(SELF.keyPressed, VVZgqQ + SELF.keyPressed + VVkXS4)
    txt = VVkXS4 + txt
   else:
    sep = "    "
    txt = sep + sep.join(group) + sep
    txt = txt.replace(sep + SELF.keyPressed + sep, "   [%s]   " % SELF.keyPressed)
   FFD1yO(SELF, txt)
def FFvprW(SELF, tableObj, colNum):
 FFD1yO(SELF)
 try:
  if tableObj and tableObj.list is not None:
   for i in range(len(tableObj.list)):
    item = tableObj.list[i][colNum + 1][7].strip()
    item = item.encode().decode()
    firstChar = item.upper()[:1]
    if firstChar == SELF.keyPressed:
     SELF.VVtpKN(i)
     break
 except:
  pass
def FF1N9D(SELF, setMenuAction=True):
 if setMenuAction:
  global VVyQYx
  VVyQYx = SELF["myMenu"].l.getCurrentSelection()[0]
 return SELF["myMenu"].l.getCurrentSelection()[1]
def FFNUl9():
 return ("  %s" % VVyQYx)
def FFHhgX(btn, txt):
 btn.setText(txt)
 if txt : btn.show()
 else : btn.hide()
def FFO8d5(txt):
 if "\c" in txt:
  txt = iSub(r"\\c(.){8}" ,"" , txt, flags=IGNORECASE)
 return txt
def FFZG1G(color):
 return parseColor(color).argb()
def FFlr8P(obj, color):
 obj.instance.setForegroundColor(parseColor(color))
 obj.instance.invalidate()
def FFobAA(obj, color):
 obj.instance.setBackgroundColor(parseColor(color))
 obj.instance.invalidate()
def FFMGhc(obj, color):
 obj.long_text.setBackgroundColor(parseColor(color))
 obj.instance.invalidate()
def FF95sl(txt, color):
 if color:
  if "/" in txt: txt = txt.replace("/", "\/")
  return " | sed 's/%s/\\%s&\%s/gI'" % (txt, color, VVZgqQ)
 else:
  return ""
def FFt615(word, color):
 if color: return "echo -e '\%s%s\n--- %s\n%s\%s';" % (color, VVZ1aI, word, VVZ1aI, VVZgqQ)
 else : return "echo -e '%s\n--- %s\n%s';" % (VVZ1aI, word, VVZ1aI)
def FFkhYI(word, color, backToColor=None):
 if backToColor : return color + word + backToColor
 else   : return color + word + VVZgqQ
def FFoEsu(color):
 if color: return "echo -e '%s' %s;" % (VVZ1aI, FF95sl(VVZ1aI, VVdWFT))
 else : return "echo -e '%s';" % VVZ1aI
def FFINY2(title, color):
 title = "%s\n%s\n%s\n" % (VVZ1aI, title, VVZ1aI)
 return FFkhYI(title, color)
def FFkCFB(menuObj, fg="#00ffffff", bg="#08005555"):
 menuObj.instance.setForegroundColorSelected(parseColor(fg))
 menuObj.instance.setBackgroundColorSelected(parseColor(bg))
def FFSEzt(menuObj):
 try:
  menuObj.instance.setHAlign(1)
 except:
  pass
def FFpoMu(callBackFunction):
 tCons = CChHJE()
 tCons.ePopen("echo", BF(FFsY5i, callBackFunction))
def FFsY5i(callBackFunction, result, retval):
 callBackFunction()
def FFlX3B(SELF, fnc, title="Processing ...", clearMsg=True):
 FFD1yO(SELF, title)
 tCons = CChHJE()
 tCons.ePopen("echo", BF(FFQgHZ, SELF, fnc, clearMsg))
def FFQgHZ(SELF, fnc, clearMsg, result, retval):
 fnc()
 if clearMsg:
  FFD1yO(SELF)
def FF3DIX(cmd):
 from subprocess import Popen, PIPE
 try:
  process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
  stdout, stderr = process.communicate()
  stdout = stdout.strip()
  stderr = stderr.strip()
  if stderr : return stderr
  else  : return stdout
 except Exception as e:
  if "memory" in str(e).lower(): return VVCYwM
  else       : return ""
def FFiGf6(cmd):
 txt = FF3DIX(cmd)
 txt = txt.splitlines()
 return list(map(str.strip, txt))
def FFj4HH(cmd):
 lines = FFiGf6(cmd)
 if lines: return lines[0]
 else : return ""
def FFJxAr(SELF, cmd):
 lines = FFiGf6(cmd)
 VVvhuK = []
 for line in lines:
  line = line.strip()
  if ":" in line:
   parts = line.split(":")
   key  = parts[0].strip()
   val  = parts[1].strip()
   VVvhuK.append((key, val))
  elif line:
   VVvhuK.append((line, ""))
 if VVvhuK:
  header   = ("Parameter" , "Value" )
  widths   = (50    , 50  )
  FF1dQ4(SELF, None, header=header, VVvytR=VVvhuK, VVoJsQ=widths, VVmp7B=28)
 else:
  FFuCjo(SELF, cmd)
def FFuCjo(    SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVPHtE=True, VVKsoz=VV72id, **kwargs)
def FFusMt(  SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, **kwargs)
def FFCa80(   SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVSzWe=True, VVccyo=True, VVKsoz=VV72id, **kwargs)
def FFKqND(  SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVSzWe=True, VVccyo=True, VVKsoz=VVtPPw, **kwargs)
def FFfbee(  SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVvnLo=True , **kwargs)
def FFufnk( SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVvFw0=True   , **kwargs)
def FFRi75( SELF, cmd, **kwargs): SELF.session.open(CCxrj2, VV6D3C=cmd, VVSpRV=True  , **kwargs)
def FFxtg8(cmd):
 return cmd + " > /dev/null 2>&1"
def FFRIHI(cmd):
 return cmd + " 2> /dev/null"
def FFYn0Q():
 return " > /dev/null 2>&1"
def FFvG4M(cmd):
 if os.system("which %s > /dev/null 2>&1" % cmd) == 0: return True
 else            : return False
def FFlfqZ(mode=0):
 if mode == 0:
  dirs = [ "*boot*", "*/ba", "/proc" ]
 else:
  dirs = [  "*boot*"
    , "*picon*"
    , "*/ba"
    , "/bin"
    , "/dev"
    , "/hdd"
    , "/lib"
    , "/linuxrc"
    , "/mnt"
    , "/newroot"
    , "/proc"
    , "/run"
    , "/sbin"
    , "/sys"
    , "/usr"
    ]
 paths = []
 for item in dirs:
  paths.append("-ipath '%s'" % item)
 txt = " -o ".join(paths)
 return "-type d \( %s \) -prune -o " % txt
def FFC2Pr():
 cmd = "if which opkg >/dev/null; then echo opkg; else if which ipkg >/dev/null; then echo ipkg; else if which dpkg >/dev/null; then echo dpkg; else echo ''; fi; fi; fi"
 return FFj4HH(cmd)
VVRq5s     = 0
VVmDYa      = 1
VVPeIJ   = 2
VVCBKn      = 3
VVpvpX      = 4
VVgetH     = 5
VV4pye     = 6
VVEoQq = 7
VVKrAC = 8
VViRav = 9
VVDDR8  = 10
VVvtgi     = 11
VVjAHQ  = 12
VVJ3c9  = 13
def FFaG6T(parmNum, grepTxt):
 if   parmNum == VVRq5s  : param = ["update"   , "dpkg update" ]
 elif parmNum == VVmDYa   : param = ["list"   , "apt list" ]
 elif parmNum == VVPeIJ: param = ["list-installed" , "dpkg -l"  ]
 else         : param = []
 if param:
  pkg = FFC2Pr()
  if   pkg in ("ipkg", "opkg"): return "%s %s %s" % (pkg, param[0], grepTxt)
  elif pkg == "dpkg"   : return "%s %s" % (param[1], grepTxt)
 return ""
def FFQ7Q5(parmNum, package):
 if   parmNum == VVCBKn      : param = ["info"      , "apt show"         ]
 elif parmNum == VVpvpX      : param = ["files"      , "dpkg -L"          ]
 elif parmNum == VVgetH     : param = ["download"     , "apt-get download"       ]
 elif parmNum == VV4pye     : param = ["install"     , "apt-get install -y"       ]
 elif parmNum == VVEoQq : param = ["install --force-reinstall" , "apt-get install --reinstall -y"    ]
 elif parmNum == VVKrAC : param = ["install --force-overwrite" , "dpkg -i --force-all"       ]
 elif parmNum == VViRav : param = ["install --force-downgrade" , "apt-get install --allow-downgrades -y"  ]
 elif parmNum == VVDDR8  : param = ["install --force-depends" , "apt-get install --no-install-recommends -y" ]
 elif parmNum == VVvtgi     : param = ["remove"      , "apt-get purge --auto-remove -y"    ]
 elif parmNum == VVjAHQ  : param = ["remove --force-remove"  , "dpkg --purge --force-all"     ]
 elif parmNum == VVJ3c9  : param = ["remove --force-depends"  , "dpkg --remove --force-depends"    ]
 else            : param = []
 if param:
  if package:
   package = "'%s'" % package
  pkg = FFC2Pr()
  if   pkg in ("ipkg", "opkg"): return "%s %s %s" % (pkg, param[0], package)
  elif pkg == "dpkg"   : return "%s %s" % (param[1], package)
 return ""
def FFr1Fs():
 result = FFj4HH("ar -V 2> /dev/null | grep 'GNU ar'")
 if result.startswith("GNU ar"):
  cmd = " allOK='1';"
 else:
  notFoundCmd = " echo -e '\"ar\" command (v3.x) not found!';"
  installCmd = FFQ7Q5(VV4pye , "")
  if installCmd:
   verCmd = "FOUND=$(ar -V 2> /dev/null | grep 'GNU ar');"
   failed1 = "Please update your software or manually install \"ar\" command and try again."
   failed2 = "(\"ar\" is available in the packages : \"opkg-tools\" or \"binutils\")"
   failed3 = "Process Failed."
   cmd  = " allOK='0';"
   cmd += verCmd
   cmd += 'if [[ -z "$FOUND" ]]; then '
   cmd +=   notFoundCmd
   cmd += "  echo -e 'Trying to install \"opkg-Tools\" ...';"
   cmd +=    FFxtg8("%s enigma2-plugin-extensions-opkg-tools" % installCmd) + ";"
   cmd +=   verCmd
   cmd += ' if [[ -z "$FOUND" ]]; then '
   cmd += " echo -e 'Trying to install \"binutils\" ...';"
   cmd +=   FFxtg8("%s binutils" % installCmd) + ";"
   cmd += " fi;"
   cmd +=   verCmd
   cmd += ' if [[ -z "$FOUND" ]]; then '
   cmd += "  echo -e 'Installation failed !';"
   cmd += "  echo -e '%s' %s;"  % (failed1, FF95sl(failed1, VVdWFT))
   cmd += "  echo -e '%s' %s;"  % (failed2, FF95sl(failed2, VVdWFT))
   cmd += "  echo -e '\n%s' %s;" % (failed3, FF95sl(failed3, VVzZva))
   cmd += " else"
   cmd += "  echo -e 'Installed successfully.';"
   cmd += "  allOK='1';"
   cmd += " fi;"
   cmd += "else"
   cmd += "  allOK='1';"
   cmd += "fi;"
  else:
   cmd = " allOK='0';"
   cmd += notFoundCmd
 return cmd
def FFqoRI(commandTool, toolPkgName, displayedName):
 cmd1 = ""
 installCmd = FFQ7Q5(VV4pye , "")
 if installCmd:
  failed1 = "Please update your software and try again."
  failed2 = "Process Failed."
  cmd1 += " echo -e '%s not found.';" % displayedName
  cmd1 += " echo -e 'Trying to install ...';"
  cmd1 +=   FFxtg8("%s %s" % (installCmd, toolPkgName)) + ";"
  cmd1 += " FOUND=$(which  %s);"  % commandTool
  cmd1 += ' if [[ -z "$FOUND" ]]; then '
  cmd1 += "  echo -e 'Installation failed !';"
  cmd1 += "  echo -e '%s\n' %s;" % (failed1, FF95sl(failed1, VVdWFT))
  cmd1 += "  echo -e '%s' %s;" % (failed2, FF95sl(failed2, VVzZva))
  cmd1 += " else"
  cmd1 += "  echo -e 'Installed successfully.';"
  cmd1 += "  allOK='1';"
  cmd1 += " fi;"
 else:
  cmd1 += " echo -e '%s not found.';" % displayedName
 cmd  = " allOK='0';"
 cmd += "FOUND=$(which %s);" % commandTool
 cmd += 'if [[ -z "$FOUND" ]]; then '
 cmd +=   cmd1
 cmd += "else"
 cmd += "  allOK='1';"
 cmd += "fi;"
 return cmd
def FFINsi(ip="1.1.1.1", timeout=1.0):
 from socket import socket, setdefaulttimeout, AF_INET, SOCK_STREAM
 try:
  setdefaulttimeout(timeout)
  socket(AF_INET, SOCK_STREAM).connect((ip, 53))
  return True
 except:
  pass
 if os.system(FFxtg8('ping -W%d -q %s -c 1 | grep " 0%% packet"' % (timeout, ip))) == 0:
  return True
 return os.system(FFxtg8("wget -q -T %d -t 1 --spider %s" % (timeout, ip))) == 0
def FFqD66(path, maxSize=-1, encLst=None):
 if   encLst is None    : encLst = CClXbe.VVk4qf()
 elif isinstance(encLst, str) : encLst = [encLst]
 txt = ""
 for enc in encLst:
  try:
   with ioOpen(path, "r", encoding=enc) as f:
    txt = f.read(maxSize)
    txt = str(txt)
   break
  except:
   pass
 if txt.startswith(chr(239) + chr(187) + chr(191)):
  txt = txt[3:]
 return txt
def FFjdnJ(path, keepends=False, maxSize=-1, encLst=None):
 txt = FFqD66(path, maxSize, encLst=encLst)
 return txt.splitlines(keepends)
def FFsdMh(SELF, path, encLst=None):
 title = os.path.basename(path)
 if fileExists(path):
  maxSize = 60000
  if (FFT03z(path) > maxSize):
   title="File too big (showing first 60kB only)"
  else:
   maxSize = -1
  lines = FFqD66(path, maxSize=maxSize, encLst=encLst)
  if lines: FFNEkd(SELF, lines, title=title, VVKsoz=VV72id)
  else : FFzfYN(SELF, path, title=title)
 else:
  FFAVqd(SELF, path, title)
def FF7SvB(SELF, path, title):
 if fileExists(path):
  txt = FFqD66(path)
  txt = txt.replace("#W#", VVZgqQ)
  txt = txt.replace("#Y#", VVoTT6)
  txt = txt.replace("#G#", VVkXS4)
  txt = txt.replace("#C#", VVpHwQ)
  txt = txt.replace("#P#", VVU8eD)
  FFNEkd(SELF, txt, title=title)
 else:
  FFAVqd(SELF, path, title)
def FFzDB4(path):
 if pathExists(path):
  tList = os.listdir(path)
  if tList:
   dirs = []
   for item in tList:
    if os.path.isdir(path + item):
     dirs.append(item)
   if dirs:
    dirs.sort()
    return dirs
 return []
def FFMjyS(path, addTrailingSlash):
 parent = os.path.abspath(os.path.join(path, os.pardir))
 if addTrailingSlash : return FF0WrY(parent)
 else    : return FFkEOw(parent)
def FFqDmh(path):
 return os.path.basename(os.path.normpath(path))
def FFT03z(path):
 try:
  return os.path.getsize(path)
 except:
  return -1
def FFX92w(path):
 try:
  os.remove(path)
 except:
  pass
def FF0WrY(path):
 if not path.endswith("/"):
  path += "/"
 return path
def FFkEOw(path):
 if not path == "/":
  path = path.rstrip("/")
 return path
def FFDOPZ():
 sigFile = "ajpanel_res_marker"
 try:
  p = os.path.abspath(os.path.dirname(__file__))
  if p:
   mainP = os.path.join(p, "")
   resP = os.path.join(p, "res", "")
   if fileExists(os.path.join(resP, sigFile)):
    return mainP, resP
 except:
  pass
 paths = []
 paths.append(VV9VaA)
 paths.append(VV9VaA.replace("lib", "lib64"))
 ba = "/media/ba/ba/"
 list = FFzDB4(ba)
 for p in list:
  p = ba + p + VV9VaA
  paths.append(p)
 for p in paths:
  p = os.path.join(p, VV0A4Z, "")
  if fileExists(os.path.join(p, "res", sigFile)):
   mainP = os.path.join(p, "")
   resP = os.path.join(mainP, "res", "")
   return mainP, resP
 mainP = os.path.join(VV9VaA, VV0A4Z , "")
 resP = os.path.join(mainP, "res", "")
 return mainP, resP
VVrE9D, VVASCC = FFDOPZ()
def FFWcGD():
 def VVtdG1(item, defPath):
  path = item.getValue()
  if not pathExists(path):
   item.setValue(defPath)
   item.save()
   return path
  return ""
 t = "/tmp/"
 oldMovieDownloadPath = ""
 if not pathExists(CFG.MovieDownloadPath.getValue()):
  for p in ("/media/hdd/movie/", "/media/usb/movie/", t, "/"):
   if pathExists(p):
    CFG.MovieDownloadPath.setValue(p)
    CFG.MovieDownloadPath.save()
    oldMovieDownloadPath = p
    break
 VVBjP8   = VVtdG1(CFG.backupPath, CCfRRs.VVKPvT())
 VVq3Od   = VVtdG1(CFG.downloadedPackagesPath, t)
 VVA0Yv  = VVtdG1(CFG.exportedTablesPath, t)
 VVHYTk  = VVtdG1(CFG.exportedPIconsPath, t)
 VVWMzg   = VVtdG1(CFG.packageOutputPath, t)
 global VVCnD5
 VVCnD5 = FF0WrY(CFG.backupPath.getValue())
 if VVBjP8 or VVWMzg or VVq3Od or VVA0Yv or VVHYTk or oldMovieDownloadPath:
  configfile.save()
 return VVBjP8, VVWMzg, VVq3Od, VVA0Yv, VVHYTk, oldMovieDownloadPath
def FFeNiq(path):
 path = FFkEOw(path)
 target = ""
 try:
  if os.path.exists(path) and os.path.islink(path):
   target = os.readlink(path)
 except:
  pass
 return target
def FFsR4g(SELF, pathList, tarFileName, addTimeStamp=True):
 VVvytR = []
 t = ""
 for path in pathList:
  if os.path.isfile(path):
   if fileExists(path):
    VVvytR.append(path)
  elif os.path.isdir(path):
   if os.listdir(path):
    VVvytR.append(path)
  else:
   dirName  = os.path.dirname(path)
   fileName = os.path.basename(path)
   fileName = fileName.replace("*", ".*")
   if crawlDirectory(dirName, fileName):
    VVvytR.append(path)
 if not VVvytR:
  FFkYsE(SELF, "Files not found!")
 elif not pathExists(VVCnD5):
  FFkYsE(SELF, "Path not found!\n\n%s" % VVCnD5)
 else:
  VVHZbd = FF0WrY(VVCnD5)
  tarFileName = "%s%s" % (VVHZbd, tarFileName)
  if addTimeStamp:
   tarFileName = "%s_%s" % (tarFileName, FFGuM2())
  tarFileName += ".tar.gz"
  filesLine = ""
  for f in VVvytR:
   filesLine +=  "%s " % f
  sep  = "echo -e '%s';" % VVZ1aI
  failed = "Process failed !"
  cmd  =  sep
  cmd += "echo -e 'Collecting files ...\n';"
  cmd += "tar -czvf '%s' %s 2> /dev/null;" % (tarFileName, filesLine)
  cmd += "if [ -f '%s' ]; then "    % tarFileName
  cmd += " chmod 644 '%s';"     % tarFileName
  cmd += " echo -e '\nDONE\n';"
  cmd += " echo -e 'Result File:\n%s\n' %s;" % (tarFileName, FF95sl(tarFileName, VV9cEK))
  cmd += "else"
  cmd += " echo -e '\n%s\n' %s;"    % (failed, FF95sl(failed, VV9cEK))
  cmd += "fi;"
  cmd +=  sep
  FFusMt(SELF, cmd)
def FF4Pls(SELF):
 btnMode = SELF.skinParam["topRightBtns"]
 if btnMode in (1, 2): FF4ISS(SELF["keyMenu"], "menu")
 if btnMode in (2, 3): FF4ISS(SELF["keyInfo"], "info")
def FF4ISS(barObj, fName):
 path = "%s%s%s" % (VVASCC, fName, ".png")
 if fileExists(path):
  try:
   barObj.instance.setScale(1)
   barObj.instance.setPixmapFromFile(path)
   return True
  except:
   pass
 return False
def FFkxbC(satNum):
 satNum  = int(satNum)
 if   satNum == 0xeeee: return "DVB-T"
 elif satNum == 0xffff: return "DVB-C"
 else:
  satName = ""
  try:
   satName = nimmanager.getSatName(satNum)
  except:
   pass
  if not satName or "N/A" in satName:
   satName = FFUBZ6(satNum)
  return satName
def FFUBZ6(satNum):
 satNum  = int(satNum)
 if   satNum == 0xeeee: return "DVB-T"
 elif satNum == 0xffff: return "DVB-C"
 else:
  satDir = "E"
  if satNum > 1800:
   satDir = "W"
   satNum = 3600 - satNum
  satNum /= 10.0
  return "%s%s" % (str(satNum), satDir)
def FF24qC(refCode, isLong):
 sat = ""
 if refCode.count(":") > 8:
  nameSpace = refCode.split(":")[6]
  s   = nameSpace.zfill(8)[:4]
  val   = int(s, 16)
  if isLong : sat = FFkxbC(val)
  else  : sat = FFUBZ6(val)
 return sat
def FFsAXk(sat):
 try:
  s = sat.upper()
  if s.endswith("E") or s.endswith("W"):
   num = float(sat[:-1]) * 10
   if s.endswith("W"):
    num = 3600 - num
   return FFkxbC(num)
 except:
  pass
 return sat
def FFbIqi(satNumStr):
 satDir = "E"
 satNum = int(satNumStr)
 if satNum < 0:
  satDir = "W"
 satNum /= 10.0
 return "%s%s" % (str(abs(satNum)), satDir)
def FFnQlZ(SELF, isFromSession=False, addInfoObj=False):
 info = refCode = decodedUrl = origUrl = iptvRef = chName = prov = state = ""
 if not isFromSession: SELF = SELF.session
 service = SELF.nav.getCurrentService()
 if service:
  info = service.info()
  if info:
   chName = info.getName()
   refCode = FFAkN7(info, iServiceInformation.sServiceref)
   prov = FFAkN7(info, iServiceInformation.sProvider)
   state = str(FFAkN7(info, iServiceInformation.sDVBState))
   if not state  : state = ""
   elif  state == "0" : state = "No free tuner"
   elif  state == "1" : state = "Tune Failed"
   elif  state == "2" : state = "Timeout reading PAT"
   elif  state == "3" : state = "SID not found in PAT"
   elif  state == "4" : state = "Timeout reading PMT"
   elif  state == "10" : state = "Check tuner configuration"
   else    : state = "Tuned"
   if refCode.count(":") > 8:
    refCode = refCode.rstrip(":")
    if FFuZb6(refCode):
     chName = chName.rstrip(":")
     if refCode.endswith(("%3a", "%3A")): refCode = refCode[:-3]
     refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(refCode)
 if addInfoObj: return refCode, decodedUrl, origUrl, iptvRef, chName, prov, state, info
 else   : return refCode, decodedUrl, origUrl, iptvRef, chName, prov, state
def FFAkN7(info, param):
 if info:
  v = info.getInfo(param)
  if v == -1: return ""
  if v == -2: return info.getInfoString(param)
  if v ==  1: return info.getInfoString(param)
  return str(v)
 else:
  return ""
def FFcJ7o(refCode, iptvRef, chName):
 if iptvRef : return iptvRef.replace(":" + chName, "")
 else  : return refCode
def FFy0JC(refCode):
 info = FFosPW(refCode)
 return info and info.getName(eServiceReference(refCode)) or ""
def FFwYmz(refCode):
 try:
  ns = refCode.split(":")[6]
  ns = ns.zfill(8)[:4]
 except:
  ns = ""
 return ns.upper()
def FFKhVc(path, fName):
 if os.path.isfile(path + fName):
  return fName
 else:
  if fName.count("_") > 8:
   parts = fName.split("_")
   parts[2] = "1"
   fName = "_".join(parts)
   if os.path.isfile(path + fName):
    return fName
 return ""
def FFosPW(refCode):
 service = eServiceReference(refCode)
 info = None
 if service:
  VVYHZX = eServiceCenter.getInstance()
  if VVYHZX:
   info = VVYHZX.info(service)
 return info
def FFJZ42(SELF, refCode, VVpyjK=True, checkParentalControl=False, isFromSession=False, fromPrtalReplay=False):
 if refCode.count(":") > 8:
  serviceRef = eServiceReference(str(refCode))
  FFSRyd(SELF, serviceRef, checkParentalControl, isFromSession, fromPrtalReplay)
  if VVpyjK:
   FF3bCE(SELF, isFromSession)
 try:
  VVurhM = InfoBar.instance
  if VVurhM:
   VVoSQy = VVurhM.servicelist
   if VVoSQy:
    servRef = eServiceReference(refCode)
    VVoSQy.saveChannel(servRef)
 except:
  pass
def FFSRyd(SELF, serviceRef, checkParentalControl=False, isFromSession=False, fromPrtalReplay=False):
 if isFromSession: session = SELF
 else   : session = SELF.session
 session.nav.playService(serviceRef, checkParentalControl=checkParentalControl)
 if not fromPrtalReplay:
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF, isFromSession=isFromSession)
  if decodedUrl:
   if "chCode=" in decodedUrl:
    pr = CCsnEk()
    if pr.VVdEw9(refCode, chName, decodedUrl, iptvRef):
     pr.VVQp2W(SELF, isFromSession)
def FFuZb6(refCode):
 if refCode:
  span = iSearch(r"([A-Fa-f0-9]+[:]){10}.+\/\/.+", refCode, IGNORECASE)
  if span : return True
  else : return False
def FFeC5o(url): return FFVq1j(url) or FFo6Ta(url)
def FFVq1j(url)  : return any(x in url for x in ("/movie/", "/vod/", "/video/", ".m3u8", "mode=vod"))
def FFo6Ta(url)  : return any(x in url for x in ("/series/", "mode=series"))
def FFMoxZ(refCode):
 span = iSearch(r"((?:[A-Fa-f0-9]+[:]){10})(.+\/\/.+)", refCode, IGNORECASE)
 if span:
  refCode = span.group(1).upper()
  origUrl = span.group(2)
  if refCode.endswith(("%3a", "%3A")):
   refCode = refCode[:-3]
  refCode = refCode.rstrip(":")
  decodedUrl = FF9CmS(origUrl)
  return refCode, decodedUrl, origUrl, refCode + ":" + origUrl
 else:
  return refCode, "", "", ""
def FF9CmS(url):
 if url and iUnquote : return iUnquote(url)
 else    : return url
def FF2NHB(url):
 if url and iQuote : return iQuote(url)
 else    : return url
def FF5o9B(txt):
 try:
  return str(b64encode(txt.encode("utf-8")).decode("utf-8"))
 except:
  return txt
def FFWbB4(txt):
 try:
  return str(b64decode(txt).decode("utf-8"))
 except:
  return txt
def FFyOvd(txt):
 try:
  return FF5o9B(FFWbB4(txt)) == txt
 except:
  return False
def FF3bCE(SELF, isFromSession=False):
 if isFromSession: session = SELF
 else   : session = SELF.session
 refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF, isFromSession=isFromSession)
 isForPlayer = False
 serv = session.nav.getCurrentlyPlayingServiceReference()
 if serv:
  servPath = serv.getPath()
  if servPath and not "FROM BOUQUET " in servPath.upper():
   isForPlayer = True
 if iptvRef or isForPlayer: CCppdx.VVgElN(session, isFromExternal=isFromSession)
 else      : FF5FGP(session, reopen=True)
def FF5FGP(session, reopen=False):
 if reopen:
  try:
   session.openWithCallback(BF(FF5FGP, session), CCWsdR)
  except:
   try:
    FFkV5Q(session, "Cannot launch Signal Monitor !", title="Signal Monitor")
   except:
    pass
def FFqcpq(refCode):
 tp = CCX8JT()
 if tp.VVrs7D(refCode) : return True
 else        : return False
def FFexa9(refCode, isHide, skipReload=False):
 if refCode.count(":") > 8:
  sRef = eServiceReference(refCode)
  if sRef:
   db = eDVBDB.getInstance()
   if db:
    if isHide : ret = db.addFlag(sRef , 0x2)
    else  : ret = db.removeFlag(sRef, 0x2)
    if skipReload:
     return True if ret == 0 else False
    elif ret == 0:
     FFlB9k(True)
     return True
 return False
def FFlB9k(save=False):
 db = eDVBDB.getInstance()
 if db:
  if save:
   db.saveServicelist()
  db.reloadServicelist()
  db.reloadBouquets()
 FFHXAS()
def FFHXAS():
 VVurhM = InfoBar.instance
 if VVurhM:
  VVoSQy = VVurhM.servicelist
  if VVoSQy:
   VVoSQy.setMode()
def FFocgD(root):
 lst = []
 try:
  servicelist  = root and eServiceCenter.getInstance().list(root)
  VVYHZX = eServiceCenter.getInstance()
  if servicelist:
   while True:
    service = servicelist.getNext()
    if not service.valid():
     break
    if service.flags & (eServiceReference.isDirectory | eServiceReference.isMarker):
     continue
    info = VVYHZX.info(service)
    lst.append((service.toString(), info.getName(service)))
 except:
  pass
 return lst
def FF92xJ():
 VV1Lo5 = {0x01:"TV MPEG-2 SD",0x02:"Radio MPEG-1",0x03:"Teletext",0x04:"NVOD SD",0x05:"NVOD SD T.Shift",0x06:"Mosaic",0x07:"FM Radio",0x08:"DVB SRM",0x09:"Res. 9",0x0A:"Radio Adv. Codec",0x0B:"AVC Mosaic",0x0C:"Data",0x0D:"CI",0x0E:"RCS Map",0x0F:"RCS FLS",0x10:"DVB MHP",0x11:"TV HD MPEG-2",0x16:"TV SD H.264",0x17:"NVOD SD T.Sh.",0x18:"NVOD SD Ref.",0x19:"TV HD H.264",0x1A:"NVOD HD T.Sh.",0x1B:"NVOD HD Ref.",0x1C:"TV HD H.264",0x1D:"NVOD HD T.Sh.",0x1E:"NVOD HD Ref.",0x1F:"TV HEVC",0x20:"TV HEVC (HDR)",0x80:"User Def.",0x64:"Custom",0x81:"Custom",0x82:"Custom",0x84:"Custom",0x95:"Custom",0x98:"Custom",0x9B:"Custom",0xAB:"Custom",0xB4:"Custom",0xB5:"Custom",0xC6:"Custom",0xFA:"Custom",0xFB:"Custom",0xFC:"Custom"}
 VVUDHC = list(VV1Lo5)
 return VVUDHC, VV1Lo5
def FFkmMQ():
 try:
  from Tools.Directories import resolveFilename, SCOPE_PLUGINS
  iPlugins.clearPluginList()
  iPlugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
 except:
  pass
def FF8dax(session, VV0qsI):
 VVfyF5, VVxCEe, VVlwNO, camCommand = FFsttR()
 if VVxCEe:
  runLog = False
  if   VV0qsI == CC97UC.VVU0pj : runLog = True
  elif VV0qsI == CC97UC.VVJP20 : runLog = True
  elif not VVlwNO          : FFkV5Q(session, message="SoftCam not started yet!")
  elif fileExists(VVlwNO)        : runLog = True
  else             : FFkV5Q(session, message="File not found !\n\n%s" % VVlwNO)
  if runLog:
   session.open(BF(CC97UC, VVfyF5=VVfyF5, VVxCEe=VVxCEe, VVlwNO=VVlwNO, VV0qsI=VV0qsI))
 else:
  FFkV5Q(session, message="No active OSCam/NCam found !", title="Live Log")
def FFsttR():
 VVfyF5 = "/etc/tuxbox/config/"
 VVxCEe = None
 VVlwNO  = None
 camCommand = FFj4HH("lsof | grep 'oscam\|ncam' | tail -1 | awk '{print($2)}'")
 if camCommand:
  camCmd = os.path.basename(camCommand).lower()
  if   camCmd.startswith("oscam") : VVxCEe = "oscam"
  elif camCmd.startswith("ncam") : VVxCEe = "ncam"
 if VVxCEe:
  path = FFj4HH(camCommand + " -V 2> /dev/null | grep -i configdir | awk '{print($2)}'")
  path = FF0WrY(path)
  if pathExists(path):
   VVfyF5 = path
  tFile = VVfyF5 + VVxCEe + ".conf"
  tFile = FFj4HH("FILE='%s'; [ -f $FILE ] && cat $FILE | grep -i LOGFILE | awk '{print($3)}'" % tFile)
  if fileExists(tFile):
   VVlwNO = tFile
 return VVfyF5, VVxCEe, VVlwNO, camCommand
def FFPPfi(delta=0):
 Time = datetime.now() + timedelta(delta)
 midnight = Time.replace(hour=0, minute=0, second=0, microsecond=0)
 return mktime(midnight.timetuple())
def FFcgMH(unixTime):
 return datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')
def FFDl5h():
 year, month, day, hour, minute, second, weekDay, yearDay, dayLight = localtime()
 return "%04d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hour, minute, second)
def FFGuM2():
 return FFDl5h().replace(" ", "_").replace("-", "").replace(":", "")
def FF3UDS(secs):
 m, s = divmod(secs, 60)
 h, m = divmod(m   , 60)
 return "%02d:%02d:%02d" % (h, m, s)
def FFdyoU():
 return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
def FF913T(url, outFile, timeout=3, mustBeImage=False):
 tmpDir  = "/tmp/"
 outFile  = tmpDir + outFile
 span = iSearch(r".*data.+base64,(.+)", url, IGNORECASE)
 if span:
  b64 = span.group(1)
  with open(outFile, "wb") as f:
   f.write(b64decode(b64))
  return outFile, ""
 if not CCqQHV.VVPus3(url, justValidate=True):
  return "", "Invalid URL"
 if not iRequest:
  return "" , "Cannot import URLLIB/URLLIB2 !"
 try:
  req = iRequest(url.strip())
  req.add_header('User-Agent', 'Enigma2-Plugin')
  res = iUrlopen(req, timeout=timeout)
  resCode = res.code
  if resCode == 200 :
   if mustBeImage and "text/html" in res.headers.get("Content-Type"):
    return "", "Received TEXT/HTML (instead of image)"
   with open(outFile, "wb") as f:
    f.write(res.read())
   cont = res.headers.get("content-disposition")
   if cont:
    phpFile = ""
    span = iSearch(r'filename=["*](.+)["*]', str(cont), IGNORECASE)
    if span:
     phpFile = span.group(1)
     phpFiLe = phpFile.replace(".", "")
     fName, ext = os.path.splitext(phpFile)
     fName = CCqQHV.VVwvI5(fName)
     phpFile = tmpDir + fName + ext
     os.system(FFxtg8("mv -f '%s' '%s'" % (outFile, phpFile)))
     outFile = phpFile
   if fileExists(outFile) : return outFile, ""
   else     : return "", "Cannot create file."
  else:
   if   resCode == 401 : err = "Unauthorized"
   elif resCode == 402 : err = "Payment Required"
   elif resCode == 408 : err = "Request Timeout"
   else    : err = "err=%d" % resCode
   return "", "Download Failed (%s)" % err
 except Exception as e:
  return "", str(e)
def FFlKzi(numStr):
 return iMatch(r"^([-+]?\d+(\.\d*)?$)", numStr) is not None
def FFICXm(num):
 return "s" if num > 1 else ""
def FF2DVg(num, minNum, maxNum):
 return max(min(maxNum, num), minNum)
def FFZMXB(OldValue, OldMin, OldMax, NewMin, NewMax):
 return (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
def FFo5A5(a, b):
 return (a > b) - (a < b)
def FFUcDJ(a, b):
 def VV21vo(var):
  return [ (int(c) if c.isdigit() else c) for c in iSplit(r'(\d+)', var) ]
 a = VV21vo(a)
 b = VV21vo(b)
 return (a > b) - (a < b)
def FFGDcX(mycmp):
 class CC3H4x(object):
  def __init__(self, obj, *args) : self.obj = obj
  def __lt__(self, other): return mycmp(self.obj, other.obj) < 0
  def __gt__(self, other): return mycmp(self.obj, other.obj) > 0
  def __eq__(self, other): return mycmp(self.obj, other.obj) == 0
  def __le__(self, other): return mycmp(self.obj, other.obj) <= 0
  def __ge__(self, other): return mycmp(self.obj, other.obj) >= 0
  def __ne__(self, other): return mycmp(self.obj, other.obj) != 0
 return CC3H4x
def FFewCE(SELF, message, title=""):
 SELF.session.open(BF(CCpYuO, title=title, message=message, VVXeWx=True))
def FFNEkd(SELF, message, title="", VVKsoz=VV72id, **kwargs):
 SELF.session.open(BF(CCpYuO, title=title, message=message, VVKsoz=VVKsoz, **kwargs))
def FFkYsE(SELF, message, title="")  : FFkV5Q(SELF.session, message, title)
def FFAVqd(SELF, path, title="") : FFkV5Q(SELF.session, "File not found !\n\n%s" % path, title)
def FFzfYN(SELF, path, title="") : FFkV5Q(SELF.session, "File is empty !\n\n%s"  % path, title)
def FFHRK6(SELF, title="")  : FFkV5Q(SELF.session, "OPKG/IPKG/DPKG Tools not found", title)
def FFkV5Q(session, message, title="") : session.open(BF(CC0jVk, title=title, message=message))
def FFbRXK(SELF, VVnFNJ, title="", defaultText="", message=""):
 mode = CFG.keyboard.getValue()
 allOK = False
 if mode == "v":
  try:
   from Screens.VirtualKeyBoard import VirtualKeyBoard
   obj = SELF.session.openWithCallback(VVnFNJ, VirtualKeyBoard, title=message, text=defaultText)
   allOK = True
   obj.setTitle(title)
  except:
   pass
 elif mode == "s":
  try:
   from Screens.InputBox import InputBox
   SELF.session.openWithCallback(VVnFNJ, InputBox, windowTitle=title, title=message.replace("\n", " "), text=defaultText)
   allOK = True
  except:
   pass
 if not allOK:
  try:
   FFkYsE(SELF, "Cannot run the Input Dialog (keyboard) !", title="Keyboard Error")
  except:
   pass
def FFMIbO(SELF, callBack_Yes, VVSidL, callBack_No=None, title="", VVUEfx=False, VVr8hX=True):
 return SELF.session.openWithCallback(BF(FFZR5S, callBack_Yes, callBack_No)
          , BF(CCQcnd, title=title, VVSidL=VVSidL, VVr8hX=VVr8hX, VVUEfx=VVUEfx))
def FFZR5S(callBack_Yes, callBack_No, FFMIbOed):
 if FFMIbOed : callBack_Yes()
 elif callBack_No: callBack_No()
def FFD1yO(SELF, message="", milliSeconds=0, isGrn=False):
 try:
  SELF["myInfoBody"].setText(str(message))
  if isGrn: color = "#00004040"
  else : color = "#00550000"
  FFobAA(SELF["myInfoBody"], color)
  if milliSeconds > 0:
   SELF["myInfoFrame"].show()
   SELF["myInfoBody"].show()
   FF5aoS(SELF, milliSeconds)
  else:
   if len(message) > 0:
    SELF["myInfoFrame"].show()
    SELF["myInfoBody"].show()
   else:
    SELF["myInfoFrame"].hide()
    SELF["myInfoBody"].hide()
 except:
  pass
def FF9RVa(SELF):
 try:
  if SELF["myInfoBody"] and SELF["myInfoBody"].visible:
   return True
 except:
  pass
 return False
VVTTdu = eTimer()
def FF5aoS(SELF, milliSeconds=1000):
 SELF.onClose.append(BF(FFDMlo, SELF))
 fnc = BF(FFDMlo, SELF)
 try:
  t = VVTTdu.timeout.connect(fnc)
 except:
  VVTTdu.callback.append(fnc)
 VVTTdu.start(milliSeconds, 1)
def FFDMlo(SELF):
 VVTTdu.stop()
 try:
  if SELF["myInfoFrame"] : SELF["myInfoFrame"].hide()
  if SELF["myInfoBody"] : SELF["myInfoBody"].hide()
 except:
  pass
def FF1dQ4(SELF, callBackFunc, **kwargs):
 try:
  if callBackFunc : win = SELF.session.openWithCallback(callBackFunc, BF(CCgB5a, **kwargs))
  else   : win = SELF.session.open(BF(CCgB5a, **kwargs))
  FFqx5h(win)
  return win
 except:
  return None
def FFuRfS(SELF, callBackFunc, **kwargs):
 win = SELF.session.openWithCallback(callBackFunc, BF(CC7aOd, **kwargs))
 FFqx5h(win)
 return win
def FFi9aC(txt):
 return ("--[ %s ]%s" % (txt,  "-" * 100), )
def FFBatl(SELF, **kwargs):
 SELF.session.open(CCARMv, **kwargs)
def FFtIlI(SELF, isTopBar=False):
 if isTopBar : names = [ "keyRedTop" , "keyGreenTop" , "keyYellowTop", "keyBlueTop"  ]
 else  : names = [ "keyRed" , "keyGreen" , "keyYellow" , "keyBlue"  ]
 for name in names:
  try:
   inst = SELF[name].instance
   inst.setBorderColor(parseColor("#000000"))
   inst.setBorderWidth(3)
   inst.setNoWrap(True)
  except:
   pass
def FFiE61(label, color, w):
 try:
  inst = label.instance
  inst.setBorderColor(parseColor(color))
  inst.setBorderWidth(w)
 except:
  pass
def FFjs4z(SELF, menuObj):
 try:
  menuObj.instance.setFont(gFont(VVFwML, SELF.skinParam["bodyFontSize"]))
 except:
  pass
def FF4FP6(SELF, menuObj=None, minRows=0):
 if not menuObj:
  menuObj = SELF["myMenu"]
 FFjs4z(SELF, menuObj)
 winW   = SELF.instance.size().width()
 winH   = SELF.instance.size().height()
 lineH   = menuObj.l.getItemSize().height()
 menuCurrentW = menuObj.instance.size().width()
 menuCurrentH = menuObj.instance.size().height()
 menuCorrectH = (max(minRows, len(menuObj.list))) * lineH
 diff   = menuCorrectH - menuCurrentH
 winNewH   = winH + diff
 if winNewH > winH:
  pos  = menuObj.getPosition()
  part = menuObj.instance.size().height() % lineH
  half = int(part / 2)
  menuObj.instance.resize(eSize(*(menuCurrentW, menuCurrentH - part)))
  menuObj.instance.move(ePoint(pos[0], pos[1] + half))
 else:
  screenSize = getDesktop(0).size()
  menuObj.instance.resize(eSize(*(menuCurrentW, menuCurrentH + diff)))
  SELF.instance.resize(eSize(*(winW, winNewH)))
  SELF.instance.move(ePoint((screenSize.width() - winW) // 2, (screenSize.height() - winNewH) // 2))
  names = [ "keyRed", "keyGreen", "keyYellow", "keyBlue", "myBar", "myLine" ]
  for name in names:
   try:
    obj = SELF[name]
    pos = obj.getPosition()
    obj.instance.move(ePoint(pos[0], pos[1] + diff))
   except:
    pass
 winSize  = SELF.instance.size()
 boxFSize = SELF["myInfoFrame"].instance.size()
 boxSize  = SELF["myInfoBody"].instance.size()
 SELF["myInfoFrame"].instance.move(ePoint((winSize.width() - boxFSize.width()) // 2, (winSize.height() - boxFSize.height()) // 2))
 SELF["myInfoBody"].instance.move(ePoint((winSize.width() - boxSize.width()) // 2, (winSize.height() - boxSize.height()) // 2))
def FFjf8O():
 s = getDesktop(0).size()
 return (s.width(), s.height())
def FFWyds(VVmp7B):
 screenSize  = FFjf8O()
 screenH   = screenSize[1]
 ratioH   = screenH / 1080.0
 bodyFontSize = int(ratioH  * VVmp7B)
 return bodyFontSize
def FFiz2E(VVmp7B, extraSpace):
 font = gFont(VVFwML, VVmp7B)
 VVyhPB = fontRenderClass.getInstance().getLineHeight(font) or (VVmp7B * 1.25)
 return int(VVyhPB + VVyhPB * extraSpace)
def FF896P(winType, width, height, titleFontSize, marginLeft, marginTop, titleColor, bodyColor, bodyFontSize, barHeight=0, topRightBtns=0, lineGap=0.15, addFramedPic=False, usefixedFont=False, winRatio=1, titleSep=True):
 screenSize = FFjf8O()
 screenW = int(screenSize[0] * winRatio)
 screenH = int(screenSize[1] * winRatio)
 if width == 0 : width  = screenW
 if height == 0: height = screenH
 ratioW   = screenW / 1920.0
 ratioH   = screenH / 1080.0
 width   = int(ratioW  * width)
 height   = int(ratioH  * height)
 titleH   = int(ratioH  * 50)
 marginLeft  = int(ratioW  * marginLeft)
 marginTop  = int(ratioH  * marginTop)
 bodyFontSize = int(ratioH  * bodyFontSize)
 barHeight  = int(ratioH  * barHeight)
 marginTop  = max(1, marginTop)
 scrollBarW  = int(ratioW * 15)
 bodyFontStr  = 'font="%s;%d"' % (VVFwML, bodyFontSize)
 alignCenter  = 'halign="center" valign="center"'
 alignLeftTop = 'halign="left" valign="top"'
 alignLeftCenter = 'halign="left" valign="center"'
 alignRightCenter= 'halign="right" valign="center"'
 titleFontSize = min(int(ratioH  * titleFontSize), int(0.7  * titleH))
 bodyLineH  = FFiz2E(bodyFontSize, lineGap)
 bodyW   = width - marginLeft * 2
 bodyTop   = titleH + 1 + marginTop
 bodyH   = height - bodyTop - marginTop
 if barHeight > 0: bodyH -= barHeight
 tmp  =  '<screen position="center,center" size="%d,%d" backgroundColor="%s" title="%s" flags="wfNoBorder" >' % (width, height, bodyColor, PLUGIN_NAME)
 tmp += '<widget  name="myBody" position="0,0" size="%d,%d" zPosition="-1" backgroundColor="%s" />' % (width, height, bodyColor)
 if titleSep:
  tmp += '<eLabel position="0,%d"  size="%d,1"  zPosition="1" backgroundColor="#22aaaaaa" />' % (titleH + 1, width)
 tmp += '<widget name="myTitle" position="0,0"   size="%d,%d" zPosition="2" noWrap="1" backgroundColor="%s" font="%s;%d" foregroundColor="#ffffbb" shadowColor="#000000" shadowOffset="-1,-1" %s />' % (width, titleH, titleColor, VVFwML, titleFontSize, alignLeftCenter)
 if winType == VVoxS0 or winType == VVJ7n1:
  if winType == VVJ7n1 : menuName = "config"
  else      : menuName = "myMenu"
  tmp += '<widget name="%s"  position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" itemHeight="%d" scrollbarMode="showOnDemand" />' % (menuName, marginLeft, bodyTop, bodyW, bodyH, bodyColor, bodyLineH)
 elif winType == VVnacN:
  tmp += '<widget name="myWinTitle" position="0,0" size="%d,%d" zPosition="3" noWrap="1" transparent="1" foregroundColor="#ffffff" shadowColor="#440000" shadowOffset="-2,-2" %s %s />' % (width, titleH, bodyFontStr, alignLeftCenter)
 elif winType == VVmOpB:
  names = ("Red", "Green", "Yellow", "Blue")
  colors = [ "#229f1313", "#22005500", "#22a08000", "#2218188b"]
  totBtns = len(names)
  gap  = 5
  btnW = int(width * 0.09)
  btnH = int(titleH * 0.7)
  left = width - btnW - titleH * 2
  top  = int((titleH - btnH) / 2.0)
  fSize = int(0.45  * titleH)
  for i in range(totBtns-1, -1, -1):
   tmp += '<widget name="key%s" position="%d,%d" size="%d,%d" zPosition="3" font="%s;%d" backgroundColor="%s" %s />' % (names[i], left, top, btnW, btnH, VVFwML, fSize, colors[i], alignCenter)
   left -= (btnW + gap)
  names = ("Del", "BGTr", "TxtFg", "TxtFnt", "TxtSiz", "Align", "ShadFg", "ShadSiz", "Pos")
  totBtns = len(names)
  btnW = int((width - gap * (totBtns + 1)) / totBtns)
  btnH = titleH
  left = gap
  param = 'size="%d,%d" zPosition="3" backgroundColor="#33222222" %s %s ' % (btnW, btnH, bodyFontStr, alignCenter)
  for i in range(totBtns):
   tmp += '<widget name="mySubt%s"  position="%d,%d" foregroundColor="#00cccccc" %s />' % (names[i], left, titleH + gap  , param)
   tmp += '<widget name="mySubt%s1" position="%d,%d" foregroundColor="#00ffff88" %s />' % (names[i], left, titleH + btnH + 1, param)
   left += btnW + gap
  tmp += '<widget name="mySubtCursor" position="0,%d" size="%d,%d" zPosition="2" backgroundColor="#00ffff00" />' % (titleH + 1, btnW + gap * 2, btnH * 2 + gap - 1)
  top = titleH + 1 + btnH * 2 + gap
  tmp += '<widget name="mySubtCover" position="0,0" size="%d,%d" zPosition="5" backgroundColor="#ff000000" />' % (width, top - 1)
  tmp += '<widget name="mySubtFr" position="0,%d" size="%d,%d" zPosition="3" backgroundColor="#ff002233" />' % (top, width, height - top)
  for i in range(4):
   tmp += '<widget name="mySubtSep%d" position="1,%d" size="%d,1" zPosition="7" backgroundColor="#00555555" %s %s />' % (i, top + 1, width - 2, bodyFontStr, alignCenter)
   if i < 3:
    tmp += '<widget name="mySubt%d"    position="1,%d" size="%d,%d" zPosition="6" backgroundColor="#00000000" %s %s />' % (i, top + 1, width - 2, titleH - 2, bodyFontStr, alignCenter)
   top += titleH
 elif winType == VV4ccg:
  barH = int((bodyH + marginTop - marginTop * 3.0) / 3.0)
  picW = int(bodyW * 0.07)
  barW = bodyW - picW - marginLeft
  b1Top = bodyTop
  b2Top = b1Top + barH + marginTop
  b3Top = b2Top + barH + marginTop
  timeW = int(barW * 0.1)
  b2Left1 = marginLeft
  b2Left2 = timeW + marginLeft * 2
  b2Left4 = barW - timeW + marginLeft
  b2Left3 = b2Left4 - marginLeft - timeW
  pLeft = width - picW - marginLeft
  FFewCEL = b2Left2 + timeW + marginLeft
  FFewCEW = b2Left3 - marginLeft - FFewCEL
  name = "myPlay"
  tmp += '<widget name="%sBarF"  position="%d,%d" size="%d,%d" zPosition="1" backgroundColor="#0a444444" />' % (name, marginLeft, b1Top, barW, barH)
  tmp += '<widget name="%sBarBG" position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#11000000" />' % (name, marginLeft + 1, b1Top + 1, barW - 2, barH - 2)
  tmp += '<widget name="%sBar"   position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="#06445566" />' % (name, marginLeft + 1, b1Top + 1, barW - 2, barH - 2)
  tmp += '<widget name="%sMov"   position="%d,%d" size="%d,%d" zPosition="4" backgroundColor="#0aff8000" />' % (name, marginLeft + 1, b1Top - 4, 3, barH + 8)
  tmp += '<widget name="%sVal"   position="%d,%d" size="%d,%d" zPosition="5" backgroundColor="#0a005555" foregroundColor="#ffffff" transparent="1" shadowColor="#00000000" shadowOffset="-1,-1" %s %s />' % (name, marginLeft + 1, b1Top + 1, barW - 2, barH - 2, bodyFontStr, alignCenter)
  param = 'zPosition="1" noWrap="1" backgroundColor="%s" %s' % (bodyColor, bodyFontStr)
  tmp += '<widget name="%sPos"  position="%d,%d" size="%d,%d" %s foregroundColor="#00aacccc" %s />' % (name, b2Left1, b2Top, timeW, barH, param, alignLeftCenter)
  tmp += '<widget name="%sSkp"  position="%d,%d" size="%d,%d" %s foregroundColor="#00ffff00" %s />' % (name, b2Left2, b2Top, timeW, barH, param, alignCenter)
  tmp += '<widget name="%sMsg"  position="%d,%d" size="%d,%d" %s foregroundColor="#00ffffff" %s />' % (name, FFewCEL , b2Top, FFewCEW , barH, param, alignCenter)
  tmp += '<widget name="%sRem"  position="%d,%d" size="%d,%d" %s foregroundColor="#00CDAE77" %s />' % (name, b2Left3, b2Top, timeW, barH, param, alignCenter)
  tmp += '<widget name="%sDur"  position="%d,%d" size="%d,%d" %s foregroundColor="#00B1C177" %s />' % (name, b2Left4, b2Top, timeW, barH, param, alignRightCenter)
  sepTop = int(b3Top - marginTop / 2.0)
  tmp += '<widget name="myPlaySep" position="0,%d" size="%d,1" zPosition="1" backgroundColor="#11444444" />' % (sepTop, pLeft)
  color = ["#0a004400", "#00555555", "#00bbbb55", "#00bbbb55", "#00777777", "#00999999", "#00999999", "#00999999", "#0a18188b"]
  names = ["Grn"  , "Jmp"   , "Dat"   , "Tim"    , "Mrk"  , "Res"   , "Fps"   , "Asp"    , "Blu"  ]
  Len  = len(names)
  b3W  = int((barW - marginLeft * (Len - 1)) / Len)
  left = marginLeft
  for i in range(9):
   if i in (0, Len-1) : bg = 'foregroundColor="#00FFFFFF" backgroundColor="%s"' % color[i]
   else     : bg = 'foregroundColor="%s"'        % color[i]
   tmp += '<widget name="myPlay%s" position="%d,%d" size="%d,%d" zPosition="1" noWrap="1" %s %s %s />' % (names[i], left, b3Top + 1, b3W, barH, bodyFontStr, alignCenter, bg)
   left += b3W + marginLeft
  pTop = titleH + 6
  pW  = width - pLeft - 8
  pH  = height - pTop - 4
  tmp += '<eLabel position="%d,%d"  size="1,%d" zPosition="1" backgroundColor="#00333333" />' % (pLeft, titleH + 2, height - titleH + 1)
  tmp += '<widget name="myPlayPic" position="%d,%d" size="%d,%d" zPosition="1" alphatest="blend" />' % (pLeft + 4, pTop, pW, pH)
  tmp += '<widget name="myPlayTyp" position="%d,%d" size="%d,%d" zPosition="1" backgroundColor="#1100202a" %s %s />' % (pLeft + 4, pTop, pW, pH, alignCenter, bodyFontStr)
  sz = int(titleH * 0.6)
  top = int((titleH - sz) / 2.0)
  tmp += '<widget name="myPlayDnld" position="%d,%d" size="%d,%d" zPosition="100" alphatest="blend" />' % (0, top, sz, sz)
  tmp += '<widget name="myPlayRpt" position="%d,%d" size="%d,%d" zPosition="100" alphatest="blend" />' % (0, top, sz, sz)
  params = 'zPosition="10" backgroundColor="#11444411"'
  tmp += '<eLabel %s position="0,0"  size="%d,1" />' % (params, width)
  tmp += '<eLabel %s position="0,%d" size="%d,1" />' % (params, height - 1, width)
  tmp += '<eLabel %s position="0,0"  size="1,%d" />' % (params, height)
  tmp += '<eLabel %s position="%d,0" size="1,%d" />' % (params, width - 1, height -1)
 elif winType == VVbZAe:
  w  = int((width - 10) / 4.0)
  h  = bodyH - 10
  left = 5
  top  = bodyTop + 5
  tmp += '<widget name="myColorF" position="%d,%d" size="%d,%d" zPosition="1" backgroundColor="#00ffffff" />' % (left, top, w, h)
  for i in range(4):
   tmp += '<widget name="myColor%d" position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="%s" foregroundColor="#ffffff" %s %s />' % (i, left + 4, top + 4, w - 8, h - 8, bodyColor, bodyFontStr, alignLeftCenter)
   left += w
 elif winType == VVEgON:
  itemsH  = bodyLineH * 2.0
  menuH  = int(bodyLineH * 2.5)
  menuW  = int(ratioW  * 200)
  menuLeft = int((width - menuW) / 2.0)
  textH  = bodyH - menuH
  menuTop  = bodyTop + textH
  itemsTop = int(menuTop + marginTop / 2.0 + (menuH - itemsH) / 2.0)
  tmp += '<widget name="myLine"  position="0,%d"  size="%d,1"  zPosition="3" backgroundColor="#11444444" />' % (menuTop, width)
  tmp += '<widget name="myLabel" position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" foregroundColor="#ffffff" %s %s />' % (marginLeft, bodyTop, bodyW, textH, bodyColor, alignCenter, bodyFontStr)
  tmp += '<widget name="myMenu"  position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" foregroundColor="#ffffff" scrollbarMode="showOnDemand" itemHeight="%d" />' % (menuLeft, itemsTop, menuW, itemsH, bodyColor, bodyLineH)
 elif winType == VV7ebZ:
  tmp += '<widget name="myTableH" position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" scrollbarMode="showOnDemand" scrollbarWidth="%d" />' % (marginLeft, bodyTop, bodyW, 0, bodyColor, scrollBarW)
  tmp += '<widget name="myTable"  position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" scrollbarMode="showOnDemand" scrollbarWidth="%d" />' % (marginLeft, bodyTop, bodyW, bodyH, bodyColor, scrollBarW)
 elif winType == VVSzFu:
  titleFont = int(bodyFontSize * 0.6)
  boxFont  = int(bodyFontSize * 1.2)
  boxH  = int(bodyFontSize * 2.0)
  digitW  = int(bodyFontSize * 1.3)
  names  = ["year", "month", "day", "gap", "hour", "min", "sec"]
  boxW  = [  4   ,    2   ,   2  ,   1  ,   2   ,   2  ,   2  ]
  gap   = 4
  boxLeft  = int((width - digitW * 15) / 2.0 - gap)
  btnTitleH = titleFont * 2
  titleTop = int(bodyTop + (height - barHeight - bodyTop - (btnTitleH + boxH + gap)) / 2.0)
  boxTop  = titleTop + btnTitleH + gap
  tmp += '<widget name="curTime" position="0,%d" size="%d,%d" zPosition="2" foregroundColor="white" transparent="1" %s %s />' % (titleH + 1, width, titleTop - titleH - 2, bodyFontStr, alignCenter)
  for i in range(0, 7):
   tmpW = digitW * boxW[i]
   tmp += '<widget name="%s" position="%d,%d" size="%d,%d" zPosition="3" font="%s;%d" foregroundColor="white" backgroundColor="#11404040" %s />' % (names[i]+"Title", boxLeft, titleTop, tmpW - gap, btnTitleH, VVFwML, titleFont, alignCenter)
   tmp += '<widget name="%s" position="%d,%d" size="%d,%d" zPosition="3" font="%s;%d" foregroundColor="white" backgroundColor="#11404040" %s />' % (names[i], boxLeft, boxTop, tmpW - gap, boxH, VVFwML, boxFont, alignCenter)
   boxLeft += tmpW + boxW[i]
 elif winType == VV3nyh:
  barW  = int(ratioW  * 500)
  infH  = int(titleH * 0.8)
  infTop  = height - infH
  infFont  = int(0.5  * infH)
  bAreaH  = int(height - titleH - infH)
  barH  = int((bAreaH - marginTop * 4) / 3)
  barTop  = titleH + marginTop
  barL  = int(width - barW - titleH / 2)
  txtW  = barL - marginLeft - 4
  name  = [ "SNR", "AGC", "BER"]
  tmp += '<widget name="mySNRdB" text="0 dB" position="%d,%d" size="%d,%d" %s %s zPosition="4" transparent="1" foregroundColor="white" />' % (0, 0, width - 20, titleH, bodyFontStr, alignRightCenter)
  for i in range(3):
   tmp += '<eLabel position="%d,%d" size="%d,%d" zPosition="5" text="%s" %s %s backgroundColor="%s" foregroundColor="white" />' % (marginLeft, barTop, txtW, barH, name[i], bodyFontStr, alignLeftCenter, bodyColor)
   tmp += '<eLabel position="%d,%d" size="%d,%d" zPosition="4" backgroundColor="#ffffff" />' % (barL-1, barTop-1, barW+2, barH+2)
   tmp += '<eLabel position="%d,%d" size="%d,%d" zPosition="4" backgroundColor="%s" />' % (barL, barTop, barW, barH, bodyColor)
   tmp += '<widget name="mySlider%s" position="%d,%d" size="%d,%d" zPosition="5" alphatest="blend" />' % (name[i], barL, barTop, barW, barH)
   tmp += '<widget name="mySliderCov%s" position="%d,%d" size="%d,%d" zPosition="6" />' % (name[i], barL, barTop, barW, barH)
   tmp += '<widget name="my%s" position="%d,%d" size="%d,%d" %s %s zPosition="7" text="0 " foregroundColor="#ffffff" transparent="1" shadowColor="#00000000" shadowOffset="-1,-1" />' % (name[i], barL, barTop, barW, barH, bodyFontStr, alignCenter)
   barTop += barH + marginTop
  tmp += '<widget name="myTPInfo" position="0,%d" size="%d,%d" zPosition="8" backgroundColor="%s" font="%s;%d" %s />' % (infTop, width, infH, titleColor, VVFwML, infFont, alignCenter)
  tmp += '<eLabel position="0,%d"  size="%d,1"  zPosition="9" backgroundColor="#22aaaaaa" />' % (infTop -1, width)
 elif winType == VV4yep:
  barW = bodyW
  barH = int(bodyH * 0.7)
  barL = marginLeft
  barT = int(bodyTop + (bodyH - barH) / 2.0)
  fontH = int(0.5  * barH)
  tmp += '<eLabel position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#ffffff" />' % (barL-1, barT-1, barW+2, barH+2)
  tmp += '<eLabel position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="%s" />' % (barL, barT, barW, barH, bodyColor)
  tmp += '<widget name="myProgBar" position="%d,%d" size="%d,%d" zPosition="4" backgroundColor="#004444" foregroundColor="#ffffff" />' % (barL, barT, barW, barH)
  tmp += '<widget name="myProgBarVal" position="%d,%d" size="%d,%d" zPosition="5" foregroundColor="#ffffff" transparent="1" shadowColor="#00000000" shadowOffset="-1,-1" font="%s;%d" %s />' % (barL, barT, barW, barH, VVFwML, fontH, alignCenter)
 elif winType == VVOdhH:
  totRows  = 5
  totCols  = 7
  infT  = titleH + 2
  infH  = int(titleH * 1.8)
  boxT  = infT + infH + 2
  boxW  = int(width  / totCols)
  boxH  = int((height - barHeight - boxT) / totRows)
  picH  = int(boxH * 0.75)
  lblH  = int(boxH * 0.25) - 2
  lblT  = boxT + picH + 2
  lblFont  = int(lblH * 0.65)
  w1, w2 = int(width * 0.45), int(width * 0.55)
  h  = int(infH  * 0.3333)
  fnt  = int(h     * 0.7)
  s  = '<widget name="myPiconInf%d" position="%d,%d" size="%d,%d" zPosition="1" backgroundColor="%s" font="%s;%d" %s />'
  y = infT + 1
  color = ("#00002828", "#00003333", "#00004444", "#00002233", "#00003344", "#00004455")
  for i in range(3):
   tmp += s % (i  , 0   , y, w1, h , color[i]  , VVFwML, fnt, alignLeftCenter)
   tmp += s % (i+3, w1+1, y, w2, h , color[i+3], VVFwML, fnt, alignLeftCenter)
   y += h
  tmp += '<eLabel position="0,%d"  size="%d,1"  zPosition="1" backgroundColor="#22aaaaaa" />' % (infT + infH, width)
  pT = infT + 3
  pH = infH - 6
  pW = int(pH * 1.66)
  pL = width - pW - 12
  tmp += '<widget name="myPiconF"   position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#0a5555" />'  % (pL    , pT    , pW  , pH)
  tmp += '<widget name="myPiconBG"  position="%d,%d" size="%d,%d" zPosition="3" backgroundColor="#0a220000" />' % (pL + 1, pT + 1, pW - 2 , pH - 2)
  tmp += '<widget name="myPiconPic" position="%d,%d" size="%d,%d" zPosition="4" alphatest="blend" />'    % (pL + 2, pT + 2, pW - 4 , pH - 5)
  y = boxT + boxH
  for i in range(totRows - 1):
   tmp += '<eLabel position="0,%d"  size="%d,1" zPosition="1" backgroundColor="#00555555" />' % (y, width)
   y += boxH
  x = boxW
  h = height - barHeight - boxT
  for i in range(totCols - 1):
   tmp += '<eLabel position="%d,%d"  size="1,%d" zPosition="1" backgroundColor="#00555555" />' % (x, boxT-2, h)
   x += boxW
  tmp += '<widget name="myPiconPtr" position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#00aaaa00"/>' % (0, boxT, boxW, boxH)
  gap  = marginTop
  gap1 = int(gap / 2.0)
  for row in range(totRows):
   boxL = 0
   for col in range(totCols):
    tmp += '<widget name="myPicon%d%d"     position="%d,%d" size="%d,%d" zPosition="4" alphatest="blend" />' % (row, col, boxL+gap1, boxT+gap1, boxW-gap, picH-2)
    tmp += '<widget name="myPiconLbl%d%d"  position="%d,%d" size="%d,%d" zPosition="5" backgroundColor="#00003333" font="%s;%d" %s />' % (row, col, boxL+gap1, lblT, boxW-gap, lblH-2, VVFwML, lblFont, alignCenter)
    boxL += boxW
   boxT += boxH
   lblT += boxH
 elif winType == VV1GIX:
  totRows = 6
  totCols = 8
  tstW = int(width - marginLeft  * 2)
  tstH = int(height * 0.15)
  tstT = int(height - barHeight - tstH)
  boxT = titleH + 2
  boxW = int(width  / totCols)
  boxH = int((height - barHeight - tstH - boxT) / totRows)
  tmp += '<widget name="myColorPtr" position="%d,%d" size="%d,%d" zPosition="1" backgroundColor="#00aaaa00" />' % (0, boxT, boxW, boxH)
  gap  = marginTop
  gap1 = int(gap / 2.0)
  for row in range(totRows):
   boxL = 0
   for col in range(totCols):
    tmp += '<widget name="myColor%d%d" position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#00000000" />' % (row, col, boxL+gap1, boxT+gap1, boxW-gap, boxH-gap)
    boxL += boxW
   boxT += boxH
  tmp += '<widget name="myColorTst" position="%d,%d" size="%d,%d" zPosition="2" backgroundColor="#00aaaaaa" %s %s />' % (marginLeft, tstT, tstW, tstH, alignCenter, bodyFontStr)
 elif winType == VVCyHa:
  tmp += '<widget name="myPic" position="%d,%d" size="%d,%d" zPosition="4" alphatest="blend" />' % (marginLeft, bodyTop, bodyW, bodyH)
 else:
  if   winType == VV0L7B : align = alignLeftCenter
  elif winType == VVhfwD : align = alignLeftTop
  else          : align = alignCenter
  if winType == VVV9ui:
   iconSize = 60
   iconLeft = int(ratioH  * 20)
   iconTop  = int(bodyTop + (height - bodyTop - iconSize) / 2.0)
   iconW  = iconSize + iconLeft * 2
   marginLeft += iconW
   bodyW  -= iconW
   tmp += '<widget name="errPic" position="%d,%d" size="%d,%d" zPosition="4" alphatest="blend" />' % (iconLeft, iconTop, iconSize, iconSize)
  fontName = VVFwML
  if usefixedFont and winType == VVhfwD:
   fnt = "Fixed"
   if fnt in FFBl25():
    fontName = "Fixed"
  moreParams = 'backgroundColor="%s" foregroundColor="#ffffff" font="%s;%d" %s ' % (bodyColor, fontName, bodyFontSize, align)
  tmp += '<widget name="myLabel" position="%d,%d" size="%d,%d" zPosition="4" %s />' % (marginLeft, bodyTop, bodyW, bodyH, moreParams)
 infoW  = int(ratioW  * 500)
 infoH  = int(ratioH  * 100)
 infoLeft = int((width - infoW) / 2.0)
 infoTop  = int((height - infoH) / 2.0)
 VVmp7B = int(ratioH  * 30)
 tmp += '<widget name="myInfoFrame" position="%d,%d" size="%d,%d" zPosition="20" backgroundColor="#aaaa00" />' % (infoLeft, infoTop, infoW, infoH)
 tmp += '<widget name="myInfoBody"  position="%d,%d" size="%d,%d" zPosition="21" backgroundColor="#550000" foregroundColor="#ffff00" font="%s;%d" %s />' % (infoLeft+2, infoTop+2, infoW-4, infoH-4, VVFwML, VVmp7B, alignCenter)
 if topRightBtns > 0:
  gap  = 6
  sz  = titleH - gap * 2
  mnuL = width - sz - gap * 2
  infL = mnuL if topRightBtns == 3 else mnuL - sz - gap
  par = 'size="%d,%d" zPosition="20" alphatest="blend"' % (sz, sz)
  if topRightBtns in (1, 2): tmp += '<widget name="keyMenu" position="%d,%d" %s />' % (mnuL, gap, par)
  if topRightBtns in (2, 3): tmp += '<widget name="keyInfo" position="%d,%d" %s />' % (infL, gap, par)
 if barHeight > 0:
  lineTop = height - barHeight
  topGap = max(3, int(ratioH  * 3))
  btnTop = lineTop + topGap
  btnH = height - btnTop - topGap
  barFont = int(0.7  * btnH)
  gap  = btnH
  spaceW = gap * (5)
  btnW = int((width - spaceW) / 4)
  left = gap
  name = [ "keyRed"   , "keyGreen" , "keyYellow", "keyBlue"  ]
  VVghPi = [ "#119f1313", "#11005500", "#11a08000", "#1118188b"]
  tmp += '<widget name="myBar"  position="0,%d"  size="%d,%d" zPosition="7" backgroundColor="%s" font="%s;%d" %s />' % (lineTop, width, height - lineTop, titleColor, VVFwML, barFont, alignLeftCenter)
  tmp += '<widget name="myLine" position="0,%d"  size="%d,1"  zPosition="8" backgroundColor="#22aaaaaa" />' % (lineTop, width)
  for i in range(4):
   tmp += '<widget name="%s" position="%d,%d" size="%d,%d" zPosition="9" backgroundColor="%s" font="%s;%d" foregroundColor="white" %s />' % (name[i], left, btnTop, btnW, btnH, VVghPi[i], VVFwML, barFont, alignCenter)
   left += btnW + gap
 if winType == VVhfwD:
  name = [ "keyRedTop", "keyGreenTop" , "keyYellowTop", "keyBlueTop" ]
  VVghPi = [ "#119f1313", "#11005500", "#11a08000", "#1118188b"]
  btnW = int(ratioW  * 85)
  btnH = int(titleH * 0.6)
  btnTop = int(titleH * 0.2)
  btnLeft = width - (btnW + btnTop) * 4
  btnFont = int(btnH * 0.65)
  for i in range(4):
   tmp += '<widget name="%s1" position="%d,%d" size="%d,%d" zPosition="10" backgroundColor="#0affffff" />' % (name[i], btnLeft, btnTop, btnW, btnH)
   tmp += '<widget name="%s"  position="%d,%d" size="%d,%d" zPosition="11" backgroundColor="%s" font="%s;%d" foregroundColor="white" %s />' % (name[i], btnLeft+1, btnTop+1, btnW-2, btnH-2, VVghPi[i], VVFwML, btnFont, alignCenter)
   btnLeft += (btnW + btnTop)
  if addFramedPic:
   picW = int(width  * 0.2)
   picH = int(height * 0.2)
   picLeft = width - picW - marginLeft - scrollBarW * 2
   tmp += '<widget name="myPicF" position="%d,%d" size="%d,%d" zPosition="12" backgroundColor="#0affffff" />' % (picLeft    , bodyTop    , picW  , picH)
   tmp += '<widget name="myPicB" position="%d,%d" size="%d,%d" zPosition="13" backgroundColor="%s" />'   % (picLeft + 1, bodyTop + 1, picW - 2 , picH - 2, bodyColor)
   tmp += '<widget name="myPic"  position="%d,%d" size="%d,%d" zPosition="14" alphatest="blend" />'   % (picLeft + 1, bodyTop + 1, picW - 2 , picH - 2)
 tmp += '</screen>'
 skinParam = {"width":width, "height":height, "titleH":titleH, "marginLeft":marginLeft, "marginTop":marginTop, "titleColor":titleColor, "bodyColor":bodyColor, "bodyFontSize":bodyFontSize, "barHeight":barHeight, "topRightBtns":topRightBtns, "bodyLineH":bodyLineH, "scrollBarW":scrollBarW, "lineGap":lineGap}
 return tmp, skinParam
class Main_Menu(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 800, 850, 50, 50, 30, "#1a002244", "#10002233", 33, barHeight=40)
  self.session  = session
  self.VVVtuF = ""
  self.themsList  = []
  s = "  "
  VV625J = []
  if VVaEAu:
   VV625J.append(("-- MY TEST --"    , "myTest"   ))
  VV625J.append((s + "File Manager"     , "FileManager"  ))
  VV625J.append(VVm77t)
  VV625J.append((s + "Services/Channels"   , "ChannelsTools" ))
  VV625J.append((s + "IPTV"       , "IptvTools"  ))
  VV625J.append((s + "PIcons"      , "PIconsTools"  ))
  VV625J.append((s + "SoftCam"      , "SoftCam"   ))
  VV625J.append(VVm77t)
  VV625J.append((s + "Plugins"      , "PluginsTools" ))
  VV625J.append((s + "Terminal"      , "Terminal"  ))
  VV625J.append((s + "Backup & Restore"    , "BackupRestore" ))
  VV625J.append(VVm77t)
  VV625J.append((s + "Date/Time"     , "Date_Time"  ))
  VV625J.append((s + "Check Internet Connection" , "CheckInternet" ))
  self.totalItems = len(VV625J)
  FFJd2Z(self, VV625J=VV625J)
  FFHhgX(self["keyRed"] , "Exit")
  FFHhgX(self["keyGreen"] , "Settings")
  FFHhgX(self["keyYellow"], "Dev. Info.")
  FFHhgX(self["keyBlue"] , "About")
  self["myActionMap"].actions.update({
   "red"   : self.close      ,
   "green"   : self.VVDWtE     ,
   "yellow"  : self.VVEu74     ,
   "blue"   : self.VVlYGU     ,
   "info"   : self.VVlYGU     ,
   "next"   : self.VVg4pp     ,
   "menu"   : self.VVCbaO   ,
   "text"   : self.VVYnq3    ,
   "0"    : BF(self.VVz8Os, 0)  ,
   "1"    : BF(self.VVI8HV, 1)   ,
   "2"    : BF(self.VVI8HV, 2)   ,
   "3"    : BF(self.VVI8HV, 3)   ,
   "4"    : BF(self.VVI8HV, 4)   ,
   "5"    : BF(self.VVI8HV, 5)   ,
   "6"    : BF(self.VVI8HV, 6)   ,
   "7"    : BF(self.VVI8HV, 7)   ,
   "8"    : BF(self.VVI8HV, 8)   ,
   "9"    : BF(self.VVI8HV, 9)
  })
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
  global VVF5vz, VVPJLC, VVe9cu
  VVF5vz = VVPJLC = VVe9cu = False
 def VVmz9T(self):
  item = FF1N9D(self)
  self.VVI8HV(item)
 def VVI8HV(self, item):
  if item is not None:
   if   item == "myTest"     : self.VVPs2i()
   elif item in ("FileManager"  , 1) : self.session.open(CC7ujK)
   elif item in ("ChannelsTools" , 2) : self.session.open(CCtSdI)
   elif item in ("IptvTools"  , 3) : self.session.open(CCqQHV)
   elif item in ("PIconsTools"  , 4) : self.VVxec7()
   elif item in ("SoftCam"   , 5) : self.session.open(CCGR8s)
   elif item in ("PluginsTools" , 6) : self.session.open(CCBWXm)
   elif item in ("Terminal"  , 7) : self.session.open(CCBZnl)
   elif item in ("BackupRestore" , 8) : self.session.open(CCeVbc)
   elif item in ("Date_Time"  , 9) : self.session.open(CCcG5l)
   elif item in ("CheckInternet" , 10) : self.session.open(CCqwcM)
   else         : self.close()
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
  FFtIlI(self)
  title = "  %s - %s" % (PLUGIN_NAME, VV73TT)
  self["myTitle"].setText(title)
  VVBjP8, VVWMzg, VVq3Od, VVA0Yv, VVHYTk, oldMovieDownloadPath = FFWcGD()
  self.VVrB7z()
  if VVBjP8 or VVWMzg or VVq3Od or VVA0Yv or VVHYTk or oldMovieDownloadPath:
   VVQQs4 = lambda path, subj: "%s:\n%s\n\n" % (subj, FFkhYI(path, VVMmz2)) if path else ""
   txt = "The following directories were not found and were changed to default:\n\n"
   txt += VVQQs4(VVBjP8   , "Backup/Restore Path"    )
   txt += VVQQs4(VVWMzg  , "Created Package Files (IPK/DEB)" )
   txt += VVQQs4(VVq3Od  , "Download Packages (from feeds)" )
   txt += VVQQs4(VVA0Yv , "Exported Tables"     )
   txt += VVQQs4(VVHYTk , "Exported PIcons"     )
   txt += VVQQs4(oldMovieDownloadPath , "Movie/Series Download"   )
   txt += "\nYou can change paths from Settings.\n"
   FFNEkd(self, txt, title="Settings Paths")
  if (EASY_MODE or VV8FUX or VVaEAu):
   FFobAA(self["myTitle"], "#ff0000")
  var = "PLUGIN" + "_VERSION"
  if var in globals():
   FFD1yO(self, "Welcome", 300)
  FFpoMu(BF(self.VV0Djo, title))
 def VV0Djo(self, title):
  if CFG.checkForUpdateAtStartup.getValue():
   url = CCfRRs.VVysnu()
   if url:
    newWebVer = CCfRRs.VVKiP7(url)
    if newWebVer:
     self["myTitle"].setText(title + "  (%s available)" % newWebVer)
 def onExit(self):
  os.system(FFxtg8("rm /tmp/ajpanel*"))
  global VVF5vz, VVPJLC, VVe9cu
  VVF5vz = VVPJLC = VVe9cu = False
 def VVz8Os(self, digit):
  self.VVVtuF += str(digit)
  ln = len(self.VVVtuF)
  global VVF5vz, VVe9cu
  if ln == 4:
   if self.VVVtuF == "0" * ln:
    VVF5vz = True
    FFobAA(self["myTitle"], "#800080")
   else:
    self.VVVtuF = "x"
  elif self.VVVtuF == "0" * 8:
   VVe9cu = True
 def VVg4pp(self):
  self.VVVtuF += ">"
  if self.VVVtuF == "0" * 4 + ">" * 2:
   global VVPJLC
   VVPJLC = True
   FFobAA(self["myTitle"], "#dd5588")
 def VVYnq3(self):
  if self.VVVtuF == "0" * 4:
   ok = False
   fnt = "ae_AlMateen.ttf"
   fontFile = "/usr/share/fonts/%s" % fnt
   if fileExists(fontFile):
    from enigma import addFont
    fontName = "AJPFont"
    try:
     addFont(fontFile, fontName, 100, True)
     ok = True
    except:
     try:
      addFont(fontFile, fontName, 100, True, 0)
      ok = True
     except:
      pass
   if ok: txt = 'Added Font: "%s"' % fnt
   else : txt = '"%s" Not Found' % fnt
   FFD1yO(self, txt, 2000, isGrn=ok)
 def VVxec7(self):
  found = False
  pPath = CCrs3r.VVsNIk()
  if pathExists(pPath):
   for fName, fType in CCrs3r.VVI7Ry(pPath):
    if fName:
     found = True
     break
  if found:
   self.session.open(CCrs3r)
  else:
   VV625J = []
   VV625J.append(("PIcons Tools" , "CCrs3r" ))
   VV625J.append(VVm77t)
   VV625J.append(CCrs3r.VV4E4p())
   VV625J.append(VVm77t)
   VV625J += CCrs3r.VVY39V()
   FFuRfS(self, self.VV4US6, VV625J=VV625J)
 def VV4US6(self, item=None):
  if item:
   if   item == "CCrs3r"   : self.session.open(CCrs3r)
   elif item == "VVdDzi"  : CCrs3r.VVdDzi(self)
   elif item == "VVicWk"  : CCrs3r.VVicWk(self)
   elif item == "findPiconBrokenSymLinks" : CCrs3r.VVSp16(self, True)
   elif item == "FindAllBrokenSymLinks" : CCrs3r.VVSp16(self, False)
 def VVDWtE(self):
  self.session.open(CCfRRs)
 def VVEu74(self):
  self.session.open(CCquCY)
 def VVlYGU(self):
  changeLogFile = VVASCC + "_changeLog.txt"
  txt = ""
  if fileExists(changeLogFile):
   lines  = FFjdnJ(changeLogFile)
   for line in lines:
    line = line.strip()
    if line and not line.startswith("#"):
     if line.startswith("[") and line.endswith("]"):
      line = line.replace("[", "").replace("]", "")
      line = FFkhYI("\n%s\n%s\n%s" % (VVZ1aI, line, VVZ1aI), VVdWFT, VVZgqQ)
     elif line.strip().startswith("-"): line = "\n" + line
     elif line.strip().startswith(".."): line = FFkhYI(line, VVkXS4, VVZgqQ)
     txt += line +"\n"
  else:
   txt += "Change Log file not found:\n%s" % changeLogFile
  FFNEkd(self, txt.strip(), title="%s %s  -  %s  - By AMAJamry" % (PLUGIN_NAME, VV73TT, PLUGIN_DESCRIPTION), VVmp7B=26)
 def VVCbaO(self):
  VV625J = []
  VV625J.append(("Title Colors"   , "title" ))
  VV625J.append(("Menu Area Colors"  , "body" ))
  VV625J.append(("Menu Pointer Colors" , "cursor" ))
  VV625J.append(("Bottom Bar Colors" , "bar"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Reset Colors"   , "reset" ))
  title = "Main Menu Colors"
  FFuRfS(self, BF(self.VVzDCj, title), VV625J=VV625J, width=500, title=title)
 def VVzDCj(self, title, item=None):
  if item:
   if item == "reset":
    FFMIbO(self, self.VVp9aQ, "Reset to default colors ?", title=title)
   else:
    tDict = self.VVl6eu()
    fg = tDict.get("main_%s_fg" % item, "")
    bg = tDict.get("main_%s_bg" % item, "")
    self.session.openWithCallback(BF(self.VVci7L, tDict, item), CCrlqE, defFG=fg, defBG=bg)
 def VVqyGI(self):
  return VVCnD5 + "ajpanel_colors"
 def VVl6eu(self):
  tDict = { "main_title_fg" : ""
    , "main_title_bg" : ""
    , "main_body_fg" : ""
    , "main_body_bg" : ""
    , "main_cursor_fg" : ""
    , "main_cursor_bg" : ""
    , "main_bar_fg"  : ""
    , "main_bar_bg"  : ""
    }
  p = self.VVqyGI()
  if fileExists(p):
   txt = FFqD66(p)
   lst = iFindall(r"(.*[^\s])\s*=\s*(#(?:[A-Fa-f0-9]{8}))", txt, IGNORECASE)
   for txt, c in lst:
    tDict[txt] = c
  return tDict
 def VVci7L(self, tDict, item, fg, bg):
  if fg:
   self.VVfBGs(item, fg)
   self.VVu3b4(item, bg)
   tDict["main_%s_fg" % item] = fg
   tDict["main_%s_bg" % item] = bg
   self.VVLzht(tDict)
 def VVLzht(self, tDict):
   p = self.VVqyGI()
   with open(p, "w") as f:
    for key, val in list(tDict.items()):
     f.write("%s=%s\n" % (key, val))
 def VVfBGs(self, item, fg):
  if   item == "title" : FFlr8P(self["myTitle"], fg)
  elif item == "body"  :
   FFlr8P(self["myMenu"], fg)
   FFlr8P(self["myBody"], fg)
  elif item == "cursor" : self["myMenu"].instance.setForegroundColorSelected(parseColor(fg))
  elif item == "bar"  :
   FFobAA(self["myBar"], fg)
   FFlr8P(self["keyRed"], fg)
   FFlr8P(self["keyGreen"], fg)
   FFlr8P(self["keyYellow"], fg)
   FFlr8P(self["keyBlue"], fg)
 def VVu3b4(self, item, bg):
  if   item == "title" : FFobAA(self["myTitle"], bg)
  elif item == "body"  :
   FFobAA(self["myMenu"], bg)
   FFobAA(self["myBody"], bg)
  elif item == "cursor" : self["myMenu"].instance.setBackgroundColorSelected(parseColor(bg))
  elif item == "bar"  : FFobAA(self["myBar"], bg)
 def VVp9aQ(self):
  os.system(FFxtg8("rm %s" % self.VVqyGI()))
  self.close()
 def VVrB7z(self):
  tDict = self.VVl6eu()
  self.VV5ZND(tDict, "title")
  self.VV5ZND(tDict, "body")
  self.VV5ZND(tDict, "cursor")
  self.VV5ZND(tDict, "bar")
 def VV5ZND(self, tDict, name):
  fg = tDict.get("main_%s_fg" % name, "")
  bg = tDict.get("main_%s_bg" % name, "")
  if fg: self.VVfBGs(name, fg)
  if bg: self.VVu3b4(name, bg)
 def VVPs2i(self):
  CCppdx.VVgElN(self.session)
class CClXbe():
 @staticmethod
 def VVk4qf():
  return [None, "utf-8"] + ["iso-8859-%d" % i for i in range(1,17)] + ["windows-125%d" % i for i in range(1,9)]
 @staticmethod
 def VVE0tE(SELF):
  import sys, locale
  lst = []
  c1 = "#f#00ffbbff#"
  c2 = "#f#00ffffaa#"
  lst.append(("Language Code"     , locale.getdefaultlocale()[0]  ))
  lst.append(("Default Locale Encoding"  , locale.getdefaultlocale()[1]  ))
  lst.append((c1 + "Preferred Encoding"  , c1 + locale.getpreferredencoding(False)))
  lst.append((c2 + "System Default Encoding" , c2 + sys.getdefaultencoding()  ))
  lst.append((c2 + "Filesystem Encoding"  , c2 + sys.getfilesystemencoding() ))
  c = "#f#11aaffff#"
  for item in locale.setlocale(locale.LC_ALL).split(";"):
   parts = item.split("=")
   if len(parts) == 2:
    lst.append((c + parts[0], c +
    parts[1]))
  FF1dQ4(SELF, None, VVvytR=lst, VVmp7B=30, VVX8bj=True)
 @staticmethod
 def VVTBCL(path, SELF=None):
  for enc in CClXbe.VVk4qf():
   try:
    with ioOpen(path, "r", encoding=enc) as f:
     for line in f:
      pass
    return enc
   except:
    pass
  if SELF:
   FFkYsE(SELF, "Cannot detect file encoding for:\n\n%s" % path)
  return -1
 @staticmethod
 def VVq1FC(SELF, path, cbFnc, defEnc="utf8", onlyWorkingEnc=True, title="Select Encoding"):
  FFD1yO(SELF)
  lst = CClXbe.VVuXBb(path, onlyWorkingEnc=onlyWorkingEnc)
  if lst:
   VV625J = []
   for name, enc in lst:
    txt = "%s (%s)" % (name, enc)
    if defEnc == enc:
     txt = FFkhYI(txt, VV9cEK)
    VV625J.append((txt, enc))
   if onlyWorkingEnc: VVz2kc, VVwpZm = "#22003344", "#22002233"
   else    : VVz2kc, VVwpZm = "#22220000", "#22220000"
   FFuRfS(SELF, cbFnc, title=title, VV625J=VV625J, width=900, VVz2kc=VVz2kc, VVwpZm=VVwpZm)
  else:
   FFD1yO(SELF, "No proper encoding", 2000)
 @staticmethod
 def VVuXBb(path, onlyWorkingEnc=True):
  encLst = []
  cPath = VVASCC + "codecs"
  if fileExists(cPath):
   lines = FFjdnJ(cPath)
   for line in lines:
    parts = line.split("\t")
    if len(parts) == 2:
     encLst.append((parts))
  if not encLst:
   tmp = list(CClXbe.VVk4qf())
   tmp.pop(0)
   encLst = [("General", ",".join(tmp))]
  lst = []
  for item in encLst:
   for enc in (item[1].split(",")):
    if onlyWorkingEnc:
     try:
      with ioOpen(path, "r", encoding=enc) as f:
       for line in f:
        pass
      lst.append((item[0], enc))
     except:
      pass
    else:
     lst.append((item[0], enc))
  return lst
class CCquCY(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 900, 650, 50, 40, 30, "#22003300", "#22001100", 30)
  self.session  = session
  VV625J = []
  VV625J.append(("Settings File"        , "SettingsFile"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Box Info"          , "VVjfaN"    ))
  VV625J.append(("Tuners Info"         , "VVSOTW"   ))
  VV625J.append(("Python Version"        , "VV55FI"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Screen Size"         , "ScreenSize"    ))
  VV625J.append(("Language/Locale"        , "Locale"     ))
  VV625J.append(("Processor"         , "Processor"    ))
  VV625J.append(("Operating System"        , "OperatingSystem"   ))
  VV625J.append(("Drivers"          , "drivers"     ))
  VV625J.append(VVm77t)
  VV625J.append(("System Users"         , "SystemUsers"    ))
  VV625J.append(("Logged-in Users"        , "LoggedInUsers"   ))
  VV625J.append(("Uptime"          , "Uptime"     ))
  VV625J.append(VVm77t)
  VV625J.append(("Host Name"         , "HostName"    ))
  VV625J.append(("MAC Address"         , "MACAddress"    ))
  VV625J.append(("Network Configuration"      , "NetworkConfiguration" ))
  VV625J.append(("Network Status"        , "NetworkStatus"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Disk Usage"         , "VVsp2X"    ))
  VV625J.append(("Mount Points"         , "MountPoints"    ))
  VV625J.append(("File System Table (FSTAB)"     , "FileSystemTable"   ))
  VV625J.append(("USB Devices"         , "USB_Devices"    ))
  VV625J.append(("List Block-Devices"       , "listBlockDevices"  ))
  VV625J.append(("Directory Size"        , "DirectorySize"   ))
  VV625J.append(("Memory"          , "Memory"     ))
  VV625J.append(VVm77t)
  VV625J.append(("Loaded Kernel Modules"      , "LoadedKernelModules"  ))
  VV625J.append(("Running Processes"       , "RunningProcesses"  ))
  VV625J.append(("Processes with open files"     , "ProcessesOpenFiles"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Bootloader Second-stage (old DreamBox only)" , "DreamBoxBootloader"  ))
  FFJd2Z(self, VV625J=VV625J, title="Device Information")
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "SettingsFile"    : self.session.open(CCYl6w)
   elif item == "VVjfaN"    : self.VVjfaN()
   elif item == "VVSOTW"   : self.VVSOTW()
   elif item == "VV55FI"   : self.VV55FI()
   elif item == "ScreenSize"    : FFNEkd(self, "Width\t: %s\nHeight\t: %s" % (FFjf8O()[0], FFjf8O()[1]))
   elif item == "Locale"     : CClXbe.VVE0tE(self)
   elif item == "Processor"    : self.VVw8ie()
   elif item == "OperatingSystem"   : FFuCjo(self, "uname -a"        )
   elif item == "drivers"     : self.VVcORE()
   elif item == "SystemUsers"    : FFuCjo(self, "id"          )
   elif item == "LoggedInUsers"   : FFuCjo(self, "who -a"         )
   elif item == "Uptime"     : FFuCjo(self, "uptime"         )
   elif item == "HostName"     : FFuCjo(self, "hostname"        )
   elif item == "MACAddress"    : self.VVhxaJ()
   elif item == "NetworkConfiguration"  : FFuCjo(self, "ifconfig %s %s" % (FF95sl("HWaddr", VVyFMl), FF95sl("addr:", VVdWFT)))
   elif item == "NetworkStatus"   : FFuCjo(self, "netstat -tulpn"       )
   elif item == "VVsp2X"    : self.VVsp2X()
   elif item == "MountPoints"    : FFuCjo(self, "mount %s" % (FF95sl(" on ", VVdWFT)))
   elif item == "FileSystemTable"   : FFuCjo(self, "cat /etc/fstab"       )
   elif item == "USB_Devices"    : FFuCjo(self, "lsusb"         )
   elif item == "listBlockDevices"   : FFuCjo(self, "blkid"         )
   elif item == "DirectorySize"   : FFuCjo(self, "du -shc /* | sed '/total/i-----\t-------------' | sed 's/total/TOTAL/g'", VVEem5="Reading size ...")
   elif item == "Memory"     : FFuCjo(self, "cat /proc/meminfo | sed 's/ //g' | sed 's/:/\t: /g' | sed '/MemAvailable/a%s'" % ("-" * 25))
   elif item == "LoadedKernelModules"  : self.VVjV2C()
   elif item == "RunningProcesses"   : FFuCjo(self, "ps"          )
   elif item == "ProcessesOpenFiles"  : FFuCjo(self, "lsof"         )
   elif item == "DreamBoxBootloader"   : self.VVUDe8()
   else         : self.close()
 def VVhxaJ(self):
  res = FF3DIX("ip link")
  list = iFindall(r"[0-9]+:\s+(.+):\s+.+\n.+\s+(.+)brd", res, IGNORECASE)
  if list:
   txt = ""
   for item in list:
    brd = item[0].upper()
    mac = item[1].upper()
    if not brd == "LO":
     txt += "%s\t: %s\n" % (item[0].upper(), item[1].upper())
   FFNEkd(self, txt)
  else:
   FFuCjo(self, "ip link")
 def VVnF7S(self, cmd, headerRepl, length, use2Spaces):
  if headerRepl:
   cmd += " | sed 's/%s/%s/g'" % (headerRepl, headerRepl.replace(" ", "_"))
  if use2Spaces:
   col = ""
   for i in range(length):
    col += "$%d" % (i + 1)
    if i < length - 1:
     col += '"#"'
   cmd += " | awk -F '  +' '{print(%s)}'" % col
  else:
   cmd += " | sed 's/[* ]\+/\#/g'"
  lines = FFiGf6(cmd)
  return lines
 def VVjEts(self, lines, headerRepl, widths, VVQqg2):
  VVvhuK = []
  header  = []
  for ndx, line in enumerate(lines):
   if ndx == 0 and headerRepl:
    line = line.replace(headerRepl.replace(" ", "_"), headerRepl)
   parts = line.split("#")
   if ndx == 0 : header = parts
   else  : VVvhuK.append(parts)
  if VVvhuK and len(header) == len(widths):
   VVvhuK.sort(key=lambda x: x[0].lower())
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VVX8bj=True)
   return True
  else:
   return False
 def VVsp2X(self):
  headerRepl = "Mounted on"
  cmd   = "df -Th"
  txt = FF3DIX(cmd)
  if not "invalid option" in txt:
   lines  = self.VVnF7S(cmd, headerRepl, 6, False)
   widths  = (25 , 12 , 10 , 9  , 10 , 9  , 25 )
   VVQqg2 = (LEFT , CENTER, CENTER, CENTER, CENTER, CENTER, LEFT )
   allOK = self.VVjEts(lines, headerRepl, widths, VVQqg2)
  else:
   cmd = "df -h"
   lines  = self.VVnF7S(cmd, headerRepl, 6, False)
   widths  = (28 , 11 , 11 , 11 , 11 , 28 )
   VVQqg2 = (LEFT , CENTER, CENTER, CENTER, CENTER, LEFT )
   allOK = self.VVjEts(lines, headerRepl, widths, VVQqg2)
  if not allOK:
   lines = FFiGf6(cmd)
   if lines:
    mountList = [os.path.join(p.mountpoint, "") for p in harddiskmanager.getMountedPartitions()]
    mountList = [FFkEOw(x) for x in mountList]
    mountList = tuple(mountList)
    txt   = ""
    note  = ""
    if VV9cEK:
     note = "\n%s" % FFkhYI("Green = Mounted Partitions", VV9cEK)
    lines = lines[:1] + sorted(lines[1:])
    for line in lines:
     if "Use%" in line:
      line = line.replace(headerRepl.replace(" ", "_"), headerRepl)
      color = VVdWFT
     elif line.endswith(mountList) : color = VV9cEK
     else       : color = VVkXS4
     txt += FFkhYI(line, color) + "\n"
    FFNEkd(self, txt + note)
   else:
    FFkYsE(self, "Not data from system !")
 def VVjV2C(self):
  cmd   = "lsmod"
  headerRepl = "Used by"
  lines  = self.VVnF7S(cmd, headerRepl, 3, True)
  widths  = [30 , 15 , 55 ]
  VVQqg2 = (LEFT , CENTER, LEFT )
  allOK = self.VVjEts(lines, headerRepl, widths, VVQqg2)
  if not allOK:
   FFuCjo(self, cmd)
 def VVcORE(self):
  cmd = FFaG6T(VVPeIJ, "| grep -e '-blindscan-\|dvb-modules\|-grab-\|-libs-\|-loadmodules-\|-opengl\|-partitions-\|-reader-\|-showiframe-'")
  if cmd : FFuCjo(self, cmd)
  else : FFHRK6(self)
 def VVw8ie(self):
  cmd  = "RES=$(uname -m | awk '{print(toupper($0))}');"
  cmd += "if [ -z \"$RES\" ] ; then RES=$(uname -a | awk '{print(toupper($12))}'); fi;"
  cmd += "if [ -z \"$RES\" ] ; then echo 'Could not read Info.!'; else echo $RES; fi"
  FFuCjo(self, cmd)
 def VVUDe8(self):
  cmd = FFaG6T(VVmDYa, "| grep secondstage")
  if cmd : FFuCjo(self, 'output=$(%s); if [ -z "$output" ] ; then echo "Not found for this receiver."; else echo $output; fi' % cmd)
  else : FFHRK6(self)
 def VVjfaN(self):
  c = VV9cEK
  VVvytR = []
  VVvytR.append((FFkhYI("Box Type"  , c), FFkhYI(self.VVyMgk("boxtype").upper(), c)))
  VVvytR.append((FFkhYI("Board Version", c), FFkhYI(self.VVyMgk("board_revision") , c)))
  VVvytR.append((FFkhYI("Chipset"  , c), FFkhYI(self.VVyMgk("chipset")  , c)))
  VVvytR.append((FFkhYI("S/N"   , c), FFkhYI(self.VVyMgk("sn")    , c)))
  VVvytR.append((FFkhYI("Version"  , c), FFkhYI(self.VVyMgk("version")  , c)))
  VV7b0I   = []
  VVQOCL = ""
  try:
   from Components.SystemInfo import SystemInfo
   keysList = list(SystemInfo)
   if keysList:
    for key in keysList:
     if key == "canMultiBoot":
      VVQOCL = SystemInfo[key]
     else:
      VV7b0I.append((FFkhYI(str(key), VVpHwQ), FFkhYI(str(SystemInfo[key]), VVpHwQ)))
  except:
   pass
  if VVQOCL:
   VVdM9i = self.VVBkbV(VVQOCL)
   if VVdM9i:
    VVdM9i.sort(key=lambda x: x[0].lower())
    VVvytR += VVdM9i
  if VV7b0I:
   VV7b0I.sort(key=lambda x: x[0].lower())
   VVvytR += VV7b0I
  if VVvytR:
   header  = ("Subject" , "Value")
   widths  = (40    , 60)
   FF1dQ4(self, None, header=header, VVvytR=VVvytR, VVoJsQ=widths, VVmp7B=28, VVX8bj=True)
  else:
   FFNEkd(self, "Could not read info!")
 def VVyMgk(self, fileName):
  fileName = "/proc/stb/info/" + fileName
  if fileExists(fileName):
   try:
    txt = FFjdnJ(fileName)[0]
    if txt:
     return txt
   except:
    pass
  return "-"
 def VVBkbV(self, mbDict):
  try:
   mbList = list(mbDict)
   VVvytR = []
   for key in mbList:
    bootDict = mbDict[key]
    device  = bootDict.get("device"  , "")
    rootsubdir = bootDict.get("rootsubdir" , "")
    startupfile = bootDict.get("startupfile", "")
    subject  = "Multiboot-" + str(key)
    value  = ""
    if startupfile : subject += " ... "      + startupfile
    if rootsubdir : value  += "Root-Sub-Dir = %s  ...  " % rootsubdir
    if device  : value  += "Device = "     + device
    if not value:
     value  = str(bootDict)
    VVvytR.append((FFkhYI(subject, VVdWFT), FFkhYI(value, VVdWFT)))
  except:
   pass
  return VVvytR
 def VVSOTW(self):
  txt = self.VVuAQQ("/proc/stb/bus/nim_sockets")
  if not txt: txt = self.VVuAQQ("/proc/bus/nim_sockets")
  if not txt: txt = self.VVUbGq()
  txt = txt.strip()
  if not txt:
   txt = "Could not read info!"
  FFNEkd(self, txt)
 def VVUbGq(self):
  txt = ""
  VVQQs4 = lambda x, y: "%s\t: %s\n" % (x, str(y))
  try:
   for slot in nimmanager.nim_slots:
    if slot.frontend_id is not None:
     slotName = VVQQs4("Slot Name" , slot.getSlotName())
     txt += FFkhYI(slotName, VVdWFT)
     txt += VVQQs4("Description"  , slot.getFullDescription())
     txt += VVQQs4("Frontend ID"  , slot.frontend_id)
     txt += VVQQs4("I2C ID"   , slot.getI2C())
     txt += "\n"
  except:
   pass
  return txt
 def VVuAQQ(self, fileName):
  txt = ""
  if fileExists(fileName):
   try   : lines = FFjdnJ(fileName)
   except: lines = None
   if lines:
    for line in lines:
     if line.endswith(":"):
      line = FFkhYI(line, VVdWFT)
      if txt:
       txt += "\n"
     elif ":" in line:
      parts = line.split(":")
      if len(parts[0]) > 12 : tab = "\t: "
      else     : tab = "\t\t: "
      line = line.replace(":", tab)
     if not "Has_Outputs" in line:
      txt += line + "\n"
  return txt
 def VV55FI(self):
  from sys import version_info
  major   = version_info[0]
  minor   = version_info[1]
  micro   = version_info[2]
  releaselevel = version_info[3]
  serial   = version_info[4]
  txt = "Version\t: %d.%d.%d\n" % (major, minor, micro)
  txt += "Release\t: %s\n"  % releaselevel
  txt += "Serial\t: %d\n"   % serial
  FFNEkd(self, txt)
 @staticmethod
 def VVWIWg():
  def VVQQs4(v, ndx):
   lst = v.split(";")[ndx].split(",")
   return {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
  v = "openbox,OpenBox,openpli,OpenPLI,openvision,OpenVision;areadeltasat,ArEaDeltaSat,cobralibero,Cobralibero,opentr,OpenTR,peter,PeterPan;italysat,ItalySat,oozoon,OoZooN,openatv,openATV,openeight,OpenEight,openmips,OpenMips,opennfr,OpenNFR,openplus,OpenPlus,openspa,OpenSPA,pure2,Pure2,rudream,ruDream,teamblue,teamBlue,titannit,OpenAFF_Titan"
  v = {"/etc/issue": VVQQs4(v,0), "/etc/issue.net": VVQQs4(v,1), "/etc/image-version": VVQQs4(v,2)}
  for p1, d in list(v.items()):
   img = CCquCY.VVc4kq(p1, d)
   if img: return img
  v = "Blackhole,Blackhole,DE,Dream-Elite,EGAMI,Egami,LT,LT,MediaSat,MediaSat,OPENDROID,OpenDroid,Bp/geminimain,GP3;Domica,Domica,SatLodge,Satlodge,Satdreamgr,SatdreamGr,TSimage,OpenTS_Ts,newnigma2,newnigma2;DemonisatManager,DDD-Demoni,VTIPanel,VTI,ViX,OpenVIX;AddOnManager,Merlin3,DreamOSatcamManager,DreamOSat CamManager,ExtraAddonss,OpenESI,HDF-Toolbox,OpenHDF,HDMUCenter,HDMU,LDteam,OpenLD,NssPanel,NonSoloSat,PKT,PKT,PowerboardCenter,PBNigma-VX,TDW,TDW"
  p = "/usr/lib/enigma2/python/"
  v = {p: VVQQs4(v,0), p + "Plugins/": VVQQs4(v,1), VVuVce: VVQQs4(v,2), VV9VaA: VVQQs4(v,3)}
  for p1, d in list(v.items()):
   img = CCquCY.VVGbjE(p1, d)
   if img: return img
  return "OpenBlackhole" if iGlob("%sScreens/BpBlue.p*" % p) else ""
 @staticmethod
 def VVc4kq(path, d):
  if fileExists(path):
   txt = FFqD66(path).lower()
   for key, val in list(d.items()):
    if key in txt: return val
  return ""
 @staticmethod
 def VVGbjE(path, d):
  for key, val in list(d.items()):
   if pathExists(path + key): return val
  return ""
class CCYl6w(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 700, 630, 50, 40, 30, "#22003300", "#22001100", 30)
  self.session  = session
  VV625J = []
  VV625J.append(("Settings (All)"   , "Settings_All"   ))
  VV625J.append(("Settings (Hot Keys)"  , "Settings_HotKeys"  ))
  if VVPJLC:
   VV625J.append(("Settings (FHDG-17)" , "Settings_FHDG_17"  ))
  VV625J.append(("Settings (Tuner/DiSEqC)" , "Settings_Tuner_DiSEqC" ))
  VV625J.append(("Settings (Plugins)"  , "Settings_Plugins"  ))
  VV625J.append(("Settings (Usage)"   , "Settings_Usage"   ))
  VV625J.append(("Settings (Time Zone)"  , "Settings_TimeZone"  ))
  VV625J.append(("Settings (Skin)"   , "Settings_Skin"   ))
  FFJd2Z(self, VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   cmd  = "cat %ssettings" % VV609C
   grep = " | grep "
   if   item == "Settings_All"    : FFuCjo(self, cmd                )
   elif item == "Settings_HotKeys"   : FFuCjo(self, cmd + grep + "'config.misc.hotkey.\|config.misc.ButtonSetup.'" )
   elif item == "Settings_FHDG_17"   : FFuCjo(self, cmd + grep + "'config.plugins.setupGlass17.'"      )
   elif item == "Settings_Tuner_DiSEqC" : FFuCjo(self, cmd + grep + "'config.Nims.'"          )
   elif item == "Settings_Plugins"   : FFuCjo(self, cmd + grep + "'.plugins.\|config.TS'"        )
   elif item == "Settings_Usage"   : FFuCjo(self, cmd + grep + "'.usage.'"           )
   elif item == "Settings_TimeZone"  : FFuCjo(self, cmd + grep + "'.timezone.'"          )
   elif item == "Settings_Skin"   : FFuCjo(self, cmd + grep + "'.skin.'"           )
   else         : self.close()
class CCGR8s(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 950, 800, 50, 40, 30, "#22003300", "#22001100", 30)
  self.session  = session
  self.VVfyF5, VVxCEe, VVlwNO, camCommand = FFsttR()
  self.VVxCEe = VVxCEe
  self.camInfo_cmd = camCommand + " -V 2> /dev/null"
  camName = "SoftCam"
  nC = oC = c = ""
  if VVxCEe:
   c = VVk6tE if VVlwNO else VVNTmM
   if   "oscam" in VVxCEe : camName, oC = "OSCam", c
   elif "ncam"  in VVxCEe : camName, nC = "NCam" , c
  VV625J = []
  VV625J.append(("OSCam Files" , "OSCamFiles"  ))
  VV625J.append(("NCam Files" , "NCamFiles"  ))
  VV625J.append(("CCcam Files" , "CCcamFiles"  ))
  VV625J.append(VVm77t)
  VV625J.append((VVoTT6 + 'Convert "/etc/CCcam.cfg" to OSCam/NCam Readers', "VVqOQS" ))
  VV625J.append(VVm77t)
  VV625J.append((oC + "OSCam Readers Table (oscam.server)" , "OSCamReaders" ))
  VV625J.append((nC + "NCam Readers Table (ncam.server)" , "NSCamReaders" ))
  VV625J.append(VVm77t)
  camCmd = os.path.basename(camCommand)
  txt = "%s Settings%s" % (camName, "" if camCmd in ("oscam", "ncam") else " ( %s )" % camCmd)
  if VVxCEe: VV625J.append((c + txt  , "camInfo" ))
  else  : VV625J.append((txt  ,    ))
  VV625J.append(VVm77t)
  camLst = ((c + camName + " Live Status" , "camLiveStatus" )
    , (c + camName + " Live Readers", "camLiveReaders" )
    , (c + camName + " Live Log" , "camLiveLog"  ))
  if VVxCEe:
   for item in camLst: VV625J.append(item)
  else:
   for item in camLst: VV625J.append((item[0], ))
  FFJd2Z(self, VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "OSCamFiles"  : self.session.open(BF(CCY47A, "oscam"))
   elif item == "NCamFiles"  : self.session.open(BF(CCY47A, "ncam"))
   elif item == "CCcamFiles"  : self.session.open(BF(CCY47A, "cccam"))
   elif item == "VVqOQS" : self.VVqOQS()
   elif item == "OSCamReaders"  : self.VVvuHC("os")
   elif item == "NSCamReaders"  : self.VVvuHC("n")
   elif item == "camInfo"   : FFJxAr(self, self.camInfo_cmd)
   elif item == "camLiveStatus" : FF8dax(self.session, CC97UC.VVU0pj)
   elif item == "camLiveReaders" : FF8dax(self.session, CC97UC.VVJP20)
   elif item == "camLiveLog"  : FF8dax(self.session, CC97UC.VVwYRS)
   else       : self.close()
 def VVqOQS(self):
  path = "/etc/CCcam.cfg"
  outFile = "%scccam_to_reader_%s.txt" % (VVCnD5, FFGuM2())
  if fileExists(path):
   lines = FFjdnJ("/etc/CCcam.cfg")
   lst = []
   for line in lines:
    line = line.strip()
    if line.startswith("C:"):
     while "  " in line: line = line.replace("  ", " ")
     parts = line.split(" ")
     if len(parts) == 5:
      CTxt, host, port, User, Pass = parts
      lst.append((host, port, User, Pass))
   newLine = []
   if lst:
    VVQQs4 = lambda txt, val: "%s= %s\n" % (txt.ljust(30), str(val))
    with open(outFile, "w") as f:
     for ndx, item in enumerate(lst):
      host, port, User, Pass = item
      f.write("[reader]\n")
      f.write(VVQQs4("label"    , "CCcam-Line-%d" % ndx))
      f.write(VVQQs4("description"  , "CCcam-Line-%d" % ndx))
      f.write(VVQQs4("protocol"   , "cccam"))
      f.write(VVQQs4("device"    , "%s,%s" % (host, port)))
      f.write(VVQQs4("user"    , User))
      f.write(VVQQs4("password"   , Pass))
      f.write(VVQQs4("fallback"   , "1"))
      f.write(VVQQs4("group"    , "64"))
      f.write(VVQQs4("cccversion"   , "2.3.2"))
      f.write(VVQQs4("audisabled"   , "1"))
      f.write("\n")
    tot = len(lst)
    FFewCE(self, "Output = %d Reader%s in:\n\n%s" % (tot, FFICXm(tot), outFile))
   else:
    FFD1yO(self, "No valid CCcam lines", 1500)
  else:
   FFD1yO(self, "%s not found" % path, 1500)
 def VVvuHC(self, camPrefix):
  VVvhuK = self.VVXMM9(camPrefix)
  if VVvhuK:
   VVvhuK.sort(key=lambda x: int(x[0]))
   if self.VVxCEe and self.VVxCEe.startswith(camPrefix):
    VV3th8 = ("Toggle State", self.VVboMk, [camPrefix], "Changing State ...")
   else:
    VV3th8 = None
   header   = ("No." , "State", "Label", "Description", "URL", "Port", "Protocol", "User", "Password")
   widths   = (4  , 5   , 21    , 18     , 14  , 7  , 11   , 10  , 10   )
   VVQqg2  = (CENTER, CENTER , LEFT   , LEFT    , LEFT , CENTER, LEFT  , LEFT, LEFT  )
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VV3th8=VV3th8, VVKNen=True)
 def VVXMM9(self, camPrefix):
  readersFile = self.VVfyF5 + camPrefix + "cam.server"
  VVvhuK = []
  if fileExists(readersFile):
   tag   = "[reader]"
   lines  = FFjdnJ(readersFile)
   tagFound = False
   enable  = label = description = url = port = protocol = User = password = ""
   onStr  = "#f#1100ff00#" + "ON"
   offStr  = "OFF"
   for ndx, line in enumerate(lines):
    if tag in line.lower() or ndx >= len(lines) - 1:
     if enable or label or description or url or port or protocol or User or password:
      if enable == "":
       enable = onStr
      VVvhuK.append((str(len(VVvhuK) + 1),enable, label, description, url, port, protocol, User, password))
     enable = label = description = url = port = protocol = User = password = ""
    elif "=" in line:
     parts = line.split("=")
     key  = parts[0].strip().lower()
     val  = parts[1].strip()
     if   key == "label"   : label   = val
     elif key == "description" : description = val
     elif key == "protocol"  : protocol  = val
     elif key == "user"   : User   = val
     elif key == "password"  : password  = val
     elif key == "enable"  :
      if val == "0" : enable = offStr
      else   : enable = onStr
     elif key == "device"  :
      if "," in val:
       parts = val.split(",")
       url  = parts[0].strip()
       port = parts[1].strip()
      else:
       url, port = val, ""
   if not VVvhuK:
    FFkYsE(self, "No readers found !")
  else:
   FFAVqd(self, readersFile)
  return VVvhuK
 def VVboMk(self, VVcpnp, camPrefix):
  confFile  = "%s%scam.conf" % (self.VVfyF5, camPrefix)
  readerState  = VVcpnp.VVQYAy(1)
  readerLabel  = VVcpnp.VVQYAy(2)
  if "off" in readerState.lower() : newState = "enable"
  else       : newState = "disable"
  urlAction = "&label=%s&action=%s" % (readerLabel, newState)
  urlStuff = CCGR8s.VVXbEU(self, camPrefix, confFile, "readerlist", urlAction)
  if urlStuff:
   UrlRequest, elementTree = urlStuff
   try:
    page = iUrlopen(UrlRequest, timeout=4)
   except Exception as e:
    VVcpnp.VVhzNf()
    FFkYsE(self, "Cannot connect to SoftCAM !\n\nError = %s" % str(e))
    return
   VVvhuK = self.VVXMM9(camPrefix)
   if VVvhuK:
    VVcpnp.VVuVux(VVvhuK)
  else:
   VVcpnp.VVhzNf()
 @staticmethod
 def VVXbEU(SELF, camPrefix, confFile, urlPart, urlAction):
  if fileExists(confFile):
   lines = FFjdnJ(confFile)
   user = "root"
   pwd  = port = ""
   if lines:
    webif = False
    for line in lines:
     line = line.strip().lower()
     if "[webif]" in line:
      webif = True
     if webif and "=" in line:
      if   line.startswith("httpuser") : user = line.split("=")[1].strip()
      elif line.startswith("httppwd")  : pwd = line.split("=")[1].strip()
      elif line.startswith("httpport") : port = line.split("=")[1].strip()
   if not webif:
    FFkYsE(SELF, "Cannot connect to SoftCAM Web Interface !")
    return None
   elif not port:
    FFkYsE(SELF, "SoftCAM Web Port not found in file:\n\n%s" % confFile)
    return None
  else:
   FFAVqd(SELF, confFile)
   return None
  if not iRequest:
   FFkYsE(SELF, "Module not found\n\nurllib/urllib2")
   return None
  if not CCGR8s.VVLXcG(SELF):
   return None
  try:
   url = "http://127.0.0.1:%s/%scamapi.html?part=%s%s" % (port, camPrefix, urlPart, urlAction)
   acceccManager  = HTTPPasswordMgrWithDefaultRealm()
   acceccManager.add_password(None, url, user, pwd)
   handlers   = HTTPDigestAuthHandler(acceccManager)
   opener    = build_opener(HTTPHandler, handlers)
   install_opener(opener)
   return iRequest(url), iElem
  except Exception as e:
   FFkYsE(SELF, "Error while preparing URL Request !\n\n %s" % str(e))
   return None
 @staticmethod
 def VVLXcG(SELF):
  if iElem:
   return True
  else:
   FFkYsE(SELF, "Module not found:\n\nxml.etree")
   return False
class CCY47A(Screen):
 def __init__(self, VVnUxC, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 700, 650, 50, 40, 30, "#22003300", "#22001100", 30)
  self.session  = session
  self.VVfyF5, VVxCEe, VVlwNO, camCommand = FFsttR()
  if   VVnUxC == "ncam" : self.prefix = "n"
  elif VVnUxC == "oscam" : self.prefix = "os"
  else     : self.prefix = ""
  VV625J = []
  if self.prefix == "":
   VV625J.append(("CCcam.cfg"         , "c_CCcam_cfg"  ))
   VV625J.append(("ecm.info"          , "c_ecm_info"  ))
  else:
   VV625J.append(("AutoRoll.Key"         , "x_AutoRoll_Key" ))
   VV625J.append(("constant.cw"         , "x_constant_cw" ))
   VV625J.append((self.prefix + "cam.ccache"      , "x_cam_ccache" ))
   VV625J.append((self.prefix + "cam.conf"      , "x_cam_conf"  ))
   VV625J.append((self.prefix + "cam.dvbapi"      , "x_cam_dvbapi" ))
   VV625J.append((self.prefix + "cam.provid"      , "x_cam_provid" ))
   VV625J.append((self.prefix + "cam.server"      , "x_cam_server" ))
   VV625J.append((self.prefix + "cam.services"     , "x_cam_services" ))
   VV625J.append((self.prefix + "cam.srvid2"      , "x_cam_srvid2" ))
   VV625J.append((self.prefix + "cam.user"      , "x_cam_user"  ))
   VV625J.append(VVm77t)
   VV625J.append(("SoftCam.Key / SoftCam.key"     , "x_SoftCam_Key" ))
   VV625J.append(("CCcam.cfg"         , "x_CCcam_cfg"  ))
   VV625J.append(VVm77t)
   VV625J.append((self.prefix + "cam.log (last 100 lines)"  , "x_cam_log"  ))
   VV625J.append((self.prefix + "cam.log-prev (last 100 lines)" , "x_cam_log_prev" ))
   VV625J.append((self.prefix + "cam.pid"      , "x_cam_pid"  ))
  FFJd2Z(self, VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  pathTmp = "/tmp/"
  if item is not None:
   if   item == "c_CCcam_cfg"  : FFsdMh(self, "/var/etc/CCcam.cfg"      )
   elif item == "c_ecm_info"  : FFsdMh(self, "/tmp/ecm.info"       )
   elif item == "x_AutoRoll_Key" : FFsdMh(self, self.VVfyF5 + "AutoRoll.Key"   )
   elif item == "x_constant_cw" : FFsdMh(self, self.VVfyF5 + "constant.cw"   )
   elif item == "x_cam_ccache"  : self.VVLgcZ("cam.ccache"        )
   elif item == "x_cam_conf"  : self.VVLgcZ("cam.conf"        )
   elif item == "x_cam_dvbapi"  : self.VVLgcZ("cam.dvbapi"        )
   elif item == "x_cam_provid"  : self.VVLgcZ("cam.provid"        )
   elif item == "x_cam_server"  : self.VVLgcZ("cam.server"        )
   elif item == "x_cam_services" : self.VVLgcZ("cam.services"       )
   elif item == "x_cam_srvid2"  : self.VVLgcZ("cam.srvid2"        )
   elif item == "x_cam_user"  : self.VVLgcZ("cam.user"        )
   elif item == "x_VVZ1aI"   : pass
   elif item == "x_SoftCam_Key" : self.VVWnA5()
   elif item == "x_CCcam_cfg"  : FFsdMh(self, self.VVfyF5 + "CCcam.cfg"    )
   elif item == "x_VVZ1aI"   : pass
   elif item == "x_cam_log"  : FFsdMh(self, pathTmp + self.prefix + "cam.log"   )
   elif item == "x_cam_log_prev" : FFsdMh(self, pathTmp + self.prefix + "cam.log-prev"  )
   elif item == "x_cam_pid"  : FFsdMh(self, pathTmp + self.prefix + "cam.pid"   )
   else       : self.close()
 def VVLgcZ(self, fileName):
  FFsdMh(self, self.VVfyF5 + self.prefix + fileName)
 def VVWnA5(self):
  path = self.VVfyF5 + "SoftCam.Key"
  if fileExists(path) : FFsdMh(self, path)
  else    : FFsdMh(self, path.replace(".Key", ".key"))
class CC97UC(Screen):
 VVU0pj  = 0
 VVJP20 = 1
 VVwYRS = 2
 def __init__(self, session, VVfyF5="", VVxCEe="", VVlwNO="", VV0qsI=VVU0pj):
  self.skin, self.skinParam = FF896P(VVhfwD, 1400, 800, 50, 30, 20, "#22002030", "#33000011", 25, barHeight=40)
  self.session   = session
  self.VVlwNO   = VVlwNO
  self.VV0qsI  = VV0qsI
  self.fileTime   = ""
  self.timer    = eTimer()
  self.timerRunning  = False
  self.Title    = "Live Log"
  self.readersFile  = VVfyF5 + VVxCEe + ".server"
  self.elementTree  = None
  self.UrlRequest   = None
  self.camWebIfData  = None
  self.camWebIfErrorFound = False
  self.user    = "root"
  self.pwd    = ""
  self.port    = ""
  if "oscam" in VVxCEe : titleTxt, self.camPrefix = "OSCam", "os"
  else     : titleTxt, self.camPrefix = "NCam" , "n"
  self.confFile   = "%s%scam.conf" % (VVfyF5, self.camPrefix)
  if self.VV0qsI == self.VVU0pj:
   self.Title   = "  %s Status"  % titleTxt
   self.period   = 10000
  elif self.VV0qsI == self.VVJP20:
   self.Title   = "  %s Readers" % titleTxt
   self.period   = 10000
  else:
   self.Title   = "  %s Live Log" % titleTxt
   self.period   = 3000
  FFJd2Z(self, self.Title, addScrollLabel=True)
  FFHhgX(self["keyRed"], "Stop")
  self["myAction"].actions["red"] = self.VVLOQD
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self["myLabel"].VVqCbn(isResizable=False)
  self["myBar"].instance.setHAlign(1)
  FFtIlI(self)
  self.VVLOQD()
 def onExit(self):
  self.timer.stop()
 def VV5tbw(self):
  try:
   self.timer_conn = self.timer.timeout.connect(self.VV7lAs)
  except:
   self.timer.callback.append(self.VV7lAs)
  self.timer.start(self.period, False)
  self.timerRunning = True
  self["keyRed"].setText("Stop")
  self["myTitle"].setText(self.Title + " (Running)")
  self["myBar"].setText("Waiting for update ...")
  FFD1yO(self, "Started", 1000)
 def VVPfXy(self):
  self.timer.stop()
  self.timerRunning = False
  try:
   self.timer.callback.remove(self.VV7lAs)
  except:
   pass
  self["keyRed"].setText("Start")
  self["myTitle"].setText(self.Title)
  self["myBar"].setText("")
  FFD1yO(self, "Stopped", 1000)
 def VVLOQD(self):
  if self.timerRunning:
   self.VVPfXy()
  else:
   self.VV5tbw()
   if self.VV0qsI == self.VVU0pj or self.VV0qsI == self.VVJP20:
    if self.VV0qsI == self.VVU0pj : urlPart = "status"
    else           : urlPart = "readerlist"
    urlStuff = CCGR8s.VVXbEU(self, self.camPrefix, self.confFile, urlPart, "")
    if urlStuff:
     self.UrlRequest, self.elementTree = urlStuff
     if self.camWebIfErrorFound:
      self.camWebIfErrorFound = False
      self["myLabel"].setText("Reading from SoftCAM Interface ...")
     FFpoMu(self.VVFM8X)
    else:
     self.close()
   else:
    self.VVAnEL()
 def VV7lAs(self):
  if self.timerRunning:
   if   self.VV0qsI == self.VVU0pj : self.VVPx1Z()
   elif self.VV0qsI == self.VVJP20 : self.VVPx1Z()
   else            : self.VVAnEL()
 def VVAnEL(self):
  if fileExists(self.VVlwNO):
   fTime = FFcgMH(os.path.getmtime(self.VVlwNO))
   if fTime != self.fileTime:
    self.fileTime = fTime
    self["myBar"].setText("Last Update : %s" % fTime)
    self["myLabel"].setText(self.VVauyZ(), VVKsoz=VVtPPw)
  else:
   self["myLabel"].setText("\n\tWaiting for %s ..." % self.VVlwNO)
 def VVFM8X(self):
  self.VVPx1Z()
 def VVPx1Z(self):
  err = ""
  try:
   page = iUrlopen(self.UrlRequest, timeout=1).read()
  except iURLError as e:
   if hasattr(e, "code") : err = "Error Code : %s\n" % str(e.code)
   if hasattr(e, "reason") : err += "Reason : %s\n" % str(e.reason)
   if not err    : err += "Error : %s"  % str(e)
  except Exception as e:
   err = str(e)
  if err:
   self["myLabel"].setText(FFkhYI("Cannot read from SoftCAM Interface !\n\nError = %s\n\nPlease activate Oscam or Ncam." % err, VVU8eD))
   self.camWebIfErrorFound = True
   self.VVPfXy()
   return
  page = page.decode("UTF-8")
  lines = page.splitlines()
  xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
  if self.VV0qsI == self.VVU0pj : tags = ("<status", "<client", "<request", "<times", "<connection", "</client", "</status")
  else           : tags = ("<readers", "<reader", "</readers")
  for line in lines:
   line = line.strip()
   if line.startswith(tags):
    xml += line
  parseError = False
  try:
   root = self.elementTree.fromstring(xml)
  except Exception as e:
   parseError = FFkhYI("Error while parsing data elements !\n\nError = %s" % str(e), VVzZva)
   self.camWebIfErrorFound = True
   self.VVPfXy()
  txt = ""
  if not parseError is False : txt = parseError
  else      : txt = self.VVzkfd(root)
  self["myLabel"].setText(txt, VVKsoz=VVtPPw)
  self["myBar"].setText("Last Update : %s" % FFDl5h())
 def VVzkfd(self, rootElement):
  def VVQQs4(key, val):
   if val : return "%s\t: %s\n" % (key, val)
   else : return ""
  txt = ""
  if self.VV0qsI == self.VVU0pj:
   for client in rootElement.findall("client"):
    name  = client.get("name")
    desc  = client.get("desc")
    protocol = client.get("protocol")
    ip   = client.find("connection").get("ip")
    port  = client.find("connection").get("port")
    status  = client.find("connection").text
    if status.upper() in ["OK", "CONNECTED"] : status = FFkhYI(status, VV9cEK)
    else          : status = FFkhYI(status, VVzZva)
    txt += VVZ1aI + "\n"
    txt += VVQQs4("Name"  , name)
    txt += VVQQs4("Description" , desc)
    txt += VVQQs4("IP/Port"  , "%s : %s" % (ip, port))
    txt += VVQQs4("Protocol" , protocol)
    txt += VVQQs4("Status"  , status)
  else:
   for client in rootElement.findall("reader"):
    label  = client.get("label")
    protocol = client.get("protocol")
    enabled  = client.get("enabled")
    if enabled == "1" : enabTxt = FFkhYI("Yes", VV9cEK)
    else    : enabTxt = FFkhYI("No", VVzZva)
    txt += VVZ1aI + "\n"
    txt += VVQQs4("Label"  , label)
    txt += VVQQs4("Protocol" , protocol)
    txt += VVQQs4("Enabled" , enabTxt)
  return txt
 def VVauyZ(self):
  lines = FFiGf6("tail -n %d %s" % (100, self.VVlwNO))
  txt   = ""
  for line in lines:
   line = line.strip()
   span = iSearch(r"^[0-9]{4}[-\/][0-9]{2}[-\/][0-9]{2}\s+", line, IGNORECASE)
   if span:
    line = "\n" + VVTdoW + line[:19] + VVkXS4 + line[19:]
    for preTxt in (" connecting to ", " from server ", " by ", "reader ", "server ", "(reader) "):
     if preTxt in line:
      if preTxt == " by " and " by WebIf" in line:
       line = line.replace("WebIf", VVYje8 + "WebIf" + VVkXS4)
      else:
       t1, t2, t3 = line.partition(preTxt)
       if t2:
        h1, h2, h3 = t3.partition(" ")
        line = t1 + t2 + VVpHwQ + h1 + h2 + VVkXS4 + h3
    span = iSearch(r"(.+:\s*)(found\s*)(\(\d+\s*ms\))(.+)", line, IGNORECASE)
    if span:
     line = "\n" + span.group(1) + VV9cEK + span.group(2) + VVoTT6 + span.group(3) + VVkXS4 + span.group(4)
    line = self.VVdvAQ(line, VVoTT6, ("(webif)", ))
    line = self.VVdvAQ(line, VVoTT6, ("(anticasc)", "(anticasc)", "(cache)", "(cccam)", "(chk)", "(client)", "(config)", "(dvbapi)", "(ecm)", "(emm)", "(emmcache)", "(emu)", "(main)", "(net)", "(newcamd)", "(reader)", "(stat)"))
    line = self.VVdvAQ(line, VV9cEK, ("OSCam", "NCam", "log switched"))
    line = self.VVdvAQ(line, VVMmz2, (": not found", "failed", "rejected group", "usr/pwd invalid", "timeout", "no matching reader", "disconnected"))
    ndx = line.find(") - ")
    if ndx > -1:
     line = line[:ndx + 3] + VVdWFT + line[ndx + 3:] + VVkXS4
   elif line.startswith("----") or ">>" in line:
    line = FFkhYI(line, VVZgqQ)
   txt += line + "\n"
  return txt
 def VVdvAQ(self, line, color, lst):
  for txt in lst:
   if txt in line:
    t1, t2, t3 = line.partition(txt)
    if t2:
     return t1 + color + t2 + VVkXS4 + t3
  return line
class CCeVbc(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 750, 1000, 50, 60, 30, "#17164965", "#17102A3F", 30)
  self.session  = session
  VV625J = []
  VV625J.append(("Backup Channels"    , "VVg6ty"   ))
  VV625J.append(("Restore Channels"    , "Restore_Channels"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Backup SoftCAM Files"   , "VVJlIy" ))
  VV625J.append(("Restore SoftCAM Files"  , "Restore_SoftCAM_Files" ))
  VV625J.append(VVm77t)
  VV625J.append(("Backup Tuner Settings"  , "Backup_TunerDiSEqC"  ))
  VV625J.append(("Restore Tuner Settings"  , "Restore_TunerDiSEqC"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Backup HotKeys Settings"  , "Backup_Hotkey_FHDG17" ))
  VV625J.append(("Restore HotKeys Settings"  , "Restore_Hotkey_FHDG17" ))
  VV625J.append(VVm77t)
  VV625J.append(("Backup Network Settings"  , "VVSmy7"   ))
  VV625J.append(("Restore Network Settings"  , "Restore_Network"   ))
  if VVPJLC:
   VV625J.append(VVm77t)
   VV625J.append((VVU8eD + "1- Fix %s Code (New Obf)"  % PLUGIN_NAME     , "VVqDVX"   ))
   VV625J.append((VV9cEK + "2- Create %s for IPK (%s)"   % (PLUGIN_NAME, VVNDdR) , "createMyIpk"   ))
   VV625J.append((VV9cEK + "3- Create %s for DEB (%s)"  % (PLUGIN_NAME, VVNDdR) , "createMyDeb"   ))
   VV625J.append((VVpHwQ + "Create %s TAR (Absolute Path)" % PLUGIN_NAME     , "createMyTar"   ))
   VV625J.append((VVpHwQ + "Decode %s Crash Report"   % PLUGIN_NAME     , "VVuRij" ))
  FFJd2Z(self, VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "VVg6ty"    : self.VVg6ty()
   elif item == "Restore_Channels"    : self.VVW4KZ("channels_backup*.tar.gz", self.VVlOQV, isChan=True)
   elif item == "VVJlIy"   : self.VVJlIy()
   elif item == "Restore_SoftCAM_Files"  : self.VVW4KZ("softcam_backup*.tar.gz", self.VV0yZ2)
   elif item == "Backup_TunerDiSEqC"   : self.VVy51f("tuner_backup", "config.Nims.")
   elif item == "Restore_TunerDiSEqC"   : self.VVW4KZ("tuner_backup*.backup", BF(self.VVue8q, "tuner"), isTuner=True)
   elif item == "Backup_Hotkey_FHDG17"   : self.VVy51f("hotkey_backup", "config.plugins.setupGlass17.\|config.misc.hotkey.\|config.misc.ButtonSetup.")
   elif item == "Restore_Hotkey_FHDG17"  : self.VVW4KZ("hotkey_*backup*.backup", BF(self.VVue8q, "misc"))
   elif item == "VVSmy7"    : self.VVSmy7()
   elif item == "Restore_Network"    : self.VVW4KZ("network_backup*.tar.gz", self.VVCdh8)
   elif item == "VVqDVX"     : FFMIbO(self, BF(FFlX3B, self, BF(CCeVbc.VVqDVX, self)), "Erase previous obf ?")
   elif item == "createMyIpk"     : self.VVpNeT(False)
   elif item == "createMyDeb"     : self.VVpNeT(True)
   elif item == "createMyTar"     : self.VVwg4x()
   elif item == "VVuRij"   : self.VVuRij()
 @staticmethod
 def VVqDVX(SELF):
  OBF_Path = VVrE9D + "OBF/"
  if fileExists(OBF_Path + "obf.py"):
   from sys import path as iPath
   iPath.append(OBF_Path)
   from imp import reload
   try:
    from .OBF import obf
   except:
    import obf
   importlib.reload(obf)
   txt, err = obf.fixCode(VVrE9D, VV73TT, VVNDdR)
   if err : FFkYsE(SELF, err)
   else : FFNEkd(SELF, txt)
  else:
   FFAVqd(SELF, OBF_Path)
 def VVpNeT(self, VVyJBC):
  OBF_Path = VVrE9D + "OBF/"
  files = iGlob("%s*main_final.py" % OBF_Path)
  if not files:
   FFkYsE(self, "Final File .py not found in:\n\n%s" % OBF_Path)
   return
  os.system("rm -f %s__pycache__/ > /dev/null 2>&1" % VVrE9D)
  os.system("mv -f %s %s" % (VVrE9D + "main.py"  , OBF_Path))
  os.system("mv -f %s %s" % (VVrE9D + "plugin.py" , OBF_Path))
  os.system("cp -f %s %s" % (OBF_Path + "*main_final.py" , VVrE9D + "plugin.py"))
  self.session.openWithCallback(self.VVmeAZ, BF(CCw9MO, path=VVrE9D, VVyJBC=VVyJBC))
 def VVmeAZ(self):
  os.system("mv -f %s %s" % (VVrE9D + "OBF/main.py"  , VVrE9D))
  os.system("mv -f %s %s" % (VVrE9D + "OBF/plugin.py" , VVrE9D))
 def VVuRij(self):
  path = "/tmp/OBF/"
  if not pathExists(path):
   FFkYsE(self, "Path not found:\n%s" % path)
   return
  files = iGlob("%s*.log" % path)
  if not files:
   FFkYsE(self, "No log files in:\n\n%s" % path)
   return
  codF, err = self.VVjd0k("%s*.list" % path)
  if err:
   FFAVqd(self, path + "*.list")
   return
  srcF, err = self.VVjd0k("%s*main_final.py" % path)
  if err:
   FFAVqd(self, path + "*.final.py")
   return
  VVvytR = []
  for f in files:
   f = os.path.basename(f)
   VVvytR.append((f, f))
  FFuRfS(self, BF(self.VVsOlm, path, codF, srcF), VV625J=VVvytR)
 def VVsOlm(self, path, codF, srcF, item=None):
  if item:
   logF = path + item
   if not fileExists(logF) : FFAVqd(self, logF)
   else     : FFlX3B(self, BF(self.VV9Gfz, logF, codF, srcF))
 def VV9Gfz(self, logF, codF, srcF):
  lst  = []
  lines = FFjdnJ(codF)
  for line in lines:
   line = line.split(":")[1]
   parts = line.split("->")
   lst.append((parts[1].strip(), parts[0].strip()))
  if not lst:
   FFkYsE(self, "No codes in : %s" % codF)
   return
  newLogF = logF.replace(".log", ".NEW.log")
  newSrcF = srcF.replace(".py" , ".DBG.py")
  totLog  = self.VVyLPa(lst, logF, newLogF)
  totSrc  = self.VVyLPa(lst, srcF, newSrcF)
  txt = "Found\t: %s\nIn\t: %s\n\nFound\t: %s\nIn\t: %s\n\nNew Files\t:\n" % (totLog, logF, totSrc, srcF)
  if not totLog and not totSrc:
   txt += "None"
  else:
   if totLog: txt += "    %s\n" % newLogF
   if totSrc: txt += "    %s\n" % newSrcF
  FFNEkd(self, txt)
 def VVjd0k(self, patt):
  tFiles = iGlob(patt)
  if not tFiles:
   return "", "*.list"
  f = tFiles[0]
  if not fileExists(f):
   return "", "Not found:\n\n"
  return f, ""
 def VVyLPa(self, lst, f1, f2):
  txt = FFqD66(f1)
  tot = 0
  for item in lst:
   if item[0] in txt:
    tot += 1
   txt = txt.replace(item[0], item[1])
  if tot > 0:
   with open(f2, "w") as f:
    f.write(txt)
  return tot
 def VVwg4x(self):
  VVvytR = []
  VVvytR.append("%s%s" % (VVrE9D, "*.py"))
  VVvytR.append("%s%s" % (VVrE9D, "*.png"))
  VVvytR.append("%s%s" % (VVrE9D, "*.xml"))
  VVvytR.append("%s"  % (VVASCC))
  FFsR4g(self, VVvytR, "%s_%s" % (PLUGIN_NAME, VV73TT), addTimeStamp=False)
 def VVg6ty(self):
  path1 = VV609C
  path2 = "/etc/tuxbox/"
  VVvytR = []
  VVvytR.append("%s%s" % (path1, "*.tv"))
  VVvytR.append("%s%s" % (path1, "*.radio"))
  VVvytR.append("%s%s" % (path1, "*list"))
  VVvytR.append("%s%s" % (path1, "lamedb*"))
  VVvytR.append("%s%s" % (path2, "*.xml"))
  FFsR4g(self, VVvytR, self.VVbd3a("channels_backup"), addTimeStamp=True)
 def VVJlIy(self):
  VVvytR = []
  VVvytR.append("/etc/tuxbox/config/")
  VVvytR.append("/usr/keys/")
  VVvytR.append("/usr/scam/")
  VVvytR.append("/etc/CCcam.cfg")
  FFsR4g(self, VVvytR, self.VVbd3a("softcam_backup"), addTimeStamp=True)
 def VVSmy7(self):
  VVvytR = []
  VVvytR.append("/etc/hostname")
  VVvytR.append("/etc/default_gw")
  VVvytR.append("/etc/resolv.conf")
  VVvytR.append("/etc/wpa_supplicant*.conf")
  VVvytR.append("/etc/network/interfaces")
  VVvytR.append("%snameserversdns.conf" % VV609C)
  FFsR4g(self, VVvytR, self.VVbd3a("network_backup"), addTimeStamp=True)
 def VVbd3a(self, fName):
  img = CCquCY.VVWIWg()
  if img: fName = "%s_%s" % (fName, img)
  return fName
 def VVlOQV(self, fileName=None):
  if fileName:
   FFMIbO(self, BF(FFlX3B, self, BF(self.VVAALG, fileName), title="Restoring ..."), "Overwrite current channels ?")
 def VVAALG(self, fileName):
  path = "%s%s" % (VVCnD5, fileName)
  if fileExists(path):
   if CC7ujK.VV6oXj(path):
    VVXBRO , VVMxmb = CCtSdI.VVQokV()
    VVsSZg, VV0E2X = CCtSdI.VVcCgD()
    cmd  = FFxtg8("cd %s" % VV609C) + ";"
    cmd += FFxtg8("rm -f *.tv *.radio *.del lamedb* whitelist blacklist satellites.xml %s %s" % (VVMxmb, VV0E2X))+ ";"
    cmd += "tar -xzf '%s' -C /" % path
    res = os.system(cmd)
    FFlB9k()
    if res == 0 : FFewCE(self, "Channels Restored.")
    else  : FFkYsE(self, "Error while restoring:\n\n%s" % fileName)
   else:
    FFkYsE(self, "Invalid tar file:\n\n%s" % path)
  else:
   FFAVqd(self, path)
 def VV0yZ2(self, fileName=None):
  if fileName:
   FFMIbO(self, BF(self.VVnl9Q, fileName), "Overwrite SoftCAM files ?")
 def VVnl9Q(self, fileName):
  fileName = "%s%s" % (VVCnD5, fileName)
  if fileExists(fileName):
   sep  = "echo -e '%s'" % VVZ1aI
   note = "You may need to restart your SoftCAM."
   FFKqND(self, "%s;tar -xzvf '%s' -C /;%s;echo -e '\nDONE\n\n%s\n' %s;%s;" % (sep, fileName, sep, note, FF95sl(note, VVdWFT), sep))
  else:
   FFAVqd(self, fileName)
 def VVCdh8(self, fileName=None):
  if fileName:
   FFMIbO(self, BF(self.VVFACv, fileName), "Overwrite Network Settings (and REBOOT) ?")
 def VVFACv(self, fileName):
  fileName = "%s%s" % (VVCnD5, fileName)
  if fileExists(fileName):
   cmd = "tar -xzvf '%s' -C /;" % fileName
   cmd += "echo ''; echo 'REBOOTING ...';"
   cmd += "sleep 3; reboot"
   FFfbee(self,  cmd)
  else:
   FFAVqd(self, fileName)
 def VVW4KZ(self, pattern, callBackFunction, isTuner=False, isChan=False):
  title = FFNUl9()
  if pathExists(VVCnD5):
   myFiles = iGlob("%s%s" % (VVCnD5, pattern))
   if len(myFiles) > 0:
    myFiles.sort(key=os.path.getmtime, reverse=True)
    VVvytR = []
    for myFile in myFiles:
     fileName = os.path.basename(myFile)
     VVvytR.append((fileName, fileName))
    if len(myFiles) > 1:
     title = title + " (Sorted by time)"
    if   isTuner  : VVmKbI = ("Sat. List", self.VV7COb)
    elif isChan and iTar: VVmKbI = ("Bouquets Importer", CCkCfQ.VVFyuq)
    else    : VVmKbI = None
    VVJ5GS = ("Delete File", self.VV91FF)
    FFuRfS(self, callBackFunction, title=title, width=1200, VV625J=VVvytR, VVmKbI=VVmKbI, VVJ5GS=VVJ5GS)
   else:
    FFkYsE(self, "No files found in:\n\n%s" % VVCnD5, title)
  else:
   FFkYsE(self, "Path not found:\n\n%s" % VVCnD5, title)
 def VV91FF(self, VVp2lZObj, path):
  FFMIbO(self, BF(self.VVZQU1, VVp2lZObj, path), "Delete this file ?\n\n%s" % path)
 def VVZQU1(self, VVp2lZObj, path):
  path = VVCnD5 + path
  FFX92w(path)
  if fileExists(path) : FFD1yO(VVp2lZObj, "Not deleted", 1000)
  else    : VVp2lZObj.VVVDex()
 def VVy51f(self, filePrefix, wordsFilter):
  settingFile = "%ssettings" % VV609C
  tCons = CChHJE()
  tCons.ePopen("if [ -f '%s' ]; then cat %s | grep '%s'; else echo '?'; fi" % (settingFile, settingFile, wordsFilter), BF(self.VVBXAz, filePrefix))
 def VVBXAz(self, filePrefix, result, retval):
  title = FFNUl9()
  if pathExists(VVCnD5):
   result = str(result).strip()
   if retval > 0 or result == "?":
    FFkYsE(self, "Cannot read settings file", title)
   else:
    fName = "%s%s%s_%s.backup" % (VVCnD5, filePrefix, self.VVbd3a(""), FFGuM2())
    try:
     VVvytR = str(result.strip()).split()
     if VVvytR:
      with open(fName, "w") as newFile:
       txt = ""
       for line in VVvytR:
        newLine = "%s\n" % line
        newFile.write(newLine)
        txt += newLine
      if fileExists(fName):
       txt += "%s\n\nDONE\n\nFile:\n%s\n\n%s" % (VVZ1aI, FFkhYI(fName, VVdWFT), VVZ1aI)
       FFNEkd(self, txt, title=title, VVKsoz=VVtPPw)
      else:
       FFkYsE(self, "File creation failed!", title)
     else:
      FFkYsE(self, "Parameters not found in settings file.", title)
    except IOError as e:
     os.system(FFxtg8("rm %s" % fName))
     FFkYsE(self, "Error [%d] : %s\n\nChange Backup Folder and try again." % (e.errno, e.strerror))
    except:
     os.system(FFxtg8("rm %s" % fName))
     FFkYsE(self, "Error while writing file.")
  else:
   FFkYsE(self, "Path not found:\n\n%s" % VVCnD5, title)
 def VVue8q(self, mode, path=None):
  if path:
   path = "%s%s" % (VVCnD5, path)
   if fileExists(path):
    lines = FFjdnJ(path, keepends=True)
    if lines:
     if mode == "tuner" : txt = "tuner"
     else    : txt = "Hotkeys"
     FFMIbO(self, BF(self.VV8GX8, path, mode, lines), "Overwrite %s settings (and restart) ?" % txt)
    else:
     FFzfYN(self, path, title=FFNUl9())
   else:
    FFAVqd(self, path)
 def VV8GX8(self, path, mode, lines):
  grepFilter = ""
  if mode == "tuner":
   grepFilter = ".Nims."
   newList = []
   for line in lines:
    newList.append(line)
    if ".dvbs." in line:
     newList.append(line.replace(".dvbs.", "."))
    else:
     parts = line.split(".")
     if len(parts) > 3:
      tunerNum = ".%s." % parts[2]
      newList.append(line.replace(tunerNum, "%sdvbs." % tunerNum))
  elif mode == "misc":
   grepFilter = ".setupGlass17.\|.hotkey.\|.ButtonSetup."
   newList = []
   for line in lines:
    newList.append(line)
    if   ".hotkey."   in line : newList.append(line.replace(".hotkey.", ".ButtonSetup."))
    elif ".ButtonSetup." in line : newList.append(line.replace(".ButtonSetup.", ".hotkey."))
  newList = list(set(newList))
  newList.sort()
  VV6D3C = []
  VV6D3C.append("echo -e 'Reading current settings ...'")
  VV6D3C.append("cat /etc/enigma2/settings | grep -v '" + grepFilter + "' > /tmp/settings_my_tmp.txt")
  settingsLines = "echo -e '"
  for line in newList:
   settingsLines += line
  settingsLines += "' >> /tmp/settings_my_tmp.txt"
  VV6D3C.append("echo -e 'Preparing new settings ...'")
  VV6D3C.append(settingsLines)
  VV6D3C.append("echo -e 'Applying new settings ...'")
  VV6D3C.append("mv /tmp/settings_my_tmp.txt /etc/enigma2/settings")
  FFRi75(self, VV6D3C)
 def VV7COb(self, VVp2lZObj, path):
  if not path:
   return
  path = VVCnD5 + path
  if not fileExists(path):
   FFAVqd(self, path)
   return
  txt = FFqD66(path)
  satList = []
  lst = iFindall(r".+[.](diseqc.?)[=](\d+)", txt, IGNORECASE)
  for sat in lst:
   diseqc = sat[0].upper()
   satNum = sat[1]
   satList.append((diseqc.replace("DISEQC", "DiSEqC-"), satNum))
  lst = iFindall(r".+[.]sat[.](\d+)[.](lnb[=].+)", txt, IGNORECASE)
  for sat in lst:
   satNum = sat[0]
   lnb  = sat[1].upper()
   satList.append((lnb.replace("LNB=", "LNB-"), satNum))
  if satList:
   satList = list(set(satList))
   satList.sort(key=lambda x: x[0])
   sep   = ""
   VVvytR  = []
   for item in satList:
    VVvytR.append("%s\t%s" % (item[0], FFkxbC(item[1])))
   FFNEkd(self, VVvytR, title="  Satellites List")
  else:
   FFkYsE(self, "Incorrect Tuner Backup file !\n\n(or missing info.)", title="  Satellites List")
class CCkCfQ():
 def __init__(self, SELF):
  self.SELF   = SELF
  self.Title   = "Bouquets Importer"
  self.fileName  = ""
  self.filePath  = ""
  self.instance  = None
  self.isZip   = False
 @staticmethod
 def VVFyuq(SELF, fName):
  bi = CCkCfQ(SELF)
  bi.instance = bi
  bi.VVx5jX(SELF, fName)
 @staticmethod
 def VV1ECt(SELF):
  bi = CCkCfQ(SELF)
  bi.instance = bi
  bi.VVKrPc()
 def VVx5jX(self, waitObg, fName):
  self.fileName = fName
  self.filePath = VVCnD5 + fName
  self.isZip   = fName.endswith(".zip")
  if fileExists(self.filePath): FFlX3B(waitObg, self.VV0VSr, title="Reading bouquets ...")
  else      : self.VVlyvg(self.filePath)
 def VV6I1g(self, txt) : FFkYsE(self.SELF, txt, title=self.Title)
 def VVl2X5(self, txt)  : FFD1yO(self, txt, 1500)
 def VVlyvg(self, path) : FFAVqd(self.SELF, path, title=self.Title)
 def VVKrPc(self):
  if pathExists(VVCnD5):
   lst = iGlob("%schannels_backup*.tar.gz" % VVCnD5)
   if iZip: lst.extend(self.VVWi8T())
   if len(lst) > 0:
    VV625J = []
    for item in lst:
     item = os.path.basename(item)
     txt = FFkhYI(item, VVoTT6) if item.endswith(".zip") else item
     VV625J.append((txt, item))
    VV625J.sort(key=lambda x: x[1].lower())
    OKBtnFnc = self.VVocj2
    FFuRfS(self.SELF, self.VVIYuC, title=self.Title, width=1200, VV625J=VV625J, OKBtnFnc=OKBtnFnc, VVz2kc="#22111111", VVwpZm="#22111111")
   else:
    self.VV6I1g("No valid backup files found in:\n\n%s" % VVCnD5)
  else:
   self.VV6I1g("Backup Directory not found:\n\n%s" % VVCnD5)
 def VVocj2(self, item=None):
  if item:
   menuInstance, txt, fName, ndx = item
   self.VVx5jX(menuInstance, fName)
 def VVIYuC(self, item=None):
  if not item and self.instance:
   del self.instance
 def VVWi8T(self):
  files = iGlob("%s*.zip" % VVCnD5)
  lst = []
  for path in files:
   bakFile = os.path.basename(path)
   with iZip.ZipFile(path) as zipF:
    dbFound = bFound = False
    for zipInfo in zipF.infolist():
     fName = os.path.basename(zipInfo.filename)
     if fName == "lamedb" : dbFound = True
     if fName.endswith(".tv"): bFound = True
     if dbFound and bFound:
      lst.append(bakFile)
      break
  return lst
 def VV0VSr(self):
  lines, err = CCkCfQ.VVo3Lj(self.filePath, "bouquets.tv")
  if err:
   self.VV6I1g(err)
   return
  bTvSortLst  = self.VVnwcW(lines)
  lines, err = CCkCfQ.VVo3Lj(self.filePath, "bouquets.radio")
  if err:
   self.VV6I1g(err)
   return
  bRadSortLst = self.VVnwcW(lines)
  VVvhuK = []
  subBouquets = {}
  if self.filePath.endswith(".zip"):
   with iZip.ZipFile(self.filePath) as zipF:
    for zipInfo in zipF.infolist():
     fName = os.path.basename(zipInfo.filename)
     span = iSearch(r"userbouquet\..+\.(tv|radio)$", fName, IGNORECASE)
     if span:
      mode = span.group(1)
      with zipF.open(zipInfo.filename) as f:
       row, bnbLst, err = self.VV3OXC(f, mode, len(VVvhuK), zipInfo.filename, False)
       if err:
        return
       tName = os.path.basename(row[9])
       if   tName in bTvSortLst : row[0] = str(bTvSortLst.index(tName))
       elif tName in bRadSortLst: row[0] = str(1000000 + bRadSortLst.index(tName))
       VVvhuK.append(row)
       parent = zipInfo.filename
       lst = []
       for fPath in bnbLst:
        for zipInfo in zipF.infolist():
         fName = os.path.basename(zipInfo.filename)
         if fName == fPath:
          with zipF.open(zipInfo.filename) as f:
           row, bnbLst, err = self.VV3OXC(f, mode, len(VVvhuK), zipInfo.filename, True)
           if err:
            return
           lst.append(row)
       if lst:
        subBouquets[tName] = lst
  else:
   with iTar.open(self.filePath) as tar:
    for mem in tar.getmembers():
     fName = os.path.basename(mem.name)
     span = iSearch(r"userbouquet\..+\.(tv|radio)$", fName, IGNORECASE)
     if span:
      mode = span.group(1)
      f = tar.extractfile(mem)
      row, bnbLst, err = self.VV3OXC(f, mode, len(VVvhuK), mem.name, False)
      if err:
       return
      tName = os.path.basename(row[9])
      if   tName in bTvSortLst : row[0] = str(bTvSortLst.index(tName))
      elif tName in bRadSortLst: row[0] = str(1000000 + bRadSortLst.index(tName))
      VVvhuK.append(row)
      parent = mem.name
      lst = []
      for fPath in bnbLst:
       for mem in tar.getmembers():
        fName = os.path.basename(mem.name)
        if fName == fPath:
         f = tar.extractfile(mem.name)
         row, bnbLst, err = self.VV3OXC(f, mode, len(VVvhuK), mem.name, True)
         if err:
          return
         lst.append(row)
      if lst:
       subBouquets[tName] = lst
  if VVvhuK:
   VVvhuK.sort(key=lambda x: int(x[0]))
   for ndx, item in enumerate(VVvhuK): VVvhuK[ndx][0] = str(ndx + 1)
   for key, lst in list(subBouquets.items()):
    for ndx, row in enumerate(VVvhuK):
     if key == os.path.basename(row[9]):
      VVvhuK = VVvhuK[:ndx+1] + lst + VVvhuK[ndx+1:]
      break
   for ndx, item in enumerate(VVvhuK): VVvhuK[ndx][0] = str(ndx + 1)
   VVghPi = "#11000600"
   VVVHmY  = ("Show Services" , self.VVO1rF  , [], "Reading ..." )
   VVOtSO = ("Options"  , self.VVQevg, []    )
   header   = ("Num" , "Bouquet Name", "Mode", "Items" , "DVB" , "IPTV", "Local" , "Marker" , "Bouquet" , "File")
   widths   = (7  , 43   , 7  , 7   , 7  , 7  , 7   , 7   , 8   ,  0.01 )
   VVQqg2  = (CENTER , LEFT   , CENTER, CENTER , CENTER, CENTER, CENTER , CENTER , CENTER ,  LEFT )
   FF1dQ4(self.SELF, None, title=self.Title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=24, VVVHmY=VVVHmY, VVOtSO=VVOtSO, searchCol=1, lastFindConfigObj=CFG.lastFindServers
     , VVz2kc=VVghPi, VVwpZm=VVghPi, VVghPi=VVghPi, VVAfLs="#11ffffff", VV0g1U="#00004455", VVooYw="#0a282828")
  else:
   self.VV6I1g("No valid bouquets in:\n\n%s" % self.filePath)
 def VVnwcW(self, lines):
  lst = []
  for line in lines:
   span = iSearch(r".+(userbouquet\..+\.(tv|radio))", line, IGNORECASE)
   if span:
    lst.append(span.group(1))
  return lst
 def VVQevg(self, VVcpnp, title, txt, colList):
  mSel = CCqgU8(self.SELF, VVcpnp)
  if VVcpnp.VVbl0M:
   totSel = VVcpnp.VVMJsS()
   if totSel: VV625J = [("Import %s Bouquet%s" % (FFkhYI(str(totSel), VV9cEK), FFICXm(totSel)), "imp")]
   else  : VV625J = [("Import Bouquet (nothing selected)", )]
  else:
   bName = colList[1]
   if len(bName) > 40: bName = bName[:40] + " .."
   bName = FFkhYI(bName, VV9cEK)
   VV625J = [("Import Selected Bouquet : %s" % bName, "imp")]
  cbFncDict = {"imp": BF(FFlX3B, VVcpnp, BF(CCkCfQ.VVJZnQ, self.SELF, VVcpnp, self.filePath))}
  mSel.VVMNiz(VV625J, cbFncDict)
 def VVO1rF(self, VVcpnp, title, txt, colList):
  err = ""
  if fileExists(self.filePath):
   lines, err = CCkCfQ.VVo3Lj(self.filePath, "lamedb")
   if err:
    self.VV6I1g(err)
    return
   dbServLst = CCtSdI.VVkHb1(lines, mode=10)
   num, bName, bMode, totItem, totDVB, totIptv, totLoc, totMrk, totBnb, fName = VVcpnp.VVPxSj()
   lines, err = CCkCfQ.VVo3Lj(self.filePath, os.path.basename(fName))
   if err:
    self.VV6I1g(err)
    return
   VVvhuK = []
   bnbFound = False
   for line in lines:
    if line.startswith("#SERVICE "):
     span = iSearch(r"1:64:(?:[A-Fa-f0-9]+:){8}:(.+)", line, IGNORECASE)
     if span:
      VVvhuK.append((span.group(1).strip(), "Marker"))
     else:
      span = iSearch(r'.+1:7:.+FROM BOUQUET\s+"(.+)"', line, IGNORECASE)
      if span:
       VVvhuK.append((span.group(1) or "-", "Sub-Bouquet"))
       bnbFound = True
      else:
       span = iSearch(r"(?:[A-Fa-f0-9]+:){10}http.+:(.+)", line)
       if span:
        VVvhuK.append((span.group(1).strip() or "-", "IPTV"))
       else:
        span = iSearch(r"(?:[A-Fa-f0-9]+:){10}(\/.+)", line)
        if span:
         VVvhuK.append((os.path.basename(span.group(1).strip() or "-"), "Local Media"))
        else:
         span = iSearch(r'.+1:7:.+FROM BOUQUET\s+"(.+)"', line, IGNORECASE)
         if span:
          VVvhuK.append((span.group(1) or "-", "Sub-Bouquet"))
          bnbFound = True
         else:
          span = iSearch(r"((?:[A-Fa-f0-9]+:){10})(?:$|:.+)", line)
          if span:
           dbCode = CCtSdI.VVVxzN(span.group(1))
           for dbCode1, name, prov in dbServLst:
            if dbCode1.upper() in dbCode:
             VVvhuK.append((name.strip() or "-", FF24qC(span.group(1), False)))
             break
   if bnbFound:
    for ndx, item in enumerate(VVvhuK):
     name, descr = item
     if iMatch(r".+\..+\.tv", name, IGNORECASE):
      lines, err = CCkCfQ.VVo3Lj(self.filePath, os.path.basename(name))
      if lines and not err:
       span = iSearch(r"#NAME\s+(.+)", lines[0], IGNORECASE)
       if span:
        bName = span.group(1).strip()
        if bName:
         VVvhuK[ndx] = (bName, descr)
   if VVvhuK:
    VVghPi = "#11001122"
    bName = iSub(r"\s{4,}" ," .. " , bName)
    header  = ("Service", "Type")
    widths  = (80  , 20 )
    VVQqg2 = (LEFT  , CENTER)
    FF1dQ4(self.SELF, None, title="Services in : %s" % bName, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VVz2kc=VVghPi, VVwpZm=VVghPi, VVghPi=VVghPi, lastFindConfigObj=CFG.lastFindServers)
   else:
    err = "No valid services !"
  else:
   err = "Cannot open file !"
  if err : FFD1yO(VVcpnp, err, 1500)
  else : VVcpnp.VVhzNf()
 def VV3OXC(self, f, mode, sequence, fPath, isSubB):
  bName = ""
  totItem = totDVB = totMrk = totBnb = totIptv = totLoc = 0
  bnbLst = []
  for line in f:
   try:
    line = str(line.decode()).strip()
   except:
    self.VV6I1g("Encoding Error in the archived file:\n\n%s" % fPath)
    return [], [], "File Encoding Error"
   if line.startswith("#SERVICE "):
    totItem +=1
    if   iMatch(r".+1:64:(?:[A-Fa-f0-9]+:){8}:.+", line)      : totMrk += 1
    elif iMatch(r".+1:7:(?:[A-Fa-f0-9]+:){8}FROM BOUQUET.+", line, IGNORECASE) :
     totBnb += 1
     span = iSearch(r'.+1:7:(?:[A-Fa-f0-9]+:){8}FROM BOUQUET\s+"(.+)".+', line)
     if span:
      bnbLst.append(span.group(1))
    elif iMatch(r".+(?:[A-Fa-f0-9]+:){10}http.+:.+", line, IGNORECASE)   : totIptv += 1
    elif iMatch(r".+(?:[A-Fa-f0-9]+:){10}\/.+", line)       : totLoc += 1
    elif iMatch(r".+(?:[A-Fa-f0-9]+:){10}(?:$|:.+)", line)      : totDVB += 1
   elif line.startswith("#NAME "):
    bName = line[6:]
  def VVD6fO(var):
   return str(var) if var else VVjrAG + str(var)
  totItem = VVdWFT + str(totItem)
  bMode = "TV" if mode == "tv" else "Radio"
  if   totBnb : bColor, totBnb  = VVU8eD   , str(totBnb)
  elif isSubB : bColor, totBnb  = VVoTT6, "Sub-B."
  else  : bColor, totBnb = ""      , VVD6fO(totBnb)
  row = [str(2000001 + sequence), bColor + bName, bMode, totItem, VVD6fO(totDVB), VVD6fO(totIptv), VVD6fO(totLoc), VVD6fO(totMrk), totBnb, fPath]
  return row, bnbLst, ""
 @staticmethod
 def VVJZnQ(SELF, VVcpnp, archPath):
  title = "Import Bouquets"
  tvBouquetFile = VV609C + "bouquets.tv"
  radBouquetFile = VV609C + "bouquets.radio"
  if not fileExists(tvBouquetFile):
   FFAVqd(SELF, tvBouquetFile, title=title)
   return
  elif not fileExists(radBouquetFile):
   FFAVqd(SELF, radBouquetFile, title=title)
   return
  isMulti = VVcpnp.VVbl0M
  if isMulti : rows = VVcpnp.VVN5aQ()
  else  : rows = [VVcpnp.VVPxSj()]
  for num, bName, bMode, totItem, totDVB, totIptv, totLoc, totMrk, totBnb, fName in rows:
   if totBnb.isdigit():
    FFkYsE(SELF, "Cannot import Sub-Bouquets from:\n\n%s" % FFO8d5(bName), title=title)
    return
  bList = []
  totAllServ = 0
  if fileExists(archPath):
   for num, bName, bMode, totItem, totDVB, totIptv, totLoc, totMrk, totBnb, fName in rows:
    totAllServ += int(FFO8d5(totItem))
    newFile = os.path.basename(fName)
    span = iSearch(r".+\.(.+)\.(tv|radio)", newFile, IGNORECASE)
    if span : fNamePart, fNameExt = span.group(1), span.group(2)
    else : fNamePart, fNameExt = "bouquet", "tv"
    newFile = "userbouquet.%s.%s" % (fNamePart, fNameExt)
    bPath = VV609C + newFile
    num  = 0
    while fileExists(bPath):
     num += 1
     newFile = "userbouquet.%s_%d.%s" % (fNamePart, num, fNameExt)
     bPath = VV609C + newFile
    CCkCfQ.VVZxQm(archPath, fName, VV609C, newFile)
    if fileExists(bPath):
     bList.append(newFile)
  totTP = totServ = totTv = totRad = totMissTP = totMissServ = 0
  if bList:
   CCgKdM.VV0WD2(tvBouquetFile)
   CCgKdM.VV0WD2(radBouquetFile)
   for bFile in bList:
    if bFile.endswith("tv") : mainBFile, totTv = tvBouquetFile , totTv  + 1
    else     : mainBFile, totRad = radBouquetFile, totRad + 1
    with open(mainBFile, "a") as f:
     f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\n' % bFile)
   totTP, totServ, totMissTP, totMissServ = CCkCfQ.VVJ1ZN(SELF, archPath, bList)
   FFlB9k()
  txt  = FFkhYI("Added:\n", VVoTT6)
  txt += "Bouquets\t: %d     (%d TV , %d Radio)\n" % (len(bList), totTv, totRad)
  txt += "Services\t: %d\n" % totAllServ
  if totTP or totServ:
   txt += "\n"
   txt += FFkhYI("Imported to lamedab:\n", VVoTT6)
   if totTP : txt += "Transponders\t: %d\n" % totTP
   if totServ : txt += "Services\t: %d\n"  % totServ
  if totMissTP or totMissServ:
   txt += "\n"
   txt += FFkhYI("Missing from archived lamedb:\n", VVU8eD)
   if totMissTP : txt += "Transponders\t: %d\n" % totMissTP
   if totMissServ : txt += "Services\t: %d"  % totMissServ
  FFNEkd(SELF, txt, title=title, width=1000)
 @staticmethod
 def VVJ1ZN(SELF, archPath, bList):
  VVXBRO, err = CCtSdI.VVR3Wk(SELF, VVDUH8=False)
  if err:
   return 0, 0, 0, 0
  dbServIDs = CCtSdI.VVPqAI(VVXBRO, mode=11)
  if not dbServIDs:
   return 0, 0, 0, 0
  newDbTpIDs  = []
  newDbServIDs = []
  for bFile in bList:
   lines = FFjdnJ(VV609C + bFile)
   for line in lines:
    span = iSearch(r"((?:[A-Fa-f0-9]+:){10}$)", line, IGNORECASE)
    if span:
     refCode = span.group(1)
     dbCode = CCtSdI.VVVxzN(refCode)
     if not dbCode in dbServIDs:
      newDbServIDs.append(dbCode)
      tpID = CCtSdI.VVlSbc(refCode)
      if not tpID in newDbTpIDs:
       newDbTpIDs.append(tpID)
  dbServIDs = None
  tFile = ""
  if newDbServIDs and fileExists(archPath):
   dbName = "lamedb"
   tFile = "/tmp/%s.tmp" % dbName
   fName = CCkCfQ.VVpHPb(archPath, dbName)
   CCkCfQ.VVZxQm(archPath, fName, "/tmp/", dbName + ".tmp")
  newTPLines = []
  if newDbTpIDs:
   for item in CCtSdI.VVPqAI(tFile, mode=0):
    if item[0].upper() in newDbTpIDs:
     newTPLines.append(item)
  newServLines = []
  for item in CCtSdI.VVPqAI(tFile, mode=10):
   if item[0].upper() in newDbServIDs:
    newServLines.append(item)
  dbCodeLst = CCtSdI.VVPqAI(tFile, mode=1)
  totMissTP = 0
  for dbCode in newDbTpIDs:
   if not dbCode in dbCodeLst:
    totMissTP += 1
  dbCodeLst = CCtSdI.VVPqAI(tFile, mode=11)
  totMissServ = 0
  for dbCode in newDbServIDs:
   if not dbCode in dbCodeLst:
    totMissServ += 1
  FFX92w(tFile)
  totServ = totTP = 0
  if newDbTpIDs or newServLines:
   isServ = isTP = False
   tmpDbFile = VVXBRO + ".tmp"
   lines   = FFjdnJ(VVXBRO)
   with open(tmpDbFile, "w") as f:
    for line in lines:
     sLine = line.strip()
     if   sLine == "transponders": isTP, isServ = True, False
     elif sLine == "services" : isTP, isServ = False, True
     elif sLine == "end":
      if isTP:
       for item in (newTPLines):
        totTP += 1
        for L in item:
         f.write(L + "\n")
      elif isServ:
       for item in (newServLines):
        totServ += 1
        for L in item:
         f.write(L + "\n")
     f.write(line + "\n")
   os.system(FFxtg8("mv -f '%s' '%s'" % (tmpDbFile, VVXBRO)))
  return totTP, totServ, totMissTP, totMissServ
 @staticmethod
 def VVlQlT(path):
  lst = []
  if path.endswith(".zip"):
   with iZip.ZipFile(path) as zipF:
    for zipInfo in zipF.infolist():
     lst.append(os.path.basename(zipInfo.filename), zipInfo.filename)
  else:
   with iTar.open(path) as tar:
    for mem in tar.getmembers():
     lst.append(os.path.basename(mem.name), mem.name)
  return lst
 @staticmethod
 def VVpHPb(path, baseName):
  if path.endswith(".zip"):
   with iZip.ZipFile(path) as zipF:
    for zipInfo in zipF.infolist():
     if os.path.basename(zipInfo.filename) == baseName:
      return zipInfo.filename
  else:
   with iTar.open(path) as tar:
    for mem in tar.getmembers():
     if os.path.basename(mem.name) == baseName:
      return mem.name
  return ""
 @staticmethod
 def VVZxQm(path, fName, newPath, newFile):
  if path.endswith(".zip"):
   with iZip.ZipFile(path) as zipF:
    zipInfo = zipF.getinfo(fName)
    zipInfo.filename = newFile
    zipF.extract(zipInfo, newPath)
  else:
   with iTar.open(path) as tar:
    mem = tar.getmember(fName)
    mem.name = newFile
    tar.extract(mem, path=newPath)
 @staticmethod
 def VVo3Lj(path, subFile):
  lines = []
  try:
   if path.endswith(".zip"):
    with iZip.ZipFile(path) as zipF:
     for zipInfo in zipF.infolist():
      fName = os.path.basename(zipInfo.filename)
      if fName == subFile:
       with zipF.open(zipInfo.filename) as f:
        lines = f.read().decode().splitlines()
       break
     else:
      return [], "Archived file not found:\n\n%s" % subFile
   else:
    with iTar.open(path) as tar:
     for mem in tar.getmembers():
      fName = os.path.basename(mem.name)
      if fName == subFile:
       f = tar.extractfile(mem)
       lines = f.read().decode().splitlines()
       break
     else:
      return [], "Archived file not found:\n\n%s" % subFile
   return [str(x.strip()) for x in lines], ""
  except:
   return [], "Error while reading the archived file:\n\n%s" % subFile
class CCBWXm(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVoxS0, 850, 800, 50, 40, 30, "#221a001a", "#22110011", 30)
  self.session   = session
  self.lastSelectedRow = -1
  VV625J = []
  VV625J.append(("Plugins Browser List"       , "VVswem"   ))
  VV625J.append(("Plugins Additional Menus"      , "pluginsMenus"    ))
  VV625J.append(("Startup Plugins"        , "pluginsStartup"    ))
  VV625J.append(VVm77t)
  VV625J.append(("Extensions and System Plugins"    , "pluginsDirList"    ))
  VV625J.append(VVm77t)
  VV625J.append(("Download/Install Packages"     , "downloadInstallPackages"  ))
  VV625J.append(("Remove Packages (show all)"     , "VVQdQ3sAll"   ))
  VV625J.append(("Remove Packages (Plugins/SoftCAMs/Skins)"  , "removePluginSkinSoftCAM"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Update List of Available Packages"   , "VV71V6"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Packaging Tool"        , "VVoDWU"    ))
  VV625J.append(("Packages Feeds"        , "packagesFeeds"    ))
  FFJd2Z(self, VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "VVswem"   : self.VVswem()
   elif item == "pluginsMenus"     : self.VVwBjJ(0)
   elif item == "pluginsStartup"    : self.VVwBjJ(1)
   elif item == "pluginsDirList"    : self.VV1EDf()
   elif item == "downloadInstallPackages"  : FFlX3B(self, BF(self.VVs3jj, 0, ""))
   elif item == "VVQdQ3sAll"   : FFlX3B(self, BF(self.VVs3jj, 1, ""))
   elif item == "removePluginSkinSoftCAM"    : FFlX3B(self, BF(self.VVs3jj, 2, "| grep -e skin -e enigma2-"))
   elif item == "VV71V6"   : self.VV71V6()
   elif item == "VVoDWU"    : self.VVoDWU()
   elif item == "packagesFeeds"    : self.VV6EcT()
   else          : self.close()
 def VV1EDf(self):
  extDirs  = FFzDB4(VV9VaA)
  sysDirs  = FFzDB4(VVuVce)
  VVvytR  = []
  for item in extDirs:
   if not "__pycache__" in item:
    VVvytR.append((item, VV9VaA + item))
  for item in sysDirs:
   if not "__pycache__" in item:
    VVvytR.append((item, VVuVce + item))
  if VVvytR:
   VVvytR.sort(key=lambda x: x[0].lower())
   VVOtSO = ("Package Info.", self.VVJHu2, [])
   VV1QO7 = ("Open in File Manager", BF(self.VV5l3b, 1), [])
   header   = ("Plugin" ,"Path" )
   widths   = (25  , 75 )
   FF1dQ4(self, None, header=header, VVvytR=VVvytR, VVoJsQ=widths, VVmp7B=28, VVOtSO=VVOtSO, VV1QO7=VV1QO7)
  else:
   FFkYsE(self, "Nothing found!")
 def VVJHu2(self, VVcpnp, title, txt, colList):
  name = colList[0]
  path = colList[1]
  loc = ""
  if   path.startswith(VV9VaA) : loc = "extensions"
  elif path.startswith(VVuVce) : loc = "systemplugins"
  if loc:
   package = "enigma2-plugin-%s-%s" % (loc, name.lower())
   self.VVsDCo(package)
  else:
   FFkYsE(self, "No info!")
 def VV6EcT(self):
  pkg = FFC2Pr()
  if pkg : FFuCjo(self, "ls -1 /var/lib/%s/lists" % pkg)
  else : FFHRK6(self)
 def VVswem(self):
  pluginList = iPlugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
  def VVQQs4(key, val):
   return key + "\t: " + str(val) + "\n"
  txt = ""
  c = 1
  for p in pluginList:
   try:
    txt += VVZ1aI + "\n"
    txt += VVQQs4("Number"   , str(c))
    txt += VVQQs4("Name"   , FFkhYI(str(p.name), VVdWFT))
    txt += VVQQs4("Path"  , p.path  )
    txt += VVQQs4("Description" , p.description )
    txt += VVQQs4("Icon"  , p.iconstr  )
    txt += VVQQs4("Wakeup Fnc" , p.wakeupfnc )
    txt += VVQQs4("NeedsRestart", p.needsRestart)
    txt += VVQQs4("Internal" , p.internal )
    txt += VVQQs4("Weight"  , p.weight  ) + "\n"
    c += 1
   except:
    pass
  if not txt:
   txt = "Could not find any plugin."
  FFNEkd(self, txt)
 def VVwBjJ(self, typ):
  if typ == 0:
   title = "Plugins Menu Items"
   tit2  = "Menu Item"
   tDict = { PluginDescriptor.WHERE_PLUGINMENU: "Plugins Browser"
     , PluginDescriptor.WHERE_EXTENSIONSMENU: "Extensions Menu"
     , PluginDescriptor.WHERE_MAINMENU: "Main Menu"
     , PluginDescriptor.WHERE_MENU: "Menu"
     , PluginDescriptor.WHERE_EVENTINFO: "Events Info Menu"
     , PluginDescriptor.WHERE_MOVIELIST: "Movie List"
     , PluginDescriptor.WHERE_NETWORKSETUP: "Network Setup"
     , PluginDescriptor.WHERE_SOFTWAREMANAGER: "WHERE_SOFTWAREMANAGER"
     , PluginDescriptor.WHERE_AUDIOMENU: "Audio Menu"
     , PluginDescriptor.WHERE_CHANNEL_CONTEXT_MENU : "Channel Context Menu"
     }
  else:
   title = "Startup Plugins"
   tit2  = "Starts as"
   tDict = { PluginDescriptor.WHERE_AUTOSTART: "Auto-Start" , PluginDescriptor.WHERE_SESSIONSTART: "Start" }
  VVvytR = []
  for key, val in list(tDict.items()):
   pluginList = iPlugins.getPlugins(key)
   for p in pluginList:
    try:
     VVvytR.append((p.path.split("/")[-1], str(p.name), val, p.description, p.path))
    except:
     pass
  if VVvytR:
   VVvytR.sort(key=lambda x: x[0].lower())
   VV1QO7 = ("Open in File Manager", BF(self.VV5l3b, 4), [])
   header   = ("Plugin" , tit2 , "Where" , "Description" , "Path")
   widths   = (19  , 25 , 20  , 27   , 9  )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvytR, VVoJsQ=widths, VVmp7B=26, VV1QO7=VV1QO7)
  else:
   FFkYsE(self, "Nothing Found", title=title)
 def VV5l3b(self, pathColNum, VVcpnp, title, txt, colList):
  path = colList[pathColNum].strip()
  if pathExists(path) : self.session.open(CC7ujK, mode=CC7ujK.VVHuGg, VVKDYx=path)
  else    : FFD1yO(VVcpnp, "Path not found !", 1500)
 def VV71V6(self):
  cmd = FFaG6T(VVRq5s, "")
  if cmd : FFfbee(self, cmd, checkNetAccess=True)
  else : FFHRK6(self)
 def VVoDWU(self):
  pkg = FFC2Pr()
  if   pkg == "ipkg" : txt = "OE2.0 - IPKG"
  elif pkg == "opkg" : txt = "OE2.0 - OPKG"
  elif pkg == "dpkg" : txt = "OE2.5/2.6 - APT-DPKG"
  else    : txt = "No packaging tools found!"
  FFewCE(self, txt)
 def VVs3jj(self, mode, grep, VVcpnp=None, title=""):
  if   mode == 0: cmd = FFaG6T(VVmDYa    , grep)
  elif mode == 1: cmd = FFaG6T(VVPeIJ , grep)
  elif mode == 2: cmd = FFaG6T(VVPeIJ , grep)
  if not cmd:
   FFHRK6(self)
   return
  VVvhuK = FFiGf6(cmd)
  if not VVvhuK:
   if VVcpnp: VVcpnp.VVhzNf()
   FFkYsE(self, "No packages found!")
   return
  elif len(VVvhuK) == 1 and VVvhuK[0] == VVCYwM:
   FFkYsE(self, VVCYwM)
   return
  wordsToSkip = ("base", "conf", "config", "configs", "common", "common3", "core", "bin", "feed", "enigma", "mount", "opkg", "samba4", "utils")
  PLUGIN  = "enigma2-plugin-"
  VVvytR  = []
  for item in VVvhuK:
   parts = item.split(" - ")
   if len(parts) > 1:
    package = parts[0]
    version = parts[1]
    parts  = package.split("-")
    totItems = len(parts)
    if "feed" in package:
     name ="feed"
    elif totItems > 3:
     if package.startswith(PLUGIN):
      if totItems > 4 and parts[4][:1].isdigit() : name = parts[3]
      elif totItems > 3       : name = "-".join(parts[3:])
      else          : name = package
     else:
      for item in reversed(parts):
       if len(item) > 3 and item.isalpha():
        if not "." in item and not item.isdigit() and not item in (wordsToSkip):
         name = item
         break
      else:
       name = parts[0]
    else:
     name = package
    VVvytR.append((name, package, version))
  if mode > 0:
   extensions = FFiGf6("ls %s -l | grep '^d' | awk '{print($9)}'" % VV9VaA)
   for item in extensions:
    if not "__pycache__" in item:
     for row in VVvytR:
      if item.lower() == row[0].lower():
       break
     else:
      name = item
      if name == "AJPan": name += "el"
      VVvytR.append((name, VV9VaA + item, "-"))
   systemPlugins = FFiGf6("ls %s -l | grep '^d' | awk '{print($9)}'" % VVuVce)
   for item in systemPlugins:
    if not "__pycache__" in item:
     for row in VVvytR:
      if item.lower() == row[0].lower():
       break
     else:
      VVvytR.append((item, VVuVce + item, "-"))
  if not VVvytR:
   FFkYsE(self, "No packages found!")
   return
  if VVcpnp:
   VVvytR.sort(key=lambda x: x[0].lower())
   VVcpnp.VVuVux(VVvytR, title)
  else:
   widths = (20, 50, 30)
   VV3th8 = None
   VV1QO7 = None
   if mode == 0:
    VVMQj9 = ("Install" , self.VVSf33   , [])
    VV3th8 = ("Download" , self.VVTC5l   , [])
    VV1QO7 = ("Filter"  , self.VV8mog , [])
   elif mode == 1:
    VVMQj9 = ("Uninstall", self.VVQdQ3, [])
   elif mode == 2:
    VVMQj9 = ("Uninstall", self.VVQdQ3, [])
    widths= (18, 57, 25)
   VVvytR.sort(key=lambda x: x[0].lower())
   VVOtSO = ("Package Info.", self.VVYCYj, [])
   header   = ("Name" ,"Package" , "Version" )
   FF1dQ4(self, None, header=header, VVvytR=VVvytR, VVoJsQ=widths, VVmp7B=28, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VV8dGa=self.lastSelectedRow, lastFindConfigObj=CFG.lastFindPackages
     , VVz2kc="#22110011", VVwpZm="#22191111", VVghPi="#22191111", VV0g1U="#00003030", VVooYw="#00333333")
 def VVYCYj(self, VVcpnp, title, txt, colList):
  package = colList[1]
  self.VVsDCo(package)
 def VV8mog(self, VVcpnp, title, txt, colList):
  words  = ("Alsa", "Dream", "Drivers", "Enigma", "Extensions", "Feeds", "Firmware", "GLibc", "GStreamer", "Kernel", "Lib", "Linux", "Locale", "Network", "Octagon", "PIcons", "Perl", "Pkg", "Plugin", "Python", "Samba", "Settings", "Skin", "SoftCam", "SystemPlugins", "Tools", "Util", "Zip")
  VV625J = []
  VV625J.append(("All Packages", "all"))
  VV625J.append(VVm77t)
  VV625J.append(("Plugin/SoftCAM/Skin", "plugins"))
  VV625J.append(VVm77t)
  for word in words:
   VV625J.append((word, word))
  FFuRfS(self, BF(self.VVToku, VVcpnp), VV625J=VV625J, title="Select Filter")
 def VVToku(self, VVcpnp, item=None):
  if item:
   if item == "all":
    titleTxt = "All"
    grep = ""
   elif item == "plugins":
    titleTxt = "Plugin/SoftCAM/Skin"
    grep  = "| grep '^enigma2-plugin-' | grep 'extensions\|systemplugins\|softcams\|skin'"
   else:
    titleTxt = item
    word = item.lower()
    if word.endswith("s"):
     word = word[:-1]
    grep = "| grep '%s'" % word
   FFlX3B(VVcpnp, BF(self.VVs3jj, 0, grep, VVcpnp, "Download/Install (Filter = %s)" % titleTxt), title="Filtering ...")
 def VVQdQ3(self, VVcpnp, title, txt, colList):
  currentRow  = colList[0]
  package  = colList[1]
  if package.startswith((VV9VaA, VVuVce)):
   FFMIbO(self, BF(self.VVNCC3, VVcpnp, package), "Delete Plugin Folder ?\n\n%s" % package)
  else:
   VV625J = []
   VV625J.append(("Remove Package"         , "remove_ExistingPackage" ))
   VV625J.append(("Remove Package (force remove)"     , "remove_ForceRemove"  ))
   VV625J.append(("Remove Package (ignore failed dependencies)"  , "remove_IgnoreDepends" ))
   FFuRfS(self, BF(self.VVnoN3, VVcpnp, package), VV625J=VV625J)
 def VVNCC3(self, VVcpnp, package):
  cmd  = "echo -e 'Deleting plugin directory:\n%s\n';" % package
  cmd += "rm -r '%s' &>/dev/null %s" % (package, VVrML3)
  FFfbee(self, cmd, VVIwP9=BF(self.VV3IkV, VVcpnp))
 def VVnoN3(self, VVcpnp, package, item):
  if item:
   if   item == "remove_ExistingPackage" : cmdOpt = VVvtgi
   elif item == "remove_ForceRemove"  : cmdOpt = VVjAHQ
   elif item == "remove_IgnoreDepends"  : cmdOpt = VVJ3c9
   FFMIbO(self, BF(self.VVg9QX, VVcpnp, package, cmdOpt), "Remove Package ?\n\n%s" % package)
 def VVg9QX(self, VVcpnp, package, cmdOpt):
  self.lastSelectedRow = VVcpnp.VVgrGB()
  cmd = FFQ7Q5(cmdOpt, package)
  if cmd : FFfbee(self, cmd, VVIwP9=BF(self.VV3IkV, VVcpnp))
  else : FFHRK6(self)
 def VV3IkV(self, VVcpnp):
  VVcpnp.cancel()
  FFkmMQ()
 def VVSf33(self, VVcpnp, title, txt, colList):
  package  = colList[1]
  VV625J = []
  VV625J.append(("Install Package"         , "install_CheckVersion" ))
  VV625J.append(("Install Package (force reinstall)"    , "install_ForceReinstall" ))
  VV625J.append(("Install Package (force overwrite)"    , "install_ForceOverwrite" ))
  VV625J.append(("Install Package (force downgrade)"    , "install_ForceDowngrade" ))
  VV625J.append(("Install Package (ignore failed dependencies)"  , "install_IgnoreDepends" ))
  FFuRfS(self, BF(self.VVEAP8, package), VV625J=VV625J)
 def VVEAP8(self, package, item):
  if item:
   if   item == "install_CheckVersion"  : cmdOpt = VV4pye
   elif item == "install_ForceReinstall" : cmdOpt = VVEoQq
   elif item == "install_ForceOverwrite" : cmdOpt = VVKrAC
   elif item == "install_ForceDowngrade" : cmdOpt = VViRav
   elif item == "install_IgnoreDepends" : cmdOpt = VVDDR8
   FFMIbO(self, BF(self.VVyNJa, package, cmdOpt), "Install Package ?\n\n%s" % package)
 def VVyNJa(self, package, cmdOpt):
  cmd = FFQ7Q5(cmdOpt, package)
  if cmd : FFfbee(self, cmd, VVIwP9=FFkmMQ, checkNetAccess=True)
  else : FFHRK6(self)
 def VVTC5l(self, VVcpnp, title, txt, colList):
  package  = colList[1]
  FFMIbO(self, BF(self.VVWUHK, package), "Download Package ?\n\n%s" % package)
 def VVWUHK(self, package):
  if FFINsi():
   cmd = FFQ7Q5(VVgetH, package)
   if cmd:
    dest = CFG.downloadedPackagesPath.getValue()
    success = "Downloaded to:"
    andTxt = "echo -e '\n%s\n%s' %s" % (success, dest, FF95sl(success, VV9cEK))
    fail = "Download Failed"
    orTxt = "echo -e '\n%s' %s" % (fail, FF95sl(fail, VVzZva))
    cmd  = "cd '%s'; %s && %s || %s" % (dest, cmd, andTxt, orTxt)
    FFfbee(self, cmd, VVour7=[VVzZva, "error:", "collected errors:", "failed", "not found"], checkNetAccess=True)
   else:
    FFHRK6(self)
  else:
   FFkYsE(self, "No internet connection !")
 def VVsDCo(self, package):
  infoCmd  = FFQ7Q5(VVCBKn, package)
  filesCmd = FFQ7Q5(VVpvpX, package)
  listInstCmd = FFaG6T(VVPeIJ, "")
  if infoCmd and filesCmd and listInstCmd:
   timeText = "Installed-Time: "
   notInst  = "Package not installed with Packaging Tools."
   sep   = FFoEsu(VVdWFT)
   cmd  = "PACK='%s';" % package
   cmd += "FOUND=$(%s | grep $PACK);" % listInstCmd
   cmd += "if [[ -z \"$FOUND\" ]]; then "
   cmd += " echo -e 'No package information !\n';"
   cmd += " echo -e '%s' %s;" % (notInst, FF95sl(notInst, VVU8eD))
   cmd += "else "
   cmd +=   FFt615("System Info", VVdWFT)
   cmd += " %s $PACK | sed 's/:/\t:/g';" % infoCmd
   cmd += " TIME=$(%s $PACK | grep %s | sed 's/%s//g');" % (infoCmd, timeText, timeText)
   cmd += " HTIME=$(date -d @$TIME);"
   cmd += " echo %s$HTIME | sed 's/: /\t: /g';" % timeText
   cmd += " echo '';"
   cmd +=   FFt615("Related Files", VVdWFT)
   cmd += "  %s $PACK | awk 'NR<2{print($0);next}{print($0)| \"sort\"}' | sed 's/files:/files:\\n/g';" % filesCmd
   cmd += " echo '';"
   cmd +=   sep
   cmd += "fi;"
   FFCa80(self, cmd)
  else:
   FFHRK6(self)
class CC2LVn():
 def VVpp9G(self, isRef):
  self.shareIsRef   = isRef
  self.shareFilePrefix = "%sajpanel_share_%s_" % (VVCnD5, "ref" if self.shareIsRef else "data")
  self.shareFilePath  = ""
  self.shareData   = []
  self.VVwcqQ()
 def VVwcqQ(self):
  files = iGlob("%s*.xml" % self.shareFilePrefix)
  if files:
   files.sort()
   VV625J = []
   for fil in files:
    VV625J.append((os.path.basename(fil), fil))
   if self.shareIsRef : VVz2kc, VVwpZm = "#22221133", "#22221133"
   else    : VVz2kc, VVwpZm = "#22003344", "#22002233"
   VVmKbI  = ("Add new File", self.VVLu9I)
   VVJ5GS = ("Delete File", self.VVhdNO)
   FFuRfS(self, self.VVBR6h, VV625J=VV625J, width=1100, VVmKbI=VVmKbI, VVJ5GS=VVJ5GS, minRows=4, VVz2kc=VVz2kc, VVwpZm=VVwpZm)
  else:
   FFMIbO(self, self.VV5Uf5, "No files found.\n\nCreate a new file ?")
 def VV5Uf5(self):
  path = self.VVEssc()
  if fileExists(path) : self.VVwcqQ()
  else    : FFD1yO(self, "Cannot create file", 1500)
 def VVLu9I(self, menuInstance, path):
  path = self.VVEssc()
  menuInstance.VVssYC((os.path.basename(path), path), isSort=True)
 def VVEssc(self):
  path = "%s%s.xml" % (self.shareFilePrefix, FFGuM2())
  with open(path, "w") as f:
   f.write('<?xml version="1.0" encoding="utf-8"?>\n<share>\n\n\t<ch>\n\t\t<name1>Channel-1</name1>  <ref1>5001:0:1:22:22:22:22:0:0:0</ref1>\n\t\t<name2>Channel-2</name2>  <ref2>4097:0:1:22:22:22:22:0:0:0</ref2>\n\t</ch>\n\n</share>')
  return path
 def VVhdNO(self, menuInstance, path):
  FFMIbO(self, BF(self.VV4kaX, menuInstance, path), "Delete this file ?\n\n%s" % path)
 def VV4kaX(self, menuInstance, path):
  FFX92w(path)
  if fileExists(path) : FFD1yO(menuInstance, "Not deleted", 1000)
  else    : menuInstance.VVVDex()
 def VVBR6h(self, path=None):
  if path:
   FFlX3B(self, BF(self.VVgZfH, path))
 def VVgZfH(self, path):
  if not fileExists(path):
   FFAVqd(self, path)
   return
  elif not CC7ujK.VV4HLe(self, path, FFNUl9()):
   return
  else:
   self.shareFilePath = path
  if not CCGR8s.VVLXcG(self):
   return
  tree = CCtSdI.VVST2L(self, self.shareFilePath)
  if not tree:
   return
  refLst = CCgKdM.VV1iFE()
  def VVQQs4(refCode):
   if   FFqcpq(refCode): return FFkhYI("DVB", VVk6tE)
   elif refCode in refLst     : return FFkhYI("IPTV", VVk6tE)
   else         : return ""
  VVvhuK= []
  errColor= "#f#00ffaa55#"
  num  = 1
  dupl = 0
  for ch in tree.getroot():
   ok, srcName, srcRef, dstName, dstRef = self.VVXvAf(ch)
   if ok:
    srcTxt = VVQQs4(srcRef)
    dstTxt = VVQQs4(dstRef)
    srcName, dstName = srcName.strip(), dstName.strip()
    skip = False
    for num1, srcName1, srcRef1, srcTxt1, dstName1, dstRef1, dstTxt1, remark1 in VVvhuK:
     if (srcRef, dstRef) == (srcRef1, dstRef1):
      dupl += 1
      break
    else:
     if  srcRef == dstRef : remark, c1, c2 = "4", errColor, errColor
     elif srcTxt and dstTxt : remark, c1, c2 = "0", ""  , ""
     elif dstTxt    : remark, c1, c2 = "1", errColor, ""
     elif srcTxt    : remark, c1, c2 = "2", ""  , errColor
     else     : remark, c1, c2 = "3", errColor, errColor
     c3 = "#f#0000ff00#" if remark == "0" else errColor
     VVvhuK.append((c3 + str(num), c1 + srcName, c1 + srcRef, c1 + srcTxt, c2 + dstName, c2 + dstRef, c2 + dstTxt, remark))
     num += 1
  refLst = None
  if VVvhuK:
   if self.shareIsRef : VVz2kc, VVwpZm, optTxt = "#22221133", "#22221133", "Share Reference"
   else    : VVz2kc, VVwpZm, optTxt = "#1a003344", "#1a002233", "Copy EPG/PIcons"
   VVKx4L = (""    , BF(self.VVqCUb, dupl), [])
   VV01dN = (""    , self.VVkwRz    , [])
   VVMQj9 = ("Delete Entry" , self.VV5UiN   , [])
   VV3th8 = ("Add Entry"  , self.VVCaeY   , [])
   VVOtSO = (optTxt   , self.VViboO  , [])
   header  = ("Num" , "Source" , "Source Ref." ,"Type" , "Destination" , "Dest. Ref." , "Type", "Remark" )
   widths  = (8  , 25  , 15   , 6  , 25   , 15   , 6  , 0   )
   VVQqg2 = (CENTER , LEFT  , LEFT   ,CENTER , LEFT   , LEFT   , CENTER, CENTER )
   VVcpnp = FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=24, VVKx4L=VVKx4L, VV01dN=VV01dN, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, VVKNen=True, searchCol=1, lastFindConfigObj=CFG.lastFindServices
         , VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVwpZm, VVAfLs="#00ffffaa", VV0g1U="#0a000000")
  else:
   FFkYsE(self, "No valid sharing data found in:\n\n%s" % self.shareFilePath)
 def VVqCUb(self, dupl, VVcpnp, title, txt, colList):
  if dupl:
   VVcpnp.VVIX8q("Skipped %d duplicate%s" % (dupl, FFICXm(dupl)), 2000)
 def VVkwRz(self, VVcpnp, title, txt, colList):
  def VVQQs4(key, val): return "%s\t: %s\n" % (key, val or FFkhYI("?", VVMmz2))
  Keys = VVcpnp.VVixmS()
  Vals = VVcpnp.VVPxSj()
  txt = ""
  for i in range(len(Keys) - 1):
   txt += VVQQs4(Keys[i], Vals[i])
   if i in (0, 3, 6):
    txt += "\n"
  remark = colList[7]
  txt1 = "Remarks\t: "
  c1, c2 = VV9cEK, VVMmz2
  if   remark == "0": txt1 += c1 + "Valid"
  elif remark == "1": txt1 += c2 + "Source channel is not in system"
  elif remark == "2": txt1 += c2 + "Destination channel is not in system"
  elif remark == "3": txt1 += c2 + "Both channels are not in system"
  elif remark == "4": txt1 += c2 + "Both channels have same Reference"
  FFNEkd(self, txt + txt1, title=title)
 def VVXvAf(self, chElem):
  srcName = chElem.find("name1")
  srcRef  = chElem.find("ref1")
  dstName = chElem.find("name2")
  dstRef  = chElem.find("ref2")
  patt = r"((?:[A-Fa-f0-9]+:){9}(?:[A-Fa-f0-9]+))"
  if srcName is not None and srcRef is not None and dstName is not None and dstRef is not None:
   lst = [srcName.text or "", srcRef.text or "", dstName.text or "", dstRef.text or ""]
   for i, text in enumerate(lst):
    lst[i] = str(text.encode("UTF-8").decode())
   srcName, srcRef, dstName, dstRef = lst
   span = iSearch(patt, srcRef)
   if span:
    srcRef = span.group(1).upper()
    span = iSearch(patt, dstRef)
    if span:
     dstRef = span.group(1).upper()
     return True, srcName.strip(), srcRef.strip(":"), dstName.strip(), dstRef.strip(":")
  return False, "", "", "", ""
 def VV5UiN(self, VVcpnp, title, txt, colList):
  if VVcpnp.VVgrGB() == 0 and VVcpnp.VVI1WG() == 1:
   isLast, ques = True, "This is the last entry.\n\nDelete File ?"
  else:
   isLast, ques = False, "Delete current row ?"
  FFMIbO(self, BF(self.VVeA2S, isLast, VVcpnp), ques)
 def VVeA2S(self, isLast, VVcpnp):
  if isLast:
   FFX92w(self.shareFilePath)
   VVcpnp.cancel()
  else:
   num, srcName, srcRef, srcType, dstName, dstRef, dstType, remark = VVcpnp.VVPxSj()
   if self.VVJ68U(srcName, srcRef, dstName, dstRef):
    VVcpnp.VVmxfU()
    VVcpnp.VVubDz()
    FFD1yO(VVcpnp, "Deleted", 500, isGrn=True)
   else:
    FFD1yO(VVcpnp, "Cannot delete from file", 2000)
 def VVCaeY(self, VVcpnp, title, txt, colList):
  self.shareData = []
  if self.shareIsRef : self.VVvFXu(VVcpnp, isDvb=True)
  else    : self.VV7ItN(VVcpnp, "Source Channel", "#22003344", "#22002233")
 def VV7ItN(self, mainTableInst, title, VVz2kc, VVwpZm):
  FFuRfS(self, BF(self.VVESLJ, mainTableInst, title), VV625J=[("DVB", "DVB"), ("IPTV", "IPTV")], title=title + " Type", width=800, VVz2kc=VVz2kc, VVwpZm=VVwpZm)
 def VVESLJ(self, mainTableInst, title, item=None):
  if item:
   FFlX3B(mainTableInst, BF(self.VVegIf, mainTableInst, title, item), clearMsg=False)
 def VVegIf(self, mainTableInst, title, item):
  FFD1yO(mainTableInst)
  if item == "DVB": self.VVvFXu(mainTableInst, isDvb=True)
  else   : self.VVvFXu(mainTableInst, isDvb=False)
 def VVIVzz(self, mainTableInst, chType, VVcpnp, title, txt, colList):
  self.shareData.append((colList[0], colList[3], chType))
  curRowNdx = VVcpnp.VVgrGB()
  if   chType == "DVB" : FFnT3A(CFG.lastSharePickerDvbRow , curRowNdx)
  elif chType == "IPTV": FFnT3A(CFG.lastSharePickerIptvRow, curRowNdx)
  if len(self.shareData) == 2:
   srcName, srcRef, srcTxt = self.shareData[0]
   dstName, dstRef, dstTxt = self.shareData[1]
   srcName, dstName = srcName.strip(), dstName.strip()
   if not srcRef == dstRef:
    for ndx, row in enumerate(mainTableInst.VVGrbO()):
     num1, srcName1, srcRef1, srcTxt1, dstName1, dstRef1, dstTxt1, remark1 = row
     if (srcRef, dstRef) == (srcRef1, dstRef1):
      FFkYsE(self, "Already added in row Num-%d" % (ndx + 1))
      break
    else:
     if self.VVWVqY(srcName, srcRef, dstName, dstRef):
      mainTableInst.VVc4hA((str(mainTableInst.VVI1WG() + 1), srcName, srcRef, srcTxt, dstName, dstRef, dstTxt, "0"))
      FFD1yO(mainTableInst, "Added", 500, isGrn=True)
     else:
      FFD1yO(mainTableInst, "Cannot edit XML File", 2000)
   else:
    FFD1yO(mainTableInst, "Cannot use same Reference", 2000)
  else:
   if self.shareIsRef : self.VVvFXu(mainTableInst, isDvb=False)
   else    : FFpoMu(BF(self.VV7ItN, mainTableInst, "Select Destination", "#11661122", "#11661122"))
  VVcpnp.cancel()
 def VViNnq(self, item, VVcpnp, title, txt, colList):
  if   item == "DVB" : ndx = CFG.lastSharePickerDvbRow.getValue()
  elif item == "IPTV": ndx = CFG.lastSharePickerIptvRow.getValue()
  VVcpnp.VVtpKN(ndx)
 def VVvFXu(self, VVcpnp, isDvb):
  typ  = "DVB" if isDvb else "IPTV"
  txt  = "Soruce" if len(self.shareData) == 0 else "Destination"
  okFnc = BF(self.VVIVzz, VVcpnp, typ)
  doneFnc = BF(self.VViNnq, typ)
  if isDvb: CC2LVn.VVXbjK(VVcpnp , "Select %s (%s)" % (txt, typ), okFnc, doneFnc)
  else : CC2LVn.VV55Ip(VVcpnp, "Select %s (%s)" % (txt, typ), okFnc, doneFnc)
 @staticmethod
 def VVXbjK(SELF, title, okFnc, doneFnc=None):
  FFlX3B(SELF, BF(CC2LVn.VVfn2g, SELF, title, okFnc, doneFnc), title="Loading DVB Services ...")
 @staticmethod
 def VVfn2g(SELF, title, okFnc, doneFnc=None):
  VVvhuK, err = CCtSdI.VV4uiY(SELF, CCtSdI.VVsyiP)
  if VVvhuK:
   color = "#0a000022"
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVVHmY = ("Select" , okFnc, [])
   VVKx4L= ("", doneFnc, []) if doneFnc else None
   header  = ("Name" , "Provider", "Sat.", "Reference" )
   widths  = (29  , 27  , 9  , 35   )
   VVQqg2 = (LEFT  , LEFT  , CENTER, LEFT    )
   FF1dQ4(SELF, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVz2kc=color, VVwpZm=color, VVghPi=color, VVVHmY=VVVHmY, VVKx4L=VVKx4L, lastFindConfigObj=CFG.lastFindServices)
  else:
   FFkYsE(SELF, "No DVB Services !")
 @staticmethod
 def VV55Ip(SELF, title, okFnc, doneFnc=None):
  FFlX3B(SELF, BF(CC2LVn.VVdmM7, SELF, title, okFnc, doneFnc), title="Loading IPTV Services ...")
 @staticmethod
 def VVdmM7(SELF, title, okFnc, doneFnc=None):
  VVvhuK = CC2LVn.VVjfPE()
  if VVvhuK:
   color = "#0a112211"
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVVHmY = ("Select" , okFnc, [])
   VVKx4L= ("", doneFnc, []) if doneFnc else None
   header  = ("Name" , "Bouquet" , "URL" , "Reference" )
   widths  = (35  , 35  , 15 , 15   )
   FF1dQ4(SELF, None, title=title, header=header, VVvytR=VVvhuK, VVoJsQ=widths, VVmp7B=26, VVz2kc=color, VVwpZm=color, VVghPi=color, VVVHmY=VVVHmY, VVKx4L=VVKx4L, lastFindConfigObj=CFG.lastFindIptv)
  else:
   FFkYsE(SELF, "No IPTV Services !")
 @staticmethod
 def VVjfPE():
  VVvhuK = []
  files  = CCqQHV.VVJ90G()
  patt  = r"#SERVICE\s+([A-Fa-f0-9]+:0:(?:[A-Fa-f0-9]+[:]){8})(http.+)\n#DESCRIPTION\s+(.+)"
  if files:
   for path in files:
    txt = FFqD66(path)
    span = iSearch(r"#NAME\s(.+)", txt, IGNORECASE)
    if span : VVb6wY = span.group(1)
    else : VVb6wY = ""
    VVb6wY_lCase = VVb6wY.lower()
    for match in iFinditer(patt, txt, IGNORECASE):
     refCode = match.group(1).upper().strip(":")
     url  = match.group(2).strip()
     chName = match.group(3).strip()
     VVvhuK.append((chName, VVb6wY, url, refCode))
  return VVvhuK
 def VVWVqY(self, srcName, srcRef, dstName, dstRef):
  tree = CCtSdI.VVST2L(self, self.shareFilePath)
  if not tree:
   return False
  root = tree.getroot()
  ch = iElem.Element("ch")
  root.append(ch)
  name  = iElem.SubElement(ch, "name1")
  ref   = iElem.SubElement(ch, "ref1")
  name.text = srcName
  ref.text = srcRef
  name  = iElem.SubElement(ch, "name2")
  ref   = iElem.SubElement(ch, "ref2")
  name.text = dstName
  ref.text = dstRef
  self.VV0ZAT(tree, root)
  return True
 def VVJ68U(self, srcName1, srcRef1, dstName1, dstRef1):
  tree = CCtSdI.VVST2L(self, self.shareFilePath)
  if not tree:
   return False
  tableLst = [srcName1, srcRef1, dstName1, dstRef1]
  found = False
  root = tree.getroot()
  for ch in root:
   ok, srcName, srcRef, dstName, dstRef = self.VVXvAf(ch)
   if ok and [srcName, srcRef, dstName, dstRef] == tableLst:
    root.remove(ch)
    found = True
  if found:
   self.VV0ZAT(tree, root)
  return found
 def VV0ZAT(self, tree, root, withComments=True):
  xmlTxt = iElem.tostring(root)
  txt  = CCtSdI.VVU5T5(xmlTxt)
  parser = CCtSdI.CCRSA9()
  if withComments : parser = iElem.XMLParser(target=parser)
  else   : parser = None
  root = iElem.fromstring(txt, parser=parser)
  tree._setroot(root)
  tree.write(self.shareFilePath, encoding="UTF-8")
 def VViboO(self, VVcpnp, title, txt, colList):
  VV625J = []
  if self.shareIsRef:
   FFMIbO(self, BF(FFlX3B, VVcpnp, BF(self.VV2ei1, VVcpnp)), "Copy all References from Source to Destination ?")
  else:
   VV625J.append(("Copy EPG\t (All List)" , "epg"  ))
   VV625J.append(("Copy Picons\t (All List)" , "picon" ))
   FFuRfS(self, BF(self.VV40or, VVcpnp), VV625J=VV625J, width=1000)
 def VV40or(self, VVcpnp, item=None):
  if item:
   if   item == "epg" : fnc, txt = self.VVYjh2  , "EPG"
   elif item == "picon": fnc, txt = self.VVamob , "PIcons"
   title = "Copy %s" % txt
   tot   = VVcpnp.VVI1WG()
   FFMIbO(self, BF(FFlX3B, VVcpnp, BF(fnc, VVcpnp, title)), "Overwrite %s for %d Service%s ?" % (FFkhYI(txt, VVdWFT), tot, FFICXm(tot)), title=title)
 def VV2ei1(self, VVcpnp):
  files = CCqQHV.VVJ90G()
  totChange = 0
  if files:
   for path in files:
    txt = FFqD66(path)
    toSave = False
    for num, srcName, srcRef, srcTxt, dstName, dstRef, dstTxt, remark in VVcpnp.VVGrbO():
     if remark == "0":
      srcPart = ":".join(srcRef.split(":")[1:]) + ":"
      dstPart = ":".join(dstRef.split(":")[1:]) + ":"
      txt, tot = iSubn(r"(#SERVICE\s+(?:[A-Fa-f0-9]+[:]))%s(.+\/\/.+)" % dstPart, r"\g<1>%s\2" % srcPart, txt, IGNORECASE)
      if tot:
       toSave = True
       totChange += tot
    if toSave:
     with open(path, "w") as f:
      f.write(txt)
  if totChange > 0:
   FFlB9k()
  tot = VVcpnp.VVI1WG()
  txt  = "Services\t: %d\n" % tot
  txt += "Changed\t: %d\n"  % totChange
  txt += "Skipped\t: %d\n"  % (tot- totChange)
  FFNEkd(self, txt)
 def VVamob(self, VVcpnp, title):
  if not iCopyfile:
   FFkYsE(self, "Module not found:\n\nshutil", title=title)
   return
  pPath = CCrs3r.VVsNIk()
  totFound = totDone = totSame = totErr = 0
  for num, srcName, srcRef, srcTxt, dstName, dstRef, dstTxt, remark in VVcpnp.VVGrbO():
   srcPng = pPath + srcRef.replace(":", "_") + ".png"
   dstPng = pPath + dstRef.replace(":", "_") + ".png"
   if fileExists(srcPng):
    totFound += 1
    if srcPng == dstPng:
     totSame += 1
    else:
     try:
      iCopyfile(srcPng, dstPng)
      totDone += 1
     except:
      totErr += 1
  txt  = "Services\t: %d\n" % VVcpnp.VVI1WG()
  txt += "Found\t: %d\n" % totFound
  txt += "Copied\t: %d"  % totDone
  if totSame: txt += "\nSame Ref.\t: %d" % totSame
  if totErr : txt += "\nErrors\t: %d"  % totErr
  FFNEkd(self, txt, title=title)
 def VVYjh2(self, VVcpnp, title):
  from enigma import eEPGCache
  totFound = totEvents = totSuccess = totInvalid = 0
  epgInst = eEPGCache.getInstance()
  if not epgInst:
   FFkYsE(self, "Cannot access EPG Cache !", title=title)
   return
  for num, srcName, srcRef, srcTxt, dstName, dstRef, dstTxt, remark in VVcpnp.VVGrbO():
   if remark == "0":
    evList = epgInst.lookupEvent(["BDTSE", (srcRef, 0, -1, 20160)])
    if evList:
     totFound += 1
     lst = []
     for item in evList:
      lst.append((item[0], item[1], item[2], item[3], item[4], 1))
     totEv, totOK = CCARMv.VVbwY9(dstRef, lst)
     totEvents += totEv
     totSuccess += totOK
   else:
    totInvalid += 1
  if totSuccess > 0:
   CC2LVn.VVdL9t()
  txt  = "Services\t: %d\n"  % VVcpnp.VVI1WG()
  txt += "Invalid Ref.\t: %s\n" % totInvalid
  txt += "With Events\t: %d\n\n" % totFound
  txt += "Found Events\t: %d\n" % totEvents
  txt += "Copied Events\t: %d\n" % totSuccess
  FFNEkd(self, txt, title=title)
 class CCRSA9(iElem.TreeBuilder):
  def comment(self, data):
   self.start(iElem.Comment, {})
   self.data(data)
   self.end(iElem.Comment)
 @staticmethod
 def VVST2L(SELF, path, withComments=True, title=""):
  try:
   if withComments : parser = iElem.XMLParser(target=CCtSdI.CCRSA9())
   else   : parser = None
   return iElem.parse(path, parser=parser)
  except Exception as e:
   txt  = "%s\n%s\n\n" % (FFkhYI("XML Parse Error in:", VVMmz2), path)
   txt += "%s\n%s\n\n" % (FFkhYI("Error:", VVMmz2), str(e))
   FFNEkd(SELF, txt, VVghPi="#11220000", title=title)
   return None
 @staticmethod
 def VVU5T5(xmlTxt):
  txt = iSub(r">[\n\s]*", ">" , xmlTxt.decode("UTF-8"))
  txt = iSub(r"([^12])>\s*<" , r"\1>\n<", txt)
  txt = iSub(r"ref1>\s*<name2", r"ref1>\n<name2", txt)
  txt = iSub(r"</ref2></ch>" , r"</ref2>\n</ch>\n", txt)
  txt = iSub(r"<ch>"   , r"\t<ch>", txt)
  txt = iSub(r"</ch>"   , r"\t</ch>", txt)
  txt = iSub(r"<name1>"  , r"\t\t<name1>", txt)
  txt = iSub(r"<name2>"  , r"\t\t<name2>", txt)
  txt = iSub(r"(<!-- .+ -->)" , r"\t\1\n", txt)
  txt = iSub(r"<share>"  , r"<share>\n", txt)
  return txt
 @staticmethod
 def VVdL9t():
  try:
   from enigma import eEPGCache
   epgInst = eEPGCache.getInstance()
   if epgInst and hasattr(eEPGCache, "save"):
    epgInst.save()
  except:
   pass
class CCtSdI(Screen, CC2LVn):
 VVh6ih  = 0
 VV5Dgx = 1
 VVJDbn  = 2
 VV2kvG  = 3
 VVtZVs = 4
 VV3E27 = 5
 VVG95i = 6
 VVsyiP   = 7
 def __init__(self, session):
  self.skin, self.skinParam = FF896P(VVoxS0, 1000, 1000, 50, 40, 30, "#22000033", "#22000011", 30)
  self.session   = session
  self.filterObj    = None
  self.VVrCVs = None
  self.lastfilterUsed  = None
  self.servFilterInFilter = False
  VV625J = self.VV5l9M()
  FFJd2Z(self, VV625J=VV625J, title="Services/Channels")
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self["myMenu"].setList(self.VV5l9M())
  FFkCFB(self["myMenu"])
  FF4FP6(self)
 def VV5l9M(self):
  VV625J = []
  c = VVk6tE
  VV625J.append((c + "Current Service (Signal / Player)"    , "currentServiceSignal"    ))
  VV625J.append((c + "Current Service (info.)"       , "currentServiceInfo"     ))
  VV625J.append(VVm77t)
  c = VVoTT6
  VV625J.append((c + "Services (Change Parental-Control & Hidden)"  , "lameDB_allChannels_with_refCode"  ))
  VV625J.append((c + "Services (Transponders)"       , "lameDB_allChannels_with_tranaponder" ))
  VV625J.append((VVMmz2 + "More tables ..."     , "VVX3qF"    ))
  c = VVNTmM
  VV625J.append(VVm77t)
  txt = "Import Bouquets from Backup Files"
  if iTar : VV625J.append((c + txt          , "VV1ECt"  ))
  else : VV625J.append((txt           ,          ))
  VV625J.append((c + 'Export Services to "channels.xml"'    , "VVYSwu"      ))
  VV625J.append((c + "Copy EPG/PIcons between Channels (from xml file)" , "copyEpgPicons"      ))
  c = VVTdoW
  VV625J.append(VVm77t)
  VV625J.append((c + "Satellites Services Cleaner"      , "SatellitesCleaner"     ))
  VV625J.append((c + "Invalid Services Cleaner"       , "VV5ctL"    ))
  c = VVTdoW
  VV625J.append(VVm77t)
  VV625J.append((c + "Delete Channels with no names"     , "VVY0HL"    ))
  VV625J.append((c + "Delete Empty Bouquets"       , "VVVmbR"     ))
  VV625J.append(VVm77t)
  VVXBRO, VVMxmb = CCtSdI.VVQokV()
  if fileExists(VVXBRO):
   enab = fileExists(VVMxmb)
   if enab: VV625J.append(("Enable Hidden Services List"    , "enableHiddenChannels"    ))
   else   : VV625J.append(("Disable Hidden Services List"   , "disableHiddenChannels"    ))
  VV625J.append(("Reset Parental Control Settings"      , "VVCmak"    ))
  VV625J.append(VVm77t)
  VV625J.append(("Reload Channels and Bouquets"       , "VVQG6O"      ))
  return VV625J
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "currentServiceSignal"     : FF3bCE(self)
   elif item == "currentServiceInfo"     : FFBatl(self, fncMode=CCARMv.VVTlHJ)
   elif item == "lameDB_allChannels_with_refCode"  : FFlX3B(self, self.VVGy2G)
   elif item == "lameDB_allChannels_with_tranaponder" : FFlX3B(self, self.VVkq1R)
   elif item == "VVX3qF"     : self.VVX3qF()
   elif item == "VV1ECt"  : CCkCfQ.VV1ECt(self)
   elif item == "VVYSwu"      : self.VVYSwu()
   elif item == "copyEpgPicons"      : self.VVpp9G(False)
   elif item == "SatellitesCleaner"     : FFlX3B(self, self.FFlX3B_SatellitesCleaner)
   elif item == "VV5ctL"    : FFlX3B(self, BF(self.VV5ctL))
   elif item == "VVY0HL"    : FFlX3B(self, self.VVY0HL)
   elif item == "VVVmbR"     : self.VVVmbR(self)
   elif item == "enableHiddenChannels"     : self.VVL3U6(True)
   elif item == "disableHiddenChannels"    : self.VVL3U6(False)
   elif item == "VVCmak"    : FFMIbO(self, self.VVCmak, "Reset and Restart ?")
   elif item == "VVQG6O"      : FFlX3B(self, BF(CCtSdI.VVQG6O, self))
 def VVX3qF(self):
  VV625J = []
  VV625J.append(("Services (IDs)"       , "lameDB_allChannels_with_details"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Services (Parental-Control List)"   , "parentalControlChannels"    ))
  VV625J.append(("Services (Hidden List)"     , "showHiddenChannels"     ))
  VV625J.append(("Services with PIcons for the System"  , "VVDCdr"     ))
  VV625J.append(("Services without PIcons for the System" , "servicesWithMissingPIcons"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Transponders (Statistics)"    , "TranspondersStats"     ))
  VV625J.append(("Satellites.xml (Statistics)"    , "SatellitesXmlStats"     ))
  FFuRfS(self, self.VV719v, VV625J=VV625J, title="Service Information", VVeYEo=True)
 def VV719v(self, item):
  if item:
   title, ref, ndx = item
   if   ref == "lameDB_allChannels_with_details" : FFlX3B(self, BF(self.VVM6PD, title))
   elif ref == "parentalControlChannels"   : FFlX3B(self, BF(self.VVM27A, title))
   elif ref == "showHiddenChannels"    : FFlX3B(self, BF(self.VV7JRM, title))
   elif ref == "VVDCdr"    : FFlX3B(self, BF(self.VVRmZg, title))
   elif ref == "servicesWithMissingPIcons"   : FFlX3B(self, BF(self.VVykCs, title))
   elif ref == "TranspondersStats"     : FFlX3B(self, BF(self.VV2nwK, title))
   elif ref == "SatellitesXmlStats"    : FFlX3B(self, BF(self.VVK0kH, title))
 def VVYSwu(self):
  VV625J = []
  VV625J.append(("All DVB-S/C/T Services", "all"))
  VV625J.extend(CCgKdM.VVJtDO())
  FFuRfS(self, self.VVvySQ, VV625J=VV625J, title="", VVeYEo=True)
 def VVvySQ(self, item=None):
  if item:
   txt, ref, ndx = item
   if ref == "all" : lst = CCtSdI.VVLZZO("1:7:")
   else   : lst = FFocgD(eServiceReference(ref))
   if lst:
    tot = len(lst)
    if tot > 0:
     rows = []
     for r, n in lst:
      sat = "?"
      serv = eServiceReference(r)
      if serv:
       chPath = serv.getPath()
       if not chPath    : sat = FF24qC(r, False)
       elif chPath.startswith("/") : sat = "Local"
       elif FFuZb6(r)    : sat = "IPTV"
       rows.append('<!-- %s --><channel id="%s">%s</channel><!-- %s -->\n' % (sat, n, r, n))
     if rows:
      rows.sort()
      fPath = "%schannels_%s.xml" % (FF0WrY(CFG.exportedTablesPath.getValue()), FFGuM2())
      with open(fPath, "w") as f:
       f.write('<?xml version="1.0" encoding="utf-8"?>\n')
       f.write('<channels>\n\n')
       for row in rows: f.write(row)
       f.write('\n</channels>\n')
      FFewCE(self, "Saved %d services to:\n\n%s" % (tot, fPath))
      return
   FFD1yO(self, "No Services found !", 1500)
 @staticmethod
 def VVQG6O(SELF):
  FFlB9k()
  FFewCE(SELF, "Finished\n\nReloaded Channels and Bouquets")
 def VVGy2G(self):
  self.VVrCVs = None
  self.lastfilterUsed  = None
  self.filterObj   = CCU3qf(self)
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VVh6ih)
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVVHmY  = ("Zap"   , self.VVw34P     , [])
   VV01dN = (""    , self.VVeoF7   , [])
   VVOtSO = ("Options"  , self.VVMyhq , [])
   VV3th8 = ("Current Service", self.VVlyCn , [])
   VV1QO7 = ("Filter"   , self.VV67E0  , [], "Loading Filters ...")
   header   = ("Name" , "Provider", "Sat.", "Reference" , "PC"  , "Hidden" )
   widths   = (24  , 20  , 9  , 34   , 6   , 7   )
   VVQqg2  = (LEFT  , LEFT  , CENTER, LEFT    , CENTER , CENTER )
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, lastFindConfigObj=CFG.lastFindServices)
 def VVkq1R(self):
  self.VVrCVs = None
  self.lastfilterUsed  = None
  self.filterObj   = CCU3qf(self)
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VV5Dgx)
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVVHmY  = ("Zap"   , self.VVw34P      , [])
   VV01dN = (""    , self.VVeoF7    , [])
   VV3th8 = ("Current Service", self.VVlyCn  , [])
   VVOtSO = ("Options"  , self.VVidMP , [])
   VV1QO7 = ("Filter"   , self.VVeszo  , [], "Loading Filters ...")
   header   = ("Name" , "Provider", "Type", "Ref.", "Sat.", "Transponder" , "Freq." , "Pol.", "FEC" , "SR" )
   widths   = (25  , 24  , 14 , 0.01 , 9  , 0.02   , 8   , 5  , 7  , 8  )
   VVQqg2  = (LEFT  , LEFT  , CENTER, CENTER, CENTER, CENTER   , CENTER , CENTER, CENTER, CENTER)
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, lastFindConfigObj=CFG.lastFindServices)
 def VVMyhq(self, VVcpnp, title, txt, colList):
  servName = colList[0].strip()
  refCode  = colList[3].strip()
  pcState  = colList[4].strip()
  hidState = colList[5].strip()
  mSel = CCqgU8(self, VVcpnp)
  VV625J = []
  isMulti = VVcpnp.VVbl0M
  if isMulti:
   refCodeList = VVcpnp.VVT6RH(3)
   if refCodeList:
    VV625J.append(("Add Selection to Parental Control"    , "parentalControl_sel_add"  ))
    VV625J.append(("Remove Selection from Parental Control"   , "parentalControl_sel_remove" ))
    VV625J.append(VVm77t)
    VV625J.append(("Add Selection to Hidden Services"    , "hiddenServices_sel_add"  ))
    VV625J.append(("Remove Selection from Hidden Services"   , "hiddenServices_sel_remove" ))
    VV625J.append(VVm77t)
  else:
   txt1 = "Add to Parental Control"
   txt2 = "Remove from Parental Control"
   if pcState == "No":
    VV625J.append((txt1, "parentalControl_add" ))
    VV625J.append((txt2,       ))
   else:
    VV625J.append((txt1,       ))
    VV625J.append((txt2, "parentalControl_remove"))
   VV625J.append(VVm77t)
   txt1 = "Add to Hidden Services"
   txt2 = "Remove from Hidden Services"
   if hidState == "No":
    VV625J.append((txt1, "hiddenServices_add" ))
    VV625J.append((txt2,       ))
   else:
    VV625J.append((txt1,       ))
    VV625J.append((txt2, "hiddenServices_remove" ))
   VV625J.append(VVm77t)
  cbFncDict = { "parentalControl_add"   : BF(self.VVdAtJ, VVcpnp, refCode, True)
     , "parentalControl_remove"  : BF(self.VVdAtJ, VVcpnp, refCode, False)
     , "hiddenServices_add"   : BF(self.VVayqo, VVcpnp, refCode, True)
     , "hiddenServices_remove"  : BF(self.VVayqo, VVcpnp, refCode, False)
     , "parentalControl_sel_add"  : BF(self.VV9a9y, VVcpnp, True)
     , "parentalControl_sel_remove" : BF(self.VV9a9y, VVcpnp, False)
     , "hiddenServices_sel_add"  : BF(self.VVvLJS, VVcpnp, True)
     , "hiddenServices_sel_remove" : BF(self.VVvLJS, VVcpnp, False)
     }
  VV625J1, cbFncDict1 = CCtSdI.VVazuu(self, VVcpnp, servName, 3)
  VV625J.extend(VV625J1)
  for key, val in list(cbFncDict1.items()): cbFncDict[key] = val
  mSel.VVMNiz(VV625J, cbFncDict)
 def VVidMP(self, VVcpnp, title, txt, colList):
  servName = colList[0]
  mSel = CCqgU8(self, VVcpnp)
  VV625J, cbFncDict = CCtSdI.VVazuu(self, VVcpnp, servName, 3)
  mSel.VVMNiz(VV625J, cbFncDict)
 @staticmethod
 def VVazuu(SELF, VVcpnp, servName, refCodeCol):
  tot = VVcpnp.VVMJsS()
  if tot > 0:
   sTxt = FFkhYI("%d Service%s" % (tot, FFICXm(tot)), VVoTT6)
   VV625J = [("Add %s to Bouquet ..." % sTxt   , "addToBouquet_multi" )]
  else:
   servName = FFO8d5(servName)
   if len(servName) > 20: servName = servName[:20] + ".."
   servName = FFkhYI(servName, VVoTT6)
   VV625J = [('Add "%s" to Bouquet ...' % servName , "addToBouquet_one" )]
  cbFncDict = { "addToBouquet_multi" : BF(CCtSdI.VVDjB4, SELF, VVcpnp, refCodeCol, True)
     , "addToBouquet_one" : BF(CCtSdI.VVDjB4, SELF, VVcpnp, refCodeCol, False)
     }
  return VV625J, cbFncDict
 @staticmethod
 def VVDjB4(SELF, VVcpnp, refCodeCol, isMulti):
  picker = CCgKdM(SELF, VVcpnp, "Add to Bouquet", BF(CCtSdI.VVY6OV, VVcpnp, refCodeCol, isMulti))
 @staticmethod
 def VVY6OV(VVcpnp, refCodeCol, isMulti):
  if isMulti : refCodeList = VVcpnp.VVT6RH(refCodeCol)
  else  : refCodeList = [VVcpnp.VVPxSj()[refCodeCol]]
  chUrlLst = []
  for ref in refCodeList:
   chUrlLst.append(ref)
  return chUrlLst
 def VVdAtJ(self, VVcpnp, refCode, isAddToBlackList):
  VVcpnp.VVphEN("Processing ...")
  FFpoMu(BF(self.VVGuKd, VVcpnp, [refCode], isAddToBlackList))
 def VV9a9y(self, VVcpnp, isAddToBlackList):
  refCodeList = VVcpnp.VVT6RH(3)
  if not refCodeList:
   FFkYsE(self, "Nothing selected", title="Change Parental-Control State")
   return
  VVcpnp.VVphEN("Processing ...")
  FFpoMu(BF(self.VVGuKd, VVcpnp, refCodeList, isAddToBlackList))
 def VVGuKd(self, VVcpnp, refCodeList, isAddToBlackList):
  for ndx, refCode in enumerate(refCodeList):
   refCode = refCode.strip()
   if not refCode.endswith(":"):
    refCode += ":"
    refCodeList[ndx] = refCode
  changed = False
  if isAddToBlackList:
   if isAddToBlackList:
    with open(VVhyQq, "a") as f:
     for refCode in refCodeList:
      f.write(refCode + "\n")
      changed = True
  elif fileExists(VVhyQq):
   lines = FFjdnJ(VVhyQq)
   if lines:
    for refCode in refCodeList:
     while refCode in lines:
      ndx = lines.index(refCode)
      lines[ndx] = ""
      changed = True
    if changed:
     with open(VVhyQq, "w") as f:
      for line in lines:
       if line:
        f.write(line + "\n")
  if changed:
   from Components.ParentalControl import parentalControl
   parentalControl.open()
   isMulti = VVcpnp.VVbl0M
   if isMulti:
    self.VVDfzo(VVcpnp, len(refCodeList))
   else:
    if refCode.endswith(":"):
     refCode = refCode[:-1]
    self.VVmaKG(VVcpnp, refCode)
    VVcpnp.VVhzNf()
  else:
   VVcpnp.VVIX8q("No changes")
 def VVayqo(self, VVcpnp, refCode, isHide):
  title = "Change Hidden State"
  if FFqcpq(refCode):
   VVcpnp.VVphEN("Processing ...")
   ret = FFexa9(refCode, isHide)
   if ret : FFlX3B(self, BF(self.VVmaKG, VVcpnp, refCode))
   else : FFkYsE(self, "Cannot Hide/Unhide this channel.", title=title)
  else:
   FFkYsE(self, "Cannot Hide/Unhide this channel.\n\n(Invalid transponder)", title=title)
 def VVmaKG(self, VVcpnp, refCode):
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VVh6ih, VVdrGG=[3, [refCode], False])
  done = False
  if VVvhuK:
   data = VVvhuK[0]
   if data[3] == refCode:
    done = VVcpnp.VVzOfF(data)
  if not done:
   self.VV9k1S(VVcpnp, VVcpnp.VVmgxl(), self.VVh6ih)
  VVcpnp.VVhzNf()
 def VVDfzo(self, VVcpnp, totRefCodes):
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VVh6ih, VVdrGG=self.VVrCVs)
  VVcpnp.VVuVux(VVvhuK)
  VVcpnp.VVBOaN(False)
  VVcpnp.VVIX8q("%d Processed" % totRefCodes)
 def VVvLJS(self, VVcpnp, isHide):
  refCodeList = VVcpnp.VVT6RH(3)
  if not refCodeList:
   FFkYsE(self, "Nothing selected", title="Change Hidden State")
   return
  VVcpnp.VVphEN("Processing ...")
  FFpoMu(BF(self.VVgQoQ, VVcpnp, refCodeList, isHide))
 def VVgQoQ(self, VVcpnp, refCodeList, isHide):
  totChanges = 0
  for refCode in refCodeList:
   ret = FFexa9(refCode, isHide, skipReload=True)
   if ret:
    totChanges += 1
  if totChanges > 0:
   FFlB9k(True)
   self.VVDfzo(VVcpnp, len(refCodeList))
  else:
   VVcpnp.VVIX8q("No changes")
 def VV67E0(self, VVcpnp, title, txt, colList):
  inFilterFnc = BF(self.VVwPNv, VVcpnp) if self.VVrCVs else None
  self.filterObj.VVBVkh(1, VVcpnp, 2, BF(self.VV9102, VVcpnp), inFilterFnc=inFilterFnc)
 def VV9102(self, VVcpnp, item):
  self.VVNYYX(VVcpnp, False, item, 2, self.VVh6ih)
 def VVwPNv(self, VVcpnp, menuInstance, item):
  self.VVNYYX(VVcpnp, True, item, 2, self.VVh6ih)
 def VVeszo(self, VVcpnp, title, txt, colList):
  inFilterFnc = BF(self.VVo6cg, VVcpnp) if self.VVrCVs else None
  self.filterObj.VVBVkh(2, VVcpnp, 4, BF(self.VV5xL5, VVcpnp), inFilterFnc=inFilterFnc)
 def VV5xL5(self, VVcpnp, item):
  self.VVNYYX(VVcpnp, False, item, 4, self.VV5Dgx)
 def VVo6cg(self, VVcpnp, menuInstance, item):
  self.VVNYYX(VVcpnp, True, item, 4, self.VV5Dgx)
 def VV0XIT(self, VVcpnp, title, txt, colList):
  inFilterFnc = BF(self.VVxyDv, VVcpnp) if self.VVrCVs else None
  self.filterObj.VVBVkh(0, VVcpnp, 4, BF(self.VVj10o, VVcpnp), inFilterFnc=inFilterFnc)
 def VVj10o(self, VVcpnp, item):
  self.VVNYYX(VVcpnp, False, item, 4, self.VVJDbn)
 def VVxyDv(self, VVcpnp, menuInstance, item):
  self.VVNYYX(VVcpnp, True, item, 4, self.VVJDbn)
 def VVNYYX(self, VVcpnp, isInFilter, item, satCol, mode):
  self.servFilterInFilter = isInFilter
  if self.lastfilterUsed and self.lastfilterUsed == [item, satCol, mode]:
   return
  self.lastfilterUsed = [item, satCol, mode]
  if   item.startswith("__s__") : col, words, title = satCol, item[5:] , item[5:]
  elif item.startswith("__w__") : col, words, title = 0  , item[5:] , item[5:]
  elif item == "parentalControl" : col, words, title = 4  , "Yes"  , "Parental Control"
  elif item == "hiddenServices" : col, words, title = 5  , "Yes"  , "Hidden Services"
  elif item == "selectedTP"  :
   tp = VVcpnp.VVQYAy(5)
   col, words, title = 5  , tp , tp
  elif item == "emptyTP"   : col, words, title = 6  , "-"  , "Channels with no Transponder"
  else       : col, words, title = None , "All"  , "All"
  title = "Filter = %s" % title
  if len(title) > 55:
   title = title[:55] + ".."
  if col is None:
   self.VVrCVs = None
  else:
   words, asPrefix = CCU3qf.VVP88C(words)
   self.VVrCVs = [col, words, asPrefix]
  if words: FFlX3B(VVcpnp, BF(self.VV9k1S, VVcpnp, title, mode), clearMsg=False)
  else : FFD1yO(VVcpnp, "Incorrect filter", 2000)
 def VV9k1S(self, VVcpnp, title, mode):
  VVvhuK, err = CCtSdI.VV4uiY(self, mode, VVdrGG=self.VVrCVs, VVwoAs=False)
  if self.servFilterInFilter:
   lst = []
   for row in VVcpnp.VVGrbO():
    try:
     ndx = VVvhuK.index(tuple(list(map(str.strip, row))))
     lst.append(VVvhuK[ndx])
    except:
     pass
   VVvhuK = lst
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVcpnp.VVuVux(VVvhuK, title)
  else:
   FFD1yO(VVcpnp, "Not found!", 1500)
 def VVgAkX(self, title, VVvytR, VVVHmY=None, VV01dN=None, VVMQj9=None, VV3th8=None, VVOtSO=None, VV1QO7=None):
  VV3th8 = ("Current Service", self.VVlyCn, [], )
  header  = ("Name" , "Provider", "Sat.", "Reference" )
  widths  = (29  , 27  , 9  , 35   )
  VVQqg2 = (LEFT  , LEFT  , CENTER, LEFT    )
  FF1dQ4(self, None, title=title, header=header, VVvytR=VVvytR, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, lastFindConfigObj=CFG.lastFindServices)
 def VVlyCn(self, VVcpnp, title, txt, colList):
  self.VVsATT(VVcpnp)
 def VVQ4HE(self, VVcpnp, title, txt, colList):
  self.VVsATT(VVcpnp, True)
 def VVsATT(self, VVcpnp, isFromDetails=False):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  if refCode:
   if isFromDetails:
    refCode  = refCode.upper()
    parts  = refCode.split(":")
    Namespace = parts[6].zfill(8)
    SID   = parts[3].zfill(4)
    TSID  = parts[4].zfill(4)
    ONID  = parts[5].zfill(4)
    colDict  = { 0:chName, 5:Namespace, 6:SID, 7:TSID, 8:ONID }
    VVcpnp.VV98P0(colDict, VVl2X5=True)
   else:
    VVcpnp.VV8yro(3, refCode, True)
   return
  FFkYsE(self, "Colud not read current Reference Code !")
 def VVM6PD(self, title):
  self.VVrCVs = None
  self.lastfilterUsed  = None
  self.filterObj   = CCU3qf(self)
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VVJDbn)
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VV01dN = (""    , self.VVimwQ , []      )
   VV3th8 = ("Current Service", self.VVQ4HE  , []      )
   VV1QO7 = ("Filter"   , self.VV0XIT   , [], "Loading Filters ..." )
   VVVHmY  = ("Zap"   , self.VVd1Eo      , []      )
   header   = ("Name" , "Provider", "Type-Val", "Type" , "Sat.", "Namespace" ,"SID" , "TSID", "ONID" )
   widths   = (24  , 22  , 0   , 16  , 9  , 11   , 6  , 6  , 6    )
   VVQqg2  = (LEFT  , LEFT  , CENTER , CENTER , CENTER, CENTER  , CENTER, CENTER, CENTER )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VV3th8=VV3th8, VV1QO7=VV1QO7, lastFindConfigObj=CFG.lastFindServices)
 def VVimwQ(self, VVcpnp, title, txt, colList):
  refCode  = self.VVJYeA(colList)
  chName  = colList[0]
  txt   = "%s\n\n%s" % (title, txt)
  txt   += "Reference\t: %s" % refCode
  FFBatl(self, fncMode=CCARMv.VV4ZrS, refCode=refCode, chName=chName, text=txt)
 def VVd1Eo(self, VVcpnp, title, txt, colList):
  refCode = self.VVJYeA(colList)
  FFJZ42(self, refCode)
 def VVw34P(self, VVcpnp, title, txt, colList):
  FFJZ42(self, colList[3])
 def VVJYeA(self, colList):
  chName, chProv, servTypeHex, STYPE, sat, NameSpace, SID, TSID, ONID = colList
  refCode = "1:0:%s:%s:%s:%s:%s:0:0:0" % (servTypeHex, SID.lstrip("0"), TSID.lstrip("0"), ONID.lstrip("0"), NameSpace.lstrip("0") )
  refCode = refCode.replace("::", ":0:")
  return refCode
 @staticmethod
 def VVPqAI(VVXBRO, mode=0):
  lines = FFjdnJ(VVXBRO, encLst=["UTF-8"])
  return CCtSdI.VVkHb1(lines, mode)
 @staticmethod
 def VVkHb1(lines, mode):
  lst = []
  header = "transponders" if mode < 10 else "services"
  if header in lines:
   lines = lines[lines.index(header) + 1:]
   if "end" in lines:
    lines = lines[:lines.index("end")]
    if len(lines) % 3 == 0:
     for i in range(0, len(lines), 3):
      if   mode in (0, 10): lst.append((lines[i], lines[i + 1], lines[i + 2]))
      elif mode in (1, 11): lst.append(lines[i].upper())
      elif mode in (2, 12): lst.append(lines[i + 1])
      elif mode in (3, 13): lst.append(lines[i + 2])
  return lst
 @staticmethod
 def VV4uiY(SELF, mode, VVdrGG=None, VVwoAs=True, VVDUH8=True):
  VVXBRO, err = CCtSdI.VVR3Wk(SELF, VVDUH8)
  if err:
   return None, err
  asPrefix = False
  if VVdrGG:
   filterCol = VVdrGG[0]
   filterWords = VVdrGG[1]
   asPrefix = VVdrGG[2]
   filterWords = list(filterWords)
   for ndx, item in enumerate(filterWords):
    filterWords[ndx] = item.strip().lower()
  else:
   filterWords = None
  if mode == CCtSdI.VVh6ih:
   blackList = None
   if fileExists(VVhyQq):
    blackList = FFjdnJ(VVhyQq)
    if blackList:
     blackList = set(blackList)
  elif mode == CCtSdI.VV5Dgx:
   tp = CCX8JT()
  VVUDHC, VV1Lo5 = FF92xJ()
  if mode in (CCtSdI.VV3E27, CCtSdI.VVG95i):
   VVvhuK = {}
  else:
   VVvhuK = []
  tagFound = False
  with ioOpen(VVXBRO, "r", encoding="utf-8") as f:
   lines = []
   for line in f:
    line = str(line).strip()
    if tagFound:
     if line == "end":
      break
     lines.append(line)
     if len(lines) >= 3:
      chCode = lines[0].upper()
      chName = lines[1]
      chProv = lines[2]
      if chCode.count(":") > 4 and not "," in chCode:
       parts = chCode.split(":")
       SID   = parts[0]
       NameSpace = parts[1]
       TSID  = parts[2]
       ONID  = parts[3]
       STYPE  = parts[4]
      else:
       SID = NameSpace = TSID = ONID = STYPE = SNUM = refCode = ""
      chProvOrig = chProv
      if ","  in chProv : chProv = chProv.split(",")[0].strip()
      if "p:" in chProv : chProv = chProv.split("p:")[1].strip()
      if len(chName) == 0 : chName = "-"
      if len(chProv) == 0 : chProv = "-"
      s = NameSpace.zfill(8)[:4]
      val = int(s, 16)
      sat = FFUBZ6(val)
      try:
       sTypeInt = int(STYPE)
       servTypeHex = (hex(sTypeInt))[2:].upper()
      except:
       sTypeInt = 0
       servTypeHex = "0"
      if mode == CCtSdI.VVJDbn:
       if sTypeInt in VVUDHC:
        STYPE = VV1Lo5[sTypeInt]
       tRow = (chName, chProv, servTypeHex, STYPE, sat, NameSpace, SID, TSID, ONID)
       if filterWords:
        tmp = tRow[filterCol].lower()
        if asPrefix:
         if any(tmp.startswith(x) for x in filterWords) : VVvhuK.append(tRow)
        elif any(x in tmp for x in filterWords)    : VVvhuK.append(tRow)
       else:
        VVvhuK.append(tRow)
      else:
       refCode = "1:0:%s:%s:%s:%s:%s:0:0:0" % (servTypeHex, SID.lstrip("0"), TSID.lstrip("0"), ONID.lstrip("0"), NameSpace.lstrip("0") )
       refCode = refCode.replace("::", ":0:")
       if mode == CCtSdI.VVsyiP:
        VVvhuK.append((chName, chProv, sat, refCode))
       elif mode == CCtSdI.VV3E27:
        VVvhuK[refCode.replace(":", "_")] = (chName, sat, 1)
       elif mode == CCtSdI.VVG95i:
        VVvhuK[chName] = refCode
       elif mode == CCtSdI.VVh6ih:
        if blackList and refCode + ":" in blackList : isBlackList = "Yes"
        else          : isBlackList = "No"
        flag = iSearch(r"f:([A-Fa-f0-9]+)", chProvOrig)
        if flag and int(flag.group(1), 16) & 2 == 2 : hidStr = "Yes"
        else          : hidStr =  "No"
        tRow = (chName, chProv, sat, refCode, isBlackList, hidStr)
        if filterWords:
         tmp = tRow[filterCol].lower()
         if asPrefix:
          if any(tmp.startswith(x) for x in filterWords) : VVvhuK.append(tRow)
         elif any(x in tmp for x in filterWords)    : VVvhuK.append(tRow)
        else:
         VVvhuK.append(tRow)
       elif mode == CCtSdI.VV5Dgx:
        if sTypeInt in VVUDHC:
         STYPE = VV1Lo5[sTypeInt]
        freq, pol, fec, sr, syst = tp.VVZtm9(refCode)
        if not "-S" in syst:
         sat = syst
        if freq == "-" : tpStr = "-"
        else   : tpStr = sat + " " + freq + " " + pol + " " + fec + " " + sr
        tRow = (chName, chProv, STYPE, refCode, sat, tpStr, freq, pol, fec, sr)
        if filterWords:
         tmp = tRow[filterCol].lower()
         if asPrefix:
          if any(tmp.startswith(x) for x in filterWords) : VVvhuK.append(tRow)
         elif any(x in tmp for x in filterWords)    : VVvhuK.append(tRow)
        else:
         VVvhuK.append(tRow)
       elif mode == CCtSdI.VV2kvG:
        flag = iSearch(r"f:([A-Fa-f0-9]+)", chProvOrig)
        if flag and int(flag.group(1), 16) & 2 == 2:
         VVvhuK.append((chName, chProv, sat, refCode))
       elif mode == CCtSdI.VVtZVs:
        VVvhuK.append((chName, chProv, sat, refCode))
      lines = []
    elif line == "services":
     tagFound = True
  if not VVvhuK and VVwoAs:
   FFkYsE(SELF, "No services found!")
  return VVvhuK, ""
 def VVM27A(self, title):
  if fileExists(VVhyQq):
   lines = FFjdnJ(VVhyQq)
   if lines:
    newRows = []
    VVvhuK, err = CCtSdI.VV4uiY(self, self.VVtZVs)
    if VVvhuK:
     lines = set(lines)
     for item in VVvhuK:
      refCode = item[3] + ":"
      if refCode in lines:
       newRows.append((item[0], item[1], item[2], refCode))
     if newRows:
      VVvhuK = newRows
      VVvhuK.sort(key=lambda x: x[0].lower())
      VV01dN = ("", self.VVeoF7, [])
      VVVHmY = ("Zap", self.VVw34P, [])
      self.VVgAkX(title, VVvhuK, VVVHmY=VVVHmY, VV01dN=VV01dN)
     else:
      FFNEkd(self, "No matching Reference Code found !\n\nPC Lines\t: %d\nLameDB\t: %d" % (len(lines), len(VVvhuK)))
   else:
    FFewCE(self, "No active Parental Control services.", FFNUl9())
  else:
   FFAVqd(self, VVhyQq)
 def VV7JRM(self, title):
  VVvhuK, err = CCtSdI.VV4uiY(self, self.VV2kvG)
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VV01dN = ("" , self.VVeoF7, [])
   VVVHmY  = ("Zap", self.VVw34P, [])
   self.VVgAkX(title, VVvhuK, VVVHmY=VVVHmY, VV01dN=VV01dN)
  elif err:
   pass
  else:
   FFewCE(self, "No hidden services.", FFNUl9())
 def VV5ctL(self):
  title = "Services unused in Tuner Configuration"
  VVXBRO, err = CCtSdI.VVR3Wk(self, title=title)
  if err:
   return
  nsLst = set()
  usedSats = CCtSdI.VVeKoR()
  for tuner in usedSats:
   for item in tuner[1]:
    ns = self.VVYdx1(str(item[0]))
    nsLst.add(ns)
  sysLst = CCtSdI.VVLZZO("1:7:")
  tpLst  = CCtSdI.VVPqAI(VVXBRO, mode=1)
  VVvhuK = []
  for refCode, chName in sysLst:
   servID = CCtSdI.VVVxzN(refCode)
   tpID = CCtSdI.VVlSbc(refCode)
   refNs = refCode.split(":")[6].zfill(8)[:4]
   if not tpID in tpLst or not refNs in nsLst:
    VVvhuK.append((chName, FF24qC(refCode, False), refCode, servID))
  if VVvhuK:
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVOtSO = ("Options"   , BF(self.VVJHwi, title), [])
   header   = ("Name" , "Media" , "Reference" , '"lamedb" Code' )
   widths   = (55  , 10  , 0    , 35    )
   VVQqg2  = (LEFT  , CENTER , LEFT   , CENTER   )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVOtSO=VVOtSO, VVz2kc="#0a001122", VVwpZm="#0a001122", VVghPi="#0a001122", VV0g1U="#00004455", VVooYw="#0a333333", VVPVU2="#11331100", lastFindConfigObj=CFG.lastFindServices)
  else:
   FFewCE(self, "No invalid service found !", title=title)
 def VVJHwi(self, Title, VVcpnp, title, txt, colList):
  mSel = CCqgU8(self, VVcpnp)
  isMulti = VVcpnp.VVbl0M
  if isMulti : txt = "Remove %s Services" % FFkhYI(str(VVcpnp.VVMJsS()), VVMmz2)
  else  : txt = "Remove : %s" % FFkhYI(VVcpnp.VVPxSj()[0], VVMmz2)
  VV625J = [(txt, "del")]
  cbFncDict = {"del": BF(FFlX3B, VVcpnp, BF(self.VV6j7J, VVcpnp, Title))}
  mSel.VVMNiz(VV625J, cbFncDict)
 def VV6j7J(self, VVcpnp, title):
  VVXBRO, err = CCtSdI.VVR3Wk(self, title=title)
  if err:
   return
  isMulti = VVcpnp.VVbl0M
  skipLst = []
  if isMulti : skipLst = VVcpnp.VVT6RH(3)
  else  : skipLst = [VVcpnp.VVPxSj()[3]]
  tpLst = CCtSdI.VVPqAI(VVXBRO, mode=0)
  servLst = CCtSdI.VVPqAI(VVXBRO, mode=10)
  tmpDbFile = VVXBRO + ".tmp"
  lines   = FFjdnJ(VVXBRO)
  skip = False
  with open(tmpDbFile, "w") as f:
   for line in lines:
    tLine = line.strip()
    if tLine == "services":
     skip = True
     f.write(line + "\n")
     for item in servLst:
      if not item[0].upper() in skipLst:
       for L in item:
        f.write(L + "\n")
    elif skip and tLine == "end":
     skip = False
    if not skip:
     f.write(line + "\n")
  os.system(FFxtg8("mv -f '%s' '%s'" % (tmpDbFile, VVXBRO)))
  VVvhuK = []
  for row in VVcpnp.VVGrbO():
   if not row[3] in skipLst:
    VVvhuK.append(row)
  FFlB9k()
  FFNEkd(self, "Removed Services : %d" % len(skipLst), title="Remove Services")
  if VVvhuK:
   VVcpnp.VVuVux(VVvhuK, title)
   VVcpnp.VVBOaN(False)
  else:
   VVcpnp.cancel()
 def VV2nwK(self, title):
  VVXBRO, err = CCtSdI.VVR3Wk(self)
  if err:
   return
  totT, totC, totA, totS, totS2, satList = self.VVeD1G(VVXBRO)
  txt = FFkhYI("Total Transponders:\n\n", VVpHwQ)
  txt += "   DVB-S    Satellite\t: %d \n"  % totS
  txt += "   DVB-S2  Satellite\t: %d\n"  % totS2
  txt += "   DVB-T    Terrestrial\t: %d\n" % totT
  txt += "   DVB-C    Cable\t: %d\n"   % totC
  txt += "   DVB-A    ATSC\t: %d\n"   % totA
  if satList and len(satList) > 0:
   txt += FFkhYI("\nSatellite Transponders (Total=%d):\n\n" % (totS + totS2), VVpHwQ)
   uniqSat = []
   for sat in satList:
    if not sat in uniqSat:
     uniqSat.append(sat)
   uniqSat.sort(key=lambda x: int(x))
   for item in uniqSat:
    txt += "   %s\t: %d\n" % (FFbIqi(item), satList.count(item))
  FFNEkd(self, txt, title)
 def VVeD1G(self, VVXBRO):
  totT = totC = totA = totS = totS2 = 0
  satList = []
  tagFound = False
  with ioOpen(VVXBRO, "r", encoding="utf-8") as f:
   lines = []
   for line in f:
    line = str(line).strip()
    if tagFound:
     if line == "end"    : break
     elif line.startswith("t")  : totT += 1
     elif line.startswith("c")  : totC += 1
     elif line.startswith("a")  : totA += 1
     elif line.startswith("s"):
      c = line.count(":")
      if   c > 9: totS2 += 1
      elif c > 5: totS  += 1
      if c > 5:
       satList.append(line.split(":")[4])
    elif line == "transponders":
     tagFound = True
  return totT, totC, totA, totS, totS2, satList
 def VVK0kH(self, title):
  path = "/etc/tuxbox/satellites.xml"
  if not fileExists(path):
   FFAVqd(self, path, title=title)
   return
  elif not CC7ujK.VV4HLe(self, path, title):
   return
  if not CCGR8s.VVLXcG(self):
   return
  tree = CCtSdI.VVST2L(self, path, title=title)
  if not tree:
   return
  VVvhuK = []
  root  = tree.getroot()
  totTpColor = "#f#00FFFF55#"
  for sat in root.findall("sat"):
   name = str(sat.get("name", "").encode("UTF-8").decode())
   pos  = sat.get("position", "")
   totTp = len(sat)
   hor = ver = cirL = cirR = unk = 0
   dvbS = dvbS2 = dvbUnk = 0
   for tp in sat.findall("transponder"):
    pol = tp.get("polarization")
    if   pol == "0" : hor += 1
    elif pol == "1" : ver += 1
    elif pol == "2" : cirL += 1
    elif pol == "3" : cirR += 1
    Sys = tp.get("system")
    if   Sys == "0" : dvbS += 1
    elif Sys == "1" : dvbS2 += 1
   try:
    posNum = int(pos)
    if posNum == 1801:
     posCalc = "180.1E"
    else:
     if posNum < 0:
      posNum += 3600
     posCalc = FFUBZ6(posNum)
   except:
    posCalc = "?"
    pos  = "-9999"
   if " " in name : posXml, name = name.split(" ", 1)
   else   : posXml = posCalc
   bg = "" if posCalc.endswith("W") else "#b#00003333#"
   VVvhuK.append((bg + name, pos, posXml, posCalc, totTpColor + str(totTp), str(hor), str(ver), str(cirL), str(cirR), str(dvbS), str(dvbS2)))
  if VVvhuK:
   VVvhuK.sort(key=lambda x: int(x[1]))
   VV3th8 = ("Current Satellite", BF(self.VVjDGV, 3), [])
   header   = ("Satellite" , "Pos #" , "xml Pos" , "Position", "TP" , "Hor" , "Ver" , "Circ-L" , "Circ-R" , "DVB-S" , "DVB-S2" )
   widths   = (36    , 8   , 0   , 10  , 6  , 5  , 5  , 7   , 7   , 8   , 8   )
   VVQqg2  = (LEFT   , CENTER , CENTER , CENTER , CENTER, CENTER, CENTER, CENTER , CENTER , CENTER , CENTER )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=25, VVaq0k=1, VV3th8=VV3th8, lastFindConfigObj=CFG.lastFindSatName)
  else:
   FFkYsE(self, "No data found !", title=title)
 def VVjDGV(self, satCol, VVcpnp, title, txt, colList):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  sat = FF24qC(refCode, False)
  for ndx, row in enumerate(VVcpnp.VVGrbO()):
   if sat == row[satCol].strip():
    VVcpnp.VVtpKN(ndx)
    break
  else:
   FFD1yO(VVcpnp, "No listed !", 1500)
 def FFlX3B_SatellitesCleaner(self):
  satLst = nimmanager.getSatList()
  if not satLst:
   FFkYsE(self, "No Satellites found !")
   return
  usedSats = CCtSdI.VVeKoR()
  VVvhuK = []
  for sat in satLst:
   tunerLst = []
   for tuner, sats in usedSats:
    if sat in sats:
     tunerLst.append(tuner)
   tunerLst.sort()
   tuners = " , ".join(tunerLst) if tunerLst else ""
   posVal = sat[0]
   if posVal > 1800: posTxt = str(posVal - 3600)
   else   : posTxt = str(posVal)
   VVvhuK.append((sat[1], posTxt, FFUBZ6(sat[0]), tuners, str(posVal)))
  if VVvhuK:
   VVghPi = "#11222222"
   VVvhuK.sort(key=lambda x: int(x[1]))
   VV3th8 = ("Current Satellite" , BF(self.VVjDGV, 2) , [])
   VVOtSO = ("Options"   , self.VVIkwf  , [])
   header   = ("Satellite" , "Pos #" , "Position", "Tuners" , "posVal" )
   widths   = ( 50    , 10  , 10  , 30  , 0   )
   VVQqg2  = ( LEFT  , CENTER , CENTER , CENTER , CENTER )
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VV3th8=VV3th8, VVOtSO=VVOtSO, VVz2kc=VVghPi, VVwpZm=VVghPi, VVghPi=VVghPi, lastFindConfigObj=CFG.lastFindSatName)
  else:
   FFkYsE(self, "No data found !")
 def VVIkwf(self, VVcpnp, title, txt, colList):
  mSel = CCqgU8(self, VVcpnp)
  isMulti = VVcpnp.VVbl0M
  if isMulti : txt = "Remove ALL Services on %s Satellites" % FFkhYI(str(VVcpnp.VVMJsS()), VVMmz2)
  else  : txt = "Remove ALL Services on : %s" % FFkhYI(VVcpnp.VVPxSj()[0], VVMmz2)
  VV625J = []
  VV625J.append((txt, "deleteSat"))
  VV625J.append(VVm77t)
  VV625J.append(("Delete Empty Bouquets", "VVVmbR"))
  cbFncDict = { "deleteSat"   : BF(FFlX3B, VVcpnp, BF(self.VVguWD, VVcpnp))
     , "VVVmbR" : BF(self.VVVmbR, VVcpnp)
     }
  mSel.VVMNiz(VV625J, cbFncDict)
 def VVguWD(self, VVcpnp):
  posLst = []
  isMulti = VVcpnp.VVbl0M
  posLst = []
  if isMulti : posLst = VVcpnp.VVT6RH(4)
  else  : posLst = [VVcpnp.VVPxSj()[4]]
  nsLst = []
  for pos in posLst:
   nsLst.append(self.VVYdx1(pos))
  db = eDVBDB.getInstance()
  if db:
   for pos in posLst:
    db.removeServices(-1, -1, -1, int(pos))
  totCh, totBoq = self.VVptcF(nsLst)
  FFlB9k(True)
  FFNEkd(self, "Deleted Satellites:\n%d\n\nDeleted Services:\n%d\n\nCleaned Bouquets:\n%d" % (len(posLst), totCh, totBoq), title="Delete Satellites")
 def VVVmbR(self, winObj):
  title = "Delete Empty Bouquets"
  FFMIbO(self, BF(FFlX3B, winObj, BF(self.VVPEIf, title)), "Delete bouquets with no services ?", title=title)
 def VVPEIf(self, title):
  bList = CCgKdM.VVKEnt()
  bNames = []
  if bList:
   fList = []
   for bName, bRef in bList:
    bFile = CCgKdM.VVa7d3(bRef)
    bPath = VV609C + bFile
    FFX92w(bPath)
    bNames.append(bName)
    fList.append(bFile)
   if fList:
    for fil in ("bouquets.tv", "bouquets.radio"):
     path = VV609C + fil
     if fileExists(path):
      lines = FFjdnJ(path)
      newLines = []
      for line in lines:
       for bFile in fList:
        if bFile in line:
         break
       else:
        newLines.append(line)
      if newLines:
       with open(path, "w") as f:
        f.write("\n".join(newLines) + "\n")
   FFlB9k(True)
  if bNames: txt = "%s\n\n%s" % (FFkhYI("Deleted Bouquets:", VVoTT6), "\n".join(bNames))
  else  : txt = "No empty bouquets."
  FFNEkd(self, txt, title=title)
 def VVYdx1(self, pos):
  pos = int(pos.strip())
  if pos < 0:
   pos += 3600
  return ("%04x" % pos).upper()
 def VVptcF(self, nsLst):
  totCh = totBoq = 0
  files = iGlob("%suserbouquet.*.tv" % VV609C)
  for srcF in files:
   if fileExists(srcF):
    lines = FFjdnJ(srcF)
    newLines = []
    found = False
    for line in lines:
     span = iSearch(r"#SERVICE\s+((?:[A-Za-z0-9]+:){10})$", line, IGNORECASE)
     if span:
      ns = FFwYmz(span.group(1))
      if ns in nsLst:
       found = True
       totCh += 1
       continue
     newLines.append(line)
    if found and newLines:
     totBoq += 1
     with open(srcF, "w") as f:
      f.write("\n".join(newLines) + "\n")
  return totCh, totBoq
 def VVRmZg(self, title)   : self.VVDCdr(title, True)
 def VVykCs(self, title) : self.VVDCdr(title, False)
 def VVDCdr(self, title, isWithPIcons):
  piconsPath = CCrs3r.VVsNIk()
  if pathExists(piconsPath):
   totalPicons = 0
   for fName, fType in CCrs3r.VVI7Ry(piconsPath):
    if fName:
     totalPicons +=1
   if totalPicons > 0:
    VVvhuK, err = CCtSdI.VV4uiY(self, self.VVtZVs)
    if VVvhuK:
     channels = []
     for (chName, chProv, sat, refCode) in VVvhuK:
      fName = refCode.replace(":", "_") + ".png"
      pFile = FFKhVc(piconsPath, fName)
      if isWithPIcons:
       if pFile:
        channels.append((chName, chProv, sat, refCode))
      else:
       if not pFile:
        channels.append((chName, chProv, sat, refCode))
     totalServices = len(VVvhuK)
     totalFound  = len(channels)
     if isWithPIcons:
      totalWithPIcons  = totalFound
      totalMissingPIcons = totalServices - totalWithPIcons
     else:
      totalMissingPIcons = totalFound
      totalWithPIcons  = totalServices - totalMissingPIcons
     def VVQQs4(key, val):
      return "%s\t\t: %s\n" % (key, str(val))
     txt = ""
     txt += VVQQs4("PIcons Path"  , piconsPath)
     txt += VVQQs4("Total PIcons" , totalPicons)
     txt += "\n"
     txt += VVQQs4("Total services" , totalServices)
     txt += VVQQs4("With PIcons"  , totalWithPIcons)
     txt += VVQQs4("Missing PIcons" , totalMissingPIcons)
     if totalFound == 0:
      FFNEkd(self, txt)
     else:
      VV01dN     = (""      , self.VVeoF7 , [])
      if isWithPIcons : VV1QO7 = ("Export Current PIcon", self.VVkRsd  , [])
      else   : VV1QO7 = None
      VVOtSO     = ("Statistics", FFNEkd, [txt])
      VVVHmY      = ("Zap", self.VVw34P, [])
      channels.sort(key=lambda x: x[0].lower())
      self.VVgAkX(title, channels, VVVHmY=VVVHmY, VV01dN=VV01dN, VVOtSO=VVOtSO, VV1QO7=VV1QO7)
   else:
    FFkYsE(self, "No picons found in path:\n\n%s" % piconsPath)
  else:
   FFkYsE(self, "PIcons path not found.\n\n%s" % piconsPath)
 def VVeoF7(self, VVcpnp, title, txt, colList):
  chName = colList[0]
  refCode = colList[3]
  txt  = "%s\n\n%s" % (title, txt)
  FFBatl(self, fncMode=CCARMv.VV4ZrS, refCode=refCode, chName=chName, text=txt)
 def VVkRsd(self, VVcpnp, title, txt, colList):
  png, path = CCrs3r.VVByZr(colList[3], colList[0])
  if path:
   CCrs3r.VVNsL7(self, png, path)
 @staticmethod
 def VVQokV():
  VVXBRO  = "%slamedb" % VV609C
  VVMxmb = "%slamedb.disabled" % VV609C
  return VVXBRO, VVMxmb
 @staticmethod
 def VVcCgD():
  VVsSZg  = "%slamedb5" % VV609C
  VV0E2X = "%slamedb5.disabled" % VV609C
  return VVsSZg, VV0E2X
 def VVL3U6(self, isEnable):
  VVXBRO, VVMxmb = CCtSdI.VVQokV()
  if isEnable and not fileExists(VVMxmb):
   FFewCE(self, "Aready enabled.")
  elif not isEnable and not fileExists(VVXBRO):
   FFkYsE(self, "LameDB File not found!")
  else:
   if isEnable : word = "Enable"
   else  : word = "Disable"
   FFMIbO(self, BF(self.VV9JYP, isEnable), "%s Hidden Channels ?" % word)
 def VV9JYP(self, isEnable):
  VVXBRO , VVMxmb = CCtSdI.VVQokV()
  VVsSZg, VV0E2X = CCtSdI.VVcCgD()
  cmd = ""
  if isEnable:
   word = "Enabled"
   cmd += "if [ -f '%s' ]; then mv -f '%s' '%s'; fi;"   % (VVMxmb, VVMxmb, VVXBRO)
   cmd += "if [ -f '%s' ]; then mv -f '%s' '%s'; fi;"   % (VV0E2X, VV0E2X, VVsSZg)
  else:
   word = "Disabled"
   cmd += "if [ -f '%s' ]; then cp '%s' '%s'; fi;"    % (VVXBRO  , VVXBRO , VVMxmb)
   cmd += "if [ -f '%s' ]; then cp '%s' '%s'; fi;"    % (VVsSZg , VVsSZg, VV0E2X)
   cmd += "if [ -f '%s' ]; then sed -i 's/,f:2//' '%s'; fi;" % (VVMxmb, VVXBRO )
   cmd += "if [ -f '%s' ]; then sed -i 's/,f:2//' '%s'; fi;" % (VV0E2X, VVsSZg)
  res = os.system(cmd)
  FFlB9k()
  if res == 0 : FFewCE(self, "Hidden List %s" % word)
  else  : FFkYsE(self, "Error while restoring:\n\n%s" % fileName)
 def VVCmak(self):
  cmd = ""
  cmd += "echo -e 'Reading current settings ...';"
  cmd += "cat %ssettings | grep -v 'config.ParentalControl' > /tmp/settings_my_tmp.txt;" % VV609C
  cmd += "echo -e 'Applying new settings ...';"
  cmd += "mv /tmp/settings_my_tmp.txt %ssettings" % VV609C
  FFRi75(self, cmd)
 def VVY0HL(self):
  VVXBRO, err = CCtSdI.VVR3Wk(self)
  if err:
   return
  tmpFile = "/tmp/ajpanel_lamedb"
  FFX92w(tmpFile)
  totChan = totRemoved = 0
  lines = FFjdnJ(VVXBRO, keepends=True)
  with open(tmpFile, "w") as f:
   servFound = False
   servLines = []
   for line in lines:
    if servFound:
     if line.strip() == "end":
      f.write(line)
      break
     else:
      servLines.append(line)
      if len(servLines) == 3:
       if len(servLines[1].strip()) > 0:
        totChan += 1
        f.write(servLines[0])
        f.write(servLines[1])
        f.write(servLines[2])
       else:
        totRemoved += 1
       servLines = []
    else:
     f.write(line)
     if line.strip() == "services":
      servFound = True
  if totRemoved:
   FFMIbO(self, BF(FFlX3B, self, BF(self.VVI1Lf, tmpFile, VVXBRO, totRemoved, totChan))
      , "Delete %d servce%s (out of %d service%s) ?" % (totRemoved, FFICXm(totRemoved), totChan, FFICXm(totChan))
      , callBack_No=BF(self.VVX22c, tmpFile))
  else:
   FFNEkd(self, "Total Channels\t: %d\nWith no names\t: %d" % (totChan, totRemoved))
 def VVI1Lf(self, tmpFile, VVXBRO, totRemoved, totChan):
  os.system(FFxtg8("mv -f '%s' '%s'" % (tmpFile, VVXBRO)))
  FFlB9k()
  FFNEkd(self, "Total Channels\t: %d\nTotal Removed\t: %d" % (totChan, totRemoved))
 def VVX22c(self, tmpFile):
  FFX92w(tmpFile)
 @staticmethod
 def VVR3Wk(SELF, VVDUH8=True, title=""):
  VVXBRO, VVMxmb = CCtSdI.VVQokV()
  if   not fileExists(VVXBRO)       : err = "File not found !\n\n%s" % VVXBRO
  elif not CC7ujK.VV4HLe(SELF, VVXBRO) : err = "'lamedb' file is not in 'UTF-8' Encoding !"
  else             : err = ""
  if err and VVDUH8:
   FFkYsE(SELF, err, title=title)
  return VVXBRO, err
 @staticmethod
 def VVlSbc(refCode):
  _, flg, _, _, tsid, nid, ns, _, _, _ = refCode.rstrip(":").split(":")
  if flg == "0": return (":".join([ns.zfill(8), tsid.zfill(4), nid.zfill(4)])).upper()
  else   : return ""
 @staticmethod
 def VVVxzN(refCode):
  _, flg, st, sid, tsid, nid, ns, _, _, _ = refCode.rstrip(":").split(":")
  if flg == "0": return (":".join([sid.zfill(4), ns.zfill(8), tsid.zfill(4), nid.zfill(4), str(int(st, 16)), "0", "0"])).upper()
  else   : return ""
 @staticmethod
 def VVLZZO(servTypes):
  VVYHZX  = eServiceCenter.getInstance()
  VVIYgT   = '%s ORDER BY name' % servTypes
  VVd39g   = eServiceReference(VVIYgT)
  VVX4Uz = VVYHZX.list(VVd39g)
  if VVX4Uz: return VVX4Uz.getContent("CN", False)
  else     : return []
 @staticmethod
 def VVeKoR():
  slotSats = []
  for slot in nimmanager.nim_slots:
   if slot.frontend_id is not None:
    lst = nimmanager.getSatListForNim(slot.frontend_id)
    if lst:
     slotSats.append((slot.getSlotName(), lst))
  return slotSats
class CCARMv(Screen):
 VVTlHJ  = 0
 VVHFwt   = 1
 VVyj5y   = 2
 VV4ZrS    = 3
 VVae7k    = 4
 VVRYNT   = 5
 VVLgSX   = 6
 VVxAjd    = 7
 VVcpeX   = 8
 VVEaIm   = 9
 VViZAY   = 10
 VV3BDs   = 11
 def __init__(self, session, **kwargs):
  self.skin, self.skinParam = FF896P(VVhfwD, 1400, 800, 50, 30, 20, "#05001921", "#05001921", 30, addFramedPic=True)
  self.session  = session
  self.fncMode  = kwargs.get("fncMode"  , self.VVTlHJ)
  self.callingSELF = kwargs.get("callingSELF" , None)
  self.info   = kwargs.get("info"   , None)
  self.refCode  = kwargs.get("refCode"  , "")
  self.decodedUrl  = kwargs.get("decodedUrl" , "")
  self.origUrl  = kwargs.get("origUrl"  , "")
  self.iptvRef  = kwargs.get("iptvRef"  , "")
  self.chName   = kwargs.get("chName"  , "")
  self.prov   = kwargs.get("prov"   , "")
  self.state   = kwargs.get("state"  , "")
  self.portalMode  = kwargs.get("portalMode" , "")
  self.portalHost  = kwargs.get("portalHost" , "")
  self.portalMac  = kwargs.get("portalMac" , "")
  self.catID   = kwargs.get("catID"  , "")
  self.stID   = kwargs.get("stID"   , "")
  self.chNum   = kwargs.get("chNum"  , "")
  self.chCm   = kwargs.get("chCm"   , "")
  self.serCode  = kwargs.get("serCode"  , "")
  self.serId   = kwargs.get("serId"  , "")
  self.picUrl   = kwargs.get("picUrl"  , "")
  self.picPath  = kwargs.get("picPath"  , "")
  self.text   = kwargs.get("text"   , "")
  self.epg   = kwargs.get("epg"   , "")
  self.chUrl   = kwargs.get("chUrl"  , "")
  self.isIptv   = kwargs.get("isIptv"  , False)
  self.piconShown  = False
  self.Sep   = FFkhYI("%s\n", VVjrAG) % VVZ1aI
  self.picViewer  = None
  FFJd2Z(self, title="Service Info.", addScrollLabel=True)
  self["myAction"].actions.update({ "info": self.VV0Tyq })
  self["myPicF"]  = Label()
  self["myPicB"]  = Label()
  self["myPic"]  = Pixmap()
  self["myPicF"].hide()
  self["myPicB"].hide()
  self["myPic"].hide()
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self["myLabel"].VVqCbn(outputFileToSave="chann_info")
  if   self.fncMode == self.VVTlHJ : fnc = self.VViNoY
  elif self.fncMode == self.VVHFwt  : fnc = self.VViNoY
  elif self.fncMode == self.VVyj5y  : fnc = self.VViNoY
  elif self.fncMode == self.VV4ZrS  : fnc = self.VVus0L
  elif self.fncMode == self.VVae7k  : fnc = self.VVNiPj
  elif self.fncMode == self.VVRYNT  : fnc = self.VVy6LM
  elif self.fncMode == self.VVLgSX  : fnc = self.VVkn5e
  elif self.fncMode == self.VVxAjd  : fnc = self.VVeBKK
  elif self.fncMode == self.VVcpeX  : fnc = self.VVFtXN
  elif self.fncMode == self.VVEaIm : fnc = self.VVCiQS
  elif self.fncMode == self.VViZAY  : fnc = self.VVdpKh
  elif self.fncMode == self.VV3BDs : fnc = self.VV8lJm
  self["myLabel"].setText("\n   Reading Info ...")
  FFpoMu(fnc)
 def onExit(self):
  if self.picViewer:
   self.picViewer.VVq3PH()
 def VVMIxh(self, err):
  self["myLabel"].setText(err)
  FFobAA(self["myTitle"], "#22200000")
  FFobAA(self["myBody"], "#22200000")
  self["myLabel"].VVtRDN("#22200000")
  self["myLabel"].VVw0Hf()
 def VViNoY(self):
  try:
   dum = self.session
  except:
   return
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  self.refCode = refCode
  self.VVlKZX(chName)
 def VVus0L(self):
  self.VVlKZX(self.chName)
 def VVNiPj(self):
  self.VVlKZX(self.chName)
 def VVy6LM(self):
  self.VVlKZX(self.chName)
 def VVkn5e(self):
  self.VVlKZX("Picon Info")
 def VVeBKK(self):
  self.VVlKZX(self.chName)
 def VVFtXN(self):
  self.VVlKZX(self.chName)
 def VVCiQS(self):
  self.VVlKZX(self.chName)
 def VVdpKh(self):
  self.chUrl = self.refCode + self.callingSELF.VV5dEp(self.portalMode, self.chCm, self.serCode, self.serId)
  self.VVlKZX(self.chName)
 def VV8lJm(self):
  self.VVlKZX(self.chName)
 def VVlKZX(self, title):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state, info = FFnQlZ(self, addInfoObj=True)
  if info and refCode.rstrip(":") == self.refCode.rstrip(":"):
   self.text  = self.VVWKam(info, refCode, decodedUrl, origUrl, iptvRef, chName, prov, state)
   self.info  = info
   self.refCode = refCode
   self.decodedUrl = decodedUrl
   self.origUrl = origUrl
   self.iptvRef = iptvRef
   self.chName  = chName
   self.prov  = prov
   self.state  = state
   self.isIptv  = len(iptvRef) > 0
  else:
   tUrl = self.decodedUrl or self.iptvRef or self.chUrl
   if tUrl:
    if not self.text.endswith("\n"):
     self.text += "\n"
    self.text += "\nURL:\n%s\n" % FFkhYI(self.VVd1A3(tUrl), VVkXS4)
  if not self.epg:
   epg = self.VVKDzk(self.info, self.refCode)
   if epg:
    self.epg = epg
    self.text += self.epg
  if not self.piconShown and self.picPath:
   self.piconShown = self.VV2DIK(self.picPath)
  if not self.piconShown and self.refCode and self.chName:
   png, path = CCrs3r.VVByZr(self.refCode, self.chName)
   if png:
    self.picPath = path
    self.piconShown = self.VV2DIK(path)
  self.VV7hCO()
  self.VVTkI8()
  self["myLabel"].setText(self.text or "   No active service", VVKsoz=VV72id)
  if self["myPicF"].getVisible() : minH = self["myPicF"].instance.size().height()
  else       : minH = 0
  self["myLabel"].VVw0Hf(minHeight=minH)
 def VVTkI8(self):
  url = max([self.refCode, self.chUrl, self.iptvRef], key=len)
  if not FFuZb6(url):
   return
  url = url.replace("%3a", ":").replace("%3A", ":")
  span = iSearch(r"((?:[A-Fa-f0-9]+[:]){10})(.+)", url, IGNORECASE)
  if span:
   self.refCode = span.group(1).upper().rstrip(":")
   url    = span.group(2)
  if "?" in url:
   url = url[:url.index("?")]
  epg, picUrl, err = self.VVuPEf(FF9CmS(url))
  if epg:
   self.text += "\n" + FFINY2("EPG:", VVoTT6) + epg
  if picUrl:
   self.picUrl = picUrl
   self.VV7hCO()
 def VV7hCO(self):
  if not self.piconShown and self.picUrl:
   path, err = FF913T(self.picUrl, "ajpanel_tmp.png", timeout=2, mustBeImage=True)
   if path:
    self.piconShown = self.VV2DIK(path)
    if self.piconShown and self.refCode:
     self.VVN3a1(path, self.refCode)
 def VVN3a1(self, path, refCode):
  if path and fileExists(path) and os.system(FFxtg8("which ffmpeg")) == 0:
   pPath = CCrs3r.VVsNIk()
   if pathExists(pPath):
    picon = refCode.replace(":", "_").rstrip("_") + ".png"
    cmd = CCARMv.VVc7qU(path)
    cmd += FFxtg8("mv -f '%s' '%s%s'" % (path, pPath, picon)) + ";"
    os.system(cmd)
 def VV2DIK(self, path):
  if path and fileExists(path):
   err, w, h = self.VVCtNl(path)
   if not err:
    if h > w:
     self.VVA6nB(self["myPicF"], w, h, True)
     self.VVA6nB(self["myPicB"], w, h, False)
     self.VVA6nB(self["myPic"] , w, h, False)
   self.picViewer = CCg2mT.VVjTx0(self["myPic"], path)
   if self.picViewer:
    self["myPicF"].show()
    self["myPicB"].show()
    self["myPic"].show()
    return True
  return False
 def VVA6nB(self, obj, picW, picH, isFrame):
  w  = obj.instance.size().width()
  pos  = obj.getPosition()
  left = pos[0]
  top  = pos[1]
  newW = obj.instance.size().width() * 0.6
  newH = newW * picH / picW
  if isFrame:
   newW += 2
  obj.instance.resize(eSize(*(int(newW), int(newH))))
  obj.instance.move(ePoint(int(left + int(w - newW)), int(top)))
 def VVCtNl(self, path):
  cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=X:p=0 '%s' 2> /dev/null" % path
  res = FFj4HH(cmd)
  if "X" in res:
   w, h = res.split("X")
   if w.isdigit() and h.isdigit() : return "", int(w), int(h)
   else       : return res, -1, -1
  else:
   return res, -1, -1
 def VVWKam(self, info, refCode, decodedUrl, origUrl, iptvRef, chName, prov, state):
  txt = ""
  txt += "Service Name\t: %s\n" % FFkhYI(chName, VVoTT6)
  txt += self.VVQQs4(info, "Provider"     , iServiceInformation.sProvider     )
  if state:
   if not state == "Tuned":
    state = FFkhYI(state, VVU8eD)
   txt += "State\t: %s\n" % state
  w = FFAkN7(info       , iServiceInformation.sVideoWidth    ) or -1
  h = FFAkN7(info       , iServiceInformation.sVideoHeight    ) or -1
  if w != -1 and h != -1:
   txt += "Dimensions\t: %s x %s\n" % (w, h)
  aspect = self.VVyWJl(info)
  if aspect:
   txt += "Video Format\t: %s\n" % aspect
  txt += self.VVQQs4(info, "Video Type"    , iServiceInformation.sVideoType  , 4  )
  txt += self.VVQQs4(info, "Frame Rate"    , iServiceInformation.sFrameRate  , 5  )
  txt += self.VVQQs4(info, "Crypted"     , iServiceInformation.sIsCrypted  , 3  )
  tot = self.VV6BNm()
  if tot > -1: txt += "Audio Tracks\t: %d\n" % tot
  tot = self.VVBJ0U()
  if tot > -1: txt += "Subtitles\t: %d\n" % tot
  fPath, fDir, fName, picFile = CCARMv.VVglzz(self)
  isLocal = False
  isIptv  = len(iptvRef) > 0
  if isIptv:
   txt += "Service Type\t: %s\n" % FFkhYI("IPTV", VVpHwQ)
   txt += self.VVk9v6(iptvRef)
  elif fPath:
   isLocal = True
   txt += "Reference\t: %s\n" % ":".join(refCode.split(":")[:10])
   txt += "Service Type\t: Local Recording\n"
   txt += "Directory\t: %s\n" % fDir
   if picFile and fileExists(picFile):
    self.picPath = picFile
  elif refCode:
   txt += "Reference\t: %s\n" % refCode
  if not isLocal:
   txt += "\n"
   txt += self.VVHUQG(refCode, iptvRef, chName)
  if not isLocal and not isIptv:
   txt += "\n"
   txt += self.Sep
   namespace = None
   if refCode:
    tp = CCX8JT()
    tpTxt, namespace = tp.VVfPTk(refCode)
    if tpTxt:
     txt += FFkhYI("Tuner:\n", VVoTT6)
     txt += tpTxt
     txt += "\n"
     txt += self.Sep
   txt += FFkhYI("Codes:\n", VVoTT6)
   if namespace: txt += "Namespace\t: %s\n" % namespace
   else  : txt += self.VVQQs4(info, "Namespace" , iServiceInformation.sNamespace  , 1, 8 )
   txt += self.VVQQs4(info, "Video PID"    , iServiceInformation.sVideoPID   , 2, 4 )
   txt += self.VVQQs4(info, "Audio PID"    , iServiceInformation.sAudioPID   , 2, 4 )
   txt += self.VVQQs4(info, "PCR PID"     , iServiceInformation.sPCRPID   , 2, 4 )
   txt += self.VVQQs4(info, "PMT PID"     , iServiceInformation.sPMTPID   , 2, 4 )
   txt += self.VVQQs4(info, "TXT PID"     , iServiceInformation.sTXTPID   , 2, 4 )
   txt += self.VVQQs4(info, "SID"      , iServiceInformation.sSID    , 2, 4 )
   txt += self.VVQQs4(info, "ONID"      , iServiceInformation.sONID    , 2, 4 )
   txt += self.VVQQs4(info, "TSID"      , iServiceInformation.sTSID    , 2, 4 )
  return txt
 @staticmethod
 def VVyWJl(info):
  if info:
   aspect = FFAkN7(info, iServiceInformation.sAspect)
   if aspect.isdigit():
    aspect = int(aspect)
    if aspect in ( 1, 2, 5, 6, 9, 0xA, 0xD, 0xE ) : return "4:3"
    else           : return "16:9"
  return ""
 def VVQQs4(self, info, name, what, mode=0, digits=0):
  tab = "\t"
  txt = str(FFAkN7(info, what))
  if len(txt) > 0:
   try  : hexVal = hex(int(txt))[2:].upper()
   except : hexVal = ""
   if digits > 0:
    hexVal = hexVal.zfill(digits)
   if   mode == 1     : txt = hexVal
   elif mode == 2     : txt = "%s\tdec: %s" % (hexVal, txt)
   elif mode == 3     : txt = "Yes" if txt=="1" else "No"
   elif mode == 4     : txt = self.VVbvZX(txt)
   elif mode == 5 and txt.isdigit(): txt = str(int(txt)/1000)
   if txt : return "%s%s: %s\n" % (name, tab, txt)
   else : return ""
  else:
   return ""
 def VVbvZX(self, sVideoType):
  codec_data = { -1: "", 0: "MPEG-2", 1: "H.264 (MPEG-4 AVC)", 2: "H.263", 3: "VC1", 4: "MPEG-4 (VC)", 5: "VC1-SM", 6: "MPEG-1", 7: "H.265 (HEVC)", 8: "VP8", 9: "VP9", 10: "XVID", 11: "11", 12: "12", 13: "DIVX 3.11", 14: "DIVX 4", 15: "DIVX 5", 16: "AVS", 17: "17", 18: "VP6", 19: "19", 20: "20", 21: "SPARK" }
  return codec_data.get(int(sVideoType), "")
 def VV6BNm(self):
  try:
   return self.session.nav.getCurrentService().audioTracks().getNumberOfTracks() or 0
  except:
   return -1
 def VVBJ0U(self):
  try:
   return len(InfoBar.instance.getCurrentServiceSubtitle().getSubtitleList())
  except:
   return -1
 def VVHUQG(self, refCode, iptvRef, chName):
  refCode = FFcJ7o(refCode, iptvRef, chName)
  if not refCode:
   return self.Sep + "Bouquet\t: -\n"
  fList = []
  txt = FFqD66(VV609C + "bouquets.tv")
  list =  iFindall(r"(userbouquet[.].*[.]tv)", txt, IGNORECASE)
  if list: fList += list
  txt = FFqD66(VV609C + "bouquets.radio")
  list =  iFindall(r"(userbouquet[.].*[.]radio)", txt, IGNORECASE)
  if list: fList.extend(list)
  VVvytR = []
  tmpRefCode = FF9CmS(refCode)
  for item in fList:
   path = VV609C + item
   if fileExists(path):
    txt = FFqD66(path)
    if tmpRefCode in FF9CmS(txt):
     span = iSearch(r"#NAME\s+(.*)", txt, IGNORECASE)
     if span : bName = span.group(1)
     else : bName = "[ No Name ]"
     VVvytR.append((bName, os.path.basename(path)))
  txt = self.Sep
  if VVvytR:
   if len(VVvytR) == 1:
    txt += "%s\t: %s%s\n" % (FFkhYI("Bouquet", VVoTT6), VVvytR[0][0], " (%s)" % VVvytR[0][1] if VVF5vz else "")
   else:
    txt += FFkhYI("Bouquets:\n", VVoTT6)
    for ndx, item in enumerate(VVvytR):
     txt += "%d- %s%s\n" % (ndx + 1, item[0].strip(), " (%s)" % item[1] if VVF5vz else "")
  else:
   txt += "Bouquet\t: -\n"
  return txt
 def VVKDzk(self, info, refCode):
  epg = ""
  if info:
   for evNum in range(2):
    try:
     event = info.getEvent(evNum)
     epg += self.VVz5T0(event, evNum)
    except:
     pass
  elif refCode:
   service = eServiceReference(refCode)
   if service:
    try:
     from enigma import eEPGCache
     eCache = eEPGCache.getInstance()
     if eCache:
      for evNum in range(2):
       event = eCache.lookupEventTime(service, -1, evNum)
       epg += self.VVz5T0(event, evNum)
    except:
     pass
    if not epg:
     try:
      info = eServiceCenter.getInstance().info(service)
      if info:
       event = info.getEvent(service)
       epg += self.VVz5T0(event, 0)
     except:
      pass
  return epg
 def VVz5T0(self, event, evNum):
  txt = ""
  if event:
   evName, evTime, evDur, evShort, evDesc, genre, PR = CCARMv.VVVxH9(event)
   if any([evName, evShort, evDesc, evTime, evDur]):
    lang = CFG.epgLanguage.getValue()
    evNameTransl = ""
    if not lang == "off":
     sep = "\nx\nx\nx\n"
     res = CCARMv.VVb9IC(evName + sep + evShort + sep + evDesc)
     if res.count(sep) >= 2:
      res = res.split(sep)
      evNameT = res[0]
      evShort = res[1]
      evDesc = res[2]
      if evName and not evName == evNameT:
       evNameTransl = evNameT
    if evName          : txt += "Name\t: %s\n"   % FFkhYI(evName, VVoTT6)
    if evNameTransl         : txt += "Name (%s)\t: %s\n" % (lang.upper(), FFkhYI(evNameTransl, VVoTT6))
    if evTime           : txt += "Start Time\t: %s\n" % FFcgMH(evTime)
    if evTime and evDur        : txt += "End Time\t: %s\n"  % FFcgMH(evTime + evDur)
    if evDur           : txt += "Duration\t: %s\n"  % FF3UDS(evDur)
    if evTime and evDur        :
     now = int(iTime())
     if   now > evTime and now < evTime + evDur : txt += "Remaining\t: %s\n" % FF3UDS(evTime + evDur - now)
     elif now < evTime        : txt += "Starts in\t: %s\n" % FF3UDS(evTime - now)
    if genre          : txt += "Genre\t: %s\n"  % genre
    if PR           : txt += "PC Rating\t: %s\n" % PR
    evShort = str(evShort)
    if evShort           : txt += "\nSummary:\n%s\n"  % FFkhYI(evShort, VVNTmM)
    if evDesc and evDesc.strip()     : txt += "\nDescription:\n%s\n" % FFkhYI(evDesc , VVNTmM)
    if txt:
     txt = FFkhYI("\n%s\n%s Event:\n%s\n" % (VVZ1aI, ("Current", "Next")[evNum], VVZ1aI), VVoTT6) + txt
  return txt
 def VVk9v6(self, refCode):
  refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(refCode)
  if decodedUrl:
   txt = "Reference\t: %s\n" % refCode
   p = CCyIre()
   valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(decodedUrl)
   del p
   if host : txt += "Portal Host\t: %s\n" % host
   if mac : txt += "Portal MAC\t: %s\n" % mac
   if mode : txt += "Portal Mode\t: %s\n" % mode.upper()
   txt += "\n"
   txt += FFkhYI("URL:", VVpHwQ) + "\n%s\n" % self.VVd1A3(decodedUrl)
  else:
   txt = "\n"
   txt += FFkhYI("Reference:", VVpHwQ) + "\n%s\n" % refCode
  return txt
 def VVd1A3(self, url):
  span = iSearch(r"(?:[A-Fa-f0-9]+[:]){10}(.+)", url, IGNORECASE)
  if span:
   url = span.group(1)
  if not VVPJLC:
   url = iSub(r"[&?]mode=.+end=", r"", url, flags=IGNORECASE)
  return url.replace("%3a", ":").replace("%3A", ":").strip()
 def VVuPEf(self, decodedUrl):
  if not FFINsi():
   return "", "", "No internet connection !"
  uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(decodedUrl)
  if not all([uHost, uUser, uPass, uId]):
   return "", "", "No EPG (invalid ULR) !"
  qUrl = "%s/player_api.php?username=%s&password=%s&action=" % (uHost, uUser, uPass)
  if   uType == "live" : qUrl += "get_simple_data_table&stream_id=%s" % (uId)
  elif uType == "movie" : qUrl += "get_vod_info&vod_id=%s" % (uId)
  elif uType == "series" : return "", "", "No EPG for Series Channels !"
  txt, err = CCqQHV.VVpi8S(qUrl, timeout=1)
  tDict = {}
  if err:
   return "", "", "No EPG from server (%s)" % err
  else:
   try:
    tDict = jLoads(txt)
   except:
    pass
   if not tDict:
    return "", "", "Could not parse server data !"
  epg = picUrl = ""
  if tDict:
   if   uType == "live" : epg = self.VVl87q(tDict)
   elif uType == "movie" : epg, picUrl = CCARMv.VVEOl4(tDict)
  err = "" if epg else "No EPG from server !"
  return epg, picUrl, err
 def VVl87q(self, tDict):
  epg = lang = ""
  if "epg_listings" in tDict:
   try:
    evNum = 1
    for item in tDict["epg_listings"]:
     tTitle    = CCqQHV.VVvsIK(item, "title"    , is_base64=True )
     lang    = CCqQHV.VVvsIK(item, "lang"         ).upper()
     description   = CCqQHV.VVvsIK(item, "description"  , is_base64=True ).replace("\n", " .. ")
     start_timestamp  = CCqQHV.VVvsIK(item, "start_timestamp" , isDate=True  )
     start_timestamp_unix= CCqQHV.VVvsIK(item, "start_timestamp"      )
     stop_timestamp  = CCqQHV.VVvsIK(item, "stop_timestamp"  , isDate=True  )
     stop_timestamp_unix = CCqQHV.VVvsIK(item, "stop_timestamp"       )
     now_playing   = CCqQHV.VVvsIK(item, "now_playing"       )
     skip = False
     try:
      if float(stop_timestamp_unix) < iTime():
       skip = True
     except:
      pass
     if not skip:
      if now_playing == "0": color, txt = VVZgqQ, ""
      else     : color, txt = VVU8eD , "    (CURRENT EVENT)"
      epg += FFkhYI("_" * 32 + "\n", VVjrAG)
      epg += FFkhYI("Event\t: %d%s\n" % (evNum, txt), color)
      epg += "Start\t: %s\n"   % start_timestamp
      epg += "End\t: %s\n"   % stop_timestamp
      epg += "Title\t: %s\n"   % tTitle
      if description : epg += "Description:\n%s\n" % FFkhYI(description, VVkXS4)
      else   : epg += "Description\t: - \n"
      evNum += 1
     try:
      start  = int(start_timestamp_unix)
      dur   = int(int(stop_timestamp_unix) - int(start_timestamp_unix))
      shortDesc = ("Language : %s" % lang) if lang else ""
      totEv, totOK = self.VVbwY9(self.refCode, [(start, dur, tTitle, shortDesc, description, 1)])
     except:
      pass
   except:
    pass
  if lang:
   epg = "Language\t: %s\n\n%s" % (lang.capitalize(), epg)
  return epg
 @staticmethod
 def VVEOl4(tDict):
  epg = movie_image = ""
  if "info" in tDict:
   try:
    item = tDict["info"]
    movie_image = CCqQHV.VVvsIK(item, "movie_image" )
    genre  = CCqQHV.VVvsIK(item, "genre"   ) or "-"
    plot  = CCqQHV.VVvsIK(item, "plot"   ) or "-"
    cast  = CCqQHV.VVvsIK(item, "cast"   ) or "-"
    rating  = CCqQHV.VVvsIK(item, "rating"   ) or "-"
    director = CCqQHV.VVvsIK(item, "director"  ) or "-"
    releasedate = CCqQHV.VVvsIK(item, "releasedate" ) or "-"
    duration = CCqQHV.VVvsIK(item, "duration"  ) or "-"
    try:
     lang = CCqQHV.VVvsIK(tDict["info"]["audio"]["tags"], "language")
     if lang:
      epg += "Language\t: %s\n" % lang.capitalize()
    except:
     pass
    epg += "Genre\t: %s\n"   % genre
    epg += "Released\t: %s\n"  % releasedate
    epg += "Duration\t: %s\n"  % duration
    epg += "Director\t: %s\n"  % director
    epg += "Rating\t: %s\n\n"  % rating
    epg += "Cast:\n%s\n\n"   % FFkhYI(cast, VVkXS4)
    epg += "Plot:\n%s"    % FFkhYI(CCARMv.VVb9IC(plot), VVkXS4)
   except:
    pass
  return epg, movie_image
 @staticmethod
 def VVb9IC(evTxt):
  lang = CFG.epgLanguage.getValue()
  if lang == "off":
   return evTxt
  else:
   txt, err = CCARMv.VVhFBe(evTxt, lang)
   return CCARMv.VVL3K6(txt).strip() or evTxt
 def VV0Tyq(self):
  if VVPJLC:
   def VVQQs4(key, val):
    return "%s= %s\n" % (key.ljust(12), val)
   txt = ""
   refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
   n = ("refCode" , "decodedUrl" , "origUrl" , "iptvRef" , "chName" , "prov", "state" )
   v = (refCode , decodedUrl , origUrl , iptvRef , chName , prov , state  )
   for i in range(len(n)):
    txt += VVQQs4(n[i], v[i])
   if "chCode" in iptvRef:
    p = CCyIre()
    valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(decodedUrl)
    n = ("valid", "ph1" , "playHost", "mode", "host", "mac" , "epNum" , "epId", "chCm", "query" )
    v = (valid , ph1 , playHost , mode , host , mac , epNum  , epId , chCm , query  )
    for i in range(len(n)):
     txt += VVQQs4(n[i], v[i])
   path = "/tmp/ajp_channel_details"
   with open(path, "a") as f:
    f.write("%s\n%s\n" % (VVZ1aI, txt))
   FFD1yO(self, "Saved to : %s" % path, 1000)
 @staticmethod
 def VVL3K6(txt):
  try:
   import html.parser
   return html.parser.HTMLParser().unescape(txt)
  except:
   pass
  try:
   import html.parser
   return html.parser.HTMLParser().unescape(txt)
  except:
   pass
  try:
   import html
   return html.unescape(txt)
  except:
   pass
  return txt
 @staticmethod
 def VVocQO(SELF):
  serv = SELF.session.nav.getCurrentlyPlayingServiceReference()
  if serv:
   try:
    from enigma import eEPGCache
    eCache = eEPGCache.getInstance()
    if eCache:
     event = eCache.lookupEventTime(serv, -1, 0)
     if event: return CCARMv.VVVxH9(event)
   except Exception as e:
    pass
   try:
    info = serv and eServiceCenter.getInstance().info(serv)
    event = info and info.getEvent(serv)
    if event: return CCARMv.VVVxH9(event)
   except:
    pass
  return [""] * 7
 @staticmethod
 def VVVxH9(event):
  evName = event.getEventName().strip()    or ""
  evTime = event.getBeginTime()      or ""
  evDur = event.getDuration()      or ""
  evShort = event.getShortDescription().strip()  or ""
  evDesc = event.getExtendedDescription().strip() or ""
  genre, PR = CCARMv.VVT08j(event)
  return evName, evTime, evDur, evShort, evDesc, genre, PR
 @staticmethod
 def VV0teF(refCode):
  service = eServiceReference(refCode)
  evLst = []
  if service:
   try:
    from enigma import eEPGCache
    eCache = eEPGCache.getInstance()
    if eCache:
     for evNum in range(2):
      event = eCache.lookupEventTime(service, -1, evNum)
      evName, evTime, evDur, evShort, evDesc, genre, PR = CCARMv.VVVxH9(event)
      evEnd = evPos = evRem = evCom = 0
      evTimeTxt = evPosTxt = evDurTxt = evEndTxt = evRemTxt = evComTxt = ""
      if evTime and evDur:
       evEnd = evTime + evDur
       evTimeTxt = FFcgMH(evTime)
       evEndTxt  = FFcgMH(evEnd)
       evDurTxt  = FF3UDS(evDur)
       now = int(iTime())
       if now > evTime and now < evEnd:
        evPos = now - evTime
        evPosTxt = FF3UDS(evPos)
        evRem = evEnd - now
        evRemTxt = FF3UDS(evRem)
       elif now < evTime:
        evCom = evTime - now
        evComTxt = FF3UDS(evCom)
      evLst.append((evName, evShort, evDesc, genre, PR, evTime, evTimeTxt, evDur, evDurTxt, evEnd, evEndTxt, evPos, evPosTxt, evRem, evRemTxt, evCom, evComTxt))
   except Exception as e:
    pass
  return evLst
 @staticmethod
 def VVhFBe(txt, toLang):
  txt = txt.strip()
  if txt:
   qUrl = "https://translate.google.com/m?&sl=auto&tl=%s&q=%s" % (toLang, FF2NHB(txt))
   txt, err = CCqQHV.VVpi8S(qUrl, timeout=1, allowDocType=True)
   if err:
    return "", err
   else:
    txt = FF9CmS(txt)
    div1, div2 = '<div class="result-container">', '</div>'
    ndx  = txt.find(div1)
    if ndx > -1:
     txt = txt[ndx + len(div1):]
     ndx  = txt.find(div2)
     if ndx > -1:
      return txt[:ndx], ""
   return "", "Could not translate"
  else:
   return "", "Nothing to translate"
 @staticmethod
 def VVbwY9(refCode, events):
  from enigma import eEPGCache
  totEv = totOK = 0
  if hasattr(eEPGCache, "importEvents"):
   epgInst = eEPGCache.getInstance()
   if epgInst:
    for data in events:
     totEv += 1
     try:
      if data[0] > iTime() + 604800:
       data = data[:4] + ("",) + data[5:]
      epgInst.importEvents(refCode, (data,))
      totOK += 1
     except:
      pass
  return totEv, totOK
 @staticmethod
 def VVsz5C(SELF):
  if not CC6sg1.VVStEc(SELF):
   return
  title = "File Size"
  fSize = "Not received from server"
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF)
  err = url =  fSize = resumable = ""
  if FFeC5o(decodedUrl):
   url = iSub(r"[&?]mode=.+end=", r"", decodedUrl, flags=IGNORECASE)
   url = iSub(r"[?]play_token.+", r"", url, flags=IGNORECASE)
   if url.endswith(":" + chName):
    url = url[:-(len(chName) + 1)]
   if "chCode" in decodedUrl:
    url = CCyIre.VVQdst(decodedUrl)
   try:
    import requests
    resp = requests.get(url, headers=CCyIre.VVDicS(), timeout=3, stream=True, verify=False)
    if not resp.ok:
     FFkYsE(SELF, "Err-%d : %s" % (resp.status_code, resp.reason), title=title)
     return
    hSize = resp.headers.get("Content-Length", "")
    if hSize and hSize.isdigit():
     size = int(hSize)
     fSize = CC7ujK.VVw1Gr(size)
     if "vnd.apple" in resp.headers.get("content-type", ""):
      fSize += FFkhYI(" (M3U/M3U8 File)", VVkXS4)
    else:
     fSize = "No info. from server. Try again later."
    resumable = "Yes" if CC9Zvn.VVXg6v(resp) else "No"
   except requests.Timeout as e: err = "Connection Timeout"
   except      : err = "Connection Error"
  else:
   err = "Not a Movie/Series !"
  def VVD6fO(subj, val):
   return "%s\n%s\n\n" % (FFkhYI("%s:" % subj, VVoTT6), val)
  title = "File Size"
  txt  = VVD6fO(title , fSize or "?")
  txt += VVD6fO("Name" , chName)
  txt += VVD6fO("URL" , url)
  if resumable: txt += VVD6fO("Supports Download-Resume", resumable)
  if err  : txt += FFkhYI("Error:\n", VVU8eD) + err
  FFNEkd(SELF, txt, title=title)
 @staticmethod
 def VVglzz(SELF):
  fPath, fDir, fName = CC7ujK.VVa1tR(SELF)
  if fPath:
   fPic = ""
   fName, fExt = os.path.splitext(fName)
   for ext in ("png", "jpg", "bmp", "gif", "jpe", "jpeg", "mvi"):
    pic = "%s%s.%s" % (fDir, fName, ext)
    if fileExists(pic):
     fPic = pic
     break
   return fPath, fDir, fName, fPic
  else:
   return "", "", "", ""
 @staticmethod
 def VVT08j(event):
  genre = PR = ""
  try:
   genre  = CCARMv.VVJw1T(event.getGenreData().getLevel1(), event.getGenreData().getLevel2())
   age = event.getParentalData().getRating()
   PR  = CCARMv.VVy7Il(age)
  except:
   pass
  return genre, PR
 @staticmethod
 def VVy7Il(age):
  if   age == 0 : return "Undefinded (all ages)"
  elif age > 15 : return "Rated by broadcaster (%d)" % age
  else   : return "Minimum Age = %d years" % (age + 3)
 @staticmethod
 def VVJw1T(L1, L2):
  if   L1 <= 0  : return "Undefined Content"
  elif L1 >= 15  : return "User Defined Genre"
  elif L1 > 12  : return "Unlisted Genre"
  else:
   MG, SG = CCARMv.VVcU9X()
   if MG and SG:
    key = "%d,%d" % (L1, L2)
    if key in SG   : return SG[key].title()
    elif L1 - 1 < len(MG) : return MG[L1 - 1] .title()
    else     : return "Unknown Genre"
   else:
    return ""
 @staticmethod
 def VVcU9X():
  path = VVASCC + "genre"
  MG = SG = ""
  if fileExists(path):
   MG = iFindall(r"\d,0;(\w+\s?\w+)", FFqD66(path), IGNORECASE)
   SG = iFindall(r"(\d+,\d+);(.+)", FFqD66(path), IGNORECASE)
   if SG: SG = dict(SG)
  return MG, SG
 @staticmethod
 def VVc7qU(path):
  return "ffmpeg -y -i '%s' -vf scale=-1:132 '%s' > /dev/null 2>&1;" % (path, path)
 @staticmethod
 def VVE38P(refCode):
  span = iSearch(r"((?:[A-Fa-f0-9]+:){9}(?:[A-Fa-f0-9]+))", refCode.rstrip(":"))
  if span:
   pPath = CCrs3r.VVsNIk() + span.group(1).strip(":").replace(":", "_").upper() + ".png"
   return pPath
  return ""
 @staticmethod
 def VVTLfj(serv):
  isLocal = isIptv = isDvb = isDvbS = isDvbC = isDvbT = False
  typeTxt = chPath = ""
  if serv:
   refCode = serv.toString() or ""
   chPath = serv.getPath() or ""
   if FFuZb6(refCode):
    isIptv = True
    typeTxt = "IPTV"
   elif chPath.startswith("/"):
    isLocal = True
    typeTxt = "Local Media"
   elif not chPath:
    isDvb = True
    ns = FFwYmz(refCode)
    if   ns.startswith("EEEE") : isDvbT, typeTxt = True, "DVB-T"
    elif ns.startswith("FFFF") : isDvbC, typeTxt = True, "DVB-C"
    else      : isDvbS, typeTxt = True, "DVB-S"
  return isLocal, isIptv, isDvb, isDvbS, isDvbC, isDvbT, typeTxt, chPath
class CCyIre():
 def __init__(self):
  self.VVPj61   = ""
  self.VVrGQ8    = ""
  self.VVBi7f   = ""
  self.VVIGxq = ""
  self.VVlrb6  = ""
  self.VVfnCF = 0
  self.VVrIFf    = ""
  self.VVMw87   = "#f#11ffffaa#User"
  self.VVwRua   = "#f#11aaffff#Server"
 def VVJLFc(self, url, mac, ph1="", VVl2X5=True):
  self.VVPj61   = ""
  self.VVrGQ8    = ""
  self.VVBi7f   = ""
  self.VVIGxq = ""
  self.VVlrb6  = ""
  self.VVfnCF = 0
  self.VVrIFf    = {"s": "/server/load.php", "p": "/portal.php"}.get(ph1, "")
  host = self.VVDIKX(url)
  if not host:
   if VVl2X5:
    self.VV6I1g("Incorrect URL Format !\n\n%s" % url)
   return False
  mac = self.VV1vDi(mac)
  if not host:
   if VVl2X5:
    self.VV6I1g("Incorrect MAC Format !\n\n%s" % mac)
   return False
  self.VVPj61 = host
  self.VVrGQ8  = mac
  return True
 def VVDIKX(self, url):
  if url.endswith("mac=") : url = url[:-4]
  if url.endswith("mac") : url = url[:-4]
  url = url.rstrip("/?")
  if url.endswith("/c") : url = url[:-2]
  url = url.rstrip("/ :")
  span = iSearch(r"(.+)(\/playlist.+mac)", url, IGNORECASE)
  if span:
   url = span.group(1)
  return url
 def VV1vDi(self, mac):
  span = iSearch(r"((?:[A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})", mac, IGNORECASE)
  if span : return span.group(1).upper()
  else : return ""
 def VVIcTT(self):
  res, err = self.VV79mN(self.VVbUoI())
  urlPath = "/stalker_portal"
  if "404" in err and urlPath in self.VVPj61:
   self.VVPj61 = self.VVPj61.replace(urlPath, "")
   res, err = self.VV79mN(self.VVbUoI())
  token = rand = ""
  if not err:
   try:
    tDict = jLoads(res.text)         #
    token = CCqQHV.VVvsIK(tDict["js"], "token")
    rand  = CCqQHV.VVvsIK(tDict["js"], "random")
   except:
    pass
  return token.strip(), rand.strip(), err
 def VV6cJP(self, VVl2X5=True):
  if not self.VVrIFf:
   self.VVrIFf = self.VVHhYV()
  err = blkMsg = FFewCETxt = ""
  try:
   token, rand, err = self.VVIcTT()
   if token:
    self.VVBi7f = token
    self.VVIGxq = rand
    if rand:
     self.VVfnCF = 2
    prof, retTxt = self.VVmMba(True)
    if prof:
     self.VVlrb6 = retTxt
     if "device_id mismatch" in retTxt:
      self.VVfnCF = 3
      prof, retTxt = self.VVmMba(False)
      if retTxt:
       self.VVlrb6 = retTxt
    return token, prof, ""
  except:
   pass
  tErr = err or "Could not get Token from server !"
  if blkMsg or FFewCETxt:
   tErr += "\n"
   if blkMsg: tErr += "\n%s" % blkMsg
   if FFewCETxt: tErr += "\n%s" % FFewCETxt
  if VVl2X5:
   self.VV6I1g(tErr)
  return "", "", tErr
 def VVHhYV(self):
  try:
   import requests
   res = requests.get("%s/c/xpcom.common.js" % self.VVPj61, headers=CCyIre.VVDicS(), stream=True, timeout=2)
   if res.ok and "javascript" in res.headers.get("content-type"):
    for line in res.iter_lines():
     if line:
      line = str(line.decode('utf-8'))
      span = iSearch(r".+ajax_loader.+'(\/.+\.php)'", line, IGNORECASE)
      if span:
       return span.group(1)
  except:
   pass
  return ""
 def VVmMba(self, capMac):
  res, err = self.VV79mN(self.VVRV7s(capMac))
  if not err:
   try:
    tDict = jLoads(res.text)
    word = "m" + "sg"
    blkMsg = CCqQHV.VVvsIK(tDict["js"], "block_%s" % word)
    FFewCETxt = CCqQHV.VVvsIK(tDict["js"], word)
    return tDict, FFewCETxt.strip() or blkMsg.strip()
   except:
    pass
  return "", ""
 def VVRV7s(self, capMac):
  param = ""
  if self.VVlrb6 or self.VVIGxq:
   param = self.getMoreAuth_params(self.getMoreAuth_IDs(self.VVrGQ8.upper() if capMac else self.VVrGQ8.lower(), self.VVIGxq))
  return self.VV69Q8() + "type=stb&action=get_profile" + param
 exec(FFWbB4("ZGVmIGdldE1vcmVBdXRoX3BhcmFtcyhzZWxmLCBJZCk6DQogcGFyYW0gID0gIiZhdXRoX3NlY29uZF9zdGVwPTEmaHdfdmVyc2lvbj0yLjE3LUlCLTAwJmh3X3ZlcnNpb25fMj02MiZzbj0lcyZkZXZpY2VfaWQ9JXMmZGV2aWNlX2lkMj0lcyZzaWduYXR1cmU9JXMiICUgKElkWzBdLCBJZFsxXSwgSWRbMV0sIElkWzJdKQ0KIHJldHVybiBwYXJhbSArICcmbWV0cmljcz17Im1hYyI6IiVzIiwic24iOiIlcyIsInR5cGUiOiJTVEIiLCJtb2RlbCI6Ik1BRzI1MCIsInJhbmRvbSI6IiVzIn0nICUgKElkWzNdLCBJZFswXSwgSWRbNF0pDQpkZWYgZ2V0TW9yZUF1dGhfSURzKHNlbGYsIG0sIHIpOg0KIGltcG9ydCBoYXNobGliDQogbWFjVXRmOCA9IG0uZW5jb2RlKCd1dGYtOCcpDQogcyA9IGhhc2hsaWIubWQ1KG1hY1V0ZjgpLmhleGRpZ2VzdCgpLnVwcGVyKClbOjEzXQ0KIHJldHVybiBzLCBoYXNobGliLnNoYTI1NihtYWNVdGY4KS5oZXhkaWdlc3QoKS51cHBlcigpLCBoYXNobGliLnNoYTI1NigocyArIG0pLmVuY29kZSgndXRmLTgnKSkuaGV4ZGlnZXN0KCkudXBwZXIoKSwgbSwgcg=="))
 def VVPBb5(self, forceMoreInfo=False):
  rows = []
  if not forceMoreInfo:
   rows = self.VVsXSp()
  if len(rows) < 10:
   rows = self.VVqZYj()
  if not rows or len(rows[0]) == 2:
   rows.append(("Host"    , self.VVPj61 ))
   rows.append(("MAC (from URL)" , self.VVrGQ8 ))
   rows.append(("Token"   , self.VVBi7f ))
   rows.sort(key=lambda x: x[0].lower())
   return rows, 2
  else:
   rows.append(("1", self.VVMw87  , "MAC" , self.VVrGQ8 ))
   rows.append(("2", self.VVwRua, "Host" , self.VVPj61 ))
   rows.append(("2", self.VVwRua, "Token" , self.VVBi7f ))
   rows.sort(key=lambda x: (x[0], x[2]))
   return rows, 4
 def VVYtsT(self, isPhp=True, VVl2X5=False):
  token, profile, tErr = self.VV6cJP(VVl2X5)
  if not token:
   return "", "", "", "", tErr
  m3u_Url = host = user1 = pass1 = err=  ""
  url = self.VVx10j()
  res, err = self.VV79mN(url)
  if not err:
   try:
    tDict = jLoads(res.text)
    m3u_Url = CCqQHV.VVvsIK(tDict["js"], "cmd")
    m3u_Url = m3u_Url.replace("ffmpeg ", "")
    span = iSearch(r"(http.+)\/(.+)\/(.+)(\/\?.+)", m3u_Url, IGNORECASE)
    if span:
     host = span.group(1)
     user1 = FF2NHB(span.group(2))
     pass1 = FF2NHB(span.group(3))
     if isPhp:
      m3u_Url = "%s/player_api.php?username=%s&password=%s" % (host, user1, pass1)
     else:
      m3u_Url = "%s/%s/%s/" % (host, user1, pass1)
   except:
    pass
  return m3u_Url, host, user1, pass1, err
 def VVsXSp(self):
  m3u_Url, host, user1, pass1, err = self.VVYtsT()
  rows = []
  if m3u_Url:
   res, err = self.VV79mN(m3u_Url)
   if not err:
    try:
     tDict = jLoads(res.text)
     for key, val in list(tDict["user_info"].items()) :
      if any(x in key for x in ("exp_date", "created_at")): val = FFcgMH(int(val))
      if isinstance(val, list): val = str(" , ".join(val))
      else     : val = str(val)
      rows.append(("1", self.VVMw87, str(key).replace("_", " ").title(), val))
     for key, val in list(tDict["server_info"].items()):
      if "timestamp_now"  in key : val = FFcgMH(int(val))
      else      : val = str(val)
      rows.append(("2", self.VVwRua, str(key).replace("_", " ").title(), val))
    except:
     pass
  return rows
 def VVqZYj(self):
  token, profile, tErr = self.VV6cJP()
  try:
   item = profile["js"]
  except:
   return []
  if not isinstance(item, dict):
   return []
  rows = []
  c  = "#f#11ffff55#"
  rows = []
  for key, val in list(item.items()):
   if not val:
    continue
   try:
    if key == "mac":
     if val and FFyOvd(val): val = FFWbB4(val.decode("UTF-8"))
     else     : val = self.VVrGQ8
    elif key == "play_token":
     parts = val.split(":")
     if len(parts) == 3:
      pToken = parts[0]
      started = FFcgMH(int(parts[1]))
      if parts[2] : ends = FFcgMH(int(parts[1]) + int(parts[2]))
      else  : ends = ""
      val = "%s (%s ... %s)" % (pToken, started, ends)
    elif key == "aspect":
     val = " , ".join(["%s=%s" % (k, v) for k, v in list(jLoads(val)["js"].items())])
    elif key in ("created", "last_watchdog"):
     val = FFcgMH(int(val))
    elif isinstance(val, list):
     val = str(" , ".join(val))
    elif isinstance(val, dict):
     val = str(val).replace("u'", "").replace("'", "").strip("{} ")
    else:
     val = str(val).strip()
   except:
    val = str(val)
   rows.append(((str(key).replace("_", " ").title(), str(val))))
  return rows
 def VV5dEp(self, mode, chCm, epNum, epId):
  token, profile, tErr = self.VV6cJP(VVl2X5=False)
  if not token:
   return ""
  crLinkUrl = self.VV7WsF(mode, chCm, epNum, epId)
  res, err = self.VV79mN(crLinkUrl)
  chUrl = ""
  if not err:
   try:
    chUrl = CCqQHV.VVvsIK(jLoads(res.text)['js'], "cmd")
   except:
    pass
  chUrl = chUrl.replace("ffmpeg ", "")
  chUrl = chUrl.replace(":", "%3a")
  chUrl = chUrl.replace("auto ", "")
  return chUrl
 def VV69Q8(self):
  return self.VVPj61 + (self.VVrIFf or "/server/load.php") + "?"
 def VVbUoI(self):
  return self.VV69Q8() + "type=stb&action=handshake&token=&mac=%s" % self.VVrGQ8
 def VViCnu(self, mode):
  url = self.VV69Q8() + "type=%s&action=" % mode
  if   mode == "itv"  : url += "get_genres"
  elif mode == "vod"  : url += "get_categories&force_ch_link_check="
  elif mode == "series": url += "get_categories"
  return url
 def VV4Pya(self, catID):
  return self.VV69Q8() + "type=series&action=get_ordered_list&sortby=added&movie_id=%s&p=1" % catID
 def VVL6LN(self, mode, catID, page):
  url = self.VV69Q8() + "type=%s&action=get_ordered_list&sortby=number&p=%d&" % (mode, page)
  if mode == "itv": url += "genre=%s" % catID
  else   : url += "category=%s&force_ch_link_check=" % catID
  return url
 def VVbPdK(self, mode, searchName, catId, page):
  catId = ("&category=%s" % catId) if catId else ""
  return self.VV69Q8() + "type=%s&action=get_ordered_list&search=%s&%s&p=%d" % (mode, searchName, catId, page)
 def VVxqVN(self, mode, catID):
  return self.VV69Q8() + "type=%s&action=get_all_channels&genre=%s&force_ch_link_check=&fav=0&sortby=number&hd=0" % (mode, catID)
 def VV7WsF(self, mode, chCm, serCode, serId):
  url = self.VV69Q8() + "action=create_link&"
  if mode == "series" : url += "type=vod&series=%s&cmd=/media/%s.mpg" % (serCode, serId)
  else    : url += "type=%s&cmd=%s&forced_storage=undefined&disable_ad=0&download=false" % (mode, chCm)
  return url
 def VVx10j(self):
  return self.VV69Q8() + "type=itv&action=create_link"
 def VVWeZp(self, host, mac, mode, chName, catID, stID, chNum, chCm, serCode, serId):
  refCode = self.VVyKHt(catID, stID, chNum)
  query = self.VVvPQ5(mode, self.VVrIFf[1:2], FF5o9B(host), FF5o9B(mac), serCode, serId, chCm)
  if chCm.endswith(".m3u8") : chUrl = "%s?%s" % (chCm, query)
  else      : chUrl = "%s/j.php?%s" % (host, query)
  chUrl = refCode + chUrl.replace(":", "%3a") + ":" + chName
  return refCode, chUrl
 def VVvPQ5(self, mode, ph1, host, mac, serCode, serId, chCm):
  query = "mode=%s&ph1=%s&hst=%s&chCode=%s&epNum=%s&epId=%s&chCm=%s&end=" % (mode, ph1, host, mac, serCode, serId, chCm)
  return query.replace("ffmpeg ", "").replace(":", "%3a")
 def VVslTC(self, url):
  if   "mode=itv"  in url: mode = "itv"
  elif "mode=vod"  in url: mode = "vod"
  elif "mode=series" in url: mode = "series"
  else       : return False, "", "", "", "", "", "", "", "", ""
  res  = iUrlparse(url)
  scheme = res.scheme
  netloc = res.netloc
  tDict = iUrlparse_qs(res.query)
  ph1  = tDict.get("ph1" , [""])[0].strip()
  host = tDict.get("hst" , [""])[0].strip()
  mac  = tDict.get("chCode", [""])[0].strip()
  epNum = tDict.get("epNum" , [""])[0].strip().replace(":" , "%3a")
  epId = tDict.get("epId" , [""])[0].strip().replace(":" , "%3a")
  chCm = tDict.get("chCm" , [""])[0].strip().replace("ffmpeg ", "").replace(":" , "%3a")
  query = self.VVvPQ5(mode, ph1, host, mac, epNum, epId, chCm)
  if scheme: scheme += "://"
  playHost = scheme + netloc
  host  = FFWbB4(host)
  mac   = FFWbB4(mac)
  valid = False
  if self.VVDIKX(playHost) and self.VVDIKX(host) and self.VVDIKX(mac):
   if (mode in ("itv", "vod") and chCm) or (mode == "series" and epNum and epId):
    valid = True
  return valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query
 def VV79mN(self, url, useCookies=True):
  try:
   import requests
  except:
   return "", 'The "Requests" library is not installed'
  err = ""
  try:
   headers = CCyIre.VVDicS()
   if self.VVBi7f:
    headers["Authorization"] = "Bearer %s" % self.VVBi7f
   if useCookies : cookies = {"mac": self.VVrGQ8, "stb_lang": "en"}
   else   : cookies = None
   res = requests.get(url, headers=headers, allow_redirects=True, timeout=2, cookies=cookies)
   if res.ok :
    return res, ""
   else:
    if res.status_code == 407: reason = "Proxy Authentication Required"
    else      : reason = "Unknown"
    err = "Err-%d : %s" % (res.status_code, res.reason or reason)
  except requests.Timeout as e     : err = "Connection Timeout"
  except requests.ConnectionError as e   : err = "Connection Error"
  except requests.exceptions.RequestException as e: err = "Request Error"
  except Exception as e       : err = "Error\n" + str(e)[:120]
  return "", err
 @staticmethod
 def VVHmZi(url, verify=False):
  try:
   import requests
   resp = requests.get(url, headers=CCyIre.VVDicS(), timeout=3, verify=verify)
   if resp.ok : return str(resp.text) , ""
   else  : return ""    , "Error %d\n\n%s" % (resp.status_code, resp.reason)
  except:
   return "", "Error while contacting server !"
 @staticmethod
 def VVDicS():
  return {'User-Agent': "Mozilla/5.0 (QtEmbedded; U; Linux; C; Emulator/1.2.12) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3"}
 @staticmethod
 def VVhoth(host, mac, tType, action, keysList=[]):
  myPortal = CCyIre()
  ph1 = "s"
  pref = "/portal.php" if par == "p" else "/server/load.php"
  ok = myPortal.VVJLFc(host, mac, ph1)
  if not ok:
   return url, "", "Incorrect URL/MAC", "", "", ""
  token, profile, tErr = myPortal.VV6cJP(VVl2X5=False)
  if not token:
   return url, "", "No Token Received", "", "", ""
  url = "%s%s?type=%s&action=%s" % (host, ph1, tType, action)
  res, err = myPortal.VV79mN(url)
  if not err:
   try:
    tDict = jLoads(res.text)
    extraDict = {}
    if keysList:
     for item in keysList:
      if item in tDict["js"]:
       extraDict[item] =  tDict["js"][item]
    return True, url, res.text, err, tDict, myPortal.VVF5oR(tDict), extraDict
   except:
    pass
  return False, url, res, err, "", "", ""
 def VVF5oR(self, tDict):
  return iDumps(tDict, indent=4, sort_keys=True)
 def VV6I1g(self, err, title="Portal Browser"):
  FFkYsE(self, str(err), title=title)
 def VV6ejl(self, mode):
  if   mode in ("itv"  , CCqQHV.VVZ3on , CCqQHV.VV3zJB)  : return "Live"
  elif mode in ("vod"  , CCqQHV.VVzxcn , CCqQHV.VV3qLZ)  : return "VOD"
  elif mode in ("series" , CCqQHV.VVTVFh , CCqQHV.VV47C9) : return "Series"
  else                          : return "IPTV"
 def VVm4JW(self, mode, searchName):
  return 'Find in %s : %s' % (self.VV6ejl(mode), FFkhYI(searchName, VVkXS4))
 def VV9NT4(self, catchup=False):
  VV625J = []
  VV625J.append(("Live"    , "live"  ))
  VV625J.append(("VOD"    , "vod"   ))
  VV625J.append(("Series"   , "series"  ))
  if catchup:
   VV625J.append(VVm77t)
   VV625J.append(("Catch-up TV" , "catchup"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Account Info." , "accountInfo" ))
  return VV625J
 @staticmethod
 def VVcW91(decodedUrl):
  m3u_Url = host = user1 = pass1 = streamId = ""
  p = CCyIre()
  valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(decodedUrl)
  if valid:
   ok = p.VVJLFc(host, mac, ph1, VVl2X5=False)
   if ok:
    m3u_Url, host, user1, pass1, err = p.VVYtsT(isPhp=False, VVl2X5=False)
    streamId = CCyIre.VVLskf(decodedUrl)
  return valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query, m3u_Url, host, user1, pass1, streamId, err
 @staticmethod
 def VVLskf(decodedUrl):
  p = CCyIre()
  valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(decodedUrl)
  if valid and chCm:
   if   mode == "itv"  : patt = r'.+ch\/(\d+)_'
   elif mode == "vod"  : patt = r'stream_id":"*(\d+)'
   elif mode == "series": patt = r'series_id":"*(\d+)'
   span = iSearch(patt, FFWbB4(chCm), IGNORECASE)
   if span:
    return span.group(1)
  return ""
 @staticmethod
 def VVQdst(decodedUrl):
  p = CCyIre()
  valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(decodedUrl)
  if valid:
   if CCyIre.VVaB6E(chCm):
    return FF9CmS(chCm)
   else:
    ok = p.VVJLFc(host, mac, ph1, VVl2X5=False)
    if ok:
     try:
      chUrl = p.VV5dEp(mode, chCm, epNum, epId)
      return FF9CmS(chUrl)
     except:
      pass
  return ""
 @staticmethod
 def VVaB6E(chCm):
  return chCm.startswith("http") and not "//localhost/" in chCm
class CCsnEk(CCyIre):
 def __init__(self):
  CCyIre.__init__(self)
  self.mode   = ""
  self.refCode  = ""
  self.chName   = ""
  self.iptvRef  = ""
  self.chCm   = ""
  self.epNum   = ""
  self.epId   = ""
  self.query   = ""
 def VVdEw9(self, refCode, chName, decodedUrl, iptvRef):
  valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = self.VVslTC(decodedUrl)
  if valid:
   if self.VVJLFc(host, mac, ph1, VVl2X5=False):
    self.mode  = mode
    self.refCode = refCode
    self.chName  = chName
    self.iptvRef = iptvRef
    self.chCm  = chCm
    self.epNum  = epNum
    self.epId  = epId
    self.query  = query
    return True
  return False
 def VVQp2W(self, passedSELF=None, isFromSession=False):
  chUrl = ""
  try:
   chUrl = self.VV5dEp(self.mode, self.chCm, self.epNum, self.epId)
  except:
   return False
  isDirect = False
  if CCyIre.VVaB6E(self.chCm):
   chUrl = FF9CmS(self.chCm)
   chUrl = FF2NHB(self.chCm)
   chUrl = chUrl.replace("%253a", "%3a")
   if not "?" in chUrl:
    chUrl += "?"
  elif " " in self.chCm or " " in chUrl:
   if " " in chUrl:
    chUrl = chUrl.split(" ")[1]
   if not "?" in chUrl:
    chUrl += "?"
  if not chUrl:
   return False
  if not self.refCode.endswith(":"):
   self.refCode += ":"
  chUrl = chUrl.strip()
  chUrl = self.refCode + chUrl + ":" + self.chName
  newIptvRef = self.VVraD5(chUrl)
  bPath = CCgKdM.VVYZBe()
  if newIptvRef:
   if passedSELF:
    FFJZ42(passedSELF, newIptvRef, VVpyjK=False, fromPrtalReplay=True, isFromSession=isFromSession)
   else:
    FFJZ42(self, newIptvRef, VVpyjK=False, fromPrtalReplay=True)
   if self.iptvRef and newIptvRef and bPath:
    serv = eServiceReference(newIptvRef)
    newCode = serv and serv.toString()
    if newCode:
     self.VVntas(self.iptvRef, newCode, bPath)
   return True
  else:
   return False
 def VVraD5(self, chUrl):
  newIptvRef = ""
  playMarks = ("play_token=", "/play/", "lid=")
  for toFind in playMarks:
   if toFind in chUrl:
    ndx = chUrl.find(toFind)
    if ndx > -1:
     ndx = chUrl.find(":", ndx)
     if ndx > -1:
      left  = chUrl[:ndx]
      right  = chUrl[ndx:]
      newIptvRef = left + "&" + self.query + right
    break
  if not newIptvRef:
   x1 = chUrl.find("?")
   if x1 > -1:
    x2 = chUrl[x1:].find(":")
    if x2 > -1:
     newIptvRef = chUrl[:x1+x2] + "&" + self.query + chUrl[x1+x2:]
  return newIptvRef
 def VVntas(self, oldCode, newCode, bPath):
  patt = r"((?:[A-Fa-f0-9]+[:]){10}).+(mode=.+)chCm="
  span = iSearch(patt, newCode, IGNORECASE)
  if span:
   newRef, newPar = span.group(1).upper(), span.group(2)
   params = ("&ph1=s", "&ph1=p", "&ph1=")
   for param in params: newPar = newPar.replace(param, "")
   lines = FFjdnJ(bPath)
   for ndx, line in enumerate(lines):
    span = iSearch(patt, line, IGNORECASE)
    if span:
     fileRef, filePar = span.group(1).upper(), span.group(2)
     if newRef == fileRef:
      for param in params: filePar = filePar.replace(param, "")
      if newPar == filePar:
       lines[ndx] = "#SERVICE %s" % newCode
       with open(bPath, "w") as f: f.write("\n".join(lines) + "\n")
       FFlB9k()
class CCoAK5(CCsnEk):
 def __init__(self, passedSession):
  CCsnEk.__init__(self)
  self.passedSession = passedSession
  self.lastRef  = ""
  self.startTime  = iTime()
  self.timer1   = eTimer()
  self.timer2   = eTimer()
  self.dnldWin  = None
  self.isFromEOF  = False
  try:
   from Components.ServiceEventTracker import ServiceEventTracker
   from enigma import iPlayableService
   evTrk = ServiceEventTracker(screen=self.passedSession.screen, eventmap={iPlayableService.evStart: self.VV0acZ, iPlayableService.evEOF: self.VV0vxx, iPlayableService.evEnd: self.VVQ0ai})
  except:
   pass
  try:
   self.timer_conn = self.timer2.timeout.connect(self.VV0Ck2)
  except:
   self.timer2.callback.append(self.VV0Ck2)
  self.timer2.start(3000, False)
  self.VV0Ck2()
 def VV0Ck2(self):
  if not CFG.downloadMonitor.getValue():
   self.VV7Kj0()
   return
  lst = CC9Zvn.VVz5tx()
  avPerc = []
  txt = ""
  if lst:
   for path, totSz, logF in lst:
    if totSz:
     totSz = int(totSz) if totSz.isdigit() else 0
     curSz = 0
     sz = FFT03z(path)
     if sz > -1:
      curSz = sz
     if totSz:
      perc = (float(curSz) / float(totSz) * 100.0)
      avPerc.append(perc)
    elif logF:
     perc = CC9Zvn.VVL7Z9(logF)
     if perc > -1:
      avPerc.append(perc)
   if lst:
    txt = "Files=%d" % len(lst)
    if avPerc:
     perc = sum(avPerc) / len(avPerc)
     if perc: txt += "   %.2f %%" % perc
  if txt:
   if not self.dnldWin:
    self.dnldWin = self.passedSession.instantiateDialog(CClv1B, txt, 30)
    self.dnldWin.instance.move(ePoint(30, 20))
    self.dnldWin.show()
    FFiE61(self.dnldWin["myWinTitle"], "#440000", 1)
   else:
    self.dnldWin["myWinTitle"].setText(txt)
  elif self.dnldWin:
   self.VV7Kj0()
 def VV7Kj0(self):
  if self.dnldWin:
   self.passedSession.deleteDialog(self.dnldWin)
   self.dnldWin = None
 def VV0acZ(self):
  self.startTime = iTime()
 def VV0vxx(self):
  global EVENT_STATE
  EVENT_STATE = ".....EOF....."
  if CFG.autoResetFrozenIptvChan.getValue() and (iTime() - self.startTime) > 5:
   serv = self.passedSession.nav.getCurrentlyPlayingServiceReference()
   if serv:
    refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self.passedSession, isFromSession=True)
    if iptvRef and not FFeC5o(decodedUrl):
     self.isFromEOF = True
     CCG7K3(self.passedSession, "Refreshing")
     self.passedSession.nav.stopService()
     self.passedSession.nav.playService(serv)
     InfoBar.instance.hide()
     self.startTime = iTime()
 def VVQ0ai(self):
  self.startTime = iTime()
  try:
   self.timer1_conn = self.timer1.timeout.connect(self.VV20ZQ)
  except:
   self.timer1.callback.append(self.VV20ZQ)
  self.timer1.start(100, True)
 def VV20ZQ(self):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self.passedSession, isFromSession=True)
  if decodedUrl:
   span = iSearch(r"(mode=.+end=)", decodedUrl, IGNORECASE)
   if span:
    ref = span.group(1)
    if self.isFromEOF or not ref == self.lastRef:
     valid = self.VVdEw9(refCode, chName, decodedUrl, iptvRef)
     if valid:
      self.lastRef = ref
      if self.isFromEOF or not CCppdx.VVKGP0:
       self.isFromEOF = False
       self.VVQp2W(self.passedSession, isFromSession=True)
class CCD3Dl():
 def __init__(self):
  self.removeTag  = CFG.hideIptvServerChannPrefix.getValue()
  self.hideAdult  = CFG.hideIptvServerAdultWords.getValue()
  self.beInTagPatt = r"(b[-]*e[-]*I[-]*N)"
  self.beInRepl  = r"beIN"
  self.nameTagPatt = iCompile( r"\s*^[A-Z0-9]+\s*\|*[|:-]\s*(.+)"
          r"|^(?!\[)*\s*[\[(|:][ A-z0-9\-._:|\]\[]+[\])|:](.+)")
  self.adultWords  = ("adult", "aduld", "sex", "porn", "xxx", "xxi", "erotic", "x-rated", "xrated", "skin flick", "dirty movie", "dirty film", "blue movie", "blue film", "18+", "+18", "r18 movie", "r18 film", "r-18 movie", "r-18 film", "r-17 movie", "r-17 film")
  self.adultWords2 = ("\\u042d\\u0440\\u043e\\u0442\\u0438\\u0447\\u0435\\u0441\\u043a\\u0438\\u0435", "dla doros\\u0142ych")
 def VV16ZS(self, name,  censored=""):
  if self.hideAdult and (censored == "1" or any(x in name.lower() for x in self.adultWords)):
   return ""
  name = iSub(self.beInTagPatt, self.beInRepl, name, flags=IGNORECASE).strip()
  if CCqQHV.VVmaA2(name):
   return CCqQHV.VVy8pO(name)
  name = self.VVmclD(name)
  return name.strip() or name
 def VVmclD(self, name):
  if self.removeTag:
   span = iSearch(self.nameTagPatt, name)
   if span:
    return span.group(1) or span.group(2)
  return name
 def VVGk9I(self, name):
  name = iSub(self.beInTagPatt, self.beInRepl, name, flags=IGNORECASE).strip()
  name = self.VVmclD(name)
  return name.lower().replace(" hd", "").replace(" fm", "").replace(" 4k", "").replace(" tv", "").replace(" sd", "").strip()
 def VVyWSY(self, name):
  if self.hideAdult:
   if any(x in name.lower() for x in self.adultWords):
    return ""
   elif any(x in name.encode('ascii', 'backslashreplace').decode('utf-8').lower() for x in self.adultWords2):
    return ""
  return name.strip()
 def VVn2Iq(self, wordsList):
  return any(x in self.adultWords for x in wordsList)
 def VV2tDQ(self):
  return 'Cannot continue with adults words !\n\n"Skip Adults Channels" is activated in settings.'
class CC6sg1(CCyIre):
 def __init__(self):
  CCyIre.__init__(self)
 def VV4wRZ(self):
  if CC6sg1.VVStEc(self):
   FFlX3B(self, BF(self.VVDqjN, 2), title="Searching ...")
 def VVQYck(self, winSession, url, mac):
  if CC6sg1.VVStEc(self):
   if self.VVJLFc(url, mac):
    FFlX3B(winSession, self.VVmzTK, title="Checking Server ...")
   else:
    FFkYsE(self, "Incorrect URL or MAC format !", title="Starting Portal Browser")
 def VViJfK(self, item=None):
  if item:
   menuInstance, txt, path, ndx = item
   enc = CClXbe.VVTBCL(path, self)
   if enc == -1:
    return
   self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
       , titlePrefix = "Processing file lines"
       , fncToRun  = BF(self.VVw5D8, path, enc)
       , VVnFNJ = BF(self.VVBjM0, menuInstance, path))
 def VVw5D8(self, path, enc, VVC69w):
  urlMacPatt  = r"(.*)(https?:\/\/.+(?::[0-9]+)*)(?:.+)((?:[A-Fa-f0-9]{2}\s*:\s*){5}[A-Fa-f0-9]{2})(.*)"
  urlOnlyPatt = r"\s*(https?:\/\/.+(?::[0-9]+)*)"
  macOnlyPatt = r"((?:(?:.*mac\s*)[^A-Fa-f0-9]\s*)*)((?:(?:(?:[A-Fa-f0-9]{2})\s*:\s*){5})\s*(?:[A-Fa-f0-9]{2}))(.*)"
  tableRows = []
  url   = ""
  c   = 0
  totLines = 0
  with ioOpen(path, "r", encoding=enc) as f:
   for line in f:
    totLines += 1
  VVC69w.VVYqos(totLines)
  VVC69w.VV0DcB = []
  lineNum = 0
  with ioOpen(path, "r", encoding=enc) as f:
   for line in f:
    lineNum += 1
    if not VVC69w or VVC69w.isCancelled:
     return
    VVC69w.VVLLRh(1, True)
    line = str(line).strip()
    if not line or len(line) > 500 or "password" in line:
     continue
    line = iSub(r"([^\x00-\x7F]+)", r" ", line, flags=IGNORECASE)
    span = iSearch(urlMacPatt, line, IGNORECASE)
    if span:
     c  += 1
     subj = span.group(1).strip() or "-"
     url  = span.group(2).strip().split(" ")[0].split("\t")[0].strip()
     mac  = span.group(3).strip().replace(" ", "").upper()
     info = span.group(4).strip().strip(";") or "-"
     host = self.VVDIKX(url)
     mac  = self.VV1vDi(mac)
     if host and mac and VVC69w:
      VVC69w.VV0DcB.append((str(c), str(lineNum), subj, host, mac, info))
     url  = ""
     continue
    if not url:
     span = iSearch(urlMacPatt, line, IGNORECASE)
     if not span:
      span = iSearch(urlOnlyPatt, line, IGNORECASE)
      if span:
       url = span.group(1).split(" ")[0]
    else:
     span = iSearch(macOnlyPatt, line.replace("\t", " "), IGNORECASE)
     if span:
      c  += 1
      subj = span.group(1).strip() or "-"
      mac  = span.group(2).strip().replace(" ", "").upper()
      info = span.group(3).strip().strip(";") or "-"
      host = self.VVDIKX(url)
      mac  = self.VV1vDi(mac)
      if host and mac and not mac.startswith("AC") and VVC69w:
       VVC69w.VV0DcB.append((str(c), str(lineNum), "-", host, mac, info))
     else:
      span = iSearch(urlOnlyPatt, line, IGNORECASE)
      if span:
       url = span.group(1).split(" ")[0]
 def VVBjM0(self, menuInstance, path, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  title = "Portals File : %s" % os.path.basename(path)
  if VV0DcB:
   VVMQj9  = ("Home Menu"  , FFSJQP            , [])
   VVOtSO = ("Edit File"  , BF(self.VV9d4o, path)       , [])
   VV3th8 = ("M3U Options" , self.VVz6cw         , [])
   VV1QO7 = ("Check & Filter" , BF(self.VVPbGm, menuInstance, path), [])
   VVVHmY  = ("Select"   , self.VV2NXi      , [])
   header   = ("Num" , "LineNum" , "Title" , "Host", "MAC-Address" , "Comments")
   widths   = (7  , 0   , 12  , 36 , 20   , 25  )
   VVQqg2  = (CENTER , CENTER , LEFT  , LEFT , CENTER  , LEFT  )
   VVcpnp = FF1dQ4(self, None, title=title, header=header, VVvytR=VV0DcB, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VVz2kc="#0a001122", VVwpZm="#0a001122", VVghPi="#0a001122", VV0g1U="#00004455", VVooYw="#0a333333", VVPVU2="#11331100", VVKNen=True, searchCol=3, lastFindConfigObj=CFG.lastFindServers)
   if not VVr4Ej:
    FFD1yO(VVcpnp, "Stopped at line %s" % threadCounter, 1000)
  else:
   if VVr4Ej:
    FFkYsE(self, "No valid portal data (or incorrect file format) in:\n\n%s" % path, title=title)
 def VVz6cw(self, VVcpnp, title, txt, colList):
  host = colList[3]
  mac  = colList[4]
  title = "Portal M3U Options"
  VV625J = []
  VV625J.append(("Browse as M3U"  , "browse"))
  VV625J.append(("Download M3U File" , "downld"))
  FFuRfS(self, BF(self.VV4O69, VVcpnp, host, mac), title=title, VV625J=VV625J, width=600, VVeYEo=True)
 def VV4O69(self, VVcpnp, host, mac, item):
  if item:
   title, item, ndx = item
   if   item == "browse": FFlX3B(VVcpnp, BF(self.VVpSDu, VVcpnp, title, host, mac, item), title="Checking Server ...")
   elif item == "downld": FFMIbO(self, BF(FFlX3B, VVcpnp, BF(self.VVpSDu, VVcpnp, title, host, mac, item), title="Downloading ..."), "Download m3u file for ?\n\n%s" % host, title=title)
 def VVpSDu(self, VVcpnp, title, host, mac, item):
  p = CCyIre()
  m3u_Url = ""
  ok = p.VVJLFc(host, mac, VVl2X5=False)
  err = ""
  if ok:
   m3u_Url, host, user1, pass1, err = p.VVYtsT(VVl2X5=False)
  if m3u_Url:
   if   item == "browse": self.VVhCXa(title, m3u_Url)
   elif item == "downld": self.VVH5mr(title, "%s/get.php?username=%s&password=%s&type=m3u" % (host, user1, pass1))
  else:
   FFkYsE(self, err or "No response from Server !", title=title)
 def VV2NXi(self, VVcpnp, title, txt, colList):
  url = colList[3]
  mac = colList[4]
  self.VVQYck(VVcpnp, url, mac)
 def VV9d4o(self, path, VVcpnp, title, txt, colList):
  rowNum = int(colList[1].strip()) - 1
  if fileExists(path) : CCYE8p(self, path, VVnFNJ=BF(self.VVxsol, VVcpnp), curRowNum=rowNum)
  else    : FFAVqd(self, path)
 def VVPbGm(self, menuInstance, path, VVcpnp, title, txt, colList):
  self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
      , titlePrefix = "Checking Portals"
      , fncToRun  = BF(self.VV9Xv4, VVcpnp)
      , VVnFNJ = BF(self.VVpGfk, menuInstance, VVcpnp, path))
 def VV9Xv4(self, VVcpnp, VVC69w):
  VVC69w.VV0DcB = []
  VVC69w.VVYqos(VVcpnp.VVI1WG())
  for row in VVcpnp.VVGrbO():
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VVLLRh(1, showFound=True)
   num, lNum, titl, host, mac, cmnt = row
   if self.VVJLFc(host, mac, VVl2X5=False):
    token, profile, tErr = self.VV6cJP(VVl2X5=False)
    if token and VVC69w and not VVC69w.isCancelled:
     res, err = self.VV79mN(self.VViCnu("itv"))
     if res and VVC69w and not VVC69w.isCancelled:
      try:
       tot = len(jLoads(res.text)["js"])
       VVC69w.VVLLRh(0, showFound=True)
       VVC69w.VV0DcB.append((titl, host, mac, cmnt))
      except:
       pass
   if not VVC69w:
    return
 def VVpGfk(self, menuInstance, VVcpnp, path, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VV0DcB:
   VVcpnp.close()
   menuInstance.close()
   newPath = "%s_OK_%s.txt" % (path, FFGuM2())
   with open(newPath, "w") as f:
    for titl, host, mac, cmnt in VV0DcB:
     f.write("%s\t%s\t%s\t%s\n" % (titl, host, mac, cmnt))
   if threadTotal == threadCounter:
    totChk = str(threadCounter)
    skipped = ""
   else:
    totChk = FFkhYI(str(threadCounter), VVU8eD)
    skipped = FFkhYI(str(threadTotal - threadCounter), VVU8eD)
   txt  = "Total Portals\t: %d\n" %  threadTotal
   txt += "Checked\t: %s\n"  %  totChk
   if skipped:
    txt += "Cancelled\t: %s\n" %  skipped
   txt += "Accessible\t: %d\n\n" %  len(VV0DcB)
   txt += "%s\n\n%s"    %  (FFkhYI("Result File:", VVoTT6), newPath)
   FFNEkd(self, txt, title="Accessible Portals")
  elif VVr4Ej:
   FFkYsE(self, "No portal access found !", title="Accessible Portals")
 def VVPsid(self, iptvRef):
  host = mac = ""
  isPortalUrl = False
  if "chCode" in iptvRef:
   isPortalUrl = True
   iptvRef = iptvRef.replace("%3a", ":").replace("%3A", ":")
   span = iSearch(r"[A-Fa-f0-9]+:0:(?:[A-Fa-f0-9]+[:]){8}(.+)", iptvRef, IGNORECASE)
   if span:
    url  = span.group(1)
    try:
     res  = iUrlparse(url)
     tDict = iUrlparse_qs(res.query)
     chCode = tDict.get("chCode", [""])[0].strip()
     mac  = FFWbB4(chCode)
     if res.netloc:
      host = res.netloc
      if res.scheme:
       host = res.scheme + "://" + host
    except:
     pass
  return host, mac, isPortalUrl
 def VVmzTK(self):
  token, profile, tErr = self.VV6cJP()
  if token:
   dots = "." * self.VVfnCF
   dots += "+" if self.VVrIFf[1:2] == "p" else ""
   VV625J  = self.VV9NT4()
   OKBtnFnc = self.VVgAN3
   VVBfJP = ("Home Menu", FFSJQP)
   VVme6L = ("Bookmark Server", BF(CCqQHV.VVyq4W, self, True, self.VVPj61 + "\t" + self.VVrGQ8))
   FFuRfS(self, None, title="Portal Resources (MAC=%s) %s" % (self.VVrGQ8, dots), VV625J=VV625J, OKBtnFnc=OKBtnFnc, VVBfJP=VVBfJP, VVme6L=VVme6L)
 def VVgAN3(self, item=None):
  if item:
   menuInstance, title, ref, ndx = item
   if   ref == "live"   : mode = "itv"
   elif ref == "vod"   : mode = "vod"
   elif ref == "series"  : mode = "series"
   elif ref == "accountInfo" : mode = ""
   if mode : FFlX3B(menuInstance, BF(self.VVKORy, mode), title="Reading Categories ...")
   else : FFlX3B(menuInstance, BF(self.VVEOAA, menuInstance, title), title="Reading Account ...")
 def VVEOAA(self, menuInstance, title, forceMoreInfo=False):
  rows, totCols = self.VVPBb5(forceMoreInfo)
  title = "%s (MAC=%s)" % (title, self.VVrGQ8)
  VVMQj9  = ("Home Menu" , FFSJQP         , [])
  VV3th8  = None
  if VVF5vz:
   VV3th8 = ("Get JS"  , BF(self.VVOGbr, self.VVPj61), [])
  if totCols == 2:
   VV1QO7 = None
   header   = ("Subject" , "Value" )
   widths   = (43   , 57  )
   searchCol  = 0
  else:
   VV1QO7 = ("More Info.", BF(self.VVZiE3, menuInstance)  , [])
   header   = ("Num", "User/Server" , "Subject" , "Value" )
   widths   = (0 , 15   , 35  , 50  )
   searchCol  = 2
  FF1dQ4(self, None, title=title, width=1200, header=header, VVvytR=rows, VVoJsQ=widths, VVmp7B=26, VVMQj9=VVMQj9, VV3th8=VV3th8, VV1QO7=VV1QO7, VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000", searchCol=searchCol)
 def VVOGbr(self, url, VVcpnp, title, txt, colList):
  FFlX3B(VVcpnp, BF(self.VVdFzC, url), title="Getting JS ...")
 def VVdFzC(self, url):
  txt = "// Host\t: %s\n" % url
  verOK = False
  ver, err = self.VV0GSF("%s/c/version.js" % url)
  if err:
   txt += err
  else:
   txt += "// Version\t: %s\n\n" % ver
   js, err = self.VV0GSF("%s/c/xpcom.common.js" % url)
   if err: txt += err
   else  : txt += "%s" % js
  FFNEkd(self, txt, title="JS Info", outputFileToSave="Server_xpcom.common.js")
 def VV0GSF(self, url):
  res, err = self.VV79mN(url)
  if err:
   return "", "Error: %s" % err
  else:
   cont = res.headers.get("content-type")
   if "javascript" in cont : return res.text, ""
   else     : return "", "\nError: content-type = %s" % cont
 def VVZiE3(self, menuInstance, VVcpnp, title, txt, colList):
  VVcpnp.cancel()
  FFlX3B(menuInstance, BF(self.VVEOAA, menuInstance, "Account Info.", forceMoreInfo=True), title="Reading Account ...")
 def VVKORy(self, mode):
  token, profile, tErr = self.VV6cJP()
  if not token:
   return
  res, err = self.VV79mN(self.VViCnu(mode))
  list = []
  if not err:
   try:
    tDict = jLoads(res.text)
    if tDict:
     VVAE0x = CCD3Dl()
     chList = tDict["js"]
     for item in chList:
      Id   = CCqQHV.VVvsIK(item, "id"       )
      Title  = CCqQHV.VVvsIK(item, "title"      )
      censored = CCqQHV.VVvsIK(item, "censored"     )
      Title = VVAE0x.VVyWSY(Title)
      if Title:
       isAll = Title.strip().lower() == "all"
       if not isAll or isAll and VVF5vz:
        list.append((Title.strip(), Id))
   except:
    pass
  title = self.VV6ejl(mode)
  if list:
   list.sort(key=lambda x: x[0].lower())
   VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ(mode)
   mName = self.VV6ejl(mode)
   VVVHmY   = ("Show List"   , BF(self.VVN3Nj, mode)   , [])
   VVMQj9  = ("Home Menu"   , FFSJQP        , [])
   if mode in ("vod", "series"):
    VVOtSO = ("Find in %s" % mName , BF(self.VViGm0, mode, False), [])
    VV1QO7 = ("Find in Selected" , BF(self.VViGm0, mode, True) , [])
   else:
    VVOtSO = None
    VV1QO7 = None
   header   = None
   widths   = (100   , 0  )
   FF1dQ4(self, None, title=title, width=1200, header=header, VVvytR=list, VVoJsQ=widths, VVmp7B=30, VVMQj9=VVMQj9, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VVVHmY=VVVHmY, VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVghPi, VV0g1U=VV0g1U, lastFindConfigObj=CFG.lastFindIptv)
  else:
   s = "Authorization failed"
   if err:
    txt = err
   elif s in res.text:
    txt = s
    if self.VVlrb6:
     txt += "\n\n( %s )" % self.VVlrb6
   else:
    txt = "Could not get Categories from server!"
   FFkYsE(self, txt, title=title)
 def VVb1PK(self, mode, VVcpnp, title, txt, colList):
  FFlX3B(VVcpnp, BF(self.VVAxt9, mode, VVcpnp, title, txt, colList), title="Downloading ...")
 def VVAxt9(self, mode, VVcpnp, title, txt, colList):
  token, profile, tErr = self.VV6cJP()
  if not token:
   return
  seriesName = colList[1]
  catID  = colList[2]
  res, err  = self.VV79mN(self.VV4Pya(catID))
  list = []
  if not err:
   try:
    tDict = jLoads(res.text)
    if tDict:
     chList  = tDict["js"]['data']
     for item in chList:
      Id    = CCqQHV.VVvsIK(item, "id"    )
      actors   = CCqQHV.VVvsIK(item, "actors"   )
      added   = CCqQHV.VVvsIK(item, "added"   )
      age    = CCqQHV.VVvsIK(item, "age"   )
      category_id  = CCqQHV.VVvsIK(item, "category_id" )
      description  = CCqQHV.VVvsIK(item, "description" )
      director  = CCqQHV.VVvsIK(item, "director"  )
      genres_str  = CCqQHV.VVvsIK(item, "genres_str"  )
      name   = CCqQHV.VVvsIK(item, "name"   )
      path   = CCqQHV.VVvsIK(item, "path"   )
      screenshot_uri = CCqQHV.VVvsIK(item, "screenshot_uri" )
      series   = CCqQHV.VVvsIK(item, "series"   )
      cmd    = CCqQHV.VVvsIK(item, "cmd"   )
      cmd    = cmd.replace("ffmpeg ", "")
      for episode in eval(series):
       list.append((seriesName, name, str(episode), category_id, Id, added, age, cmd, director, genres_str, actors, description, screenshot_uri, path))
   except:
    pass
  if list:
   list.sort(key=lambda x: (x[1], int(x[2])))
   VVVHmY  = ("Play"    , BF(self.VVXRbr, mode)       , [])
   VV01dN = (""     , BF(self.VViaYz, mode)     , [])
   VVMQj9 = ("Home Menu"   , FFSJQP            , [])
   VV3th8 = ("Download Options" , BF(self.VVIM21, mode, "sp", seriesName) , [])
   VVOtSO = ("Options"   , BF(self.VVbsEO, "pEp", mode, seriesName) , [])
   header   = ("Name" , "Season" , "Episode" , "catID" , "ID" , "Added" , "Age" , "cmd" , "Director", "Genre" , "Actors" , "Description" , "Screenshot" , "Path")
   widths   = (65  , 20  , 15  , 0   , 0   , 0.01 , 0.01 , 0  , 0.01  , 0.01  , 0   , 0    , 0    , 0  )
   VVQqg2  = (LEFT  , LEFT  , CENTER , LEFT  , LEFT  , LEFT , LEFT , LEFT , LEFT  , LEFT  , LEFT  , LEFT   , LEFT   , LEFT )
   FF1dQ4(self, None, title=seriesName, width=1200, header=header, VVvytR=list, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000")
  else:
   FFkYsE(self, "Could not get Episodes from server!", title=seriesName)
 def VViGm0(self, mode, searchInCat, VVcpnp, title, txt, colList):
  searchCatId = colList[1].strip() if searchInCat else ""
  VV625J = []
  VV625J.append(("Keyboard"  , "manualEntry"))
  VV625J.append(("From Filter" , "fromFilter"))
  FFuRfS(self, BF(self.VV7WLE, VVcpnp, mode, searchCatId), title="Input Type", VV625J=VV625J, width=400)
 def VV7WLE(self, VVcpnp, mode, searchCatId, item=None):
  if item is not None:
   if   item == "manualEntry":
    FFbRXK(self, BF(self.VVcqZ3, VVcpnp, mode, searchCatId), defaultText=CFG.lastFindIptv.getValue(), title="Find", message="Enter Name (or names separated by a comma)")
   elif item == "fromFilter":
    filterObj = CCU3qf(self)
    filterObj.VVmiWt(BF(self.VVcqZ3, VVcpnp, mode, searchCatId))
 def VVcqZ3(self, VVcpnp, mode, searchCatId, item):
  if not item is None:
   searchName = item.strip()
   FFnT3A(CFG.lastFindIptv, searchName)
   title = self.VVm4JW(mode, searchName)
   if "," in searchName : FFkYsE(self, "Use only one word to search in Portal Servers !\n\nRemove the comma.", title=title)
   elif len(searchName) < 3: FFkYsE(self, "Enter at least 3 characters.", title=title)
   else     :
    VVAE0x = CCD3Dl()
    if CFG.hideIptvServerAdultWords.getValue() and VVAE0x.VVn2Iq([searchName]):
     FFkYsE(self, VVAE0x.VV2tDQ(), title=title)
    else:
     self.VV2h6r(mode, searchName, "", searchName, searchCatId)
 def VVN3Nj(self, mode, VVcpnp, title, txt, colList):
  bName = colList[0].strip()
  catID = colList[1].strip()
  self.VV2h6r(mode, bName, catID, "", "")
 def VV2h6r(self, mode, bName, catID, searchName, searchCatId):
  self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
      , titlePrefix = "Reading from server"
      , fncToRun  = BF(self.VVwcp2, mode, bName, catID, searchName, searchCatId)
      , VVnFNJ = BF(self.VVqqxk, mode, bName, catID, searchName, searchCatId))
 def VVqqxk(self, mode, bName, catID, searchName, searchCatId, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if searchName : title = self.VVm4JW(mode, searchName)
  else   : title = "%s : %s" % (self.VV6ejl(mode), bName)
  if VV0DcB:
   VV3th8 = None
   VVOtSO = None
   if mode == "series":
    VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ("series2")
    VVVHmY  = ("Episodes"   , BF(self.VVb1PK, mode)           , [])
   else:
    VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ("")
    VVVHmY  = ("Play"    , BF(self.VVXRbr, mode)           , [])
    VV3th8 = ("Download Options" , BF(self.VVIM21, mode, "vp" if mode == "vod" else "", "") , [])
    VVOtSO = ("Options"   , BF(self.VVbsEO, "pCh", mode, bName)      , [])
   VV01dN = (""      , BF(self.VVkH1y, mode)         , [])
   VVMQj9 = ("Home Menu"    , FFSJQP                , [])
   header   = ("Num" , "Name", "catID", "genreID" , "Icon", "cmd" , "Category/Genre" , "Logo")
   widths   = (9  , 60  , 0   , 0     , 0  , 0  , 25    , 6  )
   VVQqg2  = (CENTER, LEFT  , CENTER , CENTER  , LEFT , LEFT , LEFT    , CENTER)
   VVcpnp = FF1dQ4(self, None, title=title, header=header, VVvytR=VV0DcB, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VVVHmY=VVVHmY, VV01dN=VV01dN, VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVghPi, VV0g1U=VV0g1U, VVKNen=True, searchCol=1)
   if not VVr4Ej:
    if not threadCounter == threadTotal:
     tot = " (Stopped at %d of %d) " % (threadCounter, threadTotal)
     VVcpnp.VVX6S3(VVcpnp.VVmgxl() + tot)
    if threadErr: FFD1yO(VVcpnp, "Error while reading !", 2000)
    else  : FFD1yO(VVcpnp, "Stopped at channel %s" % threadCounter, 1000)
  else:
   if searchName : FFkYsE(self, "Could not find names with:\n\n%s" % searchName, title=title)
   else   : FFkYsE(self, "Could not get list from server !", title=title)
 def VVkH1y(self, mode, VVcpnp, title, txt, colList):
  if mode == "series":
   chName = colList[1]
   picUrl = colList[4]
   txt  = "%s\n\n%s" % (title, txt)
   FFBatl(self, fncMode=CCARMv.VV3BDs, portalHost=self.VVPj61, portalMac=self.VVrGQ8, chName=chName, text=txt, picUrl=picUrl)
  else:
   self.VV9PJK(mode, VVcpnp, title, txt, colList)
 def VViaYz(self, mode, VVcpnp, title, txt, colList):
  txt += "\n"
  txt += "Actors:\n%s\n\n" % FFkhYI(colList[10], VVkXS4)
  txt += "Description:\n%s" % FFkhYI(colList[11], VVkXS4)
  self.VV9PJK(mode, VVcpnp, title, txt, colList)
 def VV9PJK(self, mode, VVcpnp, title, txt, colList):
  chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, colList)
  refCode, chUrl = self.VVWeZp(self.VVPj61, self.VVrGQ8, mode, chName, catID, stID, chNum, chCm, serCode, serId)
  txt = "%s\n\n%s" % (title, txt)
  FFBatl(self, fncMode=CCARMv.VViZAY, callingSELF=self, portalMode=mode, refCode=refCode, chName=chName, text=txt, picUrl=picUrl, chCm=chCm, serCode=serCode, serId=serId)
 def VVwcp2(self, mode, bName, catID, searchName, searchCatId, VVC69w):
  try:
   token, profile, tErr = self.VV6cJP()
   if not token:
    return
   if VVC69w.isCancelled:
    return
   VVC69w.VV0DcB, total_items, max_page_items, err = self.VVQ45C(mode, catID, 1, 1, searchName, searchCatId)
   if VVC69w.isCancelled:
    return
   if VVC69w.VV0DcB and total_items > -1 and max_page_items > -1:
    VVC69w.VVYqos(total_items)
    VVC69w.VVLLRh(max_page_items, True)
    pages = int(iCeil(float(total_items) / float(max_page_items)))
    total_items = pages
    for i in range(pages - 1):
     if VVC69w.isCancelled:
      return
     page = i + 2
     counter = (i + 1) * max_page_items + 1
     list, total_items, max_page_items, err = self.VVQ45C(mode, catID, page, counter, searchName, searchCatId)
     if err:
      VVC69w.VVon0e()
     if VVC69w.isCancelled:
      return
     if list:
      VVC69w.VV0DcB += list
      VVC69w.VVLLRh(len(list), True)
  except:
   pass
 def VVQ45C(self, mode, catID, page, counter, searchName, searchCatId):
  list  = []
  total_items = max_page_items = -1
  if searchName : url = self.VVbPdK(mode, searchName, searchCatId, page)
  else   : url = self.VVL6LN(mode, catID, page)
  res, err = self.VV79mN(url)
  if not err:
   try:
    tDict = jLoads(res.text)
    if tDict:
     item = tDict["js"]
     total_items  = self.VVUzTe(CCqQHV.VVvsIK(item, "total_items" ))
     max_page_items = self.VVUzTe(CCqQHV.VVvsIK(item, "max_page_items" ))
     VVAE0x = CCD3Dl()
     chList = tDict["js"]['data']
     cmdStr = "http://localhost/ch/"
     for item in chList:
      Id    = CCqQHV.VVvsIK(item, "id"    )
      name   = CCqQHV.VVvsIK(item, "name"   )
      o_name   = CCqQHV.VVvsIK(item, "o_name"   )
      tv_genre_id  = CCqQHV.VVvsIK(item, "tv_genre_id" )
      number   = CCqQHV.VVvsIK(item, "number"   ) or str(counter)
      logo   = CCqQHV.VVvsIK(item, "logo"   )
      screenshot_uri = CCqQHV.VVvsIK(item, "screenshot_uri" )
      cmd    = CCqQHV.VVvsIK(item, "cmd"   )
      censored  = CCqQHV.VVvsIK(item, "censored"  )
      genres_str  = CCqQHV.VVvsIK(item, "genres_str"  )
      if name == "video_name_format" and o_name:
       name = o_name
      if " " in cmd and cmdStr in cmd:
       cmd = cmd.split(" ")[1]
      if mode == "itv" and not cmdStr in cmd and not cmd.endswith(".m3u8") and not "ffrt" in cmd:
       span = iSearch(r"stream=(.+)&", cmd)
       if span:
        cmd = "%s%s_" % (cmdStr, span.group(1))
       else:
        span = iSearch(r".+\/.+\/.+\/(.+)", cmd)
        if span:
         cmd = "%s%s_" % (cmdStr, span.group(1))
      picon = logo or screenshot_uri
      isIcon = "Yes" if picon else ""
      sp = "/stalker_portal"
      if picon.startswith(sp):
       picon = (self.VVPj61 + picon).replace(sp * 2, sp)
      counter += 1
      name = VVAE0x.VV16ZS(name, censored)
      if name:
       list.append((number, name, Id, tv_genre_id, picon, cmd, genres_str, isIcon))
   except:
    err = "Channel Parse Error !"
  return list, total_items, max_page_items, err
 def VVUzTe(self, valStr):
  try:
   return int(valStr)
  except:
   return -1
 def VVXRbr(self, mode, VVcpnp, title, txt, colList):
  chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, colList)
  refCode, chUrl = self.VVWeZp(self.VVPj61, self.VVrGQ8, mode, chName, catID, stID, chNum, chCm, serCode, serId)
  if self.VVmaA2(chName):
   FFD1yO(VVcpnp, "This is a marker!", 300)
  else:
   FFlX3B(VVcpnp, BF(self.VVaI1j, mode, VVcpnp, chUrl), title="Playing ...")
 def VVaI1j(self, mode, VVcpnp, chUrl):
  FFJZ42(self, chUrl, VVpyjK=False)
  CCppdx.VVgElN(self.session, iptvTableParams=(self, VVcpnp, mode))
 def VVJOnF(self, mode, VVcpnp, colList):
  chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, colList)
  refCode, chUrl = self.VVWeZp(self.VVPj61, self.VVrGQ8, mode, chName, catID, stID, chNum, chCm, serCode, serId)
  return chName, chUrl
 def VVrhWs(self, mode, colList):
  if mode == "series":
   chName = colList[0]
   season = colList[1]
   serCode = colList[2]
   catID = colList[3]
   serId = colList[4]
   chCm = colList[7]
   picUrl = colList[12]
   chName = "%s (%s - %s)" % (chName, season, serCode)
   chNum = serCode
   stID = serId.replace(":", "")
  else:
   chNum = colList[0]
   chName = colList[1]
   catID = colList[2]
   picUrl = colList[4]
   chCm = colList[5]
   stID = catID
   serCode = ""
   serId = ""
  return chName.strip(), catID.strip(), stID.strip(), chNum.strip(), chCm.strip(), serCode.strip(), serId.strip(), picUrl.strip()
 @staticmethod
 def VVStEc(SELF):
  try:
   import requests
   return True
  except:
   title = 'Install "Requests"'
   VV625J = []
   VV625J.append((title        , "inst" ))
   VV625J.append(("Update Packages then %s" % title , "updInst" ))
   FFuRfS(SELF, BF(CC6sg1.VVqRKJ, SELF), title='This requires Python "Requests" library', VV625J=VV625J)
   return False
 @staticmethod
 def VVqRKJ(SELF, item=None):
  if item:
   from sys import version_info
   cmdUpd = FFaG6T(VVRq5s, "")
   if cmdUpd:
    cmdInst = FFQ7Q5(VV4pye, "python-requests")
    if version_info[0] >= 3:
     cmdInst = cmdInst.replace("python-", "python3-")
    if   item == "inst"  : cmd = cmdInst
    elif item == "updInst" : cmd = cmdUpd + " && " + cmdInst
    FFfbee(SELF, cmd, checkNetAccess=True, title='Installing "Requests" Library')
   else:
    FFHRK6(SELF)
class CCqQHV(Screen, CC6sg1, CC2LVn):
 VVmFH3    = 0
 VVub1F    = 1
 VV3DFJ    = 2
 VVYrjF    = 3
 VVVtaO     = 4
 VVHOMm     = 5
 VVmxL3     = 6
 VVQVS1     = 7
 VVSJlZ     = 8
 VV4YaG      = 9
 VVtssf     = 10
 VVUhbg     = 11
 VVdr1w     = 12
 VVbfFF     = 13
 VVdT8X      = 14
 VVS3tv      = 15
 VVdauk      = 16
 VV2c5y      = 17
 VVW3xs      = 18
 VV15Af    = 0
 VVZ3on   = 1
 VVzxcn   = 2
 VVTVFh   = 3
 VV9YnV  = 4
 VVeOl5  = 5
 VV3zJB   = 6
 VV3qLZ   = 7
 VV47C9  = 8
 VV3KJK  = 9
 VVUdRa  = 10
 VVVOMv = 0
 VVETmZ = 1
 def __init__(self, session, m3uOrM3u8File=None):
  self.skin, self.skinParam = FF896P(VVoxS0, 1050, 1000, 50, 40, 30, "#0a001a20", "#0a001a20", 28)
  self.session     = session
  self.m3uOrM3u8File    = m3uOrM3u8File
  self.m3uOrM3u8BName    = ""
  self.VVcpnp    = None
  self.tableTitle     = "IPTV Channels List"
  self.VVozODData    = {}
  self.localIptvFilterInFilter = False
  self.iptvFileAvailable   = CCqQHV.VVJ90G(atLeastOne=True)
  CC6sg1.__init__(self)
  VV625J = []
  VV625J.append(("IPTV Server Browser (from Playlists)"     , "VVozOD_fromPlayList" ))
  VV625J.append(("IPTV Server Browser (from Portal List)"    , "VVozOD_fromMac"  ))
  VV625J.append(("IPTV Server Browser (from M3U/M3U8 Subscription File)", "VVozOD_fromM3u"  ))
  qUrl, iptvRef = self.VVAmSO()
  item = "IPTV Server Browser (from Current Channel)"
  if qUrl or "chCode" in iptvRef : VV625J.append((item     , "VVozOD_fromCurrChan" ))
  else       : VV625J.append((item     ,       ))
  VV625J.append(VVm77t)
  VV625J.append(("M3U/M3U8 File Browser"        , "VVyWVM"   ))
  if self.iptvFileAvailable:
   VV625J.append(("Local IPTV Services"        , "iptvTable_all"   ))
  VV625J.append(VVm77t)
  item1 = "Update Current Bouquet EPG (from IPTV Server)"
  item2 = "Update Current Bouquet PIcons (from IPTV Server)"
  if qUrl or "chCode" in iptvRef:
   VV625J.append((item1            , "refreshIptvEPG"   ))
   VV625J.append((item2            , "refreshIptvPicons"  ))
  else:
   VV625J.append((item1            ,       ))
   VV625J.append((item2            ,       ))
  if self.iptvFileAvailable:
   VV625J.append(VVm77t)
   c1, c2 = VVNTmM, VVoTT6
   t1 = FFkhYI("auto-match names", VVTdoW)
   t2 = FFkhYI("from xml file"  , VVTdoW)
   VV625J.append((c1 + "Count Available IPTV Channels"    , "VVanJw"    ))
   VV625J.append((c1 + "Copy EPG/PIcons between Channels (%s)" % t2 , "copyEpgPicons"   ))
   VV625J.append(VVm77t)
   VV625J.append((c2 + "Share Reference with DVB Channels (%s)" % t2 , "renumIptvRef_fromFile" ))
   VV625J.append((c2 + "Share Reference with DVB Channels (%s)" % t1 , "VVXOYA" ))
   VV625J.append((VVMmz2 + "More Reference Tools ..."  , "VVbn0d"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Reload Channels and Bouquets"       , "VVQG6O"   ))
  VV625J.append(VVm77t)
  if not CC9Zvn.VVwsNU():
   VV625J.append(("Download Manager"         , "dload_stat"    ))
  else:
   VV625J.append(("Download Manager ... No donwloads"    ,       ))
  FFJd2Z(self, title="IPTV", VV625J=VV625J)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
  FFqx5h(self)
  if self.m3uOrM3u8File:
   self.VVt26x(self.m3uOrM3u8File)
 def VVI8HV(self, item):
  tTitle = "Share Reference with DVB Service"
  if item is not None:
   title = "Searching ..."
   if   item == "VVmhaW"   : self.VVmhaW()
   elif item == "VVTigh" : FFMIbO(self, self.VVTigh, "Change Current List References to Unique Codes ?")
   elif item == "VV1lnR_rows" : FFMIbO(self, BF(FFlX3B, self.VVcpnp, self.VV1lnR), "Change Current List References to Identical Codes ?")
   elif item == "VViay2"   : self.VViay2(tTitle)
   elif item == "VVjCr7"   : self.VVjCr7(tTitle)
   elif item == "VVozOD_fromPlayList" : FFlX3B(self, BF(self.VVDqjN, 1), title=title)
   elif item == "VVozOD_fromM3u"  : FFlX3B(self, BF(self.VVm0c2, 0), title=title)
   elif item == "VVozOD_fromMac"  : self.VV4wRZ()
   elif item == "VVozOD_fromCurrChan" : self.VVf1jy()
   elif item == "VVyWVM"   : self.VVyWVM()
   elif item == "iptvTable_all"   : FFlX3B(self, BF(self.VVKhmA, self.VVmFH3), title="Loading Channels ...")
   elif item == "refreshIptvEPG"   : self.VVNgba()
   elif item == "refreshIptvPicons"  : self.VVVkyv()
   elif item == "VVanJw"    : FFlX3B(self, self.VVanJw)
   elif item == "copyEpgPicons"   : self.VVpp9G(False)
   elif item == "renumIptvRef_fromFile" : self.VVpp9G(True)
   elif item == "VVXOYA" : FFMIbO(self, BF(FFlX3B, self, self.VVXOYA), VVSidL="Continue ?")
   elif item == "VVbn0d"    : self.VVbn0d()
   elif item == "VVQG6O"   : FFlX3B(self, BF(CCtSdI.VVQG6O, self))
   elif item == "dload_stat"    : CC9Zvn.VV4aex(self)
 def VVyWVM(self):
  if CC6sg1.VVStEc(self):
   FFlX3B(self, BF(self.VVm0c2, 1), title="Searching ...")
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  self.VVI8HV(item)
 def VVKhmA(self, mode):
  VVvhuK = self.VVjbF3(mode)
  if VVvhuK:
   VV3th8 = ("Current Service", self.VV8PVa , [])
   VVOtSO = ("Options"  , self.VV2Yj8   , [])
   VV1QO7 = ("Filter"   , self.VVAHhV   , [])
   VVVHmY  = ("Play"   , BF(self.VVnuUJ)  , [])
   VV01dN = (""    , self.VVA6ny    , [])
   VVKx4L = (""    , self.VVJ4Ak     , [])
   header   = ("Num" , "Name", "Bouquet" , "Type", "Ref.", "URL" )
   widths   = (9  , 22 , 18  , 6  , 22 , 23 )
   VVQqg2  = (CENTER , LEFT , LEFT  , CENTER, LEFT , LEFT )
   FF1dQ4(self, None, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26
     , VVVHmY=VVVHmY, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VV01dN=VV01dN, VVKx4L=VVKx4L
     , VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000", VVKNen=True, searchCol=1)
  else:
   if mode == self.VVSJlZ: err = "No Live IPTV channels !"
   else       : err = "No IPTV channels !"
   FFkYsE(self, err)
 def VVJ4Ak(self, VVcpnp, title, txt, colList):
  self.VVcpnp = VVcpnp
 def VV2Yj8(self, VVcpnp, title, txt, colList):
  VV625J = []
  VV625J.append(("Add Current List to a New Bouquet"    , "VVmhaW"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Change Current List References to Unique Codes" , "VVTigh"))
  VV625J.append(("Change Current List References to Identical Codes", "VV1lnR_rows" ))
  VV625J.append(VVm77t)
  VV625J.append(("Share Reference with DVB Service (manual entry)" , "VViay2"   ))
  VV625J.append(("Share Reference with DVB Service (auto-find)"  , "VVjCr7"   ))
  FFuRfS(self, self.VVI8HV, title="IPTV Tools", VV625J=VV625J)
 def VVAHhV(self, VVcpnp, title, txt, colList):
  VV625J = []
  VV625J.append(("All"         , "all"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Prefix of Selected Channel"   , "sameName" ))
  VV625J.append(("Suggest Words from Selected Channel" , "partName" ))
  VV625J.append(("Names with Non-English Characters" , "nonEnglish" ))
  VV625J.append(("Duplicate References"     , "depRef"  ))
  VV625J.append(("Reference x:x:x:x:0:0:0:0:0:0:"  , "ref00"  ))
  VV625J.append(FFi9aC("Category"))
  VV625J.append(("Live TV"        , "live"  ))
  VV625J.append(("VOD"         , "vod"   ))
  VV625J.append(("Series"        , "series"  ))
  VV625J.append(("Uncategorised"      , "uncat"  ))
  VV625J.append(FFi9aC("Media"))
  VV625J.append(("Video"        , "video"  ))
  VV625J.append(("Audio"        , "audio"  ))
  VV625J.append(FFi9aC("File Type"))
  VV625J.append(("MKV"         , "MKV"   ))
  VV625J.append(("MP4"         , "MP4"   ))
  VV625J.append(("MP3"         , "MP3"   ))
  VV625J.append(("AVI"         , "AVI"   ))
  VV625J.append(("FLV"         , "FLV"   ))
  VV625J.extend(CCgKdM.VVJtDO(prefix="__b__"))
  inFilterFnc = BF(self.VVF1hh, VVcpnp) if VVcpnp.VVmgxl().startswith("IPTV Filter ") else None
  filterObj = CCU3qf(self)
  filterObj.VVxv80(VV625J, VV625J, BF(self.VVuLNE, VVcpnp, False), inFilterFnc=inFilterFnc)
 def VVF1hh(self, VVcpnp, menuInstance, item):
  self.VVuLNE(VVcpnp, True, item)
 def VVuLNE(self, VVcpnp, inFilter, item=None):
  self.localIptvFilterInFilter = inFilter
  prefix = VVcpnp.VVQYAy(1).split(" ")[0]
  if item is not None:
   f = "IPTV Filter "
   if   item == "all"    : mode, words, title = self.VVmFH3 , ""  , self.tableTitle
   elif item == "sameName"   : mode, words, title = self.VVub1F , prefix , f + "= %s ..." % prefix
   elif item == "partName"   : mode, words, title = self.VV3DFJ , ""  , ""
   elif item == "nonEnglish"  : mode, words, title = self.VVYrjF , ""  , f + "= Names with Non-English Characters"
   elif item == "depRef"   : mode, words, title = self.VVmxL3  , ""  , f + "= Duplicate References"
   elif item == "ref00"   : mode, words, title = self.VVQVS1  , ""  , f + "= Reference x:x:x:x:0:0:0:0:0:0:"
   elif item == "live"    : mode, words, title = self.VVSJlZ  , ""  , f + "= Live"
   elif item == "vod"    : mode, words, title = self.VV4YaG   , ""  , f + "= VOD"
   elif item == "series"   : mode, words, title = self.VVtssf  , ""  , f + "= Series"
   elif item == "uncat"   : mode, words, title = self.VVUhbg  , ""  , f + "= Uncategorised"
   elif item == "video"   : mode, words, title = self.VVdr1w  , ""  , f + "= Video"
   elif item == "audio"   : mode, words, title = self.VVbfFF  , ""  , f + "= Audio"
   elif item == "MKV"    : mode, words, title = self.VVdT8X   , ""  , f + "= MKV"
   elif item == "MP4"    : mode, words, title = self.VVS3tv   , ""  , f + "= MP4"
   elif item == "MP3"    : mode, words, title = self.VVdauk   , ""  , f + "= MP3"
   elif item == "AVI"    : mode, words, title = self.VV2c5y   , ""  , f + "= AVI"
   elif item == "FLV"    : mode, words, title = self.VVW3xs   , ""  , f + "= FLV"
   elif item.startswith("__b__") : mode, words, title = self.VVVtaO  , item[5:] , f + "Bouquets = " + item[5:]
   elif item.startswith("__w__") : mode, words, title = self.VVHOMm  , item[5:] , f + "Name = "  + item[5:]
   else       : return
  if len(title) > 58:
   title = title[:58] + ".."
  if mode == self.VV3DFJ:
   VV625J = []
   chName = VVcpnp.VVQYAy(1)
   if chName:
    list = set()
    for match in iFinditer(r"((?:[^\x00-\x7F]+\s*)+)", chName, IGNORECASE):
     list.add(match.group(1).strip())
    if list:
     for match in iFinditer(r"(\w+)", chName, IGNORECASE):
      list.add(match.group(1).strip())
    words = chName.split(" ")
    tWord = ""
    for word in words:
     tWord += " " + word
     list.add(word.strip())
     list.add(tWord.strip())
    for item in sorted(list):
     if item:
      VV625J.append((item, item))
    if not VV625J and chName:
     VV625J.append((chName, chName))
    FFuRfS(self, BF(self.VV1iWT, title), title="Words from Current Selection", VV625J=VV625J)
   else:
    VVcpnp.VVIX8q("Invalid Channel Name")
  else:
   words, asPrefix = CCU3qf.VVP88C(words)
   if not words and mode in (self.VVVtaO, self.VVHOMm):
    FFD1yO(self.VVcpnp, "Incorrect filter", 2000)
   else:
    FFlX3B(self.VVcpnp, BF(self.VV8gRB, mode, words, asPrefix, title), clearMsg=False, title="Filtering ...")
 def VV1iWT(self, title, word=None):
  if word:
   words = [word.lower()]
   FFlX3B(self.VVcpnp, BF(self.VV8gRB, self.VV3DFJ, words, False, title), clearMsg=False, title="Filtering ...")
 @staticmethod
 def VVy8pO(txt):
  return "#f#11ffff00#" + txt
 def VV8gRB(self, mode, words, asPrefix, title):
  if self.localIptvFilterInFilter : VVvhuK = self.VVaPh1(mode=mode, words=words, asPrefix=asPrefix)
  else       : VVvhuK = self.VVjbF3(mode=mode, words=words, asPrefix=asPrefix)
  if VVvhuK : self.VVcpnp.VVuVux(VVvhuK, title)
  else  : self.VVcpnp.VVIX8q("Not found")
 def VVaPh1(self, mode=0, words=None, asPrefix=False):
  VVvhuK = []
  for row in self.VVcpnp.VVGrbO():
   row = list(map(str.strip, row))
   chNum, chName, VVb6wY, chType, refCode, url = row
   if self.VVWAQG(mode, refCode, FF9CmS(url).lower(), chName, words, VVb6wY.lower(), asPrefix):
    VVvhuK.append(row)
  VVvhuK = self.VVeCQD(mode, VVvhuK)
  return VVvhuK
 def VVjbF3(self, mode=0, words=None, asPrefix=False, isStripChan=False):
  patt = r"#SERVICE\s+([A-Fa-f0-9]+:0:(?:[A-Fa-f0-9]+[:]){8})(http.+)\n#DESCRIPTION\s+"
  if isStripChan: patt += r"[^\x00-\x7F]*(.+)[^\x00-\x7F]*"
  else    : patt += r"(.+)"
  VVvhuK = []
  files  = self.VVRuow()
  if files:
   chNum = 1
   for path in files:
    if path.endswith("radio"): chType = "Radio"
    else      : chType = "TV"
    txt = FFqD66(path)
    span = iSearch(r"#NAME\s(.+)", txt, IGNORECASE)
    if span : VVb6wY = span.group(1)
    else : VVb6wY = ""
    VVb6wY_lCase = VVb6wY.lower()
    for match in iFinditer(patt, txt, IGNORECASE):
     refCode = match.group(1).upper()
     url  = match.group(2).strip()
     chName = match.group(3).strip()
     if self.VVmaA2(chName): chNameMod = self.VVy8pO(chName)
     else        : chNameMod = chName
     row = (str(chNum), chNameMod, VVb6wY, chType, refCode, url)
     if self.VVWAQG(mode, refCode, FF9CmS(url).lower(), chName, words, VVb6wY_lCase, asPrefix):
      VVvhuK.append(row)
      chNum += 1
  VVvhuK = self.VVeCQD(mode, VVvhuK)
  return VVvhuK
 def VVeCQD(self, mode, VVvhuK):
  newRows = []
  if VVvhuK and mode == self.VVmxL3:
   from collections import Counter
   counted  = Counter(elem[4] for elem in VVvhuK)
   for item in VVvhuK:
    tot = counted.get(item[4], 0)
    if tot > 1:
     newRows.append(item)
   return newRows
  else:
   return VVvhuK
 def VVWAQG(self, mode, refCode, tUrl, chName, words, VVb6wY_lCase, asPrefix):
  if   mode == self.VVmFH3 : return True
  elif mode == self.VVmxL3 : return True
  elif mode == self.VVQVS1  : return ":0:0:0:0:0:0:" in refCode
  elif mode == self.VVdr1w  : return CCqQHV.VVPus3(tUrl, getAudVid=True) == "vid"
  elif mode == self.VVbfFF  : return CCqQHV.VVPus3(tUrl, getAudVid=True) == "aud"
  elif mode == self.VVSJlZ  : return CCqQHV.VVPus3(tUrl, compareType="live")
  elif mode == self.VV4YaG  : return CCqQHV.VVPus3(tUrl, compareType="movie")
  elif mode == self.VVtssf : return CCqQHV.VVPus3(tUrl, compareType="series")
  elif mode == self.VVUhbg  : return CCqQHV.VVPus3(tUrl, compareType="")
  elif mode == self.VVdT8X  : return CCqQHV.VVPus3(tUrl, compareExt="mkv")
  elif mode == self.VVS3tv  : return CCqQHV.VVPus3(tUrl, compareExt="mp4")
  elif mode == self.VVdauk  : return CCqQHV.VVPus3(tUrl, compareExt="mp3")
  elif mode == self.VV2c5y  : return CCqQHV.VVPus3(tUrl, compareExt="avi")
  elif mode == self.VVW3xs  : return CCqQHV.VVPus3(tUrl, compareExt="flv")
  elif mode == self.VVub1F: return chName.lower().startswith(words[0])
  elif mode == self.VV3DFJ: return words[0] in chName.lower()
  elif mode == self.VVYrjF: return bool(iSearch(r"[^\x00-\x7F]", chName))
  elif mode == self.VVVtaO : return words[0] == VVb6wY_lCase
  elif mode == self.VVHOMm :
   name = chName.lower()
   for word in words:
    if asPrefix:
     if name.startswith(word) : return True
    elif word in name    : return True
  return False
 def VVmhaW(self):
  picker = CCgKdM(self, self.VVcpnp, "Add to Bouquet", self.VVqU5F)
 def VVqU5F(self):
  chUrlLst = []
  for row in self.VVcpnp.VVGrbO():
   chUrlLst.append(row[4] + row[5])
  return chUrlLst
 def VVbn0d(self):
  c1 = VVk6tE
  t1 = FFkhYI("Bouquet", VVTdoW)
  t2 = FFkhYI("ALL", VVTdoW)
  refTxt = "(1/4097/5001/5002/8192/8193)"
  VV625J = []
  VV625J.append((c1 + "Check System Acceptable Reference Types" , "VVDtVb"    ))
  if self.iptvFileAvailable:
   VV625J.append((c1 + "Check Reference Codes Format"  , "VVKoqk"    ))
  VV625J.append(VVm77t)
  VV625J.append(('Change %s Ref. Types to %s ..' % (t1, refTxt) , "VVaM3H" ))
  VV625J.append(('Change %s Ref. Types to %s ..' % (t2, refTxt) , "VV0sDU_all"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Change %s References to Unique Codes" % t2 , "VVyP8E"  ))
  VV625J.append(("Change %s References to Identical Codes" % t2 , "VV1lnR_all"  ))
  OKBtnFnc = self.VV9VKw
  FFuRfS(self, None, width=1200, title="Reference Tools", VV625J=VV625J, OKBtnFnc=OKBtnFnc)
 def VV9VKw(self, item=None):
  if item:
   ques = "Continue ?"
   menuInstance, txt, item, ndx = item
   if   item == "VVDtVb"    : FFlX3B(menuInstance, self.VVDtVb)
   elif item == "VVKoqk"     : FFlX3B(menuInstance, self.VVKoqk)
   elif item == "VVaM3H" : self.VVaM3H(menuInstance)
   elif item == "VV0sDU_all"  : self.VVi7zT(menuInstance, None, None)
   elif item == "VVyP8E"  : FFMIbO(self, BF(self.VVyP8E , menuInstance, txt), title=txt, VVSidL=ques)
   elif item == "VV1lnR_all"  : FFMIbO(self, BF(FFlX3B, menuInstance, self.VV1lnR), title=txt, VVSidL=ques)
 def VVi7zT(self, menuInstance, bName, bPath):
  txt = "Stream Type "
  VV625J = []
  VV625J.append(('%s 1      ( DVB Stream )'  % txt , "RT_1" ))
  VV625J.append(('%s 4097 ( servicemp3 )'  % txt , "RT_4097" ))
  VV625J.append(('%s 5001 ( GST Player )'  % txt , "RT_5001" ))
  VV625J.append(('%s 5002 ( Ext-3 EPlayer )' % txt , "RT_5002" ))
  VV625J.append(('%s 8192 ( HDMI input )'  % txt , "RT_8192" ))
  VV625J.append(('%s 8193 ( eServiceUri )'  % txt , "RT_8193" ))
  FFuRfS(self, BF(self.VVEykR, menuInstance, bName, bPath), width=750, title="Change Reference Types to:", VV625J=VV625J)
 def VVEykR(self, menuInstance, bName, bPath, item=None):
  if item:
   if   item == "RT_1"  : self.VVTGGC(menuInstance, bName, bPath, "1"   )
   elif item == "RT_4097" : self.VVTGGC(menuInstance, bName, bPath, "4097")
   elif item == "RT_5001" : self.VVTGGC(menuInstance, bName, bPath, "5001")
   elif item == "RT_5002" : self.VVTGGC(menuInstance, bName, bPath, "5002")
   elif item == "RT_8192" : self.VVTGGC(menuInstance, bName, bPath, "8192")
   elif item == "RT_8193" : self.VVTGGC(menuInstance, bName, bPath, "8193")
 def VVaM3H(self, menuInstance):
  VV625J = CCgKdM.VVJtDO()
  if VV625J:
   FFuRfS(self, BF(self.VVilQ4, menuInstance), VV625J=VV625J, title="IPTV Bouquets", VVeYEo=True)
  else:
   FFD1yO(menuInstance, "No bouquets Found !", 1500)
 def VVilQ4(self, menuInstance, item=None):
  if item:
   bName, bRef, ndx = item
   span = iSearch(r'BOUQUET "(.+)" ORDER', bRef, IGNORECASE)
   if span:
    bPath = VV609C + span.group(1)
    if fileExists(bPath): self.VVi7zT(menuInstance, bName, bPath)
    else    : FFD1yO(menuInstance, "Bouquet file not found!", 2000)
   else:
    FFD1yO(menuInstance, "Cannot process bouquet !", 2000)
 def VVTGGC(self, menuInstance, bName, bPath, rType):
  if bPath: title = "Change for Bouquet : %s" % FFkhYI(bName, VVdWFT)
  else : title = "Change for %s" % FFkhYI("All IPTV Services", VVdWFT)
  FFMIbO(self, BF(FFlX3B, menuInstance, BF(self.VV5a1L, menuInstance, bName, bPath, rType), title="Changing Type ...")
    , "Change to : %s ?" % FFkhYI(rType, VVdWFT), title=title)
 def VV5a1L(self, menuInstance, bName, bPath, rType):
  totChange = 0
  if bPath: files = [bPath]
  else : files = self.VVRuow()
  if files:
   newRType = rType + ":"
   piconPath = CCrs3r.VVsNIk()
   for path in files:
    if   not fileExists(path)      : err = "Cannot read the file:\n\n%s" % path
    elif not CC7ujK.VV4HLe(self, path) : err = "File is not in 'UTF-8' Encoding:\n\n%s" % path
    else           : err = ""
    if err:
     FFkYsE(self, err)
     return
    newpFile = path + ".tmp"
    totMod = 0
    with open(newpFile, "w") as tFile:
     with ioOpen(path, "r", encoding="utf-8") as f:
      for line in f:
       span = iSearch(r"#SERVICE\s+([A-Fa-f0-9]+[:]).+http.+", line)
       if span:
        oldRType = span.group(1)
        if not oldRType == newRType:
         totMod += 1
         totChange += 1
         span = iSearch(r"((?:[A-Fa-f0-9]+[:]){10})", line)
         if span : oldPicon = piconPath + span.group(1).strip(":").replace(":", "_") + ".png"
         else : oldPicon = ""
         line = iSub(r"(#SERVICE)\s+[A-Fa-f0-9]+[:](.+http.+)", r"\1 %s\2" % newRType, line)
         if fileExists(oldPicon):
          span = iSearch(r"((?:[A-Fa-f0-9]+[:]){10})", line)
          if span:
           os.system(FFxtg8("mv -f '%s' '%s'" % (oldPicon, piconPath + span.group(1).strip(":").replace(":", "_") + ".png")))
       tFile.write(line)
    if totMod: cmd = "mv -f '%s' '%s'" % (newpFile, path)
    else  : cmd = "rm -f '%s'" % newpFile
    os.system(FFxtg8(cmd))
  self.VVdFw4(totChange > 0, 'Change Ref. Codes to "%s"' % rType, "Changes = %d" % totChange)
 def VVanJw(self):
  totFiles = 0
  files  = self.VVRuow()
  if files:
   totFiles = len(files)
  totChans = 0
  VVvhuK = self.VVjbF3()
  if VVvhuK:
   totChans = len(VVvhuK)
  FFNEkd(self, "Total Files\t: %d\nTotal Channels\t: %d" % (totFiles, totChans))
 def VVKoqk(self):
  files  = self.VVRuow()
  if files:
   totInvalid = 0
   invTxt  = ""
   for path in files:
    txt = FFqD66(path)
    for match in iFinditer(r"#SERVICE\s+(?!(?:(?:[A-Fa-f0-9]+[:]){10})).+\n#DESCRIPTION\s+(.+)", txt, IGNORECASE):
     totInvalid += 1
     invTxt += "%s\t: %s\n" % (os.path.basename(path), match.group(1))
   if totInvalid == 0 : color = VV9cEK
   else    : color = VVU8eD
   totInvalid = FFkhYI(str(totInvalid), color)
   txt  = "Processed Files\t\t: %d\n" % len(files)
   txt += "Invalid References\t: %s\n" % totInvalid
   if invTxt:
    txt += FFkhYI("\nInvalid Refrences (File & Chan. Name):\n", color)
    txt += invTxt
  else:
   txt = "No IPTV Files processed."
  FFNEkd(self, txt, title="Check IPTV References")
 def VVDtVb(self):
  bName  = "%s_IPTV_TMP_BOUQUET_DEL" % PLUGIN_NAME
  userBName = "userbouquet.%s.tv"  % bName
  chPrefix = "Testing RType "
  rTypeList = ("1", "4097", "5001", "5002", "8192", "8193")
  chUrlLst  = []
  for rType in (rTypeList):
   ref = "%s:0:1:DDD:DDD:DDD:DDD:0:0:0:http%%3a//testUrl.com/aa/bb.m3u8:Testing RType %s" % (rType, rType)
   chUrlLst.append(ref)
  CCgKdM.VVLBiS(self, "", bName, "", chUrlLst, showRes=False)
  acceptedList = []
  VVfVMT = eServiceReference('1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet' % userBName)
  if VVfVMT:
   VVa6xc = FFocgD(VVfVMT)
   if VVa6xc:
    for service in VVa6xc:
     chName = service[1]
     acceptedList.append(chName.replace(chPrefix, ""))
  path = VV609C + userBName
  bFile = VV609C + "bouquets.tv"
  tmpF = bFile + ".tmp"
  cmd = FFxtg8("grep -v '%s' '%s' > '%s'; mv '%s' '%s'" % (userBName, bFile, tmpF, tmpF, bFile))
  cmd += ";"
  cmd += FFxtg8("rm -f '%s'" % path)
  os.system(cmd)
  FFlB9k()
  title = "System Acceptable Reference Types"
  if acceptedList:
   txt = ""
   for item in rTypeList:
    if item in acceptedList : res, color = "Yes", VV9cEK
    else     : res, color = "No" , VVU8eD
    txt += "    %s\t: %s\n" % (item, FFkhYI(res, color))
   FFNEkd(self, txt, title=title)
  else:
   txt = FFkYsE(self, "Could not complete the test on your system!", title=title)
 def VVXOYA(self):
  VVooHP, err = CCtSdI.VV4uiY(self, CCtSdI.VVG95i)
  if VVooHP:
   totChannels = 0
   totChange = 0
   for path in self.VVRuow():
    toSave = False
    txt = FFqD66(path)
    for match in iFinditer(r"(#SERVICE\s+[A-Fa-f0-9]+:)0:(?:[A-Fa-f0-9]+[:]){8}(.+\n#DESCRIPTION\s+(?:.+[:()|\]\[])*(.+))", txt, IGNORECASE):
     totChannels += 1
     chName = match.group(3).strip(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
     refCode = VVooHP.get(chName, "")
     if refCode:
      refCode  = refCode[refCode.index(":") + 1:]
      toSave  = True
      totChange += 1
      txt = txt.replace(match.group(0), match.group(1) + refCode + ":" + match.group(2))
    if toSave:
     with open(path, "w") as f:
      f.write(txt)
   txt  = "Channels\t: %d\n" % totChannels
   txt += "Changed\t: %d\n" % totChange
   self.VVdFw4(totChange > 0, "Copy Ref. from existing Channels", txt)
  else:
   FFkYsE(self, 'No channels in "lamedb" !')
 def VVyP8E(self, menuInstance, title):
  bFiles = self.VVRuow()
  if bFiles:
   self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
       , titlePrefix = "Renumbering References"
       , fncToRun  = BF(self.VVWnKy, bFiles)
       , VVnFNJ = BF(self.VVbP7q, title))
  else:
   FFD1yO(menuInstance, "No bouquets files !", 1500)
 def VVWnKy(self, bFiles, VVC69w):
  VVC69w.VV0DcB = ""
  VVC69w.VV1g3S("Calculating Reference ...")
  totLines = 0
  patt = r"#SERVICE\s+(?:[A-Fa-f0-9]+[:]){10}(.+\/\/.+)"
  for path in bFiles:
   if fileExists(path):
    lines = FFjdnJ(path)
    for line in lines:
     span = iSearch(patt, line)
     if span:
      totLines += 1
  if not VVC69w or VVC69w.isCancelled:
   return
  elif not totLines:
   VVC69w.VV0DcB = "No IPTV Services !"
   return
  else:
   VVC69w.VVYqos(totLines)
  rType = CFG.iptvAddToBouquetRefType.getValue()
  startId = startNS = 0
  for path in bFiles:
   if not VVC69w or VVC69w.isCancelled:
    return
   if fileExists(path):
    toSave = False
    bName  = os.path.basename(path)
    lines  = FFjdnJ(path)
    for ndx, line in enumerate(lines):
     if not VVC69w or VVC69w.isCancelled:
      return
     if ndx == 0:
      span = iSearch(r"#NAME\s+(.+)", line, IGNORECASE)
      if span:
       bName = span.group(1)
      if VVC69w:
       VVC69w.VV1g3S("Processing : %s " % bName)
     span = iSearch(patt, line)
     if span:
      if VVC69w:
       VVC69w.VVLLRh(1)
      refCode, startId, startNS = CCgKdM.VVp0RV(rType, CCgKdM.VVRiij, [], startId, startNS)
      if refCode:
       lines[ndx] = "#SERVICE %s" % (refCode + span.group(1))
       toSave = True
      else:
       if VVC69w:
        VVC69w.VV0DcB = "Out of Free References while processing the file:\n%s" % path
       return
    if toSave:
     with open(path, "w") as f:
      f.write("\n".join(lines) + "\n")
 def VVbP7q(self, title, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  txt  = "Found\t: %d\n"  % threadTotal
  txt += "Changed\t: %d\n" % threadCounter
  if VV0DcB:
   txt += "\n\n%s\n%s" % (FFkhYI("Ended with Error:", VVU8eD), VV0DcB)
  self.VVdFw4(True, title, txt)
 def VVTigh(self):
  bFiles = self.VVRuow()
  if not bFiles:
   FFD1yO(self.VVcpnp, "No bouquets files !", 1500)
   return
  tableRefList = []
  for row in self.VVcpnp.VVGrbO():
   tableRefList.append((row[4], row[5]))
  if not tableRefList:
   FFD1yO(self.VVcpnp, "Cannot read list", 1500)
   return
  self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
      , titlePrefix = "Renumbering References"
      , fncToRun  = BF(self.VVXwVq, bFiles, tableRefList)
      , VVnFNJ = BF(self.VVbP7q, "Change Current List References to Unique Codes"))
 def VVXwVq(self, bFiles, tableRefList, VVC69w):
  VVC69w.VV0DcB = ""
  VVC69w.VV1g3S("Reading System References ...")
  refLst = CCgKdM.VVvOrZ(CCgKdM.VVRiij, stripRType=True)
  if not VVC69w or VVC69w.isCancelled:
   return
  VVC69w.VVYqos(len(tableRefList))
  rType  = CFG.iptvAddToBouquetRefType.getValue()
  startId = startNS = 0
  for path in bFiles:
   if not VVC69w or VVC69w.isCancelled:
    return
   if fileExists(path):
    toSave = False
    bName = os.path.basename(path)
    txt  = FFqD66(path)
    span = iSearch(r"#NAME\s+(.+)", txt, IGNORECASE)
    if span:
     bName = span.group(1)
    if not VVC69w or VVC69w.isCancelled:
     return
    VVC69w.VV1g3S("Processing : %s " % bName)
    for ref, url in tableRefList:
     if not VVC69w or VVC69w.isCancelled:
      return
     fullRef = ref + url
     if fullRef in txt:
      VVC69w.VVLLRh(1)
      refCode, startId, startNS = CCgKdM.VVp0RV(rType, CCgKdM.VVRiij, refLst, startId, startNS)
      if refCode:
       tot = txt.count(fullRef)
       if tot > 0:
        txt = txt.replace(fullRef, refCode + url)
        toSave = True
      else:
       if VVC69w:
        VVC69w.VV0DcB = "Out of Free References while processing the file:\n%s" % path
       return
    if toSave:
     with open(path, "w") as f:
      f.write(txt)
 def VV1lnR(self):
  list = None
  if self.VVcpnp:
   list = []
   for row in self.VVcpnp.VVGrbO():
    list.append(row[4] + row[5])
  files  = self.VVRuow()
  totChange = 0
  if files:
   for path in files:
    lines = FFjdnJ(path)
    toSave = False
    for ndx, line in enumerate(lines):
     span = iSearch(r"#SERVICE\s+(.+\/\/.+)", line, IGNORECASE)
     if span:
      if not list or span.group(1) in list:
       txt, tot = iSubn(r"(#SERVICE\s+(?:[A-Fa-f0-9]+[:]){3})(?:[A-Fa-f0-9]+[:]){7}(.+\/\/.+)", r"\g<1>%s\2" % ("0:" * 7), line, IGNORECASE)
       if tot > 0:
        lines[ndx] = txt
        toSave  = True
        totChange += 1
    if toSave:
     with open(path, "w") as f:
      f.write("\n".join(lines) + "\n")
  self.VVdFw4(totChange > 0, "Change to Identical Ref. Codes", "Changes = %d" % totChange)
 def VVdFw4(self, isChanged, title, txt, refreshTable=True):
  if isChanged:
   FFlB9k()
   if refreshTable and self.VVcpnp:
    VVvhuK = self.VVjbF3()
    if VVvhuK and self.VVcpnp:
     self.VVcpnp.VVuVux(VVvhuK, self.tableTitle)
     self.VVcpnp.VVIX8q(txt)
   FFNEkd(self, txt, title=title)
  else:
   FFewCE(self, "No changes.")
 def VVRuow(self):
  return CCqQHV.VVJ90G()
 @staticmethod
 def VVJ90G(atLeastOne=False):
  types = ('*.tv', '*.radio')
  files = []
  for f in types:
   files.extend(iGlob(VV609C + f))
  if files:
   iptvFiles = []
   for path in files:
    if fileExists(path):
     txt = FFqD66(path)
     span = iSearch(r"#SERVICE.+\/\/.+\n#DESCRIPTION.+", txt, IGNORECASE)
     if span:
      iptvFiles.append(path)
      if atLeastOne:
       return iptvFiles
   return iptvFiles
  else:
   return None
 def VVA6ny(self, VVcpnp, title, txt, colList):
  chName = colList[1]
  refCode = colList[4]
  url  = FF9CmS(colList[5]).strip()
  iptvRef = refCode.rstrip(":") + ":" + url
  if not iptvRef.endswith(":" + chName):
   iptvRef += ":" + chName
  ndx = txt.find("URL")
  if ndx > -1:
   txt = txt[:ndx]
  txt = "%s\n\n%s" % (title, txt)
  FFBatl(self, fncMode=CCARMv.VVxAjd, refCode=refCode, chName=chName, text=txt, decodedUrl=url, iptvRef=iptvRef)
 def VVv2QK(self, VVcpnp, colList):
  chName = colList[1]
  refCode = colList[4]
  url  = colList[5]
  chUrl = refCode + url
  return chName, chUrl
 def VVnuUJ(self, VVcpnp, title, txt, colList):
  chName, chUrl = self.VVv2QK(VVcpnp, colList)
  self.VVFtuD(VVcpnp, chName, chUrl, "localIptv")
 def VVSKoe(self, mode, VVcpnp, colList):
  chName, chUrl, picUrl, refCode = self.VV1lQi(mode, colList)
  return chName, chUrl
 def VVisHT(self, mode, VVcpnp, title, txt, colList):
  chName, chUrl, picUrl, refCode = self.VV1lQi(mode, colList)
  self.VVFtuD(VVcpnp, chName, chUrl, mode)
 def VVFtuD(self, VVcpnp, chName, chUrl, playerFlag):
  chName = FFO8d5(chName)
  if self.VVmaA2(chName):
   FFD1yO(VVcpnp, "This is a marker!", 300)
  else:
   FFlX3B(VVcpnp, BF(self.VVRBA7, VVcpnp, chUrl, playerFlag), title="Playing ...")
 def VVRBA7(self, VVcpnp, chUrl, playerFlag):
  FFJZ42(self, chUrl, VVpyjK=False)
  CCppdx.VVgElN(self.session, iptvTableParams=(self, VVcpnp, playerFlag))
 @staticmethod
 def VVmaA2(chName):
  mark = ("--", "__", "==", "##",  "**", "\\u2605" * 2)
  if chName.startswith(mark) and chName.endswith(mark):
   return True
  return False
 def VV8PVa(self, VVcpnp, title, txt, colList):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  if refCode:
   url1 = FF9CmS(origUrl.strip())
   for ndx, row in enumerate(VVcpnp.VVGrbO()):
    if refCode in row[4]:
     tableRow = FF9CmS(row[5].strip())
     if url1 in tableRow or tableRow in url1:
      VVcpnp.VVtpKN(ndx)
      break
   else:
    FFD1yO(VVcpnp, "No found", 1000)
 def VVm0c2(self, m3uMode):
  lines = self.VVLdnU(3)
  if lines:
   lines.sort()
   VV625J = []
   for line in lines:
    VV625J.append((line, line))
   if m3uMode == self.VVVOMv:
    title = "Browse Server from M3U URLs"
    VVme6L = ("All to Playlist", self.VV4d8h)
   else:
    title = "M3U/M3U8 File Browser"
    VVme6L = None
   OKBtnFnc = BF(self.VVEnK8, m3uMode, title)
   VVmKbI  = ("Show Full Path", self.VVaUu6)
   VVJ5GS = ("Delete File", self.VVLHB0)
   FFuRfS(self, None, title=title, VV625J=VV625J, width=1200, OKBtnFnc=OKBtnFnc, VVmKbI=VVmKbI, VVJ5GS=VVJ5GS, VVme6L=VVme6L, VVz2kc="#11221122", VVwpZm="#11221122")
 def VVEnK8(self, m3uMode, title, item=None):
  if item:
   menuInstance, txt, path, ndx = item
   if m3uMode == self.VVVOMv:
    FFlX3B(menuInstance, BF(self.VV4IBs, title, path))
   else:
    self.VVL8BU(menuInstance, path)
 def VVL8BU(self, menuInstance, path=None):
  if path:
   VV625J = []
   VV625J.append(("All"         , "all"   ))
   VV625J.append(FFi9aC("Category"))
   VV625J.append(("Live TV"        , "live"  ))
   VV625J.append(("VOD"         , "vod"   ))
   VV625J.append(("Series"        , "series"  ))
   VV625J.append(("Uncategorised"      , "uncat"  ))
   VV625J.append(FFi9aC("Media"))
   VV625J.append(("Video"        , "video"  ))
   VV625J.append(("Audio"        , "audio"  ))
   VV625J.append(FFi9aC("File Type"))
   VV625J.append(("MKV"         , "MKV"   ))
   VV625J.append(("MP4"         , "MP4"   ))
   VV625J.append(("MP3"         , "MP3"   ))
   VV625J.append(("AVI"         , "AVI"   ))
   VV625J.append(("FLV"         , "FLV"   ))
   filterObj = CCU3qf(self, VVz2kc="#11552233", VVwpZm="#11552233")
   filterObj.VVxv80(VV625J, [], BF(self.VVYfOz, menuInstance, path), inFilterFnc=None)
 def VVYfOz(self, menuInstance, path, item):
  if item is not None:
   if   item == "all"    : mode, words, fTitle = self.VVmFH3 , ""  , ""
   elif item == "live"    : mode, words, fTitle = self.VVSJlZ  , ""  , "Live"
   elif item == "vod"    : mode, words, fTitle = self.VV4YaG  , ""  , "VOD"
   elif item == "series"   : mode, words, fTitle = self.VVtssf  , ""  , "Series"
   elif item == "uncat"   : mode, words, fTitle = self.VVUhbg  , ""  , "Uncategorised"
   elif item == "video"   : mode, words, fTitle = self.VVdr1w  , ""  , "Video"
   elif item == "audio"   : mode, words, fTitle = self.VVbfFF  , ""  , "Audio"
   elif item == "MKV"    : mode, words, fTitle = self.VVdT8X  , ""  , "MKV"
   elif item == "MP4"    : mode, words, fTitle = self.VVS3tv  , ""  , "MP4"
   elif item == "MP3"    : mode, words, fTitle = self.VVdauk  , ""  , "MP3"
   elif item == "AVI"    : mode, words, fTitle = self.VV2c5y  , ""  , "AVI"
   elif item == "FLV"    : mode, words, fTitle = self.VVW3xs  , ""  , "FLV"
   elif item.startswith("__w__") : mode, words, fTitle = self.VVHOMm  , item[5:] , item[5:]
   else       : return
   words, asPrefix = CCU3qf.VVP88C(words)
   if not mode == self.VVmFH3:
    fTitle = "  Filter: %s" % (",".join(words) if words else fTitle)
    if len(fTitle) > 40: fTitle = fTitle[:40] + ".."
    fTitle = FFkhYI(fTitle, VVkXS4)
   m3uFiletrParam = (mode, words, asPrefix, fTitle)
   FFlX3B(menuInstance, BF(self.VVt26x, path, m3uFiletrParam))
 def VVt26x(self, srcPath, m3uFiletrParam):
  self.m3uOrM3u8BName = os.path.splitext(os.path.basename(srcPath))[0]
  txt  = FFqD66(srcPath)
  lst  = iFindall(r"#EXTINF:(.+),(.+)\n(.+)", txt, IGNORECASE)
  groups = set()
  VVAE0x = CCD3Dl()
  for ndx, cols in enumerate(lst, start=1):
   propLine, chName, url = cols
   group = self.VVedO8(propLine, "group-title") or "-"
   if not group == "-" and VVAE0x.VV16ZS(group):
    groups.add(group)
  VVvhuK = []
  if len(groups) > 0:
   title = "Groups" + m3uFiletrParam[3] if m3uFiletrParam else ""
   for group in groups:
    VVvhuK.append((group, group))
   VVvhuK.append(("ALL", ""))
   VVvhuK.sort(key=lambda x: x[0].lower())
   VVfPgM = self.VVj4t0
   VVVHmY  = ("Select" , BF(self.VVngsC, srcPath, m3uFiletrParam), [])
   widths   = (100  , 0)
   VVQqg2  = (LEFT  , LEFT)
   FF1dQ4(self, None, title=title, width= 1000, header=None, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=30, VVVHmY=VVVHmY, VVfPgM=VVfPgM, lastFindConfigObj=CFG.lastFindIptv
     , VVz2kc="#11110022", VVwpZm="#11110022", VVghPi="#11110022", VV0g1U="#00444400")
  else:
   txt = FFqD66(srcPath)
   self.VVuuVZ(txt, "", m3uFiletrParam)
 def VVngsC(self, srcPath, m3uFiletrParam, VVcpnp, title, txt, colList):
  group = colList[1]
  txt = FFqD66(srcPath)
  self.VVuuVZ(txt, group, m3uFiletrParam)
 def VVuuVZ(self, txt, filterGroup="", m3uFiletrParam=None):
  lst = iFindall(r"#EXTINF:(.+),(.+)\n(.+)", txt, IGNORECASE)
  bName = filterGroup or self.m3uOrM3u8BName or "ALL"
  title = ("Group : %s" % (filterGroup or "ALL")) + m3uFiletrParam[3] if m3uFiletrParam else ""
  if lst:
   self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
       , titlePrefix = "Reading File Lines"
       , fncToRun  = BF(self.VV5xbR, lst, filterGroup, m3uFiletrParam)
       , VVnFNJ = BF(self.VVc7b1, title, bName))
  else:
   self.VV6fkQ("Not valid lines found !", title)
 def VV5xbR(self, lst, filterGroup, m3uFiletrParam, VVC69w):
  VVC69w.VV0DcB = []
  VVC69w.VVYqos(len(lst))
  VVAE0x = CCD3Dl()
  num = 0
  for cols in lst:
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VVLLRh(1, True)
   cols = list(map(str.strip, cols))
   propLine, chName, url = cols
   picon = self.VVedO8(propLine, "tvg-logo")
   group = self.VVedO8(propLine, "group-title")
   if not filterGroup or filterGroup == group:
    skip = False
    if   group and not VVAE0x.VV16ZS(group) : skip = True
    elif chName and not VVAE0x.VV16ZS(chName) : skip = True
    elif m3uFiletrParam:
     mode, words, asPrefix, fTitle = m3uFiletrParam
     skip = not self.VVWAQG(mode, "", FF9CmS(url).lower(), chName, words, "", asPrefix)
    if not skip and VVC69w:
     num += 1
     VVC69w.VV0DcB.append((str(num), chName, group.capitalize(), url, picon, "Yes" if len(picon) > 0 else ""))
  if VVC69w:
   VVC69w.VVrCJd("Loading %d Channels" % len(VVC69w.VV0DcB))
 def VVc7b1(self, title, bName, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VV0DcB:
   VVfPgM = self.VVj4t0
   VVVHmY  = ("Select"   , BF(self.VVQlFX, title)   , [])
   VV01dN = (""    , self.VVyXVe        , [])
   VV3th8 = ("Download PIcons", self.VVpxRJ       , [])
   VVOtSO = ("Options"  , BF(self.VVbsEO, "m3Ch", "", bName) , [])
   header   = ("Num" , "Name", "Group" , "URL" , "piconUrl", "Logo" )
   widths   = (10  , 54 , 28  , 0  , 0   , 8   )
   VVQqg2  = (CENTER , LEFT , CENTER , LEFT , LEFT  , CENTER )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VV0DcB, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VVVHmY=VVVHmY, VVfPgM=VVfPgM, VV01dN=VV01dN, VV3th8=VV3th8, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VVKNen=True, searchCol=1
     , VVz2kc="#0a00192B", VVwpZm="#0a00192B", VVghPi="#0a00192B", VV0g1U="#00000000")
  else:
   self.VV6fkQ("Not found !", title)
 def VVpxRJ(self, VVcpnp, title, txt, colList):
  self.VV8r9L(VVcpnp, "m3u/m3u8")
 def VViWtl(self, rowNum, url, chName):
  refCode = self.VV0Ka4(rowNum, url, chName)
  chUrl = "%s%s:%s" % (refCode, FF2NHB(url), chName)
  return chUrl
 def VV0Ka4(self, rowNum, url, chName):
  span = iSearch(r"\/(\d{2,})", url, IGNORECASE)
  if span : stID = span.group(1)
  else : stID = "444"
  catID = "333"
  chNum = str(rowNum + 1)
  refCode = self.VVyKHt(catID, stID, chNum)
  return refCode
 def VVedO8(self, line, param):
  span = iSearch(r'%s="(.*?)"' % param, line, IGNORECASE)
  if span : return span.group(1).strip()
  else : return ""
 def VVQlFX(self, Title, VVcpnp, title, txt, colList):
  chName = colList[1].strip()
  url  = colList[3].strip()
  if url.endswith((".m3u", ".m3u8")):
   FFlX3B(VVcpnp, BF(self.VVtROM, Title, VVcpnp, colList), title="Checking Server ...")
  else:
   self.VVqlaL(VVcpnp, url, chName)
 def VVtROM(self, title, VVcpnp, colList):
  if not CC6sg1.VVStEc(self):
   return
  chName = colList[1]
  group = colList[2]
  url  = colList[3]
  txt, err =  CCyIre.VVHmZi(url, verify=True)
  if not err:
   if "#EXT-X-STREAM-INF" in txt:
    lst   = iFindall(r"RESOLUTION=(\d+x\d+).*\n(.+)", txt, IGNORECASE)
    VV625J = []
    for resol, fPath in lst:
     resol = str(resol).replace("x", " x ")
     fPath = str(fPath)
     fullUrl = CCqQHV.VV8M6j(url, fPath)
     VV625J.append((resol, fullUrl))
    if VV625J:
     if len(VV625J) > 1:
      FFuRfS(self, BF(self.VVinXy, VVcpnp, chName), VV625J=VV625J, title="Resolution", VVeYEo=True, VVvQ6U=True)
     else:
      self.VVqlaL(VVcpnp, VV625J[0][1], chName)
    else:
     self.VV6I1g("Cannot process server response !")
   elif "#EXTINF:" in txt:
    if url.endswith((".m3u", ".m3u8")) :
     span = iSearch(r"#EXTINF:.+\n(.+\.ts)", txt, IGNORECASE)
     if not span:
      self.VVuuVZ(txt, filterGroup="")
      return
    self.VVqlaL(VVcpnp, url, chName)
   else:
    self.VV6fkQ("Cannot process this channel !", title)
  else:
   self.VV6fkQ(err, title)
 def VVinXy(self, VVcpnp, chName, item=None):
  if item:
   txt, resolUrl, ndx = item
   self.VVqlaL(VVcpnp, resolUrl, chName)
 def VVqlaL(self, VVcpnp, url, chName):
  FFlX3B(VVcpnp, BF(self.VVeJhM, VVcpnp, url, chName), title="Playing ...")
 def VVeJhM(self, VVcpnp, url, chName):
  chUrl = self.VViWtl(VVcpnp.VVgrGB(), url, chName)
  FFJZ42(self, chUrl, VVpyjK=False)
  CCppdx.VVgElN(self.session, iptvTableParams=(self, VVcpnp, "m3u/m3u8"))
 def VVLprB(self, VVcpnp, colList):
  chName = colList[1].strip()
  url  = colList[3].strip()
  chUrl = self.VViWtl(VVcpnp.VVgrGB(), url, chName)
  return chName, chUrl
 def VVyXVe(self, VVcpnp, title, txt, colList):
  chName = colList[1].strip()
  url  = colList[3].strip()
  picUrl = colList[4].strip()
  txt = "%s\n\n%s" % (title, txt)
  FFBatl(self, fncMode=CCARMv.VVxAjd, chName=chName, text=txt, decodedUrl=url, picUrl=picUrl)
 def VV6fkQ(self, err, title):
  FFkYsE(self, err, title=title)
  if self.m3uOrM3u8File:
   self.close()
 def VVj4t0(self, VVcpnp):
  if self.m3uOrM3u8File:
   self.close()
  VVcpnp.cancel()
 def VV4d8h(self, VVp2lZObj, item=None):
  FFlX3B(VVp2lZObj, BF(self.VVqWqJ, VVp2lZObj, item))
 def VVqWqJ(self, VVp2lZObj, item):
  if item:
   pList = []
   dupl = 0
   for ndx, item in enumerate(VVp2lZObj.VV625J):
    path = item[1]
    if fileExists(path):
     enc = CClXbe.VVTBCL(path)
     if not enc == -1:
      with ioOpen(path, "r", encoding=enc) as f:
       for line in f:
        line = str(line).strip()
        if not line or len(line) > 500:
         continue
        url = self.VVhWv0(line)
        if url:
         if not url in pList : pList.append(url)
         else    : dupl += 1
         break
   title = "Create Playlist from m3u Files"
   if pList:
    pList.sort()
    path = CCqQHV.VVfFAE()
    pListF = "%sPlaylist_%s.txt" % (path, FFGuM2())
    with open(pListF, "w") as f:
     for url in pList:
      f.write(url + "\n")
    txt = ""
    txt += "Prcessed Files\t: %d\n"    % len(VVp2lZObj.VV625J)
    if dupl > 0:
     txt += "Duplicates\t: %d  (removed)\n" % dupl
    txt += "Created Lines\t: %d\n"    % len(pList)
    txt += "Playlist File\t: %s"    % pListF
    FFNEkd(self, txt, title=title)
   else:
    FFkYsE(self, "Could not obtain URLs from this file list !", title=title)
 def VVDqjN(self, mode):
  if   mode == 1: title, okFnc = "Select Playlist File", self.VVUCsE
  elif mode == 2: title, okFnc = "Select Portal File", self.VViJfK
  lines = self.VVLdnU(mode)
  if lines:
   lines.sort()
   VV625J = []
   for line in lines:
    VV625J.append((FFkhYI(line, VVoTT6) if "Bookmarks" in line else line, line))
   VVJ5GS = ("Delete File", self.VVLHB0)
   VVmKbI  = ("Show Full Path", self.VVaUu6)
   FFuRfS(self, None, title=title, VV625J=VV625J, width=1200, OKBtnFnc=okFnc, VVmKbI =VVmKbI , VVJ5GS=VVJ5GS)
 def VVaUu6(self, menuInstance, url):
  FFNEkd(self, url, title="Full Path")
 def VVLHB0(self, VVp2lZObj, path):
  FFMIbO(self, BF(self.VV61UG, VVp2lZObj, path), "Delete this file ?\n\n%s" % path)
 def VV61UG(self, VVp2lZObj, path):
  FFX92w(path)
  if fileExists(path) : FFD1yO(VVp2lZObj, "Not deleted", 1000)
  else    : VVp2lZObj.VVVDex()
 def VVUCsE(self, item=None):
  if item:
   menuInstance, txt, path, ndx = item
   FFlX3B(menuInstance, BF(self.VVMCiV, menuInstance, path), title="Processing File ...")
 def VVMCiV(self, VVpTNz, path):
  enc = CClXbe.VVTBCL(path, self)
  if enc == -1:
   return
  VVvhuK = []
  num = lineNum = 0
  with ioOpen(path, "r", encoding=enc) as f:
   for line in f:
    lineNum += 1
    line = str(line).strip()
    if not line or len(line) > 500:
     continue
    line = iSub(r"([^\x00-\x7F]+)", r" ", line, flags=IGNORECASE)
    span = iSearch(r".*(http.+php.+username=.+password=.+)", line, IGNORECASE)
    url = ""
    if span:
     url = span.group(1)
     url = url.split(" ")[0].split("\t")[0]
    else:
     span = iSearch(r"(http.+)\s+username(.+)\s+password\s+(.+)", line, IGNORECASE)
     if span:
      host = FF0WrY(span.group(1).strip())
      user1 = span.group(2).strip()
      pass1 = span.group(3).strip()
      url = "%sget.php?username=%s&password=%s&type=m3u" % (host, user1, pass1)
    if url:
     modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam = CCqQHV.VVuRWx(url)
     uURL  = uURL.rstrip("/")
     equalTo  = ""
     for item in VVvhuK:
      if item[2] == uURL and item[3] == uUser and item[4] == uPass:
       equalTo = ",".join(list([_f for _f in [item[5], item[0]] if _f]))
     num += 1
     VVvhuK.append((str(num), str(lineNum), uURL, uUser, uPass, equalTo, url))
  if VVvhuK:
   title = "Playlist File : %s" % os.path.basename(path)
   VVVHmY  = ("Start"    , BF(self.VV2F8m, "Playlist File")      , [])
   VVMQj9 = ("Home Menu"   , FFSJQP             , [])
   VV3th8 = ("Download M3U File" , self.VVhC8N         , [])
   VVOtSO = ("Edit File"   , BF(self.VV3nUz, path)        , [])
   VV1QO7 = ("Check & Filter"  , BF(self.VV0NeT, VVpTNz, path) , [])
   header   = ("Num" , "LineNum" , "Address" , "User" , "Password" , "Duplicate Line" , "URL" )
   widths   = (10  , 0   , 35  , 20  , 20   , 15    , 0.03 )
   VVQqg2  = (CENTER , CENTER , LEFT  , LEFT   , LEFT   , LEFT    , LEFT  )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVMQj9=VVMQj9, VV1QO7=VV1QO7, VV3th8=VV3th8, VVOtSO=VVOtSO, VVz2kc="#11001116", VVwpZm="#11001116", VVghPi="#11001116", VV0g1U="#00003635", VVooYw="#0a333333", VVPVU2="#11331100", VVKNen=True, searchCol=2, lastFindConfigObj=CFG.lastFindServers)
  else:
   FFkYsE(self, "No valid URLs line in this file:\n\n%s" % path, title="Get Play list URLs")
 def VVhC8N(self, VVcpnp, title, txt, colList):
  host = colList[2]
  url  = colList[6]
  title = "Download Server M3U File"
  t = "&type=m3u"
  if not url.endswith(t):
   url += t
  url = url.replace("player_api.php", "get.php" )
  FFMIbO(self, BF(FFlX3B, VVcpnp, BF(self.VVH5mr, title, url), title="Downloading ..."), "Download m3u file for ?\n\n%s" % host, title=title)
 def VVH5mr(self, title, url):
  path, err = FF913T(url, "ajpanel_tmp.m3u", timeout=3)
  errTitle = "Download Problem"
  if err:
   FFkYsE(self, err, title=errTitle)
  elif fileExists(path):
   txt = FFqD66(path)
   if '{"user_info":{"auth":0}}' in txt:
    FFX92w(path)
    FFkYsE(self, "Unauthorized", title=errTitle)
   elif not "#EXTM3U" in txt:
    FFX92w(path)
    FFkYsE(self, "Incorrect M3U file received !", title=errTitle)
   else:
    fName = os.path.basename(path)
    newPath = CCqQHV.VVfFAE() + fName
    os.system(FFxtg8("mv -f '%s' '%s'" % (path, newPath)))
    if fileExists(newPath):
     path = newPath
    FFewCE(self, "Downloaded to:\n\n%s" % path, title=title)
  else:
   FFkYsE(self, "Could not download the M3U file!", title=errTitle)
 def VV2F8m(self, Title, VVcpnp, title, txt, colList):
  url = colList[6]
  FFlX3B(VVcpnp, BF(self.VVhCXa, Title, url), title="Checking Server ...")
 def VV3nUz(self, path, VVcpnp, title, txt, colList):
  rowNum = int(colList[1].strip()) - 1
  if fileExists(path) : CCYE8p(self, path, VVnFNJ=BF(self.VVxsol, VVcpnp), curRowNum=rowNum)
  else    : FFAVqd(self, path)
 def VVxsol(self, VVcpnp, fileChanged):
  if fileChanged:
   VVcpnp.cancel()
 def VViay2(self, title):
  curChName = self.VVcpnp.VVQYAy(1)
  FFbRXK(self, BF(self.VV7Ed2, title), defaultText=curChName, title=title, message="Enter Name:")
 def VV7Ed2(self, title, name):
  if name:
   VVooHP, err = CCtSdI.VV4uiY(self, CCtSdI.VVtZVs, VVwoAs=False, VVDUH8=False)
   list = []
   if VVooHP:
    VVAE0x = CCD3Dl()
    name = VVAE0x.VVGk9I(name)
    ratio = "1"
    for item in VVooHP:
     if name in item[0].lower():
      list.append((item[0], FFsAXk(item[2]), item[3], ratio))
   if list : self.VVgtJC(list, title)
   else : FFkYsE(self, "Not found:\n\n%s" % name, title=title)
 def VVjCr7(self, title):
  curChName = self.VVcpnp.VVQYAy(1)
  self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
      , titlePrefix = "Find similar names"
      , fncToRun  = self.VVjWRm
      , VVnFNJ = BF(self.VVKMHw, title, curChName))
 def VVjWRm(self, VVC69w):
  curChName = self.VVcpnp.VVQYAy(1)
  VVooHP, err = CCtSdI.VV4uiY(self, CCtSdI.VV3E27, VVwoAs=False, VVDUH8=False)
  if not VVooHP or not VVC69w or VVC69w.isCancelled:
   return
  VVC69w.VV0DcB = []
  VVC69w.VVYqos(len(VVooHP))
  VVAE0x = CCD3Dl()
  curCh = VVAE0x.VVGk9I(curChName)
  for refCode in VVooHP:
   chName, sat, inDB = VVooHP.get(refCode, ("", "", 0))
   ratio = CCrs3r.VVwjGd(chName.lower(), curCh)
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VVLLRh(1, True)
   if VVC69w and ratio > 50:
    VVC69w.VV0DcB.append((chName, FFsAXk(sat), refCode.replace("_", ":"), str(ratio)))
 def VVKMHw(self, title, curChName, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VV0DcB: self.VVgtJC(VV0DcB, title)
  elif VVr4Ej: FFkYsE(self, "No similar names found for:\n\n%s" % curChName, title)
 def VVgtJC(self, VVvhuK, title):
  curChName = self.VVcpnp.VVQYAy(1)
  VVcobi = self.VVcpnp.VVQYAy(4)
  curUrl  = self.VVcpnp.VVQYAy(5)
  VVvhuK.sort(key=lambda x: (100-int(x[3]), x[0].lower()))
  VVVHmY  = ("Share Sat/C/T Ref.", BF(self.VVfN0m, title, curChName, VVcobi, curUrl), [])
  header   = ("Name" , "Sat"  , "Reference" , "Ratio" )
  widths   = (34  , 33  , 33   , 0   )
  FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVz2kc="#0a00112B", VVwpZm="#0a001126", VVghPi="#0a001126", VV0g1U="#00000000")
 def VVfN0m(self, newtitle, curChName, VVcobi, curUrl, VVcpnp, title, txt, colList):
  newChName = colList[0]
  newRefCode = colList[2]
  data  = newtitle, curChName, VVcobi, curUrl, newChName, newRefCode
  ques  = "IPTV Channel\t: %s\n\nSat/C/T Chan. \t: %s\n" % (curChName, newChName)
  FFMIbO(self.VVcpnp, BF(FFlX3B, self.VVcpnp, BF(self.VVj7X6, VVcpnp, data)), ques, title=newtitle, VVUEfx=True)
 def VVj7X6(self, VVcpnp, data):
  VVcpnp.cancel()
  title, curChName, VVcobi, curUrl, newChName, newRefCode = data
  curUrl  = curUrl.strip()
  VVcobi = VVcobi.strip()
  newRefCode = newRefCode.strip()
  if not VVcobi.endswith(":") : VVcobi += ":"
  if not newRefCode.endswith(":") : newRefCode += ":"
  curFullUrl = newFullUrl = ""
  span = iSearch(r"([A-Fa-f0-9]+:).+", VVcobi, IGNORECASE)
  if span:
   curRType = span.group(1)
   span = iSearch(r"[A-Fa-f0-9]+:(.+)", newRefCode, IGNORECASE)
   if span:
    newRefCode = curRType + span.group(1)
    curFullUrl = VVcobi + curUrl
    newFullUrl = newRefCode + curUrl
  totChanges = 0
  resTxt = resErr = ""
  if curFullUrl and newFullUrl:
   for path in self.VVRuow():
    txt = FFqD66(path)
    if curFullUrl in txt:
     totChanges += 1
     txt = txt.replace(curFullUrl, newFullUrl)
     with open(path, "w") as f:
      f.write(txt)
   if totChanges > 0:
    FFlB9k()
    newRow = []
    for i in range(6):
     newRow.append(self.VVcpnp.VVQYAy(i))
    newRow[4] = newRefCode
    done = self.VVcpnp.VVzOfF(newRow)
    resTxt = "Done"
   else:
    resErr = "Not found in IPTV files"
  else:
   resErr = "Cannot read Chan. Info."
  if   resTxt: FFpoMu(BF(FFewCE , self, resTxt, title=title))
  elif resErr: FFpoMu(BF(FFkYsE, self, resErr, title=title))
 def VV0NeT(self, VVpTNz, path, VVcpnp, title, txt, colList):
  self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
      , titlePrefix = "Checking Authorized Servers"
      , fncToRun  = BF(self.VV2uo8, VVcpnp)
      , VVnFNJ = BF(self.VVlBKE, VVpTNz, path, VVcpnp))
 def VV2uo8(self, VVcpnp, VVC69w):
  VVC69w.VVYqos(VVcpnp.VVHLLY())
  VVC69w.VV0DcB = []
  for row in VVcpnp.VVGrbO():
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VVLLRh(1, True)
   qUrl = self.VVLZnX(self.VV15Af, row[6])
   txt, err = self.VVpi8S(qUrl, timeout=1)
   if not err:
    try:
     tDict = jLoads(txt)
     if tDict and not err and "server_info" in tDict:
      item = tDict["user_info"]
      if not self.VVvsIK(item, "auth") == "0":
       VVC69w.VV0DcB.append(qUrl)
    except:
     pass
 def VVlBKE(self, VVpTNz, path, VVcpnp, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VVr4Ej:
   list = VV0DcB
   title = "Authorized Servers"
   if list:
    totChk = VVcpnp.VVHLLY()
    totAuth = len(list)
    if not totAuth == totChk:
     newPath = path + "_OK_%s.txt" % FFGuM2()
     with open(newPath, "w") as f:
      for item in list:
       f.write("%s\n" % item)
     self.VVDqjN(1)
     txt = ""
     txt += "Checked\t: %d\n"  %  totChk
     txt += "Authorized\t: %s\n\n" %  FFkhYI(str(totAuth), VV9cEK)
     txt += "%s\n\n%s"    %  (FFkhYI("Result File:", VVoTT6), newPath)
     FFNEkd(self, txt, title=title)
     VVcpnp.close()
     VVpTNz.close()
    else:
     FFewCE(self, "All URLs are authorized.", title=title)
   else:
    FFkYsE(self, "No authorized URL found !", title=title)
 @staticmethod
 def VVpi8S(url, timeout=3, allowDocType=False):
  if not iRequest:
   return "" , "Cannot import URLLIB/URLLIB2 !"
  try:
   req = iRequest(url)
   req.add_header('User-Agent', 'Mozilla/5.0')
   res = iUrlopen(req, timeout=timeout)
   resCode = res.code
   if resCode == 200 :
    cont = res.headers.get("Content-Type")
    if cont:
     if not any(x in cont for x in ("/json", "/ld+json", "text/html")):
      return "", "Unexpected server data type ( %s )" % cont
     res = res.read().decode("UTF-8")
     if res:
      if not allowDocType and "<!DOCTYPE html>" in res: return "", "Incorrect data format from server."
      else           : return res, ""
     else:
      return "", "No data from server."
    else:
     return "", "No data received from server"
   elif resCode == 401 : err = "Unauthorized"
   elif resCode == 402 : err = "Payment Required"
   elif resCode == 408 : err = "Request Timeout"
   else    : err = "err=%d" % resCode
   return "", err
  except Exception as e:
   return "", str(e)
 @staticmethod
 def VVuRWx(url):
  uURL = uProtoc = uHost = uPort = uQuery = uUser = uPass = ""
  modified = False
  uQueryParam = {}
  span  = iSearch(r"\s*(?:(.+):\/\/)*([^:^\/]*)(?::(\d*)\/)*\/*([^\?]*)\?*(.+)", url, IGNORECASE)
  if span:
   modified = True
   uProtoc = span.group(1) or ""
   uHost = span.group(2) or ""
   uPort = span.group(3) or ""
   uQuery = span.group(4) or ""
   param = span.group(5) or ""
   for part in param.split("&"):
    if "=" in part:
     if   part.lower().startswith("username"): uUser = part.split("=")[1]
     elif part.lower().startswith("password"): uPass = part.split("=")[1]
     parts = part.split("=")
     key = parts[0]
     val = parts[1]
     uQueryParam[key] = val
  if uProtoc : uProtoc += "://"
  if uPort : uPort = ":" + uPort
  uURL = "%s%s%s/" % (uProtoc, uHost, uPort)
  return modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam
 @staticmethod
 def VVPus3(url, justValidate=False, getAudVid=False, compareType=None, compareExt=None, justRetDotExt=False):
  res = scheme = netloc = path = params = query = fragment = username = password = hostname = port = ""
  try:
   if not iUrlparse(url).scheme:
    url = url.lstrip("/")
    url = "http://" + url
   res   = iUrlparse(url)
   scheme  = res.scheme
   netloc  = res.netloc
   path  = res.path
   params  = res.params
   query  = res.query
   fragment = res.fragment
   username = res.username or ""
   password = res.password or ""
   hostname = res.hostname or ""
   port  = res.port  or ""
  except:
   pass
  if justValidate:
   return all([scheme, netloc, path])
  tmpPath = path.strip("/")
  if   path.startswith("/live/")            : chType, tmpPath = "live" , path[6:]
  elif path.startswith("/movie/")            : chType, tmpPath = "movie" , path[7:]
  elif path.startswith("/series/")           : chType, tmpPath = "series", path[8:]
  elif any(x in tmpPath for x in (".m3u8", ".ts", "deviceUser", "deviceMac")) : chType = "live"
  else                  : chType = ""
  parts = tmpPath.split("/")
  if len(parts) >= 2:
   username = parts[0]
   password = parts[1]
   if len(parts) > 2:
    tmpPath  = "/".join(parts[2:])
  parts  = tmpPath.split(":")
  fileName = parts[0]
  if len(parts) > 1: chName = ":".join(parts[1:])
  elif ":" in query: chName = query.split(":")[1]
  else    : chName = ""
  streamId, dotExt = os.path.splitext(fileName)
  ext = dotExt[1:]
  if justRetDotExt:
   return dotExt
  if compareExt:
   if compareExt == ext: return True
   else    : return False
  if getAudVid:
   if ext:
    tDict = CCrQyy.VVrVCE()
    if   ext in list(tDict["mov"]): return "vid"
    elif ext in list(tDict["mus"]): return "aud"
   return ""
  if streamId.isdigit():
   if not chType :
    if not ext              : chType = "live"
    elif iSearch(r"(s\d\d.*e\d\d|e\d\d.*s\d\d)", chName, IGNORECASE): chType = "series"
    else               : chType = "movie:"
  else:
   streamId = ""
  if compareType is not None:
   if compareType == chType: return True
   else     : return False
  else:
   if scheme:
    scheme += "://"
   host = scheme + netloc
   return chType, host, username, password, streamId, chName
 @staticmethod
 def VVP82O(decodedUrl):
  return CCqQHV.VVPus3(decodedUrl, justRetDotExt=True)
 def VVLZnX(self, mode, url, Id="0"):
  Id = str(Id).strip()
  modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam = self.VVuRWx(url)
  url = "%splayer_api.php?username=%s&password=%s" % (uURL, uUser, uPass)
  if   mode == self.VV15Af   : return "%s"            % url
  elif mode == self.VVZ3on   : return "%s&action=get_live_categories"     % url
  elif mode == self.VVzxcn   : return "%s&action=get_vod_categories"      % url
  elif mode == self.VVTVFh  : return "%s&action=get_series_categories"     % url
  elif mode == self.VV9YnV  : return "%s&action=get_live_categories"     % url
  elif mode == self.VVeOl5 : return "%s&action=get_series_info&series_id=%s"   % (url, Id)
  elif mode == self.VV3zJB   : return "%s&action=get_live_streams&category_id=%s"  % (url, Id)
  elif mode == self.VV3qLZ    : return "%s&action=get_vod_streams&category_id=%s"   % (url, Id)
  elif mode == self.VV47C9  : return "%s&action=get_series&category_id=%s"    % (url, Id)
  elif mode == self.VVUdRa : return "%s&action=get_live_streams"      % url
  elif mode == self.VV3KJK  : return "%s&action=get_live_streams&category_id=%s"  % (url, Id)
 @staticmethod
 def VVvsIK(item, key, isDate=False, is_base64=False, isToHHMMSS=False):
  if key in item:
   val = str(item[key])
   try:
    if   isDate  : val = FFcgMH(int(val))
    elif is_base64 : val = FFWbB4(val)
    elif isToHHMMSS : val = FF3UDS(int(val))
   except:
    pass
   if val == "None": return ""
   else   : return val.strip()
  else:
   return ""
 def VV4IBs(self, title, path):
  if fileExists(path):
   enc = CClXbe.VVTBCL(path, self)
   if enc == -1:
    return
   qUrl = ""
   with ioOpen(path, "r", encoding=enc) as f:
    for line in f:
     line = str(line).strip()
     if not line or len(line) > 500:
      continue
     qUrl = self.VVhWv0(line)
     if qUrl:
      break
   if qUrl : self.VVhCXa(title, qUrl)
   else : FFkYsE(self, "Invalid M3U line format in:\n\n%s" % path, title=title)
  else:
   FFkYsE(self, "Cannot open file :\n\n%s" % path, title=title)
 def VVf1jy(self):
  title = "Current Channel Server"
  qUrl, iptvRef = self.VVAmSO()
  if qUrl or "chCode" in iptvRef:
   p = CCyIre()
   valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query = p.VVslTC(iptvRef)
   if valid:
    self.VVQYck(self, host, mac)
    return
   elif qUrl:
    FFlX3B(self, BF(self.VVhCXa, title, qUrl), title="Checking Server ...")
    return
  FFkYsE(self, "Error in current channel URL !", title=title)
 def VVAmSO(self):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  qUrl = self.VVhWv0(decodedUrl)
  return qUrl, iptvRef
 def VVhWv0(self, url):
  if url.startswith("#"):
   return ""
  url = url.strip(" /")
  try:
   res = iUrlparse(url)
  except:
   return ""
  scheme = res.scheme
  netloc = res.netloc
  if not scheme or not netloc:
   return ""
  host = scheme + "://" +  netloc
  path = res.path.strip("/")
  if   path.startswith("live/") : path = path[5:]
  elif path.startswith("movie/") : path = path[6:]
  elif path.startswith("series/") : path = path[7:]
  parts = path.split("/")
  if len(parts) == 3 and len(parts[0]) > 1: return "%s/get.php?username=%s&password=%s&type=m3u" % (host, parts[0], parts[1])
  else         : return ""
 def VVhCXa(self, title, url):
  self.VVozODData = {}
  qUrl = self.VVLZnX(self.VV15Af, url)
  txt, err = self.VVpi8S(qUrl)
  if err:
   err = "Server Error:\n\n%s" % err
  tDict = {}
  if not err:
   try:
    tDict = jLoads(txt)
   except:
    pass
   if not tDict:
    err = "Could not parse server data !"
  if tDict and not err:
   self.VVozODData = {"playListURL": url}
   if "user_info" in tDict and "server_info" in tDict:
    item = tDict["user_info"]
    self.VVozODData["username"    ] = self.VVvsIK(item, "username"        )
    self.VVozODData["password"    ] = self.VVvsIK(item, "password"        )
    self.VVozODData["message"    ] = self.VVvsIK(item, "message"        )
    self.VVozODData["auth"     ] = self.VVvsIK(item, "auth"         )
    self.VVozODData["status"    ] = self.VVvsIK(item, "status"        )
    self.VVozODData["exp_date"    ] = self.VVvsIK(item, "exp_date"    , isDate=True )
    self.VVozODData["is_trial"    ] = self.VVvsIK(item, "is_trial"        )
    self.VVozODData["active_cons"   ] = self.VVvsIK(item, "active_cons"       )
    self.VVozODData["created_at"   ] = self.VVvsIK(item, "created_at"   , isDate=True )
    self.VVozODData["max_connections"  ] = self.VVvsIK(item, "max_connections"      )
    self.VVozODData["allowed_output_formats"] = self.VVvsIK(item, "allowed_output_formats"    )
    key = "allowed_output_formats"
    val = item.get(key, None)
    if isinstance(val, list):
     self.VVozODData[key] = " , ".join(val)
    item = tDict["server_info"]
    self.VVozODData["url"    ] = self.VVvsIK(item, "url"        )
    self.VVozODData["port"    ] = self.VVvsIK(item, "port"        )
    self.VVozODData["https_port"  ] = self.VVvsIK(item, "https_port"      )
    self.VVozODData["server_protocol" ] = self.VVvsIK(item, "server_protocol"     )
    self.VVozODData["rtmp_port"   ] = self.VVvsIK(item, "rtmp_port"       )
    self.VVozODData["timezone"   ] = self.VVvsIK(item, "timezone"       )
    self.VVozODData["timestamp_now"  ] = self.VVvsIK(item, "timestamp_now"  , isDate=True )
    self.VVozODData["time_now"   ] = self.VVvsIK(item, "time_now"       )
    VV625J  = self.VV9NT4(True)
    OKBtnFnc = self.VVmZLg
    VVBfJP = ("Home Menu", FFSJQP)
    VVme6L = ("Bookmark Server", BF(CCqQHV.VVyq4W, self, False, self.VVozODData["playListURL"]))
    FFuRfS(self, None, title="IPTV Server Resources", VV625J=VV625J, OKBtnFnc=OKBtnFnc, VVBfJP=VVBfJP, VVme6L=VVme6L)
   else:
    err = "Could not get data from server !"
  if err:
   FFkYsE(self, err, title=title)
  FFD1yO(self)
 def VVmZLg(self, item=None):
  if item:
   menuInstance, title, ref, ndx = item
   wTxt = "Downloading ..."
   if   ref == "live"   : FFlX3B(menuInstance, BF(self.VVBoeS, self.VVZ3on  , title=title), title=wTxt)
   elif ref == "vod"   : FFlX3B(menuInstance, BF(self.VVBoeS, self.VVzxcn  , title=title), title=wTxt)
   elif ref == "series"  : FFlX3B(menuInstance, BF(self.VVBoeS, self.VVTVFh , title=title), title=wTxt)
   elif ref == "catchup"  : FFlX3B(menuInstance, BF(self.VVBoeS, self.VV9YnV , title=title), title=wTxt)
   elif ref == "accountInfo" : FFlX3B(menuInstance, BF(self.VVWO8z           , title=title), title=wTxt)
 def VVWO8z(self, title):
  rows = []
  for key, val in list(self.VVozODData.items()):
   if isinstance(val, list): val = str(" , ".join(val))
   else     : val = str(val)
   if any(x in key for x in ("url", "port", "https_port", "server_protocol", "rtmp_port", "timezone", "timestamp_now", "time_now")):
    num, part = "2", self.VVwRua
   else:
    num, part = "1", self.VVMw87
   rows.append((num, part, str(key).replace("_", " ").title(), str(val)))
  rows.sort(key=lambda x: (x[0], x[2]))
  VVMQj9  = ("Home Menu", FFSJQP, [])
  VV3th8  = None
  if VVF5vz:
   VV3th8 = ("Get JS" , BF(self.VVOGbr, "/".join(self.VVozODData["playListURL"].split("/")[:-1])), [])
  header    = ("Num", "User/Server" , "Subject" , "Value" )
  widths    = (0 , 15   , 35  , 50  )
  FF1dQ4(self, None, title=title, width=1200, header=header, VVvytR=rows, VVoJsQ=widths, VVmp7B=26, VVMQj9=VVMQj9, VV3th8=VV3th8, VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000", searchCol=2)
 def VVy3sZ(self, mode, jData):
  list = []
  err  = ""
  try:
   tDict = jLoads(jData)
   if tDict:
    VVAE0x = CCD3Dl()
    if mode in (self.VV3zJB, self.VV3KJK):
     for ndx, item in enumerate(tDict, start=1):
      num      = self.VVvsIK(item, "num"         )
      name     = self.VVvsIK(item, "name"        )
      stream_id    = self.VVvsIK(item, "stream_id"       )
      stream_icon    = self.VVvsIK(item, "stream_icon"       )
      epg_channel_id   = self.VVvsIK(item, "epg_channel_id"      )
      added     = self.VVvsIK(item, "added"    , isDate=True )
      is_adult    = self.VVvsIK(item, "is_adult"       )
      category_id    = self.VVvsIK(item, "category_id"       )
      tv_archive    = self.VVvsIK(item, "tv_archive"       )
      direct_source   = self.VVvsIK(item, "direct_source"      )
      tv_archive_duration  = self.VVvsIK(item, "tv_archive_duration"     )
      name = VVAE0x.VV16ZS(name, is_adult)
      if name:
       if mode == self.VV3zJB or mode == self.VV3KJK and tv_archive == "1":
        hasPicon = "Yes" if stream_icon else ""
        catchupTxt = ""
        if tv_archive == "1":
         catchupTxt = "Yes"
         if tv_archive_duration:
          if tv_archive_duration == "1" : catchupTxt = "1 day"
          else       : catchupTxt = "%s days" % tv_archive_duration
        list.append((num, name, category_id, stream_id, stream_icon, added, epg_channel_id, is_adult, hasPicon, catchupTxt, direct_source))
    elif mode == self.VV3qLZ:
     for ndx, item in enumerate(tDict, start=1):
      num     = self.VVvsIK(item, "num"         )
      name    = self.VVvsIK(item, "name"        )
      stream_id   = self.VVvsIK(item, "stream_id"       )
      stream_icon   = self.VVvsIK(item, "stream_icon"       )
      added    = self.VVvsIK(item, "added"    , isDate=True )
      is_adult   = self.VVvsIK(item, "is_adult"       )
      category_id   = self.VVvsIK(item, "category_id"       )
      container_extension = self.VVvsIK(item, "container_extension"     ) or "mp4"
      name = VVAE0x.VV16ZS(name, is_adult)
      if name:
       isPicon = "Yes" if stream_icon else ""
       list.append((num, name, category_id, stream_id, stream_icon, added, is_adult, container_extension, isPicon))
    elif mode == self.VV47C9:
     for ndx, item in enumerate(tDict, start=1):
      num     = self.VVvsIK(item, "num"        )
      name    = self.VVvsIK(item, "name"       )
      series_id   = self.VVvsIK(item, "series_id"      )
      cover    = self.VVvsIK(item, "cover"       )
      genre    = self.VVvsIK(item, "genre"       )
      episode_run_time = self.VVvsIK(item, "episode_run_time"    )
      category_id   = self.VVvsIK(item, "category_id"      )
      container_extension = self.VVvsIK(item, "container_extension"    ) or "mp4"
      name = VVAE0x.VV16ZS(name)
      if name:
       isPicon = "Yes" if cover else ""
       list.append((num, name, category_id, series_id, genre, episode_run_time, container_extension, cover, isPicon))
  except:
   err = "Cannot parse received data !"
  return list, err
 def VVBoeS(self, mode, title):
  cList, err = self.VVLYOy(mode)
  if cList and mode == self.VV9YnV:
   cList = self.VVXpAh(cList)
  if err:
   FFkYsE(self, err, title=title)
  elif cList:
   cList.sort(key=lambda x: x[0].lower())
   VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ(mode)
   mName = self.VV6ejl(mode)
   if   mode == self.VVZ3on  : fMode = self.VV3zJB
   elif mode == self.VVzxcn  : fMode = self.VV3qLZ
   elif mode == self.VVTVFh : fMode = self.VV47C9
   elif mode == self.VV9YnV : fMode = self.VV3KJK
   if mode == self.VV9YnV:
    VVOtSO = None
    VV1QO7 = None
   else:
    VVOtSO = ("Find in %s" % mName , BF(self.VVvTDA, fMode, True) , [])
    VV1QO7 = ("Find in Selected" , BF(self.VVvTDA, fMode, False) , [])
   VVVHmY   = ("Show List"   , BF(self.VVNbN1, mode)  , [])
   VVMQj9  = ("Home Menu"   , FFSJQP         , [])
   header   = None
   widths   = (100   , 0  , 0    )
   FF1dQ4(self, None, title=title, width=1200, header=header, VVvytR=cList, VVoJsQ=widths, VVmp7B=30, VVMQj9=VVMQj9, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VVVHmY=VVVHmY, VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVghPi, VV0g1U=VV0g1U, lastFindConfigObj=CFG.lastFindIptv)
  else:
   FFkYsE(self, "No list from server !", title=title)
  FFD1yO(self)
 def VVLYOy(self, mode):
  qUrl  = self.VVLZnX(mode, self.VVozODData["playListURL"])
  txt, err = self.VVpi8S(qUrl)
  if err:
   return [], "Server Error:\n\n" + err
  list = []
  try:
   hideAdult = CFG.hideIptvServerAdultWords.getValue()
   tDict = jLoads(txt)
   if tDict:
    VVAE0x = CCD3Dl()
    for item in tDict:
     category_id  = self.VVvsIK(item, "category_id"  )
     category_name = self.VVvsIK(item, "category_name" )
     parent_id  = self.VVvsIK(item, "parent_id"  )
     category_name = VVAE0x.VVyWSY(category_name)
     if category_name:
      list.append((category_name, category_id, parent_id))
  except:
   return "", "Cannot parse received data !"
  return list, ""
 def VVXpAh(self, catList):
  mode  = self.VV3KJK
  qUrl  = self.VVLZnX(mode, self.VVozODData["playListURL"])
  txt, err = self.VVpi8S(qUrl)
  chanList = []
  if err:
   return []
  chanList, err = self.VVy3sZ(mode, txt)
  newCatList = []
  for cat in catList:
   for ch in chanList:
    if cat[1] == ch[2] and not cat in newCatList:
     newCatList.append(cat)
  return newCatList
 def VVNbN1(self, mode, VVcpnp, title, txt, colList):
  title = colList[1]
  FFlX3B(VVcpnp, BF(self.VV8B5E, mode, VVcpnp, title, txt, colList), title="Downloading ...")
 def VV8B5E(self, mode, VVcpnp, title, txt, colList):
  bName  = colList[0]
  catID  = colList[1]
  parentID = colList[2]
  title = self.VV6ejl(mode) + " : "+ bName
  if   mode == self.VVZ3on  : mode = self.VV3zJB
  elif mode == self.VVzxcn  : mode = self.VV3qLZ
  elif mode == self.VVTVFh : mode = self.VV47C9
  elif mode == self.VV9YnV : mode = self.VV3KJK
  qUrl  = self.VVLZnX(mode, self.VVozODData["playListURL"], catID)
  txt, err = self.VVpi8S(qUrl)
  list  = []
  if not err and mode in (self.VV3zJB, self.VV3qLZ, self.VV47C9, self.VV3KJK):
   list, err = self.VVy3sZ(mode, txt)
  if err:
   FFkYsE(self, err, title=title)
  elif list:
   VVMQj9  = ("Home Menu"   , FFSJQP            , [])
   if mode in (self.VV3zJB, self.VV3KJK):
    VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ(mode)
    VV01dN = (""     , BF(self.VVgCfD, mode)      , [])
    VV3th8 = ("Download Options" , BF(self.VVIM21, mode, "", "")   , [])
    VVOtSO = ("Options"   , BF(self.VVbsEO, "lv", mode, bName)   , [])
    if mode == self.VV3zJB:
     VVVHmY = ("Play"    , BF(self.VVisHT, mode)       , [])
    else:
     VVVHmY = ("Programs"   , BF(self.VVebv1, mode, bName) , [])
   elif mode == self.VV3qLZ:
    VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ(mode)
    VVVHmY  = ("Play"    , BF(self.VVisHT, mode)       , [])
    VV01dN = (""     , BF(self.VVgCfD, mode)      , [])
    VV3th8 = ("Download Options" , BF(self.VVIM21, mode, "v", "")   , [])
    VVOtSO = ("Options"   , BF(self.VVbsEO, "v", mode, bName)   , [])
   elif mode == self.VV47C9:
    VVz2kc, VVwpZm, VVghPi, VV0g1U = self.VViepZ("series2")
    VVVHmY  = ("Show Seasons"  , BF(self.VVk8Dh, mode)       , [])
    VV01dN = (""     , BF(self.VVvWrM, mode)     , [])
    VV3th8 = None
    VVOtSO = None
   header, widths, VVQqg2 = self.VVHj0b(mode)
   FF1dQ4(self, None, title=title, header=header, VVvytR=list, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VV01dN=VV01dN, VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVghPi, VV0g1U=VV0g1U, VVKNen=True, searchCol=1)
  else:
   FFkYsE(self, "No Channels found !", title=title)
  FFD1yO(self)
 def VVHj0b(self, mode):
  if mode in (self.VV3zJB, self.VV3KJK):
   header   = ("Num" , "Name", "catID", "ID"  , "Icon" , "Added" , "epgID" , "Is Adult", "Logo", "Catch-up", "Link")
   widths   = (8  , 55  , 0   , 0   , 0  , 22  , 0   , 0   , 6  , 9   , 0.03 )
   VVQqg2  = (CENTER, LEFT  , CENTER , CENTER, LEFT , CENTER , CENTER , CENTER , CENTER, CENTER , CENTER)
  elif mode == self.VV3qLZ:
   header   = ("Num" , "Name", "catID", "ID"  , "Icon" , "Added" , "isAdult" , "Ext" , "Logo")
   widths   = (8  , 62  , 0   , 0   , 0  , 24  , 0   , 0  , 6  )
   VVQqg2  = (CENTER, LEFT  , CENTER , CENTER, LEFT , CENTER , CENTER , CENTER, CENTER)
  elif mode == self.VV47C9:
   header   = ("Num" , "Name", "catID", "ID"  , "Genre" , "Dur.", "Ext" , "Cover" , "Logo" )
   widths   = (8  , 56  , 0   , 0   , 30  , 0  , 0  , 0   , 6   )
   VVQqg2  = (CENTER, LEFT  , LEFT   , CENTER , LEFT , CENTER, CENTER, LEFT  , CENTER )
  return header, widths, VVQqg2
 def VVebv1(self, mode, bName, VVcpnp, title, txt, colList):
  chName  = colList[1]
  catId  = colList[2]
  streamId = colList[3]
  hostUrl  = self.VVozODData["playListURL"]
  ok_fnc  = BF(self.VVn2bc, hostUrl, chName, catId, streamId)
  FFlX3B(VVcpnp, BF(CCqQHV.VV44HD, self, hostUrl, chName, streamId, ok_fnc), title="Reading Program List ...")
 def VVn2bc(self, chUrl, chName, catId, streamId, VVcpnp, title, txt, colList):
  pTitle = colList[3]
  sTime = colList[5]
  dur  = colList[7]
  span = iSearch(r"(\d{4}-\d{2}-\d{2})\s(\d{2}):(\d{2})", sTime, IGNORECASE)
  if span:
   sTime = span.group(1) + ":" + span.group(2) + "-" + span.group(3)
   modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam = CCqQHV.VVuRWx(chUrl)
   chNum = "333"
   refCode = CCqQHV.VVyKHt(catId, streamId, chNum)
   chUrl = "%stimeshift/%s/%s/%s/%s/%s.ts" % (uURL, uUser, uPass, dur, sTime, streamId)
   chUrl = chUrl.replace(":", "%3a")
   chUrl = refCode + chUrl + ":" + chName + " >> " + pTitle
   FFJZ42(self, chUrl, VVpyjK=False)
   CCppdx.VVgElN(self.session)
  else:
   FFkYsE(self, "Incorrect Timestamp", pTitle)
 def VVk8Dh(self, mode, VVcpnp, title, txt, colList):
  title = colList[1]
  FFlX3B(VVcpnp, BF(self.VVTokd, mode, VVcpnp, title, txt, colList), title="Downloading ...")
 def VVTokd(self, mode, VVcpnp, title, txt, colList):
  series_id = colList[3]
  qUrl  = self.VVLZnX(self.VVeOl5, self.VVozODData["playListURL"], series_id)
  txt, err = self.VVpi8S(qUrl)
  list  = []
  if not err:
   list = []
   err  = ""
   try:
    tDict = jLoads(txt)
    if tDict:
     title  = "Seasons"
     category_id = "222"
     icon  = ""
     if "info" in tDict:
      title  = self.VVvsIK(tDict["info"], "name"   )
      category_id = self.VVvsIK(tDict["info"], "category_id" )
      icon  = self.VVvsIK(tDict["info"], "cover"   )
     if "episodes" in tDict:
      seasons = tDict["episodes"]
      VVAE0x = CCD3Dl()
      for season in seasons:
       item = seasons[season]
       for EP in item:
        stream_id   = self.VVvsIK(EP, "id"     )
        episode_num   = self.VVvsIK(EP, "episode_num"   )
        epTitle    = self.VVvsIK(EP, "title"     )
        container_extension = self.VVvsIK(EP, "container_extension" )
        seasonNum   = self.VVvsIK(EP, "season"    )
        epTitle = VVAE0x.VV16ZS(epTitle)
        list.append((seasonNum, episode_num, epTitle, category_id, stream_id, icon, container_extension))
   except:
    err = "Cannot parse received data !"
  if err:
   FFkYsE(self, err, title=title)
  elif list:
   VVMQj9 = ("Home Menu"   , FFSJQP          , [])
   VV3th8 = ("Download Options" , BF(self.VVIM21, mode, "s", title), [])
   VVOtSO = ("Options"   , BF(self.VVbsEO, "s", mode, title) , [])
   VV01dN = (""     , BF(self.VVgCfD, mode)    , [])
   VVVHmY  = ("Play"    , BF(self.VVisHT, mode)     , [])
   header   = ("Season" , "Episode" , "Title" , "catID" , "stID", "Icon", "Ext" )
   widths   = (10  , 10  , 80  , 0   , 0  , 0  , 0  )
   VVQqg2  = (CENTER , CENTER , LEFT  , CENTER , CENTER, LEFT , CENTER)
   FF1dQ4(self, None, title=title, header=header, VVvytR=list, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVMQj9=VVMQj9, VV3th8=VV3th8, VVVHmY=VVVHmY, VV01dN=VV01dN, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000")
  else:
   FFkYsE(self, "No Channels found !", title=title)
  FFD1yO(self)
 def VVvTDA(self, mode, isAll, VVcpnp, title, txt, colList):
  onlyCatID = None if isAll else colList[1]
  VV625J = []
  VV625J.append(("Keyboard"  , "manualEntry"))
  VV625J.append(("From Filter" , "fromFilter"))
  FFuRfS(self, BF(self.VVsWNw, VVcpnp, mode, onlyCatID), title="Input Type", VV625J=VV625J, width=400)
 def VVsWNw(self, VVcpnp, mode, onlyCatID, item=None):
  if item is not None:
   if   item == "manualEntry":
    FFbRXK(self, BF(self.VVHOQ9, VVcpnp, mode, onlyCatID), defaultText=CFG.lastFindIptv.getValue(), title="Find", message="Enter Name (or names separated by a comma)")
   elif item == "fromFilter":
    filterObj = CCU3qf(self)
    filterObj.VVmiWt(BF(self.VVHOQ9, VVcpnp, mode, onlyCatID))
 def VVHOQ9(self, VVcpnp, mode, onlyCatID, item):
  if not item is None:
   title = "Find in names"
   words = None
   toFind = item.strip()
   FFnT3A(CFG.lastFindIptv, toFind)
   if toFind:
    words, asPrefix = CCU3qf.VVP88C(toFind)
    if words:
     if len(words) == 1 and len(words[0]) < 3:
      FFkYsE(self, "Enter at least 3 characters.", title=title)
      return
     else:
      for word in words:
       if len(word) < 3:
        FFkYsE(self, "All words must be at least 3 characters !", title=title)
        return
     VVAE0x = CCD3Dl()
     if CFG.hideIptvServerAdultWords.getValue() and VVAE0x.VVn2Iq(words):
      FFkYsE(self, VVAE0x.VV2tDQ(), title="Find: %s" % " , ".join(words))
      return
     else:
      self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
          , titlePrefix = "Searching for:%s" % toFind[:15]
          , fncToRun  = BF(self.VVsnJ2, VVcpnp, mode, onlyCatID, title, words, toFind, asPrefix, VVAE0x)
          , VVnFNJ = BF(self.VVepQ3, mode, toFind, title))
   if not words:
    FFD1yO(VVcpnp, "Nothing to find !", 1500)
 def VVsnJ2(self, VVcpnp, mode, onlyCatID, title, words, toFind, asPrefix, VVAE0x, VVC69w):
  VVC69w.VVYqos(VVcpnp.VVI1WG() if onlyCatID is None else 1)
  VVC69w.VV0DcB = []
  for row in VVcpnp.VVGrbO():
   catName = row[0]
   catID = row[1]
   if not onlyCatID is None and not catID == onlyCatID:
    continue
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VVLLRh(1)
   VVC69w.VV95Yt(catName)
   qUrl  = self.VVLZnX(mode, self.VVozODData["playListURL"], catID)
   txt, err = self.VVpi8S(qUrl)
   if not err:
    tList, err = self.VVy3sZ(mode, txt)
    if tList:
     for item in tList:
      name = item[1].strip().lower()
      name = VVAE0x.VV16ZS(name)
      if name:
       if asPrefix and not name.startswith(words) : continue
       elif any(x in name for x in words)   : pass
       else          : continue
       VVC69w.VV0DcB.append(item)
 def VVepQ3(self, mode, toFind, title, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VV0DcB:
   title = self.VVm4JW(mode, toFind)
   if mode == self.VV3zJB or mode == self.VV3qLZ:
    if mode == self.VV3qLZ : typ = "v"
    else          : typ = ""
    bName   = CCqQHV.VVwvI5(toFind)
    VVVHmY  = ("Play"     , BF(self.VVisHT, mode)     , [])
    VV3th8 = ("Download Options" , BF(self.VVIM21, mode, typ, "") , [])
    VVOtSO = ("Options"   , BF(self.VVbsEO, "fnd", mode, bName), [])
   elif mode == self.VV47C9:
    VVVHmY  = ("Show Seasons"  , BF(self.VVk8Dh, mode)     , [])
    VVOtSO = None
    VV3th8 = None
   VV01dN  = (""     , BF(self.VVgCfD, mode)    , [])
   VVMQj9  = ("Home Menu"   , FFSJQP          , [])
   header, widths, VVQqg2 = self.VVHj0b(mode)
   VVcpnp = FF1dQ4(self, None, title=title, header=header, VVvytR=VV0DcB, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, VV01dN=VV01dN, VVz2kc="#0a00292B", VVwpZm="#0a002126", VVghPi="#0a002126", VV0g1U="#00000000", VVKNen=True, searchCol=1)
   if not VVr4Ej:
    FFD1yO(VVcpnp, "Stopped" , 1000)
  else:
   if VVr4Ej:
    FFkYsE(self, "Not found in names !\n\n( %s )" % toFind, title=title)
 def VV1lQi(self, mode, colList):
  colList = list(map(str.strip, colList))
  if mode in (self.VV3zJB, self.VV3KJK):
   num, name, category_id, stream_id, stream_icon, added, epg_channel_id, is_adult, hasPicon, catchupTxt, direct_source = colList
   chNum, chName, catID, stID, picUrl, ext, uCat = num, name, category_id, stream_id, stream_icon, "", ""
  elif mode == self.VV3qLZ:
   num, name, category_id, stream_id, stream_icon, added, is_adult, container_extension, isPicon = colList
   chNum, chName, catID, stID, picUrl, ext, uCat = num, name, category_id, stream_id, stream_icon, "." + container_extension, "movie/"
  else:
   seasonNum, episode_num, epTitle, category_id, stream_id, icon, container_extension = colList
   chNum, chName, catID, stID, picUrl, ext, uCat = "222", epTitle, category_id, stream_id, icon, "." + container_extension, "series/"
  chName = FFO8d5(chName)
  url = self.VVozODData["playListURL"]
  modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam = self.VVuRWx(url)
  refCode = self.VVyKHt(catID, stID, chNum)
  chUrl = "%s%s%s/%s/%s%s"  % (uURL, uCat, uUser, uPass, stID, ext)
  chUrl = chUrl.replace(":", "%3a")
  chUrl = refCode + chUrl + ":" + chName
  return chName, chUrl, picUrl, refCode
 def VVgCfD(self, mode, VVcpnp, title, txt, colList):
  FFlX3B(VVcpnp, BF(self.VVLIHT, mode, VVcpnp, title, txt, colList))
 def VVLIHT(self, mode, VVcpnp, title, txt, colList):
  chName, chUrl, picUrl, refCode = self.VV1lQi(mode, colList)
  txt = "%s\n\n%s" % (title, txt)
  FFBatl(self, fncMode=CCARMv.VVcpeX, refCode=refCode, chName=chName, text=txt, chUrl=chUrl, picUrl=picUrl)
 def VVvWrM(self, mode, VVcpnp, title, txt, colList):
  FFlX3B(VVcpnp, BF(self.VVKIyB, mode, VVcpnp, title, txt, colList))
 def VVKIyB(self, mode, VVcpnp, title, txt, colList):
  name = colList[1]
  Dur  = colList[5]
  Cover = colList[7]
  txt  = "%s\n\n%s" % (title, txt)
  txt  += "Duration\t: %s" % Dur
  FFBatl(self, fncMode=CCARMv.VVEaIm, chName=name, text=txt, picUrl=Cover)
 def VVIM21(self, mode, typ, seriesName, VVcpnp, title, txt, colList):
  VV625J = []
  isMulti = VVcpnp.VVbl0M
  tot  = VVcpnp.VVMJsS()
  if isMulti:
   if tot < 1:
    FFD1yO(VVcpnp, "Select rows first.", 1000)
    return
   else:
    name = "%d Selected" % tot
  else:
   name = "ALL"
  VV625J.append(("Download %s PIcon%s" % (name, FFICXm(tot)), "dnldPicons" ))
  if typ:
   VV625J.append(VVm77t)
   tName = "Movie" if typ.startswith("v") else "Series"
   VV625J.append(("Download Current %s" % tName    , "dnldSel"  ))
   VV625J.append(("Add Current %s to Download List" % tName , "addSel"  ))
   if typ.startswith("s"):
    VV625J.append(("Add All Episodes to Download List" , "addAllEp" ))
   if not CC9Zvn.VVwsNU():
    VV625J.append(VVm77t)
    VV625J.append(("Download Manager"      , "dload_stat" ))
  FFuRfS(self, BF(self.VVnPlt, VVcpnp, mode, typ, seriesName, colList), title="Download Options", VV625J=VV625J)
 def VVnPlt(self, VVcpnp, mode, typ, seriesName, colList, item=None):
  if item:
   if   item == "dnldPicons" : self.VV8r9L(VVcpnp, mode)
   elif item == "dnldSel"  : self.VVnYqQ(VVcpnp, mode, typ, colList, True)
   elif item == "addSel"  : self.VVnYqQ(VVcpnp, mode, typ, colList, False)
   elif item == "addAllEp"  : self.VVeuD9(VVcpnp, mode, typ, seriesName)
   elif item == "dload_stat" : CC9Zvn.VV4aex(self)
 def VVnYqQ(self, VVcpnp, mode, typ, colList, startDnld):
  chName, decodedUrl = self.VVjAEj(mode, typ, colList)
  if startDnld:
   CC9Zvn.VV8EZX(self, decodedUrl)
  else:
   self.VVQa5Z(VVcpnp, "Add to Download list", chName, [decodedUrl], startDnld)
 def VVeuD9(self, VVcpnp, mode, typ, seriesName):
  decodedUrl_list = []
  for row in VVcpnp.VVGrbO():
   chName, decodedUrl = self.VVjAEj(mode, typ, row)
   decodedUrl_list.append(decodedUrl)
  self.VVQa5Z(VVcpnp, "Add to Download list", "%s\n\n( %d Episodes )" % (seriesName, len(decodedUrl_list)), decodedUrl_list, False)
 def VVQa5Z(self, VVcpnp, title, chName, decodedUrl_list, startDnld):
  FFMIbO(self, BF(self.VVZCs0, VVcpnp, decodedUrl_list, startDnld), chName, title=title)
 def VVZCs0(self, VVcpnp, decodedUrl_list, startDnld):
  added, skipped = CC9Zvn.VVIp0j(decodedUrl_list)
  FFD1yO(VVcpnp, "Added", 1000)
 def VVjAEj(self, mode, typ, colList):
  if typ in ("v", "s"):
   chName, chUrl, picUrl, refCode = self.VV1lQi(mode, colList)
  elif typ in ("vp", "sp"):
   chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, colList)
   refCode, chUrl = self.VVWeZp(self.VVPj61, self.VVrGQ8, mode, chName, catID, stID, chNum, chCm, serCode, serId)
  refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(chUrl)
  return chName, decodedUrl
 def VV8r9L(self, VVcpnp, mode):
  if os.system(FFxtg8("which ffmpeg")) == 0:
   self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
       , titlePrefix = "Downloading PIcons"
       , fncToRun  = BF(self.VVZrFX, VVcpnp, mode)
       , VVnFNJ = self.VVaInT)
  else:
   FFMIbO(self, BF(CCqQHV.VV4Lee, self), '"FFmpeg" is required to resize the PIcons.\n\nInstall FFmpeg ?', title="Download all PIcons")
 def VVaInT(self, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  txt  = ""
  txt += "Total Processed\t\t: %d of %d\n" % (VV0DcB["proces"], VV0DcB["total"])
  txt += "Download Success\t: %d of %s\n"  % (VV0DcB["ok"], VV0DcB["attempt"])
  txt += "Skipped (PIcon exist)\t: %d\n"  % VV0DcB["exist"]
  txt += "Skipped (Size = 0)\t: %d\n"   % VV0DcB["size0"]
  txt += "Incorrect PIcon URL\t: %d\n"  % VV0DcB["badURL"]
  txt += "Download Failure\t: %d\n"   % VV0DcB["fail"]
  txt += "PIcons Path\t\t: %s\n"    % VV0DcB["path"]
  if not VVr4Ej  : color = "#11402000"
  elif VV0DcB["err"]: color = "#11201000"
  else     : color = None
  if VV0DcB["err"]:
   txt = "Critical Error\t\t: %s\n\n%s"  % (VV0DcB["err"], txt)
  title = "PIcons Download Result"
  if not VVr4Ej:
   title += "  (cancelled)"
  FFNEkd(self, txt, title=title, VVghPi=color)
 def VVZrFX(self, VVcpnp, mode, VVC69w):
  isMulti = VVcpnp.VVbl0M
  if isMulti : totRows = VVcpnp.VVMJsS()
  else  : totRows = VVcpnp.VVI1WG()
  VVC69w.VVYqos(totRows)
  VVC69w.VVRqfk(0)
  counter     = VVC69w.counter
  maxValue    = VVC69w.maxValue
  pPath     = CCrs3r.VVsNIk()
  VVC69w.VV0DcB = {   "total"  : totRows
         , "proces"  : 0
         , "attempt"  : 0
         , "fail"  : 0
         , "ok"   : 0
         , "size0"  : 0
         , "exist"  : 0
         , "badURL"  : 0
         , "path"  : pPath
         , "err"   : "" }
  try:
   for rowNum, row in enumerate(VVcpnp.VVGrbO()):
    if VVC69w.isCancelled:
     break
    if not isMulti or VVcpnp.VV3fqU(rowNum):
     VVC69w.VV0DcB["proces"] += 1
     VVC69w.VVLLRh(1)
     if mode in ("itv", "vod", "series"):
      chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, row)
      refCode = CCqQHV.VVyKHt(catID, stID, chNum)
     elif mode == "m3u/m3u8":
      chName = row[1].strip()
      url  = row[3].strip()
      picUrl = row[4].strip()
      refCode = self.VV0Ka4(rowNum, url, chName)
     else:
      chName, chUrl, picUrl, refCode = self.VV1lQi(mode, row)
     if picUrl:
      picon = refCode.replace(":", "_").rstrip("_") + ".png"
      if not fileExists(pPath + picon):
       VVC69w.VV0DcB["attempt"] += 1
       path, err = FF913T(picUrl, picon, timeout=1, mustBeImage=True)
       if path:
        if VVC69w:
         VVC69w.VV0DcB["ok"] += 1
         VVC69w.VVRqfk(VVC69w.VV0DcB["ok"])
        if FFT03z(path) > 0:
         cmd = CCARMv.VVc7qU(path)
         cmd += FFxtg8("mv -f '%s' '%s'" % (path, pPath)) + ";"
         os.system(cmd)
        else:
         if VVC69w:
          VVC69w.VV0DcB["size0"] += 1
         FFX92w(path)
       elif err:
        if VVC69w:
         VVC69w.VV0DcB["fail"] += 1
        if any(x in err.lower() for x in ("time-out", "unauthorized")):
         if VVC69w:
          VVC69w.VV0DcB["err"] = err.title()
         break
      else:
       if VVC69w:
        VVC69w.VV0DcB["exist"] += 1
     else:
      if VVC69w:
       VVC69w.VV0DcB["badURL"] += 1
  except:
   pass
 def VVVkyv(self):
  title = "Download PIcons for Current Bouquet"
  if os.system(FFxtg8("which ffmpeg")) == 0:
   self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
       , titlePrefix = ""
       , fncToRun  = self.VVzhaM
       , VVnFNJ = BF(self.VVaKEs, title))
  else:
   FFMIbO(self, BF(CCqQHV.VV4Lee, self), '"FFmpeg" is required to resize the PIcons.\n\nInstall FFmpeg ?', title=title)
 def VVzhaM(self, VVC69w):
  bName = CCgKdM.VVNJJo()
  pPath = CCrs3r.VVsNIk()
  totNotIptv = totServErr = totParseErr = totUnauth = totCh = totIptv = totPic = totPicOK = totInvServ = totInvPicUrl = totSize0 = totExist = 0
  VVC69w.VV0DcB = (bName, "", totNotIptv, totServErr, totParseErr, totUnauth, totCh, totIptv, totPic, totPicOK, totInvServ, totInvPicUrl, totSize0, totExist)
  services = CCgKdM.VVsvhM()
  if not VVC69w or VVC69w.isCancelled:
   return
  if not services or len(services) == 0:
   VVC69w.VV0DcB = (bName, 'Invalid Services in Bouquet: \n\n"%s"' % bName, totNotIptv, totServErr, totParseErr, totUnauth, totCh, totIptv, totPic, totPicOK, totInvServ, totInvPicUrl, totSize0, totExist)
   return
  totCh = len(services)
  VVC69w.VVYqos(totCh)
  VVC69w.VVRqfk(0)
  for serv in services:
   if not VVC69w or VVC69w.isCancelled:
    return
   VVC69w.VV0DcB = (bName, "", totNotIptv, totServErr, totParseErr, totUnauth, totCh, totIptv, totPic, totPicOK, totInvServ, totInvPicUrl, totSize0, totExist)
   VVC69w.VVLLRh(1)
   VVC69w.VVRqfk(totPic)
   fullRef  = serv[0]
   if FFuZb6(fullRef):
    totIptv += 1
   else:
    totNotIptv += 1
    continue
   refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(fullRef)
   picon = refCode.replace(":", "_").rstrip("_") + ".png"
   if fileExists(pPath + picon):
    totExist += 1
    continue
   span = iSearch(r"mode=.+&end=:(.+)", fullRef, IGNORECASE)
   if span:
    valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query, m3u_Url, host, user1, pass1, streamId, err = CCyIre.VVcW91(decodedUrl)
    uHost, uUser, uPass, uId, uChName = host, user1, pass1, streamId, span.group(1)
   else:
    m3u_Url = decodedUrl
    uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(m3u_Url)
   if not all([uHost, uUser, uPass, uId]):
    totInv += 1
    continue
   qUrl = "%s/player_api.php?username=%s&password=%s&action=get_vod_info&vod_id=%s" % (uHost, uUser, uPass, uId)
   txt, err = CCqQHV.VVpi8S(qUrl)
   if err:
    totServErr += 1
    if "Unauth" in err:
     totUnauth += 1
    continue
   try:
    epg, picUrl = CCARMv.VVEOl4(jLoads(txt))
   except:
    totParseErr += 1
    continue
   if not picUrl:
    totInvPicUrl += 1
    continue
   totPic += 1
   path, err = FF913T(picUrl, picon, timeout=1, mustBeImage=True)
   if path:
    if VVC69w:
     VVC69w.VVRqfk(totPic)
    if FFT03z(path) > 0:
     cmd = CCARMv.VVc7qU(path)
     cmd += FFxtg8("mv -f '%s' '%s'" % (path, pPath)) + ";"
     os.system(cmd)
     totPicOK += 1
    else:
     totSize0
     FFX92w(path)
  if VVC69w:
   VVC69w.VV0DcB = (bName, "", totNotIptv, totServErr, totParseErr, totUnauth, totCh, totIptv, totPic, totPicOK, totInvServ, totInvPicUrl, totSize0, totExist)
 def VVaKEs(self, title, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  bName, err, totNotIptv, totServErr, totParseErr, totUnauth, totCh, totIptv, totPic, totPicOK, totInvServ, totInvPicUrl, totSize0, totExist = VV0DcB
  if err:
   FFkYsE(self, err, title=title)
  else:
   txt = ""
   txt += "Bouquet\t: %s\n"  % bName
   txt += "Services\t: %d\n"  % totCh
   txt += "Processed\t: %d\n"  % totIptv
   txt += "\n"
   txt += "PIcons Found\t: %d\n" % totPic
   txt += "PIcons Added\t: %d\n" % totPicOK
   if totUnauth or totExist or totNotIptv or totServErr or totParseErr or totInvServ or totInvPicUrl or totSize0:
    txt += "\n"
    t1 = ""
    if totUnauth:
     if totUnauth == totServErr : t1 = "  (All Unauthorized)"
     else      : t1 = "  (%d Unauthorized)" % totUnauth
    if totExist  : txt += "PIcons Exist\t: %s\n"  % FFkhYI(str(totExist)  , VVU8eD)
    if totNotIptv : txt += "Not IPTV\t: %s\n"   % FFkhYI(str(totNotIptv)  , VVU8eD)
    if totServErr : txt += "Server Errors\t: %s\n" % FFkhYI(str(totServErr) + t1, VVU8eD)
    if totParseErr : txt += "Parse Errors\t: %s\n"  % FFkhYI(str(totParseErr) , VVU8eD)
    if totInvServ : txt += "Invalid Ser. URL\t: %s\n" % FFkhYI(str(totInvServ)  , VVU8eD)
    if totInvPicUrl : txt += "Invalid Pic. URL\t: %s\n" % FFkhYI(str(totInvPicUrl) , VVU8eD)
    if totSize0  : txt += "PIcons Size = 0\t: %s\n" % FFkhYI(str(totSize0)  , VVU8eD)
   if not VVr4Ej:
    title += "  (stopped)"
   FFNEkd(self, txt, title=title)
 @staticmethod
 def VV4Lee(SELF):
  cmd = FFQ7Q5(VV4pye, "ffmpeg")
  if cmd : FFfbee(SELF, cmd, title="Installing FFmpeg")
  else : FFHRK6(SELF)
 def VVNgba(self):
  self.session.open(CCC6u0, barTheme=CCC6u0.VVY9N6
      , titlePrefix = ""
      , fncToRun  = self.VVfo5G
      , VVnFNJ = self.VV6WLs)
 def VVfo5G(self, VVC69w):
  bName = CCgKdM.VVNJJo()
  uChName = ""
  totNotIptv = totServErr = totUnauth = totCh = totIptv = totEpg = totEpgOK = totInv = 0
  VVC69w.VV0DcB = (bName, "", totNotIptv, totServErr, totUnauth, totCh, totIptv, totEpg, totEpgOK, totInv)
  services = CCgKdM.VVsvhM()
  if not VVC69w or VVC69w.isCancelled:
   return
  if services and len(services) > 0:
   totCh = len(services)
   VVC69w.VVYqos(totCh)
   for serv in services:
    if not VVC69w or VVC69w.isCancelled:
     return
    VVC69w.VVLLRh(1)
    fullRef = serv[0]
    if FFuZb6(fullRef):
     totIptv += 1
     refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(fullRef)
     span = iSearch(r"mode=.+&end=:(.+)", fullRef, IGNORECASE)
     if span:
      valid, ph1, playHost, mode, host, mac, epNum, epId, chCm, query, m3u_Url, host, user1, pass1, streamId, err = CCyIre.VVcW91(decodedUrl)
      if valid and mode == "itv" : uHost, uUser, uPass, uId, uChName = host, user1, pass1, streamId, span.group(1)
      else      : uHost = uUser = uPass = uId = uChName = ""
     else:
      m3u_Url = decodedUrl
      uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(m3u_Url)
     if VVC69w:
      VVC69w.VVezgz(totEpgOK, uChName)
     if all([uHost, uUser, uPass, uId]):
      url = "%s/get.php?username=%s&password=%s" % (uHost, uUser, uPass)
      pList, err = CCqQHV.VVQu9u(url, uId)
      if err:
       totServErr += 1
       if "Unauth" in err:
        totUnauth += 1
      elif pList:
       totEv, totOK = CCARMv.VVbwY9(refCode, pList)
       totEpg += totEv
       totEpgOK += totOK
     else:
      totInv += 1
    else:
     totNotIptv += 1
    if VVC69w:
     VVC69w.VV0DcB = (bName, "", totNotIptv, totServErr, totUnauth, totCh, totIptv, totEpg, totEpgOK, totInv)
  else:
   VVC69w.VV0DcB = (bName, 'Invalid Services in Bouquet: \n\n"%s"' % bName, totNotIptv, totServErr, totUnauth, totCh, totIptv, totEpg, totEpgOK, totInv)
 def VV6WLs(self, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  bName, err, totNotIptv, totServErr, totUnauth, totCh, totIptv, totEpg, totEpgOK, totInv = VV0DcB
  title = "IPTV EPG Import"
  if err:
   FFkYsE(self, err, title=title)
  else:
   if VVr4Ej and totEpgOK > 0:
    CC2LVn.VVdL9t()
   txt = ""
   txt += "Bouquet\t: %s\n"  % bName
   txt += "Services\t: %d\n\n"  % totCh
   txt += "Processed\t: %d\n"  % totIptv
   txt += "Events Found\t: %d\n" % totEpg
   txt += "Events Added\t: %d\n" % totEpgOK
   if totNotIptv or totInv or totServErr or totUnauth:
    txt += "\n"
    t1 = ""
    if totUnauth:
     if totUnauth == totServErr : t1 = "  (All Unauthorized)"
     else      : t1 = "  (%d Unauthorized)" % totUnauth
    if totNotIptv : txt += "Not IPTV\t: %s\n"   % FFkhYI(str(totNotIptv), VVU8eD)
    if totServErr : txt += "Server Errors\t: %s\n" % FFkhYI(str(totServErr) + t1, VVU8eD)
    if totInv  : txt += "Invalid URL\t: %s\n"  % FFkhYI(str(totInv), VVU8eD)
   if not VVr4Ej:
    title += "  (stopped)"
   FFNEkd(self, txt, title=title)
 @staticmethod
 def VVQu9u(chUrl, streamId, isForCatchupTV=False):
  modified, uURL, uProtoc, uHost, uPort, uQuery, uUser, uPass, uQueryParam = CCqQHV.VVuRWx(chUrl)
  qUrl = "%splayer_api.php?username=%s&password=%s&action=get_simple_data_table&stream_id=%s" % (uURL, uUser, uPass, streamId)
  txt, err = CCqQHV.VVpi8S(qUrl)
  if err:
   return "", err
  pList = []
  try:
   tDict = jLoads(txt)
   for item in tDict["epg_listings"]:
    description   = CCqQHV.VVvsIK(item, "description" , is_base64=True ).replace("\n", " .. ")
    lang    = CCqQHV.VVvsIK(item, "lang"        ).upper()
    now_playing   = CCqQHV.VVvsIK(item, "now_playing"      )
    start    = CCqQHV.VVvsIK(item, "start"        )
    start_timestamp  = CCqQHV.VVvsIK(item, "start_timestamp", isDate=True  )
    start_timestamp_unix= CCqQHV.VVvsIK(item, "start_timestamp"     )
    stop_timestamp  = CCqQHV.VVvsIK(item, "stop_timestamp" , isDate=True  )
    stop_timestamp_unix = CCqQHV.VVvsIK(item, "stop_timestamp"      )
    tTitle    = CCqQHV.VVvsIK(item, "title"   , is_base64=True )
    if isForCatchupTV:
     try:
      if int(start_timestamp_unix) < iTime():
       dur = str(int((int(stop_timestamp_unix) - int(start_timestamp_unix)) / 60))
       pList.append((start_timestamp[:-3], stop_timestamp[:-3], lang, tTitle, description, start, now_playing, dur))
     except:
      pass
    else:
     try:
      if int(stop_timestamp_unix) > iTime():
       start  = int(start_timestamp_unix)
       dur   = int(int(stop_timestamp_unix) - int(start_timestamp_unix))
       shortDesc = ("Language : %s" % lang) if lang else ""
       pList.append((start, dur, tTitle, shortDesc, description, 1))
     except:
      pass
  except:
   return "", "Cannot parse received data !"
  return pList, ""
 @staticmethod
 def VVyKHt(catID, stID, chNum):
  MAX_4b = 65535
  MAX_8b = 4294967295
  SID  = CCqQHV.VVPxX4(catID, MAX_4b)
  TSID = CCqQHV.VVPxX4(chNum, MAX_4b)
  ONID = CCqQHV.VVPxX4(chNum, MAX_4b)
  NS  = CCqQHV.VVPxX4(stID, MAX_8b)
  if len(NS) == 4:
   NS = "1" + NS
  rType = CFG.iptvAddToBouquetRefType.getValue()
  return "%s:0:1:%s:%s:%s:%s:0:0:0:" % (rType, SID, TSID, ONID, NS)
 @staticmethod
 def VVPxX4(numStr, limit):
  if numStr.isdigit():
   i = int(numStr)
   if i > limit:
    i = limit
   return (hex(i))[2:].upper()
  else:
   return "222"
 @staticmethod
 def VVwvI5(txt):
  txt = iSub(iCompile('\W'), "_", txt)
  while "__" in txt:
   txt = txt.replace("__", "_")
  txt = txt.strip("_")
  if txt : return txt
  else : return "Bouquet"
 @staticmethod
 def VViepZ(mode):
  if   mode in ("itv"  , CCqQHV.VVZ3on)  : return "#0a21303C", "#0a21303C", "#0a21303C", "#04224040"
  elif mode in ("vod"  , CCqQHV.VVzxcn)  : return "#1a260518", "#1a260518", "#1a260518", "#04224040"
  elif mode in ("series" , CCqQHV.VVTVFh) : return "#1a36013F", "#1a26012F", "#1a26012F", "#04224040"
  elif mode in ("catchup" , CCqQHV.VV9YnV) : return "#0a213044", "#0a213044", "#0a21303C", "#04224040"
  elif mode == CCqQHV.VV3KJK    : return "#0a202020", "#0a202020", "#0a202020", "#04224040"
  elif mode == "series2"            : return "#0a462538", "#0a462538", "#0a462538", "#04224040"
  else                : return "#0a00292B", "#0a002126", "#0a002126", "#00000000"
 def VVLdnU(self, mode):
  err = excl = ""
  dirs = []
  path = "/"
  if CFG.iptvHostsMode.getValue() == VVXLG3:
   excl = FFlfqZ(1)
  else:
   lst = list(set(list(map(str.strip, CFG.iptvHostsDirs.getValue().split(",")))))
   tList = []
   for Dir in lst:
    if pathExists(Dir):
     tList.append(Dir)
   lst = sorted(tList, key=len)
   for Dir in lst:
    for dir1 in dirs:
     if len(Dir) > len(dir1) and Dir.startswith(dir1):
      break
    else:
     dirs.append(Dir)
   if   len(dirs) == 1 : path = dirs[0]
   elif len(dirs) > 1 : path = "{%s}" % ",".join(dirs)
   if not dirs:
    FFkYsE(self, 'Directory not found !\n\nCheck your settings option:\n\n"IPTV Hosts Files Path (Playlist, Portal, M3U)"')
    return []
  if   mode == 1: par = '-iname "*playlist*" | grep -i ".txt"'
  elif mode == 2: par = '\( -iname "*portal*" -o -iname "*stalker*" \) | grep -i "\.txt\|\.conf"'
  elif mode == 3: par = "-iname '*.m3u' -o -iname '*.m3u8' | grep -i '.m3u*'"
  files = FFiGf6('find %s %s %s' % (path, excl, par))
  if not files:
   if   path == "/": txt = "!"
   elif dirs  : txt = "in directories listed in settings !"
   else   : txt = "in :\n%s" % path
   if   mode == 1: err = 'No Playlist files found %s\n\n Expecting ".txt" files\n(names must include the word "playlist")' % txt
   elif mode == 2: err = 'No portal files found %s\n\n Expecting ".txt" or ".conf" files\n(name must include the word "portal" or "stalker")' % txt
   elif mode == 3: err = 'No ".m3u" files found %s' % txt
   FFkYsE(self, err)
  elif len(files) == 1 and files[0] == VVCYwM:
   FFkYsE(self, VVCYwM)
  else:
   return files
 @staticmethod
 def VVfFAE():
  for path in (CFG.backupPath.getValue(), CFG.exportedTablesPath.getValue(), "/tmp/"):
   if pathExists(path):
    return FF0WrY(path)
  return "/"
 @staticmethod
 def VV44HD(SELF, hostUrl, chName, streamId, ok_fnc):
  pList, err = CCqQHV.VVQu9u(hostUrl, streamId, True)
  title = "Catch-up TV Programs"
  if err:
   FFkYsE(SELF, "Server Error:\n\n%s" % err, title=title)
  elif pList:
   pList.sort(key=lambda x: x[0], reverse=True)
   c = "#f#00FFFF55#"
   for ndx, item in enumerate(pList):
    if item[6] == "1":
     pList[ndx] = (c + item[0], c + item[1], c + item[2], c + item[3], c + item[4], c + item[5], c + item[6], c + item[7])
     break
   VVz2kc, VVwpZm, VVghPi, VV0g1U = CCqQHV.VViepZ("")
   VVMQj9 = ("Home Menu" , FFSJQP, [])
   VVVHmY  = ("Play"  , ok_fnc , [])
   header   = ("Start" , "End" , "Lang", "Title" , "Description" , "sTime" , "Playing" , "Duration")
   widths   = (17  , 17 , 6  , 31  , 31   , 0   , 0   , 0   )
   VVQqg2  = (CENTER , CENTER, CENTER, LEFT  , LEFT   , CENTER , CENTER , CENTER )
   FF1dQ4(SELF, None, title="Programs for : " + chName, header=header, VVvytR=pList, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=24, VVVHmY=VVVHmY, VVMQj9=VVMQj9, VVz2kc=VVz2kc, VVwpZm=VVwpZm, VVghPi=VVghPi, VV0g1U=VV0g1U)
  else:
   FFkYsE(SELF, "No Programs from server", title=title)
 @staticmethod
 def VV8M6j(rUrl, fPath):
  fPath = fPath.strip()
  if fPath.startswith("http://"):
   return fPath
  elif fPath.startswith("/"):
   try:
    res = iUrlparse(rUrl)
    scheme = res.scheme
    netloc = res.netloc
    if scheme and netloc:
     host = "%s://%s" % (scheme, netloc)
     return os.path.join(host, fPath.lstrip("/"))
   except:
    pass
   return ""
  else:
   baseUrl = os.path.dirname(rUrl).strip()
   fName = os.path.basename(rUrl).strip()
   return os.path.join(baseUrl, fPath)
 @staticmethod
 def VVyq4W(SELF, isPortal, line, VVp2lZObj, item):
  myPath = "/media/usb/AAA/IPTV-Files/"
  if pathExists(myPath) : path = myPath
  else     : path = CCqQHV.VVfFAE()
  if isPortal : path += "Portal_Bookmarks.txt"
  else  : path += "Playlist_Bookmarks.txt"
  title = "Bookmark Current Server"
  try:
   if fileExists(path):
    with ioOpen(path, "r", encoding="utf-8") as f:
     for fLine in f:
      if str(line) in str(fLine):
       FFkYsE(SELF, "Already added to file:\n\n%s" % path, title=title)
       return
   with open(path, "a") as f:
    f.write(line + "\n")
   FFewCE(SELF, "Added to file:\n\n%s" % path, title=title)
  except Exception as e:
   FFkYsE(SELF, "Error:\n\n%s" % str(e), title=title)
 def VVbsEO(self, source, mode, curBName, VVcpnp, title, txt, colList):
  isMulti = VVcpnp.VVbl0M
  itemsOK = True
  totTxt = "ALL"
  if isMulti:
   tot = VVcpnp.VVMJsS()
   totTxt = "%d Service%s" % (tot, FFICXm(tot))
   if tot < 1:
    itemsOK = False
  totTxt = FFkhYI(totTxt, VVoTT6)
  mSel = CCqgU8(self, VVcpnp, addSep=False)
  VV625J, cbFncDict = [], None
  VV625J.append(VVm77t)
  if itemsOK:
   VV625J.append(("Add %s to New Bouquet : %s" % (totTxt, FFkhYI(curBName, VV9cEK)), "addToCur"))
   VV625J.append(("Add %s to Other Bouquet ..." % (totTxt)          , "addToNew"))
   cbFncDict = { "addToCur": BF(FFlX3B, mSel.VVcpnp, BF(self.VVeTXO,source, mode, curBName, VVcpnp, title), title="Adding Services ...")
      , "addToNew": BF(self.VVIcT5, source, mode, curBName, VVcpnp, title)
      }
  else:
   VV625J.append(("Add to Bouquet (nothing selected)", ))
  mSel.VVMNiz(VV625J, cbFncDict)
 def VVeTXO(self, source, mode, curBName, VVcpnp, Title):
  chUrlLst = self.VVU3Y0(source, mode, VVcpnp)
  CCgKdM.VVLBiS(self, Title, curBName, "", chUrlLst)
 def VVIcT5(self, source, mode, curBName, VVcpnp, Title):
  picker = CCgKdM(self, VVcpnp, Title, BF(self.VVU3Y0, source, mode, VVcpnp), defBName=curBName)
 def VVU3Y0(self, source, mode, VVcpnp):
  totChange = 0
  isMulti = VVcpnp.VVbl0M
  chUrlLst = []
  rowNum = 0
  for ndx, row in enumerate(VVcpnp.VVGrbO()):
   if not isMulti or VVcpnp.VV3fqU(ndx):
    chUrl = chName = 0
    if source in ("pEp", "pCh"):
     chName, catID, stID, chNum, chCm, serCode, serId, picUrl = self.VVrhWs(mode, row)
     refCode, chUrl = self.VVWeZp(self.VVPj61, self.VVrGQ8, mode, chName, catID, stID, chNum, chCm, serCode, serId)
    elif source == "m3Ch":
     chName = row[1].strip()
     url  = row[3].strip()
     chUrl = self.VViWtl(rowNum, url, chName)
     rowNum += 1
    elif source in ("lv", "v", "s", "fnd"):
     chName, chUrl, picUrl, refCode = self.VV1lQi(mode, row)
    if chUrl and chName:
     chUrlLst.append(chUrl)
  return chUrlLst
class CC7Gx2(Screen):
 def __init__(self, session, title="", csel=None, refCode="", servName="", bouquetRoot="", isFind=False):
  self.skin, self.skinParam = FF896P(VVoxS0, 700, 800, 50, 40, 30, "#22000033", "#22000011", 30)
  self.session     = session
  self.csel      = csel
  self.refCode     = refCode
  self.servName     = servName
  self.findTxt     = servName
  self.bouquetRoot    = bouquetRoot
  self.isFindMode     = isFind
  self.VV0IaT  = 0
  self.VVoZvP = 1
  self.VVoXYv  = 2
  VV625J = []
  VV625J.append(("Find in All Service (from filter)" , "VVcH6w" ))
  VV625J.append(VVm77t)
  VV625J.append(("Find in All (Manual Entry)"   , "VVPEQr"    ))
  VV625J.append(("Find in TV"       , "VVXRzB"    ))
  VV625J.append(("Find in Radio"      , "VVGMZ7"   ))
  if self.VVcw2d():
   VV625J.append(VVm77t)
   VV625J.append(("Hide Channel: %s" % self.servName , "VVzMZC"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Zap History"       , "VVPqgO"    ))
  VV625J.append(VVm77t)
  VV625J.append(("IPTV Tools"       , "iptv"      ))
  VV625J.append(("PIcons Tools"       , "PIconsTools"     ))
  VV625J.append(("Services/Channels Tools"    , "ChannelsTools"    ))
  FFJd2Z(self, VV625J=VV625J, title=title)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self)
  if self.isFindMode:
   self.VVtDnr(self.VVwfgY())
 def VVmz9T(self):
  global VVyQYx
  VVyQYx = self["myMenu"].l.getCurrentSelection()[0]
  item   = self["myMenu"].l.getCurrentSelection()[1]
  if item is not None:
   if   item == "VVPEQr"    : self.VVPEQr()
   elif item == "VVcH6w" : self.VVcH6w()
   elif item == "VVXRzB"    : self.VVXRzB()
   elif item == "VVGMZ7"   : self.VVGMZ7()
   elif item == "VVzMZC"   : self.VVzMZC()
   elif item == "VVPqgO"    : self.VVPqgO()
   elif item == "iptv"       : self.session.open(CCqQHV)
   elif item == "PIconsTools"     : self.session.open(CCrs3r)
   elif item == "ChannelsTools"    : self.session.open(CCtSdI)
   if item in ("iptv", "PIconsTools", "ChannelsTools"):
    self.close()
 def VVXRzB(self) : self.VVtDnr(self.VV0IaT)
 def VVGMZ7(self) : self.VVtDnr(self.VVoZvP)
 def VVPEQr(self) : self.VVtDnr(self.VVoXYv)
 def VVtDnr(self, mode):
  title = "Find %s Service" % ("TV", "Radio", "All")[mode]
  FFbRXK(self, BF(self.VVid4y, mode), defaultText=self.findTxt, title=title, message="Enter Name:")
 def VVcH6w(self):
  filterObj = CCU3qf(self)
  filterObj.VVmiWt(self.VVuplI)
 def VVuplI(self, item):
  self.VVid4y(self.VVoXYv, item)
 def VVcw2d(self):
  if self.servName.strip() == ""      : return False
  if self.refCode.strip()  == ""      : return False
  if self.refCode.startswith("1:7:1:0:0:0:0:0:0:0:") : return False
  if FFuZb6(self.refCode)        : return False
  return True
 def VVid4y(self, mode, VVfJWE):
  FFlX3B(self, BF(self.VVMO5n, mode, VVfJWE), title="Searching ...")
 def VVMO5n(self, mode, VVfJWE):
  if VVfJWE:
   VVfJWE = VVfJWE.strip()
  if VVfJWE:
   self.findTxt = VVfJWE
   CFG.lastFindContextFind.setValue(VVfJWE)
   if   mode == self.VV0IaT  : titlTxt, servTypes = "TV"  , service_types_tv
   elif mode == self.VVoZvP : titlTxt, servTypes = "Radio"  , service_types_radio
   else          : titlTxt, servTypes = "All" , "1:7:"
   title = 'Find %s : "%s"' % (titlTxt, VVfJWE)
   if len(title) > 55:
    title = title[:55] + ".."
   VVvhuK = self.VV3xHg(VVfJWE, servTypes)
   if self.isFindMode or mode == self.VVoXYv:
    VVvhuK += self.VVnoGx(VVfJWE)
   if VVvhuK:
    VVvhuK.sort(key=lambda x: x[0].lower())
    VVfPgM = self.VVHDtx
    VVVHmY  = ("Zap"   , self.VVFxYv    , [])
    VV3th8 = ("Current Service", self.VVbvBc , [])
    VVOtSO = ("Options"  , self.VVsL6Y , [])
    VV01dN = (""    , self.VVWOGS , [])
    header   = ("Name" , "Type", "Ref.", "Sat.", "Freq." , "Pol.", "FEC" , "SR" )
    widths   = (38  , 17 , 0  , 10 , 10  , 7  , 8  , 10 )
    VVQqg2  = (LEFT  , CENTER, LEFT  , CENTER, CENTER , CENTER, CENTER, CENTER)
    FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VVfPgM=VVfPgM, VV3th8=VV3th8, VVOtSO=VVOtSO, VV01dN=VV01dN, lastFindConfigObj=CFG.lastFindContextFind)
   else:
    self.VVtDnr(self.VVwfgY())
    FFewCE(self, "Not found", title=title)
  elif self.isFindMode:
   self.close()
  else:
   self.findTxt = self.servName
 def VV3xHg(self, VVfJWE, servTypes):
  VVvytR = CCtSdI.VVLZZO(servTypes)
  VVvhuK = []
  if VVvytR:
   VVUDHC, VV1Lo5 = FF92xJ()
   tp = CCX8JT()
   words, asPrefix = CCU3qf.VVP88C(VVfJWE)
   colorYellow  = CCLqkY.VVdf1F(VVdWFT)
   colorWhite  = CCLqkY.VVdf1F(VVZgqQ)
   for s in VVvytR:
    name = s[1]
    for word in words:
     ok = False
     tName = name.lower()
     if asPrefix:
      if tName.startswith(word):
       ok = True
     elif word in tName:
      ok = True
     if ok:
      refCode = s[0]
      if refCode.count(":") > 8:
       if asPrefix:
        name = iSub(r"(%s)" % iEscape(word), r"%s\1%s" % (colorYellow, colorWhite), name, count=1, flags=IGNORECASE)
       else:
        name = iSub(r"(%s)" % iEscape(word), r"%s\1%s" % (colorYellow, colorWhite), name, flags=IGNORECASE)
       sat = FF24qC(refCode, False)
       STYPE  = refCode.split(":")[2]
       sTypeInt = int(STYPE, 16)
       if sTypeInt in VVUDHC:
        STYPE = VV1Lo5[sTypeInt]
       freq, pol, fec, sr, syst = tp.VVZtm9(refCode)
       if not "-S" in syst:
        sat = syst
       VVvhuK.append((name, STYPE, refCode, sat, freq, pol, fec, sr))
  return VVvhuK
 def VVnoGx(self, VVfJWE):
  VVfJWE = VVfJWE.lower()
  VVvhuK = []
  colorYellow  = CCLqkY.VVdf1F(VVdWFT)
  colorWhite  = CCLqkY.VVdf1F(VVZgqQ)
  for b in CCgKdM.VV8uSL():
   VVb6wY  = b[0]
   VVdUEV  = b[1].toString()
   VVfVMT = eServiceReference(VVdUEV)
   VVa6xc = FFocgD(VVfVMT)
   for service in VVa6xc:
    refCode  = service[0]
    if FFuZb6(refCode):
     servName = service[1]
     if VVfJWE in servName.lower():
      servName = iSub(r"(%s)" % iEscape(VVfJWE), r"%s\1%s" % (colorYellow, colorWhite), servName, flags=IGNORECASE)
      VVvhuK.append((servName, "IPTV", refCode, "-", "-", "-", "-", "-"))
  return VVvhuK
 def VVwfgY(self):
  VVurhM = InfoBar.instance
  if VVurhM:
   VVoSQy = VVurhM.servicelist
   if VVoSQy:
    return VVoSQy.mode == 1
  return self.VVoXYv
 def VVHDtx(self, VVcpnp):
  self.close()
  VVcpnp.cancel()
 def VVFxYv(self, VVcpnp, title, txt, colList):
  FFJZ42(VVcpnp, colList[2], VVpyjK=False, checkParentalControl=True)
 def VVbvBc(self, VVcpnp, title, txt, colList):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(VVcpnp)
  if refCode:
   VVcpnp.VV8yro(2, FFcJ7o(refCode, iptvRef, chName), True)
 def VVsL6Y(self, VVcpnp, title, txt, colList):
  servName = colList[0]
  mSel = CCqgU8(self, VVcpnp)
  VV625J, cbFncDict = CCtSdI.VVazuu(self, VVcpnp, servName, 2)
  mSel.VVMNiz(VV625J, cbFncDict)
 def VVWOGS(self, VVcpnp, title, txt, colList):
  chName = colList[0]
  refCode = colList[2]
  ndx = txt.find("Sat.")
  if ndx > -1:
   txt = txt[:ndx]
  FFBatl(self, fncMode=CCARMv.VVae7k, refCode=refCode, chName=chName, text=txt)
 def VVzMZC(self):
  FFMIbO(self, self.VVOYDU, 'Hide "%s" ?' % self.servName, title="Hide Channel")
 def VVOYDU(self):
  ret = FFexa9(self.refCode, True)
  if ret:
   self.VVkvT2()
   self.close()
  else:
   FFD1yO(self, "Cannot change state" , 1000)
 def VVkvT2(self):
  if self.csel:
   self.csel.servicelist.removeCurrent()
  try:
   self.VVR4mo()
  except:
   self.VVcpsu()
  if self.refCode.count(":") > 8:
   servRef = self.session.nav.getCurrentlyPlayingServiceReference()
   if servRef and self.refCode in servRef.toString():
    self.session.nav.stopService()
    if self.csel:
     serviceRef = self.csel.servicelist.getCurrent()
     if serviceRef:
      FFSRyd(self, serviceRef)
 def VVR4mo(self):
  if self.refCode:
   servRef = eServiceReference(self.refCode)
   VVurhM = InfoBar.instance
   if VVurhM:
    VVoSQy = VVurhM.servicelist
    if VVoSQy:
     hList = VVoSQy.history
     newList = []
     for rec in hList:
      for servRef in rec:
       if self.refCode in servRef.toString():
        break
      else:
       newList.append(rec)
     if newList:
      oldLen = len(hList)
      newLen = len(newList)
      diff = oldLen - newLen
      if not diff == 0:
       pos = VVoSQy.history_pos - diff
       if pos > newLen -1 : pos = newLen - 1
       if pos < 0   : pos = 0
       VVoSQy.history  = newList
       VVoSQy.history_pos = pos
 def VVcpsu(self):
  VVurhM = InfoBar.instance
  if VVurhM:
   VVoSQy = VVurhM.servicelist
   if VVoSQy:
    VVoSQy.history  = []
    VVoSQy.history_pos = 0
 def VVPqgO(self):
  VVurhM = InfoBar.instance
  VVvhuK = []
  if VVurhM:
   VVoSQy = VVurhM.servicelist
   if VVoSQy:
    VVUDHC, VV1Lo5 = FF92xJ()
    for serv in VVoSQy.history:
     refCode = serv[-1].toString()
     chName = FFy0JC(refCode)
     path = serv[-1].getPath()
     isLocal = path and path.startswith("/")
     isIptv = FFuZb6(refCode)
     if   isIptv or isLocal : sat = "-"
     else     : sat = FF24qC(refCode, True)
     if isIptv : STYPE = "IPTV"
     elif isLocal: STYPE = "Local Media"
     else:
      STYPE  = refCode.split(":")[2]
      sTypeInt = int(STYPE, 16)
      if sTypeInt in VVUDHC:
       STYPE = VV1Lo5[sTypeInt]
     VVvhuK.append((chName, sat, STYPE, refCode))
  title = "Zap History"
  if VVvhuK:
   VVVHmY  = ("Zap"   , self.VVY09Y   , [])
   VVOtSO = ("Clear History" , self.VV1CP5   , [])
   VV01dN = (""    , self.VVwe6e , [] )
   header   = ("Service Name", "Satellite" , "Type" , "Ref. Code" )
   widths   = (41    , 41   , 18  , 0    )
   VVQqg2  = (LEFT    , LEFT   , CENTER , LEFT   )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VVVHmY=VVVHmY, VVOtSO=VVOtSO, VV01dN=VV01dN)
  else:
   FFewCE(self, "Not found", title=title)
 def VVY09Y(self, VVcpnp, title, txt, colList):
  FFJZ42(VVcpnp, colList[3], VVpyjK=False, checkParentalControl=True)
 def VV1CP5(self, VVcpnp, title, txt, colList):
  FFMIbO(self, BF(self.VVJnml, VVcpnp), "Clear Zap History ?")
 def VVJnml(self, VVcpnp):
  self.VVcpsu()
  VVcpnp.cancel()
 def VVwe6e(self, VVcpnp, title, txt, colList):
  chName = colList[0]
  refCode = colList[3]
  FFBatl(self, fncMode=CCARMv.VVRYNT, refCode=refCode, chName=chName, text=txt)
class CCrs3r(Screen):
 VVIcXD   = 0
 VVsPK2  = 1
 VVBp7W  = 2
 VVlZgM  = 3
 VVDcUS  = 4
 VVnKah  = 5
 VVf4Re  = 6
 VV93KM  = 7
 VVlsNO = 8
 VVdO4v = 9
 VV3Joy = 10
 VVXNEc = 11
 def __init__(self, session):
  self.skin, self.skinParam = FF896P(VVOdhH, 1400, 840, 30, 10, 14, "#22201000", "#33000000", 30, barHeight=40, topRightBtns=2)
  self.session   = session
  self.Title    = "PIcons Tools"
  FFJd2Z(self, self.Title)
  FFHhgX(self["keyRed"] , "OK = Zap")
  FFHhgX(self["keyGreen"] , "Current Service")
  FFHhgX(self["keyYellow"], "Page Options")
  FFHhgX(self["keyBlue"] , "Filter")
  self.TOTAL_ROWS   = 5
  self.TOTAL_COLS   = 7
  self.PAGE_PICONS  = self.TOTAL_ROWS * self.TOTAL_COLS
  self.pPath    = CCrs3r.VVsNIk()
  self.curChanName  = ""
  self.curChanFile  = ""
  self.curChanIndex  = -1
  self.curChanRefCode  = 0
  self.curChanIptvRef  = ""
  self.VVvytR    = []
  self.totalPIcons  = 0
  self.totalPages   = 0
  self.curPage   = 0
  self.curRow    = 0
  self.curCol    = 0
  self.curIndex   = 0
  self.lastRow   = 0
  self.lastCol   = 0
  self.nsList    = set()
  self.lastSortCol  = 0
  self.lastMode   = 0
  self.lastWords   = ['']
  self.lastAsPrefix  = False
  self.lastTimeStamp  = 0
  self.lastSTypeList  = 0
  self.lastFind   = ""
  self.filterTitle  = ""
  self.isBusy    = True
  self["myPiconPtr"]  = Label()
  self["myPiconF"]  = Label()
  self["myPiconBG"]  = Label()
  self["myPiconPic"]  = Pixmap()
  self["myPiconF"].hide()
  self["myPiconBG"].hide()
  self["myPiconPic"].hide()
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    self["myPicon%d%d" % (row, col)] = Pixmap()
    self["myPicon%d%d" % (row, col)].hide()
    self["myPiconLbl%d%d" % (row, col)] = Label()
    self["myPiconLbl%d%d" % (row, col)].hide()
  for i in range(6):
   self["myPiconInf%d" % i] = Label()
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : self.VVYuo3     ,
   "green"   : self.VVcgQQ    ,
   "yellow"  : self.VV9Ce1     ,
   "blue"   : self.VV7Bkj     ,
   "menu"   : self.VVD3bX     ,
   "info"   : self.VVaAx7    ,
   "up"   : self.VVmkvi       ,
   "down"   : self.VVcuOr      ,
   "left"   : self.VV8g7c      ,
   "right"   : self.VVkPgM      ,
   "pageUp"  : BF(self.VVMr9U, True) ,
   "chanUp"  : BF(self.VVMr9U, True) ,
   "pageDown"  : BF(self.VVMr9U, False) ,
   "chanDown"  : BF(self.VVMr9U, False) ,
   "next"   : self.VVF7h6     ,
   "last"   : self.VVvT7h      ,
   "cancel"  : self.close
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FF4Pls(self)
  FFtIlI(self)
  FFobAA(self["keyRed"], "#0a333333")
  self["myPiconPic"].instance.setScale(1)
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    self["myPicon%d%d" % (row, col)].instance.setScale(1)
    self["myPiconLbl%d%d" % (row, col)].instance.setNoWrap(True)
  self["myPiconPtr"].hide()
  FFlX3B(self, BF(self.VVRyTc, mode=self.lastMode, words=self.lastWords, asPrefix=self.lastAsPrefix, isFirstTime=True))
 def VVD3bX(self):
  if not self.isBusy:
   VV625J = []
   VV625J.append(("Statistics"           , "VVAHge"    ))
   VV625J.append(VVm77t)
   VV625J.append(("Suggest PIcons for Current Channel"     , "VVBDBH"   ))
   VV625J.append(("Set to Current Channel (copy file)"     , "VVIaAi_file"  ))
   VV625J.append(("Set to Current Channel (as SymLink)"     , "VVIaAi_link"  ))
   VV625J.append(VVm77t)
   VV625J.append(("Export Current File Names List"      , "VVZBYf" ))
   VV625J.append(CCrs3r.VV4E4p())
   VV625J.append(VVm77t)
   movTxt = "Move Unused PIcons to a Directory"
   delTxt = "DELETE Unused PIcons"
   if self.filterTitle == "PIcons without Channels":
    c = VVMmz2
    VV625J.append((c + movTxt           , "VVhfMf"  ))
    VV625J.append((c + delTxt           , "VVvQFJ" ))
   else:
    disTxt = " (Filter >> Unused PIcons)"
    VV625J.append((movTxt + disTxt         ,       ))
    VV625J.append((delTxt + disTxt         ,       ))
   VV625J.append(VVm77t)
   VV625J.append(("Delete Broken PIcons SymLinks (in PIcons Directory)" , "VVaCNa"  ))
   VV625J.append(VVm77t)
   VV625J += CCrs3r.VVY39V()
   VV625J.append(VVm77t)
   VV625J.append(("Keys Help"           , "VVHE2g"    ))
   FFuRfS(self, self.VVI8HV, width=1100, height=1050, title=self.Title, VV625J=VV625J)
 def VVI8HV(self, item=None):
  if item is not None:
   if   item == "VVAHge"     : self.VVAHge()
   elif item == "VVBDBH"    : self.VVBDBH()
   elif item == "VVIaAi_file"   : self.VVIaAi(0)
   elif item == "VVIaAi_link"   : self.VVIaAi(1)
   elif item == "VVZBYf"   : self.VVZBYf()
   elif item == "VVdDzi"   : CCrs3r.VVdDzi(self)
   elif item == "VVhfMf"    : self.VVhfMf()
   elif item == "VVvQFJ"   : self.VVvQFJ()
   elif item == "VVaCNa"   : self.VVaCNa()
   elif item == "VVicWk"   : CCrs3r.VVicWk(self)
   elif item == "findPiconBrokenSymLinks"  : CCrs3r.VVSp16(self, True)
   elif item == "FindAllBrokenSymLinks"  : CCrs3r.VVSp16(self, False)
   elif item == "VVHE2g"      : self.VVHE2g()
 def VV9Ce1(self):
  if not self.isBusy:
   VV625J = []
   VV625J.append(("Go to First PIcon"  , "VVsrhj"  ))
   VV625J.append(("Go to Last PIcon"   , "VVtAXJ"  ))
   VV625J.append(VVm77t)
   VV625J.append(("Sort by Channel Name"     , "sortByChan" ))
   VV625J.append(("Sort by File Name"  , "sortByFile" ))
   VV625J.append(VVm77t)
   VV625J.append(("Find from File List .." , "VVA5cM" ))
   FFuRfS(self, self.VVy5t1, title=self.Title, VV625J=VV625J)
 def VVy5t1(self, item=None):
  if item is not None:
   if   item == "VVsrhj"   : self.VVsrhj()
   elif item == "VVtAXJ"   : self.VVtAXJ()
   elif item == "sortByChan"  : self.VVoR2z(2)
   elif item == "sortByFile"  : self.VVoR2z(0)
   elif item == "VVA5cM"  : self.VVA5cM()
 def VVHE2g(self):
  FF7SvB(self, VVASCC + "_help_picons", "PIcons Tools (Keys Help)")
 def VVmkvi(self):
  if self.curPage == self.curRow == self.curCol == 0:
   self.VVtAXJ()
  else:
   if self.curPage == 0 and self.curRow == 0: self.curCol = 0
   else          : self.curRow -= 1
   self.VVBnvt()
 def VVcuOr(self):
  if self.curPage == self.totalPages - 1 and self.curRow == self.lastRow and self.curCol == self.lastCol:
   self.VVsrhj()
  else:
   if self.curPage == self.totalPages - 1 and self.curRow == self.lastRow:
    self.curCol = self.lastCol
   else:
    self.curRow += 1
   self.VVBnvt()
 def VV8g7c(self):
  if self.curPage == self.curRow == self.curCol == 0:
   self.VVtAXJ()
  else:
   self.curCol -= 1
   self.VVBnvt()
 def VVkPgM(self):
  if self.curPage == self.totalPages - 1 and self.curRow == self.lastRow and self.curCol == self.lastCol:
   self.VVsrhj()
  else:
   self.curCol += 1
   self.VVBnvt()
 def VVvT7h(self):
  if self.curPage == 0:
   self.curRow = 0
   self.curCol = 0
  else:
   self.curPage -= 1
  self.VVBnvt(True)
 def VVF7h6(self):
  if self.curPage == self.totalPages - 1:
   self.curRow = self.lastRow
   self.curCol = self.lastCol
  else:
   self.curPage += 1
  self.VVBnvt(True)
 def VVsrhj(self):
  self.curRow  = 0
  self.curCol  = 0
  self.curPage = 0
  self.VVBnvt(True)
 def VVtAXJ(self):
  self.curPage = self.totalPages -1
  self.curRow  = (self.TOTAL_ROWS - 1)
  self.curCol  = (self.TOTAL_COLS - 1)
  self.VVBnvt(True)
 def VVA5cM(self):
  VV625J = []
  for item in self.VVvytR:
   VV625J.append((item[0], item[0]))
  FFuRfS(self, self.VVZNql, title='PIcons ".png" Files', VV625J=VV625J, VVeYEo=True)
 def VVZNql(self, item=None):
  if item:
   txt, ref, ndx = item
   self.VVzHCh(ndx)
 def VVYuo3(self):
  if not self.isBusy and self["keyRed"].getVisible():
   filName, refCode, chName, sat, inDB = self.VVfbJ8()
   if refCode:
    FFJZ42(self, refCode)
    self.VVS2Ht()
    self.VVEhGj()
 def VVMr9U(self, isUp):
  try:
   if isUp : InfoBar.instance.zapDown()
   else : InfoBar.instance.zapUp()
   self.VVS2Ht()
   self.VVEhGj()
  except:
   pass
 def VVcgQQ(self):
  if self["keyGreen"].getVisible():
   self.VVzHCh(self.curChanIndex)
 def VVzHCh(self, ndx):
  if ndx > -1 and ndx < self.totalPIcons:
   self.curPage = int(ndx / self.PAGE_PICONS)
   firstInPage  = self.curPage * self.PAGE_PICONS
   diff   = ndx - firstInPage
   self.curRow  = int(diff / self.TOTAL_COLS)
   firstInRow  = self.curRow * self.TOTAL_COLS
   diff   = ndx - firstInPage
   self.curCol  = diff - self.curRow * self.TOTAL_COLS
   self.VVBnvt(True)
  else:
   FFD1yO(self, "Not found", 1000)
 def VVoR2z(self, col):
  reverseSort = self.lastSortCol == col
  self.lastSortCol = col
  FFlX3B(self, BF(self.VVRyTc, mode=self.lastMode, words=self.lastWords, asPrefix=self.lastAsPrefix, reverseSort=reverseSort), title="Sorting ...")
 def VVIaAi(self, mode):
  title = "Change Current Channel PIcon"
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  curChF = "%s%s.png" % (self.pPath, refCode.replace(":", "_"))
  if refCode:
   filName, refCode, chName, sat, inDB = self.VVfbJ8()
   selPiconF = "%s%s"  % (self.pPath, filName)
   if not curChF == selPiconF:
    if fileExists(curChF):
     VV625J = []
     VV625J.append(("Overwrite current PIcon"    ,  "overwrite" ))
     VV625J.append(('Rename current PIcon to ".bak.png"' ,  "backup" ))
     FFuRfS(self, BF(self.VVGgIL, mode, curChF, selPiconF), VV625J=VV625J, title="Current Channel PIcon (already exists)")
    else:
     self.VVGgIL(mode, curChF, selPiconF, "overwrite")
   else:
    FFkYsE(self, "Cannot change PIcon to itself !", title=title)
  else:
   FFkYsE(self, "Could not read current channel info. !", title=title)
 def VVGgIL(self, mode, curChF, selPiconF, item=None):
  if item is not None:
   cmd  = ""
   if item == "backup" : cmd += "mv -f '%s' '%s';" % (curChF, curChF + ".bak.png")
   else    : cmd += "rm -f '%s';" % curChF
   if mode == 0: cmd += "cp -f '%s' '%s'" % (selPiconF, curChF)
   else  : cmd += "ln -sf '%s' '%s'" % (selPiconF, curChF)
   os.system(cmd)
   FFlX3B(self, BF(self.VVRyTc, goToFirst=False), title="PIcon Changed.\nRefreshing ...")
 def VVhfMf(self):
  defDir = FF0WrY(CCrs3r.VVsNIk() + "picons_backup")
  os.system(FFxtg8("mkdir '%s'" % (defDir)))
  self.session.openWithCallback(BF(self.VVF9xC, defDir), BF(CC7ujK
         , mode=CC7ujK.VVBUn6, VVKDYx=CCrs3r.VVsNIk()))
 def VVF9xC(self, defDir, path):
  if len(path) > 0:
   title = "Move Unused PIcons"
   if path == CCrs3r.VVsNIk():
    FFkYsE(self, "Cannot move to same directory !", title=title)
   else:
    if not FF0WrY(path) == FF0WrY(defDir):
     self.VVPvhs(defDir)
    FFMIbO(self, BF(FFlX3B, self, BF(self.VV1afN, title, defDir, path), title="Moving Files ..."), "Move %d files to:\n\n%s" % (len(self.VVvytR), path), title=title)
  else:
   self.VVPvhs(defDir)
 def VV1afN(self, title, defDir, toPath):
  if not iMove:
   self.VVPvhs(defDir)
   FFkYsE(self, "Module not found:\n\nshutil", title=title)
   return
  toPath = FF0WrY(toPath)
  pPath = CCrs3r.VVsNIk()
  err  = ""
  totOK = 0
  for fName, fType, chName, sat, inDB in self.VVvytR:
   if fName:
    fName += ".png"
    From = "%s%s" % (pPath, fName)
    try:
     iMove(From, "%s%s" % (toPath, fName))
     totOK +=1
    except Exception as e:
     err  = "\nError while moving the file:\n   %s\n\n" % From
     err += "Error:\n   %s" % str(e)
     break
  txt  = "Files\t: %d\n" % len(self.VVvytR)
  txt += "Moved\t: %d\n" % totOK
  txt += err
  FFNEkd(self, txt, title=title, VVghPi="#22330000" if err else "#22002020")
  if totOK > 0:
   self.VVRMIP("all")
 def VVPvhs(self, defDir):
  try:
   os.rmdir(defDir)
  except:
   pass
 def VVvQFJ(self):
  title = "Delete Unused PIcons"
  tot = len(self.VVvytR)
  FFMIbO(self, BF(FFlX3B, self, BF(self.VVhWMu, title), title="Deleting Files ..."), "Delete %s unused PIcon file%s ?" % (tot, FFICXm(tot)), title=title)
 def VVhWMu(self, title):
  pPath = CCrs3r.VVsNIk()
  totErr = 0
  for fName, fType, chName, sat, inDB in self.VVvytR:
   if fName:
    fName = "%s%s.png" % (pPath, fName)
    try:
     os.remove(fName)
    except:
     totErr += 1
  tot = len(self.VVvytR)
  txt  = "Found\t: %d\n"  % tot
  txt += "Deleted\t: %d\n" % (tot - totErr)
  if totErr:
   txt += "Errors\t: %s" % FFkhYI(str(totErr), VVU8eD)
  FFNEkd(self, txt, title=title)
 def VVaCNa(self):
  lines = FFiGf6("find -L '%s' -type l -print" % self.pPath)
  if lines:
   tot = len(lines)
   FFMIbO(self, BF(self.VV0UHk, lines), "\n".join(lines), title="Delete %d Broken SymLink%s ?" % (tot, FFICXm(tot)), VVUEfx=True)
  else:
   FFewCE(self, "No broken SymLinks in:\n\n%s" % self.pPath)
 def VV0UHk(self, fList):
  os.system(FFxtg8("find -L '%s' -type l -delete" % self.pPath))
  FFewCE(self, "Files deleted:\n\n%s" % "\n".join(fList), title=self.Title)
 def VVaAx7(self):
  FFlX3B(self, self.VVjZ8T)
 def VVjZ8T(self):
  if self.isBusy:
   return
  filName, refCode, chName, sat, inDB = self.VVfbJ8()
  if filName:
   path = self.pPath + filName
   txt  = ""
   txt += FFkhYI("PIcon Directory:\n", VVpHwQ)
   txt += "  Path\t: %s\n"  % self.pPath
   target = FFeNiq(self.pPath)
   if target:
    txt += "  Target\t: %s\n" % target
   txt += "\n"
   target = FFeNiq(path)
   txt += FFkhYI("PIcon File:\n", VVpHwQ)
   if target:
    txt += "  SymLink\t: %s\n"   % filName
    txt += "  Target File\t: %s\n" % (os.path.dirname(target) + "/" + os.path.basename(target))
   else:
    txt += "  File\t: %s\n" % filName
   txt += "\n"
   slLst = []
   if not os.path.islink(path):
    OrigRealPath = os.path.realpath(path)
    for fName in os.listdir(self.pPath):
     fPath = os.path.join(self.pPath, fName)
     if os.path.islink(fPath):
      fRealPath = os.path.realpath(fPath)
      if fRealPath == OrigRealPath:
       slLst.append(fRealPath)
    if slLst:
     tot = len(slLst)
     txt += FFkhYI("Found %d SymLink%s to this file from:\n" % (tot, FFICXm(tot)), VVpHwQ)
     for fPath in slLst:
      txt += "  %s\n" % FFkhYI(fPath, VVkXS4)
     txt += "\n"
   if chName:
    txt += FFkhYI("Channel:\n", VVpHwQ)
    if refCode:
     txt += "  Reference\t: %s\n" % (refCode)
    txt += "  Channel\t: %s\n" % FFkhYI(chName, VV9cEK)
    if sat and not sat == "IPTV":
     txt += "  Satellite\t: %s" % sat
   elif not slLst:
    txt += FFkhYI("Remarks:\n", VVpHwQ)
    txt += "  %s\n" % FFkhYI("Unused", VVU8eD)
  else:
   txt = "No info found"
  FFBatl(self, fncMode=CCARMv.VVLgSX, refCode=refCode, chName=chName, text=txt, picPath=self.pPath + filName)
 def VVfbJ8(self):
  fName = refCode = chName = sat = inDB = ""
  if self.curIndex > -1 and self.curIndex < self.totalPIcons:
   fName, fType, chName, sat, inDB = self.VVvytR[self.curIndex]
   if fName.count("_") > 8 : refCode = fName.replace("_", ":").upper()
   else     : refCode = ""
   fName += ".png"
   sat  = FFsAXk(sat)
  return fName, refCode, chName, sat, inDB
 def VVS2Ht(self):
  self.curChanName = ""
  self.curChanFile = ""
  self.curChanIndex = -1
  self.curChanRefCode = ""
  self.curChanIptvRef = ""
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  if refCode:
   self.curChanRefCode = refCode
   self.curChanName = chName
   self.curChanFile = self.curChanRefCode.rstrip(":").replace(":", "_")
   self.curChanIptvRef = iptvRef
   path = self.pPath + self.curChanFile + ".png"
   self["myPiconF"].hide()
   self["myPiconBG"].hide()
   self["myPiconPic"].hide()
   if fileExists(path):
    try:
     self["myPiconPic"].instance.setPixmapFromFile(path)
     self["myPiconF"].show()
     self["myPiconBG"].show()
     self["myPiconPic"].show()
    except:
     pass
   for ndx, item in enumerate(self.VVvytR):
    if item[0] == self.curChanFile:
     self.curChanIndex = ndx
     break
  if self.curChanIndex > -1 : self["keyGreen"].show()
  else       : self["keyGreen"].hide()
 def VVEhGj(self):
  title = "  " + self.Title
  if self.filterTitle:
   title += "  ..  Filter = " + self.filterTitle
  if len(title) > 65:
   title = title[:65] + ".."
  self["myTitle"].setText(title)
  tabLft = " " * 4
  filName, refCode, chName, sat, inDB = self.VVfbJ8()
  fNum = "Num. : %d / %d" % (self.curIndex + 1, self.totalPIcons)
  page = "Page: %d / %d"  % (self.curPage + 1, self.totalPages)
  self["myPiconInf0"].setText(FFkhYI("%s%s%s%s" % (tabLft, fNum, " " * 12, page), VVpHwQ))
  self["myPiconInf1"].setText("%sFile : %s" % (tabLft, filName))
  self["myPiconInf2"].setText("%sRef. : %s" % (tabLft, self.VVfbJ8()[1]))
  if self.curChanIptvRef : typ = "IPTV"
  else     : typ = "Current Ch."
  self["myPiconInf3"].setText("%s%s : %s" % (tabLft, typ, FFkhYI(self.curChanName, VVdWFT)))
  self["myPiconInf4"].setText("%sFile : %s\n" % (tabLft, (self.curChanFile + ".png")))
  self["myPiconInf5"].setText("%sRef. : %s" % (tabLft, self.curChanRefCode))
 def VVAHge(self):
  VVUDHC, VV1Lo5 = FF92xJ()
  sTypeNameDict = {}
  for key, val in list(VV1Lo5.items()):
   sTypeNameDict[key] = 0
  totUsedFiles = 0
  totUsedLinks = 0
  totSymLinks  = 0
  totInDB   = 0
  totNoRefCode = 0
  totNoSType  = 0
  sTypeDict  = {}
  for fName, fType, chName, sat, inDB in self.VVvytR:
   if chName:
    if fType == 0 : totUsedFiles += 1
    else   : totUsedLinks += 1
   if fType == 1:
    totSymLinks += 1
   if inDB == 1:
    totInDB += 1
   span = iSearch(r"(?:[A-Fa-f0-9]+_){2}([A-Fa-f0-9]+)(?:_[A-Fa-f0-9]+){7}", fName, IGNORECASE)
   if span:
    stNum = int(span.group(1), 16)
    if stNum in VV1Lo5: sTypeDict[VV1Lo5[stNum]] = sTypeDict.get(VV1Lo5[stNum], 0) + 1
    else     : totNoSType += 1
   else:
    totNoRefCode += 1
  totBrokSL = FFj4HH("find -L '%s' -type l -print | wc -l" % self.pPath)
  VVvhuK = []
  c = "#b#11003333#"
  VVvhuK.append((c + "PIcons" , "%d\tUsed = %s" % (self.totalPIcons, totUsedFiles + totUsedLinks)))
  VVvhuK.append((c + "Files" , "%d\tUsed = %s" % (self.totalPIcons - totSymLinks, totUsedFiles)))
  VVvhuK.append((c + "SymLinks" , "%d\tUsed = %s" % (totSymLinks, totUsedLinks)))
  c = "#b#11004040#"
  VVvhuK.append((c + "In Database (lamedb)"  , str(totInDB)))
  VVvhuK.append((c + "Not In Database (lamedb)" , str(self.totalPIcons - totInDB)))
  VVvhuK.append((c + "Satellites"    , str(len(self.nsList))))
  VVvhuK.append((c + "Broken SymLinks"   , str(totBrokSL)))
  if totNoRefCode : VVvhuK.append((c + "File name is not a Reference Code" , str(totNoRefCode)))
  if totNoSType : VVvhuK.append((c + "Unknown Service Type"    , str(totNoSType)))
  s = "Service Type "
  if sTypeDict:
   sTypeRows = []
   for key, val in list(sTypeDict.items()):
    sTypeRows.append(("Service Type (%s)" % key, str(val)))
   sTypeRows.sort(key=lambda x: x[0].lower())
   VVvhuK.extend(sTypeRows)
  FF1dQ4(self, None, title=self.Title, VVvytR=VVvhuK, VVmp7B=28, VV0g1U="#00003333", VVooYw="#00222222")
 def VVZBYf(self):
  if self.filterTitle:
   txt = iSub(r"([^a-zA-Z0-9])", r"_", self.filterTitle, flags=IGNORECASE)
   while "__" in txt: txt = txt.replace("__", "_")
   txt = "FilteredBy_%s_" % txt.strip("_")
  else:
   txt = "All_"
  path = "%sPIconsList_%s%s.txt" % (FF0WrY(CFG.exportedTablesPath.getValue()), txt, FFGuM2())
  with open(path, "w") as f:
   for fName, fType, chName, sat, inDB in self.VVvytR:
    f.write("%s%s.png\n" % (self.pPath, fName))
  FFewCE(self, "List exported to file:\n\n%s" % path, title=self.Title)
 def VV7Bkj(self):
  if not self.isBusy:
   VV625J = []
   VV625J.append(("All"         , "all"   ))
   VV625J.append(VVm77t)
   VV625J.append(("Used by Channels"      , "used"  ))
   VV625J.append(("Unused PIcons"      , "unused"  ))
   VV625J.append(("IPTV PIcons"       , "iptv"  ))
   VV625J.append(VVm77t)
   VV625J.append(("PIcons Files"       , "pFiles"  ))
   VV625J.append(("SymLinks to PIcons"     , "pLinks"  ))
   VV625J.append(("PIcons Files Targeted by SymLinks" , "pTargets" ))
   VV625J.append(("By Files Date ..."     , "pDate"  ))
   VV625J.append(("By Service Type ..."     , "servType" ))
   if self.nsList:
    VV625J.append(FFi9aC("Satellites"))
    satsHex = list(self.nsList)
    satsHex.sort()
    for sHex in satsHex:
     val = int(sHex, 16)
     if val > 0:
      sat = FFUBZ6(val)
      VV625J.append((sat, "__s__" + sHex + "__sat__" + sat))
   filterObj = CCU3qf(self)
   filterObj.VVxv80(VV625J, self.nsList, self.VVlqiB)
 def VVlqiB(self, item=None):
  if item is not None:
   self.VVRMIP(item)
 def VVRMIP(self, item=None):
   if   item == "all"    : mode, words, self.filterTitle = self.VVIcXD   , ""  , ""
   elif item == "used"    : mode, words, self.filterTitle = self.VVsPK2   , ""  , "PIcons with Channels"
   elif item == "unused"   : mode, words, self.filterTitle = self.VVBp7W  , ""  , "PIcons without Channels"
   elif item == "iptv"    : mode, words, self.filterTitle = self.VVf4Re   , "iptv" , "IPTV PIcons"
   elif item == "pFiles"   : mode, words, self.filterTitle = self.VVlZgM  , ""  , "PIcons Files"
   elif item == "pLinks"   : mode, words, self.filterTitle = self.VVDcUS  , ""  , "SymLinks"
   elif item == "pTargets"   : mode, words, self.filterTitle = self.VVnKah  , ""  , "Targets"
   elif item == "pDate"   : mode, words, self.filterTitle = self.VV3Joy , ""  , "Date"
   elif item == "servType"   : mode, words, self.filterTitle = self.VVXNEc , ""  , "Service Type"
   elif item.startswith("__s__") : mode, words, self.filterTitle = self.VV93KM   , item[5:].split("__sat__")[0] , item[5:].split("__sat__")[1]
   elif item.startswith("__w__") : mode, words, self.filterTitle = self.VVlsNO , item[5:] , item[5:]
   else       : return
   asPrefix = self.lastAsPrefix
   if mode == self.VVnKah:
    words = []
    pngFiles = self.pPath + "*.png"
    lines = FFiGf6("find %s -type l | while read -r FILE; do if [ -L \"$FILE\" ] && [ -e \"$FILE\" ]; then ls -l \"$FILE\" 2> /dev/null | awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=$10=\"\";print}' | xargs; fi; done" % pngFiles)
    if lines:
     for f in lines:
      fName = FFqDmh(f)
      if fName.endswith(".png"):
       fName = fName[:-4]
       words.append(fName)
    if not words:
     FFD1yO(self, "Not found", 1000)
     return
   elif mode == self.VV3Joy:
    self.VVppKJ(mode)
    return
   elif mode == self.VVXNEc:
    self.VVioPV(mode)
    return
   elif mode == self.VVdO4v:
    return
   else:
    words, asPrefix = CCU3qf.VVP88C(words)
   if not words and mode in (self.VV93KM, self.VVlsNO):
    FFD1yO(self, "Incorrect filter", 2000)
   elif not self.lastMode == mode or not self.lastWords == words or not self.lastAsPrefix == asPrefix:
    FFlX3B(self, BF(self.VVRyTc, mode=mode, words=words, asPrefix=asPrefix), title="Filtering ...", clearMsg=False)
 def VVppKJ(self, mode):
  VV625J = []
  VV625J.append(("Today"   , "today" ))
  VV625J.append(("Since Yesterday" , "yest" ))
  VV625J.append(("Since 7 days"  , "week" ))
  FFuRfS(self, BF(self.VVHB8j, mode), VV625J=VV625J, title="Filter by Added/Modified Date")
 def VVHB8j(self, mode, item=None):
  if item:
   if   item == "today": stamp, self.filterTitle = FFPPfi(0) , "Today"
   elif item == "yest" : stamp, self.filterTitle = FFPPfi(-1), "Yesterday"
   elif item == "week" : stamp, self.filterTitle = FFPPfi(-7), "Last 7 Days"
   self.filterTitle = "File Date (%s)" % self.filterTitle
   if not self.lastMode == mode or not self.lastTimeStamp == stamp:
    FFlX3B(self, BF(self.VVRyTc, mode=mode, timeStamp=stamp), title="Filtering ...", clearMsg=False)
 def VVioPV(self, mode):
  VVUDHC, VV1Lo5 = FF92xJ()
  lst = set()
  for key, val in list(VV1Lo5.items()):
   lst.add(val)
  VV625J = []
  for item in lst:
   VV625J.append((item, item))
  VV625J.sort(key=lambda x: x[0])
  FFuRfS(self, BF(self.VV6SKx, mode), VV625J=VV625J, title="Filter by Service Type")
 def VV6SKx(self, mode, item=None):
  if item:
   VVUDHC, VV1Lo5 = FF92xJ()
   sTypeList = []
   for key, val in list(VV1Lo5.items()):
    if item == val:
     self.filterTitle = val
     sTypeList.append(("%01x" % key).upper())
   if not self.lastMode == mode or not self.lastSTypeList == sTypeList:
    FFlX3B(self, BF(self.VVRyTc, mode=mode, sTypeList=sTypeList), title="Filtering ...", clearMsg=False)
 def VVBDBH(self):
  self.session.open(CCC6u0, barTheme=CCC6u0.VVw5hO
      , titlePrefix = ""
      , fncToRun  = self.VVW35u
      , VVnFNJ = self.VVDmTw)
 def VVW35u(self, VVC69w):
  VVooHP, err = CCtSdI.VV4uiY(self, CCtSdI.VV3E27, VVwoAs=False, VVDUH8=False)
  files = []
  words = []
  if not VVC69w or VVC69w.isCancelled:
   return
  VVC69w.VV0DcB = []
  VVC69w.VVYqos(len(VVooHP))
  if VVooHP:
   VVAE0x = CCD3Dl()
   curCh = VVAE0x.VVGk9I(self.curChanName)
   for refCode in VVooHP:
    if not VVC69w or VVC69w.isCancelled:
     return
    VVC69w.VVLLRh(1, True)
    chName, sat, inDB = VVooHP.get(refCode, ("", "", 0))
    ratio = CCrs3r.VVwjGd(chName.lower(), curCh)
    if ratio > 50:
     allPath, fName, refCodeFile, pList = CCrs3r.VVMjRL(refCode.replace("_", ":"), self.curChanName)
     if pList:
      for f in pList:
       f = FFqDmh(f)
       VVC69w.VV0DcB.append(f.replace(".png", ""))
 def VVDmTw(self, VVr4Ej, VV0DcB, threadCounter, threadTotal, threadErr):
  if VV0DcB:
   self.timer = eTimer()
   fnc = BF(FFlX3B, self, BF(self.VVRyTc, mode=self.VVdO4v, words=VV0DcB), title="Loading ...")
   try:
    self.timer_conn = self.timer.timeout.connect(fnc)
   except:
    self.timer.callback.append(fnc)
   self.timer.start(50, True)
  else:
   FFD1yO(self, "Not found", 2000)
 def VVRyTc(self, mode=0, words=None, asPrefix=False, reverseSort=False, isFirstTime=False, goToFirst=True, timeStamp=None, sTypeList=None):
  if not self.VV46CQ(isFirstTime):
   return
  self.isBusy = True
  VVDUH8 = True if isFirstTime else False
  VVooHP, err = CCtSdI.VV4uiY(self, CCtSdI.VV3E27, VVwoAs=False, VVDUH8=VVDUH8)
  if err:
   self.close()
  iptvRefList = self.VVYP4O()
  tList = []
  for fName, fType in CCrs3r.VVI7Ry(self.pPath):
   fName = fName[:-4]
   namSp = ""
   if fName.count("_") > 8 and VVooHP:
    if fName in VVooHP:
     chName, sat, inDB = VVooHP.get(fName)
     chName = chName or "?"
     namSp = fName.split("_")[6].zfill(8)[:4]
    elif fName in iptvRefList:
     chName = iptvRefList.get(fName) or "?"
     sat, inDB = "IPTV", 1
    else:
     chName, sat, inDB = "", "", 0
   else:
    chName, sat, inDB = "", "", 0
   entry = (fName, fType, chName, sat, inDB)
   isAdd = False
   if mode == self.VVIcXD:
    if namSp:
     self.nsList.add(namSp)
    isAdd = True
   elif mode == self.VVsPK2  and chName         : isAdd = True
   elif mode == self.VVBp7W and not chName        : isAdd = True
   elif mode == self.VVlZgM  and fType == 0        : isAdd = True
   elif mode == self.VVDcUS  and fType == 1        : isAdd = True
   elif mode == self.VVnKah  and fName in words       : isAdd = True
   elif mode == self.VVdO4v and fName in words       : isAdd = True
   elif mode == self.VVf4Re  and sat.lower() == words[0]     : isAdd = True
   elif mode == self.VV93KM  and namSp.lower() == words[0]    : isAdd = True
   elif mode == self.VVlsNO:
    if asPrefix:
     if any(chName.lower().startswith(x) for x in words)       : isAdd = True
    elif any(x in chName.lower() for x in words)         : isAdd = True
   elif mode == self.VV3Joy:
    try:
     if os.stat("%s%s.png" % (self.pPath, fName)).st_ctime >= timeStamp   : isAdd = True
    except:
     pass
   elif mode == self.VVXNEc:
    span = iSearch(r"(?:[A-Fa-f0-9]+_){2}([A-Fa-f0-9]+)(?:_[A-Fa-f0-9]+){7}", fName, IGNORECASE)
    if span and span.group(1) in sTypeList           : isAdd = True
   if isAdd:
    tList.append(entry)
  if len(tList) > 0:
   self.VVvytR   = list(tList)
   tList    = None
   self.lastMode  = mode
   self.lastWords  = words
   self.lastAsPrefix = asPrefix
   self.lastTimeStamp = timeStamp
   self.lastSTypeList = sTypeList
   FFD1yO(self)
  else:
   self.isBusy = False
   FFD1yO(self, "Not found", 1000)
   return
  self.VVvytR.sort(key=lambda x: x[self.lastSortCol], reverse=reverseSort)
  self.VVS2Ht()
  self.totalPIcons = len(self.VVvytR)
  self.totalPages  = int(self.totalPIcons / self.PAGE_PICONS) + (self.totalPIcons % self.PAGE_PICONS > 0)
  if goToFirst:
   self.curPage = 0
   self.curRow  = 0
   self.curCol  = 0
   self.curIndex = 0
   self.lastRow = 0
   self.lastCol = 0
  self["myPiconPtr"].show()
  self.isBusy = False
  self.VVBnvt(True)
 def VV46CQ(self, isFirstTime):
  if fileExists(self.pPath):
   for fName, fType in CCrs3r.VVI7Ry(self.pPath):
    if fName:
     return True
   if isFirstTime : FFkYsE(self, 'No ".png" files in path:\n\n%s' % self.pPath, title=self.Title)
   else   : FFD1yO(self, "Not found", 1000)
  else:
   FFkYsE(self, "PIcons path not found.\n\n%s" % self.pPath)
  if isFirstTime:
   self.close()
  return False
 def VVYP4O(self):
  VVvhuK = {}
  files  = CCqQHV.VVJ90G()
  if files:
   for path in files:
    txt = FFqD66(path)
    list = iFindall(r"#SERVICE\s+([A-Fa-f0-9]+:0:(?:[A-Fa-f0-9]+[:]){8}).+\n#DESCRIPTION\s+(.+)", txt, IGNORECASE)
    if list:
     for item in list:
      refCode = item[0].upper().replace(":", "_").strip("_")
      VVvhuK[refCode] = item[1]
  return VVvhuK
 def VVBnvt(self, force=False):
  if self.isBusy:
   return
  oldPage = self.curPage
  if self.curCol > self.TOTAL_COLS - 1:
   self.curCol = 0
   self.curRow += 1
  elif self.curCol < 0:
   self.curCol = self.TOTAL_COLS - 1
   self.curRow -= 1
  if self.curRow > self.TOTAL_ROWS - 1:
   self.curRow = 0
   self.curPage += 1
  elif self.curRow < 0:
   self.curRow = self.TOTAL_ROWS - 1
   self.curPage -= 1
  VVkrUD = self.totalPages -1
  if   self.curPage < 0  : self.curPage = 0
  elif self.curPage > VVkrUD: self.curPage = VVkrUD
  if self.curRow > self.TOTAL_ROWS - 1: self.curRow = self.TOTAL_ROWS - 1
  if self.curCol < 0     : self.curCol = 0
  if force or not oldPage == self.curPage:
   self.VV7kU6()
  if self.curPage == VVkrUD:
   if self.curRow > self.lastRow:
    self.curRow = self.lastRow
   if self.curRow == self.lastRow and self.curCol > self.lastCol:
    self.curCol = self.lastCol
  gap = int(self.skinParam["marginLeft"] / 2)
  pos = self["myPicon%d%d" % (self.curRow, self.curCol)].getPosition()
  self["myPiconPtr"].instance.move(ePoint(pos[0]-gap, pos[1]-gap))
  self.curIndex = self.curPage * self.PAGE_PICONS + self.curRow * self.TOTAL_COLS + self.curCol
  self.VVEhGj()
  filName, refCode, chName, sat, inDB = self.VVfbJ8()
  if inDB and not sat == "IPTV" : self["keyRed"].show()
  else       : self["keyRed"].hide()
 def VV7kU6(self):
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    self["myPicon%d%d" % (row, col)].hide()
    self["myPiconLbl%d%d" % (row, col)].hide()
  last = self.totalPIcons
  f1 = self.curPage * self.PAGE_PICONS
  f2 = f1 + self.PAGE_PICONS
  if f1 > last: f1 = last
  if f2 > last: f2 = last
  row = col = 0
  for ndx in range(f1, f2):
   fName, fType, chName, sat, inDB = self.VVvytR[ndx]
   fName = self.VVvytR[ndx][0]
   path  = self.pPath + fName + ".png"
   refCode  = fName.replace("_", ":").upper()
   pic = self["myPicon%d%d" % (row, col)]
   lbl = self["myPiconLbl%d%d" % (row, col)]
   lbl.show()
   try:
    pic.instance.setPixmapFromFile(path)
    pic.show()
    if inDB : lbl.setText(FFkhYI(chName, VV9cEK))
    else : lbl.setText("-")
   except:
    lbl.setText(FFkhYI(chName, VVyFMl))
   self.lastRow = row
   self.lastCol = col
   col += 1
   if col > (self.TOTAL_COLS - 1):
    col = 0
    row += 1
 @staticmethod
 def VVwjGd(s1, s2):
  rows, cols, dist = len(s1) + 1, len(s2) + 1, []
  for i in range(rows): dist.append([0.] * cols)
  for i in range(1, rows):
   for j in range(1,cols): dist[i][0], dist[0][j] = i, j
  for col in range(1, cols):
   for row in range(1, rows):
    cost = 0 if s1[row-1] == s2[col-1] else 2
    dist[row][col] = min(dist[row-1][col] + 1, dist[row][col-1] + 1, dist[row-1][col-1] + cost)
  return int( ( ( len(s1) + len(s2) ) - dist[row][col] ) / ( len(s1) + len(s2) ) * 100 )
 @staticmethod
 def VV4E4p():
  return ("Copy Current Channel PIcon (to PIcons Export Path)" , "VVdDzi"   )
 @staticmethod
 def VVY39V():
  VV625J = []
  VV625J.append(("Find SymLinks (to PIcon Directory)"   , "VVicWk"   ))
  VV625J.append(("Find Broken SymLinks (to PIcon Directory)" , "findPiconBrokenSymLinks"  ))
  VV625J.append(("Find all Broken SymLinks"      , "FindAllBrokenSymLinks"  ))
  return VV625J
 @staticmethod
 def VVdDzi(SELF):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF)
  png, path = CCrs3r.VVByZr(refCode)
  if path : CCrs3r.VVNsL7(SELF, png, path)
  else : FFkYsE(SELF, "No PIcon found for current channel in:\n\n%s" % CCrs3r.VVsNIk())
 @staticmethod
 def VVicWk(SELF):
  if VVdWFT:
   sed1 = FF95sl("->", VVdWFT)
   sed2 = FF95sl("picon", VVU8eD)
   sed3 = "| sed 's/... Broken Link/\\t\\%s&\%s/gI'" % (VVyFMl, VVZgqQ)
  else:
   sed1 = sed2 = sed3 = ""
  grep = "| grep -i 'picon'"
  FFCa80(SELF, "find / %s -type l %s | while read -r FILE; do if [ -L \"$FILE\" ] && [ ! -e \"$FILE\" ]; then BROK='... Broken Link'; else BROK=''; fi; ls -l \"$FILE\" 2> /dev/null | sed \"s/$/${BROK}/\" | awk '{$1=$2=$3=$4=$5=$6=$7=$8=\"\";print}' | xargs; done %s %s %s" % (FFlfqZ(), grep, sed1, sed2, sed3))
 @staticmethod
 def VVSp16(SELF, isPIcon):
  sed1 = FF95sl("->", VVyFMl)
  if isPIcon:
   grep = "| grep -i 'picon'"
   sed2 = FF95sl("picon", VVU8eD)
  else:
   grep = "| grep -v /proc | grep -v /run | grep -v /etc/rcS.d"
   sed2 = ""
  FFCa80(SELF, "find / %s -type l %s | while read -r FILE; do if [ -L \"$FILE\" ] && [ ! -e \"$FILE\" ]; then ls -l \"$FILE\" 2> /dev/null | awk '{$1=$2=$3=$4=$5=$6=$7=$8=\"\";print}' | xargs; fi; done %s %s" % (FFlfqZ(), grep, sed1, sed2))
 @staticmethod
 def VVI7Ry(path):
  for f in os.listdir(path):
   if f.endswith(".png"):
    p = path + f
    if os.path.islink(p) and os.path.exists(p) : yield f , 1
    elif os.path.isfile(p)      : yield f , 0
 @staticmethod
 def VVsNIk():
  path = CFG.PIconsPath.getValue()
  return FF0WrY(path)
 @staticmethod
 def VVByZr(refCode, chName=None):
  if FFuZb6(refCode):
   refCode, decodedUrl, origUrl, iptvRef = FFMoxZ(refCode)
  allPath, fName, refCodeFile, pList = CCrs3r.VVMjRL(refCode, chName)
  if pList:
   if refCodeFile : return fName, refCodeFile
   else   : return fName, pList[0]
  else:
   return None, None
 @staticmethod
 def VVNsL7(SELF, png, path):
  dest = CFG.exportedPIconsPath.getValue()
  andTxt = "echo -e 'PIcon file copied to:\n\n%s%s' %s" % (dest, png, FF95sl("%s%s" % (dest, png), VV9cEK))
  errTxt = "Could not copy PIcon file!"
  orTxt = "echo -e '%s' %s" % (errTxt, FF95sl(errTxt, VVzZva))
  cmd = "cp -f '%s' '%s' &> /dev/null && %s || %s" % (path, dest, andTxt, orTxt)
  FFuCjo(SELF, cmd)
 @staticmethod
 def VVMjRL(refCode, chName=None):
  allPath = fName = refCodeFile = pList = None
  if refCode.count(":") > 8:
   refCode = refCode.rstrip(":")
   fName = refCode.strip()
   if fName.endswith(":"):
    fName = fName[:-1]
   fName = refCode.replace(":", "_") + ".png"
   allPath = CCrs3r.VVsNIk()
   pList = []
   pat = allPath + "*_" + "_".join(fName.split("_")[3:])
   lst = iGlob(pat)
   if lst:
    pList += lst
   if chName:
    chName = FFO8d5(chName)
    try:
     lst = iGlob(allPath + chName + ".png")
     if lst:
      pList += lst
    except:
     pass
   refCodeFile = ""
   if pList:
    for item in pList:
     if fName == FFqDmh(item):
      refCodeFile = item
    pList.sort()
  return allPath, fName, refCodeFile, pList
class CCg0pW():
 def __init__(self):
  noService = "Service unavailable"
  self.type   = type
  self.VVJYSZ  = None
  self.VVV8V4 = ""
  self.VVLvRX  = noService
  self.VVpTRb = 0
  self.VVK96V  = noService
  self.VVl0J1 = 0
  self.VVFCbn  = "-"
  self.VVs6M9 = 0
  self.VVj7uV  = ""
  self.serviceName = ""
  self.infoAvailable = False
 def VVeSwA(self, service):
  if service:
   self.infoAvailable = False
   feinfo = service.frontendInfo()
   if feinfo:
    self.infoAvailable = True
    frontEndStatus = feinfo.getFrontendStatus()
    if frontEndStatus:
     self.VVJYSZ = frontEndStatus
     self.VVPFwa()
   info = service.info()
   if info:
    self.serviceName = info.getName()
 def VVPFwa(self):
  if self.VVJYSZ:
   val = self.VVJYSZ.get("tuner_signal_quality_db", 0x12345678)
   if val is not None and val != 0x12345678: self.VVV8V4 = "%3.02f dB" % (val / 100.0)
   else         : self.VVV8V4 = ""
   val = self.VVJYSZ.get("tuner_signal_quality", 0) * 100 / 65536
   self.VVpTRb = int(val)
   self.VVLvRX  = "%d%%" % val
   val = self.VVJYSZ.get("tuner_signal_power" , 0) * 100 / 65536
   self.VVl0J1 = int(val)
   self.VVK96V  = "%d%%" % val
   val = self.VVJYSZ.get("tuner_bit_error_rate", 0)
   if not val:
    val = 0
   self.VVFCbn  = "%d" % val
   val = int(val * 100 / 500)
   self.VVs6M9 = min(500, val)
   val = self.VVJYSZ.get("tuner_locked", 0)
   if val == 1 : self.VVj7uV = "Locked"
   else  : self.VVj7uV = "Not locked"
 def VVxRg1(self)   : return self.VVV8V4
 def VVqy66(self)   : return self.VVLvRX
 def VVMvRl(self)  : return self.VVpTRb
 def VVnIAQ(self)   : return self.VVK96V
 def VVqaqs(self)  : return self.VVl0J1
 def VVIpSi(self)   : return self.VVFCbn
 def VVFe1d(self)  : return self.VVs6M9
 def VVnWKM(self)   : return self.VVj7uV
 def VVbdgJ(self) : return self.serviceName
class CCX8JT():
 def __init__(self):
  self.sat1 = self.sat2 = self.freq = self.sr = self.syst = self.inv = self.pol = self.fec    = ""
  self.mod = self.rolof = self.pil = self.plsMod = self.plsCod = self.iStId = self.t2PlId = self.t2PId = ""
  self.data  = None
  self.namespace = ""
  self.txMedia = ""
  self.D_POL  = {0:"Horizontal" , 1:"Vartical" , 2:"Left" , 3:"Right"}
  self.D_SYS_S = {0:"DVB-S", 1:"DVB-S2"}
  self.D_SYS_T = {0:"DVB-T", 1:"DVB-T2"}
  self.D_SYS_C = {0:"DVB-C", 1:"DVB-C2", 2:"DVB-C3", 3:"ATSC"}
  self.D_PIL_INV = {0:"Off" , 1:"On" , 2:"Auto"}
  self.D_PLS_MOD = {0:"Root" , 1:"Gold" , 2:"Combo" , 3:"Unknown"}
  self.D_ROLOF = {0:"35%" , 1:"25%" , 2:"20%" , 3:"Auto"}
  self.D_MOD  = {0:"Auto" , 1:"QPSK" , 2:"8PSK" , 3:"QAM16" , 4:"16APSK", 5:"32APSK"}
  self.D_FEC  = {0:"Auto" , 1:"1/2" , 2:"2/3" , 3:"3/4" , 4:"5/6" , 5:"7/8", 6:"8/9", 7:"3/5", 8:"4/5", 9:"9/10", 10:"6/7", 15:"None"}
  self.FREQ  = "frequency"
  self.SR   = "symbol_rate"
  self.POL  = "polarization"
  self.FEC  = "fec_inner"
  self.ORPOS  = "orbital_position"
  self.SYST  = "system"
  self.INV  = "inversion"
 def VVthez(self, refCode):
  self.data = None
  if refCode:
   self.namespace = FFwYmz(refCode)
   if   self.namespace.startswith("EEEE") : self.txMedia, syst = "DVB-T", self.D_SYS_T
   elif self.namespace.startswith("FFFF") : self.txMedia, syst = "DVB-C", self.D_SYS_C
   else         : self.txMedia, syst = "DVB-S", self.D_SYS_S
   servRef = eServiceReference(refCode)
   if servRef:
    info = eServiceCenter.getInstance().info(servRef)
    if info:
     self.data = info.getInfoObject(servRef, iServiceInformation.sTransponderData)
     if self.data:
      self.sat1  = self.VVoI3n(self.ORPOS  , mod=1   )
      self.sat2  = self.VVoI3n(self.ORPOS  , mod=2   )
      self.freq  = self.VVoI3n(self.FREQ  , mod=3   )
      self.sr   = self.VVoI3n(self.SR   , mod=4   )
      self.inv  = self.VVoI3n(self.INV  , self.D_PIL_INV)
      self.pol  = self.VVoI3n(self.POL  , self.D_POL )
      self.fec  = self.VVoI3n(self.FEC  , self.D_FEC )
      self.syst  = self.VVoI3n(self.SYST  , syst   )
      if "S2" in self.syst:
       self.mod = self.VVoI3n("modulation" , self.D_MOD )
       self.rolof = self.VVoI3n("rolloff"  , self.D_ROLOF )
       self.pil = self.VVoI3n("pilot"   , self.D_PIL_INV)
       self.plsMod = self.VVoI3n("pls_mode"  , self.D_PLS_MOD)
       self.plsCod = self.VVoI3n("pls_code"  )
       self.iStId = self.VVoI3n("is_id"   )
       self.t2PlId = self.VVoI3n("t2mi_plp_id" )
       self.t2PId = self.VVoI3n("t2mi_pid"  )
 def VVoI3n(self, key, valDict=None, mod=0):
  val = self.data.get(key, "?")
  if   val in ("?", -1) : return ""
  elif valDict   : return valDict.get(val, str(val))
  elif mod == 1   : return FFUBZ6(val)
  elif mod == 2   : return FFkxbC(val)
  elif mod == 3   : return str(int(val) // 1000)
  elif mod == 4   : return str(int(val) // 1000)
  else     : return str(val)
 def VVfPTk(self, refCode):
  txt = ""
  self.VVthez(refCode)
  if self.data:
   def VVQQs4(subj, val):
    if val : return "%s\t: %s\n" % (subj, val)
    else : return ""
   if self.txMedia == "DVB-S":
    txt += VVQQs4("System"   , self.syst)
    txt += VVQQs4("Satellite"  , self.sat2)
    txt += VVQQs4("Frequency"  , self.freq)
    txt += VVQQs4("Inversion"  , self.inv)
    txt += VVQQs4("Symbol Rate"  , self.sr)
    txt += VVQQs4("Polarization" , self.pol)
    txt += VVQQs4("FEC"    , self.fec)
    if "S2" in self.syst:
     txt += VVQQs4("Modulation" , self.mod)
     txt += VVQQs4("Roll-Off" , self.rolof)
     txt += VVQQs4("Pilot"  , self.pil)
     txt += VVQQs4("Input Stream", self.iStId)
     txt += VVQQs4("T2MI PLP ID" , self.t2PlId)
     txt += VVQQs4("T2MI PID" , self.t2PId)
     txt += VVQQs4("PLS Mode" , self.plsMod)
     txt += VVQQs4("PLS Code" , self.plsCod)
   else:
    txt += VVQQs4("System"   , self.txMedia)
    txt += VVQQs4("Frequency"  , self.freq)
  return txt, self.namespace
 def VVQuAW(self, refCode):
  txt = "Transpoder : ?"
  self.VVthez(refCode)
  tpTxt = "?"
  if self.data:
   maxLen = 50 + 10
   if self.txMedia == "DVB-S":
    tpTxt = ("%s %s %s %s" % (self.freq, self.pol[:1], self.fec, self.sr)).strip()
   else:
    tpTxt = "Freq = %s  (%s)" % (self.freq, self.txMedia)
   if len(tpTxt) > maxLen : txt = tpTxt[:maxLen] + ".."
   else     : txt = tpTxt
  return tpTxt, self.sat2
 def VVZtm9(self, refCode):
  if refCode and refCode.count(":") > 8: servRef = eServiceReference(refCode)
  else         : servRef = None
  self.data = None
  if servRef:
   info = eServiceCenter.getInstance().info(servRef)
   if info:
    self.data = info.getInfoObject(servRef, iServiceInformation.sTransponderData)
    if self.data:
     self.namespace = FFwYmz(refCode)
     if   self.namespace.startswith("EEEE") : isSat, syst = False, self.VVoI3n(self.SYST, self.D_SYS_T)
     elif self.namespace.startswith("FFFF") : isSat, syst = False, self.VVoI3n(self.SYST, self.D_SYS_C)
     else         : isSat, syst = True , self.VVoI3n(self.SYST, self.D_SYS_S)
     freq = self.VVoI3n(self.FREQ , mod=3  )
     if isSat:
      pol = self.VVoI3n(self.POL , self.D_POL)
      fec = self.VVoI3n(self.FEC , self.D_FEC)
      sr = self.VVoI3n(self.SR  , mod=4  )
      return freq, pol[:1], fec, sr, syst
     else:
      return freq, "-", "-", "-", syst
  return "-", "-", "-", "-", ""
 def VVrs7D(self, refCode):
  self.data = None
  self.VVthez(refCode)
  if self.data and self.freq : return True
  else      : return False
class CCYE8p():
 def __init__(self, VVcrU7, path, VVnFNJ=None, curRowNum=-1):
  self.VVcrU7  = VVcrU7
  self.origFile   = path
  self.Title    = "File Editor: " + FFqDmh(path)
  self.VVnFNJ  = VVnFNJ
  self.tmpFile   = "/tmp/ajpanel_edit"
  self.fileChanged  = False
  self.fileSaved   = False
  self.insertMode   = 0
  self.lastLineNum  = -1
  response = os.system(FFxtg8("cp -f '%s' '%s'" % (self.origFile, self.tmpFile)))
  if response == 0:
   self.VV3K4t(curRowNum)
  else:
   FFkYsE(self.VVcrU7, "Error while preparing edit!")
 def VV3K4t(self, curRowNum):
  VVvhuK = self.VVhZwJ()
  VV3th8 = ("Save Changes" , self.VV5dJz   , [])
  VVVHmY  = ("Edit Line"  , self.VVTHMz    , [])
  VVOtSO = ("Go to Line Num" , self.VVvd1u   , [])
  VV1QO7 = ("Line Options" , self.VV15K5   , [])
  VVKx4L = (""    , self.VVPz1n , [])
  VVfPgM = self.VVEmF4
  VVWlvi  = self.VVRHvn
  header   = ("Line No." , "Text" )
  widths   = (8   , 92  )
  VVQqg2  = (CENTER  , LEFT  )
  VVcpnp = FF1dQ4(self.VVcrU7, None, title=self.Title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VV3th8=VV3th8, VVVHmY=VVVHmY, VVOtSO=VVOtSO, VV1QO7=VV1QO7, VVfPgM=VVfPgM, VVWlvi=VVWlvi, VVKx4L=VVKx4L, VVKNen=True, searchCol=1, lastFindConfigObj=CFG.lastFindEditor
    , VVz2kc   = "#11001111"
    , VVwpZm   = "#11001111"
    , VVghPi   = "#11001111"
    , VV0g1U  = "#05333333"
    , VVooYw  = "#00222222"
    , VVPVU2  = "#11331133"
    )
  VVcpnp.VVtpKN(curRowNum)
 def VVvd1u(self, VVcpnp, title, txt, colList):
  totRows = VVcpnp.VVI1WG()
  lineNum = VVcpnp.VVgrGB() + 1 if self.lastLineNum == -1 else self.lastLineNum
  FFbRXK(self.VVcrU7, BF(self.VVacEl, VVcpnp, lineNum, totRows), title="Go to Line Num (1 - %d)" % totRows, defaultText="%d" % lineNum, message="Enter Line Number")
 def VVacEl(self, VVcpnp, lineNum, totRows, VVVomg):
  if VVVomg:
   VVVomg = VVVomg.strip()
   if VVVomg.isdigit():
    num = FF2DVg(int(VVVomg) - 1, 0, totRows)
    VVcpnp.VVtpKN(num)
    self.lastLineNum = num + 1
   else:
    FFD1yO(VVcpnp, "Incorrect number", 1500)
 def VV15K5(self, VVcpnp, title, txt, colList):
  lineNum = int(colList[0])
  totRows = VVcpnp.VVHLLY()
  VV625J = []
  VV625J.append(  ("Insert Empty Line (before line-%d)" % lineNum , "insertLineBefore" ))
  if lineNum == totRows:
   VV625J.append( ("Insert Empty Line (after line-%d)"  % lineNum , "VVuymn"  ))
  VV625J.append(VVm77t)
  VV625J.append(  ("Copy to clipboard"       , "copyToClipboard"  ))
  if VVDZkF:
   VV625J.append( ("Paste from clipboard (overwrite)"    , "pasteFromClipboard" ))
  VV625J.append(VVm77t)
  VV625J.append(  ("Delete Line"         , "deleteLine"   ))
  FFuRfS(self.VVcrU7, BF(self.VVRN6D, VVcpnp, lineNum), VV625J=VV625J, title="Line Options")
 def VVRN6D(self, VVcpnp, lineNum, item=None):
  if item:
   if   item == "insertLineBefore"  : self.VVxGgq("sed -i '%d i %s' '%s'" % (lineNum, "", self.tmpFile), VVcpnp)
   elif item == "VVuymn"  : self.VVuymn(VVcpnp, lineNum)
   elif item == "copyToClipboard"  : self.VVGaGR(VVcpnp, lineNum)
   elif item == "pasteFromClipboard" : self.VV9NPW(VVcpnp, lineNum)
   elif item == "deleteLine"   : self.VVxGgq("sed -i '%dd' '%s'" % (lineNum, self.tmpFile), VVcpnp)
 def VVRHvn(self, VVcpnp):
  VVcpnp.VV0vgr()
 def VVPz1n(self, VVcpnp, title, txt, colList):
  if   self.insertMode == 1: VVcpnp.VVabBl()
  elif self.insertMode == 2: VVcpnp.VVIdSv()
  self.insertMode = 0
 def VVuymn(self, VVcpnp, lineNum):
  if lineNum == VVcpnp.VVHLLY():
   self.insertMode = 1
   self.VVxGgq("echo '' >> '%s'" % self.tmpFile, VVcpnp)
  else:
   self.insertMode = 2
   self.VVxGgq("sed -i '%d i %s' '%s'" % (lineNum + 1, "", self.tmpFile), VVcpnp)
 def VVGaGR(self, VVcpnp, lineNum):
  global VVDZkF
  VVDZkF = FFj4HH("sed '%sq;d' '%s'" % (lineNum, self.tmpFile) )
  VVcpnp.VVIX8q("Copied to clipboard")
 def VV5dJz(self, VVcpnp, title, txt, colList):
  if self.fileChanged:
   backupOK = os.system(FFxtg8("cp -f '%s' '%s'" % (self.origFile, self.origFile + ".bak")))
   if backupOK == 0:
    finalOK = os.system(FFxtg8("cp -f '%s' '%s'" % (self.tmpFile, self.origFile)))
    if finalOK == 0:
     VVcpnp.VVIX8q("Saved")
     self.fileSaved   = True
     self.fileChanged = False
     VVcpnp.VV0vgr()
    else:
     FFkYsE(self.VVcrU7, "Cannot save file!")
   else:
    FFkYsE(self.VVcrU7, "Cannot create backup copy of original file!")
 def VVEmF4(self, VVcpnp):
  if self.fileChanged:
   FFMIbO(self.VVcrU7, BF(self.VVNAHL, VVcpnp), "Cancel changes ?")
  else:
   finalOK = os.system(FFxtg8("cp -f '%s' '%s'" % (self.tmpFile, self.origFile)))
   self.VVNAHL(VVcpnp)
 def VVNAHL(self, VVcpnp):
  VVcpnp.cancel()
  FFX92w(self.tmpFile)
  if self.VVnFNJ:
   self.VVnFNJ(self.fileSaved)
 def VVTHMz(self, VVcpnp, title, txt, colList):
  lineNum = int(colList[0])
  lineTxt = colList[1]
  message = VVZgqQ + "ORIGINAL TEXT:\n" + VVkXS4 + lineTxt
  FFbRXK(self.VVcrU7, BF(self.VVeH7B, lineNum, VVcpnp), title="File Line", defaultText=lineTxt, message=message)
 def VVeH7B(self, lineNum, VVcpnp, VVVomg):
  if not VVVomg is None:
   if VVcpnp.VVHLLY() <= 1:
    self.VVxGgq("echo %s > '%s'" % (VVVomg, self.tmpFile), VVcpnp)
   else:
    self.VV51JF(VVcpnp, lineNum, VVVomg)
 def VV9NPW(self, VVcpnp, lineNum):
  if lineNum == VVcpnp.VVHLLY() and VVcpnp.VVHLLY() == 1:
   self.VVxGgq("echo %s >> '%s'" % (VVDZkF, self.tmpFile), VVcpnp)
  else:
   self.VV51JF(VVcpnp, lineNum, VVDZkF)
 def VV51JF(self, VVcpnp, lineNum, newTxt):
  VVcpnp.VVphEN("Saving ...")
  lines = FFjdnJ(self.tmpFile)
  with open(self.tmpFile, "w") as f:
   for ndx, line in enumerate(lines, start=1):
    if lineNum == ndx:
     line = newTxt
    f.write(line + "\n")
  self.fileChanged = True
  VVcpnp.VV7TEw()
  VVvhuK = self.VVhZwJ()
  VVcpnp.VVuVux(VVvhuK)
 def VVxGgq(self, cmd, VVcpnp):
  tCons = CChHJE()
  tCons.ePopen(cmd, BF(self.VVLhQ3, VVcpnp))
  self.fileChanged = True
  VVcpnp.VV7TEw()
 def VVLhQ3(self, VVcpnp, result, retval):
  VVvhuK = self.VVhZwJ()
  VVcpnp.VVuVux(VVvhuK)
 def VVhZwJ(self):
  if fileExists(self.tmpFile):
   lines = FFjdnJ(self.tmpFile)
   VVvhuK = []
   if lines:
    for ndx, line in enumerate(lines, start=1):
     VVvhuK.append((str(ndx), line.strip()))
   if not VVvhuK:
    VVvhuK.append((str(1), ""))
   return VVvhuK
  else:
   FFAVqd(self.VVcrU7, self.tmpFile)
class CCU3qf():
 def __init__(self, callingSELF, VVz2kc="#22003344", VVwpZm="#22002233"):
  self.callingSELF = callingSELF
  self.VV625J  = []
  self.satList  = []
  self.VVz2kc  = VVz2kc
  self.VVwpZm   = VVwpZm
 def VVmiWt(self, VVnFNJ):
  self.VV625J = []
  VV625J, VVDMeF = CCU3qf.VVcpV6(self.callingSELF, False, True)
  if VV625J:
   self.VV625J += VV625J
   self.VVemmd(VVnFNJ, VVDMeF)
 def VVBVkh(self, mode, VVcpnp, satCol, VVnFNJ, inFilterFnc=None):
  VVcpnp.VVphEN("Loading Filters ...")
  self.VV625J = []
  self.VV625J.append(("All Services" , "all"))
  if mode == 1:
   self.VV625J.append(VVm77t)
   self.VV625J.append(("Parental Control", "parentalControl"))
   self.VV625J.append(("Hidden Services" , "hiddenServices"))
  elif mode == 2:
   self.VV625J.append(VVm77t)
   self.VV625J.append(("Selected Transponder"   , "selectedTP" ))
   self.VV625J.append(("Channels with no Transponder" , "emptyTP"  ))
  self.VVMwjP(VVcpnp, satCol)
  VV625J, VVDMeF = CCU3qf.VVcpV6(self.callingSELF, True, False)
  if VV625J:
   VV625J.insert(0, FFi9aC("Custom Words"))
   self.VV625J += VV625J
  VVcpnp.VVhzNf()
  self.VVemmd(VVnFNJ, VVDMeF, inFilterFnc)
 def VVxv80(self, VV625J, sats, VVnFNJ, inFilterFnc=None):
  self.VV625J = VV625J
  VV625J, VVDMeF = CCU3qf.VVcpV6(self.callingSELF, True, False)
  if VV625J:
   self.VV625J.append(FFi9aC("Custom Words"))
   self.VV625J += VV625J
  self.VVemmd(VVnFNJ, VVDMeF, inFilterFnc)
 def VVemmd(self, VVnFNJ, VVDMeF, inFilterFnc=None):
  VVmKbI  = ("Filter in Filter", inFilterFnc) if inFilterFnc else None
  VVJ5GS = ("Edit Filter"  , BF(self.VVq24M, VVDMeF))
  VVme6L  = ("Filter Help"  , BF(self.VV42Xy, VVDMeF))
  FFuRfS(self.callingSELF, BF(self.VVr7oV, VVnFNJ), VV625J=self.VV625J, title="Select Filter", VVmKbI=VVmKbI, VVJ5GS=VVJ5GS, VVme6L=VVme6L, VVvQ6U=True, VVz2kc=self.VVz2kc, VVwpZm=self.VVwpZm)
 def VVr7oV(self, VVnFNJ, item):
  if item:
   VVnFNJ(item)
 def VVq24M(self, VVDMeF, VVp2lZObj, sel):
  if fileExists(VVDMeF) : CCYE8p(self.callingSELF, VVDMeF, VVnFNJ=None)
  else       : FFAVqd(self.callingSELF, VVDMeF)
  VVp2lZObj.cancel()
 def VV42Xy(self, VVDMeF, VVp2lZObj, sel):
  FF7SvB(self.callingSELF, VVASCC + "_help_service_filter", "Service Filter")
 def VVMwjP(self, VVcpnp, satColNum):
  if not self.satList:
   satList = VVcpnp.VV6T0n(satColNum)
   if satList:
    satList = set(satList)
    satList = list(satList)
    if satList:
     sats = []
     for ndx, sat in enumerate(satList):
      if not sat.strip() == "":
       self.satList.append((FFsAXk(sat), "__s__" + sat))
     self.satList.sort(key=lambda x: x[0])
     self.satList.insert(0, FFi9aC("Satellites"))
  if self.VV625J:
   self.VV625J += self.satList
 @staticmethod
 def VVcpV6(SELF, addTag, VVl2X5):
  FFWcGD()
  fileName  = "ajpanel_services_filter"
  VVDMeF = VVCnD5 + fileName
  VV625J  = []
  if not fileExists(VVDMeF):
   os.system(FFxtg8("cp -f '%s' '%s'" % (VVASCC + fileName, VVDMeF)))
  fileFound = False
  if fileExists(VVDMeF):
   fileFound = True
   lines = FFjdnJ(VVDMeF)
   if lines:
    for line in lines:
     line = line.strip()
     if line and not line.startswith("#"):
      if "#" in line:
       line = line.split("#")[0].strip()
      if "," in line:
       lst = list(map(str.strip, line.split(",")))
       lst = list([_f for _f in lst if _f])
       if lst: line = ",".join(lst)
       else  : line = ""
      if line:
       if addTag: VV625J.append((line, "__w__" + line))
       else  : VV625J.append((line, line))
  if VVl2X5:
   if   not fileFound : FFAVqd(SELF, VVDMeF)
   elif not VV625J : FFzfYN(SELF, VVDMeF)
  return VV625J, VVDMeF
 @staticmethod
 def VVP88C(txt):
  txt = txt.strip()
  lst = []
  prefix = False
  if "," in txt:
   lst = list(map(str.strip, txt.split(",")))
   lst = list([_f for _f in lst if _f])
   if lst and len(lst) > 1 and lst[0] == "^":
    lst = lst[1:]
    prefix = True
  else:
   txt = txt.strip()
   if txt:
    if len(txt) > 1 and txt.startswith("^"):
     txt = txt[1:]
     prefix = True
    lst = [txt]
  return tuple(map(str.lower, lst)), prefix
class CCqgU8():
 def __init__(self, callingSELF, VVcpnp, addSep=True):
  self.callingSELF = callingSELF
  self.VVcpnp = VVcpnp
  self.VV625J = []
  iMulSel = self.VVcpnp.VVAzsT()
  if iMulSel : self.VV625J.append( ("Disable Multi-Select " , "MultSelDisab" ))
  else  : self.VV625J.append( ("Enable Multi-Select"  , "multSelEnab"  ))
  tot = self.VVcpnp.VVMJsS()
  self.VV625J.append(    ("Select all"    , "selectAll"  ))
  if iMulSel and tot > 0:
   self.VV625J.append(   ("Unselect all"    , "unselectAll"  ))
  if addSep:
   self.VV625J.append(VVm77t)
 def VVMNiz(self, extraMenu, cbFncDict):
  if extraMenu:
   self.VV625J.extend(extraMenu)
  FFuRfS(self.callingSELF, BF(self.VVFLtg, cbFncDict), title="Options", VV625J=self.VV625J)
 def VVFLtg(self, cbFncDict, item=None):
  if item:
   if   item == "multSelEnab" : self.VVcpnp.VVBOaN(True)
   elif item == "MultSelDisab" : self.VVcpnp.VVBOaN(False)
   elif item == "selectAll" : self.VVcpnp.VV1gPk()
   elif item == "unselectAll" : self.VVcpnp.VVNp4C()
   elif cbFncDict:
    fnc = cbFncDict.get(item)
    if fnc:
     fnc()
class CCcG5l(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVSzFu, 900, 480, 50, 0, 0, "#22660066", "#22330033", 35, barHeight=40)
  self.session  = session
  FFJd2Z(self)
  FFHhgX(self["keyRed"]  , "Exit")
  FFHhgX(self["keyGreen"]  , "Save")
  FFHhgX(self["keyYellow"] , "Refresh")
  FFHhgX(self["keyBlue"]  , "NTP Mode")
  self["curTime"]  = Label()
  self["yearTitle"] = Label("Year")
  self["monthTitle"] = Label("Month")
  self["dayTitle"] = Label("Day")
  self["gapTitle"] = Label()
  self["hourTitle"] = Label("Hour")
  self["minTitle"] = Label("Min")
  self["secTitle"] = Label("Sec")
  self["year"]  = Label()
  self["month"]  = Label()
  self["day"]   = Label()
  self["gap"]   = Label()
  self["hour"]  = Label()
  self["min"]   = Label()
  self["sec"]   = Label()
  self.index   = 0
  self.list   = [self["year"], self["month"], self["day"], self["hour"], self["min"], self["sec"]]
  self.timer   = eTimer()
  self["gapTitle"].hide()
  self["gap"].hide()
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "red"   : self.VVIcsD  ,
   "green"   : self.VVmyxt ,
   "yellow"  : self.VVL9eR  ,
   "blue"   : self.VVWOG1   ,
   "up"   : self.VVmkvi    ,
   "down"   : self.VVcuOr   ,
   "left"   : self.VV8g7c   ,
   "right"   : self.VVkPgM   ,
   "cancel"  : self.VVIcsD
  }, -1)
  self["myTitle"].setText("  Date/Time -> Manual Mode")
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self.VVL9eR()
  self.VVH7je()
  FFtIlI(self)
  try:
   self.timer_conn = self.timer.timeout.connect(self.VVYqrP)
  except:
   self.timer.callback.append(self.VVYqrP)
  self.timer.start(1000, False)
  self.VVYqrP()
 def onExit(self):
  self.timer.stop()
 def VVIcsD(self) : self.close(True)
 def VVJ5XP(self) : self.close(False)
 def VVWOG1(self):
  self.session.openWithCallback(self.VVosug, BF(CCzM9L))
 def VVosug(self, closeAll):
  if closeAll:
   self.close()
 def VVYqrP(self):
  self["curTime"].setText(str(FFcgMH(iTime())))
 def VVmkvi(self):
  self.VVE29e(1)
 def VVcuOr(self):
  self.VVE29e(-1)
 def VV8g7c(self):
  self.index -= 1
  if self.index < 0:
   self.index = 5
  self.VVH7je()
 def VVkPgM(self):
  self.index += 1
  if self.index > 5:
   self.index = 0
  self.VVH7je()
 def VVE29e(self, increment):
  year = int(self["year" ].getText())
  month = int(self["month"].getText())
  if   self.index == 0: minVal, maxVal = 2000, 3000
  elif self.index == 1: minVal, maxVal = 1, 12
  elif self.index == 2: minVal, maxVal = 1, self.VVKtxb(month, year)
  elif self.index == 3: minVal, maxVal = 0, 59
  elif self.index == 4: minVal, maxVal = 0, 59
  elif self.index == 5: minVal, maxVal = 0, 59
  val  = int(self.list[self.index].getText()) + increment
  if val < minVal: val = maxVal
  if val > maxVal: val = minVal
  if self.index == 0:
   val = "%04d" % val
  else:
   val = "%02d" % val
  self.list[self.index].setText(val)
  if self.index < 2:
   year = int(self["year" ].getText())
   month = int(self["month"].getText())
   day = int(self["day"].getText())
   monthDays = self.VVKtxb(month, year)
   if day > monthDays:
    self["day"].setText("%02d" % monthDays)
 def VVKtxb(self, month, year):
  MonthList = [31,28,31,30,31,30,31,31,30,31,30,31]
  days = MonthList[month-1]
  if (month == 2) and (self.VVvjlY(year)):
   days += 1
  return days
 def VVvjlY(self, year):
  if year % 4 == 0:
   if year % 100 == 0:
    if year % 400 == 0:
     return True
    else:
     return False
   else:
    return True
  else:
   return False
 def VVH7je(self):
  for obj in self.list:
   FFobAA(obj, "#11404040")
  FFobAA(self.list[self.index], "#11ff8000")
 def VVL9eR(self):
  year, month, day, hour, minute, second, weekDay, yearDay, dayLight = localtime()
  self["year" ].setText("%04d" % year)
  self["month"].setText("%02d" % month)
  self["day"  ].setText("%02d" % day)
  self["hour" ].setText("%02d" % hour)
  self["min"  ].setText("%02d" % minute)
  self["sec"  ].setText("%02d" % second)
 def VVmyxt(self):
  year = int(self["year" ].getText())
  month = self["month"].getText()
  day  = self["day"  ].getText()
  hour = self["hour" ].getText()
  minute = self["min"  ].getText()
  second = self["sec"  ].getText()
  cmd = "date -s '%s-%s-%s %s:%s:%s'" % (year, month, day, hour, minute, second)
  tCons = CChHJE()
  tCons.ePopen("echo -e 'System Response:\n'; %s" % cmd, self.VVrMzk)
 def VVrMzk(self, result, retval):
  result = str(result.strip())
  if len(result) == 0:
   FFewCE(self, "Nothing returned from the system!")
  else:
   FFewCE(self, str(result))
class CCzM9L(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VV0L7B, 900, 480, 50, 40, 10, "#22660066", "#22330033", 35, barHeight=40)
  self.session  = session
  FFJd2Z(self, addLabel=True)
  FFHhgX(self["keyRed"]  , "Exit")
  FFHhgX(self["keyGreen"]  , "Sync")
  FFHhgX(self["keyYellow"] , "Refresh")
  FFHhgX(self["keyBlue"]  , "Manual Mode")
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "red"   : self.VVIcsD   ,
   "green"   : self.VVh8MP  ,
   "yellow"  : self.VVuJoN ,
   "blue"   : self.VVpXdG  ,
   "cancel"  : self.VVIcsD
  }, -1)
  self["myTitle"].setText("  Date/Time -> NTP Mode")
  self.VVP2Kc()
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  FFtIlI(self)
  FFpoMu(self.refresh)
 def refresh(self):
  self.VVE9gY()
  self.VVDgxq(False)
 def VVIcsD(self)  : self.close(True)
 def VVpXdG(self) : self.close(False)
 def VVP2Kc(self):
  self["myLabel"].setText("Getting NTP time ... ")
 def VVE9gY(self):
  self.VVdBUS()
  self.VVOVKl()
  self.VVvyoE()
  self.VVYVfT()
 def VVuJoN(self):
  if len(self["keyYellow"].getText()) > 0:
   self.VVP2Kc()
   self.VVE9gY()
   FFpoMu(self.refresh)
 def VVh8MP(self):
  if len(self["keyGreen"].getText()) > 0:
   FFMIbO(self, self.VVek58, "Synchronize with Internet Date/Time ?")
 def VVek58(self):
  self.VVE9gY()
  FFpoMu(BF(self.VVDgxq, True))
 def VVdBUS(self)  : self["keyRed"].show()
 def VVH1Rm(self)  : self["keyGreen"].show()
 def VVIhsJ(self) : self["keyYellow"].show()
 def VV1IH4(self)  : self["keyBlue"].show()
 def VVOVKl(self)  : self["keyGreen"].hide()
 def VVvyoE(self) : self["keyYellow"].hide()
 def VVYVfT(self)  : self["keyBlue"].hide()
 def VVDgxq(self, sync):
  localTime = FFDl5h()
  ok = False
  server_list = ['ntp.iitb.ac.in', 'time.nist.gov', 'time.windows.com', 'pool.ntp.org']
  for server in server_list:
   epoch_time = self.VVVT2t(server)
   if epoch_time is not None:
    ntpTime = FFcgMH(epoch_time)
    time1 = mktime(datetime.strptime(localTime, "%Y-%m-%d %H:%M:%S").timetuple())
    time2 = mktime(datetime.strptime(ntpTime  , "%Y-%m-%d %H:%M:%S").timetuple())
    diff = time1 - time2
    if   diff == 0 : timeDiff = "None"
    elif diff == 1 : timeDiff = "%d second"  % diff
    else   : timeDiff = "%d seconds" % diff
    timeDiff = "Difference\t=  %s" % timeDiff
    if sync:
     tCons = CChHJE()
     tCons.ePopen("echo -e '\nSystem Response:\n'; date -s '%s'" % ntpTime, BF(self.VVrMzk, True))
    else:
     txt = "Local Time\t= %s\nInternet Time\t= %s\n%s\n" % (localTime, ntpTime, timeDiff)
     self["myLabel"].setText(txt)
    ok = True
    break
   else:
    pass
  self.VVIhsJ()
  self.VV1IH4()
  if ok:
   self.VVH1Rm()
  else:
   self["myLabel"].setText("Local Time\t= %s\n\nCould not get NTP time !\n" % localTime)
 def VVrMzk(self, syncAgain, result, retval):
  result = str(result.strip())
  if len(result) == 0:
   result = "\n\nNothing returned from the system!"
  elif result.count("\n") < 20:
   result = "\n\n" + result
  try:
   self["myLabel"].setText(result)
   if syncAgain:
    self.VVDgxq(False)
  except:
   pass
 def VVVT2t(self, addr='time.nist.gov'):
  from socket import socket, AF_INET, SOCK_DGRAM
  from struct import unpack as iUnpack
  time1970 = 2208988800
  data  = '\x1b' + 47 * '\0'
  data  = data.encode()
  if FFINsi():
   try:
    client = socket(AF_INET, SOCK_DGRAM)
    client.settimeout(1.0)
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
     epoch_time = iUnpack('!12I', data)[10]
     epoch_time -= time1970
     return epoch_time
   except:
    pass
  return None
class CCqwcM(Screen):
 def __init__(self, session, args=0):
  self.skin, self.skinParam = FF896P(VVm2aL, 900, 300, 50, 20, 0, "#22000060", "#22000020", 35)
  self.session  = session
  FFJd2Z(self, addLabel=True, addCloser=True)
  self["myTitle"].setText("  Internet Connectivity")
  self["myLabel"].setText("Checking Connection ...")
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFpoMu(self.VV2tXW)
 def VV2tXW(self):
  if FFINsi(): color, txt = "#22002020", "Internet Connection = Successful."
  else   : color, txt = "#22500000", "Cannot connect (or server is down) !"
  try:
   self["myLabel"].setText("  " + txt)
   FFobAA(self["myBody"], color)
   FFobAA(self["myLabel"], color)
  except:
   pass
class CCWsdR(Screen):
 VVlcTS = None
 def __init__(self, session):
  size = CFG.signalSize.getValue()
  screenW = FFjf8O()[0]
  ratio = size / 5.0
  self.skin, self.skinParam = FF896P(VV3nyh, 650, 320, 26, 20, 20, "#22003040", "#22001122", 25, winRatio=ratio)
  self.session   = session
  self["mySNRdB"]   = Label()
  self["mySNR"]   = Label()
  self["myAGC"]   = Label()
  self["myBER"]   = Label()
  self["mySliderSNR"]  = Pixmap()
  self["mySliderAGC"]  = Pixmap()
  self["mySliderBER"]  = Pixmap()
  self["mySliderCovSNR"] = Label()
  self["mySliderCovAGC"] = Label()
  self["mySliderCovBER"] = Label()
  color     = self.skinParam["bodyColor"]
  self.sliderSNR   = CCkILY(self, self["mySliderSNR"], self["mySliderCovSNR"], minN=0, maxN=100, covColor=color)
  self.sliderAGC   = CCkILY(self, self["mySliderAGC"], self["mySliderCovAGC"], minN=0, maxN=100, covColor=color)
  self.sliderBER   = CCkILY(self, self["mySliderBER"], self["mySliderCovBER"], minN=0, maxN=100, covColor=color)
  self["myTPInfo"]  = Label()
  self.timer    = eTimer()
  self.tunerInfo   = CCg0pW()
  self.stateCounter  = 0
  self.top    = 0
  self.left    = 0
  self.curPosNum   = CFG.signalPos.getValue()
  self.curSize   = CFG.signalSize.getValue()
  FFJd2Z(self, title="Signal")
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : self.close      ,
   "up"  : self.VVmkvi       ,
   "down"  : self.VVcuOr      ,
   "left"  : self.VV8g7c      ,
   "right"  : self.VVkPgM      ,
   "info"  : self.VV0lXd     ,
   "epg"  : self.VV0lXd     ,
   "menu"  : self.VVHE2g      ,
   "cancel" : self.close      ,
   "red"  : self.close      ,
   "last"  : BF(self.VV45zK, -1)  ,
   "next"  : BF(self.VV45zK, 1)  ,
   "pageUp" : BF(self.VVfnxr, True) ,
   "chanUp" : BF(self.VVfnxr, True) ,
   "pageDown" : BF(self.VVfnxr, False) ,
   "chanDown" : BF(self.VVfnxr, False) ,
   "0"   : BF(self.VV45zK, 0)  ,
   "1"   : BF(self.VVQdBI, pos=1) ,
   "2"   : BF(self.VVQdBI, pos=2) ,
   "3"   : BF(self.VVQdBI, pos=3) ,
   "4"   : BF(self.VVQdBI, pos=4) ,
   "5"   : BF(self.VVQdBI, pos=5) ,
   "6"   : BF(self.VVQdBI, pos=6) ,
   "7"   : BF(self.VVQdBI, pos=7) ,
   "8"   : BF(self.VVQdBI, pos=8) ,
   "9"   : BF(self.VVQdBI, pos=9) ,
  }, -1)
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  if not CCWsdR.VVlcTS:
   CCWsdR.VVlcTS = self
  self.sliderSNR.VVyVAx()
  self.sliderAGC.VVyVAx()
  self.sliderBER.VVyVAx(isBER=True)
  pos   = self.instance.position()
  self.left = pos.x()
  self.top = pos.y()
  self.VVQdBI()
  self.VVdCKR()
  try:
   self.timer_conn = self.timer.timeout.connect(self.VVA2aZ)
  except:
   self.timer.callback.append(self.VVA2aZ)
  self.timer.start(500, False)
 def VVdCKR(self):
  service = self.session.nav.getCurrentService()
  self.tunerInfo.VVeSwA(service)
  serviceName = self.tunerInfo.VVbdgJ()
  if not serviceName   : serviceName = "Signal"
  if len(serviceName) > 25 : serviceName = serviceName[:25] + ".."
  self["myTitle"].setText("  " + serviceName)
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  tp = CCX8JT()
  tpTxt, satTxt = tp.VVQuAW(refCode)
  self["myTPInfo"].setText(tpTxt + "  " + FFkhYI(satTxt, VVoTT6))
 def VVA2aZ(self):
  service  = self.session.nav.getCurrentService()
  self.tunerInfo.VVeSwA(service)
  if self.tunerInfo.infoAvailable:
   self["mySNRdB"].setText(self.tunerInfo.VVxRg1())
   self["mySNR"].setText(self.tunerInfo.VVqy66())
   self["myAGC"].setText(self.tunerInfo.VVnIAQ())
   self["myBER"].setText(self.tunerInfo.VVIpSi())
   self.sliderSNR.VV1oU5(self.tunerInfo.VVMvRl())
   self.sliderAGC.VV1oU5(self.tunerInfo.VVqaqs())
   self.sliderBER.VV1oU5(self.tunerInfo.VVFe1d())
  else:
   self["mySNRdB"].setText("")
   self["mySNR"].setText("?")
   self["myAGC"].setText("?")
   self["myBER"].setText("?")
   self.sliderSNR.VV1oU5(0)
   self.sliderAGC.VV1oU5(0)
   self.sliderBER.VV1oU5(0)
  if self.stateCounter > -1:
   self.stateCounter += 1
   if self.stateCounter > 8:
    self.stateCounter = -1
   else:
    refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
    if state and not state == "Tuned":
     FFD1yO(self, state.replace(" (", "\n("), 1500)
     self.stateCounter = -1
 def VV0lXd(self):
  FFBatl(self, fncMode=CCARMv.VVHFwt)
 def VVHE2g(self):
  FF7SvB(self, VVASCC + "_help_signal", "Signal Monitor (Keys)")
 def VVmkvi(self)  : self.VVQdBI(posMap={7:4, 4:1, 8:5, 5:2, 9:6, 6:3})
 def VVcuOr(self) : self.VVQdBI(posMap={1:4, 4:7, 2:5, 5:8, 3:6, 6:9})
 def VV8g7c(self) : self.VVQdBI(posMap={3:2, 2:1, 6:5, 5:4, 9:8, 8:7})
 def VVkPgM(self) : self.VVQdBI(posMap={1:2, 2:3, 4:5, 5:6, 7:8, 8:9})
 def VVQdBI(self, posMap=None, pos=-1):
  if pos > -1 or posMap:
   if pos > -1:
    self.curPosNum = pos
   elif posMap:
    self.curPosNum = posMap.get(self.curPosNum, self.curPosNum)
   FFnT3A(CFG.signalPos, self.curPosNum)
  scrSize = getDesktop(0).size()
  gapH = gapV = 20
  w  = self.instance.size().width()
  h  = self.instance.size().height()
  left = self.left
  top  = self.top
  bot  = scrSize.height() - h - gapV
  rigth = scrSize.width()  - w - gapH
  if   self.curPosNum == 1: left, top = gapH , gapV
  elif self.curPosNum == 2: left, top = left , gapV
  elif self.curPosNum == 3: left, top = rigth , gapV
  elif self.curPosNum == 4: left, top = gapH , top
  elif self.curPosNum == 5: left, top = left , top
  elif self.curPosNum == 6: left, top = rigth , top
  elif self.curPosNum == 7: left, top = gapH , bot
  elif self.curPosNum == 8: left, top = left , bot
  elif self.curPosNum == 9: left, top = rigth , bot
  else     : left, top = left , top
  self.instance.move(ePoint(left, top))
 def VV45zK(self, sizeNum):
  oldSizeNum = CFG.signalSize.getValue()
  if sizeNum == 0:
   sizeNum = 5
  else:
   sizeNum += oldSizeNum
   sizeNum = FF2DVg(sizeNum, 1, 13)
  if not oldSizeNum == sizeNum:
   FFnT3A(CFG.signalSize, sizeNum)
   self.close(True)
 def onExit(self):
  self.timer.stop()
  CCWsdR.VVlcTS = None
 def VVfnxr(self, isUp):
  FFD1yO(self)
  try:
   if isUp : InfoBar.instance.zapDown()
   else : InfoBar.instance.zapUp()
   self.stateCounter = 0
   self.VVdCKR()
  except:
   pass
class CCkILY(object):
 def __init__(self, SELF, barObj, covObj, minN=0, maxN=100, covColor="#00440000"):
  self.SELF   = SELF
  self.barObj   = barObj
  self.covObj   = covObj
  self.minN   = minN
  self.maxN   = maxN
  self.covColor  = covColor
  self.isColormode = False
 def VVyVAx(self, isBER=False):
  self.barWidth = self.barObj.instance.size().width()
  self.barHeight = self.barObj.instance.size().height()
  self.barLeft = self.barObj.getPosition()[0]
  self.barTop  = self.barObj.getPosition()[1]
  if isBER:
   FFobAA(self.covObj, "#0aaa0000")
   self.isColormode = True
  else:
   path = VVASCC +  "bar_sig.png"
   if fileExists(path):
    self.barObj.instance.setScale(1)
    self.barObj.instance.setPixmapFromFile(path)
    FFobAA(self.covObj, self.covColor)
   else:
    FFobAA(self.covObj, "#00006688")
    self.isColormode = True
  self.VV1oU5(0)
 def VV1oU5(self, val):
  val  = FF2DVg(val, self.minN, self.maxN)
  width = int(FFZMXB(val, 0, 100, 0, self.barWidth))
  height = int(self.barHeight)
  if self.isColormode:
   self.covObj.instance.resize(eSize(*(width, height)))
  else:
   width = int(FF2DVg(self.barWidth - width, 0, self.barWidth))
   top  = int(self.barTop)
   left = int(self.barLeft + self.barWidth - width)
   self.covObj.hide()
   self.covObj.instance.resize(eSize(*(width, height)))
   self.covObj.instance.move(ePoint(left, top))
   self.covObj.show()
class CCC6u0(Screen):
 VVw5hO    = 0
 VVY9N6 = 1
 VVOVUF = 2
 def __init__(self, session, titlePrefix="Processing ...", fncToRun=None, VVnFNJ=None, barTheme=VVw5hO):
  ratio = self.VVlVEB(barTheme)
  self.skin, self.skinParam = FF896P(VV4yep, 900, 200, 30, 40, 30, "#0a042328", "#0a042328", 30, winRatio=ratio)
  self.session  = session
  self.barTheme  = barTheme
  self.titlePrefix = titlePrefix
  self.newTitle  = ""
  self.fncToRun  = fncToRun
  self.VVnFNJ = VVnFNJ
  self.isCancelled = False
  self.isError  = False
  self.maxValue  = 0
  self.barWidth  = 0
  self.barHeight  = 0
  self.counter  = 0
  self.VV0DcB = None
  self.timer   = eTimer()
  self.myThread  = None
  FFJd2Z(self, title=self.titlePrefix)
  self["myProgBar"]  = Label()
  self["myProgBarVal"] = Label()
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "cancel"  : self.cancel
  }, -1)
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self.VVoH6f()
  self["myProgBarVal"].setText("0%")
  FFobAA(self["myProgBar"], "#0a915332")
  size = self["myProgBar"].instance.size()
  self.barWidth = int(size.width())
  self.barHeight = int(size.height())
  self.VVZudJ()
  try:
   self.timer_conn = self.timer.timeout.connect(self.VVZudJ)
  except:
   self.timer.callback.append(self.VVZudJ)
  self.timer.start(300, False)
  self.myThread = iThread(name="ajp_progBar", target=BF(self.fncToRun, self))
  self.myThread.start()
 def VVYqos(self, val):
  self.maxValue = val
  self.newTitle = self.titlePrefix
 def VV95Yt(self, catName):
  self.newTitle = "Found %d\t%d/%d %s" % (len(self.VV0DcB), self.counter, self.maxValue, catName)
 def VVezgz(self, totEpgOK, uChName):
  self.newTitle = "Events: %d   (%d/%d)  %s" % (totEpgOK, self.counter, self.maxValue, uChName)
 def VVRqfk(self, tot):
  self.newTitle = "Downloaded %d    Processed : %d of %d" % (tot, self.counter, self.maxValue)
 def VVrCJd(self, title):
  self.newTitle = title
  try:
   self.VVZudJ()
  except:
   pass
 def VV1g3S(self, txt):
  self.newTitle = txt
 def VVLLRh(self, addVal, showFound=False):
  try:
   self.counter += addVal
   if showFound:
    self.newTitle = "Found %d\t .. Processed : %d of %d" % (len(self.VV0DcB), self.counter, self.maxValue)
  except:
   pass
 def VVcvlX(self, val):
  try:
   self.counter = val
  except:
   pass
 def VVzES5(self):
  try:
   return self.counter >= self.maxValue
  except:
   return True
 def VVon0e(self):
  self.isError = True
  self.cancel()
 def onExit(self):
  self.timer.stop()
 def cancel(self):
  self.timer.stop()
  FFD1yO(self, "Cancelling ...")
  self.isCancelled = True
  self.VVKlNg(False)
 def VVKlNg(self, isDone):
  if self.VVnFNJ:
   self.VVnFNJ(isDone, self.VV0DcB, self.counter, self.maxValue, self.isError)
  self.close()
 def VVZudJ(self):
  val = FF2DVg(self.counter, 0, self.maxValue)
  if self.maxValue > 0:
   width = int(FFZMXB(val, 0, self.maxValue, 0, self.barWidth))
   self["myProgBarVal"].setText(str(int(val * 100.0 / self.maxValue)) + "%")
   if   self.newTitle  : self["myTitle"].setText("  %s  " % self.newTitle)
   elif self.maxValue > 0 : self["myTitle"].setText("  %s  ( %d of %d ) ..." % (self.titlePrefix, self.counter, self.maxValue))
  else:
   width = 0
  self["myProgBar"].instance.resize(eSize(*(width, self.barHeight)))
  if self.myThread and not self.myThread.is_alive():
   self.timer.stop()
   if not self.isCancelled:
    self.VVKlNg(True)
 def VVoH6f(self):
  scrW = getDesktop(0).size().width()
  winW = self.instance.size().width()
  gap  = 30
  if self.barTheme in (self.VVY9N6, self.VVOVUF):
   self.instance.move(ePoint(int(scrW - winW - gap), gap))
 def VVlVEB(self, barTheme):
  if   barTheme == self.VVY9N6 : return 0.7
  if   barTheme == self.VVOVUF : return 0.5
  else             : return 1
class CChHJE(object):
 def __init__(self):
  self.appContainers = {}
  self.appResults  = {}
  self.dataAvailFnc = {}
  self.VVnFNJ = {}
  self.commandRunning = False
  self.VVyJBC  = fileExists("/etc/apt/apt.conf")
 def ePopen(self, cmd, VVnFNJ, dataAvailFnc=None, curDir=None):
  self.commandRunning = True
  name = cmd
  i  = 0
  while name in self.appContainers:
   name = cmd +'_'+ str(i)
   i += 1
  self.appResults[name] = ""
  self.dataAvailFnc[name] = dataAvailFnc
  self.VVnFNJ[name] = VVnFNJ
  try:
   from enigma import eConsoleAppContainer
   self.appContainers[name] = eConsoleAppContainer()
   if self.VVyJBC:
    self.appContainers[name].dataAvail_conn = self.appContainers[name].dataAvail.connect(BF(self.VV8PxJ, name))
    self.appContainers[name].appClosed_conn = self.appContainers[name].appClosed.connect(BF(self.VV9ZVB , name))
   else:
    self.appContainers[name].dataAvail.append(BF(self.VV8PxJ, name))
    self.appContainers[name].appClosed.append(BF(self.VV9ZVB , name))
  except:
   self.commandRunning = False
   return False
  if isinstance(cmd, str):
   cmd = [cmd]
  if curDir:
   try:
    self.appContainers[name].setCWD(curDir)
   except:
    pass
  retval = self.appContainers[name].execute(*cmd)
  if retval:
   self.VV9ZVB(name, retval)
  return True
 def VV8PxJ(self, name, data):
  data = data.decode("UTF-8")
  self.appResults[name] += data
  if self.dataAvailFnc[name]:
   self.dataAvailFnc[name](data)
 def VV9ZVB(self, name, retval):
  if not self.VVyJBC:
   del self.appContainers[name].dataAvail[:]
   del self.appContainers[name].appClosed[:]
  del self.appContainers[name]
  del self.dataAvailFnc[name]
  self.commandRunning = False
  if self.VVnFNJ[name]:
   self.VVnFNJ[name](self.appResults[name], retval)
  del self.VVnFNJ[name]
 def VVreFV(self):
  return self.commandRunning
 def kill(self, name):
  if name in self.appContainers:
   self.appContainers[name].kill()
 def killAll(self):
  for name in self.appContainers:
   self.kill(name)
  self.commandRunning = False
class CCxrj2(Screen):
 def __init__(self, session, title="", VV6D3C=None, VVPHtE=False, VVccyo=False, VVvFw0=False, VVSpRV=False, VVSzWe=False, VVvnLo=False, VVKsoz=VVw3Mn, VVIwP9=None, VVaunm=False, VVour7=None, VVEem5="", checkNetAccess=False, enableSaveRes=True):
  self.skin, self.skinParam = FF896P(VVhfwD, 1400, 800, 50, 40, 20, "#22003040", "#22001122", 30)
  self.session   = session
  FFJd2Z(self, addScrollLabel=True)
  if not VVEem5:
   VVEem5 = "Processing ..."
  self["myLabel"].setText("   %s" % VVEem5)
  self.VVPHtE   = VVPHtE
  self.VVccyo   = VVccyo
  self.VVvFw0   = VVvFw0
  self.VVSpRV  = VVSpRV
  self.VVSzWe = VVSzWe
  self.VVvnLo = VVvnLo
  self.VVKsoz   = VVKsoz
  self.VVIwP9 = VVIwP9
  self.VVaunm  = VVaunm
  self.VVour7  = VVour7
  self.checkNetAccess  = checkNetAccess
  self.enableSaveRes  = enableSaveRes
  self.cmdNum    = 0
  self.container   = CChHJE()
  self.justStarted  = True
  self.dataFound   = False
  if len(title) == 0:
   title = FFNUl9()
  self["myTitle"].setText("  %s" % title)
  if isinstance(VV6D3C, str):
   self.VV6D3C = [VV6D3C]
  else:
   self.VV6D3C = VV6D3C
  if self.VVvFw0 or self.VVSpRV:
   restartNote = "%s\\\\nGUI WILL RESTART NOW\\\\n%s" % (VVZ1aI, VVZ1aI)
   self.VV6D3C.append("echo -e '\n%s\n' %s" % (restartNote, FF95sl(restartNote, VVdWFT)))
   if self.VVvFw0:
    self.VV6D3C.append("sleep 3; if which systemctl > /dev/null 2>&1; then systemctl restart enigma2; else init 4; sleep 3; init 3; fi")
   else:
    self.VV6D3C.append("sleep 3; killall -9 enigma2; if which systemctl > /dev/null 2>&1; then systemctl start enigma2; else init 3; fi")
  if self.VVSzWe:
   FFD1yO(self, "Processing ...")
  self.onLayoutFinish.append(self.VVTlx4)
  self.onClose.append(self.VVz0Cw)
 def VVTlx4(self):
  self["myLabel"].VVqCbn(outputFileToSave="console" if self.enableSaveRes else "")
  if self.VVPHtE:
   self["myLabel"].VVw0Hf()
  if self.checkNetAccess:
   self["myLabel"].setText("  Checking Internet ...")
   self.VVwOZC()
  else:
   self.VVLEwh()
 def VVwOZC(self):
  if FFINsi():
   self["myLabel"].setText("Processing ...")
   self.VVLEwh()
  else:
   self["myLabel"].setText(FFkhYI("\n   No connection to internet!", VVU8eD))
 def VVLEwh(self):
  allOK = self.container.ePopen(self.VV6D3C[0], self.VVfeTo, dataAvailFnc=self.dataAvail)
  if not allOK:
   self.VVfeTo("Cannot connect to Console!", -1)
 def dataAvail(self, txt):
  if len(txt) > 0:
   self.dataFound = True
  if self.justStarted:
   self.justStarted = False
   if self.VVvnLo or self.VVvFw0 or self.VVSpRV:
    self["myLabel"].setText(FFINY2("STARTED", VVdWFT) + "\n")
   else:
    self["myLabel"].setText("")
  if self.VVour7:
   colorWhite = CCLqkY.VVdf1F(VVZgqQ)
   color  = CCLqkY.VVdf1F(self.VVour7[0])
   words  = self.VVour7[1:]
   for word in words:
    txt = iSub(r"(%s)" % iEscape(word), r"%s\1%s" % (color, colorWhite), txt, flags=IGNORECASE)
  self["myLabel"].appendText(txt, VVKsoz=self.VVKsoz)
 def VVfeTo(self, data, retval):
  self.cmdNum += 1
  if self.cmdNum != len(self.VV6D3C):
   allOK = self.container.ePopen(self.VV6D3C[self.cmdNum], self.VVfeTo, dataAvailFnc=self.dataAvail)
   if not allOK:
    self.VVfeTo("Cannot connect to Console!", -1)
  else:
   if self.VVSzWe and FF9RVa(self):
    FFD1yO(self)
   if not self.dataFound:
    self["myLabel"].setText("No result.")
   if self.VVvnLo:
    self["myLabel"].appendText("\n" + FFINY2("FINISHED", VVdWFT), self.VVKsoz)
   if self.VVPHtE or self.VVccyo:
    self["myLabel"].VVw0Hf()
   if self.VVIwP9 is not None:
    self.VVIwP9()
   if not retval and self.VVaunm:
    self.VVz0Cw()
 def VVz0Cw(self):
  if self.container.VVreFV():
   self.container.killAll()
class CCBZnl(Screen):
 def __init__(self, session, VV6D3C=None, VVSzWe=False):
  self.skin, self.skinParam = FF896P(VVhfwD, 1600, 900, 50, 40, 20, "#22200010", "#0a202020", 28, barHeight=40, usefixedFont=True)
  self.session   = session
  self.commandHistoryFile = VVCnD5 + "ajpanel_terminal.history"
  self.customCommandsFile = VVCnD5 + "LinuxCommands.lst"
  self.lastCommand  = "ls"
  self.prompt    = ">>"
  self.curDir    = FFj4HH("pwd") or "/home/root"
  self.container   = CChHJE()
  FFJd2Z(self, addScrollLabel=True)
  FFHhgX(self["keyRed"] , "Exit = Stop Command")
  FFHhgX(self["keyGreen"] , "OK = History")
  FFHhgX(self["keyYellow"], "Menu = Custom Cmds")
  FFHhgX(self["keyBlue"] , "0 - 9 = Keyboard")
  self["myAction"].actions.update(
  {
   "ok"  : self.VV78eH ,
   "cancel" : self.VVH8kZ  ,
   "menu"  : self.VVl83r ,
   "last"  : self.VVXNUv  ,
   "next"  : self.VVXNUv  ,
   "1"   : self.VVXNUv  ,
   "2"   : self.VVXNUv  ,
   "3"   : self.VVXNUv  ,
   "4"   : self.VVXNUv  ,
   "5"   : self.VVXNUv  ,
   "6"   : self.VVXNUv  ,
   "7"   : self.VVXNUv  ,
   "8"   : self.VVXNUv  ,
   "9"   : self.VVXNUv  ,
   "0"   : self.VVXNUv
  })
  self.onLayoutFinish.append(self.VVqouI)
  self.onClose.append(self.VVvU8A)
 def VVqouI(self):
  self["myLabel"].VVqCbn(isResizable=False, outputFileToSave="terminal")
  FFlr8P(self["keyRed"]  , "#00ff8000")
  FFobAA(self["keyRed"]  , self.skinParam["titleColor"])
  FFobAA(self["keyGreen"]  , self.skinParam["titleColor"])
  FFobAA(self["keyYellow"] , self.skinParam["titleColor"])
  FFobAA(self["keyBlue"] , self.skinParam["titleColor"])
  self.VVwam1(FFj4HH("date"), 5)
  result = FFj4HH("tUSER=$(whoami) || tUSER=""; tHOST=$(hostname) || tHOST=""; echo $tUSER,$tHOST")
  if result and "," in result:
   result = result.replace(",", "@")
   if len(result) < 15:
    self.prompt = result + " "
  self.prompt = "\n" + self.prompt
  self.VVP269()
  if not fileExists(self.customCommandsFile):
   oldTemplate = VVASCC + "LinuxCommands.lst"
   newTemplate = VVASCC + "ajpanel_cmd_list"
   if   fileExists(oldTemplate): os.system(FFxtg8("mv -f '%s' '%s'" % (oldTemplate, self.customCommandsFile)))
   elif fileExists(newTemplate): os.system(FFxtg8("cp -f '%s' '%s'" % (newTemplate, self.customCommandsFile)))
 def VVvU8A(self):
  if self.container.VVreFV():
   self.container.killAll()
   self.VVwam1("Process killed\n", 4)
   self.VVP269()
 def VVH8kZ(self):
  if self.container.VVreFV():
   self.VVvU8A()
  else:
   FFMIbO(self, self.close, "Exit ?", VVr8hX=False)
 def VVP269(self):
  self.VVwam1(self.prompt, 1)
  self["keyRed"].hide()
 def VVwam1(self, txt, mode):
  if   mode == 1 : color = VVdWFT
  elif mode == 2 : color = VVpHwQ
  elif mode == 3 : color = VVZgqQ
  elif mode == 4 : color = VVU8eD
  elif mode == 5 : color = VVkXS4
  elif mode == 6 : color = VVjrAG
  else   : color = VVZgqQ
  try:
   self["myLabel"].appendText(FFkhYI(txt, color))
  except:
   pass
 def VVS1c2(self, cmd):
  self["keyRed"].show()
  if cmd.startswith("passwd"):
   self.VVwam1(cmd, 2)
   self.VVwam1("\nCannot change passwrod from Console this way. Try using:\n", 4)
   txt = 'echo -e "NEW_PASSWORD\#nNEW_PASSWORD" | passwd'
   for ch in txt:
    if not ch == "#":
     self.VVwam1(ch, 0)
   self.VVwam1("\nor\n", 4)
   self.VVwam1("echo root:NEW_PASSWORD | chpasswd\n", 0)
   self.VVP269()
  else:
   cmd = cmd.strip()
   if "#" in cmd:
    parts = cmd.split("#")
    left  = FFkhYI(parts[0].strip(), VVpHwQ)
    right = FFkhYI("#" + parts[1].strip(), VVjrAG)
    txt = "%s    %s\n" % (left, right)
   else:
    txt = "%s\n" % cmd
   self.VVwam1(txt, 2)
   lastLine = self.VVKMzg()
   if not lastLine or not cmd == lastLine:
    self.lastCommand = cmd
    self.VVgjaN(cmd)
   span = iSearch(r".*cd\s+([\/?\w\.+\~]+)", cmd + ";")
   if span:
    self.curDir = span.group(1)
   allOK = self.container.ePopen(cmd, self.VVfeTo, dataAvailFnc=self.dataAvail, curDir=self.curDir)
   if not allOK:
    FFkYsE(self, "Cannot connect to Console!")
   self.lastCommand = cmd
 def dataAvail(self, data):
  self.VVwam1(data, 3)
 def VVfeTo(self, data, retval):
  if not retval == 0:
   self.VVwam1("Exit Code : %d\n" % retval, 4)
  self.VVP269()
 def VV78eH(self):
  title = "Command History"
  if not fileExists(self.commandHistoryFile) or self.VVKMzg() == "":
   self.VVgjaN("cd /tmp")
   self.VVgjaN("ls")
  VVvhuK = []
  if fileExists(self.commandHistoryFile):
   lines  = FFjdnJ(self.commandHistoryFile)
   c  = 0
   lNum = len(lines) + 1
   for line in reversed(lines):
    line = line.strip()
    lNum -= 1
    if line and not line.startswith("#"):
     c += 1
     VVvhuK.append((str(c), line, str(lNum)))
   self.VVW5sE(VVvhuK, title, self.commandHistoryFile, isHistory=True)
  else:
   FFAVqd(self, self.commandHistoryFile, title=title)
 def VVKMzg(self):
  lastLine = FFj4HH("grep '.' '%s' | tail -1" % self.commandHistoryFile)
  return lastLine.strip()
 def VVgjaN(self, cmd):
  with open(self.commandHistoryFile, "a") as f:
   f.write("%s\n" % cmd)
 def VVl83r(self):
  title = "Custom Commands"
  if fileExists(self.customCommandsFile):
   lines  = FFjdnJ(self.customCommandsFile)
   lastLineIsSep = False
   VVvhuK = []
   c  = 0
   lNum = 0
   for line in lines:
    line = line.strip()
    lNum += 1
    if line:
     c += 1
     if not iMatch("^[a-zA-Z0-9_]", line):
      line = "#f#00FF8055#" + line
     VVvhuK.append((str(c), line, str(lNum)))
   self.VVW5sE(VVvhuK, title, filePath=self.customCommandsFile, isHistory=False)
  else:
   FFAVqd(self, self.customCommandsFile, title=title)
 def VVW5sE(self, VVvhuK, title, filePath=None, isHistory=False):
  if VVvhuK:
   VV0g1U = "#05333333"
   if isHistory: VVz2kc = VVwpZm = VVghPi = "#11000020"
   else  : VVz2kc = VVwpZm = VVghPi = "#06002020"
   VVVHmY   = ("Send"   , BF(self.VVsTlt, isHistory) , [])
   VV3th8  = ("Modify & Send" , self.VVRgVC     , [])
   if isHistory:
    VVOtSO = ("Clear History" , self.VVTiUi     , [])
    VV1QO7 = None
   elif filePath:
    VVOtSO = None
    VV1QO7 = ("Edit File"  , BF(self.VVkMTR, filePath) , [])
   header      = ("No."  , "Commands", "LineNum")
   widths      = (7   , 93   , 0    )
   VVQqg2     = (CENTER  , LEFT   , CENTER )
   VVcpnp = FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7, lastFindConfigObj=CFG.lastFindTerminal, VVKNen=True, searchCol=1
     , VVz2kc   = VVz2kc
     , VVwpZm   = VVwpZm
     , VVghPi   = VVghPi
     , VVAfLs  = "#05ffff00"
     , VV0g1U  = VV0g1U
    )
   if not isHistory:
    VVcpnp.VVtpKN(CFG.lastTerminalCustCmdLineNum.getValue())
  else:
   FFzfYN(self, filePath, title=title)
 def VVsTlt(self, isHistory, VVcpnp, title, txt, colList):
  if not isHistory:
   FFnT3A(CFG.lastTerminalCustCmdLineNum, VVcpnp.VVgrGB())
  cmd = colList[1].strip()
  VVcpnp.cancel()
  if not iMatch("^[a-zA-Z0-9_]", cmd):
   self.VVwam1("\n%s\n" % cmd, 6)
   self.VVwam1(self.prompt, 1)
  else:
   self.VVS1c2(cmd)
 def VVRgVC(self, VVcpnp, title, txt, colList):
  cmd = colList[1]
  self.VVlMTX(VVcpnp, cmd)
 def VVTiUi(self, VVcpnp, title, txt, colList):
  FFMIbO(self, BF(self.VV4PSl, VVcpnp), "Reset History File ?", title="Command History")
 def VV4PSl(self, VVcpnp):
  os.system(FFxtg8("echo '' > %s" % self.commandHistoryFile))
  VVcpnp.cancel()
 def VVkMTR(self, filePath, VVcpnp, title, txt, colList):
  rowNum = int(colList[2].strip()) - 1
  if fileExists(filePath) : CCYE8p(self, filePath, VVnFNJ=BF(self.VVmlq3, VVcpnp), curRowNum=rowNum)
  else     : FFAVqd(self, filePath)
 def VVmlq3(self, VVcpnp, fileChanged):
  if fileChanged:
   VVcpnp.cancel()
   FFpoMu(self.VVl83r)
 def VVXNUv(self):
  self.VVlMTX(None, self.lastCommand)
 def VVlMTX(self, VVcpnp, cmd):
  if "#" in cmd:
   cmd = cmd.split("#")[0].strip()
  FFbRXK(self, BF(self.VViKPE, VVcpnp), title="Terminal", defaultText=cmd, message="Enter Command:")
 def VViKPE(self, VVcpnp, cmd):
  if cmd and len(cmd) > 0:
   self.VVS1c2(cmd)
   if VVcpnp:
    VVcpnp.cancel()
class CCpYuO(Screen):
 def __init__(self, session, title="", message="", VVKsoz=VVw3Mn, width=1400, VVXeWx=False, VVghPi=None, VVmp7B=30, outputFileToSave=""):
  self.skin, self.skinParam = FF896P(VVhfwD, width, 800, 50, 30, 20, "#22002020", "#22001122", VVmp7B)
  self.session   = session
  FFJd2Z(self, title, addScrollLabel=True)
  self.VVKsoz   = VVKsoz
  self.VVXeWx   = VVXeWx
  self.VVghPi   = VVghPi
  self.outputFileToSave = outputFileToSave
  if isinstance(message, list):
   try:
    self.message = "\n".join(message)
   except:
    self.message = str(message)
  else:
   self.message = str(message)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self["myLabel"].VVqCbn(VVXeWx=self.VVXeWx, outputFileToSave=self.outputFileToSave)
  self["myLabel"].setText(self.message, self.VVKsoz)
  if self.VVghPi:
   FFobAA(self["myBody"], self.VVghPi)
   FFobAA(self["myLabel"], self.VVghPi)
   FFMGhc(self["myLabel"], self.VVghPi)
  self["myLabel"].VVw0Hf()
class CC0jVk(Screen):
 def __init__(self, session, title="", message=""):
  self.skin, self.skinParam = FF896P(VVV9ui, 1200, 300, 50, 20, 0, "#22330000", "#22200000", 30)
  self.session = session
  FFJd2Z(self, title, addLabel=True, addCloser=True)
  self["errPic"] = Pixmap()
  self["myLabel"].setText(message)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FF4ISS(self["errPic"], "err")
class CClv1B(Screen):
 def __init__(self, session, txt, fntSize):
  self.skin, self.skinParam = FF896P(VVnacN, 1000, 50, 20, 30, 20, "#FF000000", "#FF000000", fntSize)
  self.session  = session
  self["myWinTitle"] = Label(txt)
  FFJd2Z(self, " ", addCloser=True)
class CCG7K3():
 def __init__(self, session, txt, timeout=1500):
  self.win = session.instantiateDialog(CClv1B, txt, 24)
  self.win.instance.move(ePoint(30, 20))
  self.win.show()
  FFiE61(self.win["myWinTitle"], "#440000", 2)
  self.session = session
  self.timer  = eTimer()
  try:
   self.timer_conn = self.timer.timeout.connect(self.VVvEL1)
  except:
   self.timer.callback.append(self.VVvEL1)
  self.timer.start(timeout, True)
 def VVvEL1(self):
  self.session.deleteDialog(self.win)
class CC9Zvn():
 VVnZ12    = 0
 VV0Ls8  = 1
 VVVOfm   = ""
 VV2Mbs    = "ajpDownload"
 def __init__(self, SELF, mode, title, startDnld, decodedUrl=""):
  self.SELF     = SELF
  self.mode     = mode
  self.Title     = title
  self.VVcpnp   = None
  self.timer     = eTimer()
  self.VVPNhZ   = 0
  self.VVKkBl  = 1
  self.VVWEe6  = 2
  self.VV5TpH   = 3
  self.VVVEml   = 4
  VVvhuK = self.VVKSKp()
  if VVvhuK:
   self.VVcpnp = self.VVUcNW(VVvhuK)
  if not VVvhuK and mode == self.VVnZ12:
   self.VV6I1g("Download list is empty !")
   self.cancel()
  if mode == self.VV0Ls8:
   FFlX3B(self.VVcpnp or self.SELF, BF(self.VV9ODJ, startDnld, decodedUrl), title="Checking Server ...")
  self.VV6OWM(force=True)
  try:
   self.timer_conn = self.timer.timeout.connect(self.VV6OWM)
  except:
   self.timer.callback.append(self.VV6OWM)
  self.timer.start(1000, False)
 def VVUcNW(self, VVvhuK):
  VVvhuK.sort(key=lambda x: int(x[0]))
  VVfPgM = self.VV2c3F
  VVVHmY  = ("Play"  , self.VVjg3J , [])
  VV01dN = (""   , self.VV2SDG  , [])
  VVMQj9 = ("Stop"  , self.VVjxTn  , [])
  VV3th8 = ("Resume"  , self.VVG7iB , [])
  VVOtSO = ("Options" , self.VVD3bX  , [])
  header   = ("No." , "Name" , "Type", "File Size", "Status" , "Progress", "Path", "sizeVal" , "URL" , "decodedUrl" , "oldSize" , "Speed" , "m3u8Log" )
  widths   = (5  , 39  , 8  , 13   , 13   , 11   , 0.01 , 0   , 0.01 , 0    , 0   , 11  , 0   )
  VVQqg2  = (CENTER, LEFT  , CENTER, CENTER  , CENTER , CENTER , LEFT , CENTER , LEFT , LEFT   , CENTER , CENTER , LEFT  )
  return FF1dQ4(self.SELF, None, title=self.Title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVVHmY=VVVHmY, VV01dN=VV01dN, VVfPgM=VVfPgM, VVMQj9=VVMQj9, VV3th8=VV3th8, VVOtSO=VVOtSO, lastFindConfigObj=CFG.lastFindIptv, VVz2kc="#11220022", VVwpZm="#11110011", VVghPi="#11110011", VVAfLs="#00ffff00", VV0g1U="#00223025", VVooYw="#0a333333", VVPVU2="#0a400040", VVKNen=True, searchCol=1)
 def VVKSKp(self):
  lines = CC9Zvn.VVyPHO()
  VVvhuK = []
  if lines:
   for ndx, line in enumerate(lines):
    if "," in line:
     parts  = line.split(",", 1)
     left  = parts[0].strip()
     decodedUrl = parts[1].strip()
     if left == "-1" or left.isdigit(): size, m3u8Log = int(left), ""
     else        : size, m3u8Log = -1  , left
     if decodedUrl:
      fName, chName, url = self.VVcJOW(decodedUrl)
      if fName:
       if   FFVq1j(decodedUrl) : sType = "Movie"
       elif FFo6Ta(decodedUrl) : sType = "Series"
       else      : sType = ""
       path = self.VVYSOk(decodedUrl, fName)
       if size > -1: sizeTxt = CC7ujK.VVw1Gr(size, mode=4)
       else  : sizeTxt = ""
       status = prog = speed = oldSize = ""
       VVvhuK.append((str(len(VVvhuK) + 1), chName, sType, sizeTxt, status, prog, path, str(size), url, decodedUrl, oldSize, speed, m3u8Log))
  return VVvhuK
 def VVosl6(self):
  VVvhuK = self.VVKSKp()
  if VVvhuK:
   if self.VVcpnp : self.VVcpnp.VVuVux(VVvhuK, VVP2KcMsg=False)
   else     : self.VVcpnp = self.VVUcNW(VVvhuK)
  else:
   self.cancel()
 def VV6OWM(self, force=False):
  if self.VVcpnp:
   thrListUrls = self.VVgh8w()
   VVvhuK = []
   changed = False
   for ndx, row in enumerate(self.VVcpnp.VVGrbO()):
    row = list(map(str.strip, row))
    num, name, typ, fSize, state, progr, path, sizeV, url, decodedUrl, oldSize, speed, m3u8Log = row
    flag = self.VVPNhZ
    if m3u8Log:
     percent = CC9Zvn.VVL7Z9(m3u8Log)
     if percent > -1:
      if percent < 100: flag, progr = self.VV5TpH , "%.2f %%" % percent
      else   : flag, progr = self.VVVEml , "100 %"
     mPath = m3u8Log[:-9]
     curSize = FFT03z(mPath)
     if curSize > -1:
      fSize = CC7ujK.VVw1Gr(curSize, mode=4)
     try:
      if not oldSize in ("", "0", "-"):
       diff = int(curSize - int(oldSize))
       if diff:
        speed = CC7ujK.VVw1Gr(diff, mode=4) + "/s"
     except:
      pass
    else:
     curSize = FFT03z(path)
     if curSize > -1:
      if sizeV.isdigit():
       percent = float(curSize) / float(sizeV) * 100.0
       if percent < 100: flag, progr = self.VV5TpH , "%.2f %%" % percent
       else   : flag, progr = self.VVVEml , "100 %"
       try:
        if not oldSize in ("", "0", "-"):
         diff = int(curSize - int(oldSize))
         if diff:
          speed = CC7ujK.VVw1Gr(diff, mode=4) + "/s"
       except:
        pass
    if decodedUrl in thrListUrls:
     flag = self.VVWEe6
     if m3u8Log :
      if not speed and not force : flag = self.VVKkBl
      elif curSize == -1   : self.VVSjAq(False)
    elif flag == self.VVPNhZ  : speed = progr = "-"
    else        : speed = "-"
    color1 = "#f#00FF9999#" if m3u8Log else ""
    if   flag == self.VVPNhZ  : color2 = "#f#00555555#"
    elif flag == self.VVKkBl : color2 = "#f#0000FFFF#"
    elif flag == self.VVWEe6 : color2 = "#f#0000FFFF#"
    elif flag == self.VV5TpH  : color2 = "#f#00FF8000#"
    elif flag == self.VVVEml  : color2 = "#f#0000FF00#"
    else        : color2 = "#f#00AAAAAA#"
    state = self.VVVNwj(flag)
    oldSize = str(curSize)
    if [num, name, typ, fSize, state, progr, path, sizeV, url, decodedUrl, oldSize, speed, m3u8Log] != row:
     changed = True
    row[1]  = color1 + name
    row[2]  = color1 + typ
    row[3]  = color1 + fSize
    row[4]  = color2 + state
    row[5]  = color2 + progr
    row[10] = oldSize
    row[11] = speed if not speed.startswith("-") else "-"
    VVvhuK.append(row)
   if changed or force:
    self.VVcpnp.VVuVux(VVvhuK, VVP2KcMsg=False)
 def VVVNwj(self, flag):
  tDict = self.VVTsyp()
  return tDict.get(flag, "?")
 def VVdVUn(self, state):
  for flag, txt in list(self.VVTsyp().items()):
   if txt == state:
    return flag
  return -1
 def VVTsyp(self):
  return { self.VVPNhZ: "Not started", self.VVKkBl: "Connecting", self.VVWEe6: "Downloading", self.VV5TpH: "Stopped", self.VVVEml: "Completed" }
 def VVUb6l(self, title):
  colList = self.VVcpnp.VVPxSj()
  path = colList[6]
  url  = colList[8]
  if self.VV9Hbh() : self.VV6I1g("Cannot delete !\n\nFile is downloading.")
  else      : FFMIbO(self.SELF, BF(self.VV5MJM, path, url), "Delete ?\n\n%s" % path, title=title)
 def VV5MJM(self, path, url):
  m3u8Log = self.VVcpnp.VVPxSj()[12]
  if m3u8Log : os.system(FFxtg8("rm -f '%s' '%s' '%s'" % (m3u8Log, m3u8Log[:-4], m3u8Log[:-9])))
  else  : os.system(FFxtg8("rm -r '%s'" % path))
  self.VVWYT3(False)
  self.VVosl6()
 def VVWYT3(self, VVl2X5=True):
  if self.VV9Hbh():
   FFD1yO(self.VVcpnp, self.VVVNwj(self.VVWEe6), 500)
  else:
   colList  = self.VVcpnp.VVPxSj()
   state  = colList[4]
   decodedUrl = colList[9]
   if self.VVdVUn(state) in (self.VVPNhZ, self.VVVEml, self.VV5TpH):
    lines = CC9Zvn.VVyPHO()
    newLines = []
    found = False
    for line in lines:
     if CC9Zvn.VVR3lP(decodedUrl, line): found = True
     else            : newLines.append(line)
    if found:
     self.VVNcZL(newLines)
     self.VVosl6()
     FFD1yO(self.VVcpnp, "Removed.", 1000)
    else:
     FFD1yO(self.VVcpnp, "Not found.", 1000)
   elif VVl2X5:
    self.VV6I1g("Cannot remove partial download !\n\nYou can delete the file (from options).")
 def VVwlC3(self, flag, title):
  ques = "Only remove from table (no file deletion).\n\nContinue ?"
  FFMIbO(self.SELF, BF(self.VVdE5Z, flag), ques, title=title)
 def VVdE5Z(self, flag):
  list = []
  for ndx, row in enumerate(self.VVcpnp.VVGrbO()):
   state  = row[4].strip()
   decodedUrl = row[9].strip()
   flagVal  = self.VVdVUn(state)
   if   flag == flagVal == self.VVVEml: list.append(decodedUrl)
   elif flag == flagVal == self.VVPNhZ : list.append(decodedUrl)
  lines = CC9Zvn.VVyPHO()
  totRem = 0
  newLines = []
  for line in lines:
   if any(x in line for x in list) : totRem += 1
   else       : newLines.append(line)
  if totRem > 0:
   self.VVNcZL(newLines)
   self.VVosl6()
   FFD1yO(self.VVcpnp, "%d removed." % totRem, 1000)
  else:
   FFD1yO(self.VVcpnp, "Not found.", 1000)
 def VVRdJC(self):
  colList  = self.VVcpnp.VVPxSj()
  path  = colList[6]
  decodedUrl = colList[9]
  png   = "%s.png" % os.path.splitext(path)[0]
  if fileExists(png) : FFD1yO(self.VVcpnp, "Poster exists", 1500)
  else    : FFlX3B(self.VVcpnp, BF(self.VVXEg8, decodedUrl, path, png), title="Checking Server ...")
 def VVXEg8(self, decodedUrl, path, png):
  err = self.VVhzwu(decodedUrl, path, png)
  if err:
   FFkYsE(self.SELF, err, title="Poster Download")
 def VVhzwu(self, decodedUrl, path, png):
  if "chCode" in decodedUrl:
   decodedUrl = CCyIre.VVQdst(decodedUrl)
   if not decodedUrl:
    return "Portal connection error !"
  pUrl = ""
  uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(decodedUrl)
  if all([uHost, uUser, uPass, uId]):
   qUrl = "%s/player_api.php?username=%s&password=%s&action=get_vod_info&vod_id=%s" % (uHost, uUser, uPass, uId)
   txt, err = CCqQHV.VVpi8S(qUrl, timeout=1)
   if err:
    return "Cannot get Poster URL from server !\n\n%s" % err
   else:
    try:
     tDict = jLoads(txt)
     pUrl = CCqQHV.VVvsIK(tDict["info"], "movie_image")
    except:
     return "Cannot parse Poster URL !"
  if not pUrl:
   return "No Poster data from server !"
  ext = os.path.splitext(pUrl)[1] or ".png"
  tPath, err = FF913T(pUrl, "ajpanel_tmp%s" % ext, timeout=2, mustBeImage=True)
  if err:
   return "Cannot download poster !\n\n%s" % err
  else:
   png = "%s%s" % (os.path.splitext(path)[0], ext)
   os.system(FFxtg8("mv -f '%s' '%s'" % (tPath, png)))
   CCd1mn.VVQ7Bd(self.SELF, VVHEnC=png, showGrnMsg="Downloaded")
   return ""
 def VV2SDG(self, VVcpnp, title, txt, colList):
  def VVD6fO(key, val) : return "%s\t: %s\n" % (key, val.strip())
  def VVQQs4(key, val) : return "\n%s:\n%s\n" % (FFkhYI(key, VVoTT6), val.strip())
  heads  = self.VVcpnp.VVixmS()
  txt = ""
  for i in range(6):
   if i == 3:
    totSize = colList[7].strip()
    curSize = colList[10].strip()
    if totSize and totSize.isdigit(): txt += VVD6fO(heads[i]  , CC7ujK.VVw1Gr(int(totSize), mode=0))
    if curSize and curSize.isdigit(): txt += VVD6fO("Downloaded" , CC7ujK.VVw1Gr(int(curSize), mode=0))
   else:
    txt += VVD6fO(heads[i], colList[i])
  if not "j.php" in colList[9]:
   for i in (6, 8):
    txt += VVQQs4(heads[i], colList[i])
  FFNEkd(self.SELF, txt, title=title)
 def VVjg3J(self, VVcpnp, title, txt, colList):
  path = colList[6].strip()
  m3u8Log = colList[12].strip()
  if m3u8Log:
   path = m3u8Log[:-9]
  if fileExists(path) : CC7ujK.VVHl4q(self.SELF, path)
  else    : FFD1yO(self.VVcpnp, "File not found", 1000)
 def VV2c3F(self, VVcpnp):
  self.cancel()
 def cancel(self):
  self.timer.stop()
  if self.VVcpnp:
   self.VVcpnp.cancel()
  del self
 def VVD3bX(self, VVcpnp, title, txt, colList):
  c1, c2, c3 = VVTdoW, VVU8eD, VVoTT6
  path  = colList[6].strip()
  decodedUrl = colList[9].strip()
  resumeTxt = "Disable" if CFG.downloadAutoResume.getValue() else "Enable"
  showMonitor = "Disable" if CFG.downloadMonitor.getValue() else "Enable"
  VV625J = []
  VV625J.append((c1 + "Remove current row"       , "VVWYT3" ))
  VV625J.append(VVm77t)
  VV625J.append((c1 + 'Remove all "Completed"'      , "remFinished"   ))
  VV625J.append((c1 + 'Remove all "Not started"'     , "remPending"   ))
  VV625J.append(VVm77t)
  VV625J.append((c2 + "Delete the file (and remove from list)"  , "VVUb6l"))
  VV625J.append(VVm77t)
  VV625J.append((resumeTxt + " Auto Resume"       , "VVjj6a" ))
  VV625J.append((showMonitor + " On-screen Download Monitor"  , "toggleMonitor"  ))
  VV625J.append(VVm77t)
  t = "Download Movie Poster "
  if FFVq1j(decodedUrl): VV625J.append((c3 + "%s(from server)" % t , "VVRdJC"  ))
  else      : VV625J.append(("%s... Movies only" % t ,      ))
  if fileExists(path) : VV625J.append((c3 + "Open in File Manager" , "inFileMan,%s" % path ))
  else    : VV625J.append(("Open in File Manager"  ,      ))
  FFuRfS(self.SELF, BF(self.VV2E0G, VVcpnp), VV625J=VV625J, title=self.Title, VVeYEo=True, width=800, VVvQ6U=True, VVz2kc="#1a001122", VVwpZm="#1a001122")
 def VV2E0G(self, VVcpnp, item=None):
  if item:
   txt, ref, ndx = item
   if   ref == "VVWYT3"  : self.VVWYT3()
   elif ref == "remFinished"   : self.VVwlC3(self.VVVEml, txt)
   elif ref == "remPending"   : self.VVwlC3(self.VVPNhZ, txt)
   elif ref == "VVUb6l" : self.VVUb6l(txt)
   elif ref == "VVRdJC"  : self.VVRdJC()
   elif ref == "VVjj6a"  : FFnT3A(CFG.downloadAutoResume, not CFG.downloadAutoResume.getValue())
   elif ref == "toggleMonitor"   : FFnT3A(CFG.downloadMonitor, not CFG.downloadMonitor.getValue())
   elif ref.startswith("inFileMan,") :
    path = ref.split(",", 1)[1]
    if pathExists(path) : self.SELF.session.open(CC7ujK, mode=CC7ujK.VVPhtE, jumpToFile=path)
    else    : FFD1yO(VVcpnp, "Path not found !", 1500)
 def VV9ODJ(self, startDnld, decodedUrl):
  refreshToken = True
  if not decodedUrl:
   refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self.SELF)
  else:
   ndx = decodedUrl.find("j.php")
   if ndx > -1:
    url = CCyIre.VVQdst(decodedUrl)
    if url:
     decodedUrl = url + decodedUrl[ndx + 5:]
     refreshToken = False
    else:
     self.VV6I1g("Could not get download link !\n\nTry again later.")
     return
  for line in CC9Zvn.VVyPHO():
   if CC9Zvn.VVR3lP(decodedUrl, line):
    if self.VVcpnp:
     self.VVulXd(decodedUrl)
     FFpoMu(BF(FFD1yO, self.VVcpnp, "Already listed !", 2000))
    break
  else:
   params = self.VVee9i(decodedUrl, refreshToken)
   if len(params) == 1:
    self.VV6I1g(params[0])
   elif len(params) == 2:
    FFMIbO(self.SELF, BF(self.VVsZV9, params[0], decodedUrl), "Start downloading ?", title="Download (m3u8)")
   else:
    url, fSize, path, resp, resumable = params
    title= "Download : %s\n\n" % CC7ujK.VVw1Gr(fSize)
    FFMIbO(self.SELF, BF(self.VVecHp, decodedUrl, url, fSize, path, resp, startDnld), "Download to\n\n%s" % path, title=title)
 def VVecHp(self, decodedUrl, url, fSize, path, resp, startDnld):
  with open(CC9Zvn.VVrBPh(), "a") as f:
   f.write("%s,%s\n" % (fSize, decodedUrl))
  self.VVosl6()
  if self.VVcpnp:
   self.VVcpnp.VVIdSv()
  if startDnld:
   threadName = "%s{%s,Sz,}%s" % (CC9Zvn.VV2Mbs, path, decodedUrl)
   self.VVrYH2(threadName, url, decodedUrl, path, resp)
 def VVulXd(self, decodedUrl):
  if self.VVcpnp:
   for ndx, row in enumerate(self.VVcpnp.VVGrbO()):
    decodedUrl2 = row[9].strip()
    if decodedUrl == decodedUrl2 and self.VVcpnp:
     self.VVcpnp.VVtpKN(ndx)
     break
 def VVee9i(self, decodedUrl, checkExist=True, resumeByte=-1, refreshToken=True):
  fName = ""
  if decodedUrl:
   fName, chName, url = self.VVcJOW(decodedUrl)
  if not fName:
   return ["Cannot process URL parameters !"]
  path = self.VVYSOk(decodedUrl, fName)
  if checkExist and fileExists(path):
   return ["File already exists:\n\n%s" % path]
  if refreshToken and "chCode" in decodedUrl:
   url = CCyIre.VVQdst(decodedUrl)
   if not url:
    return ["Could not get download link from server!"]
  fSize = resumeFrom = resumeTo = 0
  resumable = False
  try:
   headers = CCyIre.VVDicS()
   if resumeByte > -1:
    headers["Range"] = "bytes=%d-" % resumeByte
   import requests
   resp = requests.get(url, headers=headers, timeout=3, stream=True, verify=False)
   if not resp.ok:
    return ["Err-%d : %s" % (resp.status_code, resp.reason)]
   head = resp.headers
   fSize = head.get("Content-Length", "")
   cType = head.get("Content-Type", "")
   resumable = CC9Zvn.VVXg6v(resp)
  except:
   return ["Could not get file info from server !"]
  if not fSize or not fSize.isdigit():
   return ["Cannot get file size from server !"]
  fSize = int(fSize)
  if not "video" in cType and not "application/octet-stream" in cType:
   if resp.url.endswith(".m3u8"):
    return [resp, 1]
   elif not cType and resumable:
    pass
   else:
    return ["Cannot download this video !\n\nIncorrect download data (or not allowed by server)."]
  err = CC9Zvn.VV93mo(fSize)
  if err:
   return [err]
  return [url, fSize, path, resp, resumable]
 def VVsZV9(self, resp, decodedUrl):
  if not os.system(FFxtg8("which ffmpeg")) == 0:
   FFMIbO(self.SELF, BF(CCqQHV.VV4Lee, self.SELF), '"FFmpeg" not found !\n\nInstall FFmpeg ?', title=chName)
   return
  fName, chName, url = self.VVcJOW(decodedUrl)
  dest = os.path.join(CFG.MovieDownloadPath.getValue(), fName)
  self.m3u8_params = resp, decodedUrl, dest, fName, chName, url
  rTxt = str(resp.text)
  rUrl = str(resp.url)
  if "#EXT-X-STREAM-INF" in rTxt:
   self.VV7sbp(rTxt, rUrl)
  elif "#EXTINF:" in rTxt:
   if fileExists(dest) : FFMIbO(self.SELF, BF(self.VVbzT6, rTxt, rUrl), "Overwrite existing file ?\n\n%s" % dest, title=chName)
   else    : self.VVbzT6(rTxt, rUrl)
  else:
   self.VV6I1g("Cannot process m3u8 file !")
 def VV7sbp(self, rTxt, rUrl):
  lst   = iFindall(r"RESOLUTION=(\d+x\d+).*\n(.+)", rTxt, IGNORECASE)
  VV625J = []
  for resol, fPath in lst:
   resol = str(resol).replace("x", " x ")
   fPath = str(fPath)
   fullUrl = CCqQHV.VV8M6j(rUrl, fPath)
   VV625J.append((resol, fullUrl))
  if VV625J:
   FFuRfS(self.SELF, self.VVc3Dk, VV625J=VV625J, title="Resolution", VVeYEo=True, VVvQ6U=True)
  else:
   self.VV6I1g("Cannot get Resolutions list from server !")
 def VVc3Dk(self, item=None):
  if item:
   txt, resolUrl, ndx = item
   resp, decodedUrl, dest, fName, chName, url = self.m3u8_params
   resol = txt.replace(" ", "")
   fPath, fExt = os.path.splitext(fName)
   fName = "%s_%s%s" % (fPath, resol, fExt)
   fPath, fExt = os.path.splitext(dest)
   dest = "%s_%s%s" % (fPath, resol, fExt)
   self.m3u8_params = resp, decodedUrl, dest, fName, chName, url
   if fileExists(dest):
    FFMIbO(self.SELF, BF(FFpoMu, BF(self.VVdgQ3, resolUrl)), "Overwrite existing file ?\n\n%s" % dest, title=chName)
   else:
    FFpoMu(BF(self.VVdgQ3, resolUrl))
 def VVdgQ3(self, resolUrl):
  txt, err = CCyIre.VVHmZi(resolUrl)
  if err : self.VV6I1g(err)
  else : self.VVbzT6(txt, resolUrl)
 def VV8zG8(self, logF, decodedUrl):
  found = False
  lines = CC9Zvn.VVyPHO()
  with open(CC9Zvn.VVrBPh(), "w") as f:
   for line in lines:
    if CC9Zvn.VVR3lP(decodedUrl, line):
     line = "%s,%s" % (logF, decodedUrl)
     found = True
    f.write(line + "\n")
  if not found:
   with open(CC9Zvn.VVrBPh(), "a") as f:
    f.write("%s,%s\n" % (logF, decodedUrl))
  self.VVosl6()
  if self.VVcpnp:
   self.VVcpnp.VVIdSv()
 def VVbzT6(self, rTxt, rUrl):
  resp, decodedUrl, dest, fName, chName, url = self.m3u8_params
  m3u8File = os.path.join(CFG.MovieDownloadPath.getValue(), "%s.m3u8" % fName)
  with open(m3u8File, "w") as f:
   lines = rTxt.splitlines()
   for line in lines:
    line = line.strip()
    if line.startswith(("#EXTM", "#EXT-")) and not line.startswith("#EXT-X-ENDLIST"):
     f.write(line + "\n")
  lst = iFindall(r"(#EXTINF:.+)\n(.+)", rTxt, IGNORECASE)
  if lst:
   with open(m3u8File, "a") as f:
    for extInf, fPath in lst:
     extInf = str(extInf)
     fPath = str(fPath)
     fPath = CCqQHV.VV8M6j(rUrl, fPath)
     f.write(extInf + "\n")
     f.write(fPath + "\n")
    f.write("#EXT-X-ENDLIST\n")
  else:
   self.VV6I1g("Incorrect m3u8 file from server !")
   return
  logF = "%s.log" % m3u8File
  self.VV8zG8(logF, decodedUrl)
  cmd  = "ffmpeg -y -hide_banner -protocol_whitelist file,http,https,tcp,tls,crypto -i '%s' -c copy '%s' > %s 2>&1" % (m3u8File, dest, logF)
  cmd += " && %s" % FFxtg8("rm -f '%s' '%s'" % (m3u8File, logF))
  threadName = "%s{%s,,%s}%s" % (CC9Zvn.VV2Mbs, dest, logF, decodedUrl)
  myThread = iThread(name=threadName, target=BF(os.system, cmd))
  myThread.start()
 @staticmethod
 def VVL7Z9(dnldLog):
  if fileExists(dnldLog):
   dur = CC9Zvn.VVXQfX(dnldLog)
   if dur > -1:
    tim = CC9Zvn.VVEG0M(dnldLog)
    if tim > -1:
     return float(tim) / float(dur) * 100
  elif fileExists(dnldLog[:-9]):
   return 100
  return -1
 @staticmethod
 def VVXQfX(dnldLog):
  lines = FFiGf6("head -n 15 %s" % dnldLog)
  for line in lines:
   span = iSearch(r"Duration:\s*(\d+):(\d+):(\d+.\d+)\s*", line, IGNORECASE)
   if span:
    return int(span.group(1)) * 3600 + int(span.group(2)) * 60 + float(span.group(3))
  return -1
 @staticmethod
 def VVEG0M(dnldLog):
  lines = FFiGf6("tail -n 15 %s" % dnldLog)
  for line in reversed(lines):
   span = iSearch(r"time=\s*(\d+):(\d+):(\d+.\d+)\s*", line, IGNORECASE)
   if span:
    return int(span.group(1)) * 3600 + int(span.group(2)) * 60 + float(span.group(3))
  return -1
 def VVYSOk(self, url, fName):
  path = CFG.MovieDownloadPath.getValue()
  if FFo6Ta(url):
   span = iSearch(r"(.+)_(Season_[0-9]*|S[0-9]*E[0-9]*|E[0-9]*S[0-9]*)_.+", fName, IGNORECASE)
   if span:
    path1 = path + span.group(1)
    os.system(FFxtg8("mkdir '%s'" % path1))
    if pathExists(path1):
     return path1 + "/" + fName
  return path + fName
 def VVrYH2(self, threadName, url, decodedUrl, path, resp, isAppend=False):
  totFileSize = int(self.VVcpnp.VVPxSj()[7])
  threadName = threadName.replace(",Sz,", ",%s," % totFileSize)
  myThread = iThread(name=threadName, target=BF(self.VVoG3L, url, decodedUrl, path, resp, totFileSize, isAppend))
  myThread.start()
 def VVoG3L(self, url, decodedUrl, path, resp, totFileSize, isAppend):
  totBytes = 0
  try:
   with open(path, "ab" if isAppend else "wb") as f:
    for chunk in resp.iter_content(chunk_size=8192):
     if fileExists(path):
      if chunk:
       try:
        f.write(chunk)
       except:
        return
      if self.VVVOfm == path:
       break
     else:
      break
  except:
   return
  if CC9Zvn.VVVOfm:
   CC9Zvn.VVVOfm = ""
  elif CFG.downloadAutoResume.getValue():
   curSize = FFT03z(path)
   if curSize > -1 and not curSize == totFileSize:
    params = self.VVee9i(decodedUrl, checkExist=False, resumeByte=curSize)
    if len(params) > 1:
     url, fSize, path, resp, resumable = params
     if resumable:
      self.VVoG3L(url, decodedUrl, path, resp, totFileSize, True)
 def VVjxTn(self, VVcpnp, title, txt, colList):
  m3u8Log = colList[12].strip()
  decodedUrl = colList[9].strip()
  if       self.VVnfd9() : FFD1yO(self.VVcpnp, self.VVVNwj(self.VVVEml), 500)
  elif not self.VV9Hbh() : FFD1yO(self.VVcpnp, self.VVVNwj(self.VV5TpH), 500)
  elif m3u8Log      : FFMIbO(self.SELF, self.VVSjAq, "This may stop other non-resumable files !\n\nStop anyway ?", title="Stopping non-resumable download")
  else:
   if decodedUrl in self.VVgh8w():
    CC9Zvn.VVVOfm = colList[6]
    FFD1yO(self.VVcpnp, "Stopping ...", 1000)
   else:
    FFD1yO(self.VVcpnp, "Stopped", 500)
 def VVSjAq(self, withMsg=True):
  if withMsg:
   FFD1yO(self.VVcpnp, "Stopping ...", 1000)
  os.system(FFxtg8("killall -INT ffmpeg"))
 def VVG7iB(self, *args):
  if   self.VVnfd9() : FFD1yO(self.VVcpnp, self.VVVNwj(self.VVVEml) , 500)
  elif self.VV9Hbh() : FFD1yO(self.VVcpnp, self.VVVNwj(self.VVWEe6), 500)
  else:
   resume = False
   m3u8Log = self.VVcpnp.VVPxSj()[12]
   if m3u8Log:
    if fileExists(m3u8Log) : FFMIbO(self.SELF, BF(self.VVIfxh, m3u8Log), "Cannot resume m3u8 type !\n\nDelete file and restart download ?", title="Resume")
    else     : resume = True
   elif self.VVzc77():
    resume = True
   if resume: FFlX3B(self.VVcpnp, BF(self.VVc8jf), title="Checking Server ...")
   else  : FFD1yO(self.VVcpnp, "Cannot resume !", 500)
 def VVIfxh(self, m3u8Log):
  os.system(FFxtg8("rm -f '%s' '%s' '%s'" % (m3u8Log, m3u8Log[:-4], m3u8Log[:-9])))
  FFlX3B(self.VVcpnp, BF(self.VVc8jf), title="Checking Server ...")
 def VVc8jf(self):
  colList  = self.VVcpnp.VVPxSj()
  path  = colList[6]
  size  = colList[7]
  decodedUrl = colList[9]
  if "j.php" in decodedUrl:
   url = CCyIre.VVQdst(decodedUrl)
   if url:
    decodedUrl = self.VVV0yc(decodedUrl, url)
   else:
    self.VV6I1g("Could not get download link !\n\nTry again later.")
    return
  curSize = FFT03z(path)
  params = self.VVee9i(decodedUrl, checkExist=False, resumeByte=curSize)
  if len(params) == 1:
   self.VV6I1g(params[0])
   return
  elif len(params) == 2:
   self.VVsZV9(params[0], decodedUrl)
   return
  url, fSize, path, resp, resumable = params
  if size == "-1":
   decodedUrl = self.VVV0yc(decodedUrl, url, fSize)
  threadName = "%s{%s,Sz,}%s" % (CC9Zvn.VV2Mbs, path, decodedUrl)
  if resumable: self.VVrYH2(threadName, url, decodedUrl, path, resp, isAppend=True)
  else  : self.VV6I1g("Cannot resume from server !")
 def VVcJOW(self, decodedUrl):
  fileExt = CCqQHV.VVP82O(decodedUrl) or ".mp4"
  fixName = True
  url = fName = chName = ""
  tUrl = iSub(r"[&?]mode=.+end=", r"", decodedUrl, flags=IGNORECASE)
  span = iSearch(r"(https?:\/\/.+\/(?:movie|series).+\/.+\/)(.+)(:.+)", tUrl, IGNORECASE)
  if span:
   url  = span.group(1)
   fName = span.group(2)
   chName = span.group(3)
  elif "j.php" in tUrl:
   span = iSearch(r"(.+j.php)(:.+)", tUrl, IGNORECASE)
   if span:
    url  = span.group(1)
    fName = "tmp"
    chName = span.group(2)
  elif "/play/" in decodedUrl:
   span = iSearch(r"(.+)&mode.+&end=(:.+)", decodedUrl, IGNORECASE)
   if span:
    url = span.group(1)
    chName = span.group(2)
   span = iSearch(r".+movie.php?.+stream=(.+\..{3,4})&.+", decodedUrl, IGNORECASE)
   if span     : fName = span.group(1)
   elif fileExt == ".php" : fName = ".mkv" if ".mkv" in decodedUrl else ".mp4"
   else     : fName = fileExt
  elif "get_download_link" in decodedUrl:
   span = iSearch(r"(.+)&mode.+chCm=(.+)&end=(:.+)", decodedUrl, IGNORECASE)
   if span:
    url  = span.group(1)
    fName = os.path.basename(span.group(2))
    chName = span.group(3).replace(":", "_").strip("_")
    fixName = False
  else:
   ok = False
   span = iSearch(r"(.+\/(.+.mp4).+m3u8).+:(.+)", decodedUrl, IGNORECASE)
   if span:
    url  = span.group(1)
    fName = span.group(2)
    chName = span.group(3)
    fixName = False
    ok  = True
   if not ok:
    span = iSearch(r"(.+\/.+m3u8).*:(.+)", decodedUrl, IGNORECASE)
    if span:
     url  = span.group(1)
     chName = span.group(2)
     fName = chName + fileExt
     fixName = False
     ok  = True
   if not ok and FFeC5o(decodedUrl):
    span = iSearch(r"(.+)\?\:(.+)", decodedUrl, IGNORECASE)
    if span:
     url  = span.group(1)
     chName = span.group(2)
     fName = chName + fileExt
     fixName = False
    else:
     span = iSearch(r"(.+):(.+)", decodedUrl, IGNORECASE)
     if span:
      url  = span.group(1)
      chName = span.group(2)
      fName = chName + fileExt
      fixName = False
  if url and fName and chName:
   if fixName:
    mix  = fName + chName
    parts = mix.split(":", 1)
    fName = parts[0]
    chName = parts[1]
    fName = iSub(r"[?]play_token.+", r"", fName, flags=IGNORECASE)
    url += fName
   chName1 = chName.replace(" ", "_")
   chName1 = "".join(x for x in chName1 if x.isalnum() or x in "_-.")
   fName = chName1 + "_" + fName.lstrip("_")
   fName = fName.replace("_-_", "_")
   while "__" in fName:
    fName = fName.replace("__", "_")
   fName = fName.strip("_.")
   return fName, chName, url
  else:
   return "", "", ""
 def VV6I1g(self, txt):
  FFkYsE(self.SELF, txt, title=self.Title)
 def VVgh8w(self):
  thrListUrls = []
  for thr in iEnumerate():
   span = iSearch(r"%s(?:{.+})*(.+)" % CC9Zvn.VV2Mbs, thr.name, IGNORECASE)
   if span:
    thrListUrls.append(span.group(1))
  return thrListUrls
 def VV9Hbh(self):
  decodedUrl = self.VVcpnp.VVPxSj()[9]
  return decodedUrl in self.VVgh8w()
 def VVnfd9(self):
  colList = self.VVcpnp.VVPxSj()
  path = colList[6]
  size = colList[7]
  m3u8Log = colList[12]
  if m3u8Log:
   return fileExists(m3u8Log[:-9]) and not fileExists(m3u8Log)
  else:
   if size == "-1" : return False
   else   : return str(FFT03z(path)) == size
 def VVzc77(self):
  colList = self.VVcpnp.VVPxSj()
  path = colList[6]
  size = int(colList[7])
  curSize = FFT03z(path)
  if curSize > -1:
   size -= curSize
  err = CC9Zvn.VV93mo(size)
  if err:
   FFkYsE(self.SELF, err, title=self.Title)
   return False
  return True
 def VVNcZL(self, list):
  with open(CC9Zvn.VVrBPh(), "w") as f:
   for line in list:
    f.write(line + "\n")
 def VVV0yc(self, decodedUrl, newUrl, newSize=-1):
  found = False
  lines = CC9Zvn.VVyPHO()
  url = decodedUrl
  with open(CC9Zvn.VVrBPh(), "w") as f:
   for line in lines:
    if CC9Zvn.VVR3lP(decodedUrl, line):
     parts = line.split(",", 1)
     oldUrl = parts[1].strip()
     if newSize and not newSize == -1: fSize = str(newSize)
     else       : fSize = parts[0]
     ndx = url.find("j.php")
     if ndx > -1:
      url = newUrl + url[ndx + 5:]
     line = "%s,%s" % (fSize, url)
     found = True
    f.write(line + "\n")
  if found:
   self.VVosl6()
  return url
 @staticmethod
 def VVyPHO():
  list = []
  if fileExists(CC9Zvn.VVrBPh()):
   for line in FFjdnJ(CC9Zvn.VVrBPh()):
    line = line.strip()
    if line:
     list.append(line)
  return list
 @staticmethod
 def VVR3lP(decodedUrl, line):
  span = iSearch(r"(mode=.+end=.+)", decodedUrl, IGNORECASE)
  if span: decodedUrl = span.group(1)
  span = iSearch(r"(mode=.+end=.+)", line, IGNORECASE)
  if span: line = span.group(1)
  return decodedUrl in line
 @staticmethod
 def VV93mo(size):
  dest = CFG.MovieDownloadPath.getValue()
  if pathExists(dest):
   free = CC7ujK.VVMZOV(dest)
   if free > size : return ""
   else   : return "No enough space on:\n%s\n\nFile Size = %s\nFree Space = %s" % (dest, CC7ujK.VVw1Gr(size), CC7ujK.VVw1Gr(free))
  else:
   return "Path not found !\n\n%s" % dest
 @staticmethod
 def VVjDLn(SELF):
  tot = CC9Zvn.VVkpCq()
  if tot:
   FFkYsE(SELF, "Cannot change while downloading.", title="")
   return True
  else:
   return False
 @staticmethod
 def VVkpCq():
  c = 0
  for thr in iEnumerate():
   if thr.name.startswith(CC9Zvn.VV2Mbs):
    c += 1
  return c
 @staticmethod
 def VVz5tx():
  lst = []
  for thr in iEnumerate():
   span = iSearch(r"%s(?:{(.+),(.*),(.*)}).+" % CC9Zvn.VV2Mbs, thr.name, IGNORECASE)
   if span:
    lst.append((span.group(1), span.group(2), span.group(3)))
  return lst
 @staticmethod
 def VVwsNU():
  return len(CC9Zvn.VVyPHO()) == 0
 @staticmethod
 def VVkQWY():
  list = []
  for p in harddiskmanager.getMountedPartitions():
   list.append(p.mountpoint)
  return list
 @staticmethod
 def VV16RV():
  mPoints = CC9Zvn.VVkQWY()
  list = []
  for mPath in mPoints:
   if not mPath == "/":
    path = mPath + "/movie/"
    if pathExists(path) : return path
    else    : list.append(mPath)
  drives = ("/hdd", "/usb", "/sd")
  for mPath in list:
   if any(x in mPath for x in drives):
    path = mPath + "/movie/"
    os.system(FFxtg8("mkdir '%s'" % path))
    if pathExists(path):
     return path
  return "/tmp/"
 @staticmethod
 def VVrBPh():
  f = "ajpanel_downloads"
  if pathExists("/home/root/"): return "/home/root/%s" % f
  else      : return "/home/%s" % f
 @staticmethod
 def VV4aex(SELF):
  CC9Zvn.VVutV2(SELF, CC9Zvn.VVnZ12)
 @staticmethod
 def VV2Asp(SELF):
  CC9Zvn.VVutV2(SELF, CC9Zvn.VV0Ls8, startDnld=True)
 @staticmethod
 def VV8EZX(SELF, url):
  CC9Zvn.VVutV2(SELF, CC9Zvn.VV0Ls8, startDnld=True, decodedUrl=url)
 @staticmethod
 def VVhnAm(SELF):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF)
  added, skipped = CC9Zvn.VVIp0j([decodedUrl])
  FFD1yO(SELF, "Added", 1000)
 @staticmethod
 def VVIp0j(list):
  added = skipped = 0
  for line in CC9Zvn.VVyPHO():
   for ndx, url in enumerate(list):
    if url and CC9Zvn.VVR3lP(url, line):
     skipped += 1
     list[ndx] = ""
     break
  with open(CC9Zvn.VVrBPh(), "a") as f:
   for url in list:
    if url:
     added += 1
     f.write("-1,%s\n" % url)
  return added, skipped
 @staticmethod
 def VVutV2(SELF, mode, startDnld=False, decodedUrl=""):
  title = "Download Manager"
  if not CC6sg1.VVStEc(SELF):
   return
  if mode == CC9Zvn.VVnZ12 and CC9Zvn.VVwsNU():
   FFkYsE(SELF, "Download list is empty !", title=title)
  else:
   inst = CC9Zvn(SELF, mode, title, startDnld=startDnld, decodedUrl=decodedUrl)
 @staticmethod
 def VVXg6v(res):
  if res.status_code == 206:
   return True
  else:
   hResume = res.headers.get("Accept-Ranges" , "")
   if hResume and not hResume == "none":
    return True
  return False
class CCppdx(Screen, CCsnEk):
 VVKGP0 = None
 def __init__(self, session, enableZapping=True, iptvTableParams=None, isFromExternal=False, enableDownloadMenu=True, enableOpenInFMan=True):
  self.skin, self.skinParam = FF896P(VV4ccg, 1600, 190, 28, 10, 6, "#1100202a", "#1100202a", 24, topRightBtns=2)
  CCsnEk.__init__(self)
  self.session    = session
  self.enableZapping   = enableZapping
  self.enableOpenInFMan  = enableOpenInFMan
  self.iptvTableParams  = iptvTableParams
  self.isFromExternal   = isFromExternal
  self.enableDownloadMenu  = enableDownloadMenu
  self.Title     = ""
  self.cutListBtn    = "Cut-List"
  self.timer     = eTimer()
  self.barWidth    = 0
  self.barHeight    = 0
  self.isManualSeek   = False
  self.manualSeekSec   = 0
  self.manualSeekPts   = 0
  self.jumpMinutes   = CFG.playerJumpMin.getValue()
  self.noteTime    = 0
  self.satInfo_TP    = ""
  self.lastPlayPos   = 0
  self.lastPlayPosTicker  = 0
  self.lastSubtitle   = None
  self.restoreLastPlayPos  = False
  self.autoReplay    = False
  self.VVFC5e   = chr(226) + chr(128) + chr(142)
  FFJd2Z(self, "")
  self["myPlayBarF"] = Label()
  self["myPlayBarBG"] = Label()
  self["myPlayBar"] = Label()
  self["myPlayMov"] = Label()
  self["myPlayVal"] = Label()
  self["myPlayPos"] = Label()
  self["myPlaySkp"] = Label()
  self["myPlayMsg"] = Label()
  self["myPlayRem"] = Label()
  self["myPlayDur"] = Label()
  self["myPlaySep"] = Label()
  self["myPlayGrn"] = Label("Refresh")
  self["myPlayJmp"] = Label(self.VVyuLQ())
  self["myPlayDat"] = Label("")
  self["myPlayTim"] = Label("")
  self["myPlayMrk"] = Label("<< || >>")
  self["myPlayRes"] = Label("")
  self["myPlayFps"] = Label()
  self["myPlayAsp"] = Label()
  self["myPlayBlu"] = Label(self.cutListBtn)
  self["myPlayTyp"] = Label()
  self["myPlayPic"] = Pixmap()
  self["myPlayDnld"] = Pixmap()
  self["myPlayRpt"] = Pixmap()
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : self.VVmz9T       ,
   "info"  : self.VV0lXd      ,
   "epg"  : self.VV0lXd      ,
   "menu"  : self.VVKSnw     ,
   "cancel" : self.cancel       ,
   "red"  : self.VVUWK8   ,
   "green"  : self.VVuE0V  ,
   "blue"  : self.VVuhrJ      ,
   "yellow" : self.VVMLqk ,
   "left"  : BF(self.VVs6QZ, -1)    ,
   "right"  : BF(self.VVs6QZ,  1)    ,
   "play"  : self.VVg5qs      ,
   "pause"  : self.VVg5qs      ,
   "playPause" : self.VVg5qs      ,
   "stop"  : self.VVg5qs      ,
   "rewind" : self.VVv06q      ,
   "forward" : self.VVksYO      ,
   "rewindDm" : self.VVv06q      ,
   "forwardDm" : self.VVksYO      ,
   "last"  : self.VVFaKX      ,
   "next"  : self.VVHjU5      ,
   "pageUp" : BF(self.VVkgDG, True)  ,
   "pageDown" : BF(self.VVkgDG, False)  ,
   "chanUp" : BF(self.VVkgDG, True)  ,
   "chanDown" : BF(self.VVkgDG, False)  ,
   "up"  : BF(self.VVkgDG, True)  ,
   "down"  : BF(self.VVkgDG, False)  ,
   "audio"  : BF(self.VVmyur, True)  ,
   "subtitle" : BF(self.VVmyur, False)  ,
   "text"  : self.VVaSUD  ,
   "0"   : BF(self.VV3KsO , 10)   ,
   "1"   : BF(self.VV3KsO , 1)   ,
   "2"   : BF(self.VV3KsO , 2)   ,
   "3"   : BF(self.VV3KsO , 3)   ,
   "4"   : BF(self.VV3KsO , 4)   ,
   "5"   : BF(self.VV3KsO , 5)   ,
   "6"   : BF(self.VV3KsO , 6)   ,
   "7"   : BF(self.VV3KsO , 7)   ,
   "8"   : BF(self.VV3KsO , 8)   ,
   "9"   : BF(self.VV3KsO , 9)
  }, -1)
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FF4Pls(self)
  if not CCppdx.VVKGP0:
   CCppdx.VVKGP0 = self
  left = self["keyInfo"].getPosition()[0]
  top  = self["myPlayDnld"].getPosition()[1]
  left -= self.skinParam["titleH"]
  self["myPlayDnld"].instance.move(ePoint(int(left), int(top)))
  self["myPlayDnld"].hide()
  FF4ISS(self["myPlayDnld"], "dnld")
  left -= self.skinParam["titleH"]
  self["myPlayRpt"].instance.move(ePoint(int(left), int(top)))
  self["myPlayRpt"].hide()
  FF4ISS(self["myPlayRpt"], "rpt")
  self.VVQagz()
  self.instance.move(ePoint(40, 40))
  self.VVSLHF(CFG.playerPos.getValue())
  self["myPlayMov"].hide()
  self["myPlaySkp"].hide()
  size = self["myPlayBar"].instance.size()
  self.barWidth = int(size.width())
  self.barHeight = int(size.height())
  self["myPlayBar"].instance.resize(eSize(*(1, self.barHeight)))
  try:
   self.timer_conn = self.timer.timeout.connect(self.VVurqT)
  except:
   self.timer.callback.append(self.VVurqT)
  self.timer.start(250, False)
  self.VVurqT("Checking ...")
  self.VVNjTE()
 def VVuE0V(self):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  self.lastSubtitle = CCSwZ2.VVre4L()
  if "chCode" in iptvRef:
   if CC6sg1.VVStEc(self):
    self.VVNjTE(True)
  else:
   self.VVurqT("Refreshing")
   serv = self.session.nav.getCurrentlyPlayingServiceReference()
   if serv:
    self.session.nav.stopService()
    self.session.nav.playService(serv)
   self.restoreLastPlayPos = True
 def VVQagz(self):
  self.satInfo_TP = ""
  refCode, decodedUrl, chName, evName, evNameNext, prov, fr, res, ratio, isDvb, isIptv, typeTxt, tColor, seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = self.VVjL8u()
  if refCode : self.Title = chName.replace("\n", " > ")
  else  : self.Title = VVMmz2 + "No Service !"
  self["myTitle"].setText("  " + self.Title + "  ")
  FFobAA(self["myTitle"], tColor)
  FFobAA(self["myBody"], tColor)
  for item in ("Pos", "Skp", "Msg", "Rem", "Dur", "Jmp", "Dat", "Tim", "Mrk", "Res", "Fps", "Asp", "Pic", "Typ"):
   FFobAA(self["myPlay%s" % item], tColor)
  picFile = CCARMv.VVE38P(refCode)
  if not fileExists(picFile):
   fPath, fDir, fName, picFile = CCARMv.VVglzz(self)
  cl = CCg2mT.VVjTx0(self["myPlayPic"], picFile, tColor)
  if cl:
   self["myPlayPic"].show()
   self["myPlayTyp"].hide()
  else:
   self["myPlayPic"].hide()
   self["myPlayTyp"].show()
   self["myPlayTyp"].setText(typeTxt)
 def VVurqT(self, stateTxt="", highlight=False):
  if not self.shown:
   return
  self["myPlayDat"].setText(datetime.now().strftime("%Y-%m-%d"))
  self["myPlayTim"].setText(datetime.now().strftime("%H:%M:%S"))
  tot = CC9Zvn.VVkpCq()
  if tot : self["myPlayDnld"].show()
  else : self["myPlayDnld"].hide()
  refCode, decodedUrl, chName, evName, evNameNext, prov, fr, res, ratio, isDvb, isIptv, typeTxt, tColor, seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = self.VVjL8u()
  if evName:
   evName = "    %s    " % FFkhYI(evName, VVkXS4)
  self["myTitle"].setText(self.VVFC5e + "  %s%s  " % (self.Title, evName))
  if seekable and self.VVr7Ww():
   FFlr8P(self["myPlayBlu"], "#00FFFFFF")
   FFobAA(self["myPlayBlu"], "#0a18188b")
   self["myPlayBlu"].setText(self.cutListBtn)
   self["myPlayBlu"].show()
  elif prov:
   FFlr8P(self["myPlayBlu"], "#00FFFF88")
   FFobAA(self["myPlayBlu"], tColor)
   self["myPlayBlu"].setText(prov)
   self["myPlayBlu"].show()
  else:
   self["myPlayBlu"].hide()
  self["myPlayRes"].setText(res)
  self["myPlayFps"].setText(fr)
  self["myPlayAsp"].setText(ratio)
  self["myPlayPos"].setText(posTxt if posTxt else "")
  self["myPlayVal"].setText(percTxt if percTxt else "")
  self["myPlayRem"].setText("-%s" % remTxt if remTxt else "")
  self["myPlayDur"].setText(durTxt if durTxt else "")
  if durTxt:
   FFobAA(self["myPlayBarBG"], "#11000000")
   self["myPlayBarBG"].show()
   self["myPlayBarF"].show()
   self["myPlayBar"].show()
   width = 0
   percent = FF2DVg(percVal, 0, 100)
   width = int(FFZMXB(percent, 0, 100, 0, self.barWidth))
   self["myPlayBar"].instance.resize(eSize(*(width, self.barHeight)))
  else:
   self["myPlayBarBG"].hide()
   self["myPlayBarF"].hide()
   self["myPlayBar"].hide()
   self["myPlayVal"].setText(">>>>")
   FFobAA(self["myPlayBarBG"], tColor)
  if stateTxt:
   if highlight: FFlr8P(self["myPlayMsg"], "#0000ffff")
   else  : FFlr8P(self["myPlayMsg"], "#00ffaa00")
   self["myPlayMsg"].setText(stateTxt)
   self.noteTime = iTime()
  if self.noteTime and iTime() - self.noteTime < 1:
   return
  else:
   self.noteTime = 0
   FFlr8P(self["myPlayMsg"], "#00ffaa00")
   self["myPlayMsg"].setText("No system info")
  if isDvb:
   FFlr8P(self["myPlayMsg"], "#00aaaaaa")
   self["myPlayMsg"].setText(self.satInfo_TP)
  if not seekable:
   return
  stateTxt = ""
  if not posTxt and not durTxt:
   stateTxt = "Not playing yet ..."
  state = self.VVaz6P()
  if state:
   if state == "Playing" and not posTxt: stateTxt = "Waiting for state change"
   elif percVal == 100     : stateTxt = "End"
   else        : stateTxt = state
   if state == "Playing" and posTxt:
    if self.restoreLastPlayPos:
     if self.lastPlayPos > 0:
      move = end = False
      s = "." * self.lastPlayPosTicker
      stateTxt = ("%s Restoring Posistion %s" % (s, s)).strip()
      self.lastPlayPosTicker += 1
      diff = abs(posVal - self.lastPlayPos)
      if   diff < 10     : end = True
      elif self.lastPlayPosTicker == 1: move = True
      elif self.lastPlayPosTicker >= 10:
       if diff > 10:
        move = True
       end = True
      if move:
       self.VVVd1K(self.lastPlayPos * 90000.0)
      if end:
       self.lastPlayPosTicker = 0
       self.restoreLastPlayPos = False
       CCSwZ2.VVjEWn(self.lastSubtitle)
     else:
      self.restoreLastPlayPos = False
    else:
     self.lastPlayPos = posVal
   elif stateTxt == "End" and self.autoReplay:
    self.VVFaKX()
  state = self.VVWRgq()
  if state:
   stateTxt = state
  if stateTxt == "Playing": FFlr8P(self["myPlayMsg"], "#0000ff00")
  else     : FFlr8P(self["myPlayMsg"], "#00FF8F5F")
  self["myPlayMsg"].setText(stateTxt)
 def VVjL8u(self, isFromSession=False, addInfoObj=False):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state, info = FFnQlZ(self, addInfoObj=True)
  seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
  serv = self.session.nav.getCurrentlyPlayingServiceReference()
  isLocal, isIptv, isDvb, isDvbS, isDvbC, isDvbT, typeTxt, chPath = CCARMv.VVTLfj(serv)
  if   isDvb        : tColor = "#1100102a"
  elif isLocal       : tColor = "#0a401100"
  elif "chCode" in decodedUrl:
   if "get_download_link" in decodedUrl: tColor = "#1120101a"
   else        : tColor = "#1120002a"
  elif "/timeshift/" in decodedUrl  : tColor = "#11223322"
  else         : tColor = "#11001c1c"
  chPath = serv and serv.getPath() or ""
  satTxt = ""
  if isDvb and not self.satInfo_TP:
   tp = CCX8JT()
   tpTxt, satTxt = tp.VVQuAW(refCode)
   self.satInfo_TP = tpTxt + "  " + FFkhYI(satTxt, VVNTmM)
  evName = evNameNext = ""
  evLst = CCARMv.VV0teF(refCode)
  if evLst:
   evName, evShort, evDesc, genre, PR, evTime, evTimeTxt, evDur, evDurTxt, evEnd, evEndTxt, evPos, evPosTxt, evRem, evRemTxt, evCom, evComTxt = evLst[0]
   if not durVal:
    if len(evLst) > 1:
     evNameNext = evLst[1][0]
    if evPos >= evDur:
     percVal = 100
     percTxt = "%d %%" % percVal
    else:
     percVal = float(evPos) * 100.0 / float(evDur)
     percTxt = "%.2f %%" % percVal
    posVal, remVal, percTxt, durTxt, posTxt, remTxt = evPos, evRem, percTxt, evDurTxt, evPosTxt, evRemTxt
  fr = res = ""
  if info:
   w = FFAkN7(info, iServiceInformation.sVideoWidth) or -1
   h = FFAkN7(info, iServiceInformation.sVideoHeight) or -1
   if w != -1 and h != -1 and not w == "0" and not h == "0":
    res = "%s x %s" % (w, h)
   rate = FFAkN7(info, iServiceInformation.sFrameRate)
   if rate.isdigit() and not rate == "0":
    fr = "%d fps" % (int(rate) / 1000)
  ratio = CCARMv.VVyWJl(info)
  return refCode, decodedUrl, chName, evName, evNameNext, prov, fr, res, ratio, isDvb, isIptv, typeTxt, tColor, seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt
 @staticmethod
 def VV7UBu(SELF):
  percVal = durVal = posVal = remVal = seekable = 0
  percTxt = durTxt = posTxt = remTxt = ""
  isEnded = False
  try:
   service = SELF.session.nav.getCurrentService()
   if service:
    pSeek = service.seek()
    if pSeek:
     seekable = pSeek.isCurrentlySeekable()
     durLst  = pSeek.getLength()
     posLst  = pSeek.getPlayPosition()
     if durLst[0] == 0:
      durVal = durLst[1] / 90000.0
      if durVal:
       durTxt = FF3UDS(durVal)
     if posLst[0] == 0:
      posVal = posLst[1] / 90000.0
      posTxt = FF3UDS(posVal)
     if durVal > 0 and posVal > 0:
      remVal = durVal - posVal + 1
      remTxt = FF3UDS(remVal)
     if durVal > 0:
      if round(posVal) >= int(durVal):
       percVal = 100
       percTxt = "%d %%" % percVal
       posVal = durVal
       posTxt = durTxt
       remTxt = ""
      else:
       percVal = float(posVal) * 100.0 / float(durVal)
       percTxt = "%.2f %%" % percVal
  except:
   pass
  return seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt
 def VVKSnw(self):
  refCode, decodedUrl, chName, evName, evNameNext, prov, fr, res, ratio, isDvb, isIptv, typeTxt, tColor, seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = self.VVjL8u()
  FFVq1jSeries = FFeC5o(decodedUrl)
  VV625J = []
  if self.isFromExternal:
   VV625J.append((VVNTmM + "IPTV Menu"   , "iptv" ))
   VV625J.append(VVm77t)
  if isIptv and not "&end=" in decodedUrl and not FFVq1jSeries:
   uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(decodedUrl)
   if all([uHost, uUser, uPass, uId]):
    VV625J.append((VVNTmM + "Catchup Programs", "catchup" ))
    VV625J.append(VVm77t)
  if refCode:
   c = VVMmz2
   VV625J.append((c + "Stop Current Service"  , "stop"  ))
   VV625J.append((c + "Restart Current Service" , "restart"  ))
   VV625J.append(VVm77t)
  if FFVq1jSeries:
   VV625J.append((VVNTmM + "File Size (on server)", "fileSize" ))
   VV625J.append(VVm77t)
  if self.enableDownloadMenu:
   c = VVNTmM
   addSep = False
   if isIptv and FFVq1jSeries:
    VV625J.append((c + "Start Download"   , "dload_cur" ))
    VV625J.append((c + "Add to Download List"  , "addToDload" ))
    addSep = True
   if not CC9Zvn.VVwsNU():
    VV625J.append((VVNTmM + "Download Manager", "dload_stat" ))
    addSep = True
   if addSep:
    VV625J.append(VVm77t)
  fPath, fDir, fName = CC7ujK.VVa1tR(self)
  if fPath:
   c = VVk6tE
   if self.enableOpenInFMan and not CC7ujK.VVxHrh:
    VV625J.append((c + "Open path in File Manager", "VVDHCc"))
   VV625J.append((c + "Add to Bouquet"             , "VVNQxY" ))
   VV625J.append((c + "%s Auto-Repeat" % ("Disable" if self.autoReplay else "Enable") , "VV7zzP"  ))
   VV625J.append(VVm77t)
  if isDvb:
   VV625J.append((VVNTmM + "Signal Monitor", "sigMon"   ))
  if posTxt and durTxt:
   VV625J.append((VVoTT6 + "Start Subtitle", "VVSYr1"))
   VV625J.append(VVm77t)
  if CFG.playerPos.getValue() : VV625J.append(("Move Bar to Bottom"  , "botm"    ))
  else      : VV625J.append(("Move Bar to Top"  , "top"     ))
  VV625J.append(("Help"             , "help"    ))
  FFuRfS(self, self.VVAlWr, VV625J=VV625J, width=600, title="Options")
 def VVAlWr(self, item=None):
  if item:
   if item == "iptv"     : self.close("close_iptvMenu")
   elif item == "catchup"    : self.VVMLqk()
   elif item == "stop"     : self.VVCt1U(0)
   elif item == "restart"    : self.VVCt1U(1)
   elif item == "fileSize"    : FFlX3B(self, BF(CCARMv.VVsz5C, self), title="Checking Server")
   elif item == "dload_cur"   : CC9Zvn.VV2Asp(self)
   elif item == "addToDload"   : CC9Zvn.VVhnAm(self)
   elif item == "dload_stat"   : CC9Zvn.VV4aex(self)
   elif item == "VVDHCc" : self.close("close_openInFileMan")
   elif item == "VVNQxY" : self.VVNQxY()
   elif item == "VVSYr1"  : self.VVJYMj()
   elif item == "VV7zzP"  : self.VV7zzP()
   elif item == "botm"     : self.VVSLHF(0)
   elif item == "top"     : self.VVSLHF(1)
   elif item == "sigMon"    : self.VVUWK8()
   elif item == "help"     : FF7SvB(self, VVASCC + "_help_player", "Player Bar (Keys)")
 def onExit(self):
  self.timer.stop()
  CCppdx.VVKGP0 = None
 def VVCt1U(self, typ):
  serv = self.session.nav.getCurrentlyPlayingServiceReference()
  if serv:
   if typ == 0:
    self.session.nav.stopService()
    self.show()
    self.VVQagz()
   elif typ == 1:
    self.VVurqT("Restarting Service ...")
    FFpoMu(BF(self.VVreyS, serv))
 def VVreyS(self, serv):
  self.session.nav.stopService()
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  if "&end=" in decodedUrl: BF(self.VVNjTE, True)
  else     : self.session.nav.playService(serv)
 def VVNQxY(self):
  fPath, fDir, fName = CC7ujK.VVa1tR(self)
  if fPath: picker = CCgKdM(self, self, "Add Current Movie to a Bouquet", BF(self.VV1Y6i, [fPath]))
  else : FFD1yO(self, "Path not found !", 1500)
 def VV1Y6i(self, pathLst):
  return CCgKdM.VVpsne(pathLst)
 def VV7zzP(self):
  ok = False
  if self.autoReplay:
   self.autoReplay = False
   txt = "Auto-Repeat OFF"
   ok = True
  else:
   seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
   if seekable and durVal > 0:
    if durVal >= 60:
     self.autoReplay = True
     txt = "Auto-Repeat ON"
     ok = True
    else: txt = "Too short (min = 1 minute)"
   else: txt = "Cannot Auto-Repeat"
  if self.autoReplay : self["myPlayRpt"].show()
  else    : self["myPlayRpt"].hide()
  self.VVurqT(txt, highlight=ok)
 def VVSLHF(self, pos):
  scrSize = getDesktop(0).size()
  scrW = scrSize.width()
  scrH = scrSize.height()
  x  = (scrW - self.instance.size().width()) / 2.0
  if pos == 0 : y = (scrH - self.instance.size().height() - 20)
  else  : y = 20
  self.instance.move(ePoint(int(x), int(y)))
  if not pos == CFG.playerPos.getValue():
   FFnT3A(CFG.playerPos, pos)
 def VVUWK8(self):
  if self.shown:
   serv = self.session.nav.getCurrentlyPlayingServiceReference()
   isLocal, isIptv, isDvb, isDvbS, isDvbC, isDvbT, typeTxt, chPath = CCARMv.VVTLfj(serv)
   if isDvb: self.close("close_sig")
   else : self.VVurqT("No Signal for Current Service")
 def VVJYMj(self):
  self.session.openWithCallback(self.VV9KIr, BF(CCSwZ2))
 def VVaSUD(self):
  if self.shown:
   refCode, decodedUrl, chName, evName, evNameNext, prov, fr, res, ratio, isDvb, isIptv, typeTxt, tColor, seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = self.VVjL8u()
   if posTxt and durTxt: self.VVJYMj()
   else    : self.VVurqT("No duration Info. !")
 def VV9KIr(self, reason):
  self.show()
  txt = ""
  if   reason == "subtExit" : pass
  elif reason == "subtCancel" : pass
  elif reason == "subtEnd" : txt = "End of subtitle reached"
  elif reason == "subtInval" : txt = "Invalid srt file"
  elif reason == "subtNoSrt" : txt = "Not found"
  elif reason == "subtZapUp" : self.VVkgDG(True)
  elif reason == "subtZapDn" : self.VVkgDG(False)
  else      : txt = reason
  if txt:
   FFD1yO(self, txt, 2000)
 def VVmz9T(self):
  if self.isManualSeek:
   self.VV9LPF()
   self.VVVd1K(self.manualSeekPts)
  elif self.shown:
   if CCSwZ2.VVJgMd(self): self.VVJYMj()
   elif self.shown       : self.hide()
  else:
   self.show()
 def cancel(self):
  if self.isManualSeek: self.VV9LPF()
  else    : self.close()
 def VV0lXd(self):
  FFBatl(self, fncMode=CCARMv.VVyj5y)
 def VVg5qs(self):
  inst = InfoBar.instance
  try:
   inst.playpauseService()
  except:
   pass
  self.VVurqT("Toggling Play/Pause ...")
 def VV9LPF(self):
  if self.isManualSeek:
   self.isManualSeek = False
   self["myPlayMov"].hide()
   self["myPlaySkp"].hide()
 def VVs6QZ(self, direc):
  seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
  if seekable and durVal > 0:
   if not self.isManualSeek:
    self.isManualSeek = True
    self["myPlayMov"].show()
    self["myPlaySkp"].show()
    self.manualSeekSec = posVal + direc * self.VV15C8()
   else:
    self.manualSeekSec += direc * self.VV15C8()
    self.manualSeekSec = FF2DVg(self.manualSeekSec, 0, durVal)
   minLeft = self["myPlayBar"].getPosition()[0] - 1
   maxLeft = self["myPlayBarBG"].getPosition()[0] + self["myPlayBarBG"].instance.size().width() - self["myPlayMov"].instance.size().width() + 1
   left = int(FFZMXB(self.manualSeekSec, 0, durVal, minLeft, maxLeft))
   self["myPlayMov"].instance.move(ePoint(left, int(self["myPlayMov"].getPosition()[1])))
   self["myPlaySkp"].setText(FF3UDS(self.manualSeekSec))
   self.manualSeekPts = self.manualSeekSec * 90000.0
 def VV3KsO(self, val):
  if not self.jumpMinutes == val:
   self.jumpMinutes = val
   self["myPlayJmp"].setText(self.VVyuLQ())
   FFnT3A(CFG.playerJumpMin, self.jumpMinutes)
  self.VVurqT("Changed Seek Time to : %d%s" % (val, self.VVYAAn()))
 def VVyuLQ(self):
  return "Seek=%d%s" % (self.jumpMinutes, self.VVYAAn())
 def VVYAAn(self) : return "s"   if self.jumpMinutes == 10 else "m"
 def VV43NO(self): return "sec" if self.jumpMinutes == 10 else "min"
 def VV15C8(self) : return 10    if self.jumpMinutes == 10 else self.jumpMinutes * 60
 def VVaz6P(self):
  if "EVENT_STATE" in globals():
   global EVENT_STATE
   if EVENT_STATE:
    EVENT_STATE = EVENT_STATE[1:-1]
    if len(EVENT_STATE) == 3: EVENT_STATE = ""
    else     : return EVENT_STATE
  try:
   inst = InfoBar.instance
   st   = inst.seekstate
   if   st == inst.SEEK_STATE_PAUSE: return "PAUSED"
   elif st == inst.SEEK_STATE_EOF : return "END"
   elif st == inst.SEEK_STATE_PLAY : return "Playing"
  except:
   pass
  return ""
 def VVuhrJ(self):
  cList = self.VVr7Ww()
  if cList:
   VV625J = []
   for pts, what in cList:
    txt = FF3UDS(int(pts) / 90000.0)
    if   what == 0 : t = "In"
    elif what == 1 : t = "Out"
    elif what == 2 : t = "Mark"
    elif what == 3 : t = "Last"
    else   : t = ""
    if t: txt += "  ( %s )" % t
    VV625J.append((txt, pts))
   FFuRfS(self, self.VVeVFC, VV625J=VV625J, title="Cut List")
  else:
   self.VVurqT("No Cut-List for this channel !")
 def VVeVFC(self, item=None):
  if item:
   self.VVVd1K(item)
 def VVr7Ww(self):
  cList = []
  try:
   cList = InfoBar.instance.cut_list or []
  except:
   pass
  return cList
 def VVksYO(self) : self.VVtlL9(1)
 def VVv06q(self) : self.VVtlL9(-1)
 def VVtlL9(self, direc):
  try:
   seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
   if durVal > 0:
    maxPts = (durVal - posVal- 10) * 90000.0
    pts = direc * self.VV15C8() * 90000.0
    pts = min(maxPts, pts)
    inst = InfoBar.instance
    inst.doSeekRelative(int(pts))
    inst.hide()
    if   direc > 0 : txt = "Forawrd"
    else   : txt = "Rewind"
    txt += " (%d %s) ..." % (self.jumpMinutes, self.VV43NO())
    self.VVurqT(txt)
  except:
   self.VVurqT("Cannot jump")
 def VVVd1K(self, pts):
  try:
   InfoBar.instance.doSeek(int(pts))
  except:
   pass
  self.VVurqT("Changing Time ...")
 def VVFaKX(self):
  self.VVCt1U(1)
  self.VVurqT("Replaying ...")
  self.VV9LPF()
 def VVHjU5(self):
  try:
   seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
   if durVal > 0:
    pts = int((durVal - 10) * 90000.0)
    InfoBar.instance.doSeek(int(pts))
    self.VVurqT("Jumping to end ...")
  except:
   pass
 def VVWRgq(self):
  try:
   service = self.session.nav.getCurrentService()
   info = service and service.info()
   if info:
    val = info.getInfo(iServiceInformation.sBuffer)
    if val and val > 0 and not val == 100:
     return "Buffering %d %%" % val
  except:
   pass
  return ""
 def VVkgDG(self, isUp):
  if self.enableZapping:
   self.VVurqT("Zap %s ..." % ("Up" if isUp else "Down"))
   self.VV9LPF()
   if self.iptvTableParams:
    FFpoMu(BF(self.VVO3u5, isUp))
   else:
    refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
    if "/timeshift/" in decodedUrl:
     self.VVurqT("Cannot Zap Catch-up TV")
    else:
     try:
      if isUp : InfoBar.instance.zapDown()
      else : InfoBar.instance.zapUp()
     except:
      pass
     self.VVEagA()
  else:
   self.VVurqT("Zap Disabled !")
 def VVEagA(self):
  self.lastPlayPos = 0
  self.VVQagz()
  self.VVNjTE()
 def VVO3u5(self, isUp):
  CCqQHV_inatance, VVcpnp, mode = self.iptvTableParams
  if isUp : VVcpnp.VVXn2S()
  else : VVcpnp.VVnk2g()
  colList = VVcpnp.VVPxSj()
  if mode == "localIptv":
   chName, chUrl = CCqQHV_inatance.VVv2QK(VVcpnp, colList)
  elif mode == "m3u/m3u8":
   chName, chUrl = CCqQHV_inatance.VVLprB(VVcpnp, colList)
  elif isinstance(mode, int):
   chName, chUrl = CCqQHV_inatance.VVSKoe(mode, VVcpnp, colList)
  elif any(x in mode for x in ("itv", "vod", "series")):
   chName, chUrl = CCqQHV_inatance.VVJOnF(mode, VVcpnp, colList)
  else:
   self.VVurqT("Cannot Zap")
   return
  FFJZ42(self, chUrl, VVpyjK=False)
  self.VVEagA()
 def VVNjTE(self, forceRefresh=False):
  try:
   if not forceRefresh:
    seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
    if posTxt:
     return
   refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
   if not self.VVdEw9(refCode, chName, decodedUrl, iptvRef):
    return
   self.VVurqT("Refreshing Portal")
   FFpoMu(self.VVg0ti)
  except:
   pass
 def VVg0ti(self):
  self.restoreLastPlayPos = self.VVQp2W()
 def VVMLqk(self):
  refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
  if not decodedUrl or FFeC5o(decodedUrl):
   self.VVurqT("Not a Catchup TV")
   return
  qUrl = streamId = ""
  ok_fnc = None
  if not "&end=" in decodedUrl:
   if "/timeshift/" in decodedUrl:
    span = iSearch(r"(.+)\/timeshift\/(.+)\/(.+)\/(.+)\/(.+)\/(.+)[.]+", decodedUrl, IGNORECASE)
    if span:
     uHost, uUser, uPass = span.group(1), span.group(2), span.group(3)
     qUrl = "%s/player_api.php?username=%s&password=%s" % (uHost, uUser, uPass)
     streamId = span.group(6)
     ndx = chName.find(" >> ")
     if ndx > -1:
      chName = chName[:ndx]
   else:
    uType, uHost, uUser, uPass, uId, uChName = CCqQHV.VVPus3(decodedUrl)
    if all([uHost, uUser, uPass, uId]):
     streamId = uId
     qUrl = "%s/player_api.php?username=%s&password=%s" % (uHost, uUser, uPass)
  if qUrl:
   self.VVurqT("Reading Program List ...")
   ok_fnc = BF(self.VVKTLl, refCode, chName, streamId, uHost, uUser, uPass)
   FFpoMu(BF(CCqQHV.VV44HD, self, qUrl, chName, streamId, ok_fnc))
  else:
   self.VVurqT("Cannot process this channel")
 def VVKTLl(self, refCode, chName, streamId, uHost, uUser, uPass, VVcpnp, title, txt, colList):
  pTitle = colList[3]
  sTime = colList[5]
  dur  = colList[7]
  VVcpnp.cancel()
  span = iSearch(r"(\d{4}-\d{2}-\d{2})\s(\d{2}):(\d{2})", sTime, IGNORECASE)
  if span:
   sTime = span.group(1) + ":" + span.group(2) + "-" + span.group(3)
   chUrl = "%s/timeshift/%s/%s/%s/%s/%s.ts" % (uHost, uUser, uPass, dur, sTime, streamId)
   chUrl = chUrl.replace(":", "%3a")
   chUrl = "%s:%s:%s >> %s" % (refCode, chUrl, chName, pTitle)
   self.VVurqT("Changing Program ...")
   FFpoMu(BF(self.VVUc7k, chUrl))
  else:
   self.VVurqT("Incorrect Timestamp !")
 def VVUc7k(self, chUrl):
  FFJZ42(self, chUrl, VVpyjK=False)
  self.lastPlayPos = 0
  self.VVQagz()
 def VVmyur(self, isAudio):
  try:
   VVurhM = InfoBar.instance
   if VVurhM:
    from Screens.AudioSelection import AudioSelection, SubtitleSelection
    if isAudio : self.session.open(AudioSelection, infobar=VVurhM)
    else  : self.session.open(SubtitleSelection, VVurhM)
  except:
   pass
 @staticmethod
 def VVXG94(session, mode=None):
  if   mode == "close_sig"   : FF5FGP(session, reopen=True)
  elif mode == "close_iptvMenu"  : session.open(CCqQHV)
  elif mode == "close_openInFileMan" : session.open(CC7ujK, gotoMovie=True)
 @staticmethod
 def VVgElN(session, isFromExternal=False, **kwargs):
  session.openWithCallback(BF(CCppdx.VVXG94, session), CCppdx, isFromExternal=isFromExternal, **kwargs)
class CCQcnd(Screen):
 def __init__(self, session, title="", VVSidL="Continue?", VVr8hX=True, VVUEfx=False):
  self.skin, self.skinParam = FF896P(VVEgON, 1200, 800, 50, 20, 20, "#11221122", "#11221122", 30)
  self.session = session
  self["myLine"] = Label()
  self.VVSidL = VVSidL
  self.VVUEfx = VVUEfx
  self.maxHeight = 0
  no  = ("No" , "no" )
  yes = ("Yes", "yes")
  if VVr8hX : VV625J = [no , yes]
  else   : VV625J = [yes, no ]
  FFJd2Z(self, title, VV625J=VV625J, addLabel=True)
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : self.VVmz9T ,
   "cancel" : self.cancel ,
   "red"  : self.cancel ,
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self.maxHeight = self.instance.size().height()
  self["myLabel"].setText("\n%s\n" % self.VVSidL)
  if self.VVUEfx:
   self["myLabel"].instance.setHAlign(0)
  self.VV0vh6()
  FFkCFB(self["myMenu"], fg="#08ffff00", bg="#08223333")
  FFSEzt(self["myMenu"])
  FFjs4z(self, self["myMenu"])
 def VVmz9T(self):
  item = FF1N9D(self, False)
  if item is not None:
   if   item == "no" : self.close(False)
   elif item == "yes" : self.close(True)
  else:
   self.close(False)
 def cancel(self):
  self.close(False)
 def VV0vh6(self):
  winW  = self.instance.size().width()
  winH  = self.instance.size().height()
  labelW  = self["myLabel"].instance.size().width()
  labelH  = self["myLabel"].instance.size().height()
  textSize = self["myLabel"].instance.calculateSize()
  textW  = textSize.width()
  textH  = textSize.height()
  diff  = textH - labelH
  winNewH  = winH + diff
  if winNewH < winH:
   screenSize = getDesktop(0).size()
   self["myLabel"].instance.resize(eSize(*(labelW, labelH + diff)))
   self.instance.resize(eSize(*(winW, winNewH)))
   self.instance.move(ePoint((screenSize.width() - winW) // 2, (screenSize.height() - winNewH) // 2))
   names = [ "myMenu", "myLine" ]
   for name in names:
    try:
     obj = self[name]
     pos = obj.getPosition()
     obj.instance.move(ePoint(pos[0], pos[1] + diff))
    except:
     pass
class CC7aOd(Screen):
 def __init__(self, session, title="", VV625J=None, width=1000, height=0, VVmp7B=30, barText="", minRows=1, OKBtnFnc=None, VVBfJP=None, VVmKbI=None, VVJ5GS=None, VVme6L=None, VVeYEo=False, VVvQ6U=False, VVz2kc="#22003344", VVwpZm="#22002233"):
  if height == 0: height = 850
  self.skin, self.skinParam = FF896P(VVoxS0, width, height, 50, 40, 30, VVz2kc, VVwpZm, VVmp7B, barHeight=40)
  self.session   = session
  self.VV625J   = VV625J
  self.barText   = barText
  self.minRows   = minRows
  self.OKBtnFnc   = OKBtnFnc
  self.VVBfJP   = VVBfJP
  self.VVmKbI  = VVmKbI
  self.VVJ5GS  = VVJ5GS
  self.VVme6L   = VVme6L
  self.VVeYEo  = VVeYEo
  self.VVvQ6U  = VVvQ6U
  FFJd2Z(self, title, VV625J=VV625J)
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : self.VVmz9T          ,
   "cancel" : self.cancel          ,
   "red"  : self.VVjoi6         ,
   "green"  : self.VV58dG         ,
   "yellow" : self.VVBVsl         ,
   "blue"  : self.VVGXfP         ,
   "pageUp" : self.VV1gOl       ,
   "chanUp" : self.VV1gOl       ,
   "pageDown" : self.VVYasy        ,
   "chanDown" : self.VVYasy
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFkCFB(self["myMenu"])
  FF4FP6(self, minRows=self.minRows)
  self.VVNRXz(self["keyRed"]  , self.VVBfJP )
  self.VVNRXz(self["keyGreen"] , self.VVmKbI )
  self.VVNRXz(self["keyYellow"] , self.VVJ5GS )
  self.VVNRXz(self["keyBlue"]  , self.VVme6L )
  if self.barText      : self["myBar"].setText("  %s" % self.barText)
  elif not self["keyRed"].getVisible(): self["myBar"].setText("  OK = Select")
  else        : self["myBar"].setText("")
  FFtIlI(self)
 def VVNRXz(self, btnObj, btnFnc):
  if btnFnc:
   FFHhgX(btnObj, btnFnc[0])
 def VVHNuG(self, fnc=None):
  self.VVmKbI = fnc
  if fnc : self.VVNRXz(self["keyGreen"], self.VVmKbI)
  else : self["keyGreen"].hide()
 def VVmz9T(self):
  item = FF1N9D(self, False)
  if item is not None:
   txt = self["myMenu"].l.getCurrentSelection()[0]
   ref = self["myMenu"].l.getCurrentSelection()[1]
   ndx = self["myMenu"].l.getCurrentSelectionIndex()
   if self.OKBtnFnc:
    self.OKBtnFnc((self, txt, ref, ndx))
   else:
    if self.VVeYEo: self.close((txt, ref, ndx))
    else     : self.close(item)
 def cancel(self):
  self.close(None)
 def VVjoi6(self)  : self.VVoBtm(self.VVBfJP)
 def VV58dG(self) : self.VVoBtm(self.VVmKbI)
 def VVBVsl(self) : self.VVoBtm(self.VVJ5GS)
 def VVGXfP(self) : self.VVoBtm(self.VVme6L)
 def VVoBtm(self, btnFnc):
  if btnFnc:
   item = FF1N9D(self, False)
   fnc = btnFnc[1]
   fnc(self, item)
   if self.VVvQ6U:
    self.cancel()
 def VVVDex(self):
  ndx = self["myMenu"].getSelectedIndex()
  VV625J = self["myMenu"].list
  VV625J.pop(ndx)
  if len(VV625J) > 0: self["myMenu"].setList(VV625J)
  else    : self.close()
 def VVIzx9(self, VV625J):
  if len(VV625J) > 0:
   newList = []
   for item in VV625J:
    newList.append((item, item))
   self["myMenu"].setList(newList)
   FF4FP6(self, minRows=self.minRows)
  else:
   self.close("")
 def VVssYC(self, newRow, isSort=False):
  lst = self["myMenu"].list
  lst.append(newRow)
  if isSort:
   lst.sort(key=lambda x: x[0].lower())
  self["myMenu"].setList(lst)
  FF4FP6(self, minRows=self.minRows)
  for ndx, item in enumerate(self["myMenu"].list):
   if item[1] == newRow[1]:
    self["myMenu"].moveToIndex(ndx)
    break
 def VValrG(self, isUp):
  ndx = self["myMenu"].getSelectionIndex()
  if   isUp and ndx > 0         : newIndex = ndx - 1
  elif not isUp and ndx < len(self["myMenu"].list) - 1 : newIndex = ndx + 1
  else             : return None
  newList = self["myMenu"].list
  newList.insert(newIndex, newList.pop(ndx))
  self["myMenu"].moveToIndex(newIndex)
  newList = []
  for item in self["myMenu"].list:
   newList.append(item[0])
  return newList
 def VV1gOl(self):
  self["myMenu"].moveToIndex(0)
 def VVYasy(self) :
  self["myMenu"].moveToIndex(len(self["myMenu"].list) - 1)
class CCgB5a(Screen):
 def __init__(self, session, title="", width=1600, height=900, header=None, VVvytR=None, VVQqg2=None, VVoJsQ=None, VVmp7B=26, VVKNen=False, VVaq0k=0, VVVHmY=None, VV01dN=None, VVMQj9=None, VV3th8=None, VVOtSO=None, VV1QO7=None, VVWlvi=None, VVKx4L=None, VVfPgM=None, VV8dGa=-1, VVX8bj=False, searchCol=0, lastFindConfigObj=None, VVz2kc=None, VVwpZm=None, VVwuy7="#00dddddd", VVghPi="#11002233", VVAfLs="#00ff8833", VV0g1U="#11111111", VVooYw="#0a555555", VVkcOa="#0affffff", VVPVU2="#11552200", VV1H0Q="#0055ff55"):
  self.skin, self.skinParam = FF896P(VV7ebZ, width, height, 50, 10, 5, "#22003344", "#22002233", 26, barHeight=40, topRightBtns=2, lineGap=0.6)
  self.session    = session
  FFJd2Z(self, title)
  self.Title     = title
  self.header     = header
  self.VVvytR     = VVvytR
  self.totalCols    = len(VVvytR[0])
  self.VVaq0k   = VVaq0k
  self.lastSortModeIsReverese = False
  self.VVKNen   = VVKNen
  self.VVkEx1   = 0.01
  self.VVi6T1   = 0.02
  self.VVMWn0 = 0.03
  self.VV0MHs  = 1
  self.VVoJsQ = VVoJsQ
  self.colWidthPixels   = []
  self.VVVHmY   = VVVHmY
  self.OKButtonObj   = None
  self.VV01dN   = VV01dN
  self.VVMQj9   = VVMQj9
  self.VV3th8   = VV3th8
  self.VVOtSO  = VVOtSO
  self.VV1QO7   = VV1QO7
  self.VVWlvi    = VVWlvi
  self.VVKx4L   = VVKx4L
  self.tableRefreshCB   = None
  self.VVfPgM  = VVfPgM
  self.VV8dGa    = VV8dGa
  self.VVX8bj   = VVX8bj
  self.searchCol    = searchCol
  self.VVQqg2    = VVQqg2
  self.keyPressed    = -1
  self.VVmp7B    = FFWyds(VVmp7B)
  self.VVyhPB    = FFiz2E(self.VVmp7B, self.skinParam["lineGap"])
  self.scrollBarWidth   = self.skinParam["scrollBarW"]
  self.VVz2kc    = VVz2kc
  self.VVwpZm      = VVwpZm
  self.VVwuy7    = FFZG1G(VVwuy7)
  self.VVghPi    = FFZG1G(VVghPi)
  self.VVAfLs    = FFZG1G(VVAfLs)
  self.VV0g1U    = FFZG1G(VV0g1U)
  self.VVooYw   = FFZG1G(VVooYw)
  self.VVkcOa    = FFZG1G(VVkcOa)
  self.VVPVU2    = FFZG1G(VVPVU2)
  self.VV1H0Q   = FFZG1G(VV1H0Q)
  self.VVbl0M  = False
  self.selectedItems   = 0
  self.VV1lkx   = FFZG1G("#01fefe01")
  self.VVRMsl   = FFZG1G("#11400040")
  self.VVxc9J  = self.VV1lkx
  self.VVqrA4  = self.VV0g1U
  self.lastFindConfigObj  = lastFindConfigObj or CFG.lastFindGeneral
  if self.VVX8bj:
   self["keyMenu"].hide()
   self["keyInfo"].hide()
   self["myBar"].setText("  OK = Row Info.")
  self["myTableH"] = MenuList([], True, eListboxPythonMultiContent)
  self["myTable"]  = MenuList([], True, eListboxPythonMultiContent)
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : self.VVZcpp  ,
   "red"   : self.VV994P  ,
   "green"   : self.VVuYZh ,
   "yellow"  : self.VVIrDY ,
   "blue"   : self.VVArNd  ,
   "menu"   : self.VVn4it ,
   "info"   : self.VVuyDj  ,
   "cancel"  : self.VVoTrf  ,
   "up"   : self.VVnk2g    ,
   "down"   : self.VVXn2S  ,
   "left"   : self.VVvT7h   ,
   "right"   : self.VVF7h6  ,
   "next"   : self.VV5cQr  ,
   "last"   : self.VVUBLy  ,
   "home"   : self.VVuohM  ,
   "pageUp"  : self.VVuohM  ,
   "chanUp"  : self.VVuohM  ,
   "end"   : self.VVIdSv  ,
   "pageDown"  : self.VVIdSv  ,
   "chanDown"  : self.VVIdSv
  }, -1)
  FFCMLR(self, self["myTable"], self.searchCol)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FF4Pls(self)
  try:
   self.VVK3mT()
  except Exception as err:
   FFkYsE(self, str(err), title=self.Title)
   self.close(None)
 def VVK3mT(self):
  FFtIlI(self)
  if self.VVz2kc:
   FFobAA(self["myTitle"], self.VVz2kc)
  if self.VVwpZm:
   FFobAA(self["myBody"] , self.VVwpZm)
   FFobAA(self["myTableH"] , self.VVwpZm)
   FFobAA(self["myTable"] , self.VVwpZm)
   FFobAA(self["myBar"]  , self.VVwpZm)
  self.VVNRXz(self.VVMQj9  , self["keyRed"])
  self.VVNRXz(self.VV3th8  , self["keyGreen"])
  self.VVNRXz(self.VVOtSO , self["keyYellow"])
  self.VVNRXz(self.VV1QO7  , self["keyBlue"])
  if self.VVVHmY:
   if   not self["keyRed"].getVisible() : self.OKButtonObj = self["keyRed"]
   elif not self["keyBlue"].getVisible() : self.OKButtonObj = self["keyBlue"]
   else         : self.OKButtonObj = None
   if self.OKButtonObj:
    self.OKButtonObj.show()
    self.OKButtonObj.setText("OK = %s" % self.VVVHmY[0])
    FFobAA(self.OKButtonObj, "#11000000")
  self["myTableH"].l.setSelectionClip(eRect(0, 0, 0, 0))
  self["myTable"].l.setSelectionClip(eRect(0, 0, 0, 0))
  self["myTableH"].l.setItemHeight(self.VVyhPB)
  self["myTableH"].l.setFont(0, gFont(VVFwML, self.VVmp7B))
  self["myTable"].l.setItemHeight(self.VVyhPB)
  self["myTable"].l.setFont(0, gFont(VVFwML, self.VVmp7B))
  try:
   self["myTable"].instance.setScrollbarSliderBorderWidth(0)
  except:
   pass
  w  = self["myTable"].instance.size().width()
  h  = self["myTable"].instance.size().height()
  pos  = self["myTable"].getPosition()
  if self.header:
   self["myTableH"].instance.resize(eSize(*(w, self.VVyhPB)))
   self["myTable"].instance.move(ePoint(pos[0], pos[1] + self.VVyhPB))
   self["myTable"].instance.resize(eSize(*(w, h - self.VVyhPB)))
  h  = self["myTable"].instance.size().height()
  pos  = self["myTable"].getPosition()
  part = self["myTable"].instance.size().height() % self.VVyhPB
  half = int(part / 2)
  self["myTable"].instance.resize(eSize(*(w, h - part)))
  self["myTable"].instance.move(ePoint(pos[0], pos[1] + half))
  if self.header:
   pos = self["myTableH"].getPosition()
   self["myTableH"].instance.move(ePoint(pos[0], pos[1] + half))
  menuWidth = self["myTable"].instance.size().width()
  if self.VVyhPB * len(self.VVvytR) > self["myTable"].instance.size().height():
   menuWidth = menuWidth - int(self.scrollBarWidth) - 5
  if not self.VVoJsQ:
   self.VVoJsQ = ([float(100.0 / self.totalCols)] * self.totalCols)
  self.colWidthPixels = list(self.VVoJsQ)
  if not self.colWidthPixels:
   self.colWidthPixels = int([menuWidth / self.totalCols] * self.totalCols)
  else:
   for i, item in enumerate(self.colWidthPixels):
    self.colWidthPixels[i] = int(item * menuWidth / 100)
  if not self.VVQqg2:
   self.VVQqg2 = [LEFT | RT_VALIGN_CENTER] * self.totalCols
  else:
   tmpList = self.VVQqg2
   self.VVQqg2 = []
   for item in tmpList:
    self.VVQqg2.append(item | RT_VALIGN_CENTER)
  self.VVIJX7()
  if self.VVWlvi:
   self.VVWlvi(self)
 def VVNRXz(self, btnFnc, btn):
  if btnFnc : FFHhgX(btn, btnFnc[0])
  else  : FFHhgX(btn, "")
 def VVonmQ(self, waitTxt):
  FFlX3B(self, self.VVIJX7, title=waitTxt)
 def VVIJX7(self, onlyHeader=False):
  try:
   if self.header:
    self["myTableH"].setList([self.VV0AwH(0, self.header, self.VVkcOa, self.VVPVU2, self.VVkcOa, self.VVPVU2, self.VV1H0Q)])
   if onlyHeader:
    return
   self["myTable"].list = []
   for c, row in enumerate(self.VVvytR):
    self["myTable"].list.append(self.VV0AwH(c, row, self.VVwuy7, self.VVghPi, self.VVAfLs, self.VV0g1U, None))
   self.VVvytR = []
   self["myTable"].setList(self["myTable"].list)
   if self.VV8dGa > -1:
    self["myTable"].moveToIndex(self.VV8dGa )
   self.VV32dH()
   if self.VVX8bj:
    tableH = self["myTable"].instance.size().height()
    rowsH = self.VVyhPB * len(self["myTable"].list)
    if rowsH < tableH:
     diff = tableH - rowsH
     newH = self.instance.size().height() - diff
     screenSize = getDesktop(0).size()
     width = self.instance.size().width()
     self.instance.resize(eSize(*(width, newH)))
     self.instance.move(ePoint((screenSize.width() - width) // 2, (screenSize.height() - newH) // 2))
     names = [ "keyRed", "keyGreen", "keyYellow", "keyBlue", "myBar", "myLine" ]
     for name in names:
      obj = self[name]
      pos = obj.getPosition()
      obj.instance.move(ePoint(pos[0], pos[1] - diff))
   if self.VVKx4L:
    self.VVoBtm(self.VVKx4L, None)
   if self.tableRefreshCB:
    self.VVoBtm(self.tableRefreshCB, None)
    self.tableRefreshCB = None
  except AttributeError as attrErr:
   pass
  except Exception as err:
   try:
    FFkYsE(self, str(err), title=self.Title)
    self.close()
   except:
    pass
 def VV0AwH(self, keyIndex, columns, VVwuy7, VVghPi, VVAfLs, VV0g1U, VV1H0Q):
  row = [keyIndex]
  posX = 0
  for ndx, entry in enumerate(columns):
   if VV1H0Q and ndx == self.VVaq0k : textColor = VV1H0Q
   else           : textColor = VVwuy7
   span = iSearch(r"\s*#(.)(#[a-fA-F0-9]{8})#(.*)", entry, IGNORECASE)
   if span:
    c = FFZG1G(span.group(2))
    if span.group(1) == "f" : textColor = c
    else     : VVghPi = c
    entry = span.group(3)
   if self.VVQqg2[ndx] & LEFT:
    entry = " " + entry + " "
   row.append(MultiContentEntryText( pos   = (posX, 0)
           , size   = (self.colWidthPixels[ndx], self.VVyhPB)
           , font   = 0
           , flags   = self.VVQqg2[ndx]
           , text   = entry
           , color   = textColor
           , backcolor  = VVghPi
           , color_sel  = VVAfLs
           , backcolor_sel = VV0g1U
           , border_width = 1
           , border_color = self.VVooYw
           ))
   posX += self.colWidthPixels[ndx]
  return row
 def VVuyDj(self):
  rowData = self.VVpest()
  if rowData:
   title, txt, colList = rowData
   if self.VV01dN:
    fnc  = self.VV01dN[1]
    params = self.VV01dN[2]
    fnc(self, title, txt, colList)
   else:
    FFNEkd(self, txt, title)
 def VVZcpp(self):
  if   self.VVbl0M : self.VVzfA3(self.VVgrGB(), mode=2)
  elif self.VVVHmY  : self.VVoBtm(self.VVVHmY, None)
  else      : self.VVuyDj()
 def VV994P(self) : self.VVoBtm(self.VVMQj9 , self["keyRed"])
 def VVuYZh(self) : self.VVoBtm(self.VV3th8 , self["keyGreen"])
 def VVIrDY(self): self.VVoBtm(self.VVOtSO , self["keyYellow"])
 def VVArNd(self) : self.VVoBtm(self.VV1QO7 , self["keyBlue"])
 def VVoBtm(self, buttonFnc, btnObj):
  if btnObj and not btnObj.getVisible():
   return
  if buttonFnc:
   if len(buttonFnc) > 3 and buttonFnc[3]:
    FFD1yO(self, buttonFnc[3])
    FFpoMu(BF(self.VVncfU, buttonFnc))
   else:
    self.VVncfU(buttonFnc)
 def VVncfU(self, buttonFnc):
  fnc   = buttonFnc[1]
  params  = buttonFnc[2]
  rowData = self.VVpest()
  if rowData:
   title, txt, colList = rowData
   if not params : fnc(self, title, txt, colList)
   else   : fnc(self, *params)
 def VVzfA3(self, ndx, mode=0):
  try:  row = self["myTable"].list[ndx]
  except: row = None
  if row:
   isSelected = row[1][9] == self.VV1lkx
   newRow = self.VVPxSj()
   if mode == 0 or (mode == 2 and isSelected):
    newRow = self.VV0AwH(ndx, newRow, self.VVwuy7, self.VVghPi, self.VVAfLs, self.VV0g1U, None)
    if isSelected:
     self.selectedItems -= 1
   else:
    newRow = self.VV0AwH(ndx, newRow, self.VV1lkx, self.VVRMsl, self.VVxc9J, self.VVqrA4, None)
    self.selectedItems += 1
   self["myTable"].list.pop(ndx)
   self["myTable"].list.insert(ndx, newRow)
   if self.VVgrGB() < len(self["myTable"].list) - 1:
    self.VVXn2S()
   else:
    self.VV32dH()
 def VV1gPk(self)  : FFlX3B(self, BF(self.VVcHiw, True ), title="Selecting all ..."  )
 def VVNp4C(self) : FFlX3B(self, BF(self.VVcHiw, False), title="Unselecting all ...")
 def VVcHiw(self, isSel=True):
  if isSel:
   fg, bg = self.VV1lkx, self.VVRMsl
   self.selectedItems = len(self["myTable"].list)
   self.VVBOaN(True)
  else:
   fg, bg = self.VVwuy7, self.VVghPi
   self.selectedItems = 0
  for ndx, row in enumerate(self["myTable"].list):
   isPainted = row[1][9] == self.VV1lkx
   if (isSel and not isPainted) or (not isSel and isPainted):
    for col in range(1, len(row)):
     param = list(self["myTable"].list[ndx][col])
     param[8]  = fg
     param[9]  = fg
     param[10] = bg
     self["myTable"].list[ndx][col] = tuple(param)
  self["myTable"].l.invalidate()
 def VVpest(self):
  item = self["myTable"].getCurrent()
  if item:
   colList = []
   txt  = ""
   tot  = 0
   for i in range(self.totalCols):
    colTxt = item[i + 1][7].strip()
    colList.append(colTxt)
    if self.VVoJsQ[i] > 1 or self.VVoJsQ[i] == self.VVkEx1 or self.VVoJsQ[i] == self.VVMWn0:
     tot += 1
     if self.header : name = self.header[i]
     else   : name = "Column-%d" % (i + 1)
     txt += "%s\t: %s\n" % (name, colTxt)
   if tot == 1:
    txt = colList[0]
   rowNum = "Row Number\t: %d of %d" % (item[0] + 1, len(self["myTable"].list))
   return rowNum, txt, colList
  else:
   return None
 def VVoTrf(self):
  if self.VVfPgM : self.VVfPgM(self)
  else     : self.close(None)
 def cancel(self):
  self["myTable"].onSelectionChanged = []
  self.close(None)
 def VVmgxl(self):
  return self["myTitle"].getText().strip()
 def VVixmS(self):
  return self.header
 def VVX6S3(self, title):
  self.Title = title
  self["myTitle"].setText("  " + title.strip() + "  ")
 def VVhl6o(self, title, color=None):
  self["myBar"].setText("  " + title.strip() + "  ")
  if color:
   FFlr8P(self["myBar"], color)
 def VVphEN(self, txt):
  FFD1yO(self, txt)
 def VVIX8q(self, txt, Time=1000):
  FFD1yO(self, txt, Time)
 def VV7TEw(self): self["keyGreen"].show()
 def VV0vgr(self): self["keyGreen"].hide()
 def VVhzNf(self):
  FFD1yO(self)
 def VViPb6(self, fnc):
  self["myTable"].onSelectionChanged.append(fnc)
 def VVHLLY(self):
  return len(self["myTable"].list)
 def VVgrGB(self):
  return self["myTable"].l.getCurrentSelectionIndex()
 def VVI1WG(self):
  return len(self["myTable"].list)
 def VVBOaN(self, isOn):
  self.VVbl0M = isOn
  if isOn:
   color = "#01883366"
   self["keyMenu"].hide()
   if self.VV1QO7: self["keyBlue"].hide()
   if self.VVVHmY and self.OKButtonObj: self.OKButtonObj.setText("OK = Select")
  else:
   color = self.skinParam["titleColor"]
   self["keyMenu"].show()
   if self.VV1QO7: self["keyBlue"].show()
   if self.VVVHmY and self.OKButtonObj: self.OKButtonObj.setText("OK = %s" % self.VVVHmY[0])
   self.VVNp4C()
  FFobAA(self["myTitle"], color)
  FFobAA(self["myBar"]  , color)
 def VVAzsT(self):
  return self.VVbl0M
 def VVMJsS(self):
  return self.selectedItems
 def VVabBl(self):
  curRow = self["myTable"].l.getCurrentSelectionIndex()
  self["myTable"].moveToIndex(curRow + 1)
  self.VV32dH()
 def VVAnII(self, colNum):
  if colNum < self.totalCols:
   if self.header : subj = self.header[colNum]
   else   : subj = ""
   lst = set()
   for item in self["myTable"].list:
    lst.add(item[colNum + 1][7])
   return subj, str(len(lst))
  else:
   return "", ""
 def VVcuSv(self):
  txt  = "Total Rows\t: %d\n\n" % self.VVHLLY()
  txt += FFINY2("Total Unique Items", VVU8eD)
  for i in range(self.totalCols):
   if self.VVoJsQ[i - 1] > 1 or self.VVoJsQ[i - 1] == self.VVkEx1 or self.VVoJsQ[i - 1] == self.VVMWn0:
    name, tot = self.VVAnII(i)
    txt +=  "%s\t: %s\n" % (name, tot)
  FFNEkd(self, txt)
 def VVQYAy(self, colNum):
  item = self["myTable"].getCurrent()
  if item : return item[colNum + 1][7].strip()
  else : return None
 def VVPxSj(self):
  return self.VVauPE(self["myTable"].l.getCurrentSelectionIndex())
 def VVauPE(self, rowNdx):
  colList = []
  item = self["myTable"].list[rowNdx]
  if item:
   for i in range(1, self.totalCols + 1):
    colList.append(item[i][7].strip())
  return colList
 def VVuVux(self, newList, newTitle="", VVP2KcMsg=True, tableRefreshCB=None):
  if newTitle:
   self.VVX6S3(newTitle)
  if newList:
   self.VVvytR = newList
   if tableRefreshCB:
    self.tableRefreshCB = ("", tableRefreshCB, [])
   isNum = False
   if self.VVKNen and self.VVaq0k == 0:
    isNum = True
   else:
    for cols in self.VVvytR:
     if not FFlKzi(cols[self.VVaq0k]): break
    else:
     isNum = True
   if isNum: self.VVvytR.sort(key=lambda x: int(x[self.VVaq0k])  , reverse=self.lastSortModeIsReverese)
   else : self.VVvytR.sort(key=lambda x: x[self.VVaq0k].lower() , reverse=self.lastSortModeIsReverese)
   if VVP2KcMsg : self.VVonmQ("Refreshing ...")
   else   : self.VVIJX7()
  else:
   FFkYsE(self, "Cannot refresh list", title=self.Title)
   self.cancel()
 def VVc4hA(self, row, moveCurs=True):
  row = self["myTable"].list.append(self.VV0AwH(self.VVI1WG(), row, self.VVwuy7, self.VVghPi, self.VVAfLs, self.VV0g1U, None))
  self["myTable"].l.setList(self["myTable"].list)
  if moveCurs: self.VVIdSv()
 def VVmxfU(self):
  self["myTable"].list.pop(self.VVgrGB())
  self["myTable"].l.setList(self["myTable"].list)
 def VVzOfF(self, data):
  ndx = self.VVgrGB()
  newRow = self.VV0AwH(ndx, data, self.VVwuy7, self.VVghPi, self.VVAfLs, self.VV0g1U, None)
  if newRow:
   self["myTable"].list[ndx] = newRow
   self.VV32dH()
   return True
  else:
   return False
 def VVubDz(self, colNum=0):
  for ndx, item in enumerate(self["myTable"].list):
   lst = list(self["myTable"].list[ndx][colNum + 1])
   lst[7] = str(ndx + 1)
   self["myTable"].list[ndx][colNum + 1] = tuple(lst)
  self["myTable"].l.setList(self["myTable"].list)
 def VV8yro(self, colNum, textToFind, VVl2X5=False):
  for i in range(len(self["myTable"].list)):
   item = self["myTable"].list[i][colNum + 1][7].strip()
   if textToFind in item:
    self["myTable"].moveToIndex(i)
    self.VV32dH()
    break
  else:
   if VVl2X5:
    FFD1yO(self, "Not found", 1000)
 def VV98P0(self, colDict, VVl2X5=False):
  length = len(colDict)
  for i in range(len(self["myTable"].list)):
   for colNum, txt in list(colDict.items()):
    if not txt == self["myTable"].list[i][colNum + 1][7].strip():
     break
   else:
    self["myTable"].moveToIndex(i)
    self.VV32dH()
    return
  if VVl2X5:
   FFD1yO(self, "Not found", 1000)
 def VV6T0n(self, colNum):
  tList = []
  for i in range(len(self["myTable"].list)):
   item = self["myTable"].list[i][colNum + 1][7].strip()
   tList.append(item)
  return tList
 def VVcH2C(self, colNum):
  for i in range(len(self["myTable"].list)):
   if not FFlKzi(self["myTable"].list[i][colNum + 1][7].strip()):
    return False
  return True
 def VVT6RH(self, colNum):
  tList = []
  for ndx, row in enumerate(self["myTable"].list):
   if row[1][9] == self.VV1lkx:
    item = self["myTable"].list[ndx][colNum + 1][7].strip()
    tList.append(item)
  return tList
 def VVN5aQ(self):
  tList = []
  for ndx, row in enumerate(self["myTable"].list):
   if row[1][9] == self.VV1lkx:
    item = self["myTable"].list[ndx]
    colList = []
    for i in range(1, self.totalCols + 1):
     colList.append(item[i][7].strip())
    tList.append(colList)
  return tList
 def VV3fqU(self, colNum):
  row = self["myTable"].list[colNum]
  if row[1][9] == self.VV1lkx: return True
  else        : return False
 def VVGrbO(self):
  for ndx, row in enumerate(self["myTable"].list):
   item = self["myTable"].list[ndx]
   colList = []
   for i in range(1, self.totalCols + 1):
    colTxt = item[i][7].strip()
    colList.append(colTxt)
   yield colList
 def VVn4it(self):
  if not self["keyMenu"].getVisible() or self.VVX8bj:
   return
  txt  = self.lastFindConfigObj.getValue()
  curRow = self.VVgrGB()
  totRows = len(self["myTable"].list)
  itemOf = lambda cond, p1, p2: (p1, p2) if cond else (p1, )
  VV625J1, VVDMeF = CCU3qf.VVcpV6(self, False, False)
  VV625J = []
  VV625J.append(itemOf(txt and curRow < totRows - 1 , "Find Next\t\t>"     , "findNext"  ))
  VV625J.append(itemOf(txt and curRow > 0   , "Find Previous\t\t<"    , "findPrev"  ))
  VV625J.append(("Find ...\t\t%s" % (FFkhYI(txt, VVpHwQ) if txt else ""), "findNew"   ))
  VV625J.append(itemOf(bool(VV625J1)    , "Find (from Filter) ..."   , "filter"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Table Statistcis"             , "tableStat"  ))
  VV625J.append(VVm77t)
  VV625J.append((FFkhYI("Export Table to .html"     , VVU8eD) , "VVHk65" ))
  VV625J.append((FFkhYI("Export Table to .csv"     , VVU8eD) , "VVKRTB" ))
  VV625J.append((FFkhYI("Export Table to .txt (Tab Separated)", VVU8eD) , "VVs3mO" ))
  sList = []
  tot  = 0
  for i in range(self.totalCols):
   if self.VVoJsQ[i] > 1 or self.VVoJsQ[i] == self.VVi6T1:
    tot += 1
    if self.header : name = self.header[i]
    else   : name = "Column-%d" % (i + 1)
    sList.append(("Sort by : %s" % name, i))
  if tot:
   VV625J.append(VVm77t)
   if tot == 1 : VV625J.append(("Sort", sList[0][1]))
   else  : VV625J += sList
  VVme6L = ("Keys Help", self.FF1dQ4Help)
  FFuRfS(self, self.VVEWlN, VV625J=VV625J, title=self.VVmgxl(), VVme6L=VVme6L)
 def VVEWlN(self, item=None):
  if item is not None:
   title="Exporting ..."
   if   item == "findNext"  : self.VV85nm()
   elif item == "findPrev"  : self.VV85nm(isPrev=True)
   elif item == "findNew"  : self.VV2AjS()
   elif item == "filter"  : self.VVTF7P()
   elif item == "tableStat" : self.VVcuSv()
   elif item == "VVHk65": FFlX3B(self, self.VVHk65, title=title)
   elif item == "VVKRTB" : FFlX3B(self, self.VVKRTB , title=title)
   elif item == "VVs3mO" : FFlX3B(self, self.VVs3mO , title=title)
   else:
    self.lastSortModeIsReverese = False
    if self.VVaq0k == item: self.lastSortModeIsReverese = not self.lastSortModeIsReverese
    else      : self.VVaq0k = item
    if self.VVKNen and self.VVaq0k == 0 or self.VVcH2C(item):
     self["myTable"].list.sort(key=lambda x: int(x[item + 1][7]), reverse=self.lastSortModeIsReverese)
    else:
     self["myTable"].list.sort(key=lambda x: x[item + 1][7].lower(), reverse=self.lastSortModeIsReverese)
    self["myTable"].l.setList(self["myTable"].list)
    self.VVIJX7(onlyHeader=True)
 def FF1dQ4Help(self, menuInstance, path):
  FF7SvB(self, VVASCC + "_help_table", "Table (Keys Help)")
 def VVnk2g(self):
  self["myTable"].up()
  self.VV32dH()
 def VVXn2S(self):
  self["myTable"].down()
  self.VV32dH()
 def VVvT7h(self):
  self["myTable"].pageUp()
  self.VV32dH()
 def VVF7h6(self):
  self["myTable"].pageDown()
  self.VV32dH()
 def VVuohM(self):
  self["myTable"].moveToIndex(0)
  self.VV32dH()
 def VVIdSv(self):
  self["myTable"].moveToIndex(len(self["myTable"].list) - 1)
  self.VV32dH()
 def VVtpKN(self, rowNdx):
  self["myTable"].moveToIndex(rowNdx)
  self.VV32dH()
 def VV5cQr(self):
  if self.lastFindConfigObj.getValue():
   if self.VVgrGB() == len(self["myTable"].list) - 1 : FFD1yO(self, "End reached", 1000)
   else              : self.VV85nm()
  else:
   FFD1yO(self, 'Set "Find" in Menu', 1500)
 def VVUBLy(self):
  if self.lastFindConfigObj.getValue():
   if self.VVgrGB() == 0 : FFD1yO(self, "Top reached", 1000)
   else       : self.VV85nm(isPrev=True)
  else:
   FFD1yO(self, 'Set "Find" in Menu', 1500)
 def VVVCRb(self, txt):
  FFnT3A(self.lastFindConfigObj, txt)
 def VV2AjS(self):
  FFbRXK(self, self.VVwXTf, title="Find in Table", defaultText=self.lastFindConfigObj.getValue(), message="Enter Text:")
 def VVwXTf(self, VVVomg):
  if not VVVomg is None:
   txt = VVVomg.strip()
   self.VVVCRb(txt)
   if VVVomg: self.VV85nm(reset=True)
   else  : FFD1yO(self, "Nothing to find !", 1500)
 def VVTF7P(self):
  VV625J, VVDMeF = CCU3qf.VVcpV6(self, False, False)
  if VV625J : FFuRfS(self, self.VVQ4RH, VV625J=VV625J, title="Find from Filter")
  else  : FFD1yO(self, "Filter Error !", 1500)
 def VVQ4RH(self, item=None):
  if item is not None:
   txt = item.strip()
   if txt:
    self.VVVCRb(txt)
    self.VV85nm(reset=True)
   else:
    FFD1yO(self, "No entry !", 1500)
 def VV85nm(self, reset=False, isPrev=False):
  curRow = self.VVgrGB()
  totRows = len(self["myTable"].list)
  if   reset : row1, row2, steps = 0, totRows, 1
  elif isPrev : row1, row2, steps = curRow - 1, -1, -1
  else  : row1, row2, steps = curRow + 1, totRows, 1
  tupl, asPrefix = CCU3qf.VVP88C(self.lastFindConfigObj.getValue())
  if tupl:
   for i in range(row1, row2, steps):
    line = self["myTable"].list[i][self.searchCol + 1][7]
    line = line.strip().lower()
    if asPrefix:
     if line.startswith(tupl):
      self.VVtpKN(i)
      break
    elif any(x in line for x in tupl):
     self.VVtpKN(i)
     break
   else:
    FFD1yO(self, "Not found", 1000)
  else:
   FFD1yO(self, "Check your query", 1500)
 def VVs3mO(self):
  expFile = self.VVmURi() + ".txt"
  with open(expFile, "w") as f:
   filteredHeader = self.VVOctg()
   if filteredHeader:
    f.write("\t".join(filteredHeader) + "\n")
   for i in range(len(self["myTable"].list)):
    row = self.VVauPE(i)
    newRow = []
    for ndx, col in enumerate(row):
     if self.VVoJsQ[ndx] > self.VV0MHs or self.VVoJsQ[ndx] == self.VVMWn0:
      col = self.VV9OSl(col)
      col = col.replace("\n", " _ ")
      newRow.append(col)
    f.write("\t".join(newRow) + "\n")
  self.VVY4od(expFile)
 def VVKRTB(self):
  expFile = self.VVmURi() + ".csv"
  with open(expFile, "w") as f:
   filteredHeader = self.VVOctg()
   if filteredHeader:
    f.write(",".join(filteredHeader) + "\n")
   pattern = "^[0-9a-fA-F]*$"
   for i in range(len(self["myTable"].list)):
    row = self.VVauPE(i)
    newRow = []
    for ndx, col in enumerate(row):
     if self.VVoJsQ[ndx] > self.VV0MHs or self.VVoJsQ[ndx] == self.VVMWn0:
      if iMatch(pattern, col) : prefix = "'"
      else     : prefix = ""
      col = self.VV9OSl(col)
      col = col.replace(",", ";").replace("\n", " _ ")
      newRow.append(prefix + col)
    f.write(",".join(newRow) + "\n")
  self.VVY4od(expFile)
 def VVHk65(self):
  txt   = '<!DOCTYPE html>\n'
  txt  += '<html>\n'
  txt  += ' <head>\n'
  txt  += ' <meta charset="utf-8">\n'
  txt  += ' <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
  txt  += ' <TITLE>%s - %s (%s)</TITLE>\n' % (self.VVmgxl(), PLUGIN_NAME, VV73TT)
  txt  += ' <style>\n'
  txt  += '  table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; }\n'
  txt  += '  td,th { border: 1px solid #dddddd; text-align: left; padding: 5px; }\n'
  txt  += '  td { font-size: 0.8em; }\n'
  txt  += '  th { color:#006000; background-color:#FFFFaa; font-size: 1.2em; }\n'
  txt  += '  tr:nth-child(even) { background-color: #f8f8f8; }\n'
  txt  += ' </style>\n'
  txt  += ' </head>\n'
  txt  += ' <body>\n'
  txt  += '  <h2 style="color:#006000;">%s</h2>\n' % self.VVmgxl()
  txt  += '  <table>\n'
  txt  +=     '#colgroup#'
  txt  += '   <tr>#tableHead#</tr>\n'
  txt2  = '  <table>\n'
  txt2 += ' </body>\n'
  txt2 += '</html>\n'
  tableHead  = ""
  filteredHeader = self.VVOctg()
  if filteredHeader:
   for col in filteredHeader:
    tableHead += '<th>%s</th>' % col
  txt = txt.replace("#tableHead#", tableHead)
  colgroup = ""
  if self.VVoJsQ:
   colgroup += '   <colgroup>'
   for w in self.VVoJsQ:
    if w > self.VV0MHs or w == self.VVMWn0:
     colgroup += '<col style="width: %d%s;" />' % (w, "%")
   colgroup += "</colgroup>\n"
  txt = txt.replace("#colgroup#", colgroup)
  expFile = self.VVmURi() + ".html"
  with open(expFile, "w") as f:
   f.write(txt)
   for i in range(len(self["myTable"].list)):
    row = self.VVauPE(i)
    newRow = "   <tr>"
    for ndx, col in enumerate(row):
     if self.VVoJsQ[ndx] > self.VV0MHs or self.VVoJsQ[ndx] == self.VVMWn0:
      col = self.VV9OSl(col)
      newRow += '<td>%s</td>' % col
    newRow += "</tr>\n"
    f.write(newRow)
   f.write(txt2)
  self.VVY4od(expFile)
 def VVOctg(self):
  newRow = []
  if self.header:
   for ndx, col in enumerate(self.header):
    if self.VVoJsQ[ndx] > self.VV0MHs or self.VVoJsQ[ndx] == self.VVMWn0:
     newRow.append(col.strip())
  return newRow
 def VV9OSl(self, col):
  if col.count(":") > 8:
   col = col.replace(":", "_")
   col = col.rstrip("_")
  col = iSub(r"(#.#[a-fA-F0-9]{8}#)" ,"" , col, flags=IGNORECASE)
  return FFO8d5(col)
 def VVmURi(self):
  fileName = iSub("[^0-9a-zA-Z]+", "_", self.VVmgxl())
  fileName = fileName.replace("__", "_")
  path  = FF0WrY(CFG.exportedTablesPath.getValue())
  expFile  = path + fileName + "_" + FFGuM2()
  return expFile
 def VVY4od(self, expFile):
  FFewCE(self, "File exported to:\n\n%s" % expFile, title=self.VVmgxl())
 def VV32dH(self):
  row = self["myTable"].l.getCurrentSelection()
  if row:
   firstColumn = row[1]
   lastColumn = row[len(row) - 1]
   self["myTable"].l.setSelectionClip(eRect(int(firstColumn[1]), int(firstColumn[0]), int(lastColumn[1] + lastColumn[3]), int(lastColumn[4])), True)
   self["myTable"].l.setSelectionClip(eRect(int(firstColumn[1]), int(firstColumn[0]), int(lastColumn[1] + lastColumn[3]), int(lastColumn[4])), False)
class CCg2mT():
 def __init__(self, pixmapObj, picPath, VVghPi=None):
  from enigma import ePicLoad
  from Components.AVSwitch import AVSwitch
  self.picLoad  = ePicLoad()
  self.scale   = AVSwitch().getFramebufferScale()
  self.picload_conn = None
  self.pixmapObj  = pixmapObj
  self.picPath  = picPath
  self.VVghPi  = VVghPi or "#2200002a"
 def VVLett(self):
  if self.pixmapObj and self.picPath and fileExists(self.picPath):
   try:
    try:
     self.picload_conn = self.picLoad.PictureData.connect(self.VV9w0k)
    except:
     self.picLoad.PictureData.get().append(self.VV9w0k)
    size = self.pixmapObj.instance.size()
    self.picLoad.setPara([size.width(), size.height(), self.scale[0], self.scale[1], False, 1, self.VVghPi])
    self.picLoad.startDecode(self.picPath)
    return True
   except:
    pass
  return False
 def VV9w0k(self, pInfo=""):
  if self.picLoad and pInfo:
   ptr = self.picLoad.getData()
   if ptr != None:
    try:
     self.pixmapObj.instance.setPixmap(ptr)
    except:
     pass
 def VVq3PH(self):
  del self.picLoad
  self.picLoad = None
  self.picload_conn = None
 @staticmethod
 def VVjTx0(pixmapObj, path, VVghPi=None):
  cl = CCg2mT(pixmapObj, path, VVghPi)
  ok = cl.VVLett()
  if ok: return cl
  else : return None
class CCd1mn(Screen):
 def __init__(self, session, title="", VVHEnC=None, showGrnMsg=""):
  self.skin, self.skinParam = FF896P(VVCyHa, 1400, 800, 30, 40, 20, "#22000060", "#2200002a", 30)
  if not title:
   title = os.path.basename(VVHEnC),
  self.session = session
  FFJd2Z(self, title, addCloser=True)
  self["myPic"]  = Pixmap()
  self.VVHEnC = VVHEnC
  self.showGrnMsg  = showGrnMsg
  self.picViewer  = None
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.onExit)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self.picViewer = CCg2mT.VVjTx0(self["myPic"], self.VVHEnC)
  if self.picViewer:
   if self.showGrnMsg:
    FFD1yO(self, self.showGrnMsg, 1000, isGrn=True)
  else:
   FFkYsE(self, "Cannot view picture file:\n\n%s" % self.VVHEnC)
   self.close()
 def onExit(self):
  if self.picViewer:
   self.picViewer.VVq3PH()
 @staticmethod
 def VVQ7Bd(SELF, VVHEnC, title="", showGrnMsg=""):
  SELF.session.open(BF(CCd1mn, title=title, VVHEnC=VVHEnC, showGrnMsg=showGrnMsg))
class CCfRRs(Screen, ConfigListScreen):
 def __init__(self, session):
  self.skin, self.skinParam = FF896P(VVJ7n1, 1400, 1000, 50, 40, 40, "#11201010", "#11101010", 26, barHeight=40, topRightBtns=1)
  self.session  = session
  self.Title   = "%s Settings" % PLUGIN_NAME
  FFJd2Z(self, title=self.Title)
  FFHhgX(self["keyGreen"], "Save")
  lst = []
  lst.append(getConfigListEntry("Show in Main Menu"           , CFG.showInMainMenu   ))
  lst.append(getConfigListEntry("Show in Extensions Menu"          , CFG.showInExtensionMenu  ))
  lst.append(getConfigListEntry("Show in Channel List Context Menu"       , CFG.showInChannelListMenu  ))
  lst.append(getConfigListEntry("Show in Events Info Menu"         , CFG.EventsInfoMenu   ))
  lst.append(getConfigListEntry("Input Type"             , CFG.keyboard     ))
  lst.append(getConfigListEntry("File Manage Exit-Button Action"        , CFG.FileManagerExit   ))
  lst.append(getConfigListEntry("Signal & Player Cotroller Hotkey"       , CFG.hotkey_signal    ))
  if VVe9cu:
   lst.append(getConfigListEntry("EPG Translation Language"        , CFG.epgLanguage    ))
  lst.append(getConfigListEntry(VVZ1aI *2              ,         ))
  lst.append(getConfigListEntry("Default IPTV Reference Type"         , CFG.iptvAddToBouquetRefType ))
  lst.append(getConfigListEntry("Auto Reset Frozen Live Channels (player dependent)"   , CFG.autoResetFrozenIptvChan ))
  lst.append(getConfigListEntry("Skip Adults Channels (from IPTV Server)"      , CFG.hideIptvServerAdultWords ))
  lst.append(getConfigListEntry("Remove IPTV Channel Name Prefix (|EN| , |AR|Drama|)"   , CFG.hideIptvServerChannPrefix ))
  lst.append(getConfigListEntry("IPTV Hosts Files Path (Playlist, Portal, M3U)"    , CFG.iptvHostsMode    ))
  lst.append(getConfigListEntry("Movie/Series Download Path"         , CFG.MovieDownloadPath   ))
  lst.append(getConfigListEntry(VVZ1aI *2              ,         ))
  lst.append(getConfigListEntry("PIcons Path"             , CFG.PIconsPath    ))
  lst.append(getConfigListEntry(VVZ1aI *2              ,         ))
  lst.append(getConfigListEntry("Backup/Restore Path"           , CFG.backupPath    ))
  lst.append(getConfigListEntry("Created Package Files (IPK/DEB)"        , CFG.packageOutputPath   ))
  lst.append(getConfigListEntry("Downloaded Packages (from feeds)"       , CFG.downloadedPackagesPath ))
  lst.append(getConfigListEntry("Exported Tables"            , CFG.exportedTablesPath  ))
  lst.append(getConfigListEntry("Exported PIcons"            , CFG.exportedPIconsPath  ))
  ConfigListScreen.__init__(self, lst, session)
  self.VVs7wI()
  self.onShown.append(self.VVqouI)
 def VVs7wI(self):
  kList = {
    "ok"  : self.VVmz9T    ,
    "green"  : self.VVEKYa  ,
    "menu"  : self.VVjrgJ  ,
    "cancel" : self.VVshYl  ,
    }
  kLeft = kRight = None
  try:
   from Components.config import ConfigSubList, KEY_LEFT as kLeft, KEY_RIGHT as kRight
  except:
   try:
    from Components.config import ConfigSubList, ACTIONKEY_LEFT as kLeft, ACTIONKEY_RIGHT as kRight
   except:
    pass
  if not (kLeft == kRight == None):
   kList["left"] = BF(self["config"].handleKey, kLeft)
   kList["right"] = BF(self["config"].handleKey, kRight)
   try:
    kList["chanUp"]  = self["config"].pageUp
    kList["chanDown"] = self["config"].pageDown
   except:
    try:
     kList["chanUp"]  = BF(self["config"].VVVBaC, 0)
     kList["chanDown"] = BF(self["config"].VVVBaC, len(self["config"].list) - 1)
    except:
     pass
   self["config_actions"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"], kList, -1)
  else:
   self["actions"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"], kList, -1)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FF4Pls(self)
  FFkCFB(self["config"])
  FF4FP6(self, self["config"])
  FFtIlI(self)
 def VVmz9T(self):
  item = self["config"].getCurrent()[1]
  if item:
   if   item == CFG.iptvHostsMode   : self.VVwPBw()
   elif item == CFG.MovieDownloadPath   : self.VVAvvV(item, self["config"].getCurrent()[0])
   elif item == CFG.PIconsPath    : self.VVzeGj(item)
   elif item == CFG.backupPath    : self.VVzeGj(item)
   elif item == CFG.packageOutputPath  : self.VVzeGj(item)
   elif item == CFG.downloadedPackagesPath : self.VVzeGj(item)
   elif item == CFG.exportedTablesPath  : self.VVzeGj(item)
   elif item == CFG.exportedPIconsPath  : self.VVzeGj(item)
 def VVAvvV(self, item, title):
  tot = CC9Zvn.VVkpCq()
  if tot : FFkYsE(self, "Cannot change while downloading.", title=title)
  else : self.VVzeGj(item)
 def VVwPBw(self):
  VV625J = []
  VV625J.append(("Auto Find" , "auto"))
  VV625J.append(("Custom Path" , "cust"))
  FFuRfS(self, self.VV9Iz6, VV625J=VV625J, title="IPTV Hosts Files Path")
 def VV9Iz6(self, item=None):
  if item:
   if item == "auto":
    CFG.iptvHostsMode.setValue(VVXLG3)
   elif item == "cust":
    VVvhuK = self.VVs7Hk()
    if VVvhuK : self.VVzsxL(VVvhuK)
    else  : self.session.openWithCallback(self.VVebtK, BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx="/"))
 def VVzsxL(self, VVvhuK):
  VVfPgM = self.VVHdWX
  VVMQj9 = ("Remove"  , self.VVDuLl , [])
  VVOtSO = ("Add "  , self.VVc3xO, [])
  header   = ("Directory" , "Remarks" )
  widths   = (80   , 20  )
  VVQqg2  = (LEFT   , LEFT  )
  FF1dQ4(self, None, title="IPTV Hosts Search Paths", header=header, VVvytR=VVvhuK, width=1200, height=700, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=26, VVfPgM=VVfPgM, VVMQj9=VVMQj9, VVOtSO=VVOtSO
    , VVz2kc="#11220000", VVwpZm="#11110000", VVghPi="#11110011", VVAfLs="#00ffff00", VV0g1U="#00223025", VVooYw="#0a333333", VVPVU2="#0a400040")
 def VVHdWX(self, VVcpnp):
  if CFG.iptvHostsDirs.getValue():
   CFG.iptvHostsMode.setValue(VV1nAS)
  VVcpnp.cancel()
 def VVebtK(self, path):
  if path:
   FFnT3A(CFG.iptvHostsDirs, FF0WrY(path.strip()))
   VVvhuK = self.VVs7Hk()
   if VVvhuK : self.VVzsxL(VVvhuK)
   else  : FFD1yO(self, "Cannot add dir", 1500)
 def VV3m0Q(self):
  lst = CFG.iptvHostsDirs.getValue().split(",")
  lst = list(set(list(map(str.strip, lst))))
  if len(lst) == 0 or len(lst[0]) == 0 or lst[0] == VVXLG3:
   return []
  return lst
 def VVs7Hk(self):
  lst = self.VV3m0Q()
  if lst:
   VVvhuK = []
   for Dir in lst:
    VVvhuK.append((Dir, "#f#0000ff00#Dir exists" if pathExists(Dir) else "#f#00ffa000#Not found"))
   VVvhuK.sort(key=lambda x: x[0].lower())
   return VVvhuK
  else:
   return []
 def VVc3xO(self, VVcpnp, title, txt, colList):
  sDir = parent = os.path.abspath(os.path.join(colList[0], os.pardir))
  self.session.openWithCallback(BF(self.VVwgg1, VVcpnp)
         , BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx=sDir))
 def VVwgg1(self, VVcpnp, path):
  if path:
   path = FF0WrY(path.strip())
   if self.VVMctx(VVcpnp, path):
    FFD1yO(VVcpnp, "Already added", 1500)
   else:
    lst = self.VV3m0Q()
    lst.append(path)
    FFnT3A(CFG.iptvHostsDirs, ",".join(lst))
    VVvhuK = self.VVs7Hk()
    VVcpnp.VVuVux(VVvhuK, tableRefreshCB=BF(self.VVLUCz, path))
 def VVLUCz(self, path, VVcpnp, title, txt, colList):
  self.VVMctx(VVcpnp, path)
 def VVMctx(self, VVcpnp, path):
  for ndx, row in enumerate(VVcpnp.VVGrbO()):
   if row[0].strip() == path.strip():
    VVcpnp.VVtpKN(ndx)
    return True
  return False
 def VVDuLl(self, VVcpnp, title, txt, colList):
  path = colList[0]
  FFMIbO(self, BF(self.VVVGRa, VVcpnp), "Remove this path from list?\n\n%s" % path, title="Remove path from list")
 def VVVGRa(self, VVcpnp):
  row = VVcpnp.VVPxSj()
  path, rem = row[0], row[1]
  VVvhuK = []
  lst = []
  for ndx, row in enumerate(VVcpnp.VVGrbO()):
   tPath, tRem = row[0].strip(), row[1].strip()
   if not path == tPath:
    lst.append(tPath)
    VVvhuK.append((tPath, tRem))
  if len(VVvhuK) > 0:
   FFnT3A(CFG.iptvHostsDirs, ",".join(lst))
   VVcpnp.VVuVux(VVvhuK)
   FFD1yO(VVcpnp, "Deleted", 1500)
  else:
   FFnT3A(CFG.iptvHostsMode, VVXLG3)
   FFnT3A(CFG.iptvHostsDirs, "")
   VVcpnp.cancel()
   FFpoMu(BF(FFD1yO, self, "Changed to Auto-Find", 1500))
 def VVzeGj(self, configObj):
  sDir = configObj.getValue()
  self.session.openWithCallback(BF(self.VVQrK6, configObj)
         , BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx=sDir))
 def VVQrK6(self, configObj, path):
  if len(path) > 0:
   configObj.setValue(path)
 def VVshYl(self):
  for x in self["config"].list:
   try:
    if x[1].isChanged():
     FFMIbO(self, self.VVEKYa, "Save Changes ?", callBack_No=self.cancel, title=self.Title)
     break
   except:
    pass
  else:
   self.cancel()
 def VVEKYa(self):
  for x in self["config"].list:
   try:
    x[1].save()
   except:
    pass
  self.VV7uuB()
  self.close()
 def cancel(self):
  for x in self["config"].list:
   try:
    x[1].cancel()
   except:
    pass
  self.close()
 def VVjrgJ(self):
  VV625J = []
  VV625J.append(("Use Backup Path for Package/Download/Tables/PIcons"   , "VVBFKk"   ))
  VV625J.append(("Reset %s Settings" % PLUGIN_NAME        , "VVNxDa"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Change Text Color Scheme (fix Transparent Text)"    , "changeColorScheme" ))
  VV625J.append(VVm77t)
  VV625J.append(("Backup %s Settings" % PLUGIN_NAME        , "VVwT8G"  ))
  VV625J.append(("Restore %s Settings" % PLUGIN_NAME       , "VVtnW7"  ))
  if fileExists(VVCnD5 + VVJNDG):
   VV625J.append(VVm77t)
   if CFG.checkForUpdateAtStartup.getValue() : txt1, txt2 = "Disable"  , "disableChkUpdate"
   else          : txt1, txt2 = "Enable"   , "enableChkUpdate"
   VV625J.append(('%s Checking for Update' % txt1       , txt2     ))
   VV625J.append(("Reinstall %s" % PLUGIN_NAME        , "VVcC3P"  ))
   VV625J.append(("Update %s" % PLUGIN_NAME        , "VVC1PP"   ))
  FFuRfS(self, self.VVK5vI, VV625J=VV625J, title="Config. Options")
 def VVK5vI(self, item=None):
  if item:
   if   item == "VVBFKk"  : FFMIbO(self, self.VVBFKk , "Use Backup directory in all other paths (and save) ?")
   elif item == "VVNxDa"  : FFMIbO(self, self.VVNxDa, "Clear all settings (including File Manager bookmarks) ?")
   elif item == "changeColorScheme": self.session.open(CCLqkY)
   elif item == "VVwT8G" : self.VVwT8G()
   elif item == "VVtnW7" : FFlX3B(self, self.VVtnW7, title="Searching for Settings ...")
   elif item == "enableChkUpdate" : FFnT3A(CFG.checkForUpdateAtStartup, True)
   elif item == "disableChkUpdate" : FFnT3A(CFG.checkForUpdateAtStartup, False)
   elif item == "VVcC3P" : FFlX3B(self, self.VVcC3P , "Checking Server ...")
   elif item == "VVC1PP"  : FFlX3B(self, self.VVC1PP  , "Checking Server ...")
 def VVwT8G(self):
  path = "%sajpanel_settings_%s" % (VVCnD5, FFGuM2())
  os.system("grep .%s. %ssettings > %s" % (PLUGIN_NAME, VV609C, path))
  FFewCE(self, "Saved to file:\n\n%s" % path, title="Export %s Settings" % PLUGIN_NAME)
 def VVtnW7(self):
  title = "Import %s Settings" % PLUGIN_NAME
  name = "ajpanel_settings_"
  lines = FFiGf6("find / %s -iname '%s*' | grep %s" % (FFlfqZ(1), name, name))
  if lines:
   lines.sort()
   VV625J = []
   for line in lines:
    VV625J.append((line, line))
   FFuRfS(self, BF(self.VVsQWm, title), title=title, VV625J=VV625J, width=1200)
  else:
   FFkYsE(self, "No settings files found !", title=title)
 def VVsQWm(self, title, path=None):
  if path:
   if pathExists(path):
    lines  = FFjdnJ(path)
    for line in lines:
     eqNdx = line.find('=')
     if eqNdx > -1:
      name = line[:eqNdx].strip()
      val  = line[eqNdx + 1:].strip()
      try:
       configEntry = eval(name)
       if configEntry is not None:
        if   isinstance(configEntry, ConfigInteger)  : val = int(val)
        elif isinstance(configEntry, ConfigYesNo)  : val = { "true": True, "false": False }.get(val)
        if not val is None:
         configEntry.value = val
         configEntry.save()
      except:
       pass
    self.VV7uuB()
    FFWcGD()
   else:
    FFAVqd(SELF, path, title=title)
 def VVBFKk(self):
  newPath = FF0WrY(VVCnD5)
  CFG.packageOutputPath.setValue(newPath)
  CFG.downloadedPackagesPath.setValue(newPath)
  CFG.exportedTablesPath.setValue(newPath)
  CFG.exportedPIconsPath.setValue(newPath)
  CFG.packageOutputPath.save()
  CFG.downloadedPackagesPath.save()
  CFG.exportedTablesPath.save()
  CFG.exportedPIconsPath.save()
  self.VV7uuB()
 @staticmethod
 def VVKPvT():
  backUpPath = "/media/usb/"
  if pathExists(backUpPath):
   return backUpPath
  else:
   return "/"
 def VVNxDa(self):
  for (key, cfg) in list(CFG.content.items.items()):
   cfg.setValue(cfg.default)
  for x in self["config"].list:
   try:
    x[1].save()
   except:
    pass
  self.VV7uuB()
  self.close()
 def VV7uuB(self):
  configfile.save()
  global VVCnD5
  VVCnD5 = CFG.backupPath.getValue()
  FFnm9f()
 def VVC1PP(self):
  title = "Update %s (from server)" % PLUGIN_NAME
  webVer = self.VVgp9Q(title)
  if webVer:
   FFMIbO(self, BF(FFlX3B, self, BF(self.VVHmGq, webVer, title)), "Update with v%s and Restart ?" % webVer, title=title)
 def VVcC3P(self):
  title = "Reinstall %s (from server)" % PLUGIN_NAME
  webVer = self.VVgp9Q(title, True)
  if webVer:
   FFMIbO(self, BF(FFlX3B, self, BF(self.VVHmGq, webVer, title, True)), "Install and Restart ?", title=title)
 def VVHmGq(self, webVer, title, isReinst=False):
  url = self.VVysnu(self, title)
  if url:
   VVyJBC = FFC2Pr() == "dpkg"
   if VVyJBC == "dpkg" : ext = "deb"
   else     : ext = "ipk"
   fName = "enigma2-plugin-extensions-ajpanel_v%s_all.%s" % (webVer, "deb" if VVyJBC else "ipk")
   path, err = FF913T(url + fName, fName, timeout=2)
   if path:
    if isReinst : cmd = FFQ7Q5(VVEoQq, path)
    else  : cmd = FFQ7Q5(VVKrAC, path)
    if cmd:
     cmd = "%s && echo -e '\nSUCCESSFUL' || echo -e '\nERROR FOUND !'; rm -r '%s'" % (cmd, path)
     FFfbee(self, cmd)
    else:
     FFHRK6(self, title=title)
   else:
    FFkYsE(self, err, title=title)
 def VVgp9Q(self, title, anyVer=False):
  url = self.VVysnu(self, title)
  if not url:
   return ""
  path, err = FF913T(url + "version", "ajpanel_tmp.ver", timeout=2)
  if not path:
   FFkYsE(self, err, title)
   return ""
  webVer = ""
  if fileExists(path):
   txt  = FFqD66(path)
   txt  = txt.replace(" ", "")
   span = iSearch(r"version\s*\=\s*v*(.+)", txt, IGNORECASE)
   if span : webVer = span.group(1)
   else : err = 'Server version not found !'
  else:
   err = 'Cannot download server "version" file !'
  if err:
   FFkYsE(self, err, title)
   return ""
  if anyVer:
   return webVer
  curVer = VV73TT.lstrip("v").lstrip("V")
  if not curVer == webVer:
   cmd = "printf '%s\n%s\n' | sort -V" % (curVer, webVer)
   list = FFiGf6(cmd)
   if list and curVer == list[0]:
    return webVer
  FFewCE(self, FFkhYI("No update required.", VV9cEK) + "\n\nCurrent Version = %s\n\nWeb Version = %s" % (curVer, webVer), title)
  return ""
 @staticmethod
 def VVysnu(SELF=None, title=None):
  url  = ""
  err  = ""
  path = VVCnD5 + VVJNDG
  if fileExists(path):
   span = iSearch(r"(http.+)", FFqD66(path), IGNORECASE)
   if span : url = FF0WrY(span.group(1))
   else : err = "No URL in:\n\n%s" % path
  else:
   err = "Update File not found:\n\n%s" % path
  if err and SELF and title:
   FFkYsE(SELF, err, title)
  return url
 @staticmethod
 def VVKiP7(url):
  path, err = FF913T(url + "version", "ajpanel_tmp.ver", timeout=2)
  if path and fileExists(path):
   txt  = FFqD66(path)
   txt  = txt.replace(" ", "")
   span = iSearch(r"version\s*\=\s*v*(.+)", txt, IGNORECASE)
   if span:
    webVer = span.group(1)
    curVer = VV73TT.lstrip("v").lstrip("V")
    if not curVer == webVer:
     cmd = "printf '%s\n%s\n' | sort -V" % (curVer, webVer)
     list = FFiGf6(cmd)
     if list and curVer == list[0]:
      return "v" + webVer
  return ""
class CCLqkY(Screen):
 def __init__(self, session):
  self.skin, self.skinParam = FF896P(VVbZAe, 1200, 620, 50, 20, 0, "#22002020", "#22001122", 30)
  self.cursorPos = COLOR_SCHEME_NUM
  self.Title  = "Select Color Scheme (for areas with mixed-color text)"
  self.session = session
  FFJd2Z(self, title=self.Title)
  sp = "    "
  self["myColorF"] = Label()
  for i in range(4):
   txt = "\n"
   txt += self.VVwnvX("\c00FFFFFF", i) + sp + "WHITE\n"
   txt += self.VVwnvX("\c00888888", i) + sp + "GREY\n"
   txt += self.VVwnvX("\c005A5A5A", i) + sp + "DARK GREY\n"
   txt += self.VVwnvX("\c00FF0000", i) + sp + "RED\n"
   txt += self.VVwnvX("\c00FF5000", i) + sp + "ORANGE\n"
   txt += self.VVwnvX("\c00FFFF00", i) + sp + "YELLOW\n"
   txt += self.VVwnvX("\c00FFFFAA", i) + sp + "B. YELLOW\n"
   txt += self.VVwnvX("\c0000FF00", i) + sp + "GREEN\n"
   txt += self.VVwnvX("\c000066FF", i) + sp + "BLUE\n"
   txt += self.VVwnvX("\c0000FFFF", i) + sp + "CYAN\n"
   txt += self.VVwnvX("\c00FA55E7", i) + sp + "PURPLE\n"
   txt += self.VVwnvX("\c00FF8F5F", i) + sp + "PEACH\n"
   self["myColor%s" % i] = Label(txt)
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : self.VVmz9T ,
   "green"   : self.VVmz9T ,
   "left"   : self.VV8g7c ,
   "right"   : self.VVkPgM ,
   "cancel"  : self.close
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  self.VVsv9D()
 def VVmz9T(self):
  if self.cursorPos == 0 : txt = "No Colors"
  else     : txt = "Color Scheme-%d" % self.cursorPos
  FFMIbO(self, self.VVTWBr, "Change to : %s" % txt, title=self.Title)
 def VVTWBr(self):
  FFnT3A(CFG.mixedColorScheme, self.cursorPos)
  global COLOR_SCHEME_NUM
  COLOR_SCHEME_NUM = self.cursorPos
  self.VViBd2()
  self.close()
 def VV8g7c(self):
  self.cursorPos -= 1
  if self.cursorPos < 0:
   self.cursorPos = 3
  self.VVsv9D()
 def VVkPgM(self):
  self.cursorPos += 1
  if self.cursorPos > 3:
   self.cursorPos = 0
  self.VVsv9D()
 def VVsv9D(self):
  left = []
  for i in range(4):
   left.append(self["myColor%s" % i].getPosition()[0])
  left = left[self.cursorPos] - 4
  top = self["myColor0"].getPosition()[1] - 4
  self.cursorPos
  self["myColorF"].instance.move(ePoint(left, top))
 @staticmethod
 def VVwnvX(color, mode):
  if   mode == 1 : return color
  elif mode == 2 : return color.replace("A", "9").replace("B", "9").replace("C", "9").replace("D", "9").replace("E", "9").replace("F", "9")
  elif mode == 3 : return color.replace("A", ":").replace("B", ";").replace("C", "<").replace("D", "=").replace("E", ">").replace("F", "?")
  else   : return ""
 @staticmethod
 def VVdf1F(color):
  if VVdWFT: return "\\" + color
  else    : return ""
 @staticmethod
 def VViBd2():
  global VVjrAG, VVkXS4, VVzZva, VVMmz2, VVU8eD, VVTdoW, VVYje8, VVhR0y, VV9cEK, VVk6tE, VVdWFT, VVoTT6, VVpHwQ, VVNTmM, VVyFMl, VVZgqQ
  VVZgqQ   = CCLqkY.VVwnvX("\c00FFFFFF", COLOR_SCHEME_NUM)
  VVkXS4    = CCLqkY.VVwnvX("\c00888888", COLOR_SCHEME_NUM)
  VVjrAG  = CCLqkY.VVwnvX("\c005A5A5A", COLOR_SCHEME_NUM)
  VVhR0y    = CCLqkY.VVwnvX("\c00FF0000", COLOR_SCHEME_NUM)
  VVzZva   = CCLqkY.VVwnvX("\c00FF5000", COLOR_SCHEME_NUM)
  VVMmz2   = CCLqkY.VVwnvX("\c00FFBB66", COLOR_SCHEME_NUM)
  VVdWFT   = CCLqkY.VVwnvX("\c00FFFF00", COLOR_SCHEME_NUM)
  VVoTT6 = CCLqkY.VVwnvX("\c00FFFFAA", COLOR_SCHEME_NUM)
  VV9cEK   = CCLqkY.VVwnvX("\c0000FF00", COLOR_SCHEME_NUM)
  VVk6tE  = CCLqkY.VVwnvX("\c00AAFFAA", COLOR_SCHEME_NUM)
  VVYje8    = CCLqkY.VVwnvX("\c000066FF", COLOR_SCHEME_NUM)
  VVpHwQ    = CCLqkY.VVwnvX("\c0000FFFF", COLOR_SCHEME_NUM)
  VVNTmM  = CCLqkY.VVwnvX("\c00AAFFFF", COLOR_SCHEME_NUM)  #
  VVyFMl   = CCLqkY.VVwnvX("\c00FA55E7", COLOR_SCHEME_NUM)
  VVU8eD    = CCLqkY.VVwnvX("\c00FF8F5F", COLOR_SCHEME_NUM)
  VVTdoW  = CCLqkY.VVwnvX("\c00FFC0C0", COLOR_SCHEME_NUM)
CCLqkY.VViBd2()
class CCw9MO(Screen):
 def __init__(self, session, path, VVyJBC):
  self.skin, self.skinParam = FF896P(VV0L7B, 1400, 850, 50, 30, 20, "#11001020", "#11001122", 26, barHeight=40)
  self.session    = session
  self.Path     = path
  self.VVbRg6   = path
  self.VVML6G   = ""
  self.VV9U8g   = ""
  self.VVyJBC    = VVyJBC
  self.VVg2aY    = ""
  self.VVpnBT  = ""
  self.VVbmLa    = False
  self.VVUza7  = False
  self.origPackageName  = ""
  self.postInstAcion   = 0
  self.VVEcCh  = "enigma2-plugin-extensions-"
  self.VV7DoR  = "enigma2-plugin-systemplugins-"
  self.VVlPMm = "enigma2-"
  self.VVODa4  = 0
  self.VVy184  = 1
  self.VVcyMM  = 2
  if pathExists(self.Path + "DEBIAN") : self.VV4Zxm = "DEBIAN"
  else        : self.VV4Zxm = "CONTROL"
  self.controlPath = self.Path + self.VV4Zxm
  self.controlFile = self.controlPath + "/control"
  self.preinstFile = self.controlPath + "/preinst"
  self.postinstFile = self.controlPath + "/postinst"
  self.prermFile  = self.controlPath + "/prerm"
  self.postrmFile  = self.controlPath + "/postrm"
  self.newControlPath = ""
  if self.VVyJBC:
   self.packageExt  = ".deb"
   self.VVghPi  = "#11001010"
  else:
   self.packageExt  = ".ipk"
   self.VVghPi  = "#11001020"
  FFJd2Z(self, "Create Package (%s)" % self.packageExt, addLabel=True)
  FFHhgX(self["keyRed"] , "Create")
  FFHhgX(self["keyGreen"] , "Post Install")
  FFHhgX(self["keyYellow"], "Installation Path")
  FFHhgX(self["keyBlue"] , "Change Version")
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "red"   : self.VVqR14  ,
   "green"   : self.VVlHa8 ,
   "yellow"  : self.VV3C4z  ,
   "blue"   : self.VVaKon  ,
   "cancel"  : self.VVIcsD
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFtIlI(self)
  if self.VVghPi:
   FFobAA(self["myBody"], self.VVghPi)
   FFobAA(self["myLabel"], self.VVghPi)
  self.VV4Agi(True)
  self.VVHnng(True)
 def VVHnng(self, isFirstTime=False):
  controlInfo, errTxt, package = self.VVnftE()
  if isFirstTime:
   if   package.startswith(self.VVEcCh) : self.VVbRg6 = VV9VaA + self.VVg2aY + "/"
   elif package.startswith(self.VV7DoR) : self.VVbRg6 = VVuVce + self.VVg2aY + "/"
   else            : self.VVbRg6 = self.Path
  if self.VVbmLa : myColor = VVU8eD
  else    : myColor = VVZgqQ
  txt  = ""
  txt += "Source Path\t: %s\n" % FFkhYI(self.Path  , myColor)
  txt += "Installation\t: %s\n" % FFkhYI(self.VVbRg6, VVdWFT)
  if self.VV9U8g : txt += "Package File\t: %s\n" % FFkhYI(self.VV9U8g, VVkXS4)
  elif errTxt   : txt += "Warning\t: %s\n"  % FFkhYI("Check Control File fields : %s" % errTxt, VVzZva)
  if self["keyGreen"].getVisible():
   if   self.postInstAcion == 1: act = "Add commands to %s after installation." % FFkhYI("Restart GUI", VVU8eD)
   elif self.postInstAcion == 2: act = "Add commands to %s after installation." % FFkhYI("Reboot Device", VVU8eD)
   else      : act = "No action."
   txt += "\n%s\t: %s\n" % (FFkhYI("Post Install", VV9cEK), act)
  if not errTxt and VVzZva in controlInfo:
   txt += "Warning\t: %s\n" % FFkhYI("Errors in control file may affect the result package.", VVzZva)
  txt += "\nControl File\t: %s\n" % FFkhYI(self.controlFile, VVkXS4)
  txt += controlInfo.replace(":", "\t:")
  self["myLabel"].setText(txt)
 def VVlHa8(self):
  if self["keyGreen"].getVisible():
   VV625J = []
   VV625J.append(("No Action"    , "noAction"  ))
   VV625J.append(("Restart GUI"    , "VVvFw0"  ))
   VV625J.append(("Reboot Device"   , "rebootDev"  ))
   FFuRfS(self, self.VVU0QF, title="Package Installation Option (after completing installation)", VV625J=VV625J)
 def VVU0QF(self, item=None):
  if item is not None:
   if   item == "noAction"   : self.postInstAcion = 0
   elif item == "VVvFw0"  : self.postInstAcion = 1
   elif item == "rebootDev"  : self.postInstAcion = 2
   self.VV4Agi(False)
   self.VVHnng()
 def VV3C4z(self):
  rootPath = FFkhYI("/%s/" % self.VVg2aY, VVoTT6)
  VV625J = []
  VV625J.append(("Current Path"        , "toCurrent"  ))
  VV625J.append(VVm77t)
  VV625J.append(("Extension Path"       , "toExtensions" ))
  VV625J.append(("System Plugins Path"      , "toSystemPlugins" ))
  VV625J.append(VVm77t)
  VV625J.append(("Package Name in Root : %s" % rootPath  , "toRootPath"  ))
  VV625J.append(('Root "/" (Multiple Directories Package)' , "toRoot"   ))
  VV625J.append(VVm77t)
  VV625J.append(("Pick Path with File Manager ..."   , "toOthers"  ))
  FFuRfS(self, self.VVa9jg, title="Installation Path", VV625J=VV625J)
 def VVa9jg(self, item=None):
  if item is not None:
   if   item == "toCurrent"  : self.VVvFUQ(FFMjyS(self.Path, True))
   elif item == "toExtensions"  : self.VVvFUQ(VV9VaA)
   elif item == "toSystemPlugins" : self.VVvFUQ(VVuVce)
   elif item == "toRootPath"  : self.VVvFUQ("/")
   elif item == "toRoot"   : self.VVvFUQ("/", False)
   elif item == "toOthers"   : self.session.openWithCallback(self.VVYrAE, BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx=VVCnD5))
 def VVYrAE(self, path):
  if len(path) > 0:
   self.VVvFUQ(path)
 def VVvFUQ(self, parent, withPackageName=True):
  if withPackageName : self.VVbRg6 = parent + self.VVg2aY + "/"
  else    : self.VVbRg6 = "/"
  mode = self.VV6QGP()
  os.system("sed -i '/Package/c\Package: %s' %s" % (self.VVS24o(mode), self.controlFile))
  self.VVHnng()
 def VVaKon(self):
  if fileExists(self.controlFile):
   lines = FFjdnJ(self.controlFile)
   version = ""
   for line in lines:
    if ":" in line:
     parts = line.split(":")
     key  = parts[0].strip()
     val  = parts[1].strip()
     if key == "Version":
      version = val
      break
   if version : FFbRXK(self, self.VVuVrg, title="Change Package Version", defaultText=version, message="Enter Version:")
   else  : FFkYsE(self, "Version not found or incorrectly set !")
  else:
   FFAVqd(self, self.controlFile)
 def VVuVrg(self, VVVomg):
  if VVVomg:
   version, color = self.VV7Xh2(VVVomg, False)
   if color == VVpHwQ:
    os.system("sed -i '/Version:/c\Version: %s' %s" % (VVVomg, self.controlFile))
    self.VVHnng()
   else:
    FFkYsE(self, "Incorrect Version Syntax !\n\nAllowed characters : letter, digits and _+-.~")
 def VVIcsD(self):
  if self.newControlPath:
   if self.VVbmLa:
    self.VVoh9n()
   else:
    txt  = "Control Files were created in:\n%s\n\n" % FFkhYI(self.newControlPath, VVkXS4)
    txt += FFkhYI("Do you want to keep these files ?", VVdWFT)
    FFMIbO(self, self.close, txt, callBack_No=self.VVoh9n, title="Create Package", VVUEfx=True)
  else:
   self.close()
 def VVoh9n(self):
  os.system(FFxtg8("rm -r '%s'" % self.newControlPath))
  self.close()
 def VVS24o(self, mode):
  prefix, name = "", ""
  package = self.origPackageName or self.VVpnBT
  if package.startswith(self.VVlPMm):
   span = iSearch(r"(.+-)(.+)", package)
   if span:
    prefix, name = span.group(1).strip(), span.group(2)
  if not name:
   prefix, name = self.VVlPMm, package
  prefix = iSub(r"([^a-z0-9+-.]+)", r"-", prefix)
  name = iSub(r"([^a-z0-9+-.]+)", r"-", name)
  if   mode == self.VVy184 : prefix = self.VVEcCh
  elif mode == self.VVcyMM : prefix = self.VV7DoR
  return (prefix + name).lower()
 def VV6QGP(self):
  if   self.VVbRg6.startswith(VV9VaA) : return self.VVy184
  elif self.VVbRg6.startswith(VVuVce) : return self.VVcyMM
  else            : return self.VVODa4
 def VV4Agi(self, isFirstTime):
  self.VVg2aY   = FFqDmh(self.Path)
  self.VVg2aY   = "_".join(self.VVg2aY.split())
  self.VVpnBT = self.VVg2aY.lower()
  self.VVbmLa = self.VVpnBT == VV0A4Z.lower()
  if self.VVbmLa and self.VVpnBT.endswith("ajpan"):
   self.VVpnBT += "el"
  if self.VVbmLa : self.VVML6G = VVCnD5
  else    : self.VVML6G = CFG.packageOutputPath.getValue()
  self.VVML6G = FF0WrY(self.VVML6G)
  if not pathExists(self.controlPath):
   os.system(FFxtg8("mkdir '%s'" % self.controlPath))
   self.newControlPath = self.controlPath
  else:
   self.newControlPath = ""
  mode = self.VV6QGP()
  if fileExists(self.controlFile):
   lines = FFjdnJ(self.controlFile)
   for line in lines:
    if line.strip().startswith("Package") and line.count(":") == 1:
     self.origPackageName = line.split(":")[1].strip()
     break
  else:
   if self.VVbmLa : version, descripton, maintainer = VV73TT , PLUGIN_DESCRIPTION, "AMA-Jamry"
   else    : version, descripton, maintainer = "v1.0"   , self.VVg2aY , self.VVg2aY
   txt = ""
   txt += "Package: %s\n"  % self.VVS24o(mode)
   txt += "Version: %s\n"  % version
   txt += "Description: %s\n" % descripton
   txt += "Maintainer: %s\n" % maintainer
   txt += "Architecture: all\n"
   txt += "Priority: optional\n"
   txt += "Section: base\n"
   txt += "License: none\n"
   txt += "OE: enigma2\n"
   txt += "Homepage: unknown\n"
   txt += "Depends: enigma2\n"
   txt += "Source: none\n"
   with open(self.controlFile, "w") as f:
    f.write(txt)
  if self.VVbmLa : t = PLUGIN_NAME
  else    : t = self.VVg2aY
  self.VV0ZTb(self.prermFile, "echo 'Removing package : %s ...'\n" % t)
  self.VV0ZTb(self.postrmFile, "echo 'Package removed.'\n")
  if self.VVbmLa : self.VV0ZTb(self.preinstFile, "echo 'Installing %s (%s) ...'\n" % (PLUGIN_NAME, VV73TT))
  else    : self.VV0ZTb(self.preinstFile, "echo 'Installing Package : %s ...'\n" % self.VVg2aY)
  if isFirstTime and not mode == self.VVODa4:
   self.postInstAcion = 1
  txt = self.VV3Aqk(self.postInstAcion)
  canChange = True
  self["keyGreen"].show()
  if fileExists(self.postinstFile):
   fText = FFqD66(self.postinstFile).strip()
   if txt.strip() == fText:
    canChange = False
   else:
    for action in range(3):
     if fText.strip() == self.VV3Aqk(action).strip():
      break
    else:
     canChange = False
     self["keyGreen"].hide()
  if canChange:
   with open(self.postinstFile, "w") as f:
    f.write(txt)
  os.system(FFxtg8("chmod 755 '%s' '%s' '%s' '%s' " % (self.preinstFile, self.postinstFile, self.prermFile, self.postrmFile)))
 def VV0ZTb(self, path, lines):
  if not fileExists(path):
   with open(path, "w") as f:
    f.write("#!/bin/bash\n")
    f.write(lines)
    f.write("exit 0\n")
 def VV3Aqk(self, action):
  sep  = "echo '%s'\n" % VVZ1aI
  txt = "#!/bin/bash\n" + sep
  if action == 0:
   txt += "echo '--- FINISHED ---'\n"
   txt += sep
   txt += "echo 'You may need to Restart GUI.'\n"
  elif action == 1:
   txt += "echo 'RESTARTING GUI ...'\n"
   txt += sep
   txt += "if which systemctl > /dev/null 2>&1; then sleep 2; systemctl restart enigma2; else init 4; sleep 4; init 3; fi\n"
  elif action == 2:
   txt += "echo 'REBOOTING DEVICE ...'\n"
   txt += sep
   txt += "sleep 3; reboot\n"
  else:
   return ""
  txt += "exit 0\n"
  return txt
 def VVnftE(self):
  txt = package = version = descr = arch = maint = ""
  if fileExists(self.controlFile):
   lines = FFjdnJ(self.controlFile)
   descrFound  = False
   ignoreList  = []
   descrIndex  = -1
   isDescrValid = False
   for ndx, line in enumerate(lines):
    if line.strip().startswith("Description"):
     descrFound = True
     descrIndex = ndx
     descr  = line + "\n"
     ignoreList.append(ndx)
     if ":" in line:
      parts = line.split(":")
      key, val= parts[0].strip(), parts[1].strip()
      if key == "Description":
       isDescrValid = True
    elif descrFound and not ":" in line:
     if line.startswith(" .") and len(line) > 2 : line = FFkhYI(line, VVzZva)
     elif not line.startswith(" ")    : line = FFkhYI(line, VVzZva)
     else          : line = FFkhYI(line, VVpHwQ)
     descr += line + "\n"
     ignoreList.append(ndx)
    elif descrFound and ":" in line:
     break
   if isDescrValid : color = VVpHwQ
   else   : color = VVzZva
   descr = FFkhYI(descr, color)
   for ndx, line in enumerate(lines):
    if ndx not in ignoreList:
     if line.strip() == "":
      line = "[ EMPTY LINES ARE NOT ALLOWED ]"
      color = VVzZva
     elif line.startswith((" ", "\t")) : color = VVzZva
     elif line.startswith("#")   : color = VVkXS4
     elif ":" in line:
      parts = line.split(":")
      key  = parts[0].strip()
      val  = parts[1].strip()
      if   key == "Package"  : package, color = self.VV7Xh2(val, True)
      elif key == "Version"  : version, color = self.VV7Xh2(val, False)
      elif key == "Maintainer" : maint  , color = val, VVpHwQ
      elif key == "Architecture" : arch  , color = val, VVpHwQ
      else:
       color = VVpHwQ
      if not key == "OE" and not key.istitle():
       color = VVzZva
     else:
      color = VVU8eD
     txt += FFkhYI(line, color) + "\n"
    else:
     if ndx == descrIndex:
      txt += descr
  if package and version and arch and descr and maint:
   packageName   = "%s_%s_%s%s" % (package, version, arch, self.packageExt)
   packageName   = packageName.replace(" ", "")
   self.VV9U8g = self.VVML6G + packageName
   self.VVUza7 = True
   errTxt = ""
  else:
   self.VV9U8g  = ""
   self.VVUza7 = False
   err = []
   if not package : err.append("Package")
   if not descr : err.append("Description")
   if not version : err.append("Version")
   if not arch  : err.append("Architecture")
   if not maint : err.append("Maintainer")
   errTxt = " , ".join(err) + ")"
  return txt, errTxt, package
 def VV7Xh2(self, val, isPackage):
  if   isPackage : pattern = r"^[a-z]+[a-z0-9+-_.]+$"
  else   : pattern = r"^[a-zA-Z0-9_+-.~]*$"
  if iMatch(pattern, val) and len(val) >= 2 : return val, VVpHwQ
  else          : return val, VVzZva
 def VVqR14(self):
  if not self.VVUza7:
   FFkYsE(self, "Please fix Control File errors first.")
   return
  if self.VVyJBC: tarParam, tarExt = "-cJhf", ".tar.xz"
  else   : tarParam, tarExt = "-czhf", ".tar.gz"
  projDir   = "/tmp/_%s/" % PLUGIN_NAME
  parent   = FFMjyS(self.VVbRg6, True)
  dataFile  = projDir + "data"   + tarExt
  controlFile  = projDir + "control" + tarExt
  debianFile  = projDir + "debian-binary"
  dataTmpPath  = projDir + "DATA/"
  newPath   = dataTmpPath + parent[1:]
  symlink   = dataTmpPath + parent[1:] + self.VVg2aY
  symlinkTo  = FFkEOw(self.Path)
  dataDir   = self.VVbRg6.rstrip("/")
  removePorjDir = FFxtg8("rm -r '%s'"  % projDir) + ";"
  cmd  = ""
  cmd += FFxtg8("rm -f '%s'" % self.VV9U8g) + ";"
  cmd += removePorjDir
  cmd += "mkdir -p '%s';"  % newPath
  cmd += "ln -sf '%s' '%s';" % (symlinkTo, symlink)
  cmd += FFr1Fs()
  if self.VVyJBC:
   cmd += 'if [ "$allOK" -eq "1" ]; then '
   cmd +=   FFqoRI("xz", "xz", "XZ")
   cmd += "fi;"
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd += " echo 'Creating Package ...';"
  tarExclude = "--exclude CONTROL --exclude DEBIAN --exclude __pycache__"
  if self.VVbmLa:
   tarExclude += " --exclude OBF --exclude *.pyo --exclude *.pyc"
  cmd += "cd '%s';"       % dataTmpPath
  if self.VVbRg6 == "/":
   cmd += " tar -C '%s' %s %s '%s' ./;" % (self.Path, tarExclude, tarParam, dataFile)
  else:
   cmd += " tar %s %s '%s' '.%s';" % (tarExclude, tarParam, dataFile, dataDir)
  cmd += " cd '%s%s';"  % (self.Path, self.VV4Zxm)
  cmd += " tar %s '%s' ./*;" % (tarParam, controlFile)
  cmd += " echo '2.0' > %s;" % debianFile
  checkCmd = " if [ ! -f '%s' ]; then allOK='0'; echo 'Colud not create %s'; fi;"
  cmd += checkCmd % (debianFile , "debian-binary")
  cmd += checkCmd % (controlFile , "control.tar")
  cmd += checkCmd % (dataFile  , "data.tar")
  cmd += ' if [ "$allOK" -eq "1" ]; then '
  cmd += "  cd '%s';"  % projDir
  cmd += "  ar -r '%s' %s %s %s;" % (self.VV9U8g, debianFile, controlFile, dataFile)
  cmd += " fi;"
  myTarCmd = ""
  result  = "Package:"
  instPath = "Designed to be installed in:"
  failed  = "Process Failed."
  cmd += " if [ -f '%s' ]; then "   % self.VV9U8g
  cmd += "  echo -e '\n%s\n%s' %s;" % (result  , self.VV9U8g, FF95sl(result  , VV9cEK))
  cmd +=    myTarCmd
  cmd += "  echo -e '\n%s\n%s' %s;" % (instPath, self.VVbRg6, FF95sl(instPath, VVpHwQ))
  cmd += " else"
  cmd += "  echo -e '\n%s' %s;" % (failed, FF95sl(failed, VVzZva))
  cmd += " fi;"
  cmd += "fi;"
  cmd += removePorjDir
  FFfbee(self, cmd)
class CCgKdM():
 VVYlEA  = "666"
 VVRiij   = "888"
 def __init__(self, SELF, waitMsgSELF, title, servRefListFnc, defBName="Bouquet1"):
  self.SELF     = SELF
  self.waitMsgSELF   = waitMsgSELF
  self.Title     = title
  self.servRefListFnc   = servRefListFnc
  self.defBName    = defBName
  self.menuInstance   = None
  self.VVsxs1()
 def VVsxs1(self):
  VV625J = CCgKdM.VVJtDO()
  if VV625J:
   VVJ5GS = ("Create New", self.VVicqc)
   self.menuInstance = FFuRfS(self.SELF, self.VVh4uk, VV625J=VV625J, title=self.Title, VVJ5GS=VVJ5GS, VVeYEo=True, VVz2kc="#22222233", VVwpZm="#22222233")
  else:
   self.VVicqc()
 def VVh4uk(self, item):
  if item:
   bName, bRef, ndx = item
   self.VVUUey(bName, bRef)
  else:
   CCgKdM.VVDGSc(self)
 def VVicqc(self, VVp2lZObj=None, item=None):
  FFbRXK(self.SELF, BF(self.VVanQa), defaultText=self.defBName, title="Create New Bouquet", message="Enter Bouquet Name:")
 def VVanQa(self, bName):
  if bName:
   bName = bName.strip()
   if bName:
    if self.menuInstance:
     self.menuInstance.cancel()
    self.VVUUey(bName, "")
   else:
    FFD1yO(self.menuInstance, "Incorrect Bouquet Name !", 2000)
    CCgKdM.VVDGSc(self)
 def VVUUey(self, bName, bRef):
  FFlX3B(self.waitMsgSELF, BF(self.VVXdio, bName, bRef), title="Adding Services ...")
 def VVXdio(self, bName, bRef):
  CCgKdM.VVLBiS(self.SELF, self.Title, bName, bRef, self.servRefListFnc())
 @staticmethod
 def VVDGSc(classObj):
  del classObj
 @staticmethod
 def VVLBiS(SELF, title, bName, bRef, servRefLst, showRes=True):
  if not servRefLst:
   FFkYsE(SELF, "No services to add !", title=title)
   return
  tvBouquetFile = VV609C + "bouquets.tv"
  if not fileExists(tvBouquetFile):
   FFAVqd(SELF, tvBouquetFile, title=title)
   return
  if bRef:
   bFile = CCgKdM.VVa7d3(bRef)
   bPath = VV609C + bFile
  else:
   fName = CCqQHV.VVwvI5(bName)
   bFile = "userbouquet.%s.tv" % fName
   bPath = VV609C + bFile
   num   = 0
   while fileExists(bPath):
    num += 1
    bFile = "userbouquet.%s_%d.tv" % (fName, num)
    bPath = VV609C + bFile
   with open(bPath, "w") as f:
    f.write("#NAME %s\n" % bName)
  CCgKdM.VV0WD2(bPath)
  with open(bPath, "a") as f:
   for chUrl in servRefLst:
    serv = eServiceReference(chUrl)
    chName = serv and serv.getName() or ""
    try:
     chName = chName.encode("UTF-8", "replace").decode()
    except:
     chName = iSub(r"([^\x00-\x7F]+)", r"?", chName)
    f.write("#SERVICE %s\n"  % chUrl)
    f.write("#DESCRIPTION %s\n" % chName)
  if not bRef and fileExists(bPath):
   CCgKdM.VV0WD2(tvBouquetFile)
   with open(tvBouquetFile, "a") as f:
    f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\n' % bFile)
  totPicons = 0
  piconPath = CCrs3r.VVsNIk()
  for chUrl in servRefLst:
   span = iSearch(r"((?:[A-Fa-f0-9]+:){10})", chUrl.rstrip(":"))
   if span:
    serv = eServiceReference(chUrl)
    if serv:
     picon = piconPath + span.group(1).strip(":").replace(":", "_").upper() + ".png"
     fPath = serv.getPath()
     fNameNoExt = os.path.splitext(serv.getPath())[0]
     for ext in ("png", "jpg", "bmp", "gif", "jpe", "jpeg", "mvi"):
      poster = "%s.%s" % (fNameNoExt, ext)
      if fileExists(poster):
       totPicons += 1
       os.system(FFxtg8("cp -f '%s' '%s'" % (poster, picon)))
       os.system(CCARMv.VVc7qU(picon))
       break
  FFlB9k()
  if showRes:
   txt  = "Bouquet Name\t\t: %s\n"  % bName
   txt += "Added Services\t\t: %d\n" % len(servRefLst)
   if totPicons:
    txt += "Added PIcons\t\t: %s" % totPicons
   FFNEkd(SELF, txt, title=title)
 @staticmethod
 def VVJtDO(mode=2, showTitle=True, prefix=""):
  VV625J = []
  if mode in (0, 2): VV625J.extend(CCgKdM.VVeJ8a(0, showTitle, prefix))
  if mode in (1, 2): VV625J.extend(CCgKdM.VVeJ8a(1, showTitle, prefix))
  return VV625J
 @staticmethod
 def VVeJ8a(mode, showTitle, prefix):
  VV625J = []
  lst = CCgKdM.VVZZ3k(mode)
  if lst:
   if showTitle:
    VV625J.append(FFi9aC("TV Bouquets" if mode == 0 else "Radio Bouquets"))
   if prefix:
    for item in lst : VV625J.append((item[0], prefix + item[0]))
   else:
    for item in lst : VV625J.append((item[0], item[1].toString()))
  return VV625J
 @staticmethod
 def VV8uSL():
  bLise = CCgKdM.VVZZ3k(0)
  bLise.extend(CCgKdM.VVZZ3k(1))
  return bLise
 @staticmethod
 def VVZZ3k(mode=0):
  bList = []
  VVurhM = InfoBar.instance
  VVoSQy = VVurhM and VVurhM.servicelist
  if VVoSQy:
   curMode = VVoSQy.mode
   CCgKdM.VV8hsK(VVoSQy, mode)
   bList.extend(VVoSQy.getBouquetList() or [])
   CCgKdM.VV8hsK(VVoSQy, curMode)
  return bList
 @staticmethod
 def VV8hsK(VVoSQy, mode):
  if not mode == VVoSQy.mode:
   if   mode == 0: VVoSQy.setModeTv()
   elif mode == 1: VVoSQy.setModeRadio()
 @staticmethod
 def VV0WD2(fPath):
  with open(fPath, "rb+") as f:
   try:
    f.seek(-1, 2)
    if ord(f.read(1)) not in (10, 13):
     f.write(b"\n")
   except:
    pass
 @staticmethod
 def VVa7d3(bRef):
  span = iSearch(r'BOUQUET\s+"(.+)"\s+ORDER', bRef, IGNORECASE)
  if span : return span.group(1)
  else : ""
 @staticmethod
 def VVYZBe():
  try:
   fName = CCgKdM.VVa7d3(InfoBar.instance.servicelist.getRoot().toString())
   path = "%s%s" % (VV609C, fName)
   if fileExists(path):
    return path
  except:
   pass
  return ""
 @staticmethod
 def VVNJJo():
  path = CCgKdM.VVYZBe()
  if path:
   txt = FFqD66(path, maxSize=300)
   span = iSearch(r"#NAME\s+(.*)", txt, IGNORECASE)
   if span:
    return span.group(1).strip()
  return ""
 @staticmethod
 def VVsvhM():
  return FFocgD(InfoBar.instance.servicelist.getRoot())
 @staticmethod
 def VVKEnt():
  lst = []
  for b in CCgKdM.VV8uSL():
   bName = b[0]
   bRef  = b[1].toString()
   path = VV609C + CCgKdM.VVa7d3(bRef)
   if fileExists(path):
    lines = FFjdnJ(path)
    for line in lines:
     if line.startswith("#SERVICE"):
      if not line.startswith("#SERVICE 1:64:"):
       break
    else:
     if not "userbouquet.favourites." in bRef:
      lst.append((bName, bRef))
  return lst
 @staticmethod
 def VVgSBD(SID, stripRType):
  if stripRType: return r"(?:[A-Fa-f0-9]+:)((?:[A-Fa-f0-9]+:){2}%s:(?:[A-Fa-f0-9]+:){6})" % SID
  else   : return r"((?:[A-Fa-f0-9]+:){3}%s:(?:[A-Fa-f0-9]+:){6})" % SID
 @staticmethod
 def VVvOrZ(SID="", stripRType=False):
  if SID : patt = CCgKdM.VVgSBD(SID, stripRType)
  else : patt = r"((?:[A-Fa-f0-9]+:){10})"
  lst = []
  for b in CCgKdM.VV8uSL():
   for service in FFocgD(b[1]):
    span = iSearch(patt, service[0])
    if span:
     lst.append(span.group(1).upper())
  return lst
 @staticmethod
 def VV1iFE():
  patt = r"((?:[A-Fa-f0-9]+:){10})http.+"
  lst = []
  for b in CCgKdM.VV8uSL():
   for service in FFocgD(b[1]):
    span = iSearch(patt, service[0])
    if span:
     lst.append(span.group(1).upper().rstrip(":"))
  return lst
 @staticmethod
 def VVp0RV(rType, SID, refLst, startId, startNS):
  for Id in range(max(6, startId), 65535):
   hexId = ("%1x" % Id).upper()
   for NS in range(startNS, 65535):
    hexNS = ("FFF%04x" % NS).upper()
    tRef = "0:1:%s:%s:%s:%s:0:0:0:" % (SID, hexId, hexId, hexNS)
    if not tRef in refLst:
     refCode = "%s:0:1:%s:%s:%s:%s:0:0:0:" % (rType, SID, hexId, hexId, hexNS)
     if NS < 65535 - 1: NS += 1
     else    : NS, Id = 6, Id + 1
     return refCode, Id, NS
  return "", 0, 0
 @staticmethod
 def VVpsne(pathLst):
  refLst = CCgKdM.VVvOrZ(CCgKdM.VVYlEA, stripRType=True)
  chUrlLst = []
  startId  = startNS = 0
  rType  = CFG.iptvAddToBouquetRefType.getValue()
  for path in pathLst:
   refCode, startId, startNS = CCgKdM.VVp0RV(rType, CCgKdM.VVYlEA, refLst, startId, startNS)
   if refCode:
    chName = os.path.splitext(os.path.basename(path))[0].replace("-", " ").replace("_", " ").replace(".", " ")
    chUrl = "%s%s:%s" % (refCode, path, chName)
    chUrlLst.append(chUrl)
   else:
    break
  return chUrlLst
class CC7ujK(Screen):
 VVPhtE   = 0
 VVHuGg  = 1
 VVBUn6  = 2
 VVWJV5  = 3
 VVVgDr    = 20
 VVxHrh  = None
 def __init__(self, session, VVKDYx="/", mode=VVPhtE, VVrLQt="Select", height=920, VVmp7B=30, gotoMovie=False, jumpToFile=""):
  self.skin, self.skinParam = FF896P(VVoxS0, 1400, height, 30, 40, 20, "#22001111", "#22000000", 30, barHeight=40, topRightBtns=2)
  self.session   = session
  FFJd2Z(self)
  FFHhgX(self["keyRed"] , "Exit" if mode == self.VVPhtE else "Cancel")
  FFHhgX(self["keyYellow"], "More Options")
  FFHhgX(self["keyBlue"] , "Bookmarks")
  self.maxTitleWidth  = 1000
  self.mode    = mode
  self.VVrLQt = VVrLQt
  self.jumpToFile   = jumpToFile
  self.gotoMovie   = gotoMovie
  self.bookmarkMenu  = None
  self.bigDirSize   = 300
  self.edited_newFile  = "file1"
  self.edited_newDir  = "dir1"
  self.cursorBG   = "#06003333"
  CC7ujK.VVxHrh = self
  if   self.jumpToFile       : VVDQj4, self.VVKDYx = True , FFMjyS(self.jumpToFile, True) or "/"
  elif self.gotoMovie        : VVDQj4, self.VVKDYx = True , CC7ujK.VVa1tR(self)[1] or "/"
  elif self.mode == self.VVPhtE  : VVDQj4, self.VVKDYx = True , CFG.browserStartPath.getValue()
  elif self.mode == self.VVBUn6 : VVDQj4, self.VVKDYx = False, VVKDYx
  elif self.mode == self.VVWJV5 : VVDQj4, self.VVKDYx = True , VVKDYx
  else           : VVDQj4, self.VVKDYx = True , VVKDYx
  self.VVKDYx = FF0WrY(self.VVKDYx)
  VVVPfW = None
  if self.mode == self.VVWJV5:
   VVVPfW = "^.*\.srt"
  self["myMenu"] = CCrQyy(  directory   = None
         , VVVPfW = VVVPfW
         , VVDQj4   = VVDQj4
         , VV8O4O = True
         , VV3ePF = True
         , VVsSYD   = self.skinParam["width"]
         , VVmp7B   = self.skinParam["bodyFontSize"]
         , VVyhPB  = self.skinParam["bodyLineH"]
         , VVQzgv  = self.skinParam["bodyColor"]
         , pngBGColorSelStr = self.cursorBG)
  self["myActionMap"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : self.VVmz9T    ,
   "red"  : self.VV0WYH   ,
   "green"  : self.VVteLf,
   "yellow" : self.VVkrPQ  ,
   "blue"  : self.VVEt59 ,
   "menu"  : self.VVshjT  ,
   "info"  : self.VVqpVw  ,
   "cancel" : self.VVqK2V    ,
   "pageUp" : self.VVPGFd   ,
   "chanUp" : self.VVPGFd
  }, -1)
  FFCMLR(self, self["myMenu"])
  self.onShown.append(self.start)
  self.onClose.append(self.onExit)
  self["myMenu"].onSelectionChanged.append(self.VVH7je)
 def onExit(self):
  CC7ujK.VVxHrh = None
 def start(self):
  self.onShown.remove(self.start)
  self.onShown.append(self.VVH7je)
  FF4Pls(self)
  FFkCFB(self["myMenu"], bg=self.cursorBG)
  FFtIlI(self)
  self.maxTitleWidth = self["keyInfo"].getPosition()[0] - 40
  if self.mode in (self.VVBUn6, self.VVWJV5):
   FFHhgX(self["keyGreen"], self.VVrLQt)
   color = "#22000022"
   FFobAA(self["myBody"], color)
   FFobAA(self["myMenu"], color)
   color = "#22220000"
   FFobAA(self["myTitle"], color)
   FFobAA(self["myBar"], color)
  self.VVH7je()
  if self.VVvjfY(self.VVKDYx) > self.bigDirSize: FFlX3B(self, self.VVi03s, title="Changing directory...")
  else              : self.VVi03s()
 def VVi03s(self):
  if self.jumpToFile : self.VVe5uc(self.jumpToFile)
  elif self.gotoMovie : self.VVxeMq(chDir=False)
  else    : self["myMenu"].VVimWq(self.VVKDYx)
 def VVtpKN(self, rowNdx):
  self["myMenu"].moveToIndex(rowNdx)
 def VVI84O(self):
  self["myMenu"].refresh()
  FFkmMQ()
 def VVvjfY(self, path):
  try:
   return len(os.listdir(path))
  except:
   return 0
 def VVmz9T(self):
  if self["myMenu"].VV5bSS() : self.VVrvBb()
  else       : self.VVN6IY()
 def VVPGFd(self):
  self["myMenu"].moveToIndex(0)
  if self["myMenu"].VVO6Ur():
   self.VVrvBb()
 def VVrvBb(self, isDirUp=False):
  if self["myMenu"].VV5bSS():
   if not self["myMenu"].getSelection() is None: path = self["myMenu"].getSelection()[0]
   else          : path = self.VVpWgW(self.VVp2lZ())
   if self.VVvjfY(path) > self.bigDirSize : FFlX3B(self, self.VVeaZX, title="Changing directory...")
   else           : self.VVeaZX()
 def VVeaZX(self):
  self["myMenu"].descent()
  self.VVH7je()
 def VVqK2V(self):
  if CFG.FileManagerExit.getValue() == "e": self.VV0WYH()
  else         : self.VVPGFd()
 def VV0WYH(self):
  if not FF9RVa(self):
   self.close("")
 def VVteLf(self):
  path = self.VVpWgW(self.VVp2lZ())
  if self.mode == self.VVBUn6:
   self.close(path)
  elif self.mode == self.VVWJV5:
   if os.path.isfile(path) : self.close(path)
   else     : FFD1yO(self, "Only .srt files", 1000)
 def VVqpVw(self):
  if not self.mode == self.VVWJV5:
   FFlX3B(self, self.VVka8Y, title="Calculating size ...")
 def VVka8Y(self):
  path = self.VVpWgW(self.VVp2lZ())
  param = self.VVLE27(path)
  if param:
   path, typeStr, typeChar, iNode, permUser, permGroup, permOther, permExtra, hLinks, owner, group, size, slTarget, slBroken, hLinkedFiles = param
   contents = totSize = freeSize = ""
   if typeChar == "d":
    exclude = "-type d \( -ipath '/media' -o -ipath '/mnt' -o -ipath '*boot*' -o -ipath '*/ba' \) -prune -o"
    result = FFj4HH("totDirs=$(find '%s' %s -type d -print | wc -l); totFiles=$(find '%s' %s ! -type d | wc -l); echo $totDirs','$totFiles" % (path, exclude, path, exclude))
    if iMatch("^[0-9]*,[0-9]*", result):
     parts = result.split(",")
     contents += "Directories\t: %s\n" % format(int(parts[0]), ',d')
     contents += "Files\t: %s\n"   % format(int(parts[1]), ',d')
    if os.path.ismount(path):
     typeStr += " (Mount)"
     totSize  = CC7ujK.VVgxIS(path)
     freeSize = CC7ujK.VVMZOV(path)
     size = totSize - freeSize
     totSize  = CC7ujK.VVw1Gr(totSize)
     freeSize = CC7ujK.VVw1Gr(freeSize)
    else:
     size = FFj4HH("find '%s' ! -type d -print0 2> /dev/null | xargs -0 ls -lsa 2> /dev/null | awk '{sum+=$6;} END {print(sum);}'" % path)
     size = int(size)
   usedSize = CC7ujK.VVw1Gr(size)
   if len(path) < 58 : pathTxt = path
   else    : pathTxt = "\n" + path
   pathTxt = FFkhYI(pathTxt, VVU8eD) + "\n"
   if slBroken : fileTime = self.VVBWS1(path)
   else  : fileTime = self.VVXrSR(path)
   def VVD6fO(key, val):
    return "%s\t: %s\n" % (key, str(val))
   txt = ""
   txt += VVD6fO("Path"    , pathTxt)
   txt += VVD6fO("Type"    , typeStr)
   if len(slTarget) > 0:
    txt += VVD6fO("Target"   , slTarget)
   if os.path.ismount(path):
    txt += VVD6fO("Total Size"   , "%s" % totSize)
    txt += VVD6fO("Used Size"   , "%s" % usedSize)
    txt += VVD6fO("Free Size"   , "%s" % freeSize)
   else:
    txt += VVD6fO("Size"    , "%s" % usedSize)
   txt += contents
   txt += "\n"
   txt += VVD6fO("Owner"    , owner)
   txt += VVD6fO("Group"    , group)
   txt += VVD6fO("Perm. (User)"  , permUser)
   txt += VVD6fO("Perm. (Group)"  , permGroup)
   txt += VVD6fO("Perm. (Other)"  , permOther)
   if len(permExtra) > 0:
    txt += VVD6fO("Perm. (Ext.)" , permExtra)
   txt += VVD6fO("iNode"    , iNode)
   txt += VVD6fO("Hard Links"   , hLinks)
   txt += fileTime
   if hLinkedFiles:
    txt += "\n%s\nHard Linked Files (files with same iNode)\n%s\n" % (VVZ1aI, VVZ1aI)
    txt += hLinkedFiles
   txt += self.VVFRWj(path)
  else:
   FFkYsE(self, "Cannot access information !")
  if len(txt) > 0:
   FFNEkd(self, txt)
 def VVLE27(self, path):
  path = path.strip()
  path = FFkEOw(path)
  result = FFj4HH("FILE='%s'; BROKEN=$(if [ ! -e \"$FILE\" ]; then echo 'yes'; else echo 'no'; fi); LINE=$(ls -lid \"$FILE\" 2> /dev/null); PARAM=$(echo $LINE | awk '{print($1\",\"$2\",\"$3\",\"$4\",\"$5\",\"$6}')); SLINK=$(echo $LINE | awk '{$1=$2=$3=$4=$5=$6=$7=$8=$9=\"\";print}'  | sed 's/ -> /,/g' | xargs); echo $PARAM','$BROKEN','$SLINK" % path)
  parts = result.split(",")
  if len(parts) > 7:
   iNode  = parts[0]
   perm  = parts[1]
   hLinks  = parts[2]
   owner  = parts[3]
   group  = parts[4]
   size  = parts[5]
   slBroken = parts[6]
   fName  = parts[7]
   slTarget = ""
   if len(parts) > 8:
    slTarget = parts[8]
   size = int(size)
   def VV937v(perm, start, end):
    val = perm[start : end]
    p  = { "---": "0" , "--x": "1" , "-w-": "2" , "-wx": "3" , "r--": "4" , "r-x": "5" , "rw-": "6" , "rwx": "7" , "+": "ACL" }
    if val in p : return "%s\t%s" % (val, p[val])
    else  : return val
   permUser = VV937v(perm, 1, 4)
   permGroup = VV937v(perm, 4, 7)
   permOther = VV937v(perm, 7, 10)
   permExtra = VV937v(perm, 10, 100)
   typeChar = perm[0:1]
   if   typeChar == "-": typeStr = "File"
   elif typeChar == "b": typeStr = "Block Device File"
   elif typeChar == "c": typeStr = "Character Device File"
   elif typeChar == "d": typeStr = "Directory"
   elif typeChar == "l": typeStr = "Symbolic Link"
   elif typeChar == "n": typeStr = "Network File"
   elif typeChar == "p": typeStr = "Named Pipe"
   elif typeChar == "s": typeStr = "Local Socket File"
   else    : typeStr = "Unknown"
   if "yes" in slBroken:
    slBroken = True
    typeStr  = "Broken Symlink (target not found)"
   else:
    slBroken = False
   hLinkedFiles = ""
   if typeChar != "d" and int(hLinks) > 1:
    hLinkedFiles = FF3DIX("find / -inum %s | grep -v /proc/" % iNode)
   return path, typeStr, typeChar, iNode, permUser, permGroup, permOther, permExtra, hLinks, owner, group, size, slTarget, slBroken, hLinkedFiles
  else:
   return None
 def VVFRWj(self, path):
  txt  = ""
  res  = FFj4HH("lsattr -d %s" % path)
  span = iSearch(r"([acdeijstuACDST-]{13})\s", res, IGNORECASE)
  if span:
   res = span.group(1)
   tDict = { "a": "Append only", "c": "Compressed", "d": "No dump", "e": "Extent format", "i": "Immutable", "j": "Data journalling", "s": "Secure deletion (s)", "t": "Tail-merging", "u": "Undeletable", "A": "No atime updates", "C": "No copy on write", "D": "Synchronous directory updates", "S": "Synchronous updates", "T": "Top of directory hierarchy", "h": "Huge file", "E": "Compression error", "I": "Indexed directory", "X": "Compression raw access", "Z": "Compressed dirty file" }
   lst = []
   for key, val in list(tDict.items()):
    if key in res:
     lst.append("%s  ( %s )\n" % (val, key))
   if lst:
    lst.sort()
    for item in lst:
     txt += "    %s" % item
    txt = "\n%s\n%s" % (FFkhYI("File Attributes:", VVyFMl), txt)
  return txt
 def VVXrSR(self, path):
  txt = "\n"
  txt += "Access time\t: %s\n" % FFcgMH(os.path.getatime(path))
  txt += "Modified time\t: %s\n" % FFcgMH(os.path.getmtime(path))
  txt += "Change time\t: %s\n" % FFcgMH(os.path.getctime(path))
  return txt
 def VVBWS1(self, path):
  txt = "\n"
  txt += "Access time\t: %s\n" % FFj4HH("stat -c %%x '%s'" % path).replace(".000000000", "")
  txt += "Modified time\t: %s\n" % FFj4HH("stat -c %%y '%s'" % path).replace(".000000000", "")
  txt += "Change time\t: %s\n" % FFj4HH("stat -c %%z '%s'" % path).replace(".000000000", "")
  return txt
 def VVpWgW(self, currentSel):
  currentDir  = self["myMenu"].VVpNPJ()
  if currentDir is None:
   path = currentSel
  elif currentSel is None:
   path = currentDir
  else:
   if currentSel == "/":
    path = currentDir
   else:
    if not self["myMenu"].VV5bSS():
     path = currentDir + currentSel
    else:
     if len(currentDir) > len(currentSel):
      path = currentDir
     else:
      path = currentSel
  return str(path)
 def VVp2lZ(self):
  sel = self["myMenu"].getSelection()
  if sel : return sel[0]
  else : return None
 def VVH7je(self):
  path = self.VVpWgW(self.VVp2lZ())
  self["myTitle"].setText("  " + path)
  if self["myTitle"].instance:
   textW = self["myTitle"].instance.calculateSize().width()
   if textW > self.maxTitleWidth:
    length = len(path)
    tmpPath = path[4:]
    for i in range(length, 40, -1):
     self["myTitle"].setText("  .." + tmpPath)
     textW = self["myTitle"].instance.calculateSize().width()
     if textW > self.maxTitleWidth: tmpPath = tmpPath[1:]
     else       : break
  self.VV2jwa()
  if self.mode == self.VVPhtE and len(path) > 0 : self["keyMenu"].show()
  else              : self["keyMenu"].hide()
  if self.mode == self.VVWJV5 and len(path) > 0 : self["keyInfo"].hide()
  else               : self["keyInfo"].show()
  if self.mode == self.VVWJV5:
   path = self.VVpWgW(self.VVp2lZ())
   if os.path.isfile(path) : self["keyGreen"].show()
   else     : self["keyGreen"].hide()
 def VV2jwa(self):
  if self.VVCxQv() : self["keyBlue"].show()
  else      : self["keyBlue"].hide()
 def VVshjT(self):
  if self.mode == self.VVPhtE:
   color1  = VVTdoW
   color2  = VVoTT6
   path  = self.VVpWgW(self.VVp2lZ())
   VV625J = []
   VV625J.append(("Properties", "properties"))
   if os.path.isdir(path):
    sepShown = False
    if not self.VVUhxC(path):
     sepShown = True
     VV625J.append(VVm77t)
     VV625J.append((color1 + "Archiving / Packaging", "VVPTnC_dir"))
    if self.VVJjkq(path):
     if not sepShown:
      VV625J.append(VVm77t)
     VV625J.append((color1 + "Read Backup information"   , "VV2v8i"  ))
     VV625J.append((color1 + "Compress Octagon Image (to zip)" , "VVKO5R" ))
   elif os.path.isfile(path):
    selFile = self.VVp2lZ()
    isArch = selFile.endswith((".tar", ".tar.gz", ".tar.bz2", "tar.xz", ".zip", ".rar"))
    if not isArch:
     VV625J.append((color1 + "Archive ...", "VVPTnC_file"))
    isText = False
    txt = ""
    if   isArch              : VV625J.extend(self.VVRaYd(path, True))
    elif selFile.endswith(".bootlogo.tar.gz")      : txt = "Replace Bootloader"
    elif selFile.endswith((".ipk", ".deb"))       : txt = "Package Tools"
    elif selFile.endswith((".jpg", ".jpeg", ".jpe", ".png", ".bmp")): txt = "View Picture"
    elif selFile.endswith(".m3u")         : VV625J.extend(self.VVbRkN(True))
    elif selFile.endswith(".sh"):
     VV625J.extend(self.VVVBRx(True))
     isText = True
    elif selFile.endswith((".py", ".xml", ".txt", ".htm", ".html", ".cfg", ".conf")) or not CC7ujK.VVFLgc(path):
     VV625J.append(VVm77t)
     VV625J.append((color2 + "View"     , "textView_def"))
     VV625J.append((color2 + "View (Select Encoder)" , "textView_enc"))
     VV625J.append((color2 + "Edit"     , "text_Edit" ))
     isText = True
    elif selFile.endswith(CC7ujK.VVMdDF()):
     VV625J.append(VVm77t)
     VV625J.append((color2 + "Add Media File to a Bouquet"    , "addMovieToBouquet"  ))
     VV625J.append((color2 + "Add all Media in Directory to a Bouquet" , "addAllMoviesToBouquet" ))
    if isText:
     VV625J.append((color1 + "Save as UTF-8 ..."      , "textSave_encUtf8"))
     VV625J.append((color1 + "Save as other Encoding ..."    , "textSave_encOthr"))
     VV625J.append((color1 + "Convert Line-Breaks to Unix Format..." , "VVc1NP" ))
    if len(txt) > 0:
     VV625J.append(VVm77t)
     VV625J.append((color1 + txt, "VVN6IY"))
   VV625J.append(VVm77t)
   VV625J.append(("Create SymLink", "VV9w2w"))
   if not self.VVUhxC(path):
    VV625J.append(("Rename"      , "VVCTNt" ))
    VV625J.append(("Copy"       , "copyFileOrDir" ))
    VV625J.append(("Move"       , "moveFileOrDir" ))
    VV625J.append((VVzZva + "DELETE" , "VVK3do" ))
    if fileExists(path):
     VV625J.append(VVm77t)
     perm = oct(os.stat(path).st_mode)[-3:]
     if   perm == "644" : show644, show755, show777 = False, True , True
     elif perm == "755" : show644, show755, show777 = True , False , True
     elif perm == "777" : show644, show755, show777 = True , True , False
     else    : show644, show755, show777 = True , True , True
     chmodTxt = "Change Permissions (from %s to " % perm
     if show644 : VV625J.append((chmodTxt + "644)", "chmod644"))
     if show755 : VV625J.append((chmodTxt + "755)", "chmod755"))
     if show777 : VV625J.append((chmodTxt + "777)", "chmod777"))
   c = VVNTmM
   VV625J.append(VVm77t)
   VV625J.append((c + "Create New File (in current directory)"  , "createNewFile" ))
   VV625J.append((c + "Create New Directory (in current directory)" , "createNewDir" ))
   fPath, fDir, fName = CC7ujK.VVa1tR(self)
   if fPath:
    VV625J.append(VVm77t)
    VV625J.append((color2 + "Go to Current Movie Dir", "VVxeMq"))
   FFuRfS(self, self.VV2doG, height=1050, title="Options", VV625J=VV625J, VVz2kc="#00101020", VVwpZm="#00101A2A")
 def VV2doG(self, item=None):
  if self.mode == self.VVPhtE:
   if item is not None:
    path = self.VVpWgW(self.VVp2lZ())
    selFile = self.VVp2lZ()
    if   item == "properties"    : self.VVqpVw()
    elif item == "VVPTnC_dir" : self.VVPTnC(path, True)
    elif item == "VVPTnC_file" : self.VVPTnC(path, False)
    elif item == "VV2v8i"  : self.VV2v8i(path)
    elif item == "VVKO5R" : self.VVKO5R(path)
    elif item == "VVF68F"  : self.VVF68F(path)
    elif item == "VVsOjY"  : self.VVsOjY(path)
    elif item.startswith("extract_")  : self.VVDGoF(path, selFile, item)
    elif item.startswith("script_")   : self.VVcZBg(path, selFile, item)
    elif item.startswith("m3u_")   : self.VVcTng(path, selFile, item)
    elif item.startswith("textView_def") : FFsdMh(self, path)
    elif item.startswith("textView_enc") : self.VV2gEO(path)
    elif item.startswith("text_Edit")  : FFlX3B(self, BF(CCYE8p, self, path), title="Opening File ...")
    elif item.startswith("textSave_encUtf8"): self.VVVIoN(path, "Save as UTF-8"   , True)
    elif item.startswith("textSave_encOthr"): self.VVVIoN(path, "Save as Other Encoding", False)
    elif item.startswith("VVc1NP") : self.VVc1NP(path)
    elif item == "addMovieToBouquet"  : self.VVZO24(path, False)
    elif item == "addAllMoviesToBouquet" : self.VVZO24(path, True)
    elif item == "VV9w2w"   : self.VV9w2w(path, selFile)
    elif item == "VVCTNt"   : self.VVCTNt(path, selFile)
    elif item == "copyFileOrDir"   : self.VVafXm(path, selFile, False)
    elif item == "moveFileOrDir"   : self.VVafXm(path, selFile, True)
    elif item == "VVK3do"   : self.VVK3do(path, selFile)
    elif item == "chmod644"     : self.VVVF6o(path, selFile, "644")
    elif item == "chmod755"     : self.VVVF6o(path, selFile, "755")
    elif item == "chmod777"     : self.VVVF6o(path, selFile, "777")
    elif item == "createNewFile"   : self.VVNlnw(path, True)
    elif item == "createNewDir"    : self.VVNlnw(path, False)
    elif item == "VVxeMq"   : self.VVxeMq()
    elif item == "VVN6IY"    : self.VVN6IY()
    else         : self.close()
 def VVN6IY(self):
  if self.mode == self.VVWJV5:
   return
  selFile = self.VVp2lZ()
  path  = self.VVpWgW(selFile)
  if os.path.isfile(path):
   VV6D3C = []
   category = self["myMenu"].VVK76x(path)
   t = "Playing Media ..."
   if   selFile.endswith(".bootlogo.tar.gz") : self.VVx56s(selFile, "Replace Bootloader ?", "mount -rw /boot -o remount", "sleep 3","tar -xzvf '" + path + "' -C /", "mount -ro /boot -o remount")
   elif category == "pic"      : CCd1mn.VVQ7Bd(self, path)
   elif category == "txt"      : FFsdMh(self, path)
   elif category in ("tar", "zip", "rar")  : self.VVVWRn(path, selFile)
   elif category == "scr"      : self.VVCDH0(path, selFile)
   elif category == "m3u"      : self.VVMZSq(path, selFile)
   elif category in ("ipk", "deb")    : self.VVPYA1(path, selFile)
   elif category == "mus"      : FFlX3B(self, BF(self.VVHl4q,self, path), title=t)
   elif category == "mov"      : FFlX3B(self, BF(self.VVHl4q,self, path), title=t)
   elif not CC7ujK.VVFLgc(path) : FFsdMh(self, path)
 def VVEt59(self):
  if self["keyBlue"].getVisible():
   VVvytR = self.VVCxQv()
   if VVvytR:
    path = self.VVpWgW(self.VVp2lZ())
    enableGreenBtn = False if path in self.VVCxQv() else True
    newList = []
    for line in VVvytR:
     newList.append((line, line))
    VVBfJP  = ("Delete"    , self.VVDVCd    )
    VVmKbI  = ("Add Current Dir"   , BF(self.VVOdrR, path) ) if enableGreenBtn else None
    VVJ5GS = ("Move Up"     , self.VVkwaD    )
    VVme6L  = ("Move Down"   , self.VVFcJV    )
    self.bookmarkMenu = FFuRfS(self, self.VV4gFk, width=1200, title="Bookmarks", VV625J=newList, minRows=10 ,VVBfJP=VVBfJP, VVmKbI=VVmKbI, VVJ5GS=VVJ5GS, VVme6L=VVme6L, VVz2kc="#00000022", VVwpZm="#00000022")
 def VVDVCd(self, menuInstance=None, path=None):
  VVvytR = self.VVCxQv()
  if VVvytR:
   while path in VVvytR:
    VVvytR.remove(path)
   self.VVZsP2(VVvytR)
  if self.bookmarkMenu:
   self.bookmarkMenu.VVIzx9(VVvytR)
   self.bookmarkMenu.VVHNuG(("Add Current Dir", BF(self.VVOdrR, path)))
  else:
   FFD1yO(self, "Removed", 800)
  self.VV2jwa()
 def VVOdrR(self, path, menuInstance=None, item=None):
  VVvytR = self.VVCxQv()
  if len(VVvytR) >= self.VVVgDr:
   FFkYsE(SELF, "Max bookmarks reached (max=%d)." % self.VVVgDr)
  elif not path in VVvytR:
   newList = [path] + VVvytR
   self.VVZsP2(newList)
   if self.bookmarkMenu:
    self.bookmarkMenu.VVIzx9(newList)
    self.bookmarkMenu.VVHNuG()
   else:
    FFD1yO(self, "Added", 800)
  self.VV2jwa()
 def VVkwaD(self, VVp2lZObj, path):
  if self.bookmarkMenu:
   VVvytR = self.bookmarkMenu.VValrG(True)
   if VVvytR:
    self.VVZsP2(VVvytR)
 def VVFcJV(self, VVp2lZObj, path):
  if self.bookmarkMenu:
   VVvytR = self.bookmarkMenu.VValrG(False)
   if VVvytR:
    self.VVZsP2(VVvytR)
 def VV4gFk(self, folder=None):
  if folder:
   folder = FF0WrY(folder)
   self["myMenu"].VVimWq(folder)
   self["myMenu"].moveToIndex(0)
  self.VVH7je()
 def VVCxQv(self):
  line = CFG.browserBookmarks.getValue().strip()
  while " ," in line : line.replace(" ,", ",")
  while ", " in line : line.replace(", ", ",")
  if   "," in line : return line.split(",")
  elif len(line) > 0 : return [line]
  else    : return []
 def VVOR1X(self):
  return True if VVCxQv() else False
 def VVZsP2(self, VVvytR):
  line = ",".join(VVvytR)
  FFnT3A(CFG.browserBookmarks, line)
 def VVe5uc(self, path):
  if fileExists(path):
   fDir  = FF0WrY(os.path.dirname(path))
   if fDir:
    self["myMenu"].VVimWq(fDir)
   fName = os.path.basename(path)
   for ndx, item in enumerate(self["myMenu"].list):
    colNum = 1
    if fName == item[0][0]:
     self["myMenu"].moveToIndex(ndx)
     break
  else:
   FFD1yO(self, "Not found", 1000)
 def VVxeMq(self, chDir=True):
  fPath, fDir, fName = CC7ujK.VVa1tR(self)
  self.VVe5uc(fPath)
 def VVkrPQ(self):
  path = self.VVpWgW(self.VVp2lZ())
  isAdd = False if path in self.VVCxQv() else True
  dirTxt = "Selected" if os.path.isdir(path) else "Current"
  VV625J = []
  VV625J.append(   ("Find Files ..."      , "find" ))
  VV625J.append(   ("Sort ..."        , "sort" ))
  VV625J.append(VVm77t)
  if isAdd: VV625J.append( ("Add %s Dir to Bookmarks" % dirTxt  , "addBM" ))
  else : VV625J.append( ("Remove %s Dir from Bookmarks" % dirTxt, "remBM" ))
  VV625J.append(VVm77t)
  VV625J.append(   ('Set %s Dir as "Startup Dir"' % dirTxt , "start" ))
  FFuRfS(self, BF(self.VVPkKi, path), width=750, title="More Options", VV625J=VV625J, VVz2kc="#00221111", VVwpZm="#00221111")
 def VVPkKi(self, path, item):
  if item:
   if   item == "find" : self.VVi8BN(path)
   elif item == "sort" : self.VVpCzB()
   elif item == "addBM": self.VVOdrR(path)
   elif item == "remBM": self.VVDVCd(None, path)
   elif item == "start": self.VVejIm(path)
 def VVi8BN(self, path):
  VV625J = []
  VV625J.append(("Find in Current Directory"    , "findCur"  ))
  VV625J.append(("Find in Current Directory (recursive)" , "findCurR" ))
  VV625J.append(("Find in all Storage Systems"    , "findAll"  ))
  FFuRfS(self, BF(self.VVp0xy, path), width=700, title="Find File/Pattern", VV625J=VV625J, VVeYEo=True, VVvQ6U=True, VVz2kc="#00221111", VVwpZm="#00221111")
 def VVp0xy(self, path, item):
  if item:
   title, item, ndx = item
   if   item == "findCur" : self.VVkXxM(0, path, title)
   elif item == "findCurR" : self.VVkXxM(1, path, title)
   elif item == "findAll" : self.VVkXxM(2, path, title)
 def VVkXxM(self, mode, path, title):
  if CFG.lastFileManFindPatt.getValue(): txt = CFG.lastFileManFindPatt.getValue()
  else         : txt = "*.ipk"
  FFbRXK(self, BF(self.VVZpYT, mode, path, title), defaultText=txt, title=title, message="Enter Name/Pattern:")
 def VVZpYT(self, mode, path, title, filePatt):
  if filePatt is not None:
   filePatt = filePatt.strip()
   FFnT3A(CFG.lastFileManFindPatt, filePatt)
   badLst = filePatt.replace(" ", "") in ("*.*", "*.", ".*")
   if not filePatt : FFD1yO(self, "No entery", 1500)
   elif badLst  : FFD1yO(self, "Too many file !", 1500)
   else   : FFlX3B(self, BF(self.VVh9YN, mode, path, title, filePatt), title="Searching ...", clearMsg=False)
 def VVh9YN(self, mode, path, title, filePatt):
  FFD1yO(self)
  lst = FFiGf6(FFRIHI("find '%s' -type f -iname '%s' %s" % ("/" if mode==2 else path, filePatt, "-maxdepth 1" if mode == 0 else "")))
  if lst:
   if len(lst) == 1 and lst[0] == VVCYwM:
    FFkYsE(self, VVCYwM)
   else:
    for ndx, path in enumerate(lst):
     lst[ndx] = (os.path.basename(path), os.path.dirname(path))
    lst.sort(key=lambda x: x[0].lower())
    header = ("File", "Directory" )
    widths = (50  , 50   )
    VV01dN = (""     , self.VVZeoY , [])
    VV3th8 = ("Go to File Location", self.VVn4KW  , [])
    FF1dQ4(self, None, title="%s : %s" % (title, filePatt), header=header, VVvytR=lst, VVoJsQ=widths, VVmp7B=26, VV01dN=VV01dN, VV3th8=VV3th8)
  else:
   FFD1yO(self, "Not found !", 2000)
 def VVn4KW(self, VVcpnp, title, txt, colList):
  path = os.path.join(colList[1], colList[0])
  if fileExists(path):
   VVcpnp.cancel()
   self.VVe5uc(path)
  else:
   FFD1yO(VVcpnp, "Path not found !", 1000)
 def VVZeoY(self, VVcpnp, title, txt, colList):
  txt = "%s\n%s\n\n" % (FFkhYI("File:"  , VVoTT6), colList[0])
  txt += "%s\n%s"  % (FFkhYI("Directory:", VVoTT6), FF0WrY(colList[1]))
  FFNEkd(VVcpnp, txt, title=title)
 def VVpCzB(self):
  nameAlpMode, nameAlpTxt, nameNumMode, nameNumTxt , dateMode, dateTxt, typeMode, typeTxt, txt = self["myMenu"].VVOIhF()
  VV625J = []
  VV625J.append(("Name\t%s" % nameAlpTxt, "nameAlp"))
  VV625J.append(("Name\t%s" % nameNumTxt, "nameNum"))
  VV625J.append(("Date\t%s" % dateTxt, "dateAlp"))
  VV625J.append(("Type\t%s" % typeTxt, "typeAlp"))
  VVme6L = ("Mix", BF(self.VV95fg, True))
  FFuRfS(self, BF(self.VVLtJp, False), barText=txt, width=650, title="Sort Options", VV625J=VV625J, VVme6L=VVme6L, VVvQ6U=True, VVz2kc="#00221111", VVwpZm="#00221111")
 def VV95fg(self, isMix, menuInstance, item):
  self.VVLtJp(True, item)
 def VVLtJp(self, isMix, item):
  if item:
   nameAlpMode, nameAlpTxt, nameNumMode, nameNumTxt , dateMode, dateTxt, typeMode, typeTxt, txt = self["myMenu"].VVOIhF()
   title = "Sorting ... "
   if   item == "nameAlp": FFlX3B(self, BF(self["myMenu"].VV94Wp, nameAlpMode, isMix, False), title=title)
   elif item == "nameNum": FFlX3B(self, BF(self["myMenu"].VV94Wp, nameNumMode, isMix, True ), title=title)
   elif item == "dateAlp": FFlX3B(self, BF(self["myMenu"].VV94Wp, dateMode , isMix, False), title=title)
   elif item == "typeAlp": FFlX3B(self, BF(self["myMenu"].VV94Wp, typeMode , isMix, False), title=title)
 def VVejIm(self, path):
  if not os.path.isdir(path):
   path = FFMjyS(path, True)
  FFnT3A(CFG.browserStartPath, path)
  FFD1yO(self, "Done", 500)
 def VVx56s(self, selFile, VVSidL, command):
  FFMIbO(self, BF(FFfbee, self, command, VVIwP9=self.VVI84O), "%s\n\n%s" % (VVSidL, selFile))
 def VVRaYd(self, path, calledFromMenu):
  destPath = self.VVvGz7(path)
  lastPart = FFqDmh(destPath)
  VV625J = []
  if calledFromMenu:
   VV625J.append(VVm77t)
   color = VVoTT6
  else:
   color = ""
  VV625J.append((color + "List Archived Files"          , "extract_listFiles" ))
  VV625J.append(VVm77t)
  VV625J.append((color + 'Extract to "%s"' % lastPart        , "extract_toDir"  ))
  VV625J.append((color + 'Extract to Root Directory "/"  (recommended for plugins)' , "extract_toRoot"  ))
  VV625J.append((color + "Extract Here"            , "extract_here"  ))
  if iTar and iZip:
   if path.endswith(".zip"):
    if not calledFromMenu: VV625J.append(VVm77t)
    VV625J.append((color + "Convert .zip to .tar.gz"       , "VVF68F" ))
   elif path.endswith(".tar.gz"):
    if not calledFromMenu: VV625J.append(VVm77t)
    VV625J.append((color + "Convert .tar.gz to .zip"       , "VVsOjY" ))
  return VV625J
 def VVVWRn(self, path, selFile):
  FFuRfS(self, BF(self.VVDGoF, path, selFile), title="Compressed File Options", VV625J=self.VVRaYd(path, False))
 def VVDGoF(self, path, selFile, item=None):
  if item is not None:
   parent  = FFMjyS(path, False)
   destPath = self.VVvGz7(path)
   lastPart = FFqDmh(destPath)
   cmd   = ""
   if item == "extract_listFiles":
    linux_sep = "echo -e %s;" % VVZ1aI
    cmd += linux_sep
    if path.endswith(".zip"):
     cmd += FFqoRI("unzip", "unzip", "Unzip")
     cmd += 'if [ "$allOK" -eq "1" ]; then '
     cmd += " echo '';"
     cmd += " unzip -l '%s';" % path
     cmd += "fi;"
    elif path.endswith(".rar"):
     cmd += FFqoRI("unrar", "unrar", "Unrar")
     cmd += 'if [ "$allOK" -eq "1" ]; then '
     cmd += " echo '';"
     cmd += " unrar l '%s';" % path
     cmd += "fi;"
    else:
     cmd += "echo -e 'Archive:\n%s\n';" % path
     cmd += "echo -e '%s\n--- Contents:\n%s';" % (VVZ1aI, VVZ1aI)
     cmd += "tar -tf '%s';" % path
    cmd += "echo '';"
    cmd += linux_sep
    FFCa80(self, cmd)
   elif path.endswith(".zip"):
    if item == "VVF68F" : self.VVF68F(path)
    else       : self.VVV2MU(item, path, parent, destPath, "Unzip this file ?\n\n%s" % selFile)
   elif item == "VVsOjY" and path.endswith(".tar.gz"):
    self.VVsOjY(path)
   elif path.endswith(".rar"):
    self.VVMaP0(item, path, parent, destPath, "Unrar this file ?\n\n%s" % selFile)
   elif item == "extract_toDir":
    cmd += "cd '%s';" % parent
    cmd += FFxtg8("mkdir '%s'"   % lastPart) + ";"
    cmd += 'if [ -d "%s" ]; then '  % lastPart
    cmd += " tar -xvf '%s' -C '%s';" % (path, lastPart)
    cmd += "else"
    cmd += " echo -e 'Cannot create directory:\n%s';" % lastPart
    cmd += "fi"
    self.VVx56s(selFile, 'Extract to "%s" ?' % lastPart  , cmd)
   elif item == "extract_toRoot":
    cmd += "cd '%s';" % parent
    cmd += "tar -xvf '%s' -C /" % path
    self.VVx56s(selFile, 'Extract to Root Directory ("/") ?' , cmd)
   elif item == "extract_here":
    parent = FFMjyS(path, False)
    cmd += "cd '%s';" % parent
    cmd += "tar -xvf '%s'" % path
    self.VVx56s(selFile, "Extract Here ?"      , cmd)
 def VVvGz7(self, path, addSep=False):
  if   path.endswith(".tar")  : extLen = 4
  elif path.endswith(".tar.gz") : extLen = 7
  elif path.endswith(".tar.xz") : extLen = 7
  elif path.endswith(".tar.bz2") : extLen = 8
  elif path.endswith(".zip")  : extLen = 4
  elif path.endswith(".rar")  : extLen = 4
  else       : extLen = 0
  return path[:-extLen]
 def VVV2MU(self, item, path, parent, destPath, VVSidL):
  FFMIbO(self, BF(self.VV0SM2, item, path, parent, destPath), VVSidL)
 def VV0SM2(self, item, path, parent, destPath):
  archCmd = ""
  if item == "extract_toDir":
   archCmd += " cd '%s';" % parent
   archCmd += " [ ! -d '%s' ] && mkdir '%s';" % (destPath, destPath)
  elif item == "extract_toRoot":
   destPath = "/"
  elif item == "extract_here":
   destPath = parent
  archCmd += " unzip -l '%s';"   % path
  archCmd += " unzip -o -q '%s' -d '%s';" % (path, destPath)
  sep   = " echo -e '%s\n';" % VVZ1aI
  cmd  = FFqoRI("unzip", "unzip", "Unzip")
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd +=   sep
  cmd +=   archCmd
  cmd +=   sep
  cmd += " echo -e 'Done.\n\nFiles extracted to:\n%s\n' %s;" % (destPath, FF95sl(destPath, VV9cEK))
  cmd +=   sep
  cmd += "fi;"
  FFKqND(self, cmd, VVIwP9=self.VVI84O)
 def VVMaP0(self, item, path, parent, destPath, VVSidL):
  FFMIbO(self, BF(self.VVdPYB, item, path, parent, destPath), VVSidL)
 def VVdPYB(self, item, path, parent, destPath):
  archCmd = ""
  if   item == "extract_toDir" : destPath = FF0WrY(destPath)
  elif item == "extract_toRoot" : destPath = "/"
  elif item == "extract_here"  : destPath = parent
  archCmd += " unrar x '%s' '%s';" % (path, destPath)
  sep   = " echo -e '%s\n';" % VVZ1aI
  cmd  = FFqoRI("unrar", "unrar", "Unrar")
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd +=   sep
  cmd +=   archCmd
  cmd +=   sep
  cmd += " echo -e 'Done.\n\nFiles extracted to:\n%s\n' %s;" % (destPath, FF95sl(destPath, VV9cEK))
  cmd +=   sep
  cmd += "fi;"
  FFKqND(self, cmd, VVIwP9=self.VVI84O)
 def VVVBRx(self, addSep=False):
  VV625J = []
  if addSep:
   VV625J.append(VVm77t)
  VV625J.append((VVoTT6 + "View Script File"  , "script_View"  ))
  VV625J.append((VVoTT6 + "Execute Script File" , "script_Execute" ))
  VV625J.append((VVoTT6 + "Edit"     , "script_Edit" ))
  return VV625J
 def VVCDH0(self, path, selFile):
  FFuRfS(self, BF(self.VVcZBg, path, selFile), title="Script File Options", VV625J=self.VVVBRx())
 def VVcZBg(self, path, selFile, item=None):
  if item is not None:
   if   item == "script_View"  : FFsdMh(self, path)
   elif item == "script_Execute" : self.VVx56s(selFile, "Run Script File ?", "chmod +x '%s'; '%s'" % (path, path))
   elif item == "script_Edit"  : CCYE8p(self, path)
 def VVbRkN(self, addSep=False):
  VV625J = []
  if addSep:
   VV625J.append(VVm77t)
  VV625J.append((VVoTT6 + "Browse IPTV Channels"  , "m3u_Browse" ))
  VV625J.append((VVoTT6 + "Edit"      , "m3u_Edit" ))
  VV625J.append((VVoTT6 + "View"      , "m3u_View" ))
  return VV625J
 def VVMZSq(self, path, selFile):
  FFuRfS(self, BF(self.VVcTng, path, selFile), title="M3U/M3U8 File Options", VV625J=self.VVbRkN())
 def VVcTng(self, path, selFile, item=None):
  if item is not None:
   if   item == "m3u_Browse" : FFlX3B(self, BF(self.session.open, CCqQHV, m3uOrM3u8File=path))
   elif item == "m3u_Edit"  : CCYE8p(self, path)
   elif item == "m3u_View"  : FFsdMh(self, path)
 def VV2gEO(self, path):
  if fileExists(path) : FFlX3B(self, BF(CClXbe.VVq1FC, self, path, BF(self.VVpygW, path)), title="Loading Codecs ...", clearMsg=False)
  else    : FFAVqd(self, path)
 def VVpygW(self, path, item=None):
  if item:
   FFsdMh(self, path, encLst=item)
 def VVVIoN(self, path, title, asUtf8):
  if fileExists(path) : FFlX3B(self, BF(CClXbe.VVq1FC, self, path, BF(self.VVNpZu, path, title, asUtf8), title="Original Encoding"), clearMsg=False, title="Loading Codecs ...")
  else    : FFAVqd(self, path)
 def VVNpZu(self, path, title, asUtf8, fromEnc=None):
  if fromEnc:
   if asUtf8 : self.VV6WjF(path, title, fromEnc, "UTF-8")
   else  : CClXbe.VVq1FC(self, path,  BF(self.VV6WjF, path, title, fromEnc), onlyWorkingEnc=False, title="Convert to Encoding")
 def VV6WjF(self, path, title, fromEnc, toEnc):
  if toEnc:
   if fileExists(path):
    try:
     outFile = "%s_%s%s" % (path, toEnc, os.path.splitext(path)[1])
     with ioOpen(path, "r", encoding=fromEnc) as src:
      BLOCK_1MB = 1048576
      with ioOpen(outFile, "w", encoding=toEnc) as dest:
       while True:
        cont = src.read(BLOCK_1MB)
        if not cont:
         break
        dest.write(cont)
      txt  = FFkhYI("Successful\n\n", VV9cEK)
      txt += FFkhYI("From Encoding (%s):\n" % fromEnc, VVdWFT)
      txt += "%s\n\n" % path
      txt += FFkhYI("To Encoding (%s):\n" % toEnc, VVdWFT)
      txt += "%s\n\n" % outFile
      FFNEkd(self, txt, title=title)
    except:
     FFkYsE(self, 'Cannot encode the file:\n%s\n\nFrom "%s" to "%s"' % (path, fromEnc, toEnc), title=title)
   else:
    FFD1yO(self, "Cannot open file", 2000)
  self.VVI84O()
 def VVc1NP(self, path):
  title = "File Line-Break Conversion"
  FFMIbO(self, BF(self.VVPEtK, path, title), "Convert Line-Breaks to Unix for the file:\n\n%s" % path, title=title)
 def VVPEtK(self, path, title):
  if fileExists:
   with open(path, 'rb') as f:
    data = f.read()
   done = False
   if data:
    CRLF, LF, To = b"\r\n", b"\r", b"\n"
    totCRLF = data.count(CRLF)
    totLF = data.count(LF)
    if totCRLF or totLF:
     done = True
     with open(path, 'wb') as f:
      f.write(data.replace(CRLF, To).replace(LF, To))
   if done : txt = "%s\n\n%s" % (FFkhYI("File converted:", VV9cEK), path)
   else : txt = "Nothing to convert in:\n\n%s" % path
   FFewCE(self, txt, title=title)
  else:
   FFAVqd(self, path, title=title)
 def VVVF6o(self, path, selFile, newChmod):
  FFMIbO(self, BF(self.VVDgDB, path, newChmod), "Change Permission to %s ?\n\n%s" % (newChmod, selFile))
 def VVDgDB(self, path, newChmod):
  cmd = "chmod %s '%s' %s" % (newChmod, path, VVrML3)
  result = FFj4HH(cmd)
  if result == "Successful" : FFewCE(self, result)
  else      : FFkYsE(self, result)
 def VV9w2w(self, path, selFile):
  parent = FFMjyS(path, False)
  self.session.openWithCallback(self.VVtHpx, BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx=parent, VVrLQt="Create Symlink here"))
 def VVtHpx(self, newPath):
  if len(newPath) > 0:
   target = self.VVpWgW(self.VVp2lZ())
   target = FFkEOw(target)
   linkName = FFqDmh(target)
   dotIndex = linkName.find(".")
   if dotIndex > -1:
    linkName = linkName[:dotIndex]
   newPath = FF0WrY(newPath)
   link = newPath + linkName
   if   os.path.islink(link) : txt = ""
   elif os.path.ismount(link) : txt = "MOUNT:"
   elif os.path.isfile(link) : txt = "FILE:"
   elif os.path.isdir(link) : txt = "DIRECTORY:"
   else      : txt = ""
   if len(txt) > 0:
    FFkYsE(self, "Name already used for %s\n\n%s" % (txt, link))
    return
   txt  = "-> TARGET:\n%s\n\n" % target
   txt += "<- LINK:\n%s"  % link
   FFMIbO(self, BF(self.VV9YvF, target, link), "Create Soft Link ?\n\n%s" % txt, VVUEfx=True)
 def VV9YvF(self, target, link):
  cmd = "LINK='%s'; if [ -e $LINK ]; then rm $LINK; fi; ln -sfv '%s' '%s' &>/dev/null %s" % (link, target, link, VVrML3)
  result = FFj4HH(cmd)
  if result == "Successful" : FFewCE(self, result)
  else      : FFkYsE(self, result)
 def VVCTNt(self, path, selFile):
  lastPart = FFqDmh(path)
  FFbRXK(self, BF(self.VVZeHE, path, selFile), title="Rename", defaultText=lastPart, message="Enter New Name:")
 def VVZeHE(self, path, selFile, VVVomg):
  if VVVomg:
   parent = FFMjyS(path, True)
   if os.path.isdir(path):
    path = FFkEOw(path)
   newName = parent + VVVomg
   cmd = "mv '%s' '%s' %s" % (path, newName, VVrML3)
   if VVVomg:
    if selFile != VVVomg:
     message = "%s\n\nTo:\n\n%s" % (path, newName)
     FFMIbO(self, BF(self.VVKYTX, cmd), message, title="Rename file?")
    else:
     FFkYsE(self, "Cannot use same name!", title="Rename")
 def VVKYTX(self, cmd):
  result = FFj4HH(cmd)
  if "Fail" in result:
   FFkYsE(self, result)
  self.VVI84O()
 def VVafXm(self, path, selFile, isMove):
  if isMove : VVrLQt = "Move to here"
  else  : VVrLQt = "Paste here"
  parent = FFMjyS(path, False)
  self.session.openWithCallback(BF(self.VV3cSA, isMove, path, selFile)
         , BF(CC7ujK, mode=CC7ujK.VVBUn6, VVKDYx=parent, VVrLQt=VVrLQt))
 def VV3cSA(self, isMove, path, selFile, newPath):
  if len(newPath) > 0:
   lastPart = FFqDmh(path)
   if os.path.isdir(path):
    path = FFkEOw(path)
   newPath = FF0WrY(newPath)
   dest = newPath + lastPart
   if os.path.isdir(path) and os.path.isdir(dest):
    if isMove:
     FFkYsE(self, 'Same directory already exists:\n\n%s\n\n( Try to copy then delete the source )' % dest)
     return
    else:
     dest = newPath
   if isMove : action, cmd = "Move", "mv"
   else  : action, cmd = "Copy", "cp -rf"
   txt  = "%s\t: %s\n" % (action, lastPart)
   txt += "to\t: %s\n\n" % newPath
   if fileExists(dest) : txt += "%s (overwrite) ?" % action
   else    : txt += "%s now ?"   % action
   if not path == dest:
    cmd = "RES=$(%s '%s' '%s') && echo Successful || echo $RES" % (cmd, path, dest)
    FFMIbO(self, BF(FFuCjo, self, cmd, VVIwP9=self.VVI84O), txt, VVUEfx=True)
   else:
    FFkYsE(self, "Cannot %s to same directory !" % action.lower())
 def VVK3do(self, path, fileName):
  path = FFkEOw(path)
  if   os.path.islink(path) : pathType = "SymLink"
  elif os.path.isfile(path) : pathType = "File"
  elif os.path.isdir(path) : pathType = "Directory"
  elif os.path.ismount(path) : pathType = "Mount"
  else      : pathType = ""
  FFMIbO(self, BF(self.VVkkoh, path), "Delete %s ?\n\n%s" % (pathType, path))
 def VVkkoh(self, path):
  opt = "-f"
  if os.path.isdir(path):
   opt = "-r"
  os.system("chattr -iR '%s' > /dev/null 2>&1; rm %s '%s'" % (path, opt, path))
  self.VVI84O()
 def VVUhxC(self, path):
  if self["myMenu"].l.getCurrentSelectionIndex() == 0      : return True
  elif self["myMenu"].mountpoints and path in self["myMenu"].mountpoints : return True
  elif not VVF5vz and path in [ "/DEBIAN/"
          , "/bin/"
          , "/boot/"
          , "/dev/"
          , "/etc/"
          , "/hdd/"
          , "/home/"
          , "/lib/"
          , "/media/"
          , "/mnt/"
          , "/network/"
          , "/proc/"
          , "/run/"
          , "/sbin/"
          , "/sys/"
          , "/tmp/"
          , "/usr/"
          , "/var/"]     : return True
  return False
 def VVNlnw(self, path, isFile):
  dirName = FF0WrY(os.path.dirname(path))
  if isFile : objName, VVVomg = "File"  , self.edited_newFile
  else  : objName, VVVomg = "Directory" , self.edited_newDir
  title="Create New %s" % objName
  FFbRXK(self, BF(self.VVDeNd, dirName, isFile, title), title=title, defaultText=VVVomg, message="Enter %s Name:" % objName)
 def VVDeNd(self, dirName, isFile, title, VVVomg):
  if VVVomg:
   if isFile : self.edited_newFile = VVVomg
   else  : self.edited_newDir  = VVVomg
   path = dirName + VVVomg
   if not fileExists(path):
    if isFile : cmd = "touch '%s' %s" % (path, VVrML3)
    else  : cmd = "mkdir '%s' %s" % (path, VVrML3)
    result = FFj4HH(cmd)
    if "Fail" in result:
     FFkYsE(self, result)
    self.VVI84O()
   else:
    FFkYsE(self, "Name already exists !\n\n%s" % path, title)
 def VVPYA1(self, path, selFile):
  VV625J = []
  VV625J.append(("List Package Files"          , "VVIXRJ"     ))
  VV625J.append(("Package Information"          , "VVcP4V"     ))
  VV625J.append(VVm77t)
  VV625J.append(("Install Package"           , "VVoFvy_CheckVersion" ))
  VV625J.append(("Install Package (force reinstall)"      , "VVoFvy_ForceReinstall" ))
  VV625J.append(("Install Package (force overwrite)"      , "VVoFvy_ForceOverwrite" ))
  VV625J.append(("Install Package (force downgrade)"      , "VVoFvy_ForceDowngrade" ))
  VV625J.append(("Install Package (ignore failed dependencies)"    , "VVoFvy_IgnoreDepends" ))
  VV625J.append(VVm77t)
  VV625J.append(("Remove Related Package"         , "VVGUJh_ExistingPackage" ))
  VV625J.append(("Remove Related Package (force remove)"     , "VVGUJh_ForceRemove"  ))
  VV625J.append(("Remove Related Package (ignore failed dependencies)"  , "VVGUJh_IgnoreDepends" ))
  VV625J.append(VVm77t)
  VV625J.append(("Extract Files"           , "VVPsqa"     ))
  VV625J.append(("Unbuild Package"           , "VVnkCQ"     ))
  FFuRfS(self, BF(self.VVdrPY, path, selFile), VV625J=VV625J)
 def VVdrPY(self, path, selFile, item=None):
  if item is not None:
   if   item == "VVIXRJ"      : self.VVIXRJ(path, selFile)
   elif item == "VVcP4V"      : self.VVcP4V(path)
   elif item == "VVoFvy_CheckVersion"  : self.VVoFvy(path, selFile, VV4pye     )
   elif item == "VVoFvy_ForceReinstall" : self.VVoFvy(path, selFile, VVEoQq )
   elif item == "VVoFvy_ForceOverwrite" : self.VVoFvy(path, selFile, VVKrAC )
   elif item == "VVoFvy_ForceDowngrade" : self.VVoFvy(path, selFile, VViRav )
   elif item == "VVoFvy_IgnoreDepends" : self.VVoFvy(path, selFile, VVDDR8 )
   elif item == "VVGUJh_ExistingPackage" : self.VVGUJh(path, selFile, VVvtgi     )
   elif item == "VVGUJh_ForceRemove"  : self.VVGUJh(path, selFile, VVjAHQ  )
   elif item == "VVGUJh_IgnoreDepends"  : self.VVGUJh(path, selFile, VVJ3c9 )
   elif item == "VVPsqa"     : self.VVPsqa(path, selFile)
   elif item == "VVnkCQ"     : self.VVnkCQ(path, selFile)
   else           : self.close()
 def VVIXRJ(self, path, selFile):
  if FFvG4M("ar") : cmd = "allOK='1';"
  else    : cmd  = FFr1Fs()
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd += "  echo -e '%s\nFile:\n%s\n';" % (VVZ1aI, path)
  cmd += "  echo -e '%s\n--- Contents:\n%s';" % (VVZ1aI, VVZ1aI)
  cmd += "  ar -t '%s';" % path
  cmd += "fi;"
  FFusMt(self, cmd, VVIwP9=self.VVI84O)
 def VVPsqa(self, path, selFile):
  lastPart = FFqDmh(path)
  dest  = FFMjyS(path, True) + selFile[:-4]
  cmd  =  FFr1Fs()
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd +=    FFxtg8("mkdir '%s'" % dest) + ";"
  cmd +=    FFxtg8("cd '%s'" % dest) + ";"
  cmd += "  echo 'Extrcting files ...';"
  cmd += "  ar -xo '%s';" % path
  cmd += "  echo -e 'Done.\n';"
  cmd += "  echo -e 'Output Directory:\n%s' %s;" % (dest, FF95sl(dest, VV9cEK))
  cmd += "fi;"
  FFfbee(self, cmd, VVIwP9=self.VVI84O)
 def VVnkCQ(self, path, selFile):
  if path.endswith((".ipk", ".deb")) : VVHZbd = os.path.splitext(path)[0]
  else        : VVHZbd = path + "_"
  if path.endswith(".deb")   : VV4Zxm = "DEBIAN"
  else        : VV4Zxm = "CONTROL"
  cmd  = FFr1Fs()
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd += "  rm -r '%s' %s;"   % (VVHZbd, FFYn0Q())
  cmd += "  mkdir '%s';"    % VVHZbd
  cmd += "  CONTPATH='%s/%s';"  % (VVHZbd, VV4Zxm)
  cmd += "  mkdir $CONTPATH;"
  cmd += "  cd '%s';"     % VVHZbd
  cmd += "  echo 'Unpacking ...';"
  cmd += "  ar -x '%s';"    % path
  cmd += "  FILE='%s/data.tar.gz';    [ -f $FILE ] && tar -xzf $FILE -C '%s'      && rm -f $FILE;" % (VVHZbd, VVHZbd)
  cmd += "  FILE='%s/control.tar.gz'; [ -f $FILE ] && tar -xzf $FILE -C $CONTPATH && rm -f $FILE;" %  VVHZbd
  cmd += "  FILE='%s/data.tar.xz';    [ -f $FILE ] && tar -xJf $FILE -C '%s'      && rm -f $FILE;" % (VVHZbd, VVHZbd)
  cmd += "  FILE='%s/control.tar.xz'; [ -f $FILE ] && tar -xJf $FILE -C $CONTPATH && rm -f $FILE;" %  VVHZbd
  cmd += "  FILE='%s/debian-binary';  [ -f $FILE ]                                && rm -f $FILE;" %  VVHZbd
  cmd += "  echo -e 'Done.\n';"
  cmd += "  echo -e 'Output Directory:\n%s' %s;" % (VVHZbd, FF95sl(VVHZbd, VV9cEK))
  cmd += "fi;"
  FFfbee(self, cmd, VVIwP9=self.VVI84O)
 def VVcP4V(self, path):
  listCmd  = FFaG6T(VVPeIJ, "")
  infoCmd  = FFQ7Q5(VVCBKn , "")
  filesCmd = FFQ7Q5(VVpvpX, "")
  if listCmd and infoCmd and filesCmd:
   txt  = "Installed-Time: "
   sep  = FFoEsu(VVdWFT)
   notInst = "Package not installed."
   cmd  = FFt615("File Info", VVdWFT)
   cmd += "FILE='%s';" % path
   cmd += "echo -e 'File = '$FILE'\n';"
   cmd += "PACK=$(%s \"$FILE\" | grep Package | sed 's/Package: //g');" % infoCmd
   cmd += "if [[ -z \"$PACK\" ]]; then "
   cmd += " echo -e 'Cannot read Package Name from file.\n';"
   cmd += "else"
   cmd += " %s \"$FILE\" | sed 's/:/\t:/g';" % infoCmd
   cmd +=   FFt615("System Info", VVdWFT)
   cmd += " FOUND=$(%s | grep $PACK);" % listCmd
   cmd += " if [[ -z \"$FOUND\" ]]; then "
   cmd += "  echo -e '%s\n' %s;" % (notInst, FF95sl(notInst, VVU8eD))
   cmd += " else"
   cmd += "  %s $PACK | sed 's/:/\t:/g';" % infoCmd
   cmd += "  TIME=$(%s $PACK | grep %s | sed 's/%s//g');" % (infoCmd, txt, txt)
   cmd += "  HTIME=$(date -d @$TIME);"
   cmd += "  echo %s$HTIME | sed 's/: /\t: /g';" % txt
   cmd += "  echo '';"
   cmd +=    FFt615("Related Files", VVdWFT)
   cmd += "  %s $PACK | awk 'NR<2{print($0);next}{print($0)| \"sort\"}' | sed 's/files:/files:\\n/g';" % filesCmd
   cmd += " fi;"
   cmd += "fi;"
   cmd += "echo '';"
   cmd += sep
   FFCa80(self, cmd)
  else:
   FFHRK6(self)
 def VVoFvy(self, path, selFile, cmdOpt):
  cmd = FFQ7Q5(cmdOpt, path)
  if cmd:
   cmd = "%s && echo -e '\nSUCCESSFUL' || echo -e '\nERROR FOUND !'" % cmd
   FFMIbO(self, BF(FFfbee, self, cmd, VVIwP9=FFkmMQ), "Install Package ?\n\n%s" % selFile)
  else:
   FFHRK6(self)
 def VVGUJh(self, path, selFile, cmdOpt):
  listCmd  = FFaG6T(VVPeIJ, "")
  infoCmd  = FFQ7Q5(VVCBKn, "")
  instRemCmd = FFQ7Q5(cmdOpt    , "")
  if listCmd and infoCmd and instRemCmd:
   result  = " && echo -e '\nSUCCESSFUL' || echo -e '\nERROR FOUND !'"
   cannotTxt = "Cannot remove with Packaging Tools!"
   tryTxt  = "Try to delete the directory:"
   errTxt  = "Package not found by Packaging Tools!"
   cmd  = "FILE='%s';" % path
   cmd += "echo -e 'Reading package name ...';"
   cmd += "PACK=$(%s \"$FILE\" | grep Package | sed 's/Package: //g');" % infoCmd
   cmd += "if [[ -z \"$PACK\" ]]; then "
   cmd += " echo -e 'Cannot read Package Name from file.\n';"
   cmd += "else"
   cmd += " echo 'Package = '$PACK;"
   cmd += " FOUND=$(%s | grep $PACK);" % listCmd
   cmd += " if [[ -z \"$FOUND\" ]]; then "
   cmd += "  pNAME=$(echo $PACK | awk -F- '{print($NF)}');"
   cmd += "  tLOC=$(find %s -iname $pNAME);" % resolveFilename(SCOPE_PLUGINS)
   cmd += "  if [[ -z \"$tLOC\" ]]; then "
   cmd += "   echo -e '\n%s' %s;" % (errTxt, FF95sl(errTxt, VVU8eD))
   cmd += "  else"
   cmd += "   echo -e '\n%s' %s;" % (cannotTxt, FF95sl(cannotTxt, VVU8eD))
   cmd += "   echo -e '\n%s' %s;" % (tryTxt, FF95sl(tryTxt, VVU8eD))
   cmd += "   echo $tLOC;"
   cmd += "  fi;"
   cmd += " else"
   cmd += "  %s $PACK %s;" % (instRemCmd, result)
   cmd += " fi;"
   cmd += "fi"
   cmdIsOK = True
   FFMIbO(self, BF(FFfbee, self, cmd, VVIwP9=FFkmMQ), "Remove package related to this file ?\n\n%s" % selFile)
  else:
   FFHRK6(self)
 def VV0Q7R(self, path):
  hostName = FFj4HH("hostname").lower()
  kernelFile = path + hostName + "/kernel.bin"
  rootfsFile = path + hostName + "/rootfs.tar.bz2"
  versionFile = path + hostName + "/imageversion"
  return hostName, kernelFile, rootfsFile, versionFile
 def VVJjkq(self, path):
  hostName, kernelFile, rootfsFile, versionFile = self.VV0Q7R(path)
  if fileExists(kernelFile) and fileExists(rootfsFile):
   return True
  else:
   return False
 def VVPTnC(self, path, isDir):
  Dir  = "Archive to "
  Path = "Archive (Preserve Path Structure) to "
  VV625J = []
  VV625J.append(("%s.tar"  % Dir   , "archDir_tar"   ))
  VV625J.append(("%s.tar.gz" % Dir   , "archDir_tar_gz"  ))
  VV625J.append(("%s.tar.xz" % Dir   , "archDir_tar_xz"  ))
  VV625J.append(("%s.tar.bz2" % Dir   , "archDir_tar_bz2"  ))
  VV625J.append(("%s.zip"  % Dir   , "archDir_zip"   ))
  VV625J.append(VVm77t)
  VV625J.append(("%s.tar"  % Path   , "archPath_tar"  ))
  VV625J.append(("%s.tar.gz" % Path   , "archPath_tar_gz"  ))
  VV625J.append(("%s.tar.xz" % Path   , "archPath_tar_xz"  ))
  VV625J.append(("%s.tar.bz2" % Path   , "archPath_tar_bz2" ))
  VV625J.append(("%s.zip"  % Path   , "archPath_zip"  ))
  if isDir:
   VV625J.append(VVm77t)
   VV625J.append(('Convert to ".ipk" Package' , "convertDirToIpk" ))
   VV625J.append(('Convert to ".deb" Package' , "convertDirToDeb" ))
  if isDir: c1, c2, title = "#11003322", "#11002222", "Archive Directory"
  else : c1, c2, title = "#11003344", "#11002244", "Archive File"
  FFuRfS(self, BF(self.VV2TbK, path, isDir, title), VV625J=VV625J, title=title, VVz2kc=c1, VVwpZm=c2)
 def VV2TbK(self, path, isDir, title, item):
  if item is not None:
   if   item == "archDir_tar"    : self.VVxMF9(title, path, isDir, ".tar" , False)
   elif item == "archDir_tar_gz"   : self.VVxMF9(title, path, isDir, ".tar.gz" , False)
   elif item == "archDir_tar_xz"   : self.VVxMF9(title, path, isDir, ".tar.xz" , False)
   elif item == "archDir_tar_bz2"   : self.VVxMF9(title, path, isDir, ".tar.bz2", False)
   elif item == "archDir_zip"    : self.VVxMF9(title, path, isDir, ".zip" , False)
   elif item == "archPath_tar"    : self.VVxMF9(title, path, isDir, ".tar" , True)
   elif item == "archPath_tar_gz"   : self.VVxMF9(title, path, isDir, ".tar.gz" , True)
   elif item == "archPath_tar_xz"   : self.VVxMF9(title, path, isDir, ".tar.xz" , True)
   elif item == "archPath_tar_bz2"   : self.VVxMF9(title, path, isDir, ".tar.bz2", True)
   elif item == "archPath_zip"    : self.VVxMF9(title, path, isDir, ".zip" , True)
   elif item == "convertDirToIpk"   : self.VVCmeG(path, False)
   elif item == "convertDirToDeb"   : self.VVCmeG(path, True)
   else         : self.close()
 def VVCmeG(self, path, VVyJBC):
  self.session.openWithCallback(self.VVI84O, BF(CCw9MO, path=path, VVyJBC=VVyJBC))
 def VVxMF9(self, title, path, isDir, fileExt, preserveDirStruct):
  parent  = FFMjyS(path, True)
  lastPart = FFqDmh(path)
  archFile = lastPart + fileExt
  resultFile = parent + archFile
  if preserveDirStruct:
   archFile = resultFile
   targetDir = parent + lastPart
  else:
   targetDir = lastPart
  if isDir: outFile, srcTxt = archFile , "Source Directory"
  else : outFile, srcTxt = resultFile , "Source File"
  if   fileExt == ".tar"  : archCmd, toolCmd = "tar -cvf"  , "allOK='1';"
  elif fileExt == ".tar.gz" : archCmd, toolCmd = "tar -cvzf" , "allOK='1';"
  elif fileExt == ".tar.xz" : archCmd, toolCmd = "tar -cvJf" , FFqoRI("xz" , "xz"  , "XZ"  )
  elif fileExt == ".tar.bz2" : archCmd, toolCmd = "tar -cvjf" , FFqoRI("bzip2" , "bzip2" , "BZip2" )
  elif fileExt == ".zip"  : archCmd, toolCmd = "zip -r"  , FFqoRI("zip" , "zip"  , "Zip"  )
  if preserveDirStruct:
   if archCmd.startswith("tar") and targetDir.startswith("/") : archCmd = "%s '%s' -C / '%s';" % (archCmd, outFile, targetDir[1:])
   else              : archCmd = "%s '%s' '%s';"    % (archCmd, outFile, targetDir)
  else:
   if isDir: archCmd = "cd '%s'; %s '../%s' *;" % (path, archCmd, outFile)
   else : archCmd = "cd '%s'; %s '%s' '%s';" % (parent, archCmd, outFile, os.path.basename(path))
  failed = "Process failed !"
  sep  = " echo -e '%s';" % VVZ1aI
  cmd  = toolCmd
  cmd += "echo -e 'Archiving ...\n';"
  cmd += 'if [ "$allOK" -eq "1" ]; then '
  cmd +=   sep
  cmd +=   FFxtg8("rm -f '%s'" % archFile) + ";"
  cmd +=   archCmd
  cmd += " cd '%s';"      % parent
  cmd +=   sep
  cmd += " if [ $? -ne 0 ]; then "
  cmd += "  echo -e '\n%s\n' %s;"   % (failed, FF95sl(failed, VVMmz2))
  cmd += "  rm -f '%s' > /dev/null 2>&1;" % archFile
  cmd += " elif [ -f '%s' ]; then "  % archFile
  cmd += "  chmod 644 '%s';"    % archFile
  cmd += "  echo -e '\nDONE\n';"
  cmd += "  echo -e '%s:' %s;"   % (srcTxt, FF95sl(srcTxt, VVpHwQ))
  cmd += "  echo -e '%s:\n';"    % path
  cmd += "  echo -e '%s:' %s;"   % ("Output", FF95sl("Output", VV9cEK))
  cmd += "  echo -e '%s\n';"    % outFile
  cmd += " else"
  cmd += "  echo -e '\n%s\n' %s;"   % (failed, FF95sl(failed, VVzZva))
  cmd += "  rm -f '%s' > /dev/null 2>&1;" % archFile
  cmd += " fi;"
  cmd +=   sep
  cmd += "fi;"
  FFusMt(self, cmd, VVIwP9=self.VVI84O, title=title)
 def VVZO24(self, path, isAll):
  if isAll: title, pathLst = "Add all Media in Directory to a Bouquet", CC7ujK.VVOHAH(FFMjyS(path, True))
  else : title, pathLst = "Add Media File to a Bouquet"   , [path]
  picker = CCgKdM(self, self, title, BF(self.VV1Y6i, pathLst))
 def VV1Y6i(self, pathLst):
  return CCgKdM.VVpsne(pathLst)
 def VV2v8i(self, path):
  versionFile = path + "sf8008/imageversion"
  if fileExists(versionFile):
   FFsdMh(self, versionFile)
 def VVKO5R(self, path):
  hostName, kernelFile, rootfsFile, versionFile = self.VV0Q7R(path)
  if not fileExists(kernelFile) or not fileExists(rootfsFile):
   FFkYsE(self, "Essential files not found !")
   return
  fileUnixTime = os.path.getmtime(rootfsFile)
  backupDate  = datetime.fromtimestamp(fileUnixTime).strftime('%Y%m%d')
  outpuFileName = "octagon-backup-%s-%s" % (hostName, backupDate)
  version = ""
  if fileExists(versionFile):
   c = 0
   for line in FFjdnJ(versionFile):
    if "Version = " in line:
     version = (line.split("=", 1)[1]).strip().replace(" ", "-")
     outpuFileName = "%s-%s-%s" % (version, hostName, backupDate)
     version + "-" + hostName + backupDate
     break
    elif line.count("-") == 3:
     outpuFileName = line
     break
    c += 1
    if c > 7:
     break
  parent  = FFMjyS(path, False)
  VVHZbd = ("%s/%s_mmc.zip" % (parent, outpuFileName))
  errCmd  = "Zipping tools not found (zip , p7zip)!"
  errCmd  = " echo -e '\n%s' %s;" % (errCmd, FF95sl(errCmd, VVzZva))
  installCmd = FFQ7Q5(VV4pye , "")
  cmd  = 'FOUND=$(which zip);'
  cmd += 'if [[ -z "$FOUND" ]]; then '
  cmd += '  FOUND=$(which 7za);'
  cmd += 'fi;'
  if installCmd:
   cmd += 'if [[ -z "$FOUND" ]]; then '
   cmd += '  echo -e "Zip not found ...";'
   cmd += '  echo -e "Installing zip ...";'
   cmd += '  %s install zip >/dev/null;' % installCmd
   cmd += '  FOUND=$(which zip);'
   cmd += 'fi;'
   cmd += 'if [[ -z "$FOUND" ]]; then '
   cmd += '  echo -e "Could not install zip!";'
   cmd += '  echo -e "Installing p7zip ...";'
   cmd += '  %s install p7zip >/dev/null;' % installCmd
   cmd += '  FOUND=$(which 7za);'
   cmd += 'fi;'
   cmd += 'if [[ -z "$FOUND" ]]; then '
   cmd += '  echo -e "Could not install p7zip!";'
   cmd +=    errCmd
   cmd += 'else'
   cmd += ' echo -e "\nPlease wait ...";'
   cmd += '  if [ -f "%s" ]; then rm "%s"; fi;' % (VVHZbd, VVHZbd)
   cmd += '  cd "%s";'        % parent
   cmd += '  if [[ $(which zip) ]]; then '
   cmd += '    zip -r "%s" ./octagon/*;'   % VVHZbd
   cmd += '  elif [[  $(which 7za) ]]; then '
   cmd += '    7za a "%s" octagon/;'    % VVHZbd
   cmd += '  else'
   cmd += '    echo -e "\nZipping tool not found!";'
   cmd += '  fi;'
   cmd += '  if [ -f "%s" ]; then echo -e "\nOutput File:\n%s"; fi;' % (VVHZbd, VVHZbd)
   cmd += 'fi'
  else:
   cmd += 'if [[ -z "$FOUND" ]]; then '
   cmd +=    errCmd
   cmd += 'fi;'
  FFfbee(self, cmd, VVIwP9=self.VVI84O)
 def VVF68F(self, zipPath):
  title = "Convert .zip to .tar.gz"
  if iZip.is_zipfile(zipPath):
   tarPath = os.path.splitext(zipPath)[0] + ".tar.gz"
   fnc  = BF(self.VVmt8M, zipPath, tarPath, title)
   txt  = "Converting ..."
   if fileExists(tarPath) : FFMIbO(self, BF(FFlX3B, self, fnc, title=txt), "File already exists:\n\n%s\n\nOverwrite ?" % os.path.basename(tarPath), title=title)
   else     : FFlX3B(self, fnc, title=txt)
  else:
   FFkYsE(self, "Invalid zip file:\n\n%s" % os.path.basename(zipPath), title=title)
 def VVmt8M(self, zipPath, tarPath, title):
  try:
   with iZip.ZipFile(zipPath) as zipF:
    with iTar.open(tarPath, 'w:gz') as tarF:
     for zipInfo in zipF.infolist():
      tarInfo = iTar.TarInfo(name=zipInfo.filename)
      tarInfo.size = zipInfo.file_size
      tarInfo.mtime = mktime(tuple(list(zipInfo.date_time) + [-1, -1, -1]))
      tarF.addfile(tarinfo=tarInfo, fileobj=zipF.open(zipInfo.filename))
   ok = True
  except:
   ok = False
  if ok and fileExists(tarPath):
   FFNEkd(self, "Done\n\nSource File\t: %s\nOutput File\t: %s" % (os.path.basename(zipPath), os.path.basename(tarPath)), title=title)
   self.VVI84O()
  else:
   FFX92w(tarPath)
   FFkYsE(self, "Error while converting.", title=title)
 def VVsOjY(self, tarPath):
  title = "Convert .tar.gz to .zip"
  if iTar.is_tarfile(tarPath):
   zipPath = tarPath[:-7] + ".zip"
   fnc  = BF(self.VVKjxw, tarPath, zipPath, title)
   txt  = "Converting ..."
   if fileExists(tarPath) : FFMIbO(self, BF(FFlX3B, self, fnc, title=txt), "File already exists:\n\n%s\n\nOverwrite ?" % os.path.basename(tarPath), title=title)
   else     : FFlX3B(self, fnc, title=txt)
  else:
   FFkYsE(self, "Invalid tar file:\n\n%s" % os.path.basename(tarPath), title=title)
 def VVKjxw(self, tarPath, zipPath, title):
  try:
   with iTar.open(tarPath) as tar:
    with iZip.ZipFile(zipPath, mode='w', compression=iZip.ZIP_DEFLATED) as zipF:
     for mem in tar.getmembers():
      if mem.isfile():
       mtime = datetime.fromtimestamp(mem.mtime)
       zipInfo = iZip.ZipInfo(filename=mem.name, date_time=(mtime.year, mtime.month, mtime.day, mtime.hour, mtime.minute, mtime.second))
       zipF.writestr(zipInfo, tar.extractfile(mem).read(), compress_type=iZip.ZIP_DEFLATED)
   ok = True
  except:
   ok = False
  if ok and fileExists(tarPath):
   FFNEkd(self, "Done\n\nSource File\t: %s\nOutput File\t: %s" % (os.path.basename(tarPath), os.path.basename(zipPath)), title=title)
   self.VVI84O()
  else:
   FFX92w(zipPath)
   FFkYsE(self, "Error while converting.", title=title)
 @staticmethod
 def VVHl4q(SELF, path):
  try:
   if   path.endswith(".ts") : prefix = "1"
   elif path.endswith(".m2ts") : prefix = "3"
   else      : prefix = CFG.iptvAddToBouquetRefType.getValue()
   refCode = "%s:%s%s" % (prefix, "0:" * 9, path)
   SELF.session.nav.playService(eServiceReference(refCode))
   CCppdx.VVgElN(SELF.session, enableZapping= False, enableDownloadMenu=False, enableOpenInFMan=False)
  except:
   pass
 @staticmethod
 def VVa1tR(SELF):
  serv = SELF.session.nav.getCurrentlyPlayingServiceReference()
  fPath = serv and serv.getPath()
  if fPath and fileExists(fPath):
   fDir, fName = os.path.split(fPath)
   return fPath, FF0WrY(fDir), fName
  return "", "", ""
 @staticmethod
 def VVgxIS(path):
  Stat = os.statvfs(path)
  return Stat.f_frsize * Stat.f_blocks
 @staticmethod
 def VVMZOV(path):
  Stat = os.statvfs(path)
  return Stat.f_frsize * Stat.f_bfree
 @staticmethod
 def VVw1Gr(size, mode=0):
  txt = CC7ujK.VVPPWP(size)
  if size >= 1024 :
   commaSize = format(size, ',d')
   if mode == 1: return "%s (%s)"   % (txt, commaSize)
   if mode == 2: return "%s (%s)"   % (commaSize, txt)
   if mode == 3: return "%s (%s)"   % (size, txt)
   if mode == 4: return "%s"    % txt
   else  : return "%s  ( %s bytes )" % (txt, commaSize)
  else:
   return txt
 @staticmethod
 def VVPPWP(bytes):
  kilo, unit = 1024.0, ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
  if bytes < kilo:
   return "%d B" % bytes
  i = int(iFloor(iLog(bytes, 1024)))
  s = str("%.2f" % (bytes / (kilo ** i))).rstrip(".0")
  return "%s %s" % (s, unit[i])
 @staticmethod
 def VVFLgc(path):
  rangeList = list(range(0x20, 0x100))
  with open(path, 'rb') as f:
   bytes = f.read(1024)
  textchars = bytearray({7,8,9,10,12,13,27} | set(rangeList) - {0x7f})
  return bool(bytes.translate(None, textchars))
 @staticmethod
 def VV4HLe(SELF, path, title=""):
  try:
   with ioOpen(path, "r", encoding="UTF-8") as f:
    txt = f.read()
   return True
  except:
   if title:
    FFkYsE(SELF, "File is not in 'UTF-8' Encoding:\n\n%s" % path, title=title)
   return False
 @staticmethod
 def VVMdDF():
  tDict = CCrQyy.VVrVCE()
  lst = list(tDict["mov"])
  lst.extend(list(tDict["mus"]))
  return tuple(lst)
 @staticmethod
 def VVOHAH(path):
  lst = []
  for ext in CC7ujK.VVMdDF():
   lst.extend(iGlob("%s/*.%s" % (path, ext)))
  return sorted(lst, key=FFGDcX(FFUcDJ))
 @staticmethod
 def VV6oXj(path):
  res = os.system("tar -tzf '%s' >/dev/null" % path)
  return res == 0
class CCrQyy(MenuList):
 VVXAWX  = 0
 VVY5nR  = 1
 VV7O5K  = 2
 VV1cFw  = 3
 VVNL86  = 4
 VVJriY  = 5
 VVHdpe  = 6
 VV3adM  = 7
 VVKxUk  = "<List of Storage Devices>"
 VVrNuR = "<Parent Directory>"
 def __init__(self, VV3ePF=False, directory="/", VVpLps=True, VVDQj4=True, VV8O4O=True, VVVPfW=None, VVItQG=False, VVgskY=False, VVdIO6=False, isTop=False, VViU81=None, VVsSYD=1000, VVmp7B=30, VVyhPB=30, VVQzgv="#00000000", pngBGColorSelStr="#06003333"):
  MenuList.__init__(self, list, VV3ePF, eListboxPythonMultiContent)
  self.VVpLps  = VVpLps
  self.VVDQj4    = VVDQj4
  self.VV8O4O  = VV8O4O
  self.VVVPfW  = VVVPfW
  self.VVItQG   = VVItQG
  self.VVgskY   = VVgskY or []
  self.VVdIO6   = VVdIO6 or []
  self.isTop     = isTop
  self.additional_extensions = VViU81
  self.VVsSYD    = VVsSYD
  self.VVmp7B    = VVmp7B
  self.VVyhPB    = VVyhPB
  self.pngBGColor    = FFZG1G(VVQzgv)
  self.pngBGColorSel   = FFZG1G(pngBGColorSelStr)
  self.EXTENSIONS    = CCrQyy.VVrVCE()
  self.VVYHZX   = eServiceCenter.getInstance()
  self.mountpoints   = []
  self.current_directory  = None
  self.current_mountpoint  = None
  self.l.setFont(0, gFont(VVFwML, self.VVmp7B))
  self.l.setItemHeight(self.VVyhPB)
  self.png_mem   = self.VV54he("mem")
  self.png_usb   = self.VV54he("usb")
  self.png_fil   = self.VV54he("fil")
  self.png_dir   = self.VV54he("dir")
  self.png_dirup   = self.VV54he("dirup")
  self.png_srv   = self.VV54he("srv")
  self.png_slwfil   = self.VV54he("slwfil")
  self.png_slbfil   = self.VV54he("slbfil")
  self.png_slwdir   = self.VV54he("slwdir")
  self.VVz9vR()
  self.VVimWq(directory)
 def VV54he(self, category):
  return LoadPixmap("%s%s.png" % (VVASCC, category), getDesktop(0))
 @staticmethod
 def VVrVCE():
  return {"pic":("bmp","gif","jpe","jpeg","jpg","mvi","png"),"mov":("3g2","3gp","asf","avi","divx","flv","ifo","iso","m2ts","m4v","mkv","mod","mov","mp4","mpe","mpeg","mpg","mts","ogm","ogv","pva","rm","rmvb","ts","vob","webm","wmv","wtv","h264","h265","mjpeg","mk3d","mks","xvid"),"mus":("aac","ac3","alac","amr","ape","au","dts","flac","m2a","m4a","mid","mka","mp2","mp3","oga","ogg","wav","wave","wma","wv","m3u","m4b","m4p","mpc","wpl"),"txt":("cfg","conf","htm","html","py","txt","xml"),"tar":("bz2","gz","tar","xz"),"rar":("rar"),"zip":("zip"),"ipk":("ipk"),"deb":("deb"),"scr":("sh"),"m3u":("m3u","m3u8")}
 def VVOfnT(self, name, absolute=None, isDir=False, png=None):
  if absolute and isDir:
   path = absolute
   path = FFkEOw(path)
   if os.path.islink(path):
    png = self.png_slwdir
    name += FFkhYI(" -> " , VVdWFT) + FFkhYI(os.readlink(path), VV9cEK)
  tableRow = [ (absolute, isDir) ]
  tableRow.append((eListboxPythonMultiContent.TYPE_TEXT, self.VVyhPB + 10, 0, self.VVsSYD, self.VVyhPB, 0, LEFT | RT_VALIGN_CENTER, name))
  if png is not None:
   if VVlTBS: tableRow.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 0, 2, self.VVyhPB-4, self.VVyhPB-4, png, self.pngBGColor, self.pngBGColorSel, VVlTBS))
   else   : tableRow.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 0, 2, self.VVyhPB-4, self.VVyhPB-4, png, self.pngBGColor, self.pngBGColorSel))
  return tableRow
 def VVK76x(self, name):
  ext = os.path.splitext(name)[1]
  if ext:
   ext = ext.lstrip(".").lower()
   for cat, lst in list(self.EXTENSIONS.items()):
    if ext in lst:
     return cat
  return ""
 def VVz9vR(self):
  self.mountpoints = [os.path.join(p.mountpoint, "") for p in harddiskmanager.getMountedPartitions()]
  self.mountpoints.sort(reverse=True)
 def VVQAp7(self, file):
  file = os.path.join(os.path.realpath(file), "")
  for m in self.mountpoints:
   if file.startswith(m):
    return m
  return False
 def VVxMeL(self, file):
  if os.path.realpath(file) == file:
   return self.VVQAp7(file)
  else:
   if file[-1] == "/":
    file = file[:-1]
   mp = self.VVQAp7(file)
   last = file
   file = os.path.dirname(file)
   while last != "/" and mp == self.VVQAp7(file):
    last = file
    file = os.path.dirname(file)
   return os.path.join(last, "")
 def getSelection(self):
  if self.l.getCurrentSelection() is None:
   return None
  return self.l.getCurrentSelection()[0]
 def VVSg8w(self):
  l = self.l.getCurrentSelection()
  if not l or l[0][1] == True:
   return None
  else:
   return self.VVYHZX.info(l[0][0]).getEvent(l[0][0])
 def VVhnvV(self):
  return self.list
 def VVnSnO(self, dir, parents):
  dir = os.path.realpath(dir)
  for p in parents:
   if dir.startswith(p):
    return True
  return False
 def VVimWq(self, directory, select = None):
  self.list = []
  directories = []
  files = []
  if self.current_directory is None:
   if directory and self.VV8O4O:
    self.current_mountpoint = self.VVxMeL(directory)
   else:
    self.current_mountpoint = None
  self.current_directory = directory
  if directory is None:
   if self.VV8O4O:
    for p in harddiskmanager.getMountedPartitions():
     path = os.path.join(p.mountpoint, "")
     if path not in self.VVdIO6 and not self.VVnSnO(path, self.VVgskY):
      if path == "/" : png = self.png_mem
      else   : png = self.png_usb
      self.list.append(self.VVOfnT(name=p.description, absolute=path, isDir=True, png=png))
    path = "/"
    if path not in self.VVdIO6 and not self.VVnSnO(path, self.VVgskY):
     for item in self.list:
      if path == item[0][0]:
       break
     else:
      self.list.append(self.VVOfnT(name="INTERNAL FLASH", absolute="/", isDir=True, png=self.png_mem))
  elif self.VVItQG:
   root = eServiceReference(2, 0, directory)
   if self.additional_extensions:
    root.setName(self.additional_extensions)
   VVYHZX = eServiceCenter.getInstance()
   list = VVYHZX.list(root)
   while 1:
    s = list.getNext()
    if not s.valid():
     del list
     break
    if s.flags & s.mustDescent:
     directories.append(s.getPath())
    else:
     files.append(s)
  else:
   if fileExists(directory):
    try:
     files = os.listdir(directory)
    except:
     files = []
    tmpfiles = files[:]
    for x in tmpfiles:
     if os.path.isdir(directory + x):
      directories.append(directory + x + "/")
      files.remove(x)
  if directory is not None and self.VVpLps and not self.isTop:
   if directory == self.current_mountpoint and self.VV8O4O:
    self.list.append(self.VVOfnT(name=self.VVKxUk, absolute=None, isDir=True, png=self.png_dirup))
   elif (directory != "/") and not (self.VVdIO6 and self.VVQAp7(directory) in self.VVdIO6):
    self.list.append(self.VVOfnT(name=self.VVrNuR, absolute='/'.join(directory.split('/')[:-2]) + '/', isDir=True, png=self.png_dirup))
  if self.VVpLps:
   for x in directories:
    if not (self.VVdIO6 and self.VVQAp7(x) in self.VVdIO6) and not self.VVnSnO(x, self.VVgskY):
     name = x.split('/')[-2]
     if x in self.mountpoints: png = self.png_usb
     else     : png = self.png_dir
     self.list.append(self.VVOfnT(name=name, absolute=x, isDir=True, png=png))
  if self.VVDQj4:
   for x in files:
    if self.VVItQG:
     path = x.getPath()
     name = path.split('/')[-1]
     png  = self.png_srv
    else:
     path = directory + x
     name = x
     png  = self.png_fil
     if os.path.islink(path):
      try:
       target = os.readlink(path)
       if fileExists(self.current_directory + target):
        png = self.png_slwfil
        name += FFkhYI(" -> " , VVdWFT) + FFkhYI(target, VV9cEK)
       else:
        png = self.png_slbfil
        name += FFkhYI(" -> " , VVdWFT) + FFkhYI(target, VVzZva)
      except:
       png = self.png_slbfil
     elif "." in name:
      category = self.VVK76x(name)
      if category:
       png = LoadPixmap("%s%s.png" % (VVASCC, category))
    if (self.VVVPfW is None) or iCompile(self.VVVPfW).search(path):
     self.list.append(self.VVOfnT(name=name, absolute=x , isDir=False, png=png))
  if self.VV8O4O and len(self.list) == 0:
   self.list.append(self.VVOfnT(name=FFkhYI("No USB connected", VVkXS4), absolute=None, isDir=False, png=self.png_usb))
  self.l.setList(self.list)
  self.VV94Wp()
  if select is not None:
   i = 0
   self.moveToIndex(0)
   for x in self.list:
    p = x[0][0]
    if isinstance(p, eServiceReference):
     p = p.getPath()
    if p == select:
     self.moveToIndex(i)
    i += 1
 def VVpNPJ(self):
  return self.current_directory
 def VV5bSS(self):
  if self.getSelection() is None:
   return False
  return self.getSelection()[1]
 def VVO6Ur(self):
  return self.VVWpwW() and self.VVpNPJ()
 def VVWpwW(self):
  return self.list[0][1][7] in (self.VVKxUk, self.VVrNuR)
 def descent(self):
  if self.getSelection() is None:
   return
  self.VVimWq(self.getSelection()[0], select = self.current_directory)
 def VV6e4N(self):
  if self.getSelection() is None:
   return None
  x = self.getSelection()[0]
  if isinstance(x, eServiceReference):
   x = x.getPath()
  return x
 def VVJQmn(self):
  if self.getSelection() is None:
   return None
  x = self.getSelection()[0]
  if isinstance(x, eServiceReference):
   return x
  return None
 def execBegin(self):
  harddiskmanager.on_partition_list_change.append(self.VV4uwO)
 def execEnd(self):
  harddiskmanager.on_partition_list_change.remove(self.VV4uwO)
 def refresh(self):
  self.VVimWq(self.current_directory, self.VV6e4N())
 def VV4uwO(self, action, device):
  self.VVz9vR()
  if self.current_directory is None:
   self.refresh()
 def VVOIhF(self):
  mode = CFG.browserSortMode.getValue()
  mix  = CFG.browserSortMix.getValue()
  sAZ, sZA, s09, s90, sNO, sON = "A > Z", "Z > A", "0 > 9", "9 > 0", "New > Old", "Old > New"
  if mode == self.VVXAWX : nameAlpMode, nameAlpTxt = self.VVY5nR, sZA
  else       : nameAlpMode, nameAlpTxt = self.VVXAWX, sAZ
  if mode == self.VV7O5K : nameNumMode, nameNumTxt = self.VV1cFw, s90
  else       : nameNumMode, nameNumTxt = self.VV7O5K, s09
  if mode == self.VVNL86 : dateMode, dateTxt = self.VVJriY, sON
  else       : dateMode, dateTxt = self.VVNL86, sNO
  if mode == self.VVHdpe : typeMode, typeTxt = self.VV3adM, sZA
  else       : typeMode, typeTxt = self.VVHdpe, sAZ
  if   mode in (self.VVXAWX, self.VVY5nR): txt = "Name (%s)" % (sAZ if mode == self.VVXAWX else sZA)
  elif mode in (self.VV7O5K, self.VV1cFw): txt = "Name (%s)" % (s09 if mode == self.VVXAWX else s90)
  elif mode in (self.VVNL86, self.VVJriY): txt = "Date (%s)" % (sNO if mode == self.VVNL86 else sON)
  elif mode in (self.VVHdpe, self.VV3adM): txt = "Type (%s)" % (sAZ if mode == self.VVHdpe else sZA)
  if mix:
   txt += " .. Mixed"
  return nameAlpMode, nameAlpTxt, nameNumMode, nameNumTxt, dateMode, dateTxt, typeMode, typeTxt, "Cur = by %s" % txt
 def VV94Wp(self, mode=None, isMix=False, isNum=False):
  if not mode is None:
   FFnT3A(CFG.browserSortMode, mode)
   FFnT3A(CFG.browserSortMix, isMix)
  if self.list:
   if self.VVWpwW() : item0, topRow = 1, self.list[0]
   else    : item0, topRow = 0, None
   mode = CFG.browserSortMode.getValue()
   isMix = CFG.browserSortMix.getValue()
   if mode in (self.VVXAWX, self.VVY5nR):
    rev = True if mode == self.VVY5nR else False
    if isMix: self.list = sorted(self.list[item0:], key=lambda x: x[1][7]         , reverse=rev)
    else : self.list = sorted(self.list[item0:], key=lambda x: (x[0][1] if rev else not x[0][1], x[1][7]), reverse=rev)
   elif mode in (self.VV7O5K, self.VV1cFw):
    rev = True if mode == self.VV1cFw else False
    self.list = sorted(self.list[item0:], key=FFGDcX(BF(self.VV1Wwu, isMix, rev)), reverse=rev)
   elif mode in (self.VVNL86, self.VVJriY):
    rev = True if mode == self.VVJriY else False
    self.list = sorted(self.list[item0:], key=FFGDcX(BF(self.VVO1pn, isMix)), reverse=rev)
   else:
    rev = True if mode == self.VV3adM else False
    if isMix: self.list = sorted(self.list[item0:], key=lambda x: os.path.splitext(x[1][7])[1]            , reverse=rev)
    else : self.list = sorted(self.list[item0:], key=lambda x: (x[0][1] if rev else not x[0][1], os.path.splitext(x[1][7])[1], x[1][7]) , reverse=rev)
   if topRow:
    self.list.insert(0, topRow)
   self.l.setList(self.list)
 def VV1Wwu(self, mix, rev, p1, p2):
  dir1, name1 = p1[0][1], p1[1][7]
  dir2, name2 = p2[0][1], p2[1][7]
  if mix:
   return FFUcDJ(name1.lower(), name2.lower())
  else:
   if rev: dir1, dir2 = dir2, dir1
   return FFo5A5(dir2, dir1) or FFUcDJ(name1, name2)
 def VVO1pn(self, mix, p1, p2):
  dir1 = p1[0][1]
  dir2 = p2[0][1]
  if mix or dir1 == dir2:
   path1 = "" if dir1 else self.current_directory
   path2 = "" if dir2 else self.current_directory
   try:
    stat1 = os.stat(path1 + p1[0][0])
    stat2 = os.stat(path2 + p2[0][0])
    if mix : return FFo5A5(stat2.st_ctime, stat1.st_ctime)
    else : return FFo5A5(dir2, dir1) or FFo5A5(stat2.st_ctime, stat1.st_ctime)
   except:
    pass
  return 0
class CCrlqE(Screen):
 def __init__(self, session, defFG="", defBG=""):
  self.skin, self.skinParam = FF896P(VV1GIX, 900, 700, 35, 10, 14, "#22333333", "#22333333", 30, barHeight=40)
  self.session  = session
  self.Title   = "Color Picker"
  self.TOTAL_ROWS  = 6
  self.TOTAL_COLS  = 8
  self.VVvytR   = []
  self.curRow   = 0
  self.curCol   = 0
  self.isBgMode  = True
  self.defFG   = self.VVWNXS(defFG, "#00FFFFFF")
  self.defBG   = self.VVWNXS(defBG, "#11000000")
  self.transp   = int(self.defBG[1:3], 16)
  self.colors   = (   ("FFFFFF", "FFC0C0", "FFE0C0", "FFFFC0", "C0FFC0", "C0FFFF", "C0C0FF", "FFC0FF")
        , ("E0E0E0", "FF8080", "FFC080", "FFFF80", "80FF80", "80FFFF", "8080FF", "FF80FF")
        , ("C0C0C0", "FF0000", "FF8000", "FFFF00", "00FF00", "00FFFF", "0000FF", "FF00FF")
        , ("808080", "C00000", "C04000", "C0C000", "00C000", "00C0C0", "0000C0", "C000C0")
        , ("404040", "800000", "804000", "808000", "008000", "008080", "000080", "800080")
        , ("000000", "400000", "804040", "404000", "004000", "004040", "000040", "400040")
        )
  FFJd2Z(self, self.Title)
  self["keyRed"].show()
  FFHhgX(self["keyGreen"] , "< > Transp.")
  FFHhgX(self["keyYellow"], "Foreground")
  FFHhgX(self["keyBlue"] , "Background")
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    self["myColor%d%d" % (row, col)] = Label()
  self["myColorPtr"] = Label()
  self["myColorTst"] = Label("This is a test message.\n0123456789")
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : self.VV5FXR     ,
   "yellow"  : BF(self.VVzZjp, False)  ,
   "blue"   : BF(self.VVzZjp, True)  ,
   "up"   : self.VVmkvi       ,
   "down"   : self.VVcuOr      ,
   "left"   : self.VV8g7c      ,
   "right"   : self.VVkPgM      ,
   "last"   : BF(self.VVg8hE, -5) ,
   "next"   : BF(self.VVg8hE, 5) ,
   "cancel"  : BF(self.close, None, None)
  }, -1)
  self.onShown.append(self.VVqouI)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    FFobAA(self["myColor%d%d" % (row, col)], "#11%s" % self.colors[row][col])
  c = "#11333333"
  FFobAA(self["keyRed"] , c)
  FFobAA(self["keyGreen"] , c)
  self.VVAHdk()
  self.VVwmg7()
  FFlr8P(self["myColorTst"], self.defFG)
  FFobAA(self["myColorTst"], self.defBG)
 def VVWNXS(self, color, defColor):
  color = color.upper()
  span = iSearch(r"([#][a-fA-F0-9]{8})", color, IGNORECASE)
  if span : return color
  else : return defColor
 def VVwmg7(self):
  for row in range(self.TOTAL_ROWS):
   for col in range(self.TOTAL_COLS):
    color = self.colors[row][col]
    found = False
    if self.isBgMode:
     if self.defBG[3:] == self.colors[row][col]:
      found = True
    else:
     if self.defFG[3:] == self.colors[row][col]:
      found = True
    if found:
     self.curRow = row
     self.curCol = col
     self.VVoZNa(0, 0)
     return
 def VV5FXR(self):
  self.close(self.defFG, self.defBG)
 def VVmkvi(self): self.VVoZNa(-1, 0)
 def VVcuOr(self): self.VVoZNa(1, 0)
 def VV8g7c(self): self.VVoZNa(0, -1)
 def VVkPgM(self): self.VVoZNa(0, 1)
 def VVoZNa(self, row, col):
  self.curRow += row
  self.curCol += col
  if   self.curRow > self.TOTAL_ROWS -1 : self.curRow = 0
  elif self.curRow < 0     : self.curRow = self.TOTAL_ROWS - 1
  if   self.curCol > self.TOTAL_COLS -1 : self.curCol = 0
  elif self.curCol < 0     : self.curCol = self.TOTAL_COLS - 1
  color = self.VVD7n7()
  self["keyRed"].setText(color)
  if self.isBgMode: self.defBG = color
  else   : self.defFG = color
  gap = int(self.skinParam["marginLeft"] / 2)
  pos = self["myColor%d%d" % (self.curRow, self.curCol)].getPosition()
  self["myColorPtr"].instance.move(ePoint(pos[0] - gap - 2, pos[1] - gap - 2))
  self.VVDu2O()
 def VVAHdk(self):
  self["myTitle"].setText("  %s %s" % ("Background" if self.isBgMode else "Foreground", self.Title))
 def VVDu2O(self):
  color = self.VVD7n7()
  if self.isBgMode: FFobAA(self["myColorTst"], color)
  else   : FFlr8P(self["myColorTst"], color)
 def VVzZjp(self, isBg):
  self.isBgMode = isBg
  self.VVAHdk()
  self.VVwmg7()
 def VVg8hE(self, val):
  self.transp += val
  if   self.transp > 255 : self.transp = 255
  elif self.transp < 0 : self.transp = 0
  self. VVoZNa(0, 0)
 def VVs3Sh(self):
  return hex(self.transp)[2:].zfill(2)
 def VVD7n7(self):
  return ("#%s%s" % (self.VVs3Sh(), self.colors[self.curRow][self.curCol])).upper()
class CCSwZ2(Screen):
 def __init__(self, session):
  self.session = session
  screenSize  = FFjf8O()
  margin   = 50
  w    = int(screenSize[0] - margin)
  h    = int(screenSize[1] - margin)
  self.skin, self.skinParam = FF896P(VVmOpB, w, h, 28, 20, 30, "#33002233", "#33002233", 25, topRightBtns=2)
  self.timerUpdate  = eTimer()
  self.timerEndText  = eTimer()
  self.subtList   = []
  self.lastSubtInfo  = ""
  self.lastSubtFile  = ""
  self.lastSubtEnc  = ""
  self.currentIndex  = -1
  self.settingShown  = False
  self.CursorPos   = 0
  self.Title    = "Subtitle Settings"
  FFJd2Z(self, title="%s%s%s" % (self.Title, " " * 10, FFkhYI("Change values with Up , Down, < , 0 , >", VVkXS4)))
  self["mySubtCover"] = Label()
  self.ctrlBtns = ("keyRed", "keyGreen", "keyYellow", "keyBlue")
  subj = ("Reset All", "Save", "Reset Delay", "Pick Line")
  for i, name in enumerate(self.ctrlBtns):
   self[name] = Label(subj[i])
  self["mySubtCursor"] = Label()
  subj = ("Delay", "BG Trans %", "Text Color", "Text Font", "Text Size", "Alignment", "Shadow Color", "Shadow Size", "Posision")
  self.settingLabels = ["Del", "BGTr", "TxtFg", "TxtFnt", "TxtSiz", "Align", "ShadFg", "ShadSiz", "Pos"]
  self.settingLabels1 = list(self.settingLabels)
  for i, name in enumerate(self.settingLabels):
   self.settingLabels[i]  = "mySubt%s"   % name
   self.settingLabels1[i] = "mySubt%s1"  % name
   self[self.settingLabels[i]]  = Label(subj[i])
   self[self.settingLabels1[i]] = Label(subj[i])
  self["mySubtFr"] = Label()
  for i in range(3): self["mySubt%d"  % i] = Label()
  for i in range(4): self["mySubtSep%d" % i] = Label()
  self["myAction"] = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"  : BF(self.close, "subtExit")  ,
   "cancel" : self.VVl8rx      ,
   "info"  : self.VV7H6j    ,
   "red"  : self.VVhGdn  ,
   "green"  : self.VVtJR3   ,
   "yellow" : BF(self.VVKtu1, 0)  ,
   "blue"  : self.VVaU2w    ,
   "menu"  : self.VVgRRg      ,
   "left"  : self.VV8g7c      ,
   "right"  : self.VVkPgM      ,
   "last"  : self.VVwXoP     ,
   "next"  : self.VVcqzI     ,
   "0"   : self.VVEsuE    ,
   "up"  : self.VVmkvi       ,
   "down"  : self.VVcuOr      ,
   "pageUp" : BF(self.VVZ9mP, True) ,
   "pageDown" : BF(self.VVZ9mP, False) ,
   "chanUp" : BF(self.VVZ9mP, True) ,
   "chanDown" : BF(self.VVZ9mP, False)
  }, -1)
  self.onShown.append(self.VVqouI)
  self.onClose.append(self.VVCZyw)
 def VVqouI(self):
  self.onShown.remove(self.VVqouI)
  FFtIlI(self)
  FF4Pls(self)
  for i in range(3):
   self["mySubt%d" % i].instance.setNoWrap(True)
   self["mySubt%d" % i].hide()
  self.VVZ19s()
  self.VVMdcN()
  self.VVSYr1()
 def VVCZyw(self):
  self.timerUpdate.stop()
  self.timerEndText.stop()
 def VVNw7y(self):
  self.settingShown = True
  for name in self.ctrlBtns: self[name].show()
  for name in self.settingLabels : self[name].show()
  for name in self.settingLabels1: self[name].show()
  for i in range(4): self["mySubtSep%d" % i].show()
  self["myTitle"].show()
  self["mySubtFr"].show()
  FFobAA(self["myBody"], "#33002233")
  self["keyMenu"].show()
  self["keyInfo"].show()
  self["mySubtCover"].hide()
  self.VVmCMC()
 def VVZ19s(self):
  self.settingShown = False
  for name in self.ctrlBtns: self[name].hide()
  for name in self.settingLabels : self[name].hide()
  for name in self.settingLabels1: self[name].hide()
  for i in range(4): self["mySubtSep%d" % i].hide()
  self["myTitle"].hide()
  self["mySubtFr"].hide()
  FFobAA(self["myBody"], "#ff000000")
  self["keyMenu"].hide()
  self["keyInfo"].hide()
  self["mySubtCover"].show()
 def VVmz9T(self):
  if self.settingShown: self.VVZ19s()
  else    : self.VVNw7y()
 def VVl8rx(self):
  for confItem in self.VVT8uy():
   if confItem.isChanged():
    FFMIbO(self, self.VV36qa, "Save Changes ?", callBack_No=self.VV7YLk, title=self.Title)
    break
  else:
   if self.settingShown: self.VVZ19s()
   else    : self.close("subtExit")
 def VVgRRg(self):
  if self.settingShown: self.VVrrUC()
  else    : self.VVNw7y()
 def VV8g7c(self): self.VVDujE(-1)
 def VVkPgM(self): self.VVDujE(1)
 def VVDujE(self, pos):
  if self.settingShown:
   self.CursorPos += pos
   if   self.CursorPos > len(self.settingLabels) - 1: self.CursorPos = 0
   elif self.CursorPos < 0        : self.CursorPos = len(self.settingLabels) - 1
   inst = self[self.settingLabels[self.CursorPos]].instance
   left = inst.position().x() - 5
   inst = self["mySubtCursor"].instance
   inst.move(ePoint(left, int(inst.position().y())))
 def VVZ9mP(self, isUp):
  self.close("subtZapUp" if isUp else "subtZapUp")
 def VVwXoP(self) : self.VVJrza(5)
 def VVcqzI(self) : self.VVJrza(6)
 def VVEsuE(self) : self.VVJrza(-1)
 def VVmkvi(self):
  if self.settingShown: self.VVJrza(1)
  else    : self.VVZ9mP(True)
 def VVcuOr(self):
  if self.settingShown: self.VVJrza(0)
  else    : self.VVZ9mP(False)
 def VVJrza(self, direction):
  if self.settingShown:
   confItem = self.VVT8uy()[self.CursorPos]
   if direction == -1:
    confItem.setValue(confItem.default)
   else:
    if confItem is CFG.subtVerticalPos:
     if   direction == 0: direction = 1
     elif direction == 1: direction = 0
    confItem.handleKey(direction)
   if confItem is CFG.subtTextAlign:
    align = CFG.subtTextAlign.getValue()
    boxWidth= self.instance.size().width()
    for i in range(3):
     inst = self["mySubt%d" % i].instance
     w   = inst.calculateSize().width() + 50
     if   align == "0" : left = 0
     elif align == "2" : left = boxWidth - w
     else    : left = int((getDesktop(0).size().width() - w) / 2.0)
     inst.move(ePoint(left, int(inst.position().y())))
   self.VVmCMC()
   self.VVMdcN()
   self.VVUBJP(True)
 def VVT8uy(self):
  return (  CFG.subtDelaySec
    , CFG.subtBGTransp
    , CFG.subtTextFg
    , CFG.subtTextFont
    , CFG.subtTextSize
    , CFG.subtTextAlign
    , CFG.subtShadowColor
    , CFG.subtShadowSize
    , CFG.subtVerticalPos)
 def VV7YLk(self):
  for confItem in self.VVT8uy(): confItem.cancel()
  self.VVmCMC()
  self.VVMdcN()
 def VVhGdn(self):
  if self.settingShown:
   FFMIbO(self, self.VVwbHF, "Reset Subtitle Settings to default ?", title=self.Title)
 def VVwbHF(self):
  for confItem in self.VVT8uy(): confItem.setValue(confItem.default)
  self.VV36qa()
  self.VVmCMC()
  self.VVMdcN()
 def VVKtu1(self, delay, force=False):
  if self.settingShown or force:
   FFnT3A(CFG.subtDelaySec, delay)
   self.VVExmX()
   self.VVmCMC()
   self.VVMdcN()
   if self.settingShown:
    FFD1yO(self, 'Reset to "0"', 800, isGrn=True)
 def VVtJR3(self):
  if self.settingShown:
   self.VV36qa()
   self.VVZ19s()
 def VV36qa(self):
  for confItem in self.VVT8uy(): confItem.save()
  configfile.save()
  self.VVExmX()
  FFD1yO(self, "Saved", 1000, isGrn=True)
 def VVmCMC(self):
  cfgLst = self.VVT8uy()
  for i, name in enumerate(self.settingLabels1):
   self[name].setText(str(cfgLst[i].getText()))
 def VVMdcN(self):
  fnt = CFG.subtTextFont.getValue()
  if not fnt in FFBl25():
   fnt = VVFwML
  lineH = 0
  top = self["mySubt0"].instance.position().y()
  bg = int(FFZMXB(CFG.subtBGTransp.getValue(), 0, 100, 0, 255))
  try:
   for i in range(3):
    obj = self["mySubt%d" % i]
    inst = obj.instance
    bodyFontSize = CFG.subtTextSize.getValue()
    if CFG.subtTextFg.getValue().startswith("#"):
     FFlr8P(obj, CFG.subtTextFg.getValue())
    inst.setFont(gFont(fnt, bodyFontSize))
    FFobAA(obj, "#%0.2X000000" % bg)
    inst.setBorderColor(parseColor(CFG.subtShadowColor.getValue()))
    inst.setBorderWidth(int(CFG.subtShadowSize.getValue()))
    inst.setNoWrap(True)
    lineH = FFiz2E(bodyFontSize, 0.18)
    inst.resize(eSize(*(int(inst.size().width()), lineH)))
    if i > 0:
     inst.move(ePoint(int(inst.position().x()), int(top + lineH * i + i * 1 )))
   for i in range(1, 4):
    inst = self["mySubtSep%d" % i].instance
    inst.move(ePoint(int(inst.position().x()), int(top + lineH * i + i * 1 )))
  except:
   pass
  inst = self["mySubt2"].instance
  winH = inst.position().y() + inst.size().height() + 2
  winW = self.instance.size().width()
  self.instance.resize(eSize(*(int(winW), int(winH))))
  y = int(FFZMXB(CFG.subtVerticalPos.getValue(), 0, 100, 0, FFjf8O()[1] - winH))
  self.instance.move(ePoint(int(self.instance.position().x()), y))
  boxFSize = self["myInfoFrame"].instance.size()
  boxSize  = self["myInfoBody"].instance.size()
  self["myInfoFrame"].instance.move(ePoint(int((winW - boxFSize.width()) // 2), int((winH - boxFSize.height()) // 2)))
  self["myInfoBody"].instance.move(ePoint(int((winW - boxSize.width()) // 2) , int((winH - boxSize.height()) // 2)))
 def VV7H6j(self):
  sp = "    "
  txt  = "%s\n"   % FFkhYI("Subtitle File:", VVoTT6)
  txt += sp + "%s\n\n" % self.lastSubtFile
  txt += "%s\n"     % FFkhYI("Subtitle Settings:", VVoTT6)
  txt += sp + "Encoding\t: %s\n" % (self.lastSubtEnc or "Default")
  txt += sp + "Delay\t: %s sec\n" % CFG.subtDelaySec.getValue()
  if self.subtList:
   posVal, durVal = self.VVbwNa()
   capNum1, frmSec1, toSec1, subtLines1 = self.subtList[0]
   capNum2, frmSec2, toSec2, subtLines2 = self.subtList[len(self.subtList) - 1]
   time1 = FF3UDS(frmSec1)
   time2 = FF3UDS(toSec2)
   txt += "\n"
   txt += "%s\n"       % FFkhYI("Timing:", VVoTT6)
   txt += sp + "Captions\t: %s - %s\n"  % (capNum1, capNum2)
   txt += sp + "Subt. Time\t: %s - %s\n" % (time1, time2)
   txt += sp + "Event Dur.\t: %s\n"  % FF3UDS(durVal)
   txt += sp + "Progress\t: %s\n" % FF3UDS(posVal)
   if posVal > toSec2: txt += sp + "Remarks\t: %s\n" % FFkhYI("Subtitle end reached.", VVMmz2)
  FFNEkd(self, txt, title="Current Subtitle")
 def VVSYr1(self, path="", delay=0, enc=""):
  FFlX3B(self, BF(self.VVK2iW, path=path, delay=delay, enc=enc), "Checking Subtitle ...", clearMsg=False)
 def VVK2iW(self, path="", delay=0, enc=""):
  FFD1yO(self)
  try:
   self.timerUpdate.stop()
   if path:
    subtList, err = self.VVHx5k(path, enc=enc)
    if err    : self.close(err)
    elif not subtList : self.close("subtInval")
    else    :
     self.subtList = subtList
     CFG.subtDelaySec.setValue(int(delay))
     self.VVmCMC()
     self.VVvElS()
   else:
    path, delay, enc = CCSwZ2.VVh13g(self)
    if path:
     self.VVSYr1(path=path, delay=delay, enc=enc)
    else:
     self.VVrrUC()
  except:
   pass
 def VVvElS(self):
  posVal, durVal = self.VVbwNa()
  if self.VVYeIF(posVal):
   return
  CCSwZ2.VVjEWn(None)
  try:
   self.timerUpdate_conn = self.timerUpdate.timeout.connect(self.VVUBJP)
  except:
   self.timerUpdate.callback.append(self.VVUBJP)
  self.timerUpdate.start(500, False)
  try:
   self.timerEndText_conn = self.timerEndText.timeout.connect(self.VVSHAa)
  except:
   self.timerEndText.callback.append(self.VVSHAa)
  FFD1yO(self, "Subtitle started", 700, isGrn=True)
 def VVYeIF(self, posVal):
  capNum2, frmSec2, toSec2, subtLines2 = self.subtList[len(self.subtList) - 1]
  if posVal > toSec2:
   path = CCSwZ2.VVk2Xv(self)
   FFX92w(path)
   self.close("subtEnd")
   return True
  else:
   return False
 def VVrrUC(self):
  c1, c2, c3, c4, c5 = "", VVoTT6, VVNTmM, VVTdoW, VVMmz2
  VV625J = []
  VV625J.append((c1 + "Find srt Files (in all directories)"  , "allSrt"  ))
  VV625J.append((c1 + "Find srt Files (in Current Directory)" , "curDirSrt" ))
  VV625J.append(VVm77t)
  VV625J.append((c2 + "Manual Search (with File Manager)"  , "fileMan"  ))
  VV625J.append(VVm77t)
  VV625J.append((c3 + "Suggest srt files (25% similar)"   , "sugSrt0.25" ))
  VV625J.append((c3 + "Suggest srt files (50% similar)"   , "sugSrt0.50" ))
  VV625J.append((c3 + "Suggest srt files (75% similar)"   , "sugSrt0.70" ))
  if self.settingShown:
   VV625J.append(VVm77t)
   VV625J.append((c4 + "Change Subtitle File Encoding"  , "enc"   ))
   VV625J.append((c5 + "Disable Current Subtitle"   , "disab"  ))
   VV625J.append(VVm77t)
   VV625J.append(("Help (Keys)"        , "help"  ))
  FFuRfS(self, self.VVg18D, VV625J=VV625J, width=700, title='Find Subtitle ".srt" File', VVz2kc="#33221111", VVwpZm="#33110011")
 def VVg18D(self, item=None):
  if item:
   if   item == "allSrt"   : self.VVG3Ho(defSrt=self.lastSubtFile, mode=0)
   elif item == "curDirSrt"  : self.VVG3Ho(defSrt=self.lastSubtFile, mode=1)
   elif item == "fileMan"   :
    dir1 = CFG.lastFileManFindSrt.getValue()
    dir2 = CFG.MovieDownloadPath.getValue()
    sDir = "/"
    for path in (dir1, dir2, "/media/usb/movie/", "/media/hdd/movie/", "/media/"):
     if pathExists(path):
      sDir = path
      break
    self.session.openWithCallback(self.VViJeZ, BF(CC7ujK, mode=CC7ujK.VVWJV5, VVKDYx=sDir))
   elif item.startswith("sugSrt") : self.VVG3Ho(defSrt=self.lastSubtFile, mode=2, coeff=float(item[6:]))
   elif item == "enc":
    if self.lastSubtFile and fileExists(self.lastSubtFile) : FFlX3B(self, BF(CClXbe.VVq1FC, self, self.lastSubtFile, self.VV9nrF, defEnc=self.lastSubtEnc), title="Loading Codecs ...", clearMsg=False)
    else             : FFD1yO(self, "SRT File error", 1000)
   elif item == "disab":
    FFX92w(CCSwZ2.VVk2Xv(self))
    self.close("subtExit")
   elif item == "help"    : FF7SvB(self, VVASCC + "_help_subt", "Subtitle (Keys)")
  elif not self.settingShown:
   self.close("subtCancel")
 def VV9nrF(self, item=None):
  if item:
   FFlX3B(self, BF(self.VVSYr1, path=self.lastSubtFile, delay=CFG.subtDelaySec.getValue(), enc=item), title="Loading Subtitle ...")
 def VViJeZ(self, path):
  if path:
   FFnT3A(CFG.lastFileManFindSrt, os.path.dirname(path))
   self.VVSYr1(path=path)
  elif not self.settingShown:
   self.close("subtCancel")
 def VVG3Ho(self, defSrt="", mode=0, coeff=0.25):
  FFlX3B(self, BF(self.VV36EN, defSrt, mode=mode, coeff=coeff), title="Searching for srt files", clearMsg=False)
 def VV36EN(self, defSrt="", mode=0, coeff=0.25):
  FFD1yO(self)
  if mode == 1:
   srtList = CCSwZ2.VVDGBu(self)
   srtList.sort()
   title = "Subtitle Files (from Current Path)"
  else:
   srtList = FFiGf6('find / %s \( -iname "*.srt" \) | grep -i "\.srt"' % (FFlfqZ(1)))
   if srtList:
    srtList.sort()
    if mode == 2:
     title = "Subtitle Files (with Similar Names)"
     srtList, err = self.VVcsUv(srtList, coeff)
     if err:
      if self.settingShown: FFD1yO(self, err, 1500)
      else    : self.close(err)
      return
    else:
     title = "Subtitle Files (all srt files)"
  if srtList:
   VVvhuK = []
   curColor = "#f#0000FF00#"
   for path in srtList:
    fName, Dir = os.path.basename(path), FF0WrY(os.path.dirname(path))
    if defSrt == Dir + fName:
     fName, Dir = curColor + fName, curColor + Dir
    VVvhuK.append((fName, Dir))
   VVVHmY  = ("Select"    , self.VVilVH     , [])
   VVfPgM = self.VVMlvQ
   VV01dN = (""     , self.VVjKLR       , [])
   VVKx4L = (""     , BF(self.VVFUIc, defSrt, False) , [])
   VV3th8 = ("Find Current File" , BF(self.VVFUIc, defSrt, True) , [])
   header   = ("File" , "Directory" )
   widths   = (60  , 40   )
   FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVoJsQ=widths, VVmp7B=28, VVVHmY=VVVHmY, VVfPgM=VVfPgM, VV01dN=VV01dN, VVKx4L=VVKx4L, VV3th8=VV3th8, lastFindConfigObj=CFG.lastFindSubtitle
     , VVz2kc="#11002222", VVwpZm="#33001111", VVghPi="#33001111", VVAfLs="#11ffff00", VV0g1U="#11445544", VVooYw="#22222222", VVPVU2="#11002233")
  elif self.settingShown : FFD1yO(self, "Not found", 1500)
  else     : self.close("subtNoSrt")
 def VVMlvQ(self, VVcpnp):
  VVcpnp.cancel()
  if not self.settingShown:
   self.close("subtCancel")
 def VVjKLR(self, VVcpnp, title, txt, colList):
  fName, Dir = colList
  FFNEkd(VVcpnp, "%s\n\n%s%s" % (FFkhYI("Path:", VVoTT6), Dir, fName), title=title)
 def VVFUIc(self, path, VVl2X5, VVcpnp, title, txt, colList):
  for ndx, row in enumerate(VVcpnp.VVGrbO()):
   if path == row[1].strip() + row[0].strip():
    VVcpnp.VVtpKN(ndx)
    break
  else:
   if VVl2X5:
    FFD1yO(VVcpnp, "Not in list !", 1000)
 def VVilVH(self, VVcpnp, title, txt, colList):
  VVcpnp.cancel()
  path = "%s%s" % (colList[1].strip(), colList[0].strip())
  self.VVSYr1(path=path)
 def VVcsUv(self, srtList, coeff):
  lst = []
  err = ""
  serv = self.session.nav.getCurrentlyPlayingServiceReference()
  if serv and not serv.getPath():
   evName, evTime, evDur, evShort, evDesc, genre, PR = CCARMv.VVocQO(self)
  else:
   refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(self)
   evName = os.path.splitext(os.path.basename(chName))[0]
  if evName:
   lst, err = CCSwZ2.VVUhbW(evName, srtList, 50, coeff)
   if not err and not lst: err = "No Similar Names !"
  else:
   err = "No event Name !"
  return lst, err
 def VVHx5k(self, path, enc=None):
  if not fileExists(path):
   return [], "File not found"
  if (FFT03z(path) > 1024 * 700):
   return [], "File too big"
  frmSec = toSec = bold = italic = under = 0
  capNum  = ""
  capFound = True
  color  = ""
  subtLines = []
  subtList = []
  lines  = FFjdnJ(path, encLst=enc if enc else None)
  lastNdx  = len(lines) - 1
  for ndx, line in enumerate(lines):
   line = str(line).strip()
   if line:
    if line.isdigit():
     capNum = line
    else:
     span = iSearch(r'(\d{2}:\d{2}:\d{2},\d{3})\s*\-->\s*(\d{2}:\d{2}:\d{2},\d{3})', line, IGNORECASE)
     if span:
      p  = list(map(int, span.group(1).replace(",", ":").split(":")))
      frmSec = p[0] * 3600 + p[1] * 60 + p[2] + p[3] / 1000.0
      p  = list(map(int, span.group(2).replace(",", ":").split(":")))
      toSec = p[0] * 3600 + p[1] * 60 + p[2] + p[3] / 1000.0
      subtLines = []
     else:
      span = iSearch(r'<font color="(.+)">(.+)', line, IGNORECASE)
      if span:
       color = self.VVRdGH(span.group(1))
       line = span.group(2)
      if "<b>" in line: bold = 1
      if "<i>" in line: italic = 1
      if "<u>" in line: under = 1
      line = line.replace("</font>", "").replace("</b>", "").replace("</i>", "").replace("</u>", "")
      line = line.replace("<b>", "").replace("<i>", "").replace("<u>", "")
      span = iSearch(r"{\\a\d}(.+)", line, IGNORECASE)
      if span:
       line = span.group(1)
      subtLines.append((line.strip(), color, bold, italic, under))
      if ndx == lastNdx and subtList and (toSec - frmSec) > 0 and not subtList[len(subtList) - 1] == (capNum, frmSec, toSec, subtLines):
       subtList.append((capNum, frmSec, toSec, subtLines))
   else:
    if toSec > frmSec and subtLines:
     subtList.append((capNum, frmSec, toSec, subtLines))
    frmSec = toSec = bold = italic = under = 0
    capNum  = ""
    color  = ""
    subtLines = []
  if subtList:
   self.lastSubtFile = path
   self.lastSubtEnc  = enc
   self.VVExmX()
  return subtList, ""
 def VVRdGH(self, color):
  lst = { "black": "#000000", "blue": "#0000ff", "brown":"#a52a2a", "cyan":"#00ffff", "darkblue": "#0000a0", "gray":"#808080", "green":"#008000", "grey": "#808080", "lightblue":"#add8E6", "lime":"#00ff00", "magenta":"#ff00ff", "maroon":"#800000", "olive":"#808000", "orange":"#ffa500", "purple":"#800080", "red":"#ff0000", "silver":"#c0c0c0", "white":"#ffffff", "yellow":"#ffff00"}
  code = lst.get(color.lower(), "")
  if code:
   return code
  else:
   span = iSearch(r"(#[A-Fa-f0-9]{6})", color, IGNORECASE)
   if span : return span.group(1)
   else : return ""
 def VVExmX(self):
  path = CCSwZ2.VVk2Xv(self)
  if path:
   try:
    with open(path, "w") as f:
     f.write("srt=%s\n" % self.lastSubtFile)
     f.write("delay=%s\n" % CFG.subtDelaySec.getValue())
     if self.lastSubtEnc:
      f.write("enc=%s\n" % self.lastSubtEnc)
   except:
    pass
 def VVUBJP(self, force=False):
  posVal, durVal = self.VVbwNa()
  if self.VVYeIF(posVal):
   return
  self.VVLgOp(posVal)
  if self.currentIndex == -2:
   return
  txtDur = 0
  if posVal:
   capNum, frmSec, toSec, subtLines = self.subtList[self.currentIndex]
   if force or not self.lastSubtInfo == subtLines:
    self.lastSubtInfo = subtLines
    settingColor = ""
    if CFG.subtTextFg.getValue().startswith("#"):
     settingColor = CFG.subtTextFg.getValue()
    self.VVSHAa()
    subtLines = list(subtLines)
    l = len(subtLines)
    for i in range(3 - len(subtLines)):
     subtLines.insert(0, ("", "", 0, 0, 0))
    align = CFG.subtTextAlign.getValue()
    boxWidth= self.instance.size().width()
    for ndx, (line, color, bold, italic, under) in enumerate(subtLines):
     txtDur = int(toSec * 1000 - frmSec * 1000)
     if txtDur > 0:
      if line:
       if   bold   : newColor = "#aaffff"
       elif italic   : newColor = "#aaaaaa"
       elif under   : newColor = "#ffffaa"
       elif settingColor : newColor = settingColor
       elif color   : newColor = color
       else    : newColor = ""
       if ndx < 3:
        line = line.replace("\\u202A", "")
        line = line.replace("\\u202B", "")
        line = line.replace("\\u202C", "")
        line = line.replace("\r", "..").replace("\n", "..")
        line = str(line)
        if newColor:
         FFlr8P(self["mySubt%d" % ndx], newColor)
        self["mySubt%d" % ndx].setText(line)
        self["mySubt%d" % ndx].show()
        inst = self["mySubt%d" % ndx].instance
        w   = inst.calculateSize().width() + 50
        inst.resize(eSize(*(w, inst.size().height())))
        if   align == "0" : left = 0
        elif align == "2" : left = boxWidth - w
        else    : left = int((getDesktop(0).size().width() - w) / 2.0)
        inst.move(ePoint(left, int(inst.position().y())))
      self.timerEndText.start(txtDur, True)
 def VVbwNa(self):
  seekable, percVal, durVal, posVal, remVal, percTxt, durTxt, posTxt, remTxt = CCppdx.VV7UBu(self)
  if not durVal and not posVal:
   evName, evTime, evDur, evShort, evDesc, genre, PR = CCARMv.VVocQO(self)
   if evTime and evDur:
    posVal, durVal = iTime() - evTime, evDur
  return posVal, durVal
 def VVLgOp(self, posVal):
  if posVal > 0:
   delay = CFG.subtDelaySec.getValue()
   for ndx, item in enumerate(self.subtList):
    frmSec = item[1] + delay
    toSec = item[2] + delay
    if posVal > frmSec and posVal < toSec:
     self.currentIndex = ndx
     return
  self.currentIndex = -2
 def VVSHAa(self):
  for i in range(3):
   self["mySubt%d" % i].setText("")
   FFlr8P(self["mySubt%d" % i], "#00ffffff")
   self["mySubt%d" % i].hide()
 def VVaU2w(self):
  FFlX3B(self, self.VVc28J, title="Loading Lines ...", clearMsg=False)
 def VVc28J(self):
  FFD1yO(self)
  VVvhuK = []
  for cap, frm, to, lines in self.subtList:
   firstLine = lines[0][0] if lines else ""
   VVvhuK.append((cap, FF3UDS(frm), str(frm), firstLine))
  if VVvhuK:
   title = "Select Current Subtitle Line"
   VVVHmY  = ("Select"   , self.VVSWot , [title])
   VVKx4L = (""    , self.VVI648 , [False])
   VV3th8 = ("Current Line" , self.VVI648 , [True])
   VVOtSO = ("Reset Delay" , self.VVJvZE , [])
   VV1QO7 = ("New Delay"  , self.VVZSkX   , [])
   header   = ("Cap" , "Time", "Time Val", "Subtitle Text" )
   widths   = (8  , 15 , 0    , 77    )
   VVQqg2  = (CENTER , CENTER, CENTER , LEFT    )
   VVcpnp = FF1dQ4(self, None, title=title, header=header, VVvytR=VVvhuK, VVQqg2=VVQqg2, VVoJsQ=widths, VVmp7B=28, VVVHmY=VVVHmY, VVKx4L=VVKx4L, VV3th8=VV3th8, VVOtSO=VVOtSO, VV1QO7=VV1QO7
          , VVz2kc="#33002222", VVwpZm="#33001111", VVghPi="#33110011", VVAfLs="#11ffff00", VV0g1U="#11223025", VVooYw="#22222222", VVPVU2="#33002233")
   if CFG.subtDelaySec.getValue():
    VVcpnp["keyYellow"].show()
    VVcpnp["keyYellow"].setText("Reset Delay (%s sec)" % CFG.subtDelaySec.getValue())
   else:
    VVcpnp["keyYellow"].hide()
   VVcpnp["keyBlue"].setText("New Delay: %s sec" % CFG.subtDelaySec.getValue())
   FFobAA(VVcpnp["keyBlue"], "#22222222")
   VVcpnp.VViPb6(BF(self.VVgtgB, VVcpnp))
  else:
   FFD1yO(self, "Cannot read lines !", 2000)
 def VVSWot(self, VVcpnp, Title):
  delay, color, allow = self.VVDUJz(VVcpnp)
  if allow:
   VVcpnp.cancel()
   self.VVKtu1(delay, True)
  else:
   FFD1yO(VVcpnp, "Delay out of range", 1500)
 def VVI648(self, VVcpnp, VVl2X5):
  posVal, durVal = self.VVbwNa()
  if posVal > 0:
   curTime = posVal - float(CFG.subtDelaySec.getValue())
   for ndx, row in enumerate(VVcpnp.VVGrbO()):
    cap, at, atVal, l1 = list(map(str.strip, row))
    atVal = float(atVal)
    if atVal > curTime:
     VVcpnp.VVtpKN(ndx)
     break
   else:
    if VVl2X5: FFD1yO(VVcpnp, "Not found", 2000)
  elif VVl2X5:
   FFD1yO(VVcpnp, "Current Playing Position = 0 !", 2000)
 def VVJvZE(self, VVcpnp, title, txt, colList):
  if VVcpnp["keyYellow"].getVisible():
   self.VVKtu1(0, True)
   VVcpnp["keyYellow"].hide()
   self.VVI648(VVcpnp, False)
 def VVgtgB(self, VVcpnp):
  delay, color, allow = self.VVDUJz(VVcpnp)
  VVcpnp["keyBlue"].setText("%sNew Delay: %d sec" % (color, delay))
 def VVDUJz(self, VVcpnp):
  lineTime = float(VVcpnp.VVPxSj()[2].strip())
  posVal, durVal = self.VVbwNa()
  delay, color, allow = 0, "", False
  if posVal > 0:
   val = int(round(posVal - lineTime))
   if -600 <= val <= 600: allow, color = True , VVk6tE
   else     : allow, color = False, VVMmz2
   delay = FF2DVg(val, -600, 600)
  return delay, color, allow
 def VVZSkX(self, VVcpnp, title, txt, colList):
  pass
 @staticmethod
 def VVJgMd(SELF):
  path, delay, enc = CCSwZ2.VVh13g(SELF)
  return True if path else False
 @staticmethod
 def VVh13g(SELF):
  path, delay, enc = CCSwZ2.VVmKgQ(SELF)
  if not path:
   path = CCSwZ2.VVsFpi(SELF)
  return path, delay, enc
 @staticmethod
 def VVmKgQ(SELF):
  srtCfgPath = CCSwZ2.VVk2Xv(SELF)
  path = enc = ""
  delay = 0
  if srtCfgPath:
   if fileExists(srtCfgPath):
    lines = FFjdnJ(srtCfgPath)
    for line in lines:
     line = line.strip()
     if   line.startswith("srt=") : path = line.split("=")[1].strip()
     elif line.startswith("delay=") : delay = line.split("=")[1].strip()
     elif line.startswith("enc=") : enc = line.split("=")[1].strip()
  if path and fileExists(path):
   try:
    delay = int(delay)
   except:
    pass
   return path, delay, enc
  else:
   return "", 0, ""
 @staticmethod
 def VVk2Xv(SELF):
  fPath, fDir, fName = CC7ujK.VVa1tR(SELF)
  if not fPath:
   evName, evTime, evDur, evShort, evDesc, genre, PR = CCARMv.VVocQO(SELF)
   if evName.strip() and evTime and evDur:
    fPath = "/tmp/" + evName[:30].strip()
  if not fPath:
   refCode, decodedUrl, origUrl, iptvRef, chName, prov, state = FFnQlZ(SELF)
   if chName.strip():
    fPath = "/tmp/" + chName.strip()
  if fPath: return fPath + ".ajp"
  else : return ""
 @staticmethod
 def VVsFpi(SELF):
  bestRatio = 0
  fPath, fDir, fName = CC7ujK.VVa1tR(SELF)
  if fName:
   movName = os.path.splitext(fName)[0]
   paths = CCSwZ2.VVDGBu(SELF)
   bLst, err = CCSwZ2.VVUhbW(movName, paths, 1, 0.3)
   if bLst:
    return bLst[0]
  return ""
 @staticmethod
 def VVDGBu(SELF):
  fPath, fDir, fName = CC7ujK.VVa1tR(SELF)
  if pathExists(fDir):
   files = iGlob("%s*.srt" % fDir)
   if files:
    return files
  return []
 @staticmethod
 def VVUhbW(word, paths, n=-1, cutoff=0.3):
  lst  = []
  if paths:
   try:
    from difflib import get_close_matches as iClosest
   except:
    return lst, 'Missing "difflib" library'
   if n == -1:
    n = len(paths)
   files = []
   for ndx, p in enumerate(paths):
    fName = os.path.splitext(os.path.basename(os.path.basename(p)))[0]
    files.append("%d,%s" % (ndx, fName))
   bLst = iClosest(word, files, n=n, cutoff=cutoff)
   if bLst:
    for item in bLst:
     ndx, fName = item.split(",", 1)
     lst.append(paths[int(ndx)])
  return lst, ""
 @staticmethod
 def VVre4L():
  try:
   return InfoBar.instance.selected_subtitle
  except:
   try:
    return InfoBar.instance.__selected_subtitle
   except:
    return None
 @staticmethod
 def VVjEWn(subt):
  if subt and isinstance(subt, tuple) and len(subt) >= 4 : state = True
  else             : subt, state = None, False
  try:
   InfoBar.instance.enableSubtitle(subt)
  except:
   try:
    if state:
     InfoBar.instance.__selected_subtitle = subt
    InfoBar.instance.setSubtitlesEnable(state)
   except:
    pass
  CCSwZ2.VVEf3M()
 @staticmethod
 def VVEf3M():
  try:
   if config.subtitles.show.value : InfoBar.instance.subtitle_window.show()
   else       : InfoBar.instance.subtitle_window.hide()
  except:
   pass
class CC3sIb(ScrollLabel):
 def __init__(self, parentSELF, text="", VVJSxJ=True):
  ScrollLabel.__init__(self, text)
  self.VVJSxJ   = VVJSxJ
  self.long_text    = None
  self.scrollbar    = None
  self.message    = text
  self.instance    = None
  self.VVKnNX  = 0
  self.curPos     = 0
  self.pageHeight    = 0
  self.column     = 0
  self.outputFileToSave  = ""
  self.parentSELF    = parentSELF
  self.isResizable   = None
  self.minHeight    = 40
  self.fontFamily    = None
  self.VVmp7B    = None
  self.parentW    = None
  self.parentH    = None
  self.firstTime    = True
  self.wrapEnabled   = True
  parentSELF["keyRedTop"]  = Label("Menu")
  parentSELF["keyGreenTop"] = Label("Reset")
  parentSELF["keyYellowTop"] = Label("Font -")
  parentSELF["keyBlueTop"] = Label("Font +")
  parentSELF["keyRedTop1"] = Label()
  parentSELF["keyGreenTop1"] = Label()
  parentSELF["keyYellowTop1"] = Label()
  parentSELF["keyBlueTop1"] = Label()
  parentSELF["myAction"]  = ActionMap(["KeyMap_RC", "KeyMap_KeyBoard"],
  {
   "ok"   : parentSELF.close  ,
   "cancel"  : parentSELF.close  ,
   "menu"   : self.VVq0lp ,
   "green"   : self.VVd5HQ ,
   "yellow"  : self.VVztuC ,
   "blue"   : self.VVY7Qq ,
   "up"   : self.pageUp   ,
   "down"   : self.pageDown   ,
   "left"   : self.pageUp   ,
   "right"   : self.pageDown   ,
   "last"   : BF(self.VVwG80, 0) ,
   "0"    : BF(self.VVwG80, 1) ,
   "next"   : BF(self.VVwG80, 2) ,
   "pageUp"  : self.VV18SD   ,
   "chanUp"  : self.VV18SD   ,
   "pageDown"  : self.VVkrUD   ,
   "chanDown"  : self.VVkrUD
  }, -1)
 def VVqCbn(self, isResizable=True, VVXeWx=False, outputFileToSave=""):
  self.outputFileToSave = outputFileToSave
  FFlr8P(self.parentSELF["keyRedTop"], "#0055FF55" if outputFileToSave else "#00FFFFFF" )
  FFobAA(self.parentSELF["keyRedTop"], "#113A5365")
  FFtIlI(self.parentSELF, True)
  self.isResizable = isResizable
  if VVXeWx:
   self.long_text.setHAlign(1)
  size    = self.parentSELF.instance.size()
  self.parentW  = size.width()
  self.parentH  = size.height()
  font    = self.long_text.getFont()
  self.fontFamily  = font.family
  self.VVmp7B  = font.pointSize
  try: self.scrollbar.setBorderColor(parseColor("#11555555"))
  except: pass
  try: self.scrollbar.setForegroundColor(parseColor("#11AA8E48"))
  except: pass
  try: self.scrollbar.setBackgroundColor(parseColor("#11111111"))
  except: pass
  color = self.parentSELF.skinParam["bodyColor"]
  FFobAA(self, color)
 def VVtRDN(self, color):
  self.long_text.setBackgroundColor(parseColor(color))
 def applySkin(self, desktop, parent):
  import skin
  from enigma import eLabel, eSlider
  self.long_text = eLabel(self.instance)
  self.scrollbar = eSlider(self.instance)
  skin.applyAllAttributes(self.long_text, desktop, self.skinAttributes, parent.scale)
  self.pageWidth = self.long_text.size().width()
  lineheight  = int(fontRenderClass.getInstance().getLineHeight(self.long_text.getFont())) or 30
  lines   = int(self.long_text.size().height() / lineheight)
  margin   = int(lineheight / 6)
  self.pageHeight = int(lines * lineheight)
  self.instance.move(self.long_text.position())
  self.instance.resize(eSize(self.pageWidth, self.pageHeight + margin))
  w = 20
  self.scrollbar.move(ePoint(self.pageWidth - w, 0))
  self.scrollbar.resize(eSize(w, self.pageHeight + margin))
  self.scrollbar.setOrientation(eSlider.orVertical)
  self.scrollbar.setRange(0, 100)
  self.scrollbar.setBorderWidth(1)
  self.setText(self.message)
  return True
 def setPos(self, pos):
  self.curPos = max(0, min(pos, self.VVKnNX - self.pageHeight))
  self.long_text.move(ePoint(0, -self.curPos))
  self.VVtIIQ()
 def pageUp(self):
  if self.VVKnNX > self.pageHeight:
   self.setPos(self.curPos - self.pageHeight)
 def pageDown(self):
  if self.VVKnNX > self.pageHeight:
   self.setPos(self.curPos + self.pageHeight)
 def VV18SD(self):
  self.setPos(0)
 def VVkrUD(self):
  self.setPos(self.VVKnNX-self.pageHeight)
 def VVXIU1(self):
  return self.VVKnNX <= self.pageHeight or self.curPos == self.VVKnNX - self.pageHeight
 def getText(self):
  return self.message
 def VVtIIQ(self):
  try:
   vis = int(max(100 * self.pageHeight / self.VVKnNX, 3))
   start = int((100 - vis) * self.curPos / (self.VVKnNX - self.pageHeight))
   self.scrollbar.setStartEnd(start, start + vis)
  except:
   pass
 def setText(self, text, VVKsoz=VVw3Mn):
  old_VVXIU1 = self.VVXIU1()
  self.message = str(text)
  if self.pageHeight:
   self.long_text.setText(self.message)
   self.VVKnNX = self.long_text.calculateSize().height()
   if self.VVJSxJ and self.VVKnNX > self.pageHeight:
    self.scrollbar.show()
    self.VVtIIQ()
    w = self.parentSELF.skinParam["scrollBarW"] + 5
   else:
    self.scrollbar.hide()
    w = 0
   pageWidth  = self.instance.size().width()
   self.long_text.resize(eSize(pageWidth - w, self.VVKnNX))
   if   VVKsoz == VV72id: self.setPos(0)
   elif VVKsoz == VVtPPw : self.VVkrUD()
   elif old_VVXIU1    : self.VVkrUD()
   if self.firstTime and len(self.message) > 0:
    self.firstTime = False
    self.setText(self.message, VVKsoz=VVKsoz)
 def appendText(self, text, VVKsoz=VVtPPw):
  self.setText(self.message + str(text), VVKsoz=VVKsoz)
 def VVztuC(self):
  size = int(self.long_text.getFont().pointSize * 0.8)
  if size > 5:
   self.VVdIGQ(size)
 def VVY7Qq(self):
  size = int(self.long_text.getFont().pointSize * 1.2)
  if size < 80:
   self.VVdIGQ(size)
 def VVd5HQ(self):
  self.VVdIGQ(self.VVmp7B)
 def VVdIGQ(self, VVmp7B):
  self.long_text.setFont(gFont(self.fontFamily, VVmp7B))
  self.setText(self.message, VVKsoz=VVw3Mn)
  self.VVw0Hf(calledFromFontSizer=True)
 def VVwG80(self, align):
  self.long_text.setHAlign(align)
 def VVq0lp(self):
  VV625J = []
  VV625J.append(("%s Wrapping" % ("Disable" if self.wrapEnabled else "Enable"), "wrap" ))
  VV625J.append(VVm77t)
  VV625J.append(("Align Left"  , "left" ))
  VV625J.append(("Align Center"  , "center" ))
  VV625J.append(("Align Right"  , "right" ))
  if self.outputFileToSave:
   VV625J.append(VVm77t)
   VV625J.append((FFkhYI("Save to File", VVoTT6), "save" ))
  VV625J.append(VVm77t)
  VV625J.append(("Keys (Shortcuts)" , "help" ))
  FFuRfS(self.parentSELF, self.VVxWmq, VV625J=VV625J, title="Text Option", width=500)
 def VVxWmq(self, item=None):
  if item:
   if item == "wrap"  :
    self.wrapEnabled = not self.wrapEnabled
    self.long_text.setNoWrap(not self.wrapEnabled)
   elif item == "left"  : self.VVwG80(0)
   elif item == "center" : self.VVwG80(1)
   elif item == "right" : self.VVwG80(2)
   elif item == "save"  : self.VVH8TK()
   elif item == "help"  : FF7SvB(self.parentSELF, VVASCC + "_help_txt", "Text Viewer (Keys)")
 def VVH8TK(self):
  title = "%s Log File" % self.outputFileToSave.capitalize()
  expPath = CFG.exportedTablesPath.getValue()
  try:
   outF = "%sAJPanel_log_%s_%s.txt" % (FF0WrY(expPath), self.outputFileToSave, FFGuM2())
   with open(outF, "w") as f:
    f.write(FFO8d5(self.message))
   FFewCE(self.parentSELF, "Saved to:\n\n%s" % outF, title=title)
  except:
   FFkYsE(self.parentSELF, "Could not save to:\n\n%s" % expPath, title=title)
 def VVw0Hf(self, calledFromFontSizer=False, minHeight=0):
  if minHeight > 0:
   self.minHeight = minHeight
  if not calledFromFontSizer and self.VVKnNX > 0 and self.pageHeight > 0:
   if self.VVKnNX < self.pageHeight * 0.8:
    if not self.message.startswith("\n"):
     self.message = "\n" + self.message
    self.setText(self.message.rstrip() + "\n")
  if self.isResizable:
   pageH = self.pageHeight
   textH = self.VVKnNX
   diff = pageH - textH
   newH = self.parentH - diff
   if diff < 0:
    newH = self.parentH
   self.resize(eSize(*(self.instance.size().width(), min(textH, pageH) + 6)))
   newH = min(self.parentH, self.getPosition()[1] + textH + self.parentSELF.skinParam["marginTop"])
   if self.minHeight > 0:
    newH = max(newH, self.minHeight + self.parentSELF.skinParam["titleH"] + self.parentSELF.skinParam["marginTop"] * 2 + 1)
   screenSize = getDesktop(0).size()
   self.parentSELF.instance.resize(eSize(*(self.parentW, newH)))
   self.parentSELF.instance.move(ePoint((screenSize.width() - self.parentW) // 2, (screenSize.height() - newH) // 2))
