import errno
import os
import tempfile
import unittest
from unittest import mock

import Config


class InvalidCookieTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cookie_path = Config.cookie_path
        Config.cookie_path = os.path.join(self.temp_dir.name, 'cookie.txt')
        self.color_print = mock.patch.object(Config, '__color_print').start()

    def tearDown(self):
        mock.patch.stopall()
        Config.cookie_path = self.original_cookie_path
        self.temp_dir.cleanup()

    @property
    def invalid_cookie_path(self):
        return os.path.join(self.temp_dir.name, 'invalid_cookie.txt')

    def write_cookie(self, value=b'BAHARUNE=invalid-cookie'):
        with open(Config.cookie_path, 'wb') as cookie_file:
            cookie_file.write(value)

    def test_regular_file_is_atomically_renamed(self):
        self.write_cookie()
        with open(self.invalid_cookie_path, 'wb') as invalid_cookie_file:
            invalid_cookie_file.write(b'older-cookie')
        Config.cookie = {'BAHARUNE': 'invalid-cookie'}

        Config.invalid_cookie()

        self.assertFalse(os.path.exists(Config.cookie_path))
        with open(self.invalid_cookie_path, 'rb') as invalid_cookie_file:
            self.assertEqual(invalid_cookie_file.read(), b'BAHARUNE=invalid-cookie')
        self.assertIsNone(Config.cookie)

    def test_bind_mount_busy_error_copies_then_clears_source(self):
        self.write_cookie()
        with open(self.invalid_cookie_path, 'wb') as invalid_cookie_file:
            invalid_cookie_file.write(b'older-cookie')

        busy_error = OSError(errno.EBUSY, 'Device or resource busy')
        with mock.patch.object(Config.os, 'replace', side_effect=busy_error):
            Config.invalid_cookie()

        with open(Config.cookie_path, 'rb') as cookie_file:
            self.assertEqual(cookie_file.read(), b'')
        with open(self.invalid_cookie_path, 'rb') as invalid_cookie_file:
            self.assertEqual(invalid_cookie_file.read(), b'BAHARUNE=invalid-cookie')

    def test_second_busy_invalidation_does_not_erase_saved_cookie(self):
        self.write_cookie()
        busy_error = OSError(errno.EBUSY, 'Device or resource busy')
        with mock.patch.object(Config.os, 'replace', side_effect=busy_error):
            Config.invalid_cookie()
            Config.invalid_cookie()

        with open(self.invalid_cookie_path, 'rb') as invalid_cookie_file:
            self.assertEqual(invalid_cookie_file.read(), b'BAHARUNE=invalid-cookie')


if __name__ == '__main__':
    unittest.main()
