from .Error import WrongArgs
from .connection import PostConnect, GetConnect
from . import Error
from SuperQQBot.core.types import *
from . import logging
from time import time
import asyncio

_log = logging.get_logger()


# AccessToken类
class Token:
    def __init__(self, appId: str, client_secret: str):
        self.appId = appId
        self.client_secret = client_secret
        self.access_token = None
        self.active_time = None
        self.start = float()
        self.renew_access_token()

    def validate_access_token(self) -> bool:
        return self.access_token is not None and self.active_time is not None

    def get_access_token(self) -> str:
        if not self.validate_access_token():
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

# 基类，用于公共部分的继承
class BaseBotApi:
    """API基类"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        self.access_token = access_token
        self.public_url = "https://sandbox.api.sgroup.qq.com" \
            if is_sandbox else "https://api.sgroup.qq.com/"

# WebSocket相关API
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
        """获取频道详情
        :param guild_id: 频道ID
        :rtype: Guild
        :return: guild_id 指定的频道的详情。"""
        response = GetConnect(f"/guilds/{guild_id}", self.access_token, self.public_url).json()
        return Guild(**response)

    async def get_channel_list(self, guild_id: str | int | Guild) -> List[Channel]:
        """获取子频道列表
        :param guild_id: 频道ID
        :rtype: List[Channel]
        :return: guild_id 指定的频道下的子频道列表。"""
        output = []
        response = GetConnect(f"/guilds/{guild_id}/channels", self.access_token, self.public_url).json()
        for i in response:
            output.append(Channel(**i))
        return output

    async def me(self) -> User:
        """获取用户详情。
        :rtype: User
        :return: 当前用户（机器人）详细"""
        response = GetConnect("/users/@me", self.access_token, self.public_url).json()
        return User(**response)

    async def me_guild(self) -> List[Guild]:
        """获取用户频道列表
        :return: 当前用户（机器人）所加入的频道列表
        :rtype: List[Guild}"""
        output = []
        response = GetConnect("/users/@me/guilds", self.access_token, self.public_url).json()
        for i in response:
            output.append(Guild(**i))
        return output
    async def about_channel(self, channel_id: str | int | Channel) -> Channel:
        """获取子频道详情
        :param channel_id: 子频道ID
        :rtype: Channel
        :return: channel_id 指定的子频道的详情。"""
        response = GetConnect(f"/channels/{channel_id}", self.access_token, self.public_url).json()
        return Channel(**response)
    async def create_channel(self,
                             position: int,
                             name:str | None = None,
                             type:ChannelType | None = None,
                             sub_type:ChannelSubType | None = None,
                             parent_id:str | None = None,
                             private_type: PrivateType | None = None,
                             private_user_ids: List[str] | None = None,
                             speak_permission:int | None = None,
                             application_id:str | None = None) -> Channel:
        """创建子频道
        :param name: 子频道名称
        :param type: 子频道类型
        :param sub_type: 子频道子类型（如果type给的不是1这个就得传None）
        :param position: 子频道排序，必填；当子频道类型为 子频道分组（ChannelType=4）时，必须大于等于 2
        :param parent_id: 子频道所属分组ID
        :param private_type: 子频道私密类型
        :param private_user_ids: 子频道私密类型成员 ID
        :param speak_permission: 子频道发言权限
        :param application_id: 应用类型子频道应用 AppID，仅应用子频道需要该字段"""
        if type.type!=0 and sub_type is not None:
            raise (
                UnSupposeUsage("目前只有文字子频道具有 ChannelSubType 二级分类，其他类型频道二级分类"))
        if type.type == 4 and position < 2:
            raise (
                WrongArgs("当子频道类型为 子频道分组（ChannelType=4）时，必须大于等于 2"))


class BotAPI(WebSocketAPI, GuildManagementApi):
    """便于用户快速调用所有API，这是一个通用接口"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
