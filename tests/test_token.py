# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

from SuperQQBot import Token
from SuperQQBot.core import logging
from tests import test_config

logger = logging.get_logger()

test_params_ = test_config["token"]
APP_ID = test_params_["appid"]
CLIENT_SECRET = test_params_["token"]


class TokenTestCase(unittest.TestCase):

    def setUp(self):
        self.token = Token(APP_ID, CLIENT_SECRET)

    def test_init(self):
        self.assertEqual(self.token.appId, APP_ID)
        self.assertEqual(self.token.client_secret, CLIENT_SECRET)
        self.assertIsNotNone(self.token.access_token)
        self.assertIsNotNone(self.token.active_time)
        self.assertIsNotNone(self.token.start)

    def test_validate_access_token(self):
        self.assertTrue(self.token.validate_access_token())

    def test_get_access_token_valid(self):
        access_token = self.token.get_access_token()
        self.assertIsNotNone(access_token)

    def test_get_access_token_expired(self):
        # Mock the current time to make the token appear expired
        with patch('time.time', return_value=self.token.start + self.token.active_time + 1):
            access_token = self.token.get_access_token()
            self.assertIsNotNone(access_token)

    def test_is_access_token_activity(self):
        self.assertTrue(self.token.is_access_token_activity())

    def test_renew_access_token(self):
        # Mock the current time to make the token appear expired
        with patch('time.time', return_value=self.token.start + self.token.active_time + 1):
            new_access_token = self.token.renew_access_token()
            self.assertIsInstance(new_access_token, str)
            self.assertGreater(len(new_access_token), 0)


if __name__ == "__main__":
    unittest.main()
