import json
import os
from unittest import TestCase, skip, expectedFailure

import Gui.jumpcutterGui as J_gui

# constants


PROJECT_ROOT = os.path.normpath(os.path.join(__file__, '..', '..'))
DOWNLOAD_FOLDER = r"C:\Users\frank\Downloads"
GUI_FOLDER = os.path.join(PROJECT_ROOT, "Gui")
SETTINGS_FILE = os.path.join(GUI_FOLDER, "gui_settings.json")
TESTS_FOLDER = os.path.join(PROJECT_ROOT, "tests")
FOOTAGE_FOLDER = os.path.join(TESTS_FOLDER, "Footage")
SELECT_ME_FILE = os.path.join(FOOTAGE_FOLDER, "select_me.txt")

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
                         msg=f"the Settings-Files should be indifferent :(")

    def test_load_settings_virgin(self):
        self.json_load_settings_test_helper(self.settings_virgin, self.settings_download)

    def test_load_settings_tampered(self):
        self.json_load_settings_test_helper(self.settings_tampered, self.settings_tampered)

    def save_gui_settings_helper(self, expected, settings=None):
        if settings is None:
            J_gui.save_gui_settings()
        else:
            J_gui.save_gui_settings(settings)
        with open(SETTINGS_FILE, "r") as settings_file:
            loaded_settings = json.load(settings_file)
        self.assertEqual(loaded_settings, expected,
                         msg=f"the Settings-Files should be indifferent :(")

    def test_save_gui_settings_none(self):
        self.save_gui_settings_helper(self.settings_download)

    def test_save_gui_settings(self):
        self.save_gui_settings_helper(self.settings_download, settings=self.settings_download)
        self.save_gui_settings_helper(self.settings_download, settings=self.settings_download)
        self.save_gui_settings_helper(self.settings_tampered, settings=self.settings_tampered)


class GuiPopUps(TestCase):

    @skip("gui tests apparrently are really anoying")
    def test_save_file(self):
        # todo debug, why these things dont Pop-Up
        self.assertEqual(PROJECT_ROOT, J_gui.save_file(PROJECT_ROOT, "save Nothing"),
                         msg="you should have saved Nothing")
        self.assertEqual(SELECT_ME_FILE, J_gui.save_file(FOOTAGE_FOLDER, f"save {SELECT_ME_FILE}"),
                         msg=f"you should have chosen {SELECT_ME_FILE}")

    @skip("gui tests apparrently are really anoying")
    def test_choose_file(self):
        # todo debug, why these things dont Pop-Up
        self.assertEqual(PROJECT_ROOT, J_gui.choose_file(PROJECT_ROOT, "select Nothing"),
                         msg="you should have chosen Nothing")
        self.assertEqual(SELECT_ME_FILE, J_gui.choose_file(FOOTAGE_FOLDER, f"select {SELECT_ME_FILE}"),
                         msg=f"you should have chosen {SELECT_ME_FILE}")

    @skip("gui tests apparrently are really anoying")
    def test_choose_directory(self):
        # todo debug, why these things dont Pop-Up
        self.assertEqual(PROJECT_ROOT, J_gui.choose_directory(PROJECT_ROOT, "select Nothing"),
                         msg="you should have chosen Nothing")
        self.assertEqual(FOOTAGE_FOLDER, J_gui.choose_directory(TESTS_FOLDER, f"select {FOOTAGE_FOLDER}"),
                         msg=f"you should have chosen {FOOTAGE_FOLDER}")

    @skip("gui tests apparrently are really anoying to implement")
    def test_create_warning_popup(self):
        # todo debug, why these things dont Pop-Up
        J_gui.create_warning_popup("Intended Popup")
        self.assertEqual(input("did a popup show up? (y/n)").lower(), "y")


class GuiHardcore(TestCase):

    @skip("gui tests apparrently are really anoying to use")
    @expectedFailure()
    def test_initiate_gui(self):
        J_gui.initiate_gui()
