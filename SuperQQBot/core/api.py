from .connection import PostConnect, GetConnect
from . import Error
from SuperQQBot.core.types import *
from . import logging
from time import time

_log = logging.get_logger()

class Token:
    def __init__(self, appId: str, client_secret: str):
        self.appId = appId
        self.client_secret = client_secret
        self.access_token = None
        self.active_time = None
        self.start = float()
        self.renew_access_token()

    def validate_accessToken(self) -> bool:
        return self.access_token is not None and self.active_time is not None

    def get_access_token(self) -> str:
        if not self.validate_accessToken():
            raise Error.UnknownAccessToken()
        elif not self.is_access_token_activity():
            return self.renew_access_token()
        else:
            return self.access_token

    def is_access_token_activity(self) -> bool:
        return time() - self.start < self.active_time

    def renew_access_token(self):
        self.start = time()
        response = PostConnect(function="/app/getAppAccessToken", access_token="",
                               json={"appId": self.appId, "clientSecret": self.client_secret},
                               url="https://bots.qq.com")
        if response.is_error():
            if response.error_reason() == "internal err":
                raise Error.IPNotInWhiteList()
            elif response.error_code() == 100007:
                raise Error.UnknownAppId(self.appId)
            elif response.error_reason() == 'invalid appid or secret':
                raise Error.AppIdAndSecretDoNotMatch()
            else:
                raise Error.UnknownError(response.text)

        else:
            response = response.json()
            try:
                self.access_token = response["access_token"]
                self.active_time = int(response["expires_in"])
            except KeyError:
                raise Error.UnknownError(response)
            _log.info(f"[QQBot]AccessToken存活时间：{self.active_time}")
            return self.access_token


class BaseBotApi:
    """API基类"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        self.access_token = access_token
        self.public_url = "https://sandbox.api.sgroup.qq.com" \
            if is_sandbox else "https://api.sgroup.qq.com/"


class WebSocketAPI(BaseBotApi):
    """WebSocket相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def get_wss_url(self) -> str:
        response = GetConnect("/gateway", self.access_token, self.public_url).json()
        return response["url"]


class GuildManagementApi(BaseBotApi):
    """频道管理相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def about_guild(self, guild_id: str | int | Guild) -> Guild:
        response = GetConnect(f"/guilds/{guild_id}", self.access_token, self.public_url).json()
        return Guild(**response)

    async def get_channel_list(self, guild_id: str | int | Guild) -> List[Channel]:
        output = []
        response = GetConnect(f"/guilds/{guild_id}/channels", self.access_token, self.public_url).json()
        for i in response:
            output.append(Channel(**i))
        return output

    def me(self) -> User:
        response = GetConnect("/users/@me", self.access_token, self.public_url).json()
        return User(**response)

    async def me_guild(self) -> List[Guild]:
        output = []
        response = GetConnect("/users/@me/guilds", self.access_token, self.public_url).json()
        for i in response:
            output.append(Guild(**i))
        return output


class MessageManagementApi(BaseBotApi):
    """消息管理相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def send_direct_message(self, recipient_id: str, message: str) -> DirectMessage:
        payload = {"recipient_id": recipient_id, "content": message}
        response = PostConnect("/directmessages", self.access_token, payload).json()
        return DirectMessage(**response)

    async def send_group_message(self, group_id: str, message: str) -> GroupMessage:
        payload = {"target": group_id, "content": message}
        response = PostConnect("/channels/messages", self.access_token, payload).json()
        return GroupMessage(**response)

    async def send_c2c_message(self, user_id: str, message: str) -> C2CMessage:
        payload = {"target": user_id, "content": message}
        response = PostConnect("/channels/messages", self.access_token, payload).json()
        return C2CMessage(**response)


class InteractionApi(BaseBotApi):
    """交互相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def handle_interaction(self, interaction_id: str, interaction_token: str, data: Dict[str, Any]) -> Interaction:
        payload = {"interaction_id": interaction_id, "interaction_token": interaction_token, **data}
        response = PostConnect("/interactions", self.access_token, payload).json()
        return Interaction(**response)


class MessageAuditApi(BaseBotApi):
    """消息审核相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def audit_message(self, message_id: str, result: bool, reason: Optional[str] = None) -> MessageAudit:
        payload = {"message_id": message_id, "result": result, "reason": reason}
        response = PostConnect("/messages/audit", self.access_token, payload).json()
        return MessageAudit(**response)


class ForumManagementApi(BaseBotApi):
    """论坛管理相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def create_forum_thread(self, channel_id: str, title: str, content: str, formate:int) -> ForumThread:
        payload = {"title": title, "content": content, "format": formate}
        response = PostConnect(f"/channels/{channel_id}/threads", self.access_token, payload).json()
        return ForumThread(**response)

    async def publish_forum_post(self, thread_id: str, content: str) -> ForumPost:
        payload = {"thread_id": thread_id, "content": content}
        response = PostConnect("/forum/posts", self.access_token, json=payload, url=self.public_url).json()
        return ForumPost(**response)

    async def publish_forum_reply(self, post_id: str, content: str) -> ForumReply:
        payload = {"post_id": post_id, "content": content}
        response = PostConnect("/forum/replies", self.access_token, payload).json()
        return ForumReply(**response)

    async def audit_forum_publish(self, thread_id: str, result: bool, reason: Optional[str] = None) -> ForumPublishAudit:
        payload = {"thread_id": thread_id, "result": result, "reason": reason}
        response = PostConnect("/forum/publish/audit", self.access_token, payload).json()
        return ForumPublishAudit(**response)


class AudioActionApi(BaseBotApi):
    """音频操作相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def start_audio(self, channel_id: str, duration: int) -> AudioAction:
        payload = {"channel_id": channel_id, "action": "start", "duration": duration}
        response = PostConnect("/audio/actions", self.access_token, payload).json()
        return AudioAction(**response)

    async def stop_audio(self, channel_id: str) -> AudioAction:
        payload = {"channel_id": channel_id, "action": "stop"}
        response = PostConnect("/audio/actions", self.access_token, payload).json()
        return AudioAction(**response)


class PublicMessageApi(BaseBotApi):
    """公开消息相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def send_public_message(self, channel_id: str, message: str) -> PublicMessage:
        payload = {"channel_id": channel_id,
                    "content": message}
        response = PostConnect("/public/messages", self.access_token, payload).json()
        return PublicMessage(**response)

    async def delete_public_message(self, message_id: str) -> bool:
        response = PostConnect(f"/public/messages/{message_id}", self.access_token, payload).json()
        return response.get("success", False)


class BotAPI(GuildManagementApi, WebSocketAPI, MessageManagementApi, InteractionApi, MessageAuditApi, ForumManagementApi, AudioActionApi, PublicMessageApi):
    """便于用户快速调用所有API，这是一个通用接口"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
