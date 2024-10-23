from .Error import WrongArgs, ParameterMappingFailed
from .connection import PostConnect, GetConnect
from .types import Guild
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

    def me(self) -> User:
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
                             guild_id : str | int | Guild,
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
        data = {
            "name": name,
            "type": type.type,
            "sub_type": sub_type.type if sub_type else None,
            "position": position,
            "parent_id": parent_id,
            "private_type": private_type.type if private_type else None,
            "private_user_ids": private_user_ids,
            "speak_permission": speak_permission,
            "application_id": application_id
        }
        return Channel(**PostConnect(f"/guilds/{guild_id}/channels", self.access_token, data, self.public_url).json())
    async def patch_channel(self,
                             channel_id: str | int | Channel,
                             name : str | None = None,
                             position: int | None = None,
                             parent_id: str | None = None,
                             private_type: PrivateType | None = None,
                             speak_permission: SpeakPermission | None = None) -> Channel:
        """删除子频道
        :param channel_id: 子频道ID
        :param name: 子频道名
        :param position: 排序
        :param parent_id: 分组 id
        :param private_type: 子频道私密类型 PrivateType
        :param speak_permission: 子频道发言权限 SpeakPermission
        :return: 返回Channel 对象
        需要修改哪个字段，就传递哪个字段即可。"""
        if name is not None:
            data = {"name" : name}
        elif position is not None:
            data = {"position" : position}
        elif parent_id is not None:
            data = {"parent_id" : parent_id}
        elif private_type is not None:
            data = {"private_type" : private_type.type}
        elif speak_permission is not None:
            data = {"speak_permission" : speak_permission.type}
        else:
            raise (
                WrongArgs("没有要修改的参数"))
        return Channel(
            **PostConnect(
                f"/channels/{channel_id}",
                self.access_token, data,
                self.public_url)
            .json())
    async def delete_channel(self, channel_id: str | int | Channel) -> None:
        """删除子频道
        :param channel_id: 子频道ID"""
        PostConnect(f"/channels/{channel_id}", self.access_token, {}, self.public_url).verify_data()
        return
class MessageAPI(BaseBotApi):
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
    async def post_dms(self,
                       openid: str,
                       msg_type: MessageType,
                       content: str | None = None,
                       makedown: MakeDown | None = None,
                       keyboard: Keyboard | None = None,
                       ark: Ark | None = None,
                       media: Media_C2C | None = None,
                       message_reference : Optional[Any] = None,
                       event_id: str | None = None,
                       msg_id : str | None = None,
                       msg_seq : int | None = None
                       ) -> C2C_Message_Info:
        """单独发动消息给用户。
        :param openid: 	QQ 用户的 openid，可在各类事件中获得。
        :param content: 文本内容
        :param msg_type: 消息类型：0 是文本，2 是 markdown， 3 ark，4 embed，7 media 富媒体
        :param msg_id: 前置收到的用户发送过来的消息 ID，用于发送被动（回复）消息
        :param makedown: Markdown对象
        :param keyboard: Keyboard对象
        :param ark: Ark对象
        :param media: 富媒体单聊的file_info
        :param message_reference: 【暂未支持】消息引用
        :param event_id: 前置收到的事件 ID，用于发送被动消息，支持事件："INTERACTION_CREATE"、"C2C_MSG_RECEIVE"、"FRIEND_ADD"
        :param msg_seq: 前置收到的用户发送过来的消息 ID，用于发送被动（回复）消息
        """
        data = {
            "content": content,
            "msg_id": msg_id,
            "msg_type": msg_type.type
        }
        if message_reference is not None:
            raise (
                UnSupposeUsage("message_reference"))
        if msg_type.type == 0 and content is None:
            raise (
                ParameterMappingFailed("content", "msg_type", content, msg_type))
        elif msg_type.type == 2 and makedown is None:
            raise (
                ParameterMappingFailed("makedown", "msg_type", makedown, msg_type))
        elif msg_type.type == 3 and ark is None:
            raise (
                ParameterMappingFailed("ark", "msg_type", ark, msg_type))
        elif msg_type.type == 4 and media is None:
            raise (
                ParameterMappingFailed("media", "msg_type", media, msg_type))
        else:
            if msg_type == 0:
                data["content"] = content
            elif msg_type == 2:
                data["makedown"] = makedown.to_dict()
            elif msg_type == 3:
                data["ark"] = ark.to_dict()
            elif msg_type == 4:
                data["media"] = media.to_dict()
        return C2C_Message_Info(**PostConnect(f"/v2/users/{openid}/messages", self.access_token, data, self.public_url).json())
    async def post_channel_messages(self,
                                    channel_id: str | int | Channel,
                                    embed: Optional[MessageEmbed] = None,
                                    content: str | None = None,
                                    makedown: MakeDown | None = None,
                                    ark: Ark | None = None,
                                    message_reference : Optional[Any] = None,
                                    event_id: str | None = None,
                                    image : Optional[str] = None,
                                    msg_id : Optional[str] = None
    ) -> Channel_Message_Info:
        """功能描述
    用于向 channel_id 指定的子频道发送消息。

    要求操作人在该子频道具有发送消息的权限。\n
    主动消息在频道主或管理设置了情况下，按设置的数量进行限频。在未设置的情况遵循如下限制:\n
    主动推送消息，默认每天往每个子频道可推送的消息数是 20 条，超过会被限制。\n
    主动推送消息在每个频道中，每天可以往 2 个子频道推送消息。超过后会被限制。\n
    不论主动消息还是被动消息，在一个子频道中，每 1s 只能发送 5 条消息。\n
    被动回复消息有效期为 5 分钟。超时会报错。\n
    发送消息接口要求机器人接口需要连接到 websocket 上保持在线状态\n
    有关主动消息审核，可以通过 Intents 中审核事件 MESSAGE_AUDIT 返回 MessageAudited 对象获取结果。\n
    :param channel_id: 频道ID
    :param content: 选填，消息内容，文本内容，支持内嵌格式
    :param embed: 选填，embed 消息，一种特殊的 ark，详情参考Embed消息
    :param ark: 选填，ark 消息
    :param message_reference: 	选填，引用消息
    :param image: 选填，图片url地址，平台会转存该图片，用于下发图片消息
    :param msg_id: 选填，要回复的消息id(Message.id), 在 AT_CREATE_MESSAGE 事件中获取。
    :param event_id: 选填，要回复的事件id, 在各事件对象中获取。
    :param makedown: 选填，markdown 消息
"""
        if content is None and makedown is None and ark is None and embed is None:
            raise (
                WrongArgs("content, embed, ark, image/file_image, markdown 至少需要有一个字段，否则无法下发消息。"))
        else:
            data = {
                "content": content
            }
            if image is not None:
                data["image"] = image
            if content is not None:
                data["content"] = content
            if embed is not None:
                data["embed"] = embed.to_dict()
            if ark is not None:
                data["ark"] = ark.to_dict()
            if message_reference is not None:
                data["message_reference"] = message_reference
            if image is not None:
                data["image"] = image
            if msg_id is not None:
                data["msg_id"] = msg_id
            if event_id is not None:
                data["event_id"] = event_id
            if makedown is not None:
                data["makedown"] = makedown.to_dict()
        response = PostConnect(f"/channels/{channel_id}/messages", self.access_token, data, self.public_url).json()
        return Channel_Message_Info(
            id=response["id"],
            channel_id=response["channel_id"],
            guild_id=response["guild_id"],
            timestamp=response["timestamp"],
            author=User(
                id=response["author"]["id"],
                username=response["author"]["username"],
                avatar=response["author"]["avatar"],
                bot=response["author"]["bot"]
            ),
            content=response["content"],
            type=response["type"],
            embeds=response["embeds"],
            tts=response["tts"],
            mention_everyone=response["mention_everyone"],
            pinned=response["pinned"],
            flag=response["flag"]
        )





class BotAPI(WebSocketAPI, GuildManagementApi, MessageAPI):
    """便于用户快速调用所有API，这是一个通用接口"""
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
