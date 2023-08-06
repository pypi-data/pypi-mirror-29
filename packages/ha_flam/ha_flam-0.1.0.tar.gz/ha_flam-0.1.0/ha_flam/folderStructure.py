#showFolderStructure.py

import os




def makeDefaultShowFolder(showName, path):
    showLoc = os.path.join(path, showName)
    fullPath = os.path.join(showLoc,("SHOTS"))

    try:
        os.makedirs(fullPath)
        print "SHOW: '%s' - Created at: '%s'." % (showName, showLoc)
    except WindowsError, e:
        print "Show '%s' exists. Skipping folder creation." % showName
        #print "WindowsError:", e

def makeDefaultShotFolder(showName, shotName, path):
    showLoc = os.path.join(path, showName)
    shotsLoc = os.path.join(showLoc,"SHOTS")
    shotPath = os.path.join(shotsLoc, shotName)

    #folders
    folderDict = {"ASSETS" : ["FOOTAGE", "VFX"], "RENDERS" : ["OUTPUT","PRECOMP", "WIP"], "SCRIPTS" : ["NUKE"]}

    ###SHOT NAME FOLDER
    try:
        os.makedirs(shotPath)
        print "SHOT: '%s' - Created at: '%s'." % (shotName, shotPath)
    except WindowsError, e:
        print "Skipping '%s'." % shotName
        #print "WindowsError:", e

    #iterate through to create structure
    for f, sf in folderDict.items():
        #CURRENT FOLDER
        curFolder = os.path.join(shotPath, f)
        try:
            os.makedirs(curFolder)
        except WindowsError, e:
            print "Skipping '%s'." % f
            #print "WindowsError:", e

        #CREATING SUBFOLDERS
        for sub in sf:
            subFolder = os.path.join(curFolder, sub)
            try:
                os.makedirs(subFolder)
            except WindowsError, e:
                print "Skipping '%s'." % sub
                #print "WindowsError:", e







def main():
    showName = "UNK"
    testShotName = "tst_0010"
    testPath = r"Z:\Localize"

    #makeDefaultShowFolder(showName, testPath)
    #makeDefaultShotFolder(showName, testShotName, testPath)


if __name__ == "__main__":
    main()