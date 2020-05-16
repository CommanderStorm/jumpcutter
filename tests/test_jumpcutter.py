import os
from unittest import TestCase

import jumpcutter as j
from jumpcutter import TEMP_TEMP_FOLDER, TEMP_FOLDER, PROJECT_ROOT

TESTS_FOLDER = os.path.join(PROJECT_ROOT, "tests")
FOOTAGE_FOLDER = os.path.join(TESTS_FOLDER, "Footage")


class Helpers(TestCase):
    def help_setup(self, directory):
        if os.path.isdir(directory):
            j.delete_path(directory)
            self.assertFalse(os.path.isdir(directory), msg="directory deletion failed")
        j.create_path(directory)
        self.assertTrue(os.path.isdir(directory), msg="directory creation failed")

    def help_teardown(self, directory):
        if os.path.isdir(directory):
            j.delete_path(directory)
        self.assertFalse(os.path.isdir(directory), msg="directory deletion failed")

    def setUp(self) -> None:
        self.help_setup(TEMP_FOLDER)
        self.help_setup(TEMP_TEMP_FOLDER)

    def tearDown(self) -> None:
        self.help_teardown(TEMP_TEMP_FOLDER)
        self.help_teardown(TEMP_FOLDER)

    def test_get_max_volume(self):
        # TODO add test
        pass

    def test_copy_frame(self):
        # TODO add test
        pass

    def test_input_to_output_filename(self):
        # TODO add test
        pass

    def test_download_file(self):
        # TODO add test
        pass

    def test_count_mp4_files_in_folder(self):
        # TODO add test
        pass

    def test_call_subprocess(self):
        # TODO add test
        pass


class Core(TestCase):
    def test_process(self):
        # TODO add test
        pass

    def test_process_folder(self):
        # TODO add test
        pass

    def test_process_yt(self):
        # TODO add test
        pass

    def test_process_settings(self):
        # TODO add test
        pass
