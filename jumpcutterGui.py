import json
import os
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QLocale
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QMessageBox, QMainWindow
import jumpcutter

GUI_SETTINGS_FILENAME = "gui_settings.json"


# jea.. Windows.. I guess.. wish everything would be as simple as
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


def save_file(starting_path="", message="Select a filename"):
    user_input = QFileDialog.getSaveFileName(None, message, get_download_folder(), filter="*.mp4")[0]
    if len(user_input) is not None:
        return user_input
    return starting_path


def choose_file(starting_path="", message="Select a filename"):
    user_input = QFileDialog.getOpenFileName(None, message, get_download_folder(), filter="*.mp4")[0]
    if len(user_input) is not None:
        return user_input
    return starting_path


def choose_directory(starting_path="", message='Select a folder'):
    user_input = QFileDialog.getExistingDirectory(None, message, get_download_folder())
    if len(user_input) is not None:
        return user_input
    return starting_path


def create_warning_popup(text: str):
    msg = QMessageBox()
    msg.setWindowTitle("Something Went Wrong")
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()


class UiJumpcutter(object):
    def __init__(self, main_window: QMainWindow):
        # variables
        self.sourceMode = 1  # file
        self.destinationMode = 1  # file
        # locale for Validators
        self.locale = QLocale(QLocale.English, QLocale.UnitedStates)
        # Setup Validators
        self.onlyInt = QIntValidator()
        self.onlyInt.setLocale(self.locale)
        self.onlyInt.setBottom(0)
        self.onlyFloat = QDoubleValidator()
        self.onlyFloat.setLocale(self.locale)
        self.onlyFloat.setBottom(0.0)

        main_window.setObjectName("Jumpcutter")
        main_window.resize(900, 750)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 850, 720))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.widget.setFont(font)
        self.widget.setToolTip("")
        self.widget.setObjectName("widget")

        # colors
        self.redPalette = self.widget.palette()
        self.redPalette.setColor(self.widget.backgroundRole(), QtCore.Qt.red)
        self.whitePalette = self.widget.palette()
        self.whitePalette.setColor(self.widget.backgroundRole(), QtCore.Qt.white)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setToolTip("")
        self.label_12.setTextFormat(QtCore.Qt.AutoText)
        self.label_12.setScaledContents(False)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.sourceSelectioncomboBox = QtWidgets.QComboBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.sourceSelectioncomboBox.setFont(font)
        self.sourceSelectioncomboBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.sourceSelectioncomboBox.setToolTip("")
        self.sourceSelectioncomboBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sourceSelectioncomboBox.setObjectName("sourceSelectioncomboBox")
        self.sourceSelectioncomboBox.addItem("")
        self.sourceSelectioncomboBox.addItem("")
        self.sourceSelectioncomboBox.addItem("")
        self.verticalLayout_3.addWidget(self.sourceSelectioncomboBox)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item)
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setToolTip("")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        spacer_item1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item1)
        self.label_11 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setToolTip("")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_3.addWidget(self.label_11)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI/URL depending on what is "
            "selected above</span></p></body></html>")
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.sourceLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.sourceLineEdit.setFont(font)
        self.sourceLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.sourceLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI/URL depending on what is "
            "selected above</span></p></body></html>")
        self.sourceLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sourceLineEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.sourceLineEdit.setObjectName("sourceLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sourceLineEdit)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_3.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI</span></p></body></html>")
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.destinationLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.destinationLineEdit.setFont(font)
        self.destinationLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.destinationLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Format: Full URI</span></p></body></html>")
        self.destinationLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.destinationLineEdit.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.destinationLineEdit.setObjectName("destinationLineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.destinationLineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sourceSelectionButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.sourceSelectionButton.setFont(font)
        self.sourceSelectionButton.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Opens a Source Selection Popup Depending on the "
            "Processing option selected above</span></p></body></html>")
        self.sourceSelectionButton.setObjectName("sourceSelectionButton")
        self.horizontalLayout.addWidget(self.sourceSelectionButton)
        self.destinationSelectionButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.destinationSelectionButton.setFont(font)
        self.destinationSelectionButton.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Opens a Destination Selection Popup Depending on "
            "the Processing option selected above</span></p></body></html>")
        self.destinationSelectionButton.setObjectName("destinationSelectionButton")
        self.horizontalLayout.addWidget(self.destinationSelectionButton)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        spacer_item2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item2)
        self.line = QtWidgets.QFrame(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.line.setFont(font)
        self.line.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.line.setToolTip("")
        self.line.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        spacer_item3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item3)
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setToolTip("")
        self.label_9.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(25, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_4.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">The volume amount that frames\' audio needs to "
            "surpass to be consider &quot;sounded&quot;.</span></p><p><span style=\" font-size:10pt;\">It ranges from "
            "0 (silence) to 1 (max volume)</span></p></body></html>")
        self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.silentThresholdLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.silentThresholdLineEdit.setFont(font)
        self.silentThresholdLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.silentThresholdLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">The volume amount that frames\' audio needs to "
            "surpass to be consider &quot;sounded&quot;.</span></p><p><span style=\" font-size:10pt;\">It ranges from "
            "0 (silence) to 1 (max volume)</span></p></body></html>")
        self.silentThresholdLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.silentThresholdLineEdit.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.silentThresholdLineEdit.setValidator(self.onlyFloat)
        self.silentThresholdLineEdit.setObjectName("silentThresholdLineEdit")
        self.silentThresholdLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.silentThresholdLineEdit))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.silentThresholdLineEdit)
        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setAcceptDrops(False)
        self.label_5.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">The speed that silent frames should be played "
            "at.</span></p><p><span style=\" font-size:10pt;\">999999 for jumpcutting.</span></p></body></html>")
        self.label_5.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.silentSpeedLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.silentSpeedLineEdit.setFont(font)
        self.silentSpeedLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.silentSpeedLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">The speed that silent frames should be played "
            "at.</span></p><p><span style=\" font-size:10pt;\">999999 for jumpcutting.</span></p></body></html>")
        self.silentSpeedLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.silentSpeedLineEdit.setValidator(self.onlyFloat)
        self.silentSpeedLineEdit.setObjectName("silentSpeedLineEdit")
        self.silentSpeedLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.silentSpeedLineEdit))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.silentSpeedLineEdit)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">the speed that sounded (spoken) frames should be "
            "played at.</span></p><p><span style=\" font-size:10pt;\">Typically 1 to 1.5</span></p></body></html>")
        self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.soundedSpeedLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.soundedSpeedLineEdit.setFont(font)
        self.soundedSpeedLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.soundedSpeedLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">the speed that sounded (spoken) frames should be "
            "played at.</span></p><p><span style=\" font-size:10pt;\">Typically 1 to 1.5</span></p></body></html>")
        self.soundedSpeedLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.soundedSpeedLineEdit.setValidator(self.onlyFloat)
        self.soundedSpeedLineEdit.setObjectName("soundedSpeedLineEdit")
        self.soundedSpeedLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.soundedSpeedLineEdit))
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.soundedSpeedLineEdit)
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_6.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Sample rate of the input and output "
            "videos</span></p></body></html>")
        self.label_6.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.sampleRateLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.sampleRateLineEdit.setFont(font)
        self.sampleRateLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.sampleRateLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Sample rate of the input and output "
            "videos</span></p></body></html>")
        self.sampleRateLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.sampleRateLineEdit.setValidator(self.onlyFloat)
        self.sampleRateLineEdit.setObjectName("sampleRateLineEdit")
        self.sampleRateLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.sampleRateLineEdit))
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.sampleRateLineEdit)
        self.frameRateLineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.frameRateLineEdit.setFont(font)
        self.frameRateLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.frameRateLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Frame rate of the input and output videos. "
            "optional... I try to find it out myself,</span></p><p><span style=\" font-size:10pt;\">But it doesn\'t "
            "always work.</span></p></body></html>")
        self.frameRateLineEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.frameRateLineEdit.setValidator(self.onlyFloat)
        self.frameRateLineEdit.setText("")
        self.frameRateLineEdit.setMaxLength(4)
        self.frameRateLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.frameRateLineEdit.setPlaceholderText("")
        self.frameRateLineEdit.setClearButtonEnabled(False)
        self.frameRateLineEdit.setObjectName("frameRateLineEdit")
        self.frameRateLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.frameRateLineEdit))
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.frameRateLineEdit)
        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_8.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Quality of frames to be extracted from input "
            "video. 1 is highest, 31 is lowest, </span></p><p><span style=\" font-size:10pt;\">3 is the "
            "default.</span></p></body></html>")
        self.label_8.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.frameQualityhorizontalSlider = QtWidgets.QSlider(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.frameQualityhorizontalSlider.setFont(font)
        self.frameQualityhorizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frameQualityhorizontalSlider.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Quality of frames to be extracted from input "
            "video. 1 is highest, 31 is lowest, </span></p><p><span style=\" font-size:10pt;\">3 is the "
            "default.</span></p></body></html>")
        self.frameQualityhorizontalSlider.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.frameQualityhorizontalSlider.setMinimum(0)
        self.frameQualityhorizontalSlider.setMaximum(31)
        self.frameQualityhorizontalSlider.setProperty("value", 3)
        self.frameQualityhorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.frameQualityhorizontalSlider.setObjectName("frameQualityhorizontalSlider")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.frameQualityhorizontalSlider)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_7.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Frame rate of the input and output videos. "
            "optional... I try to find it out myself,</span></p><p><span style=\" font-size:10pt;\">But it doesn\'t "
            "always work.</span></p></body></html>")
        self.label_7.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_10 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">some silent frames adjacent to sounded frames are "
            "included to provide context. How many frames on either the side of speech should be included? That's "
            "this variable.</span></p></body></html>")
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.frameMarginLineEdit = QtWidgets.QLineEdit(self.widget)
        self.frameMarginLineEdit.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">some silent frames adjacent to sounded frames are "
            "included to provide context. How many frames on either the side of speech should be included? That's "
            "this variable.</span></p></body></html>")
        self.frameMarginLineEdit.setObjectName("frameMarginLineEdit")
        self.frameMarginLineEdit.setValidator(self.onlyInt)
        self.frameRateLineEdit.textEdited.connect(lambda: self.validate_line_edit(self.frameRateLineEdit))
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frameMarginLineEdit)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacer_item4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item4)
        spacer_item5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacer_item5)
        self.runButton = QtWidgets.QPushButton(self.widget)
        self.runButton.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(size_policy)
        self.runButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.runButton.setFont(font)
        self.runButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.runButton.setToolTip(
            "<html><head/><body><p><span style=\" font-size:10pt;\">Modifies a video file to play at different speeds "
            "when there is sound vs. silence.<br/><br/></span><span style=\" font-size:12pt; "
            "font-weight:600;\">Expected Runtime is 0.5 to 2x the original playback speed<br/>Long videos may require "
            "python 64bit due to memory requirenments</span></p></body></html>")
        self.runButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.runButton.setAutoDefault(True)
        self.runButton.setDefault(True)
        self.runButton.setFlat(False)
        self.runButton.setObjectName("runButton")
        self.verticalLayout_3.addWidget(self.runButton)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.label_12.setBuddy(self.sourceSelectioncomboBox)
        self.label.setBuddy(self.sourceLineEdit)
        self.label_3.setBuddy(self.destinationLineEdit)
        self.label_4.setBuddy(self.silentThresholdLineEdit)
        self.label_5.setBuddy(self.silentSpeedLineEdit)
        self.label_2.setBuddy(self.soundedSpeedLineEdit)
        self.label_6.setBuddy(self.sampleRateLineEdit)
        self.label_8.setBuddy(self.frameQualityhorizontalSlider)
        self.label_7.setBuddy(self.frameRateLineEdit)
        self.label_10.setBuddy(self.frameMarginLineEdit)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        main_window.setTabOrder(self.sourceSelectioncomboBox, self.sourceSelectionButton)
        main_window.setTabOrder(self.sourceSelectionButton, self.destinationSelectionButton)
        main_window.setTabOrder(self.destinationSelectionButton, self.sourceLineEdit)
        main_window.setTabOrder(self.sourceLineEdit, self.destinationLineEdit)
        main_window.setTabOrder(self.destinationLineEdit, self.silentThresholdLineEdit)
        main_window.setTabOrder(self.silentThresholdLineEdit, self.silentSpeedLineEdit)
        main_window.setTabOrder(self.silentSpeedLineEdit, self.soundedSpeedLineEdit)
        main_window.setTabOrder(self.soundedSpeedLineEdit, self.sampleRateLineEdit)
        main_window.setTabOrder(self.sampleRateLineEdit, self.frameRateLineEdit)
        main_window.setTabOrder(self.frameRateLineEdit, self.frameMarginLineEdit)
        main_window.setTabOrder(self.frameMarginLineEdit, self.frameQualityhorizontalSlider)
        main_window.setTabOrder(self.frameQualityhorizontalSlider, self.runButton)

        # ---------------- LISTENERS ----------------
        self.runButton.clicked.connect(self.run_clicked)
        self.sourceSelectionButton.clicked.connect(self.source_selection_clicked)
        self.destinationSelectionButton.clicked.connect(self.destination_selection_clicked)
        self.sourceSelectioncomboBox.currentIndexChanged.connect(self.mode_switch)
        # ---------------- LISTENERS ----------------

    def retranslate_ui(self, main_window: QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("Jumpcutter", "Jumpcutter"))
        self.label_12.setText(_translate("Jumpcutter", "1. Main Processing Options Selection"))
        self.sourceSelectioncomboBox.setItemText(0, _translate("Jumpcutter", "Download Video from Youtube"))
        self.sourceSelectioncomboBox.setItemText(1, _translate("Jumpcutter", "Convert all .mp4\'s in a whole Folder"))
        self.sourceSelectioncomboBox.setItemText(2, _translate("Jumpcutter", "Convert a single .mp4 File"))
        self.label_11.setText(_translate("Jumpcutter", "2. Source and Destination Settings"))
        self.label.setText(_translate("Jumpcutter", "Source:"))
        self.label_3.setText(_translate("Jumpcutter", "Destination:"))
        self.sourceSelectionButton.setText(_translate("Jumpcutter", "Select Source Popup"))
        self.destinationSelectionButton.setText(_translate("Jumpcutter", "Select Destination Popup"))
        self.label_9.setText(_translate("Jumpcutter", "3. Detailed Settings"))
        self.label_4.setText(_translate("Jumpcutter", "Slilent Threshold"))
        self.label_5.setText(_translate("Jumpcutter", "Silent Speed"))
        self.label_2.setText(_translate("Jumpcutter", "Sounded Speed"))
        self.label_6.setText(_translate("Jumpcutter", "Sample Rate"))
        self.label_8.setText(_translate("Jumpcutter", "Frame Quality"))
        self.label_7.setText(_translate("Jumpcutter", "Frame Rate"))
        self.label_10.setText(_translate("Jumpcutter", "Frame Margin"))
        self.runButton.setText(_translate("Jumpcutter", "4. Run!"))

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
        settings["state_of_combobox"] = int(self.sourceSelectioncomboBox.currentIndex())
        # textboxes
        settings["source"] = self.sourceLineEdit.text()
        settings["destination"] = self.destinationLineEdit.text()
        settings["silent_threshold"] = float(self.silentThresholdLineEdit.text())
        settings["sounded_speed"] = float(self.soundedSpeedLineEdit.text())
        settings["silent_speed"] = float(self.silentSpeedLineEdit.text())
        settings["frame_margin"] = int(self.frameMarginLineEdit.text())
        settings["sample_rate"] = float(self.sampleRateLineEdit.text())
        settings["frame_rate"] = float(self.frameRateLineEdit.text())
        # sliders
        settings["frame_quality"] = int(self.frameQualityhorizontalSlider.value())
        return settings

    # invoked by listener
    def run_clicked(self):
        self.runButton.setEnabled(False)
        settings = self.get_settings()
        try:
            jumpcutter.process_settings(settings)
        except [AssertionError, IOError, TypeError]:
            create_warning_popup("Something went wrong. Please check the Console for spesifics")
        self.runButton.setEnabled(True)

    # invoked by listener
    def mode_switch(self):
        index = self.sourceSelectioncomboBox.currentIndex()
        if index == 0:  # ytdownload
            self.sourceSelectionButton.setEnabled(False)
            self.sourceSelectionButton.setText("Just Copy-Paste the YT Link")
            self.destinationMode = 1  # file
            self.destinationSelectionButton.setText("Save a Destination File")
        elif index == 1:  # folder conversion
            self.sourceSelectionButton.setEnabled(True)
            self.sourceMode = 2  # folder
            self.sourceSelectionButton.setText("Select a Source Folder")
            self.destinationMode = 2  # folder
            self.destinationSelectionButton.setText("Select a Destination Folder")
        else:  # file conversion
            self.sourceSelectionButton.setEnabled(True)
            self.sourceMode = 1  # file
            self.sourceSelectionButton.setText("Select a Source File")
            self.destinationMode = 1  # file
            self.destinationSelectionButton.setText("Save a Destination File")

    # invoked by listener
    def source_selection_clicked(self):
        if self.sourceMode == 1:  # file
            self.sourceLineEdit.setText(choose_file(starting_path=self.sourceLineEdit.text()))
        elif self.sourceMode == 2:  # folder
            self.sourceLineEdit.setText(choose_directory(starting_path=self.sourceLineEdit.text()))

    # invoked by listener
    def destination_selection_clicked(self):
        if self.sourceMode == 1:  # file
            self.sourceLineEdit.setText(save_file(starting_path=self.sourceLineEdit.text()))
        elif self.sourceMode == 2:  # folder
            self.sourceLineEdit.setText(choose_directory(starting_path=self.sourceLineEdit.text()))

    def validate_line_edit(self, line_edit: QLineEdit):
        if line_edit.validator().validate(line_edit.text(), 0) is not QValidator.Acceptable:
            line_edit.setPalette(self.redPalette)
        else:
            line_edit.setPalette(self.redPalette)


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
            "sample_rate": 44100.0,
            "frame_rate": 30.0,
            "frame_quality": 3
        }
    with open(GUI_SETTINGS_FILENAME, "w+") as settings_file:
        json.dump(settings, settings_file)


def initiate_gui():
    if not os.path.isfile(GUI_SETTINGS_FILENAME):
        save_gui_settings()
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    settings = generate_settings()
    ui = UiJumpcutter(main_window)
    ui.apply_settings(settings)
    main_window.show()

    # app was closed
    exitcode = app.exec_()
    save_gui_settings(ui.get_settings())
    sys.exit(exitcode)


if __name__ == "__main__":
    initiate_gui()
