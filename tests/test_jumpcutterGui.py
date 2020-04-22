import json
import os
from unittest import TestCase

import Gui.jumpcutterGui as J_gui

# constants
PROJECT_ROOT = os.path.normpath(os.path.join(__file__, '..', '..'))
DOWNLOAD_FOLDER = r"C:\Users\frank\Downloads"
GUI_FOLDER = os.path.join(PROJECT_ROOT, "Gui")
SETTINGS_FILE = os.path.join(GUI_FOLDER, "gui_settings.json")

if not os.path.isdir(PROJECT_ROOT):
    raise RuntimeError(f"Specify the actual PROJECT_ROOT using the file manager {PROJECT_ROOT} does not exist.")
if not os.path.isdir(DOWNLOAD_FOLDER):
    raise RuntimeError(f"Specify the actual Download Folder using the file manager {DOWNLOAD_FOLDER} does not exist.")
if not os.path.isdir(GUI_FOLDER):
    raise RuntimeError(f"Specify the actual GUI Folder using the file manager {GUI_FOLDER} does not exist.")


def delete_settings_if_there():
    global SETTINGS_FILE
    if os.path.isfile(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)


class GUIHelpers(TestCase):

    def tearDown(self) -> None:
        delete_settings_if_there()

    def setUp(self) -> None:
        delete_settings_if_there()
        self.settings_virgin = {
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

        self.settings_download = {
            "state_of_combobox": 2,
            "source": DOWNLOAD_FOLDER,
            "destination": DOWNLOAD_FOLDER,
            "silent_threshold": 0.03,
            "sounded_speed": 1.00,
            "silent_speed": 5.00,
            "frame_margin": 1,
            "sample_rate": 44100.0,
            "frame_rate": 30.0,
            "frame_quality": 3
        }

        self.settings_tampered = {
            "state_of_combobox": 2,
            "source": "C:\\",
            "destination": "C:\\",
            "silent_threshold": 0.03,
            "sounded_speed": 1.00,
            "silent_speed": 5.00,
            "frame_margin": 1,
            "sample_rate": 44100.0,
            "frame_rate": 30.0,
            "frame_quality": 3
        }

    def test_get_download_folder(self):
        global DOWNLOAD_FOLDER
        download_folder = J_gui.get_download_folder()
        print(f"Download-Folder is: '{download_folder}'")
        self.assertEqual(download_folder, DOWNLOAD_FOLDER,
                         msg=f"download_folder is {download_folder} instead of {DOWNLOAD_FOLDER}")

    def json_load_settings_test_helper(self, save, expected):
        with open(SETTINGS_FILE, "w+") as settings_file:
            json.dump(save, settings_file)
        loaded_settings = J_gui.load_settings()
        self.assertEqual(loaded_settings, expected,
                         msg=f"the settingsfiles should be indifferent :C\n"
                             f"loaded:\n"
                             f"{loaded_settings}\n\n"
                             f"actual:\n"
                             f"{expected}")

    def test_load_settings_virgin(self):
        self.json_load_settings_test_helper(self.settings_virgin, self.settings_download)

    def test_load_settings_tampered(self):
        self.json_load_settings_test_helper(self.settings_tampered, self.settings_tampered)

    def test_save_gui_settings(self):
        # TODO add test
        pass


class GUI_PopUps(TestCase):

    def test_save_file(self):
        # TODO add test
        pass

    def test_choose_file(self):
        # TODO add test
        pass

    def test_choose_directory(self):
        # TODO add test
        pass

    def test_create_warning_popup(self):
        # TODO add test
        pass


class GUI_Hardcore(TestCase):
    def test_initiate_gui(self):
        # TODO add test
        pass

    def test_jumpcutter_gui(self):
        # TODO add test
        pass
