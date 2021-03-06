# -*- coding: utf-8 -*-

import os
import unittest

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


from themetail import config


CLIENT_WITHOUT_PASSWORD = """
[client]
email: example@example.com
"""


CLIENT_WITHOUT_EMAIL = """
[client]
password: foobar
"""

CLIENT_WITHOUT_EITHER = """
[client]
"""

WITH_ALL = """
[client]
email: example@example.com
password: foobar
"""


class TestConfig(unittest.TestCase):
    def generate_conf(self, string):
        string = string.strip()
        fp = StringIO()
        fp.write(string)
        fp.seek(0)
        conf = config.load_fp(fp)
        return conf

    def test_exit_without_conf(self):
        config._conf = None

        envvar = config.CONF_ENV_VARIABLE
        backup = os.getenv(envvar)
        os.environ[envvar] = ''
        self.assertRaises(SystemExit, config.load)

        if backup is None:
            os.unsetenv(envvar)
        else:
            os.environ[envvar] = backup

    def test_client_section_validation(self):
        without_password = self.generate_conf(CLIENT_WITHOUT_PASSWORD)
        without_email = self.generate_conf(CLIENT_WITHOUT_EMAIL)
        without_either = self.generate_conf(CLIENT_WITHOUT_EITHER)
        with_all = self.generate_conf(WITH_ALL)

        validator = config.is_valid_client_section
        self.assertFalse(validator(without_password))
        self.assertFalse(validator(without_email))
        self.assertFalse(validator(without_either))
        self.assertTrue(validator(with_all))
