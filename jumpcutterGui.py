import json
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

GUI_SETTINGS_FILENAME = "gui_settings.json"


# jea.. Windows.. I guess
def get_download_folder():
    if os.name == 'nt':
        import ctypes
        from ctypes import windll, wintypes
        from uuid import UUID

        # ctypes GUID copied from MSDN sample code
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ]

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff

        sh_get_known_folder_path = windll.shell32.SHGetKnownFolderPath
        sh_get_known_folder_path.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD,
            wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = ctypes.c_wchar_p()
            guid = GUID(uuidstr)
            if sh_get_known_folder_path(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
                raise ctypes.WinError()
            return pathptr.value

        folderid_download = '{374DE290-123F-4565-9164-39C4925E467B}'
        return _get_known_folder_path(folderid_download)
    else:
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


class UiJumpcutter(object):
    def __init__(self, jumpcutter):
        jumpcutter.setObjectName("jumpcutter")
        jumpcutter.resize(790, 600)
        self.centralwidget = QtWidgets.QWidget(jumpcutter)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 0, 761, 571))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.horizontalLayoutWidget_2.setFont(font)
        self.horizontalLayoutWidget_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.horizontalLayoutWidget_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sourceSelectioncomboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.sourceSelectioncomboBox.setFont(font)
        self.sourceSelectioncomboBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.sourceSelectioncomboBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sourceSelectioncomboBox.setObjectName("sourceSelectioncomboBox")
        self.sourceSelectioncomboBox.addItem("")
        self.sourceSelectioncomboBox.addItem("")
        self.sourceSelectioncomboBox.addItem("")
        self.verticalLayout_3.addWidget(self.sourceSelectioncomboBox)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.sourceLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.sourceLineEdit.setFont(font)
        self.sourceLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.sourceLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sourceLineEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.sourceLineEdit.setObjectName("sourceLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sourceLineEdit)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.destinationLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.destinationLineEdit.setFont(font)
        self.destinationLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.destinationLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.destinationLineEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.destinationLineEdit.setObjectName("destinationLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.destinationLineEdit)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.line.setFont(font)
        self.line.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.line.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_9.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(25, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.silentThresholdLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.silentThresholdLineEdit.setFont(font)
        self.silentThresholdLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.silentThresholdLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.silentThresholdLineEdit.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.silentThresholdLineEdit.setObjectName("silentThresholdLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.silentThresholdLineEdit)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setAcceptDrops(False)
        self.label_5.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.silentSpeedLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.silentSpeedLineEdit.setFont(font)
        self.silentSpeedLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.silentSpeedLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.silentSpeedLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.silentSpeedLineEdit.setObjectName("silentSpeedLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.silentSpeedLineEdit)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.soundedSpeedLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.soundedSpeedLineEdit.setFont(font)
        self.soundedSpeedLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.soundedSpeedLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.soundedSpeedLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.soundedSpeedLineEdit.setObjectName("soundedSpeedLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.soundedSpeedLineEdit)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_6.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.sampleRateLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.sampleRateLineEdit.setFont(font)
        self.sampleRateLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.sampleRateLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sampleRateLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.sampleRateLineEdit.setObjectName("sampleRateLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.sampleRateLineEdit)
        self.frameRateLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.frameRateLineEdit.setFont(font)
        self.frameRateLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.frameRateLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.frameRateLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.frameRateLineEdit.setText("")
        self.frameRateLineEdit.setMaxLength(4)
        self.frameRateLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.frameRateLineEdit.setPlaceholderText("")
        self.frameRateLineEdit.setClearButtonEnabled(False)
        self.frameRateLineEdit.setObjectName("frameRateLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.frameRateLineEdit)
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_8.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.frameQualityhorizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.frameQualityhorizontalSlider.setFont(font)
        self.frameQualityhorizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frameQualityhorizontalSlider.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.frameQualityhorizontalSlider.setMinimum(0)
        self.frameQualityhorizontalSlider.setMaximum(31)
        self.frameQualityhorizontalSlider.setProperty("value", 3)
        self.frameQualityhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.frameQualityhorizontalSlider.setObjectName("frameQualityhorizontalSlider")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.frameQualityhorizontalSlider)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_7.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.frameMarginLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.frameMarginLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.frameMarginLineEdit.setObjectName("frameMarginLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frameMarginLineEdit)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.line_2.setFont(font)
        self.line_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.line_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item)
        self.runButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.runButton.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.runButton.setFont(font)
        self.runButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.runButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.runButton.setObjectName("runButton")
        self.verticalLayout_3.addWidget(self.runButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        jumpcutter.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(jumpcutter)
        self.statusbar.setObjectName("statusbar")
        jumpcutter.setStatusBar(self.statusbar)

        self.retranslateUi(jumpcutter)
        QtCore.QMetaObject.connectSlotsByName(jumpcutter)

    def retranslateUi(self, Jumpcutter):
        _translate = QtCore.QCoreApplication.translate
        Jumpcutter.setWindowTitle(_translate("jumpcutter", "jumpcutter"))
        self.sourceSelectioncomboBox.setItemText(0, _translate("jumpcutter", "Download Video from Youtube"))
        self.sourceSelectioncomboBox.setItemText(1, _translate("jumpcutter", "Convert all .mp4\'s in a whole Folder"))
        self.sourceSelectioncomboBox.setItemText(2, _translate("jumpcutter", "Convert a single .mp4 File"))
        self.label.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI/URL depending on what "
                       "is selected above</span></p></body></html>"))
        self.label.setText(_translate("jumpcutter", "Source:"))
        self.sourceLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI/URL depending on what "
                       "is selected above</span></p></body></html>"))
        self.label_3.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full "
                       "URI</span></p></body></html>"))
        self.label_3.setText(_translate("jumpcutter", "Destination:"))
        self.destinationLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full "
                       "URI</span></p></body></html>"))
        self.label_9.setText(_translate("jumpcutter", "Detailed Settings"))
        self.label_4.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">The volume amount that frames\' audio "
                       "needs to surpass to be consider &quot;sounded&quot;.</span></p><p><span style=\" "
                       "font-size:10pt;\">It ranges from 0 (silence) to 1 (max volume)</span></p></body></html>"))
        self.label_4.setText(_translate("jumpcutter", "Slilent Threshold"))
        self.silentThresholdLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">The volume amount that frames\' audio "
                       "needs to surpass to be consider &quot;sounded&quot;.</span></p><p><span style=\" "
                       "font-size:10pt;\">It ranges from 0 (silence) to 1 (max volume)</span></p></body></html>"))
        self.label_5.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">The speed that silent frames should be "
                       "played at.</span></p><p><span style=\" font-size:10pt;\">999999 for "
                       "jumpcutting.</span></p></body></html>"))
        self.label_5.setText(_translate("jumpcutter", "Silent Speed"))
        self.silentSpeedLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">The speed that silent frames should be "
                       "played at.</span></p><p><span style=\" font-size:10pt;\">999999 for "
                       "jumpcutting.</span></p></body></html>"))
        self.label_2.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">the speed that sounded (spoken) frames "
                       "should be played at.</span></p><p><span style=\" font-size:10pt;\">Typically 1 to "
                       "1.5</span></p></body></html>"))
        self.label_2.setText(_translate("jumpcutter", "Sounded Speed"))
        self.soundedSpeedLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">the speed that sounded (spoken) frames "
                       "should be played at.</span></p><p><span style=\" font-size:10pt;\">Typically 1 to "
                       "1.5</span></p></body></html>"))
        self.label_6.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Sample rate of the input and output "
                       "videos</span></p></body></html>"))
        self.label_6.setText(_translate("jumpcutter", "Sample Rate"))
        self.sampleRateLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Sample rate of the input and output "
                       "videos</span></p></body></html>"))
        self.frameRateLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Frame rate of the input and output "
                       "videos. optional... I try to find it out myself,</span></p><p><span style=\" "
                       "font-size:10pt;\">But it doesn\'t always work.</span></p></body></html>"))
        self.label_8.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Quality of frames to be extracted from "
                       "input video. 1 is highest, 31 is lowest, </span></p><p><span style=\" font-size:10pt;\">3 is "
                       "the default.</span></p></body></html>"))
        self.label_8.setText(
            _translate("jumpcutter", "Frame Quality"))
        self.frameQualityhorizontalSlider.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Quality of frames to be extracted from "
                       "input video. 1 is highest, 31 is lowest, </span></p><p><span style=\" font-size:10pt;\">3 is "
                       "the default.</span></p></body></html>"))
        self.label_7.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Frame rate of the input and output "
                       "videos. optional... I try to find it out myself,</span></p><p><span style=\" "
                       "font-size:10pt;\">But it doesn\'t always work.</span></p></body></html>"))
        self.label_7.setText(
            _translate("jumpcutter", "Frame Rate"))
        self.label_10.setText(
            _translate("jumpcutter", "Frame Margin"))
        self.frameMarginLineEdit.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">some silent frames adjacent to sounded "
                       "frames are included to provide context.</span></p><p><span style=\" font-size:10pt;\"> How "
                       "many frames on either the side of speech should be included? That's this "
                       "variable.</span></p></body></html>"))
        self.runButton.setToolTip(
            _translate("jumpcutter",
                       "<html><head/><body><p><span style=\" font-size:10pt;\">Modifies a video file to play at "
                       "different speeds when there is sound vs. silence.<br/><br/></span><span style=\" "
                       "font-size:12pt; font-weight:600;\">Expected Runtime is 0.5 to 2x the original playback "
                       "speed<br/>Long videos may require python 64bit due to memory "
                       "requirenments</span></p></body></html>"))
        self.runButton.setText(
            _translate("jumpcutter", "Run!"))

    def apply_settings(self, settings: dict):
        # comboboxes
        self.sourceSelectioncomboBox.setCurrentIndex(settings["state_of_combobox"])
        # textboxes
        self.sourceLineEdit.setText(settings["source"])
        self.destinationLineEdit.setText(settings["destination"])
        self.silentThresholdLineEdit.setText(str(settings["silent_threshold"]))
        self.soundedSpeedLineEdit.setText(str(settings["sounded_speed"]))
        self.silentSpeedLineEdit.setText(str(settings["silent_speed"]))
        self.frameMarginLineEdit.setText(str(settings["frame_margin"]))
        self.sampleRateLineEdit.setText(str(settings["sample_rate"]))
        self.frameRateLineEdit.setText(str(settings["frame_rate"]))
        # sliders
        self.frameQualityhorizontalSlider.setValue(settings["frame_quality"])

    def get_settings(self):
        settings = dict()
        # comboboxes
        settings["state_of_combobox"] = self.sourceSelectioncomboBox.currentIndex()
        # textboxes
        settings["source"] = self.sourceLineEdit.text()
        settings["destination"] = self.destinationLineEdit.text()
        settings["silent_threshold"] = self.silentThresholdLineEdit.text()
        settings["sounded_speed"] = self.soundedSpeedLineEdit.text()
        settings["silent_speed"] = self.silentSpeedLineEdit.text()
        settings["frame_margin"] = self.frameMarginLineEdit.text()
        settings["sample_rate"] = self.sampleRateLineEdit.text()
        settings["frame_rate"] = self.frameRateLineEdit.text()
        # sliders
        settings["frame_quality"] = self.frameQualityhorizontalSlider.value()
        return settings


def generate_settings():
    with open(GUI_SETTINGS_FILENAME, "r") as settings_file:
        settings = json.load(settings_file)
    if settings["source"] == "":
        settings["source"] = get_download_folder()
    if settings["destination"] == "":
        settings["destination"] = get_download_folder()
    return settings


def save_gui_settings(settings=None):
    if settings is None:
        settings = {
            "state_of_combobox": 2,
            "source": "",
            "destination": "",
            "silent_threshold": 0.03,
            "sounded_speed": 1.00,
            "silent_speed": 5.00,
            "frame_margin": 1,
            "sample_rate": 44100,
            "frame_rate": 30,
            "frame_quality": 3
        }
    with open(GUI_SETTINGS_FILENAME, "w+") as settings_file:
        json.dump(settings, settings_file)


def initiate_gui():
    if not os.path.isfile(GUI_SETTINGS_FILENAME):
        save_gui_settings()
    app = QtWidgets.QApplication(sys.argv)
    jumpcutter = QtWidgets.QMainWindow()
    settings = generate_settings()
    ui = UiJumpcutter(jumpcutter)
    ui.apply_settings(settings)
    jumpcutter.show()

    # app was closed
    exitcode = app.exec_()
    save_gui_settings(ui.get_settings())
    sys.exit(exitcode)


if __name__ == "__main__":
    initiate_gui()
