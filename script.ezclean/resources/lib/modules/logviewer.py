# -*- coding: utf-8 -*-

import re,os,sys,urllib,urllib2,time
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from resources.lib.modules import control
from datetime import datetime

dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
addonInfo = xbmcaddon.Addon().getAddonInfo
AddonTitle = "EZ Clean"
AddonID = 'script.ezclean'

def open_Settings():
    open_Settings = xbmcaddon.Addon(id=AddonID).openSettings()

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def logView():
    modes = ['View Log', 'Upload Log to Pastebin']
    logPaths = []
    logNames = []
    select = control.selectDialog(modes)
    try:
        if select == -1: raise Exception()
        logfile_path = xbmc.translatePath('special://logpath')
        logfile_names = ('kodi.log', 'kodi.old.log', 'xbmc.log', 'xbmc.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'freetelly.log', 'ftmc.log', 'firemc.log', 'nodi.log', 'scrubsv2.log')
        for logfile_name in logfile_names:
            log_file_path = os.path.join(logfile_path, logfile_name)
            if os.path.isfile(log_file_path):
                logNames.append(logfile_name)
                logPaths.append(log_file_path)
        selectLog = control.selectDialog(logNames)
        selectedLog = logPaths[selectLog]
        if selectLog == -1: raise Exception()
        if select == 0:
            from resources.lib.modules import TextViewer
            TextViewer.text_view(selectedLog)
        elif select == 1:
            f = open(selectedLog, 'r')
            text = f.read()
            f.close()
            from resources.lib.api import pastebin
            upload_Link = pastebin.api().paste(text)
            print ("LOGVIEW UPLOADED LINK", upload_Link)
            if upload_Link != None:
                if not "Error" in upload_Link:
                    label = "Log Link: [COLOR skyblue][B]" + upload_Link + "[/B][/COLOR]"
                    dialog.ok(AddonTitle, "Log Uploaded to Pastebin", label)
                else: dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin", "Reason " + upload_Link)
            else: dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin", "")
    except:pass

