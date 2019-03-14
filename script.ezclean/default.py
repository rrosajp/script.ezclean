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

def getMenuEnabled(menu_title):
    is_enabled = control.setting(menu_title).strip()
    if (is_enabled == '' or is_enabled == 'false'): return False
    return True

def CATEGORIES():
    if getMenuEnabled('navi.maintenance') == True:
        CreateDir('[B]MAINTENANCE[/B]','ur', 'maintenance', ADDON_ICON,ADDON_FANART,'', isFolder=True)
    if getMenuEnabled('navi.logviewer') == True:
        CreateDir('[B]LOG VIEWER/UPLOADER[/B]','ur', 'log_tools', ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.tools') == True:
        CreateDir('[B]TOOLS[/B]','ur','tools',ADDON_ICON,ADDON_FANART,'', isFolder=True)
    if getMenuEnabled('navi.settings') == True:
        CreateDir('[B]SETTINGS[/B]','ur','settings',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.changelog') == True:
        CreateDir('[B]SHOW CHANGELOG[/B]','ur','changeLog',ADDON_ICON,ADDON_FANART,'')

def CAT_TOOLS():
    if getMenuEnabled('navi.advansett') == True:
        CreateDir('[B]ADVANCED SETTINGS (BUFFER SIZE)[/B]','ur', 'adv_settings', ADDON_ICON,ADDON_FANART,'')
        CreateDir('[B]CLEAR ADVANCED SETTINGS (BUFFER SIZE)[/B]','ur', 'clearAdv_settings', ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.forcup') == True:
        CreateDir('[B]FORCE UPDATES[/B]','ur', 'forceUpdate', ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.enadd') == True:
        CreateDir('[B]ENABLE ALL ADDONS[/B]','ur', 'enableAddons', ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.enunsour') == True:
        CreateDir('[B]ENABLE UNKNOWN SOURCES[/B]','ur', 'enableUnknownSources', ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.backre') == True:
        CreateDir('[B]BACKUP/RESTORE[/B]','ur','backup_restore',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.builwiz') == True:
        CreateDir('[B]BUILDS/WIZARD[/B]','ur','builds',ADDON_ICON,ADDON_FANART,'', isFolder=True)
    if getMenuEnabled('navi.reloski') == True:
        CreateDir('[B][I]RELOAD SKIN[/I][/B]','ur','reloadMySkin',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.relopro') == True:
        CreateDir('[B][I]RELOAD PROFILE[/I][/B](MASTER USER)','ur','reloadUser',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.fresta') == True:
        CreateDir('[B][I]FRESH START[/I][/B]','url','fresh_start',ADDON_ICON,ADDON_FANART,'')

def MAINTENANCE():
    if getMenuEnabled('navi.clearemall') == True:
        CreateDir('[B]CLEAR ALL[/B](CACHE, PACKAGES, THUMBNAILS)','url','clear_ALL',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.clearcache') == True:
        CreateDir('[B]CLEAR CACHE[/B]','url','clear_cache',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.clearpack') == True:
        CreateDir('[B]CLEAR PACKAGES[/B]','url','clear_packages',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.clearthumb') == True:
        CreateDir('[B]CLEAR THUMBNAILS[/B]','url','clear_thumbs',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.clearempfold') == True:
        CreateDir('[B][I]CLEAR EMPTY FOLDERS[/I][/B]','url','clearEmptyFolders',ADDON_ICON,ADDON_FANART,'')
    if getMenuEnabled('navi.clearresolvecache') == True:
        CreateDir('[B][I]CLEAR RESOLVERS CACHE[/I][/B]','url','reset_ResolversCache',ADDON_ICON,ADDON_FANART,'')

def OPEN_URL(url):
    r = requests.get(url).content
    return r

def BUILDS():
    if wizard1!= 'false':
        try:
            name = unicode(control.setting('name1'))
            url = unicode(control.setting('url1'))
            img = unicode(control.setting('img1'))
            fanart = unicode(control.setting('img1'))
            CreateDir('[B][Wizard][/B] ' + name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    if wizard2!= 'false':
        try:
            name = unicode(selfAddon.getSetting('name2'))
            url = unicode(selfAddon.getSetting('url2'))
            img = unicode(selfAddon.getSetting('img2'))
            fanart = unicode(selfAddon.getSetting('img2'))
            CreateDir('[B][Wizard][/B] ' +name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    if wizard3!= 'false':
        try:
            name = unicode(selfAddon.getSetting('name3'))
            url = unicode(selfAddon.getSetting('url3'))
            img = unicode(selfAddon.getSetting('img3'))
            fanart = unicode(selfAddon.getSetting('img3'))
            CreateDir('[B][Wizard][/B] ' +name, url, 'install_build' , img, fanart, 'My custom Build', isFolder=False)
        except: pass
    CreateDir('[B]WIZARD SETTINGS[/B]','ur','wizSettings',ADDON_ICON,ADDON_FANART,'')

def FRESHSTART(mode='verbose'):
    if mode!= 'silent': select = xbmcgui.Dialog().yesno("EZ Clean", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
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
    if mode!= 'silent': dialog.ok(AddonTitle,'Wipe Successful, The interface will now be reset...','','')
    # xbmc.executebuiltin('Mastermode')
    if mode!= 'silent': xbmc.executebuiltin('LoadProfile(Master user)')
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

def ReloadMySkin():
	xbmc.executebuiltin("ReloadSkin()")

def WizSettings():
	from resources.lib.modules import control
	control.openSettings(query='3.0')

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
elif action == 'reloadUser': killxbmc()
elif action == 'reloadMySkin': ReloadMySkin()

elif action == 'enableAddons':
    from resources.lib.modules import tools
    tools.ENABLE_ADDONS()

elif action == 'enableUnknownSources':
    from resources.lib.modules import tools
    tools.swapUS()

elif action == 'adv_settings':
    from resources.lib.modules import tools
    tools.advancedSettings()

elif action == 'clearAdv_settings':
    from resources.lib.modules import tools
    tools.clearAdvancedSettings()

elif action == 'changeLog':
    from resources.lib.modules import changelog
    changelog.get()

elif action == 'log_tools':
    from resources.lib.modules import logviewer
    logviewer.logView()

elif action == 'clear_ALL':
    from resources.lib.modules import maintenance
    maintenance.clearCache()
    maintenance.purgePackages()
    maintenance.deleteThumbnails()

elif action == 'clear_cache':
    from resources.lib.modules import maintenance
    maintenance.clearCache()

elif action == 'clear_packages':
    from resources.lib.modules import maintenance
    maintenance.purgePackages()

elif action == 'clear_thumbs':
    from resources.lib.modules import maintenance
    maintenance.deleteThumbnails()

elif action == 'clearEmptyFolders':
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (AddonTitle,  'Clearing Empty Folders...' , '5000', ADDON_ICON))
    REMOVE_EMPTY_FOLDERS()
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (AddonTitle,  'Done Clearing Empty Folders.' , '5000', ADDON_ICON))

elif action == 'reset_ResolversCache':
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (AddonTitle,  'Clearing Resolver Cache...' , '5000', ADDON_ICON))
    from resources.lib.modules import tools
    tools.resetResolversCache()

elif action == 'fresh_start':
    yesDialog = dialog.yesno(AddonTitle, 'Are you sure you want to perform a Fresh Start?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        dialog.ok(AddonTitle, 'Before Proceeding please switch skin to the default Kodi... Confluence or Estuary...','','')
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

