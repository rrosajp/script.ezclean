# -*- coding: UTF-8 -*-

import xbmc,xbmcvfs,xbmcaddon,xbmcgui,re,os,glob,thread
from datetime import datetime
try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

def log(self, msg, level=xbmc.LOGNOTICE):
    try:
        if isinstance(msg, unicode):
            msg = '%s' % (msg.encode('utf-8'))
        xbmc.log('[EZ Clean]: %s' % msg, level)
    except Exception as e:
        try: xbmc.log('[EZ Clean] Logging Failure: %s' % (e), xbmc.LOGERROR)
        except: pass

def swapUS():
    new = '"addons.unknownsources"'
    value = 'true'
    query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (new)
    response = xbmc.executeJSONRPC(query)
    if 'true' in response:
        xbmcgui.Dialog().notification("EZ Clean", "Unknown Sources: Already Enabled.")
    if 'false' in response:
        #thread.start_new_thread(dialogWatch, ())
        xbmc.sleep(200)
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = xbmc.executeJSONRPC(query)
        xbmcgui.Dialog().notification("EZ Clean", "Unknown Sources: Enabled.")

def dialogWatch():
    x = 0
    while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 100:
        x += 1
        xbmc.sleep(100)
    if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
        xbmc.executebuiltin('SendClick(11)')

