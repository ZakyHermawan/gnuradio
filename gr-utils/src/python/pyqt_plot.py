# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt_plot.ui'
#
# Created: Tue Aug 11 23:12:27 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 696)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.plotHBar = QtGui.QScrollBar(self.centralwidget)
        self.plotHBar.setOrientation(QtCore.Qt.Horizontal)
        self.plotHBar.setObjectName("plotHBar")
        self.gridLayout.addWidget(self.plotHBar, 2, 0, 1, 2)
        self.tabGroup = QtGui.QTabWidget(self.centralwidget)
        self.tabGroup.setObjectName("tabGroup")
        self.timeTab = QtGui.QWidget()
        self.timeTab.setObjectName("timeTab")
        self.horizontalLayout = QtGui.QHBoxLayout(self.timeTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.timePlot = Qwt5.QwtPlot(self.timeTab)
        self.timePlot.setObjectName("timePlot")
        self.horizontalLayout.addWidget(self.timePlot)
        self.tabGroup.addTab(self.timeTab, "")
        self.freqTab = QtGui.QWidget()
        self.freqTab.setObjectName("freqTab")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.freqTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fftPropBox = QtGui.QGroupBox(self.freqTab)
        self.fftPropBox.setMinimumSize(QtCore.QSize(160, 0))
        self.fftPropBox.setObjectName("fftPropBox")
        self.formLayoutWidget = QtGui.QWidget(self.fftPropBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 20, 151, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.fftSizeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.fftSizeLabel.setObjectName("fftSizeLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.fftSizeLabel)
        self.fftComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.fftComboBox.setObjectName("fftComboBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fftComboBox)
        self.horizontalLayout_2.addWidget(self.fftPropBox)
        self.freqPlot = Qwt5.QwtPlot(self.freqTab)
        self.freqPlot.setObjectName("freqPlot")
        self.horizontalLayout_2.addWidget(self.freqPlot)
        self.tabGroup.addTab(self.freqTab, "")
        self.gridLayout.addWidget(self.tabGroup, 1, 0, 1, 1)
        self.filePosBox = QtGui.QGroupBox(self.centralwidget)
        self.filePosBox.setMinimumSize(QtCore.QSize(0, 120))
        self.filePosBox.setObjectName("filePosBox")
        self.formLayoutWidget_2 = QtGui.QWidget(self.filePosBox)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 160, 92))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.filePosLayout = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.filePosLayout.setObjectName("filePosLayout")
        self.filePosStartLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.filePosStartLabel.setObjectName("filePosStartLabel")
        self.filePosLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.filePosStartLabel)
        self.filePosStartLineEdit = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.filePosStartLineEdit.setObjectName("filePosStartLineEdit")
        self.filePosLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.filePosStartLineEdit)
        self.filePosStopLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.filePosStopLabel.setObjectName("filePosStopLabel")
        self.filePosLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.filePosStopLabel)
        self.filePosStopLineEdit = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.filePosStopLineEdit.setObjectName("filePosStopLineEdit")
        self.filePosLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.filePosStopLineEdit)
        self.filePosLengthLabel = QtGui.QLabel(self.formLayoutWidget_2)
        self.filePosLengthLabel.setObjectName("filePosLengthLabel")
        self.filePosLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.filePosLengthLabel)
        self.filePosLengthLineEdit = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.filePosLengthLineEdit.setObjectName("filePosLengthLineEdit")
        self.filePosLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.filePosLengthLineEdit)
        self.formLayoutWidget_4 = QtGui.QWidget(self.filePosBox)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(180, 20, 231, 92))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.fileTimeLayout = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.fileTimeLayout.setObjectName("fileTimeLayout")
        self.fileTimeStartLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.fileTimeStartLabel.setObjectName("fileTimeStartLabel")
        self.fileTimeLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.fileTimeStartLabel)
        self.fileTimeStartLineEdit = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.fileTimeStartLineEdit.setObjectName("fileTimeStartLineEdit")
        self.fileTimeLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fileTimeStartLineEdit)
        self.fileTimeStopLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.fileTimeStopLabel.setObjectName("fileTimeStopLabel")
        self.fileTimeLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fileTimeStopLabel)
        self.fileTimeStopLineEdit = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.fileTimeStopLineEdit.setObjectName("fileTimeStopLineEdit")
        self.fileTimeLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fileTimeStopLineEdit)
        self.fileTimeLengthLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.fileTimeLengthLabel.setObjectName("fileTimeLengthLabel")
        self.fileTimeLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.fileTimeLengthLabel)
        self.fileTimeLengthLineEdit = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.fileTimeLengthLineEdit.setObjectName("fileTimeLengthLineEdit")
        self.fileTimeLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.fileTimeLengthLineEdit)
        self.sysGroupBox = QtGui.QGroupBox(self.filePosBox)
        self.sysGroupBox.setGeometry(QtCore.QRect(530, 0, 200, 120))
        self.sysGroupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sysGroupBox.setObjectName("sysGroupBox")
        self.formLayoutWidget_3 = QtGui.QWidget(self.sysGroupBox)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(0, 20, 191, 91))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_2.setObjectName("formLayout_2")
        self.sampleRateLabel = QtGui.QLabel(self.formLayoutWidget_3)
        self.sampleRateLabel.setObjectName("sampleRateLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.sampleRateLabel)
        self.sampleRateLineEdit = QtGui.QLineEdit(self.formLayoutWidget_3)
        self.sampleRateLineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.sampleRateLineEdit.setObjectName("sampleRateLineEdit")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.sampleRateLineEdit)
        self.displayGroupBox = QtGui.QGroupBox(self.filePosBox)
        self.displayGroupBox.setGeometry(QtCore.QRect(730, 0, 170, 120))
        self.displayGroupBox.setMinimumSize(QtCore.QSize(170, 0))
        self.displayGroupBox.setObjectName("displayGroupBox")
        self.verticalLayoutWidget = QtGui.QWidget(self.displayGroupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 160, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.colorComboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.colorComboBox.setObjectName("colorComboBox")
        self.verticalLayout.addWidget(self.colorComboBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.filePosBox, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 25))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtGui.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_exit = QtGui.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.menu_File.addAction(self.action_open)
        self.menu_File.addAction(self.action_exit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        self.tabGroup.setCurrentIndex(0)
        QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL("activated()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabGroup.setTabText(self.tabGroup.indexOf(self.timeTab), QtGui.QApplication.translate("MainWindow", "Time Domain", None, QtGui.QApplication.UnicodeUTF8))
        self.fftPropBox.setTitle(QtGui.QApplication.translate("MainWindow", "FFT Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.fftSizeLabel.setText(QtGui.QApplication.translate("MainWindow", "FFT Size", None, QtGui.QApplication.UnicodeUTF8))
        self.tabGroup.setTabText(self.tabGroup.indexOf(self.freqTab), QtGui.QApplication.translate("MainWindow", "Frequency Domain", None, QtGui.QApplication.UnicodeUTF8))
        self.filePosBox.setTitle(QtGui.QApplication.translate("MainWindow", "File Position", None, QtGui.QApplication.UnicodeUTF8))
        self.filePosStartLabel.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.filePosStopLabel.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.filePosLengthLabel.setText(QtGui.QApplication.translate("MainWindow", "Length", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTimeStartLabel.setText(QtGui.QApplication.translate("MainWindow", "time start (sec)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTimeStopLabel.setText(QtGui.QApplication.translate("MainWindow", "time stop (sec)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTimeLengthLabel.setText(QtGui.QApplication.translate("MainWindow", "time length (sec)", None, QtGui.QApplication.UnicodeUTF8))
        self.sysGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "System Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.sampleRateLabel.setText(QtGui.QApplication.translate("MainWindow", "Sample Rate", None, QtGui.QApplication.UnicodeUTF8))
        self.displayGroupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Display Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_open.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qwt5
