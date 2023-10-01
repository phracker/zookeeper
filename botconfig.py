#!/usr/bin/python
CONFIG_FILE="zookeeper.conf"

import time, shelve, os, sys, random, string, shutil

try:
    config = open(CONFIG_FILE).read().split("\n")
except IOError:
    cwd = raw_input("ZooKeeper has detected that you are running ZooKeeper from a nonstandard path!\nPlease enter the absolute path for the ZooKeeper directory (zookeeper/)\n(e.g. /home/user/zookeeper)\n>>> ")
    os.chdir(cwd)

conf = shelve.open(".config")
conf.clear()
conf.close()
    
def configure(rehash="NO"):
    config = open(CONFIG_FILE).read().split("\n")
    linenumber = 1
    defined = {}
    for line in config:
        if line == "":
            pass
        elif line[0] == "#":
            pass
        else:
            option = line.split()[0]
            if option == "BotNick":
                if "BotNick" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** BotNick already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
			if tmp == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option BotNick, using default (ZooKeeper) ***"
                            defined["BotNick"] = "ZooKeeper"
			else:
			    defined["BotNick"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option BotNick, using default (ZooKeeper) ***"
                        defined["BotNick"] = "ZooKeeper"
            elif option == "IRCServer":
                if "IRCServer" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** IRCServer already defined, using earlier definition ***"
                else:    
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
			if tmp == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option IRCServer, using default (localhost) ***"
                            defined["IRCServer"] = "localhost"
			else:
			    defined["IRCServer"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option IRCServer, using default (localhost) ***"
                        defined["IRCServer"] = "localhost"
            elif option == "IRCPort":
                if "IRCPort" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** IRCPort already defined, using earlier definition ***"
                else:
                    try:
                        IPort = line.split("=")[1].strip().split("##")[0].strip()
			if IPort == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option IRCPort, using default (6667) ***"
                            defined["IRCPort"] = "6667"
			else:
			    defined["IRCPort"] = IPort
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option IRCPort, using default (6667) ***"
                        defined["IRCPort"] = "6667"
	    elif option == "ListenerHost":
                if "ListenerHost" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** ListenerHost already defined, using earlier definition ***"
                else:    
                    try:
                        LHost = line.strip().split("=")[1].strip().split("##")[0].strip()
			if LHost == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option ListenerHost, using default (localhost) ***"
                            defined["ListenerHost"] = "localhost"
			else:
			    defined["ListenerHost"] = LHost
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option ListenerHost, using default (localhost) ***"
                        defined["ListenerHost"] = "localhost"
            elif option == "ListenerPort":
                if "ListenerPort" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** ListenerPort already defined, using earlier definition ***"
                else:
                    try:
                        LPort = line.strip().split("=")[1].strip().split("##")[0].strip()
			if LPort == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option ListenerPort, using default (31337) ***"
                            defined["ListenerPort"] = "31337"
			else:
			    defined["ListenerPort"] = LPort
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option ListenerPort, using default (31337) ***"
                        defined["ListenerPort"] = "31337"
            elif option == "BotNickservPass":
                if "BotNickservPass" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** BotNickservPass already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
			if tmp == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option BotNickservPass, using default (NONE) ***"
                            defined["BotNickservPass"] = "NONE"
			else:
			    defined["BotNickservPass"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option BotNickservPass, using default (NONE) ***"
                        defined["BotNickservPass"] = "NONE"
            elif option == "SiteTLD":
                if "SiteTLD" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** SiteTLD already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
			if tmp == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option SiteTLD, using default (yoursite.org) ***"
                            defined["SiteTLD"] = "yoursite.org"
			else:
			    defined["SiteTLD"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option SiteTLD, using default (yoursite.org) ***"
                        defined["SiteTLD"] = "yoursite.org"
            elif option == "SiteName":
                if "SiteName" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** SiteName already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
			if tmp == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option SiteName, using default (YourSite) ***"
                            defined["SiteName"] = "YourSite"
			else:
			    defined["SiteName"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option SiteName, using default (YourSite) ***"
                        defined["SiteName"] = "YourSite"
            elif option == "SSL_SiteURL":
                if "SSL_SiteURL" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** SSL_SiteURL already defined, using earlier definition ***"
                else:
                    try:
                        defined["SSL_SiteURL"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option SSL_SiteURL ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "NonSSL_SiteURL":
                if "NonSSL_SiteURL" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** NonSSL_SiteURL already defined, using earlier definition ***"
                else:
                    try:
                        defined["NonSSL_SiteURL"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option NonSSL_SiteURL ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "AdminChannel":
                if "AdminChannel" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** AdminChannel already defined, using earlier definition ***"
                else:
                    try:
                        defined["AdminChannel"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option AdminChannel ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "AdminChannelPass":
                if "AdminChannelPass" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** AdminChannelPass already defined, using earlier definition ***"
                else:
                    try:
                        defined["AdminChannelPass"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option AdminChannelPass, using default "" ***"
			defined["AdminChannelPass"] = ""
            elif option == "StaffChan":
                if "StaffChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** StaffChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["StaffChan"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option StaffChan ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
	    elif option == "UserWatchChan":
                if "UserWatchChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** UserWatchChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["UserWatchChan"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option UserWatchChan ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "OperUser":
                if "OperUser" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** OperUser already defined, using earlier definition ***"
                else:
                    try:
                        defined["OperUser"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option OperUser ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "OperPass":
                if "OperPass" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** OperPass already defined, using earlier definition ***"
                else:
                    try:
                        defined["OperPass"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option OperPass ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "sajoinCmd":
                if "sajoinCmd" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** sajoinCmd already defined, using earlier definition ***"
                else:
                    try:
                        defined["sajoinCmd"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option sajoinCmd, using default (SAJOIN) ***"
                        defined["sajoinCmd"] = "SAJOIN"
            elif option == "MySQL_host":
                if "MySQL_host" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MySQL_host already defined, using earlier definition ***"
                else:
                    try:
                        defined["MySQL_host"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MySQL_host ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "MySQL_port":
                if "MySQL_port" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MySQL_port already defined, using earlier definition ***"
                else:
                    try:
                        MPort = line.strip().split("=")[1].strip().split("##")[0].strip()
			if MPort == "":
			    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option MySQL_port, using default (3306) ***"
                            defined["MySQL_port"] = "3306"
			else:
			    defined["MySQL_port"] = MPort
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MySQL_port, using default (3306) ***"
                        defined["MySQL_port"] = "3306"
            elif option == "MySQL_passwd":
                if "MySQL_passwd" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MySQL_passwd already defined, using earlier definition ***"
                else:
                    try:
                        defined["MySQL_passwd"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MySQL_passwd ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "MySQL_user":
                if "MySQL_user" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MySQL_user already defined, using earlier definition ***"
                else:
                    try:
                        defined["MySQL_user"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MySQL_user ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "MySQL_db":
                if "MySQL_db" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MySQL_db already defined, using earlier definition ***"
                else:
                    try:
                        defined["MySQL_db"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MySQL_db ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "Staff":
                if "Staff" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** Staff already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
                        if tmp == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option Staff, using default "" ***"
                            defined["Staff"] = ""
                        else:
                            defined["Staff"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option Staff, using default "" ***"
                        defined["Staff"] = ""       
            elif option == "HighStaff":
                if "HighStaff" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** HighStaff already defined, using earlier definition ***"
                else:
                    try:
                        tmp = line.split("=")[1].strip().split("##")[0].strip()
                        if tmp == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** No arguments for option HighStaff, using default "" ***"
                            defined["HighStaff"] = ""
                        else:
                            defined["HighStaff"] = tmp
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option HighStaff ***"
                        print "*** No arguments for option HighStaff, using default "" ***"
                        defined["HighStaff"] = ""
            elif option == "MinStaffPermID":
                if "MinStaffPermID" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** MinStaffPermID already defined, using earlier definition ***"
                else:
                    try:
                        defined["MinStaffPermID"] = line.split("=")[1].strip().split("##")[0].strip()
                        if defined["Staff"] == "" and defined["MinStaffPermID"] == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Must have arguments for either Staff or MinStaffPermID!! ***"
                            return "Error"
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option MinStaffPermID, using default (0) ***"
                        if defined["Staff"] == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Must have arguments for either Staff or MinStaffPermID!! ***"
                            return "Error"
                        defined["MinStaffPermID"] = 0
            elif option == "HighStaffPermID":
                if "HighStaffPermID" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** HighStaffPermID already defined, using earlier definition ***"
                else:
                    try:
                        defined["HighStaffPermID"] = line.split("=")[1].strip().split("##")[0].strip()
                        if defined["HighStaff"] == "" and defined["HighStaffPermID"] == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Must have arguments for either HighStaff or HighStaffPermID!! ***"
                            return "Error"
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option HighStaffPermID, using default (0) ***"
                        if defined["Staff"] == "":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Must have arguments for either HighStaff or HighStaffPermID!! ***"
                            return "Error"
                        defined["HighStaffPermID"] = 0
	    elif option == "Voiced":
                if "Voiced" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** Voiced already defined, using earlier definition ***"
                else:
                    try:
                        defined["Voiced"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option Voiced, using default "" ***"
                        defined["Voiced"] = ""
	    elif option == "HalfOps":
                if "HalfOps" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** HalfOps already defined, using earlier definition ***"
                else:
                    try:
                        defined["HalfOps"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option HalfOps, using default "" ***"
                        defined["HalfOps"] = ""
	    elif option == "Opers":
                if "Opers" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** Opers already defined, using earlier definition ***"
                else:
                    try:
                        defined["Opers"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option Opers, using default "" ***"
                        defined["Opers"] = ""
            elif option == "Channels":
                if "Channels" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** Channels already defined, using earlier definition ***"
                else:
                    try:
                        defined["Channels"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option Channels ***"
                        if rehash == "NO":
                            print "*** FATAL: quitting ***"
                        return "Error"
            elif option == "AnnounceChan":
                if "AnnounceChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** AnnounceChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["AnnounceChan"] = line.split("=")[1].strip().split("##")[0].strip()
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option AnnounceChan, using default "" (NONE) ***"
                        defined["AnnounceChan"] = ""
            elif option == "DisabledChan":
                if "DisabledChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** DisabledChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["DisabledChan"] = line.split("=")[1].strip().split("##")[0].strip().strip("\"")
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option DisabledChan, using default "" (NONE) ***"
                        defined["DisabledChan"] = ""
            elif option == "InvitesChan":
                if "InvitesChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** InvitesChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["InvitesChan"] = line.split("=")[1].strip().split("##")[0].strip().strip("\"")
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option InvitesChan, using default "" (NONE) ***"
                        defined["InvitesChan"] = ""
            elif option == "HelpChan":
                if "HelpChan" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** HelpChan already defined, using earlier definition ***"
                else:
                    try:
                        defined["HelpChan"] = line.split("=")[1].strip().split("##")[0].strip().strip("\"")
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option HelpChan, using default "" (NONE) ***"
                        defined["HelpChan"] = ""

#### mod_Greeting ##############################################################################################
            elif option == "mod_Greeting":
                if "mod_Greeting" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** mod_Greeting already defined, using earlier definition ***"
                else:
                    try:
			mgreeting = line.split("=")[1].strip().split("##")[0].strip()
			if mgreeting.upper() != "TRUE" and mgreeting.upper() != "FALSE":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Invalid arguments for option mod_Greeting, using default (FALSE) ***"
                            print "*** Choices: TRUE, FALSE ***"
			    defined["mod_Greeting"] = "FALSE"
			else:
                            defined["mod_Greeting"] = mgreeting
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option mod_Greeting, using default (FALSE) ***"
			defined["mod_Greeting"] = "FALSE"

## mod_StaffAssistAlerts ######################################################################################
            elif option == "mod_StaffAssistAlerts":
                if "mod_StaffAssistAlerts" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** mod_StaffAssistAlerts already defined, using earlier definition ***"
                else:
                    try:
			StaffAssistAlerts = line.split("=")[1].strip().split("##")[0].strip()
			if StaffAssistAlerts.upper() != "TRUE" and StaffAssistAlerts.upper() != "FALSE":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Invalid arguments for option mod_StaffAssistAlerts, using default (FALSE) ***"
                            print "*** Choices: TRUE, FALSE ***"
			    defined["mod_StaffAssistAlerts"] = "FALSE"
			else:
                            defined["mod_StaffAssistAlerts"] = StaffAssistAlerts
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option mod_StaffAssistAlerts, using default (FALSE) ***"
			defined["mod_StaffAssistAlerts"] = "FALSE"
            elif option == "mod_SAA_AlertLevel":
                if "mod_SAA_AlertLevel" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** mod_SAA_AlertLevel already defined, using earlier definition ***"
                else:
                    try:
			SAA_AlertLevel = line.split("=")[1].strip().split("##")[0].strip()
			if SAA_AlertLevel != "1" and SAA_AlertLevel != "2":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Invalid arguments for option mod_SAA_AlertLevel, using default (1) ***"
                            print "*** Choices: 1, 2 ***"
			    defined["mod_SAA_AlertLevel"] = "1"
			else:
                            defined["mod_SAA_AlertLevel"] = SAA_AlertLevel
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option mod_SAA_AlertLevel, using default (1) ***"
			defined["mod_SAA_AlertLevel"] = "1"

#### mod_OnIRC #########################################################################################
            elif option == "mod_OnIRC":
                if "mod_OnIRC" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** mod_OnIRC already defined, using earlier definition ***"
                else:
                    try:
			monirc = line.split("=")[1].strip().split("##")[0].strip()
			if monirc.upper() != "TRUE" and monirc.upper() != "FALSE":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Invalid arguments for option mod_OnIRC, using default (FALSE) ***"
                            print "*** Choices: TRUE, FALSE ***"
			    defined["mod_OnIRC"] = "FALSE"
			else:
                            defined["mod_OnIRC"] = monirc
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option mod_OnIRC, using default (FALSE) ***"
			defined["mod_OnIRC"] = "FALSE"

#### mod_IRCPrivs #######################################################################################
            elif option == "mod_IRCPrivs":
                if "mod_IRCPrivs" in defined:
                    print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                    print "*** mod_IRCPrivs already defined, using earlier definition ***"
                else:
                    try:
			mircprivs = line.split("=")[1].strip().split("##")[0].strip()
			if mircprivs.upper() != "TRUE" and mircprivs.upper() != "FALSE":
                            print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                            print "*** Invalid arguments for option mod_IRCPrivs, using default (FALSE) ***"
                            print "*** Choices: TRUE, FALSE ***"
			    defined["mod_IRCPrivs"] = "FALSE"
			else:
                            defined["mod_IRCPrivs"] = mircprivs
                    except IndexError:
                        print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                        print "*** No arguments for option mod_IRCPrivs, using default (FALSE) ***"
			defined["mod_IRCPrivs"] = "FALSE"
            else:
                print "*** CONFIG PARSE ERROR ON LINE " + str(linenumber) + " ***"
                print "*** Unknown option: " + option + " ***"
                print "*** Ignoring ***"
        linenumber += 1
            
    if "BotNick" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No BotNick defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "IRCServer" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No IRCServer defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "IRCPort" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No IRCPort defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "ListenerHost" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No ListenerHost defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "ListenerPort" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No ListenerPort defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "AdminChannel" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No AdminChannel defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "AdminChannelPass" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No AdminChannelPass defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "StaffChan" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No StaffChan defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "Channels" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No Channels defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "AnnounceChan" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No AnnounceChan defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "DisabledChan" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No DisabledChan defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "InvitesChan" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No InvitesChan defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "HelpChan" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No HelpChan defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "Staff" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No Staff defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "HighStaff" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No HighStaff defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "MinStaffPermID" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No MinStaffPermID defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "HighStaffPermID" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No HighStaffPermID defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "Voiced" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No Voiced defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "HalfOps" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No Voiced defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "Opers" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No Opers defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "BotNickservPass" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No BotNickservPass defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "sajoinCmd" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No sajoinCmd defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "OperUser" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No OperUser defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "OperPass" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No OperPass defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "SiteName" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No SiteName defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "SiteTLD" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No SiteTLD defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "SSL_SiteURL" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No SiteName defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "NonSSL_SiteURL" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No NonSSL_SiteURL defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "MySQL_host" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No MySQL_host defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "MySQL_user" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No MySQL_user defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "MySQL_passwd" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No MySQL_passwd defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "MySQL_db" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No MySQL_db defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "mod_Greeting" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No mod_Greeting defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "mod_StaffAssistAlerts" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No mod_StaffAssistAlerts defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "mod_SAA_AlertLevel" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No mod_SAA_AlertLevel defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "mod_OnIRC" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No mod_OnIRC defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"
    if "mod_IRCPrivs" not in defined.keys():
        print "*** CONFIG PARSE ERROR ***"
        print "*** No mod_IRCPrivs defined ***"
        if rehash == "NO":
            print "*** FATAL: quitting ***"
        return "Error"

    return defined
