# -*- coding: utf-8 -*-
import unittest
from SuperQQBot.core import logging
from SuperQQBot import Intents
from tests import test_config

logger = logging.get_logger()

test_params_ = test_config["test_params"]
GUILD_ID = test_params_["guild_id"]
GUILD_OWNER_ID = test_params_["guild_owner_id"]
GUILD_OWNER_NAME = test_params_["guild_owner_name"]
GUILD_TEST_MEMBER_ID = test_params_["guild_test_member_id"]
CHANNEL_ID = test_params_["channel_id"]
CHANNEL_NAME = test_params_["channel_name"]
ROBOT_NAME = test_params_["robot_name"]
IS_SANDBOX = test_params_["is_sandbox"]
MESSAGE_ID = test_params_["message_id"]

class IntentsTestCase(unittest.TestCase):

    def test_init_default(self):
        intents = Intents()
        self.assertEqual(intents.value, Intents.DEFAULT_VALUE)
        self.assertFalse(any(intents.intents.values()))

    def test_init_with_kwargs(self):
        intents = Intents(GUILDS=True, GUILD_MESSAGES=True)
        self.assertTrue(intents.intents['GUILDS'])
        self.assertTrue(intents.intents['GUILD_MESSAGES'])
        self.assertFalse(intents.intents['GUILD_MEMBERS'])
        self.assertEqual(intents.value, Intents._GUILDS_BIT | Intents._GUILD_MESSAGES_BIT)

    def test_init_invalid_flag(self):
        with self.assertRaises(TypeError):
            Intents(INVALID_FLAG=True)

    def test_all(self):
         intents = Intents.all()
         self.assertTrue(all(intents.intents.values()))
         self.assertEqual(intents.value, 2113934851)


    def test_none(self):
        intents = Intents.none()
        self.assertFalse(any(intents.intents.values()))
        self.assertEqual(intents.value, Intents.DEFAULT_VALUE)

    def test_default(self):
        intents = Intents.default()
        self.assertTrue(intents.intents['GUILDS'])
        self.assertTrue(intents.intents['GUILD_MEMBERS'])
        self.assertTrue(intents.intents['PUBLIC_GUILD_MESSAGES'])
        expected_value = Intents._GUILDS_BIT | Intents._GUILD_MEMBERS_BIT | Intents._PUBLIC_GUILD_MESSAGES_BIT
        self.assertEqual(intents.value, expected_value)

    def test_set_intent_valid(self):
        intents = Intents()
        intents.set_intent('GUILDS', True)
        self.assertTrue(intents.intents['GUILDS'])
        self.assertEqual(intents.value, Intents._GUILDS_BIT)

    def test_set_intent_invalid(self):
        intents = Intents()
        with self.assertRaises(TypeError):
            intents.set_intent('INVALID_FLAG', True)

    def test_update_bitwise_value(self):
        intents = Intents()
        intents.intents['GUILDS'] = True
        intents.intents['GUILD_MESSAGES'] = True
        intents._update_bitwise_value()
        self.assertEqual(intents.value, Intents._GUILDS_BIT | Intents._GUILD_MESSAGES_BIT)

if __name__ == "__main__":
    unittest.main()
