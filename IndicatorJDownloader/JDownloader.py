#!/usr/bin/python -tt
'''
Created on 10.02.2014

@author: Dirk Rother
@contact: dirrot@web.de
@license: GPL
@version: 0.1

'''

import gobject
import gtk
import appindicator
import os, sys
import JDRemote

HOST = "192.168.1.105"
PORT = "10025"    
VNC_VIEWER = "xvnc4viewer"
VNC_CMD = VNC_VIEWER + " " + HOST

def quitApplication(widget, optionName):
    sys.exit(0)
                                        
def startDownload(widget, optionName, indicator):
    JDRemote.action_start(HOST, PORT)
    redraw_ui(indicator)
            
def stopDownload(widget, optionName, indicator):
    JDRemote.action_stop(HOST, PORT)
    redraw_ui(indicator)

def downloadFilesInQueue():
    count = JDRemote.get_downloads_all_count(HOST, PORT)
    return count

def allDownloadsInQueue():
    downloadList = JDRemote.get_downloads_all_list(HOST, PORT) 
    return downloadList   

def openVNCClient(widget, optionName):
    os.system(VNC_CMD)

def redraw_ui(indicator):

    # create a menu
    menu = gtk.Menu()
    
    isServerOnline = True
    try:
        JDRemote.is_running(HOST, PORT)
    except IOError:
        isServerOnline = False   
    
    # server status menu item
    menuitem = gtk.MenuItem("Server:\t\toffline")
    if isServerOnline:
        if JDRemote.is_running(HOST, PORT):
            menuitem = gtk.MenuItem("Server:\t\tonline")
    menuitem.show()
    menu.append(menuitem)

    # download status menu item
    menuitem_server = gtk.MenuItem("Download:\tnot running")
    if isServerOnline:
        if JDRemote.get_downloadstatus(HOST, PORT) == "RUNNING":
            menuitem_server = gtk.MenuItem("Download:\trunning")
        
    # submenu for server start and stop
    submenu = gtk.Menu()
    download_start_item = gtk.MenuItem("Start")
    download_start_item.connect("activate", startDownload, "Start", ind)
    download_start_item.show()
    submenu.append(download_start_item)
    download_stop_item = gtk.MenuItem("Stop")
    download_stop_item.connect("activate", stopDownload, "Stop", ind)
    download_stop_item.show()
    submenu.append(download_stop_item)
    if isServerOnline:
        if JDRemote.get_downloadstatus(HOST, PORT) == "RUNNING":
            download_start_item.set_sensitive(False)
            download_stop_item.set_sensitive(True)
        else:
            download_start_item.set_sensitive(True)
            download_stop_item.set_sensitive(False)
    else:
        download_start_item.set_sensitive(False)
        download_stop_item.set_sensitive(False)            
    menuitem_server.set_submenu(submenu)
    menuitem_server.show()
    menu.append(menuitem_server)    
    
    # seperator
    separator = gtk.SeparatorMenuItem();
    separator.show()
    menu.append(separator)     

    # all packages in queue
    menuitem = gtk.MenuItem("VNC -> JDownloader")
    menuitem.set_sensitive(False)
    menuitem.connect("activate", openVNCClient, "VNC -> JDownloader")
    if isServerOnline:
        menuitem.set_sensitive(True)
    menuitem.show()
    menu.append(menuitem)
    
    # seperator
    separator = gtk.SeparatorMenuItem();
    separator.show()
    menu.append(separator)  
    
    # all packages in queue
    menuitem = gtk.MenuItem("All packages:\t0")
    if isServerOnline:
        count = downloadFilesInQueue()
        menuitem = gtk.MenuItem("All packages:\t" + str(count))
    menuitem.show()
    menu.append(menuitem)       
    
    # all downloads in queue
    if isServerOnline:
        downloadList = allDownloadsInQueue()
        
        for download in downloadList:
            doneFiles = 0
            for fileitem in download["files"]:
                if fileitem["percent"] == "100.00":
                    doneFiles = doneFiles + 1
                
            strDoneFiles = ""
            if doneFiles <= 9:
                strDoneFiles = "0" + str(doneFiles)
            else:
                strDoneFiles = str(doneFiles)
                
            allFiles = len(download["files"])
            strAllFiles = ""
            if allFiles <= 9:
                strAllFiles = "0" + str(allFiles)
            else:
                strAllFiles = str(allFiles)            
            
            menuitem = gtk.MenuItem(download["percent"] + "%\t" 
		+ download["speed"] + "/s\t" 
                + "[" + strDoneFiles + "/" + strAllFiles + "]\t" 
                + download["name"] + "\t" 
		+ download["ETA"])
            menuitem.show()
            menu.append(menuitem)                   
    
    # seperator
    separator = gtk.SeparatorMenuItem();
    separator.show()
    menu.append(separator)        
    
    # quit menu item
    menuitem = gtk.MenuItem("Exit")
    menuitem.connect("activate", quitApplication, "Exit")
    menuitem.show()
    menu.append(menuitem)
    
    # add menu to IndicatorJDownloader
    ind.set_menu(menu)     

    return True

if __name__ == "__main__":  

    icon = '/usr/local/share/IndicatorJDownloader/icons/jd_ubuntu.png'

    ind = appindicator.Indicator(
            "IndicatorJDownloader",
            icon,
            appindicator.CATEGORY_APPLICATION_STATUS)
    
    ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_attention_icon(icon)
    
    # start draw
    redraw_ui(ind)
    # every 5 sec draw
    gobject.timeout_add(5000, redraw_ui, ind)
    gtk.main()
    
     
   
    
    
       
        
        
                     

                
