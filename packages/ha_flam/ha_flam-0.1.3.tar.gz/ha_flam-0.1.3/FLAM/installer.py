import ConfigParser
import os

import tkMessageBox
from Tkinter import Tk
from tkFileDialog import askdirectory


from getpass import getuser
username = getuser()

########################
testing = True
########################




def unifiySlash(slashPath):
    return slashPath.replace("/", os.sep)


class FlamInstall(object):
    def __init__(self):
        self.appSettingsFolder = r"C:\\Users\\%s\\AppData\\Local\\FLAM" % username
        self.appSettingsFile = os.path.join(self.appSettingsFolder, 'FLAMSettings.ini')
        try:
            os.makedirs(self.appSettingsFolder)
        except WindowsError, e:
                print "Settings folder already created."

        self.settingsPath = ""
        self.installDir = ""
        self.config = ConfigParser.RawConfigParser()

    def setInstallDirectory(self):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        tkMessageBox.showinfo("FLAM Install","Please select a directory to install FLAM to...")    
        self.installDir = unifiySlash(askdirectory(initialdir = "Z:\Code\FLAManager")) # show an "Open" dialog box and return the path to the selected file
        
        #self.settingsPath = os.path.join(self.installDir,'FLAMSettings.ini')
        print "Install Dir: %s" % self.installDir




    def makeSettings(self):
        ###
        ###Creates FLAMSettings.ini based off of colected path if it does not exist
        ###
        if os.path.isfile(self.appSettingsFile):
            print "Settings file has already been created. --> %s" % self.appSettingsFile
            print "\n\nReading Settings:\n"

            
        else:
            print "Creating FLAMSettings.ini at %s" % self.appSettingsFile

            # When adding sections or items, add them in the reverse order of
            # how you want them to be displayed in the actual file.
            # In addition, please note that using RawConfigParser's and the raw
            # mode of ConfigParser's respective set functions, you can assign
            # non-string values to keys internally, but will receive an error
            # when attempting to write to a file or when you get it in non-raw
            # mode. SafeConfigParser does not allow such assignments to take place.
            self.config.add_section('Location')
            self.config.set('Location', 'Server Path', self.installDir)
            self.config.set('Location', 'Local Path', '')
            self.config.set('Location', 'Settings', self.appSettingsFile)

            # Writing our configuration file to 'example.cfg'
            with open(self.appSettingsFile, 'wb') as configfile:
                self.config.write(configfile)

    def readSettings(self):
        print "Setting found. Skipping install."

        configReader = ConfigParser.SafeConfigParser()
        configReader.read(self.getSettingsFile())

        for section_name in configReader.sections():
            print 'Section:', section_name
            print '  Options:', configReader.options(section_name)
            for name, value in configReader.items(section_name):
                print '  %s = %s' % (name, value)
            print

    def getSettingsFile(self):
        return self.appSettingsFile

    def getSetting(self, setting):
        configReader = ConfigParser.SafeConfigParser()
        configReader.read(self.getSettingsFile())
        settingFound = False
        for section_name in configReader.sections():
            for name, value in configReader.items(section_name):
                #print '  %s = %s' % (name, value)
                if setting in name:
                    settingFound = True
                    settingValue = value
        if settingFound:
            return settingValue
        else:
            return None



    def install(self):
        if not os.path.isfile(self.appSettingsFile):
            self.setInstallDirectory()
            self.makeSettings()
        else:
            self.readSettings()




if __name__ == '__main__':
    print "\n\n"
    if testing:
        install = FlamInstall()
        install.setInstallDirectory()
        install.makeSettings()
        input("Install completed. Press enter to exit.")
else:
    print '%s.py imported.' % __name__


