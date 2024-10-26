# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from SuperQQBot.core import logging
from SuperQQBot import BotSendReceiveAPI, Token
from tests import test_config

logger = logging.get_logger()

token = Token(test_config["token"]["appid"], test_config["token"]["token"])
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

class APITestCase(unittest.TestCase):
    async def setUp(self):
        self.access_token = token.get_access_token()
        self.bot_api = BotSendReceiveAPI(self.access_token, IS_SANDBOX)

    @patch('SuperQQBot.WebSocketAPI.get_wss_url')
    async def test_get_wss_url(self, mock_get_wss_url):
        expected_url = 'wss://example.com'
        mock_get_wss_url.return_value = expected_url

        url = self.bot_api.get_wss_url()

        self.assertEqual(url, expected_url)
        mock_get_wss_url.assert_called_once()

    @patch('SuperQQBot.GuildManagementApi.get_guild')
    async def test_get_guild(self, mock_get_guild):
        expected_guild = MagicMock()
        mock_get_guild.return_value = expected_guild

        guild = self.bot_api.get_guild(GUILD_ID)

        self.assertEqual(guild, expected_guild)
        mock_get_guild.assert_called_once_with(GUILD_ID)

    @patch('SuperQQBot.MessageSendReceiveAPI.post_channel_messages')
    async def test_post_channel_messages(self, mock_post_channel_messages):
        content = 'test content'
        expected_response = MagicMock()
        mock_post_channel_messages.return_value = expected_response

        response = self.bot_api.post_channel_messages(CHANNEL_ID, content=content)

        self.assertEqual(response, expected_response)
        mock_post_channel_messages.assert_called_once_with(CHANNEL_ID, content=content)

    @patch('SuperQQBot.GuildManagementApi.get_channels')
    async def test_get_channels(self, mock_get_channels):
        expected_channels = [MagicMock()]
        mock_get_channels.return_value = expected_channels

        channels = self.bot_api.get_channels(GUILD_ID)

        self.assertEqual(channels, expected_channels)
        mock_get_channels.assert_called_once_with(GUILD_ID)

    @patch('SuperQQBot.GuildManagementApi.me')
    async def test_me(self, mock_me):
        expected_user = MagicMock()
        mock_me.return_value = expected_user

        user = self.bot_api.me()

        self.assertEqual(user, expected_user)
        mock_me.assert_called_once()

    @patch('SuperQQBot.GuildManagementApi.me_guilds')
    async def test_me_guilds(self, mock_me_guilds):
        expected_guilds = [MagicMock()]
        mock_me_guilds.return_value = expected_guilds

        guilds = self.bot_api.me_guilds()

        self.assertEqual(guilds, expected_guilds)
        mock_me_guilds.assert_called_once()

    @patch('SuperQQBot.GuildManagementApi.get_channel')
    async def test_get_channel(self, mock_get_channel):
        expected_channel = MagicMock()
        mock_get_channel.return_value = expected_channel

        channel = self.bot_api.get_channel(CHANNEL_ID)

        self.assertEqual(channel, expected_channel)
        mock_get_channel.assert_called_once_with(CHANNEL_ID)

    @patch('SuperQQBot.GuildManagementApi.create_channel')
    async def test_create_channel(self, mock_create_channel):
        expected_channel = AsyncMock()
        mock_create_channel.return_value = expected_channel

        channel = self.bot_api.create_channel(GUILD_ID, position=1, name="Test Channel")

        self.assertEqual(channel, expected_channel)
        mock_create_channel.assert_called_once_with(GUILD_ID, position=1, name="Test Channel")

    @patch('SuperQQBot.GuildManagementApi.update_channel')
    async def test_update_channel(self, mock_update_channel):
        expected_channel = MagicMock()
        mock_update_channel.return_value = expected_channel

        channel = self.bot_api.update_channel(CHANNEL_ID, name="Updated Channel")

        self.assertEqual(channel, expected_channel)
        mock_update_channel.assert_called_once_with(CHANNEL_ID, name="Updated Channel")

    @patch('SuperQQBot.GuildManagementApi.delete_channel')
    async def test_delete_channel(self, mock_delete_channel):
        await self.bot_api.delete_channel(CHANNEL_ID)

        mock_delete_channel.assert_called_once_with(CHANNEL_ID)

    @patch('SuperQQBot.MessageSendReceiveAPI.post_dms')
    async def test_post_dms(self, mock_post_dms):
        expected_response = MagicMock()
        mock_post_dms.return_value = expected_response

        response = self.bot_api.post_dms(GUILD_OWNER_ID, msg_type=0, content="Hello")

        self.assertEqual(response, expected_response)
        mock_post_dms.assert_called_once_with(GUILD_OWNER_ID, msg_type=0, content="Hello")

    @patch('SuperQQBot.MessageSendReceiveAPI.post_group_message')
    async def test_post_group_message(self, mock_post_group_message):
        expected_response = MagicMock()
        mock_post_group_message.return_value = expected_response

        response = self.bot_api.post_group_message(GUILD_ID, msg_type=0, content="Hello Group")

        self.assertEqual(response, expected_response)
        mock_post_group_message.assert_called_once_with(GUILD_ID, msg_type=0, content="Hello Group")

    @patch('SuperQQBot.MessageSendReceiveAPI.post_c2c_file')
    async def test_post_c2c_file(self, mock_post_c2c_file):
        expected_response = MagicMock()
        mock_post_c2c_file.return_value = expected_response

        response = self.bot_api.post_c2c_file(GUILD_OWNER_ID, file_type=1, url="http://example.com/image.jpg", srv_send_msg=True)

        self.assertEqual(response, expected_response)
        mock_post_c2c_file.assert_called_once_with(GUILD_OWNER_ID, file_type=1, url="http://example.com/image.jpg", srv_send_msg=True)

    @patch('SuperQQBot.MessageSendReceiveAPI.post_group_file')
    async def test_post_group_file(self, mock_post_group_file):
        expected_response = MagicMock()
        mock_post_group_file.return_value = expected_response

        response = self.bot_api.post_group_file(GUILD_ID, file_type=1, url="http://example.com/image.jpg", srv_send_msg=True)

        self.assertEqual(response, expected_response)
        mock_post_group_file.assert_called_once_with(GUILD_ID, file_type=1, url="http://example.com/image.jpg", srv_send_msg=True)

    @patch('SuperQQBot.MessageSendReceiveAPI.recall_c2c_message')
    async def test_recall_c2c_message(self, mock_recall_c2c_message):
        await self.bot_api.recall_c2c_message(GUILD_OWNER_ID, MESSAGE_ID)

        mock_recall_c2c_message.assert_called_once_with(GUILD_OWNER_ID, MESSAGE_ID)

    @patch('SuperQQBot.MessageSendReceiveAPI.recall_group_message')
    async def test_recall_group_message(self, mock_recall_group_message):
        await self.bot_api.recall_group_message(GUILD_ID, MESSAGE_ID)

        mock_recall_group_message.assert_called_once_with(GUILD_ID, MESSAGE_ID)

    @patch('SuperQQBot.MessageSendReceiveAPI.recall_channel_message')
    async def test_recall_channel_message(self, mock_recall_channel_message):
        await self.bot_api.recall_channel_message(CHANNEL_ID, MESSAGE_ID)

        mock_recall_channel_message.assert_called_once_with(CHANNEL_ID, MESSAGE_ID)

    @patch('SuperQQBot.MessageSendReceiveAPI.recall_dms_message')
    async def test_recall_dms_message(self, mock_recall_dms_message):
        await self.bot_api.recall_dms_message(GUILD_ID, MESSAGE_ID)

        mock_recall_dms_message.assert_called_once_with(GUILD_ID, MESSAGE_ID)

    @patch('SuperQQBot.MessageExpressionInteraction.send_reaction_expression')
    async def test_send_reaction_expression(self, mock_send_reaction_expression):
        emoji = MagicMock(type=1, id="emoji_id")
        await self.bot_api.send_reaction_expression(CHANNEL_ID, MESSAGE_ID, emoji)

        mock_send_reaction_expression.assert_called_once_with(CHANNEL_ID, MESSAGE_ID, emoji)

    @patch('SuperQQBot.MessageExpressionInteraction.delete_reaction_expression')
    async def test_delete_reaction_expression(self, mock_delete_reaction_expression):
        emoji = MagicMock(type=1, id="emoji_id")
        await self.bot_api.delete_reaction_expression(CHANNEL_ID, MESSAGE_ID, emoji)

        mock_delete_reaction_expression.assert_called_once_with(CHANNEL_ID, MESSAGE_ID, emoji)

    @patch('SuperQQBot.MessageExpressionInteraction.get_reaction_users')
    async def test_get_reaction_users(self, mock_get_reaction_users):
        emoji = MagicMock(type=1, id="emoji_id")

        expected_response = MagicMock()
        mock_get_reaction_users.return_value = expected_response

        response = self.bot_api.get_reaction_users(CHANNEL_ID, MESSAGE_ID, emoji)

        self.assertEqual(response, expected_response)
        mock_get_reaction_users.assert_called_once_with(CHANNEL_ID, MESSAGE_ID, emoji)

if __name__ == "__main__":
    unittest.main()
