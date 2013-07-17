#!/usr/bin/python
VERSION="1.97"

import time, shelve, os, sys, random, string, MySQLdb, threading, socket, shutil
import ircbot, irclib, botconfig, updater, hashlib

print "\n*********************************************************************"
print "** ZooKeeper " + VERSION + " - Gazelle Server IRC Bot"
print "** http://tbsf.me/zookeeper - Written By: eXploytIT - April 2011" 
print "*********************************************************************"
print "** Options: --noupdate || -n : Don't check for updates"
print "*********************************************************************\n"

## Check for updates
if "--noupdate" not in sys.argv and "-n" not in sys.argv:
    updater.update(VERSION)

## Validate config file
config_response = botconfig.configure()
if config_response != "Error":
    print "*** Config read OK ***"
    conf = shelve.open(".config")
    for i,v in config_response.iteritems():
        conf[i] = v
    conf.close()
else:
    sys.exit()

## Make the config dictionary
config = shelve.open(".config")

###############################################################################################
###############################################################################################
## Bot settings variables

Channels = config["Channels"].split(",")
AnnounceChans = config["AnnounceChan"].split(",")
MySQL_host = config["MySQL_host"]
MySQL_user = config["MySQL_user"]
MySQL_passwd = config["MySQL_passwd"]
MySQL_db = config["MySQL_db"]
ListenerHost = config["ListenerHost"]
ListenerPort = int(config["ListenerPort"])
Name = "ZooKeeper"

# dict of privlege levels and their associated commands. 
# i.e. if priv level is '3', the 'op' command will be used to promote the target user
IRCPrivCmds = {'0':'none','1':'voice','2':'halfop','3':'op'} 
AssistCount = {}
FirstAssistReq = {}

###############################################################################################
###############################################################################################
## Classes

## Listener Thread
class Listener(threading.Thread):
    def __init__(self):
        self.running = True
	self.connection = False
        threading.Thread.__init__(self)
 
    def stop(self):
        self.running = False
	## The following is a HACK to make the thread stop when it is told to
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((ListenerHost, ListenerPort))
	client_socket.send("QUITTING")
	client_socket.close()

    def setConnection(self, con):
	self.connection = con
 
    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server_socket.bind((ListenerHost, ListenerPort))
    	server_socket.listen(5)
    	print "-> Listener waiting for connection on port " + str(ListenerPort)

    	while self.running:
	    client_socket, address = server_socket.accept()
            data = client_socket.recv(512).strip()
	    print "-> Listener Recieved:" , data
	    client_socket.close()
	    try:
	    	self.connection.send_raw(data)
	    except socket.error, e:
		print "*** Socket Error: %d: %s ***" % (e.args[0], e.args[1])

	server_socket.close()

## MySQL Class
class mysql:
    def __init__(self):
	self.running = True;
	try:
    	    self.sql = MySQLdb.connect(host = MySQL_host, user = MySQL_user, passwd = MySQL_passwd, db = MySQL_db, reconnect = 1)
	except MySQLdb.Error, e:
	    self.running = True;
    	    print "*** MySQL Error %d: %s ***" % (e.args[0], e.args[1])
    	    print "*** FATAL: quitting ***"
    	    sys.exit(1)
    
    def execute(self, query):
	self.cursor = self.sql.cursor()
	self.cursor.execute(query)
	self.open = True
	
    def rowcount(self):
	if self.open:
	    return self.cursor.rowcount
	else:
	    print "*** rowcount: No DB cursor is open! ***"
	    return 0

    def fetchone(self):
	if self.open:
	    return self.cursor.fetchone()
	else:
	    print "*** fetchone: No DB cursor is open! ***"
	    return 0

    def fetchall(self):
	if self.open:
	    return self.cursor.fetchall()
	else:
	    print "*** fetchall: No DB cursor is open! ***"
	    return 0

    def closecursor(self):
	if self.open:
	    self.sql.commit()
	    return self.cursor.close()
	else:
	    print "*** close: No DB cursor is open! ***"
	    return 0

    def close(self):
	if self.open:
	    self.sql.commit()
	    return self.cursor.close()
	else:
	    print "*** close: No DB cursor is open! ***"
	    return 0

###############################################################################################
###############################################################################################
## Functions

def dbVal(s): # Protect against MySQL injection attacks
    s = ''.join([ c for c in s if c not in ('\'','\x1a','\r','\n','\"','\x00', '\\')])
    return s

def IsStaff(user): # Is the given username a staff member?
    if conf["MinStaffPermID"] == "0":
        Staff = str(config["Staff"] + "," + config["HighStaff"]).split(",")
    else:
        Staff = GetAllStaff()   
    if user in Staff:
	return True
    else:
	return False

def IsHighStaff(user): # Is the given username a high-level staff member?
    if conf["HighStaffPermID"] == "0":
        HighStaff = config["HighStaff"].split(",")
    else:
        HighStaff = GetHighStaff()        
    if user in HighStaff:
	return True
    else:
	return False

def GetAllStaff():
    s = []
    if conf["MinStaffPermID"] == "0":
	print "-> MinStaffPermID NOT SET!"
	AllStaff = conf["Staff"] + "," + conf["HighStaff"]
	return AllStaff.split(",")
    else:
	SQL= mysql()
	SQL.execute("SELECT Username FROM users_main JOIN permissions AS p ON p.ID=PermissionID WHERE p.Level>='" + conf["MinStaffPermID"] + "'")
	t = SQL.fetchall()
	SQL.close()
	for user in t:
	    s.append(user[0])
	return s

def GetHighStaff():
    u = []
    if conf["HighStaffPermID"] == "0":
	print "-> HighStaffPermID NOT SET!"
	return conf["HighStaff"].split(",")
    else:
	SQL= mysql()
	SQL.execute("SELECT Username FROM users_main JOIN permissions AS p ON p.ID=PermissionID WHERE p.Level>='" + conf["HighStaffPermID"] + "'")
	r = SQL.fetchall()
	SQL.close()
	for user in r:
	    u.append(user[0])
	return u

def getUserID(user): # Get a UserID from the Gazelle database
    SQL = mysql()
    SQL.execute("SELECT ID FROM users_main WHERE Username='" + dbVal(user) + "'")
    rows = SQL.rowcount()
    if rows < 1:
        SQL.close()
        return "0"
    else:
	row = SQL.fetchone()
        SQL.close()
        return str(row[0])

def ValidateUser(user, irckey):
    SQL = mysql()
    SQL.execute("SELECT IRCKey, Enabled FROM users_main WHERE Username='" + dbVal(user) + "'")
    rows = SQL.rowcount()
    if rows == 0:
        SQL.close()
	return "USER_NOT_FOUND"
    row = SQL.fetchone()
    SQL.close()
    if row[1] != "1":
	return "DISABLED"
    elif row[0] == irckey:
	return "MATCH"
    elif row[0] == "":
	return "KEY_NOT_SET"
    else:
	return "NO_MATCH"

def getUserHost(user): # Make a hostname for the specified user with values from the Gazelle database
    SQL = mysql()
    SQL.execute("SELECT ID, PermissionID FROM users_main WHERE Username='" + dbVal(user) + "'")
    rows = SQL.rowcount()
    if rows == 0:
        SQL.close()
        return user + ".unknown." + conf["SiteTLD"]
    else:
	row = SQL.fetchone()
	userid = str(row[0])
	permid = str(row[1])
	SQL.execute("SELECT Name FROM permissions WHERE ID='" + permid + "'")
	row2 = SQL.fetchone()
	SQL.close()
	cls = row2[0].lower()
	cls = ''.join([c for c in cls if c not in (' ')])
        return user + "." + cls + "." + conf["SiteTLD"]

def getUserInfo(user): # Get user info from the Gazelle database
    show_forumposts=True
    SQL = mysql()
    SQL.execute("SELECT um.ID, um.PermissionID, um.Title, ui.Donor, um.Uploaded, um.Downloaded, COUNT(fp.ID) FROM users_main AS um JOIN users_info AS ui ON ui.UserID=um.ID JOIN forums_posts AS fp ON fp.AuthorID=um.ID WHERE um.Username='" + dbVal(user) + "'")
    rows = SQL.rowcount()
    if rows == 0:
        SQL.close()
	return "Username not found!"
    else:
	row = SQL.fetchone()
	permid = str(row[1])
	SQL.execute("SELECT Name FROM permissions WHERE ID='" + permid + "'")
	row2 = SQL.fetchone()
        SQL.close()
	uploadnum = float(float(row[4])/1073741824)
	downloadnum = float(float(row[5])/1073741824)
	forumposts = str(row[6])
	if downloadnum > 0.05:
	     ratio = str(uploadnum/downloadnum).split(".")[0] + "." + str(uploadnum/downloadnum).split(".")[1][:2]
	else:
	     ratio = "Infinite"
	upload = str(uploadnum).split(".")[0] + "." + str(uploadnum).split(".")[1][:2]
	download = str(downloadnum).split(".")[0] + "." + str(downloadnum).split(".")[1][:2]
	out = "User: " + user
	if str(row[3]) == "1": 
	    out = out + " <3"
	out = out + " \002::\002 " + str(row2[0]) + " \002::\002"
	out = out + " \002UP:\002 " + upload + "Gb | \002DOWN:\002 " + download + "Gb | \002RATIO:\002 " + ratio
	if show_forumposts:
	    out = out + " | \002Forum Posts:\002 " + forumposts
	out = out + " \002::\002 " + conf["NonSSL_SiteURL"] + "/user.php?id=" + str(row[0])
	out = out + " || " + conf["SSL_SiteURL"] + "/user.php?id=" + str(row[0])
        return out
    SQL.close()
    return "SUCCESS"

def getBonusPoints(user):
    SQL = mysql()
    SQL.execute("SELECT (seed+irc) AS Points FROM users_bonuses WHERE userid='" + str(getUserID(user)) + "'")
    rows = SQL.rowcount()
    if rows == 0:
        SQL.close()
	return "Username not found!"
    row = SQL.fetchone()
    SQL.close()
    return str(row[0])

def checkSiteURL(url):
    out=""
    if url.count(conf["SSL_SiteURL"]) > 0:
    	print "-> Parse site URLs in message and give alternatives -- Found: HTTPS"
	urlarray = url.split();
	for item in urlarray:
	    if item.count(conf["SSL_SiteURL"]) > 0:
		out=out + string.replace(item, conf["SSL_SiteURL"], conf["NonSSL_SiteURL"]) + " "
	out="Alternate Site URL (Non-SSL): " + out.strip()
    elif url.count(conf["NonSSL_SiteURL"]) > 0:
    	print "-> Parse site URLs in message and give alternatives -- Found: HTTP"
	urlarray = url.split();
	for item in urlarray:
	    if item.count(conf["NonSSL_SiteURL"]) > 0:
		out=out + string.replace(item, conf["NonSSL_SiteURL"], conf["SSL_SiteURL"]) + " "
	out="Alternate Site URL (SSL): " + out.strip()
    else:
	return "NONE"
    return out

##
## Admin Tools and stuff
##

def EnableUser(user): # Enable a user on the Gazelle site
    userid = getUserID(user)
    if userid == "0":
        return "XUSER"
    SQL = mysql()
    SQL.execute("SELECT Enabled FROM users_main WHERE ID=" + userid)
    row = SQL.fetchone()
    if row[0] == "1":
	SQL.close()
	return "ISENABLED"
    SQL.execute("UPDATE users_main SET Enabled='1' WHERE ID=" + userid)
    SQL.close()
    return "SUCCESS"

##
## Modules
##
def getIRCPrivs(user): # Get a UserID from the Gazelle database
    if config["mod_IRCPrivs"].upper() != "TRUE":
	priv = "0"
        if user in config['Opers']:
            priv = "3"
        if user in config['HalfOps']:
            priv = "2"
        if user in config['Voiced']:
            priv = "1"
	print "-> The [zookeeper.conf] IRC privlege for " + user + " is " + priv
	return priv
    else:
        SQL = mysql()
        SQL.execute("SELECT IRCPrivs FROM users_info WHERE UserID='" + dbVal(getUserID(user)) + "'")
        if SQL.rowcount() < 1:
            SQL.close()
            return "0"
        else:
            row = SQL.fetchone()
            SQL.close()
            ircprivs = str(row[0])
	    print "-> The [MySQL users_info] IRC privlege for " + user + " is " + IRCPrivCmds[str(ircprivs)]
            return ircprivs

def getGreeting(userid): # mod_Greeting: Fetch a users IRCGreeting from the Gazelle database
    if conf["mod_Greeting"].upper() != "TRUE":
	return "DISABLED"
    try:
	dummy = int(userid)
    except:
    	return "NONE"
    SQL = mysql()
    SQL.execute("SELECT IRCGreeting FROM users_info WHERE UserID='" + dbVal(userid) + "'")
    row = SQL.fetchone()
    SQL.close()
    if len(row[0]) == 0:
        return "NONE"
    else:
        return str(row[0])

def OnIRC(user, nick, status): # mod_OnIRC: add or remove a user in the irc_online_users table
    if conf["mod_OnIRC"].upper() != "TRUE":
	return "DISABLED"
    SQL = mysql()
    if status == "0":
        SQL.execute("DELETE FROM irc_online_users WHERE Username='" + dbVal(user) + "'")
    else:
    	SQL.execute("DELETE FROM irc_online_users WHERE Nickname='" + dbVal(nick) + "'")
	SQL.closecursor()
	SQL.execute("SELECT * FROM irc_online_users WHERE Username='" + dbVal(user) + "'")
	rows = SQL.rowcount()
	SQL.closecursor()
	if rows == 0:
    	   SQL.execute("INSERT INTO irc_online_users (Username, Nickname) VALUES ('" + dbVal(user) + "', '" + dbVal(nick) + "')")
    SQL.close()
    return "SUCCESS"

def changeUserNick(user, nick):
    if conf["mod_OnIRC"].upper() != "TRUE":
	return "DISABLED"
    SQL = mysql()
    SQL.execute("SELECT Nickname FROM irc_online_users WHERE Username='" + dbVal(user) + "'")
    if SQL.rowcount() < 1:
	SQL.close()
	return "XFOUND"
    SQL.closecursor()
    SQL.execute("UPDATE irc_online_users SET Nickname='" + dbVal(nick) + "' WHERE Username='" + dbVal(user) + "'")
    SQL.close()
    return "SUCCESS"

def checkOnIRC(nicks):
    if conf["mod_OnIRC"].upper() != "TRUE":
	return "DISABLED"
    SQL = mysql()
    SQL.execute("SELECT Username, Nickname FROM irc_online_users")
    allonline = SQL.fetchall()
    SQL.closecursor()
    Nicknames = []
    for rawnick in nicks:
	nick = rawnick.strip("~").strip("&")
	Nicknames.append(nick)
    for row in allonline:
	if row[1] not in Nicknames:
    	    SQL.execute("DELETE FROM irc_online_users WHERE Nickname='" + dbVal(row[1]) + "'")
	    SQL.closecursor()
    SQL.close()
    return "SUCCESS"

def AssistAlert(conn, nick, chan):
    if conf["mod_StaffAssistAlerts"].upper() != "TRUE":
	return "DISABLED"

    purged = PurgeAssistReqs()

    if AssistCount.get(nick, 0) > 3:
	conn.privmsg(nick, "You cannot request assistance more than three times in 24Hrs. Staff has been notified and are probably just busy. Please try again later...")
	return "TOO_MANY_REQUESTS"
    elif AssistCount.get(nick, 0) == 0:
	AssistCount[nick] = 1
	FirstAssistReq[nick] = time.time()
    else:
	AssistCount[nick] = int(AssistCount[nick]) + 1
	if not FirstAssistReq.has_key(nick):
	    FirstAssistReq[nick] = time.time()
	AssistCount[nick] = AssistCount.get(nick, 0) + 1

    if chan == conf["DisabledChan"]:
	if conf["mod_SAA_AlertLevel"] == "2":
	    print "*** eMail Alerts for mod_StaffAssistAlerts not yet completed! Sorry! ***" 
	for staffer in GetHighStaff():
            conn.privmsg(staffer[0].strip(" "), nick + " needs assistance in " + chan)
	    ##if conf["mod_SAA_AlertLevel"] == "2":
		## eMail staff member code here....
    else:
	if conf["mod_SAA_AlertLevel"] == "2":
	    print "*** eMail Alerts for mod_StaffAssistAlerts not yet completed! Sorry! ***" 
	for staffer in GetAllStaff():
            conn.privmsg(staffer[0].strip(" "), nick + " needs assistance in " + chan)
	    ##if conf["mod_SAA_AlertLevel"] == "2":
		## eMail staff member code here....
    return purged

def PurgeAssistReqs():
    if conf["mod_StaffAssistAlerts"].upper() != "TRUE":
	return "DISABLED"
    if len(FirstAssistReq) < 1:
        return "EMPTY"
    for nick in FirstAssistReq.keys():
	print nick + "-> First assistance request was " + str(time.time() - FirstAssistReq[nick]) + " seconds ago"
        if time.time() - FirstAssistReq[nick] > 86400:
            del FirstAssistReq[nick]
            del AssistCount[nick]
            return "PURGED"
    return "NOTING_TO_PURGE"


###############################################################################################
###############################################################################################
## IRC Class

print "-> Connecting to IRC Server..."
class ModularBot(ircbot.SingleServerIRCBot): # Executed if the bot's nickname is already taken
    def on_nicknameinuse(self, connection, event):
        print "*** ERROR: Bot's nickname is in use! ***"
	conf["BotNick"] = "_" + conf["BotNick"]
	connection.nick(self, conf["BotNick"])
	
    def on_erroneusnickname(self, connection, event): # Executed if the bot's nickname contains invalid characters
        print "*** ERROR: Illegal characters in BotNick ***"
        print "*** FATAL: quitting ***"
        sys.exit()

## ON WELCOME #####################################################################################
    def on_welcome(self, connection, event): # Executed after the bot is connected
	threadListener.setConnection(connection)
        print "-> Connected to " + conf["IRCServer"] + " with nick: " + conf["BotNick"]
	connection.send_raw("OPER " + conf["OperUser"] + " " + conf["OperPass"])
	connection.privmsg("NICKSERV", "IDENTIFY " + conf["BotNickservPass"])
	connection.send_raw("SETHOST " + conf["BotNick"].lower() + "." + conf["SiteTLD"])
	connection.join(conf["AdminChannel"], conf["AdminChannelPass"])
	threadListener.start()
        print "-> Listening to admin channel: " + conf["AdminChannel"]
	for chanconf in Channels:
	    chan = chanconf.split(' ')
	    if len(chan) > 1 and chan[1].strip(' ') != "":
	        connection.join(chan[0], chan[1]) #Join a password protected channel
	        print "-> Listening to (passworded): " + chan[1]
	    else:
	        connection.send_raw(conf["sajoinCmd"] + " " + conf["BotNick"] + " " + chanconf)
	        print "-> Listening to: " + chanconf

## ON PUBMSG #####################################################################################
    def on_pubmsg(self, connection, event): # Executed when a pulic message is sent in any channel
	conf = shelve.open(".config")
        print event.arguments()[0]
	sent_msg = " ".join(event.arguments())
	sent_nick = event.source().split("!")[0]
	sent_user = event.source().split("!")[1].split("@")[1].split(".")[0]
	sent_host = event.source().split("!")[1].split("@")[1]
	sent_chan = event.target()
	try:
	    sent_cmd = event.arguments()[0].split()[0].upper()
	except IndexError:
	    if len(event.arguments()) <= 1:
	        sent_cmd = event.arguments()
	    else:
		sent_cmd = event.arguments()[0]

	res = checkSiteURL(" ".join(event.arguments()))
	if res != "NONE":
	    connection.privmsg(sent_chan, res)
        if "!HELLO" == sent_cmd:
	    connection.privmsg(sent_nick, "Hello, " + sent_nick + ". Welcome to " + conf["SiteName"] + " IRC!")
        if "!SANDWICH" == sent_cmd:
	    if len(event.arguments()[0].split()) == 1:
	    	connection.privmsg(sent_chan, "Make it yourself, " + sent_nick)
	    else:
                connection.privmsg(sent_chan, sent_nick + " gives " + event.arguments()[0].split()[1] + " a sandwich")
#	if "!SEX" == sent_cmd:
#	    if sent_nick == "PBI325":
#		connection.privmsg(sent_chan, "Tux virtual humps PBI325")
#	    else:
#		connection.privmsg(sent_chan, "Do you really want to sex a penguin, " + sent_nick + "?")
        if "!SUDOSANDWICH" == sent_cmd:
            connection.privmsg(sent_chan, "Ok, " + sent_nick + " here you go... [SANDWICH]")
        if "!SLAP" == sent_cmd and len(event.arguments()[0].split()) == 2:
	    connection.privmsg(sent_chan, sent_nick + " slaps " + event.arguments()[0].split()[1])
#        if "!SUDOSLAP" == sent_cmd and len(event.arguments()[0].split()) == 2:
#            if IsStaff(sent_user):
#                connection.privmsg(sent_chan, event.arguments()[0].split()[1] + " has been sudo slapped!")
#                connection.send_raw("kick" + " " + event.target() + " " + event.arguments()[0].split()[1] + " " + event.arguments()[0].split()[1] + " has been sudo slapped")
#            else:
#                connection.privmsg(sent_chan, "You are not in the sudoers file, this incedent will be reported!")
#        if "!BONUS" == sent_cmd or "!BP" == sent_cmd:
#            connection.privmsg(sent_nick,"You have " + getBonusPoints(sent_user)  + " bonus points")
	if "!USER" == sent_cmd and len(event.arguments()[0].split()) == 2:
	    inf = getUserInfo(event.arguments()[0].split()[1])
	    connection.privmsg(event.target(), inf)
	if "!USER" == sent_cmd and len(event.arguments()[0].split()) == 1:
	    inf = getUserInfo(sent_user)
	    connection.privmsg(event.target(), inf)
	if "!HELP" == sent_cmd:
	    if conf["DisabledChan"] == sent_chan or conf["HelpChan"] == sent_chan or conf["InvitesChan"] == sent_chan:
	        response = AssistAlert(connection, sent_nick, sent_chan)
		if response == "PURGED":
		    print "-> AssistCount and LastAssistReq DICTs purged"
		elif response == "EMPTY":
		    print "-> AssistCount DICT is empty"
		elif response == "NOTHING_TO_PURGE":
		    print "-> No assistance requests to purge.."
		else:
		    print "-> Response from AssistAlert(): " + response
	    else:
	        connection.privmsg(sent_nick, "---- " + conf["BotNick"] + " Help ----")
	        connection.privmsg(sent_nick, "-Commands:")
	        connection.privmsg(sent_nick, "--> !hello : " + conf["BotNick"] + " will send you a PM welcoming you to the server")
	        connection.privmsg(sent_nick, "--> !user [USERNAME] : Returns some basic info on [USERNAME] or yourself if [USERNAME] is not specified")
                connection.privmsg(sent_nick, "--> !sandwich : Ask for a sandwich")
                connection.privmsg(sent_nick, "--> !sudosandwich : Ask for a sandwich like you mean it")
                connection.privmsg(sent_nick, "--> !slap [NICKNAME] : Make  " + conf["BotNick"] + "  slap a user/nick")
	        connection.privmsg(sent_nick, "-Joining Restricted Channels:")
	        connection.privmsg(sent_nick, "--> Syntax: /msg " + conf["BotNick"] + " enter CHANNEL(,CHANNEL2) USERNAME IRCKEY")
	        connection.privmsg(sent_nick, "--> Type the above command anywhere in your IRC client window.")
	        connection.privmsg(sent_nick, "--> You must set your IRCKey in your user profile first!")
	        connection.privmsg(sent_nick, "---- //END Help ----")

## ON PRIVMSG #####################################################################################
    def on_privmsg(self, connection, event): # Executed when the bot recieves a PM
	conf = shelve.open(".config")
	if(len(event.arguments()) == 0):
	     return
	try:
	    sent_cmd = event.arguments()[0].split()[0].upper()
	except IndexError:
	    if len(event.arguments()) <= 1:
	    	sent_cmd = event.arguments()
	    else:
		sent_cmd = event.arguments()[0]
	sent_nick = event.source().split("!")[0]
	sent_user = event.source().split("!")[1].split("@")[1].split(".")[0]

	print "-> PRIVMSG from " + sent_nick + ": " + event.arguments()[0]

        if sent_cmd == "ENTER":
	    if len(event.arguments()[0].split()) < 4:
		connection.privmsg(sent_nick, "Not enough arguments for 'enter' command!")
		connection.privmsg(sent_nick, "Syntax: /msg " + conf["BotNick"] + " enter CHANNEL(,CHANNEL2) USERNAME IRCKEY")
	    else:
	    	sent_chan = event.arguments()[0].split()[1]
		sent_chans = sent_chan.split(",")
	    	sent_userval = event.arguments()[0].split()[2]
	    	sent_irckey = event.arguments()[0].split()[3]

	    	print "-> User(nickname) " + sent_nick + " executed the 'enter' command to enter " + sent_chan + ". Given username: " + sent_userval

	    	if sent_userval == "" or sent_irckey == "" or sent_chan == "":
		    connection.privmsg(sent_nick, "Not enough arguments for 'enter' command!")
		    connection.privmsg(sent_nick, "Syntax: /msg " + conf["BotNick"] + " enter CHANNEL(,CHANNEL2) USERNAME IRCKEY")
	    	else:
		    res = ValidateUser(sent_userval, sent_irckey)
		    print "-> enter Command Result: " + res
		    if res == "MATCH":
			print "-> Changing host and identity for " + sent_userval
			connection.send_raw("CHGIDENT " + sent_nick + " " + str(getUserID(sent_userval)))
			connection.send_raw("CHGHOST " + sent_nick + " " + getUserHost(sent_userval))
			for chan in sent_chans:
		            connection.send_raw(conf["sajoinCmd"] + " " + sent_nick + " " + chan)
			    ircprivs = getIRCPrivs(sent_userval) 
			    if ircprivs != "0": 
	    			connection.privmsg("CHANSERV", IRCPrivCmds[ircprivs] + " " + event.target() + " " + sent_nick)
		    elif res == "DISABLED":
		        connection.privmsg(sent_nick, "You are disabled! You cannot join the member channels unless you are enabled!")
		        if conf["DisabledChan"] != "":
			    connection.privmsg(sent_nick, "You may join " + conf["DisabledChan"] + " and politely ask for your account back...")
		    elif res == "NO_MATCH":
		        connection.privmsg(sent_nick, "Incorrent IRC Key!")
		    elif res == "USER_NOT_FOUND":
		        connection.privmsg(sent_nick, "The username you specified was NOT found!")
		    elif res == "KEY_NOT_SET":
		        connection.privmsg(sent_nick, "Your IRC Key is not set! Please set your IRC Key to join the channels!")

	elif sent_cmd == "RELOAD" and IsHighStaff(sent_user):
            print "-> Reloading configuration"
            connection.privmsg(sent_nick, "Reloading")
            config_response = botconfig.configure("YES")
            if config_response != "Error":
                print "Reload successful"
                conf = shelve.open(".config")
                for i,v in config_response.iteritems():
                    conf[i] = v
                conf.close()
                connection.privmsg(sent_nick, "Reload successful")
            else:
                connection.privmsg(event.source().split("!")[0], "Reload failed, see bot output for details")

	elif sent_cmd == "ENABLE" and IsHighStaff(sent_user) and len(event.arguments()[0].split()) == 2:
	    targetuser = event.arguments()[0].split()[1]
	    print "-> Enabling user '" + targetuser + "'"
	    res = EnableUser(targetuser)
	    if res == "XUSER":
		print "-> Enabling user '" + targetuser + "'" + ": **USER NOT FOUND!**"
		connection.privmsg(sent_nick, "Username not found!")
	    elif res == "ISENABLED":
		print "-> Enabling user '" + targetuser + "' : User Already Enabled!"
		connection.privmsg(sent_nick, "User '" + targetuser + "' is already enabled!")
	    elif res == "SUCCESS":
		print "-> Enabling user '" + targetuser + "' : User Enabled Successfully!"
		connection.privmsg(sent_nick, "User '" + targetuser + "' has been enabled!")
	    
## ON JOIN #####################################################################################
    def on_join(self, connection, event): # Executed when a user JOINS
	conf = shelve.open(".config")
	sent_userid = event.source().split("!")[1].split("@")[0]
	sent_user = event.source().split("!")[1].split("@")[1].split('.')[0]
	sent_nick = event.source().split("!")[0]

	if sent_nick != conf["BotNick"]: # Things to do if the joined nick isn't the ZooKeeper bot
	    print "-> " + sent_user + " (" + sent_userid + ") joined " + event.target() + " with nick '" + sent_nick + "'"

	    if IsHighStaff(sent_nick) and event.target() == conf["AdminChannel"]:
	        connection.send_raw("CHGIDENT " + sent_nick + " " + str(getUserID(sent_nick)))
	        connection.send_raw("CHGHOST " + sent_nick + " " + getUserHost(sent_nick))
	        print ""
	        print "###-> " + sent_nick + " JOINED " + conf["AdminChannel"] + "!"
	        print "-> Changing host and identity for " + sent_nick
	        print "-> SAJOINing " + sent_nick + " to all the channels on the network"
	        print ""
	        for chan in Channels:
	            connection.send_raw(conf["sajoinCmd"] + " " + sent_nick + " " + chan)
	    elif event.target() == conf["AdminChannel"]:
                print "-> Unauthorized user tried to join " + conf["AdminChannel"] + "!!! KICKING USER..."
                connection.send_raw("kick" + " " + event.target() + " " + sent_nick)

	    if event.target() == conf["StaffChan"] and not IsStaff(sent_nick):
	    	connection.send_raw("kick" + " " + event.target() + " " + sent_nick)
	
	    ircprivs = getIRCPrivs(sent_user)
	    if ircprivs != "0":
	        connection.privmsg("CHANSERV", IRCPrivCmds[ircprivs] + " " + event.target() + " " + sent_nick)

	    if event.target() == conf["UserWatchChan"]:
	        res = OnIRC(sent_user, sent_nick, "1")
	        if res == "USER_NOT_FOUND":
		    print "-> OnIRC: User '" + sent_user + "' not found!"
	        elif res == "SUCCESS":
	    	    print "-> '" + sent_user + "' was successfully added to irc_online_users!"
	        greeting = getGreeting(sent_userid)
	        if greeting != "NONE" and greeting != "DISABLED" and event.target() not in AnnounceChans:
                    connection.privmsg(event.target(), "\002[" + sent_nick + "]:\002 " + greeting)

## ON PART #####################################################################################
    def on_part(self, connection, event): # Executed when a user PARTS
	conf = shelve.open(".config")
	sent_user = event.source().split("!")[1].split("@")[1].split('.')[0]
	sent_userid = event.source().split("!")[1].split("@")[0]
	sent_nick = event.source().split("!")[0]

	if sent_nick != conf["BotNick"]:
	    print "-> " + sent_user + " (" + str(sent_userid) + ") parted " + event.target()

	    if event.target() == conf["UserWatchChan"]:
	        res = OnIRC(sent_user, sent_nick, "0")
	        if res == "USER_NOT_FOUND":
		    print "-> OnIRC: User '" + sent_user + "' not found!"
	       	elif res == "SUCCESS":
	    	    print "-> '" + sent_user + "' was successfully removed from irc_online_users!"
	    chan_users = self.channels[conf["UserWatchChan"]].users()
	    res = checkOnIRC(chan_users)
	    print "-> Check online IRC users: " + res

## ON NICK #####################################################################################
    def on_nick(self, connection, event): # Executed when a changes NICK
	conf = shelve.open(".config")
	sent_user = event.source().split("!")[1].split("@")[1].split('.')[0]
	sent_userid = event.source().split("!")[1].split("@")[0]
	try:
	    sent_nick = event.arguments()[0]
	except IndexError:
	    sent_nick = event.arguments()

	if sent_nick != conf["BotNick"]:
	    print "-> " + sent_user + " (" + str(sent_userid) + ") changed their nickname to " + event.target()
	    res = changeUserNick(sent_user, event.target())
	    if res == "XFOUND":
	        print "-> Username '" + sent_user + "' was not found in irc_online_users!"

## ON KICK #####################################################################################
    def on_kick(self, connection, event): # Executed when a user is KICKED
	conf = shelve.open(".config")
	try:
	    sent_nick = event.arguments()[0]
	except IndexError:
	    sent_nick = event.arguments()

	if sent_nick != conf["BotNick"]:
	    print "-> " + sent_nick + " (" + str(getUserID(sent_nick)) + ") was kicked from " + event.target()

	    if event.target() == conf["UserWatchChan"]:
	        res = OnIRC(sent_nick, sent_nick, "0")
	        if res == "USER_NOT_FOUND":
		    print "-> OnIRC: User '" + sent_nick + "' not found!"
	       	elif res == "SUCCESS":
	    	    print "-> '" + sent_nick + "' was successfully removed from irc_online_users!"
	    chan_users = self.channels[conf["UserWatchChan"]].users()
	    res = checkOnIRC(chan_users)
	    print "-> Check online IRC users: " + res

## ON QUIT #####################################################################################
    def on_quit(self, connection, event): # Executed when a user QUITS
	conf = shelve.open(".config")
	sent_user = event.source().split("!")[1].split("@")[1].split('.')[0]
	sent_userid = event.source().split("!")[1].split("@")[0]
	sent_nick = event.source().split("!")[0]

	if sent_nick != conf["BotNick"]:
	    print "-> " + sent_user + " (" + str(sent_userid) + ") has quit"

	    res = OnIRC(sent_user, sent_nick, "0")
	    if res == "USER_NOT_FOUND":
		    print "-> OnIRC: User '" + sent_user + "' not found!"
	    elif res == "SUCCESS":
	    	print "-> '" + sent_user + "' was successfully removed from irc_online_users!"
	    chan_users = self.channels[conf["UserWatchChan"]].users()
	    res = checkOnIRC(chan_users)
	    print "-> Check online IRC users: " + res


###############################################################################################
###############################################################################################
## Start the bot

threadListener = Listener() # Define the listener thread
conf = shelve.open(".config")
bot = ModularBot([(conf["IRCServer"], int(conf["IRCPort"]))], conf["BotNick"], Name) # Define the IRC bot class
try:
    bot.start() # Start the IRC bot
    while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit): # Wait for a keyboard interupt
    print "\n*** Received keyboard interrupt, quitting threads ***"
    threadListener.stop() # Stop the thread
    sys.exit(0)
