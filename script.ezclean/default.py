# -*- coding: utf-8 -*-

import re,os,sys,urllib,requests,time
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from resources.lib.modules import control,tools

AddonID = 'script.ezclean'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
selfAddon = xbmcaddon.Addon(id=AddonID)
wizard1 = control.setting('enable_wiz1')
wizard2 = control.setting('enable_wiz2')
wizard3 = control.setting('enable_wiz3')
backupfull = control.setting('backup_database')
backupaddons = control.setting('backup_addon_data')
backupzip = control.setting("remote_backup")
USB = xbmc.translatePath(os.path.join(backupzip))
ADDON_FANART = control.addonFanart()
ADDON_ICON = control.addonIcon()
backupdir = xbmc.translatePath(os.path.join('special://home/backupdir',''))
packagesdir = xbmc.translatePath(os.path.join('special://home/addons/packages',''))
USERDATA = xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA = xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
HOME = xbmc.translatePath('special://home/')
HOME_ADDONS = xbmc.translatePath('special://home/addons')
backup_zip = xbmc.translatePath(os.path.join(backupdir,'backup_addon_data.zip'))
dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()
AddonTitle = "EZ Clean"
EXCLUDES = [AddonID, 'backupdir','backup.zip','script.module.requests','script.module.urllib3','script.module.chardet','script.module.idna','script.module.certifi','repository.jewrepo']
EXCLUDES_ADDONS = ['notification','packages']

def SETTINGS():
    xbmcaddon.Addon(id=AddonID).openSettings()

def ENABLE_WIZARD():
    try:
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (AddonID)
        xbmc.executeJSONRPC(query)
    except:
        pass

def CATEGORIES():
    CreateDir('[COLOR white][B]MAINTENANCE[/B][/COLOR]','ur', 'maintenance', ADDON_ICON,ADDON_FANART,'', isFolder=True)
    CreateDir('[COLOR white][B]LOG VIEWER/UPLOADER[/B][/COLOR]','ur', 'log_tools', ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]TOOLS[/B][/COLOR]','ur','tools',ADDON_ICON,ADDON_FANART,'', isFolder=True)
    CreateDir('[COLOR white][B]SETTINGS[/B][/COLOR]','ur','settings',ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]SHOW CHANGELOG[/B][/COLOR]','ur','changeLog',ADDON_ICON,ADDON_FANART,'')

def CAT_TOOLS():
    CreateDir('[COLOR white][B]ADVANCED SETTINGS (BUFFER SIZE)[/B][/COLOR]','ur', 'adv_settings', ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]FORCE UPDATES[/B][/COLOR]','ur', 'forceUpdate', ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]BACKUP/RESTORE[/B][/COLOR]','ur','backup_restore',ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]BUILDS/WIZARD[/B][/COLOR]','ur','builds',ADDON_ICON,ADDON_FANART,'', isFolder=True)
    CreateDir('[COLOR red][B]FRESH START[/B][/COLOR]','url','fresh_start',ADDON_ICON,ADDON_FANART,'')

def MAINTENANCE():
    CreateDir('[COLOR white][B]Clear Cache[/B][/COLOR]','url','clear_cache',ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]Clear Packages[/B][/COLOR]','url','clear_packages',ADDON_ICON,ADDON_FANART,'')
    CreateDir('[COLOR white][B]Clear Thumbnails[/B][/COLOR]','url','clear_thumbs',ADDON_ICON,ADDON_FANART,'')

def OPEN_URL(url):
    r = requests.get(url).content
    return r

def BUILDS():
    if wizard1 != 'false':
        try:
            name = unicode(control.setting('name1'))
            url = unicode(control.setting('url1'))
            img = unicode(control.setting('img1'))
            fanart = unicode(control.setting('img1'))
            CreateDir('[COLOR lime][B][Wizard][/B][/COLOR] ' + name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    if wizard2 != 'false':
        try:
            name = unicode(selfAddon.getSetting('name2'))
            url = unicode(selfAddon.getSetting('url2'))
            img = unicode(selfAddon.getSetting('img2'))
            fanart = unicode(selfAddon.getSetting('img2'))
            CreateDir('[COLOR skyblue][B][Wizard][/B][/COLOR] ' +name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    if wizard3 != 'false':
        try:
            name = unicode(selfAddon.getSetting('name3'))
            url = unicode(selfAddon.getSetting('url3'))
            img = unicode(selfAddon.getSetting('img3'))
            fanart = unicode(selfAddon.getSetting('img3'))
            CreateDir('[COLOR cyan][B][Wizard][/B][/COLOR] ' +name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    CreateDir('[COLOR white][B]WIZARD SETTINGS[/B][/COLOR]','ur','wizSettings',ADDON_ICON,ADDON_FANART,'')

def FRESHSTART(mode='verbose'):
    if mode != 'silent': select = xbmcgui.Dialog().yesno("EZ Clean", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
    else: select = 1
    if select == 0: return
    elif select == 1:
        progressDialog.create(AddonTitle,"Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    # RESTOREFAV()
    # ENABLE_WIZARD()
    if mode != 'silent': dialog.ok(AddonTitle,'Wipe Successful, The interface will now be reset...','','')
    # xbmc.executebuiltin('Mastermode')
    if mode != 'silent': xbmc.executebuiltin('LoadProfile(Master user)')
    # xbmc.executebuiltin('Mastermode')

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        try:
            if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
                empty_count += 1 #increment empty_count
                os.rmdir(curdir) #delete the directory
                print "successfully removed: "+curdir
            elif len(subdirs) > 0 and len(files) > 0: #check for used directories
                used_count += 1 #increment used_count
        except:pass

def killxbmc():
    dialog.ok("PROCESS COMPLETE", 'The skin will now be reset', 'To start using your new setup please switch the skin System > Appearance > Skin to the desired one... if images are not showing, just restart Kodi', 'Click OK to Continue')
    # xbmc.executebuiltin('Mastermode')
    xbmc.executebuiltin('LoadProfile(Master user)')
    # xbmc.executebuiltin('Mastermode')

def CreateDir(name, url, action, icon, fanart, description, isFolder=False):
    if icon == None or icon == '': icon = ADDON_ICON
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+str(action)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(icon)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    return ok

def ForceUpdate():
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    xbmc.executebuiltin("UpdateAddonRepos")
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (AddonTitle,  'Checking for Updates...' , '5000', ADDON_ICON))

def WizSettings():
	from resources.lib.modules import control
	control.openSettings(query='2.0')

from urlparse import parse_qsl

params = dict(parse_qsl(sys.argv[2].replace('?','')))
action = params.get('action')
icon = params.get('icon')
name = params.get('name')
title = params.get('title')
year = params.get('year')
fanart = params.get('fanart')
tvdb = params.get('tvdb')
tmdb = params.get('tmdb')
season = params.get('season')
episode = params.get('episode')
tvshowtitle = params.get('tvshowtitle')
premiered = params.get('premiered')
url = params.get('url')
image = params.get('image')
meta = params.get('meta')
select = params.get('select')
query = params.get('query')
description = params.get('description')
content = params.get('content')

if action == None: CATEGORIES()
elif action == 'builds': BUILDS()
elif action == 'tools': CAT_TOOLS()
elif action == 'maintenance': MAINTENANCE()
elif action == 'forceUpdate': ForceUpdate()
elif action == 'wizSettings': WizSettings()
elif action == 'settings': control.openSettings()

elif action == 'adv_settings':
    from resources.lib.modules import tools
    tools.advancedSettings()

elif action == 'changeLog':
    from resources.lib.modules import changelog
    changelog.get()

elif action == 'log_tools':
    from resources.lib.modules import logviewer
    logviewer.logView()

elif action == 'clear_cache':
    from resources.lib.modules import maintenance
    maintenance.clearCache()

elif action == 'clear_packages':
    from resources.lib.modules import maintenance
    maintenance.purgePackages()

elif action == 'clear_thumbs':
    from resources.lib.modules import maintenance
    maintenance.deleteThumbnails()

elif action == 'fresh_start':
    dialog.ok(AddonTitle,'Before Proceeding please switch skin to the default Kodi... Confluence or Estuary...','','')
    from resources.lib.modules import wiz
    wiz.skinswap()
    FRESHSTART()

elif action == 'backup_restore':
    from resources.lib.modules import wiz
    typeOfBackup = ['BACKUP', 'RESTORE']
    s_type = control.selectDialog(typeOfBackup)
    if s_type == 0:
        modes = ['Full Backup', 'Addons Settings']
        select = control.selectDialog(modes)
        if select == 0: wiz.backup(mode='full')
        elif select == 1: wiz.backup(mode='userdata')
    elif s_type == 1: wiz.restoreFolder()

elif action == 'install_build':
    from resources.lib.modules import wiz
    wiz.skinswap()
    yesDialog = dialog.yesno(AddonTitle, 'Do you want to perform a Fresh Start before Installing your Build?', yeslabel='Yes', nolabel='No')
    if yesDialog: FRESHSTART(mode='silent')
    wiz.buildInstaller(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

