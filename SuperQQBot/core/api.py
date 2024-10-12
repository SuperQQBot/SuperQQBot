from requests.utils import resolve_proxies

from .connection import PostConnect, GetConnect
from . import Error
import json
from .types import *
from . import log
from time import time
from typing import Type

_log = log.get_logger()

class Token:
    def __init__(self, appId:str, client_secret:str):
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
            raise (
                Error.UnknownAccessToken)
        elif not self.is_access_token_activity():
            return self.renew_access_token()
        else:
            return self.access_token
    def is_access_token_activity(self) -> bool:
        return time() - self.start < self.active_time
    def renew_access_token(self):
        self.start = time() + 1
        response = PostConnect(function="/app/getAppAccessToken",
                               json={"appId": self.appId, "clientSecret": self.client_secret},
                               access_token="",
                               url="https://bots.qq.com")
        if response.is_error():
            if response.error_reason() == "internal err":
                raise (
                    Error.IPNotInWhiteList)
            elif response.error_code() == 100007:
                raise (
                    Error.UnknownAppId(self.appId))
            elif response.error_reason() == 'invalid appid or secret':
                raise (
                    Error.AppIdAndSecretDoNotMatch)
            else:
                raise (
                    Error.UnknownError(response.text))

        else:
            response = response.json()
            try:
                self.access_token = response["access_token"]
                self.active_time = int(response["expires_in"])
            except KeyError:
                raise (
                    Error.UnknownError(response))
            _log.info(f"[QQBot]AccessToken存活时间：{self.active_time}")
            return self.access_token


class BaseBotApi:
    """API基类"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        self.access_token = access_token
        self.public_url = "https://sandbox.api.sgroup.qq.com" \
            if is_sandbox else "https://api.sgroup.qq.com/"

# WebSocket模块API
class WebSocketAPI(BaseBotApi):
    """WebSocket相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def get_wss_url(self) -> str:
        response = GetConnect("/gateway", self.access_token, self.public_url).json()
        return response["url"]

# 频道模块API
class GuildManagementApi(BaseBotApi):
    """频道管理相关API"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
    async def about_guild(self, guild_id: str | int | Guild) -> Guild:
        response = GetConnect(f"/guilds/{guild_id}", self.access_token, self.public_url).json()
        return Guild(**response)

    async def get_channel_list(self, guild_id: str | int | Guild) -> List[Channel]:
        output = list()
        response = GetConnect(f"/guilds/{guild_id}/channels", self.access_token, self.public_url).json()
        for i in response:
            output.append(Channel(**i))
        return output
    async def me(self) -> User:
        response = GetConnect("/users/@me", self.access_token, self.public_url).json()
        return User(**response)

    async def me_guild(self) -> List[Guild]:
        output = list()
        response = GetConnect("/users/@me/guilds", self.access_token, self.public_url).json()
        for i in response:
            output.append(Guild(**i))
        return output

# 通用接口
class BotAPI(GuildManagementApi, WebSocketAPI):
    """便于用户快速调用所有API，这是一个通用接口"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)