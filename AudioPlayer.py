import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
import sys
from pygame import mixer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QAction, QLabel, QPushButton,
                            QFileDialog, QHBoxLayout, QVBoxLayout,
                            QWidget, QFileSystemModel, QTreeView)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDir, QModelIndex
mixer.init()

class AudioMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 750, 500)
        self.setWindowTitle("audio player")

        self.AudioList = QFileSystemModel()
        audioList = self.AudioList
        self.TreeView = QTreeView()
        self.TreeView.setModel(audioList)

        self.TreeView.hideColumn(1)
        self.TreeView.hideColumn(2)
        w0 = self.TreeView.columnWidth(0) + 100
        self.TreeView.setColumnWidth(0, w0)

        self.soundPlayNotice = QWidget()
        SPNLabel = QLabel("sound playing...", self.soundPlayNotice)
        self.SPNstopButton = QPushButton("click to stop", self.soundPlayNotice)
        self.SPNLayout = QVBoxLayout()
        self.SPNLayout.addWidget(SPNLabel)
        self.SPNLayout.addWidget(self.SPNstopButton)
        self.soundPlayNotice.setLayout(self.SPNLayout)

        mainWidget = QWidget()
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.TreeView)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        self.MenuBarInit()
        self.initGui()


    def MenuBarInit(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")

        getFilesAction = QAction("&get files", self)
        getFilesAction.setShortcut("Ctrl+G")
        getFilesAction.setStatusTip("retrieve files from file manager")
        getFilesAction.triggered.connect(self.fileInput)

        fileMenu.addAction(getFilesAction)

    def initGui(self):
        treeView = self.TreeView
    
    def fileInput(self):
        fileGet = QFileDialog.getExistingDirectory()

        treeView = self.TreeView
        audioList = self.AudioList
        audioList.setRootPath(fileGet)
        audioList.setNameFilters(['*.mp3'])
        audioList.setFilter(QDir.Files)
        audioList.setNameFilterDisables(False)
        treeView.setRootIndex(audioList.index(fileGet))
        treeView.clicked.connect(self.fileClicked)
    
    def fileClicked(self, indexFile: QModelIndex):
        filePath = self.AudioList.filePath(indexFile)
        mixer.music.load(filePath)
        self.SPNstopButton.clicked.connect(self.stopMusic)
        self.soundPlayNotice.show()
        mixer.music.play(-1)
    
    def stopMusic(self):
        mixer.music.stop()
        self.soundPlayNotice.close()

windowApp = QApplication(sys.argv)
windowMain = AudioMainWindow()
windowMain.show()
sys.exit(windowApp.exec_())