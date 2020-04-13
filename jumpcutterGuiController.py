import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from jumpcutterGuiModelView import Ui_Jumpcutter


def initiate():
    app = QtWidgets.QApplication(sys.argv)
    jumpcutter = QtWidgets.QMainWindow()
    ui = Ui_Jumpcutter()
    ui.setupUi(jumpcutter)
    jumpcutter.show()
    sys.exit(app.exec_())
