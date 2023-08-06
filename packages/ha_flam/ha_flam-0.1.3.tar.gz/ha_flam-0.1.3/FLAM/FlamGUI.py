#FlamGUI.py
#Created By: Hunter Albaugh
#git yiiisss


import sys
from PySide import QtGui
from PySide import QtCore
from ConfigParser import SafeConfigParser

from installer import FlamInstall

import QTCSS as css

import dbQueries as db
from dbQueries import DATABASE_LOCATION

import folderStructure

print "FlamGui - DBLOC - %s" % DATABASE_LOCATION


#MAIN GUI WINDOW
class FlamGui(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(FlamGui, self).__init__(parent)

        self.appStyle = '{background-color: rgb(60, 60, 60);}'
        self.setStyleSheet("QMainWindow" + self.appStyle)
        
        self.initUI()
        

        

    def initUI(self):
        ###File/Exit
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        ###File/Open
        openProjectAction = QtGui.QAction('&Open project', self)
        openProjectAction.setShortcut('Ctrl+O')
        openProjectAction.setStatusTip('Open a project...')
        openProjectAction.triggered.connect(self.openProject)

        ###File/Test Function 
        testFunctionAction = QtGui.QAction('&Test Function', self)
        testFunctionAction.setShortcut('Ctrl+T')
        testFunctionAction.setStatusTip('Test Function...')
        testFunctionAction.triggered.connect(self.testFunc)



        status = self.statusBar().setStyleSheet("statusBar" + self.appStyle)

        menubar = self.menuBar()

        menubar.setStyleSheet(css.menubarCSS)




        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openProjectAction)
        fileMenu.addAction(testFunctionAction)
        fileMenu.addAction(exitAction)

        self.resize(1200, 700)
        self.center()
        
        self.setWindowTitle('Freelance Asset Manager')
        self.setWindowIcon(QtGui.QIcon('icons/flam_icon.png'))
        

        self.addMainGui()

    def addMainGui(self):

        self.flam_widget = FLAMWidget(self)
        self.ingest_widget = IngestPanel()

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(self.flam_widget, "Project View")
        self.tabWidget.addTab(self.ingest_widget, "Ingest")
        self.tabWidget.setStyleSheet(css.mainTabCSS)
        _widget = QtGui.QWidget()
        _layout = QtGui.QVBoxLayout(_widget)
        _layout.addWidget(self.tabWidget)
        self.setCentralWidget(_widget)
 

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def openProject(self):
        QtGui.QMessageBox.question(self, 'Placeholder',
            "This is a placeholder button.", QtGui.QMessageBox.Ok )


    #Used to test anything.......
    def testFunc(self):
        ###HOW DO I GET RID OF THIS MONSTER EFFICIENTLY?!?!?
        ###
        self.flam_widget.infoPane.projectNameLabel.setContent("Pine Apple Express: 7")
        ###
        ###

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", 
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
                                            QtGui.QMessageBox.Yes)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def getSettings(self):
        pass    
  
#LAYOUTS FOR WINDOW
class FLAMWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(FLAMWidget, self).__init__(parent)
        self.__layout()


    def __layout(self):

        #project info  #asset preview
                #asset browser

        #self.test_button = QtGui.QPushButton("Click me")
        
        #Top Left Show Selection Panel
        self.showSelectionPane = ShowSelectionPanel()
        print "CUR SHOW FROM SHOW SELECTION PANE: %s" % self.showSelectionPane.getCurrentShow()

        #Top Left Pane
        self.infoPane = ProjectInfoFrame()
        if self.showSelectionPane.getCurrentShow():
            self.infoPane.updateProjectName(self.showSelectionPane.getCurrentShow().getName())
            self.infoPane.updateShotName(self.showSelectionPane.getCurrentShot().getName())

        #Adds control based on show/shot changes
        self.showSelectionPane.addInfoPane(self.infoPane)


        #Top Right Pane
        self.assetFrame = AssetViewerFrame()
        


        #Bottom Pane
        self.assets_frame = QtGui.QFrame(self)
        self.assets_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.assets_frame.setStyleSheet("background-color: rgb(50, 50, 50)")
        self.assets_frame.setFrameStyle(QtGui.QFrame.Sunken)

        #Creating Layouts
        self.rootVbox = QtGui.QVBoxLayout()
        self.topBox = QtGui.QHBoxLayout()
        self.bottomBox = QtGui.QHBoxLayout()
        self.splitterLayout = QtGui.QVBoxLayout()

        #splitter testing -- HORIZONTAL
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter1.addWidget(self.showSelectionPane)
        self.splitter1.addWidget(self.infoPane)
        self.splitter1.addWidget(self.assetFrame)
        self.splitter1.setStretchFactor(1,10)
        
        #self.splitter1.setSizes([1000,200])

        #splitter testing -- VERTICAL
        self.splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.assets_frame)
        self.splitter2.setStretchFactor(1,10)
        self.splitter2.setStyleSheet(css.splitterCSS)

        self.splitterLayout.addWidget(self.splitter2)

        #Adding widgets to layouts
        self.topBox.addWidget(self.infoPane)
        self.topBox.addWidget(self.assetFrame)
        self.bottomBox.addWidget(self.assets_frame)

        #self.rootVbox.addStretch(1)
        self.rootVbox.addLayout(self.topBox)
        self.rootVbox.addLayout(self.bottomBox)

        self.setLayout(self.splitterLayout)


class AssetViewerFrame(QtGui.QFrame):
    def __init__(self, parent = None):
        super(AssetViewerFrame, self).__init__(parent)

        ###
        ###TEMP HARD CODED
        self.tempImage = QtGui.QPixmap("icons/temp.png")
        self.tempImage = self.tempImage.scaled(250, 250, QtCore.Qt.KeepAspectRatio) 
        ###
        ###FRAME STILL NEEDS TO BE RESIZED SO ITS NOT HUGE

        self.buildFrame()
        self.buildContent()
        self.buildLayout()


    def buildFrame(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameStyle(QtGui.QFrame.Sunken)
        #self.setMaximumSize(400,180)
        self.setStyleSheet("background-color: rgb(53, 50, 50)")

    def buildContent(self):
        self.imgLabel = QtGui.QLabel(self)
        self.imgLabel.setPixmap(self.tempImage)


    def buildLayout(self):
        self.asset_info_layout = QtGui.QVBoxLayout()
        self.asset_info_layout.addStretch(0)
        self.asset_info_layout.addWidget(self.imgLabel)
        self.setLayout(self.asset_info_layout)


class AssetBrowserFrame(QtGui.QFrame):
    def __init__(self, parent = None):
        super(AssetBrowserFrame, self).__init__(parent)

        ###
        ###TEMP HARD CODED
        ###

        self.buildFrame()
        self.buildContent()
        self.buildLayout()


    def buildFrame(self):   
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameStyle(QtGui.QFrame.Sunken)
        self.setStyleSheet("background-color: rgb(50, 50, 50)")

    def buildContent(self):
        self.imgLabel = QtGui.QLabel(self)
        self.imgLabel.setPixmap(self.tempImage)


    def buildLayout(self):
        self.asset_info_layout = QtGui.QVBoxLayout()
        self.asset_info_layout.addStretch(0)
        self.asset_info_layout.addWidget(self.imgLabel)
        self.setLayout(self.asset_info_layout)


class ProjectInfoFrame(QtGui.QFrame):
    def __init__(self, parent = None):
        super(ProjectInfoFrame, self).__init__(parent)

        ###
        ###TEMP HARD CODED
        self.labelTextColor = "rgb(150, 150, 150)"
        self.infoTextColor = "rgb(220, 220, 220)"

        self.projectName = ""
        self.shotName = ""
        self.shotFrameRange = ""
        ###
        ###

        self.buildFrame()
        self.buildInfoLabels()
        self.buildLayout()


    def buildFrame(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameStyle(QtGui.QFrame.Sunken)
        #self.setMaximumSize(400,180)
        self.setStyleSheet("background-color: rgb(50, 50, 50)")

    #Would it be faster to edit instead of rebuild? Might be worth making all of this easily accessable.
    def buildInfoLabels(self):

        self.projectNameLabel = ProjectInfoLabel('Project Name:', self.projectName, self.labelTextColor, self.infoTextColor)
        self.shotNameLabel = ProjectInfoLabel('Shot Name:', self.shotName, self.labelTextColor, self.infoTextColor)
        #self.shotFrameRangeLabel = ProjectInfoLabel('Frame Range:', self.shotFrameRange, self.labelTextColor, self.infoTextColor)


    def buildLayout(self):
        self.shot_info_layout = QtGui.QVBoxLayout()
        self.shot_info_layout.addLayout(self.projectNameLabel)
        self.shot_info_layout.addLayout(self.shotNameLabel)
        #self.shot_info_layout.addLayout(self.shotFrameRangeLabel)
        self.shot_info_layout.addStretch(0)
        self.setLayout(self.shot_info_layout)

    def updateProjectName(self, name):
        self.projectNameLabel.setContent(name)

    def updateShotName(self, name):
        self.shotNameLabel.setContent(name)


class ShowSelectionPanel(QtGui.QFrame):
    def __init__(self, parent = None):
        super(ShowSelectionPanel, self).__init__(parent)

        self.currentShow = None
        self.currentShot = None
        self.infoPane = None

        self.currentShotList = []
        try:
            self.showList = db.getAllShows()
        except:
            self.showList = []


        self.buildFrame()
        self.buildComboBoxes()
        self.buildLayout()





    def buildFrame(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameStyle(QtGui.QFrame.Sunken)
        #self.setMaximumSize(400,180)
        self.setStyleSheet("background-color: rgb(50, 50, 50)")

    #Would it be faster to edit instead of rebuild? Might be worth making all of this easily accessable.
    def buildComboBoxes(self):

        ####PROJECT LIST COMBO BOX
        #print "INIT SHOW COMBO BOXES."
        showList = self.getShowList()
        
        self.projectComboFrame = QtGui.QFrame()
        self.shotComboFrame = QtGui.QFrame()

        self.projectComboLabel = QtGui.QLabel("Project:")
        self.shotComboLabel = QtGui.QLabel("Shot:")

        self.projectComboFrameLayout = QtGui.QHBoxLayout()
        self.shotComboFrameLayout = QtGui.QHBoxLayout()


        self.projectCombo = QtGui.QComboBox(self)
        for s in showList:
            self.projectCombo.addItem(s.getName())
        self.projectCombo.setStyleSheet(css.showComboBoxCSS)
        self.projectCombo.currentIndexChanged.connect(self.showComboChanged)

        #NOT THE BEST WAY TO DO THIS
        #WILL HAVE TO ELIMINATE THE POSSIBILITY OF DUPLICATES
        curShowName = self.projectCombo.currentText()
        #Saving Show object to be easily tangible
        try:
            self.setCurrentShow(db.getShow(curShowName))
        except Exception, e:
            print "self.setCurrentShow(db.getShow(curShowName))\n%s" % e



        #prep to create shot list
        try:
            curShowId = self.getCurrentShow().getShowID()
            self.setCurrentShotList(db.getAllShots(curShowId))
        except AttributeError, e:
            print "Database is currently empty. ERR: %s" % e
        curShotList = self.getCurrentShotList()

        ####SHOT LIST FOR CURRENT PROJECT
        self.shotCombo = QtGui.QComboBox(self)

        if curShotList:
            for s in curShotList:
                self.shotCombo.addItem(s.getName())
        self.shotCombo.setStyleSheet(css.showComboBoxCSS)
        self.shotCombo.currentIndexChanged.connect(self.shotComboChanged)

        curShotName = self.shotCombo.currentText()
        if curShotList:
            for s in curShotList:
                if s.getName() == curShotName:
                    self.setCurrentShot(s)

        #print "FINISHED COMBO BOX INIT."

        self.projectComboFrameLayout.addWidget(self.projectComboLabel)
        self.projectComboFrameLayout.addWidget(self.projectCombo)

        self.shotComboFrameLayout.addWidget(self.shotComboLabel)
        self.shotComboFrameLayout.addWidget(self.shotCombo)

        self.projectComboFrame.setLayout(self.projectComboFrameLayout)
        self.shotComboFrame.setLayout(self.shotComboFrameLayout)

        self.applyButton = QtGui.QPushButton("Apply")
        self.applyButton.clicked.connect(self.updateInfoPane)

    def buildLayout(self):
        self.shot_info_layout = QtGui.QVBoxLayout()
        self.shot_info_layout.addWidget(self.projectComboFrame)
        self.shot_info_layout.addWidget(self.shotComboFrame)
        self.shot_info_layout.addWidget(self.applyButton)
        self.shot_info_layout.addStretch(0)
        self.setLayout(self.shot_info_layout)

    def getCurrentShow(self):
        #print "Getting current show"
        return self.currentShow

    def getCurrentShot(self):
        #print "Getting current shot"
        return self.currentShot

    def getCurrentShotList(self):
        #print "Getting current shot"
        return self.currentShotList

    def getShowList(self):
        return self.showList

    def _setShowList(self, newList):
        self.showList = newList
    
    def setCurrentShotList(self, shotList):
        #print "Getting current shot"
        self.currentShotList = shotList

    def setCurrentShow(self, show):
        self.currentShow = show

    def setCurrentShot(self, shot):
        self.currentShot = shot

    def showComboChanged(self):
        print "SHOW CHANGED. UPDATING SHOTS."
        curShowName = self.projectCombo.currentText()
        if not self.getCurrentShow().getName() == curShowName:
            self.setCurrentShow(db.getShow(curShowName))

            #Rebuilding shot list
            curShowId = self.getCurrentShow().getShowID()
            self.setCurrentShotList(db.getAllShots(curShowId))
            curShotList = self.getCurrentShotList()
            self.shotCombo.clear()
            for s in curShotList:
                self.shotCombo.addItem(s.getName())

            curShotName = self.shotCombo.currentText()
            for s in curShotList:
                if s.getName() == curShotName:
                    self.setCurrentShot(s)


    def shotComboChanged(self):
        curShotName = self.shotCombo.currentText()
        for s in self.getCurrentShotList():
            if s.getName() == curShotName:
                self.setCurrentShot(s)


    def addInfoPane(self, pane):
        self.infoPane = pane

    def updateInfoPane(self):
        self.infoPane.updateProjectName(self.getCurrentShow().getName())
        self.infoPane.updateShotName(self.getCurrentShot().getName())


class ProjectInfoLabel(QtGui.QHBoxLayout):
    def __init__(self, title, content, titleColor, contentColor):
        super(ProjectInfoLabel, self).__init__()
        self.titleColor = titleColor
        self.contentColor = contentColor
        self.title = title
        self.content = content

        self.initLabel()

    def initLabel(self):
        #Creating title label
        self.titleLabel = QtGui.QLabel(self.title)
        self.titleLabel.setStyleSheet("QLabel {color: %s ; font: bold 16pt Calibri  }" % self.titleColor)

        #Creating content label
        self.contentLabel = QtGui.QLabel(self.content)
        self.contentLabel.setStyleSheet("QLabel {color: %s ; font: 16pt Calibri  }" % self.contentColor)

        #Adding to self.layout
        self.addWidget(self.titleLabel)
        self.addWidget(self.contentLabel)
        self.addStretch(0)


    def getTitle(self):
        return self.title

    def setTitle(self, newTitle):
        if not self.title == newTitle:
            self.title = newTitle
            self.updateGui()

    def getContent(self):
        return self.content

    def setContent(self, newContent):
        if not self.content == newContent:
            self.content = newContent
            self.updateGui()

    def updateGui(self):
        self.titleLabel.setText(self.title)
        self.contentLabel.setText(self.content)


class IngestPanel(QtGui.QWidget):
    def __init__(self):
        super(IngestPanel, self).__init__()

        ###TEMP CALL##################################
        ###NEEDS TO MORE EFFICIENTLY CALL DB FOR SHOWS
        ###If already called, should not call again. 
        self.showList = db.getAllShows()

        self.buildIngestPane()

    #From qtDesigner
    def buildIngestPane(self):

        self.injestTab = QtGui.QWidget()  
        self.setObjectName("injestTab")

        self.mainContainerHlayout = QtGui.QHBoxLayout(self)
        self.mainContainerHlayout.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.mainContainerHlayout.setObjectName("mainContainerHlayout")
        self.ingestViewMainFrame = QtGui.QFrame(self)
        self.ingestViewMainFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ingestViewMainFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.ingestViewMainFrame.setObjectName("ingestViewMainFrame")

        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.ingestViewMainFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
       
        self.frame_7 = QtGui.QFrame(self.ingestViewMainFrame)
        self.frame_7.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.ingestModeComboFrame = QtGui.QFrame(self.frame_7)
        self.ingestModeComboFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ingestModeComboFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.ingestModeComboFrame.setObjectName("ingestModeComboFrame")
        
        self.showMenu_vertLayout = QtGui.QVBoxLayout()

        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.ingestModeComboFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        
        self.ingestModeLabel = QtGui.QLabel( "Ingest Mode:")
        self.ingestModeLabel.setObjectName("ingestModeLabel")
        
        self.ingestModeComboBox = QtGui.QComboBox(self.ingestModeComboFrame)
        self.ingestModeComboBox.setObjectName("ingestMode")
        self.ingestModeComboBox.addItem("Show")
        self.ingestModeComboBox.addItem("Shot")
        self.ingestModeComboBox.addItem("Asset")
        
        self.horizontalLayout_5.addWidget(self.ingestModeLabel)
        self.horizontalLayout_5.addWidget(self.ingestModeComboBox)

        self.shotModeComboFrame = QtGui.QFrame(self.frame_7)
        self.shotModeComboFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.shotModeComboFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.shotModeComboFrame.setObjectName("shotModeComboFrame")

        self.showSelect_horizontalLayout = QtGui.QHBoxLayout(self.shotModeComboFrame)
        self.showSelect_horizontalLayout.setObjectName("showSelect_horizontalLayout")

        self.showSelectLabel = QtGui.QLabel( "Show:",)
        self.showSelectLabel.setObjectName("showSelectLabel")
        
        self.showSelectComboBox = QtGui.QComboBox()
        self.showSelectComboBox.setObjectName("ingestMode")

        for s in self.showList:
            self.showSelectComboBox.addItem(s.getName())

        self.showSelect_horizontalLayout.addWidget(self.showSelectLabel)
        self.showSelect_horizontalLayout.addWidget(self.showSelectComboBox)

        #self.shotModeComboFrame.addWidget()

        self.verticalLayout_3.addWidget(self.shotModeComboFrame)
        self.verticalLayout_3.addWidget(self.ingestModeComboFrame)
        self.verticalLayout_3.addStretch(1)
        self.horizontalLayout_3.addWidget(self.frame_7)
        
        self.ingestInputFrame = QtGui.QFrame(self.ingestViewMainFrame)
        self.ingestInputFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ingestInputFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.ingestInputFrame.setObjectName("ingestInputFrame")
        
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ingestInputFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        self.ingestNameLineEditFrame = QtGui.QFrame(self.ingestInputFrame)
        self.ingestNameLineEditFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ingestNameLineEditFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.ingestNameLineEditFrame.setObjectName("ingestNameLineEditFrame")
        
        self.nameLineEditHlayout = QtGui.QHBoxLayout(self.ingestNameLineEditFrame)
        self.nameLineEditHlayout.setObjectName("nameLineEditHlayout")
        
        self.nameLabel = QtGui.QLabel("Name:", self.ingestNameLineEditFrame)
        self.nameLabel.setObjectName("nameLabel")
        
        self.nameLineEditHlayout.addWidget(self.nameLabel)
        
        self.nameLineEdit = QtGui.QLineEdit(self.ingestNameLineEditFrame)
        self.nameLineEdit.setFixedWidth(400)
        self.nameLineEdit.setFrame(True)
        self.nameLineEdit.setDragEnabled(False)
        self.nameLineEdit.setReadOnly(False)
        self.nameLineEdit.setObjectName("nameLineEdit")
        
        self.nameLineEditHlayout.addWidget(self.nameLineEdit)
        self.nameLineEditHlayout.addStretch(1)

        self.verticalLayout_4.addWidget(self.ingestNameLineEditFrame)
        
        self.ingestPathLineEditFrame = QtGui.QFrame(self.ingestInputFrame)
        self.ingestPathLineEditFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.ingestPathLineEditFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.ingestPathLineEditFrame.setObjectName("ingestPathLineEditFrame")
        
        self.pathLineEditHlayout = QtGui.QHBoxLayout(self.ingestPathLineEditFrame)
        self.pathLineEditHlayout.setObjectName("pathLineEditHlayout")
        
        self.filePathLabel = QtGui.QLabel("Location:", self.ingestPathLineEditFrame)
        self.filePathLabel.setObjectName("filePathLabel")
        
        self.pathLineEditHlayout.addWidget(self.filePathLabel)
        
        self.filePathLineEdit = QtGui.QLineEdit(self.ingestPathLineEditFrame)
        self.filePathLineEdit.setFixedWidth(400)
        self.filePathLineEdit.setAutoFillBackground(False)
        self.filePathLineEdit.setObjectName("filePathLineEdit")
        self.filePathLineEdit.setPlaceholderText("Click browse to select a path...")
        self.filePathLineEdit.setReadOnly(True)
        
        self.pathLineEditHlayout.addWidget(self.filePathLineEdit)
        
        self.browseButton = QtGui.QPushButton(self.ingestPathLineEditFrame)
        self.browseButton.setText("Browse...")
        self.browseButton.setAutoDefault(False)
        self.browseButton.setDefault(True)
        self.browseButton.setFlat(False)
        self.browseButton.setObjectName("browseButton")
        self.browseButton.clicked.connect(self.browseFilePath)
        
        self.pathLineEditHlayout.addWidget(self.browseButton)
        self.pathLineEditHlayout.addStretch(1)

        self.ingestSubmitButton = QtGui.QPushButton(self.ingestPathLineEditFrame)
        self.ingestSubmitButton.setText("Submit...")
        self.ingestSubmitButton.setFixedWidth(100)
        self.ingestSubmitButton.clicked.connect(self.ingestCreate)

        self.verticalLayout_4.addWidget(self.ingestPathLineEditFrame)
        self.verticalLayout_4.addWidget(self.ingestSubmitButton)
        self.verticalLayout_4.addStretch(1)

        self.horizontalLayout_3.addWidget(self.ingestInputFrame)
        self.mainContainerHlayout.addWidget(self.ingestViewMainFrame)


    def browseFilePath(self):
        print "IT FUCKING WORKED"
        folderName = QtGui.QFileDialog.getExistingDirectory(None,'Open File', '/')
        print folderName
        self.filePathLineEdit.setText(folderName)

    def ingestCreate(self):
        cbText = self.ingestModeComboBox.currentText().lower()
        if "show" in cbText:
            self.createShow()

        elif "shot" in cbText:
            self.createShot()

        elif "asset" in cbText:
            self.createAsset()


    def createShow(self):
        print "Show created."
        print "Test Change"


    def createShot(self):
        path = self.filePathLineEdit.text()
        show = self.getCurShow()
        shotName = self.nameLineEdit.text()
        #DB CALL - NEEDS PATHS TO BE ADDED TO DB
        #db.addShotToShow(show,shotName)
        #create folder strucuture here

        print "PATH: %s" % path
        print "SHOW: %s" % show
        print "NAME: %s" % shotName
        print "Shot created."

    def createAsset(self):
        print "Asset created."

    def ingestSubmit(self):
        pass

    def getCurShow(self):
        return self.showSelectComboBox.currentText().upper()




def main():
    
    app = QtGui.QApplication(sys.argv)
    #flam = Example()
    flam = FlamGui()
    flam.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
            myFlamInstall = FlamInstall()
            myFlamInstall.install()

    except Exception, e:
        print "Error installing.  Double check..."
        print "Error: %s" % e

    main()