import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from jumpcutterGuiModelView import Ui_Jumpcutter


def get_download_folder():
    return ""


def initiateGUI():
    app = QtWidgets.QApplication(sys.argv)
    jumpcutter = QtWidgets.QMainWindow()
    ui = generate_ui_from_settings()
    ui.setupUi(jumpcutter)
    jumpcutter.show()
    sys.exit(app.exec_())


def generate_ui_from_settings():
    with open("gui_settings.json", "r") as settings_file:
        settings = json.load(settings_file)
        if settings["source"] == "":
            settings["source"] = get_download_folder()
        if settings["destination"] == "":
            settings["destination"] = get_download_folder()
        ui = Ui_Jumpcutter()
        # comboboxes
        ui.sourceSelectioncomboBox.setCurrentIndex(settings["state_of_combobox"])
        # textboxes
        ui.sourceLineEdit.setText(settings["source"])
        ui.destinationLineEdit.setText(settings["destination"])
        ui.silentThresholdLineEdit.setText(settings["silent_threshold"])
        ui.soundedSpeedLineEdit.setText(settings["sounded_speed"])
        ui.silentSpeedLineEdit.setText(settings["silent_speed"])
        ui.frameMarginLineEdit.setText(settings["frame_margin"])
        ui.sampleRateLineEdit.setText(settings["sample_rate"])
        ui.frameRateLineEdit.setText(settings["frame_rate"])
        # sliders
        ui.frameQualityhorizontalSlider.setValue(settings["frame_quality"])
    return ui


def generate_gui_settings_json():
    settings = {
        "state_of_combobox": 1,
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
    with open("gui_settings.json", "w+") as settings_file:
        json.dump(settings, settings_file)


if __name__ == "__main__":
    generate_gui_settings_json()
    initiateGUI()
