#Created on 28.10.2012
#
#@author: reecon
#@version: 0.1.0

import urllib
import logging
import xml.dom.minidom as dom

## Check if JD is running with the given credentials.
#@param jdbaseaddress: 
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return True if a connection to JD could be established.
def is_running(jdbaseaddress='localhost', port=10025):
    jdcommand = "http://{}:{}/help".format(jdbaseaddress, port)
    isrunning = True
    try:
        urllib.urlopen(jdcommand)
    except IOError:
        isrunning = False
    return isrunning
    
## Get current speed.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Current speed as int in KB/s. (int)
#@throws IOError: If the connection to the given address could not be established.
def get_speed(jdbaseaddress="localhost", port=10025):
    jdcommand = "http://{}:{}/get/speed".format(jdbaseaddress, port)
    response = urllib.urlopen(jdcommand)
    return int(response.readline())
    
    
## Get current IP.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: current IP as string.
#@throws IOError: If the connection to the given address could not be established.
def get_ip(jdbaseaddress="localhost", port=10025):
    jdcommand = "http://{}:{}/get/ip".format(jdbaseaddress, port)
    response = urllib.urlopen(jdcommand)
    return response.readline()
    
## Awnswers with random IP as replacement for real IP-Check.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: random IP as string
#@throws IOError: If the connection to the given address could not be established.
def get_random_ip(jdbaseaddress="localhost", port=10025):
    jdcommand = "http://{}:{}/get/randomip".format(jdbaseaddress, port)
    response = urllib.urlopen(jdcommand)
    return response.readline()

## Get current config.
#
# Gives you a map of config-keywords with their values. <br>
# Where the values are converted into their respective Python-types when possible. <br>
# i.e. 'true' => True or 'null' => None or "3.14" => float and so on. <br>
# Empty values are returned as None-types as well.
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Map of current configuration keys and values.
#@throws IOError: If the connection to the given address could not be established.
def get_config(jdbaseaddress="localhost", port=10025):
    config={}
    jdcommand = "http://{}:{}/get/config".format(jdbaseaddress, port)
    response = urllib.urlopen(jdcommand)
    
    for line in response:
        line = line.strip()
        words = line.split(" ")
        key = words[0]
        
        # ignore <pre> formating
        if key.startswith("<pre>"):
            key = key[5:]   
        if key.startswith("</pre>"):
            break
        
        value = None # first look if there is a value
        if len(words) > 2:
            value = words[2]
            if value == "true":
                value = True
            elif value == "false":
                value = False
            elif value == "null":
                value = None
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass
        config[key] = value
        
    return config

## Get version.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: JD Version.
#@throws IOError: If the connection to the given address could not be established.
def get_version(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/version".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return response.readline()

## Get RemoteControl version.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Current version of RemoteControl as string
#@throws IOError: If the connection to the given address could not be established.
def get_rcversion(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/rcversion".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return response.readline()

## Get the current speedlimit.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: The current speedlimit as int in KB/s. (int)
#@throws IOError: If the connection to the given address could not be established.
def get_speedlimit(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/speedlimit".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return int(response.readline())

## Get if reconnect.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: True if reconnecting.
#@throws IOError: If the connection to the given address could not be established.
def get_isreconnect(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/isreconnect".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    reconnect = response.readline()
    if reconnect == 'true':
        reconnect = True
    else:
        reconnect = False
    return reconnect

## Get download status.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: 'RUNNING' | 'NOT_RUNNING' | 'STOPPING'
#@throws IOError: If the connection to the given address could not be established.
def get_downloadstatus(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloadstatus".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return response.readline()

## Get amount of current downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Amount of current downloads. (int)
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_current_count(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/currentcount".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return int(response.readline())

## Get current downloads in list.
#
# Returns a list with one dictionary for each package. The package-dictionary
# contains a list with a dictionary for each file in the package as well as
# an entry for each attribute given by JD. Each file-dictionary contains the
# attributes given by JD for each file. 
#
# @image html dllist.png
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: List of all active downloads.
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_current_list(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/currentlist".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    document = dom.parse(response)
    result = []
    root = document.documentElement
    packages = root.getElementsByTagName("package")
    for package in packages:
        pckg = {}
        pckg["ETA"] = package.getAttribute("package_ETA")
        pckg["linksinprogress"] = package.getAttribute("package_linksinprogress")
        pckg["linkstotal"] = package.getAttribute("package_linkstotal")
        pckg["loaded"] = package.getAttribute("package_loaded")
        pckg["name"] = package.getAttribute("package_name")
        pckg["percent"] = package.getAttribute("package_percent")
        pckg["size"] = package.getAttribute("package_size")
        pckg["speed"] = package.getAttribute("package_speed")
        pckg["todo"] = package.getAttribute("package_todo")
        
        files = package.getElementsByTagName("file")
        fls = []
        
        for file_ in files:
            f = {}
            f["hoster"] = file_.getAttribute("file_hoster")
            f["name"] = file_.getAttribute("file_name")
            f["package"] = file_.getAttribute("file_package")
            f["percent"] = file_.getAttribute("file_percent")
            f["speed"] = file_.getAttribute("file_speed")
            f["status"] = file_.getAttribute("file_status")
            fls.append(f)
        
        pckg["files"] = fls
        
        result.append(pckg)
        
    return result

## Get amount of all downloads in list.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Amount of downloads in list.
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_all_count(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/allcount".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return int(response.readline())

## Get list of all downloads in list.
#
# Returns a list with one dictionary for each package. The package-dictionary
# contains a list with a dictionary for each file in the package as well as
# an entry for each attribute given by JD. Each file-dictionary contains the
# attributes given by JD for each file. 
#
# @image html dllist.png
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: List of all downloads.
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_all_list(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/alllist".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    document = dom.parse(response)
    result = []
    root = document.documentElement
    packages = root.getElementsByTagName("package")
    for package in packages:
        pckg = {}
        pckg["ETA"] = package.getAttribute("package_ETA")
        pckg["linksinprogress"] = package.getAttribute("package_linksinprogress")
        pckg["linkstotal"] = package.getAttribute("package_linkstotal")
        pckg["loaded"] = package.getAttribute("package_loaded")
        pckg["name"] = package.getAttribute("package_name")
        pckg["percent"] = package.getAttribute("package_percent")
        pckg["size"] = package.getAttribute("package_size")
        pckg["speed"] = package.getAttribute("package_speed")
        pckg["todo"] = package.getAttribute("package_todo")
        
        files = package.getElementsByTagName("file")
        fls = []
        
        for file_ in files:
            f = {}
            f["hoster"] = file_.getAttribute("file_hoster")
            f["name"] = file_.getAttribute("file_name")
            f["package"] = file_.getAttribute("file_package")
            f["percent"] = file_.getAttribute("file_percent")
            f["speed"] = file_.getAttribute("file_speed")
            f["status"] = file_.getAttribute("file_status")
            fls.append(f)
        
        pckg["files"] = fls
        
        result.append(pckg)
        
    return result

## Get amount of finished downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: Amount of finished downloads.
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_finished_count(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/finishedcount".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    return int(response.readline())

## Get finished downloads list.
#
# Returns a list with one dictionary for each package. The package-dictionary
# contains a list with a dictionary for each file in the package as well as
# an entry for each attribute given by JD. Each file-dictionary contains the
# attributes given by JD for each file. 
#
# @image html dllist.png
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@return: List of finisched downloads.
#@throws IOError: If the connection to the given address could not be established.
def get_downloads_finished_list(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/get/downloads/finishedlist".format(jdbaseaddress, port)
    response = urllib.urlopen(command)
    document = dom.parse(response)
    result = []
    root = document.documentElement
    packages = root.getElementsByTagName("package")
    for package in packages:
        pckg = {}
        pckg["ETA"] = package.getAttribute("package_ETA")
        pckg["linksinprogress"] = package.getAttribute("package_linksinprogress")
        pckg["linkstotal"] = package.getAttribute("package_linkstotal")
        pckg["loaded"] = package.getAttribute("package_loaded")
        pckg["name"] = package.getAttribute("package_name")
        pckg["percent"] = package.getAttribute("package_percent")
        pckg["size"] = package.getAttribute("package_size")
        pckg["speed"] = package.getAttribute("package_speed")
        pckg["todo"] = package.getAttribute("package_todo")
        
        files = package.getElementsByTagName("file")
        fls = []
        
        for file_ in files:
            f = {}
            f["hoster"] = file_.getAttribute("file_hoster")
            f["name"] = file_.getAttribute("file_name")
            f["package"] = file_.getAttribute("file_package")
            f["percent"] = file_.getAttribute("file_percent")
            f["speed"] = file_.getAttribute("file_speed")
            f["status"] = file_.getAttribute("file_status")
            fls.append(f)
        
        pckg["files"] = fls
        
        result.append(pckg)
        
    return result

## Start downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_start(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/start".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Pauses/Unpauses downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_pause(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/pause".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Stop downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_stop(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/stop".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Toggle downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_toggle(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/toggle".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Do Webupdate.
#
# If force is set to True activates auto-restart if update is possible
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param force: If Ture do auto-restart if update is possible.
#@throws IOError: If the connection to the given address could not be established.
def action_update(force=True, jdbaseaddress="localhost", port=10025):
    f = 1
    if not force:
        f = 0
    command = "http://{}:{}/action/update/force{}".format(jdbaseaddress, port,f)
    urllib.urlopen(command)

## Do a reconnect.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_reconnect(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/reconnect".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Restart JDownloader.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_restart(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/restart".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Shutdown JDownloader.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@throws IOError: If the connection to the given address could not be established.
def action_shutdown(jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/shutdown".format(jdbaseaddress, port)
    urllib.urlopen(command)

## Set download-speedlimit.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param limit: The desired speedlimit in KB/s.
#@return: The new limit returned by JD. (int)
#@throws IOError: If the connection to the given address could not be established.
def action_set_download_limit(limit, jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/set/download/limit/{}".format(jdbaseaddress, port, limit)
    response = urllib.urlopen(command)
    newlimit = response.readline().strip().split("=")[1]
    return newlimit

## Set max simultaneous downloads.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param maximum: Maximum simultaneous downloads.
#@throws IOError: If the connection to the given address could not be established.
def action_set_download_max(maximum, jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/set/download/max/{}".format(jdbaseaddress, port, maximum)
    response = urllib.urlopen(command)
    newmax = response.readline().strip().split("=")[1]
    return newmax

## Adds links to the grabber.
#
# Adds links to the grabber and starts them immediately if you want.
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param links: List of links which are to be added to the grabber.
#@param grabber: Only add links to the linkgrabber.
#@param start: Start downloads immediately after adding.
#@return: JD-confirmed list of added links.
#@throws IOError: If the connection to the given address could not be established.
def action_add_links(links, grabber=False, start=True, jdbaseaddress="localhost", port=10025):
    gr = 0
    if grabber:
        gr = 1
    st = 1
    if not start:
        st = 0
    command = "http://{}:{}/action/add/links/grabber{}/start{}/".format(jdbaseaddress, port, gr, st)
    for link in links:
        command = "{}{} ".format(command, link)
    urllib.urlopen(command)
    logging.debug("Sent command to JD: '{}'".format(command))
    if start:
        action_start(jdbaseaddress, port)  # just to be sure
    
## Adds a container to the grabber.
#
# Adds a container-file at the specified path to the grabber.
#@bug: Bug in plugin for JD 0.9.xxx - Doesn't do anything.<br>
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param container: Path to the containerfile.
#@param grabber: If True shows the linkgrabber.
#@param start: If True starts downloads immediately.
#@throws IOError: If the connection to the given address could not be established.
def action_add_container(container, grabber=False, start=True, jdbaseaddress="localhost", port=10025):
    pass

## Save DLC-Container.
#
# Save a DLC-Container with all links to the specified Path.
#
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param container: Path and Containername including file-ending. Path only inside JD-Installfolder.
#@throws IOError: If the connection to the given address could not be established.
def action_save_container(container, jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/save/container/{}".format(jdbaseaddress, port, container)
    urllib.urlopen(command)
    
## Enables/Disabes reconnect.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param enable: If True reconnect will be enabled.
#@return: Tuple of Bools (new_status, has_changed).
#@throws IOError: If the connection to the given address could not be established.
def action_set_reconnect_enabled(enable, jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/set/reconnectenabled/{}".format(jdbaseaddress, port, enable)
    response = urllib.urlopen(command)
    result = response.readline().strip().split(" ")
    current = enable
    changed = False
    if result[0].split("=")[1] == "true":
        current = True
    else:
        current = False
    if result[1].split("=")[1] == "true":
        changed = True
    else:
        changed = False
    return (current, changed)
    
## Enables/Disables use of premium accounts.
#@param jdbaseaddress: IP, hostname or domainname of the JD-host.
#@param port: Port specified for JD-RemoteControll plugin.
#@param enable: If True premium accounts will be enabled.
#@return: Tuple of Bools (new_status, has_changed).
#@throws IOError: If the connection to the given address could not be established.
def action_set_premium_enabled(enable, jdbaseaddress="localhost", port=10025):
    command = "http://{}:{}/action/set/premiumenabled/{}".format(jdbaseaddress, port, enable)
    response = urllib.urlopen(command)
    result = response.readline().strip().split(" ")
    current = enable
    changed = False
    if result[0].split("=")[1] == "true":
        current = True
    else:
        current = False
    if result[1].split("=")[1] == "true":
        changed = True
    else:
        changed = False
    return (current, changed)
