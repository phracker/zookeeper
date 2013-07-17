#!/usr/bin/python

import urllib, urllib2
import time, os, sys, string, tarfile, shutil

def update(VERSION="NONE"):
    print "Checking for updates ...",
    URL = "http://tbsf.me/zookeeper/zookeeperupdate.php?version=%s" % VERSION
    response = urllib.urlopen(URL).read().replace("\n","")
    #response =
    #           OK : pass
    #           NO/NO/versionnumber : get new version, no config changes
    #           NO/YES/versionnumber/instructions : get new version, confirm config changes
    if response != "OK":
        try:
            if response.split("/")[1] == "NO":
                print "\n*******************************************************"
		print "** NEW VERSION OF ZooKeeper IS AVAILABLE!"
		print "** Current Version: " + VERSION
		print "********************************************************\n"
		ans = raw_input('Would you like to download the new version? (Y/n):'); 
		if ans.upper() != "Y" and ans.upper() != "YES":
		    return
                print
                print "Upgrading to version " + response.split("/")[2]
                print "---------------------------------------------"
                print "Downloading zookeeper-%s.tar.gz from server ... " % response.split("/")[2],
                # urllib.urlretrieve(url[, filename[, reporthook[, data]]])
                url = "http://tbsf.me/zookeeper/zookeeper-%s.tar.gz" % response.split("/")[2]
                file = urllib.urlopen(url).read()
                open("../zookeeper-%s.tar.gz" % response.split("/")[2],"w").write(file)
                print "Done"
                print "Extracting files ... ",
                tarball = tarfile.open("../zookeeper-%s.tar.gz" % response.split("/")[2], "r:gz")
                tarball.extractall(path="..")
                print "Done"
                print "Removing tarball ... ",
                os.remove("../zookeeper-%s.tar.gz" % response.split("/")[2])
                print "Done"
                print "Copying conf file to new location ... ",
                shutil.copyfile("zookeeper.conf", "../zookeeper-%s/zookeeper.conf" % response.split("/")[2])
                print "Done"
                print "Update complete"
                newdir = os.getcwd().split("/")
                newdir.pop()
                newdir += ["zookeeper-%s" % response.split("/")[2]]
                print "You can find your new ZooKeeper at %s" % "/".join(newdir)
		print "The zookeeper.conf file has been copied there also"
                sys.exit()
            else:
                print
                print "WARNING: this update requires changes to zookeeper.conf"
                print "ZooKeeper may become unusable with your current configuration"
                while True:
                    upgrade = raw_input("Do you want to upgrade to version %s anyway? (y/n/v/q)\n(y=upgrade, n=continue, v=see changelog, q=quit\n>>> " % response.split("/")[2])
                    if upgrade == "y":
                        print "Upgrading to version " + response.split("/")[2]
                        print "---------------------------------------------"
                        print "Downloading zookeeper-%s.tar.gz from server ... " % response.split("/")[2],
                        # urllib.urlretrieve(url[, filename[, reporthook[, data]]])
                        url = "http://tbsf.me/zookeeper/zookeeper-%s.tar.gz" % response.split("/")[2]
                        file = urllib.urlopen(url).read()
                        open("../zookeeper-%s.tar.gz" % response.split("/")[2],"w").write(file)
                        print "Done"
                        print "Extracting files ... ",
                        tarball = tarfile.open("../zookeeper-%s.tar.gz" % response.split("/")[2], "r:gz")
                        tarball.extractall(path="..")
                        print "Done"
                        print "Removing tarball ... ",
                        os.remove("../zookeeper-%s.tar.gz" % response.split("/")[2])
                        print "Done"
                        print "Copying conf file to new location (with suffix .old) ... ",
                        shutil.copyfile("zookeeper.conf", "../zookeeper-%s/zookeeper.conf.old" % response.split("/")[2])
                        print "Done"
                        print "Update complete"
                        newdir = os.getcwd().split("/")
                        newdir.pop()
                        newdir += ["zookeeper-%s" % response.split("/")[2]]
                        print "You can find your new ZooKeeper at %s" % "/".join(newdir)
                        print "Remember to edit zookeeper.conf before using ZooKeeper again"
                        print "\n------------------------------------------------------"
                        print " Instructions for upgrading Zookeeper config"
                        print "------------------------------------------------------"
                        print "------------------------------------------------------"
                        print response.split("/")[3].replace("NEWLINE", "\n")
                        print "------------------------------------------------------\n"
                        sys.exit()
                        
                        break
                    elif upgrade == "n":
                        print "Ignoring upgrade, to ignore ugrades in future, use the --noupdates command line option"
                        break
                    elif upgrade == "v":
                        changelog = urllib.urlopen("http://tbsf.me/zookeeper/CHANGES").read()
                        changes = changelog.split("\n")
                        versiondone = "no"
                        for line in changes:
                            if "version" in line:
                                if versiondone == "yes":
                                    break
                                else:
                                    versiondone = "yes"
                            print line
                    elif upgrade == "q":
                        sys.exit()
                        
        except IndexError:
            print "Error updating, using current version"
    else: 
        print " None found"


