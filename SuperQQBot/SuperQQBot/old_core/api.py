import warnings

from typing import List

from .types import *
from . import Error, log
from .Error import WrongArgs, ParameterMappingFailed, CompatibilityWillBeUnSuppose, UsingBetaFunction
from .connection import PostConnect, GetConnect, DeleteRequests, PutRequests, my_ipaddress
from .. import Member

_log = log.get_logger()




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
        get_connect = GetConnect("/gateway", self.access_token, self.public_url)
        await get_connect.apply()
        return get_connect.json()["url"]


# 频道模块API
class GuildManagementApi(BaseBotApi):
    """频道管理相关API"""

    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def get_guild(self, guild_id: str | int) -> Guild:
        """获取频道详情
        :param guild_id: 频道ID
        :rtype: Guild
        :return: guild_id 指定的频道的详情。"""
        get_connect = GetConnect(f"/guilds/{guild_id}", self.access_token, self.public_url)
        await get_connect.apply()
        return Guild(**get_connect.json())

    async def get_channels(self, guild_id: str | int) -> List[Channel]:
        """获取子频道列表
        :param guild_id: 频道ID
        :rtype: List[Channel]
        :return: guild_id 指定的频道下的子频道列表。"""
        output = []
        get_connect = GetConnect(f"/guilds/{guild_id}/channels", self.access_token, self.public_url)
        await get_connect.apply()
        for i in get_connect.json():
            output.append(Channel(**i))
        return output

    async def me(self) -> User:
        """获取用户详情。
        :rtype: User
        :return: 当前用户（机器人）详细"""
        get_connect = GetConnect("/users/@me", self.access_token, self.public_url)
        await get_connect.apply()
        return User(**get_connect.json())

    async def me_guilds(self) -> List[Guild]:
        """获取用户频道列表
        :return: 当前用户（机器人）所加入的频道列表
        :rtype: List[Guild}"""
        output = []
        get_connect = GetConnect("/users/@me/guilds", self.access_token, self.public_url)
        await get_connect.apply()
        for i in get_connect.json():
            output.append(Guild(**i))
        return output

    async def get_channel(self, channel_id: str | int | Channel) -> Channel:
        """获取子频道详情
        :param channel_id: 子频道ID
        :rtype: Channel
        :return: channel_id 指定的子频道的详情。"""
        get_connect = GetConnect(f"/channels/{channel_id}", self.access_token, self.public_url)
        await get_connect.apply()
        return Channel(**get_connect.json())

    async def create_channel(self,
                             guild_id: str | int | Guild,
                             position: int,
                             name: str | None = None,
                             type: ChannelType | None = None,
                             sub_type: ChannelSubType | None = None,
                             parent_id: str | None = None,
                             private_type: PrivateType | None = None,
                             private_user_ids: List[str] | None = None,
                             speak_permission: int | None = None,
                             application_id: str | None = None) -> Channel:
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
        if type.type != 0 and sub_type is not None:
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
        post_connect = PostConnect(f"/guilds/{guild_id}/channels", self.access_token, data, self.public_url)
        await post_connect.apply()
        return Channel(**post_connect.json())

    async def update_channel(self,
                             channel_id: str | int | Channel,
                             name: str | None = None,
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
            data = {"name": name}
        elif position is not None:
            data = {"position": position}
        elif parent_id is not None:
            data = {"parent_id": parent_id}
        elif private_type is not None:
            data = {"private_type": private_type.type}
        elif speak_permission is not None:
            data = {"speak_permission": speak_permission.type}
        else:
            raise (
                WrongArgs("没有要修改的参数"))
        get_connect = PostConnect(
                f"/channels/{channel_id}",
                self.access_token, data,
                self.public_url)
        await get_connect.apply()
        return Channel(
            **get_connect
            .json())

    async def delete_channel(self,
                             channel_id: str | int | Channel) -> None:
        """删除子频道
        :param channel_id: 子频道ID"""
        delete_requests = DeleteRequests(f"/channels/{channel_id}", self.access_token, self.public_url)
        await delete_requests.apply()
        delete_requests.verify_data()
        return
class GuildMemberApi(BaseBotApi):
    def __init__(self,
                 access_token: str,
                 is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
    async def get_online_num(self,
                             channel_id: str | int | Channel) -> Optional[int]:
        """用于查询音视频/直播子频道 channel_id 的在线成员数。
        :param channel_id: 子频道ID"""
        try:
            get_connect = GetConnect(f"/channels/{channel_id}/online_num",
                       self.access_token, self.public_url)
            await get_connect.apply()
            return int(get_connect.json()["online_nums"])
        except TypeError:
            return None
    async def get_guild_member(self,
                               guild_id: str | int | Guild,
                               after: str = "0",
                               limit: int = 1):
        """用于获取 guild_id 指定的频道中所有成员的详情列表，支持分页。

            注意

                公域机器人暂不支持申请，仅私域机器人可用，选择私域机器人后默认开通。
                注意: 开通后需要先将机器人从频道移除，然后重新添加，方可生效。
        :param guild_id: 频道ID
        :param after: 上一次回包中最后一个member的user id， 如果是第一次请求填 0，默认为 0
        :param limit: 分页大小，1-400，默认是 1。成员较多的频道尽量使用较大的limit值，以减少请求数
        注意：在每次翻页的过程中，可能会返回上一次请求已经返回过的member信息，需要调用方自己根据user id来进行去重。

        每次返回的member数量与limit不一定完全相等。翻页请使用最后一个member的user id作为下一次请求的after参数，直到回包为空，拉取结束。"""
        get_connect = GetConnect(f"/guilds/{guild_id}/members",self.access_token,
                                                self.public_url, query={"after": after, "limit": limit})
        await get_connect.apply()
        return [Member(**i) for i in get_connect.json()]
    async def get_role_member_list(self,
                                   guild_id: str | int | Guild,
                                   role_id: str | int,
                                   start_index: str = "0",
                                   limit: int = 1) -> dict[str, list[Member]]:
        """用于获取 guild_id 频道中指定role_id身份组下所有成员的详情列表，支持分页。

        注意

            公域机器人暂不支持申请，仅私域机器人可用，选择私域机器人后默认开通。
            注意: 开通后需要先将机器人从频道移除，然后重新添加，方可生效。
        :param guild_id: 频道ID
        :param role_id: 身份组ID
        :param start_index: 将上一次回包中next填入， 如果是第一次请求填 0，默认为 0
        :param limit: 分页大小，1-400，默认是 1。成员较多的频道尽量使用较大的limit值，以减少请求数
        """
        get_connect = GetConnect(f"/guilds/{guild_id}/roles/{role_id}/members",
                                                self.access_token,
                                                self.public_url,
                                                query={"start_index": start_index, "limit": limit})
        await get_connect.apply()
        return {"data": [Member(**i) for i in get_connect.json()["data"]],
                "next": get_connect.json()["next"]}
    async def get_channel_members_details(self,
                                          guild_id: str | int | Guild,
                                          user_id: str) -> Member:
        """用于获取 guild_id 指定的频道中 user_id 对应成员的详细信息。
        :param guild_id: 频道ID
        :param user_id: 用户ID
        :return: Member类型的guild_id 指定的频道中 user_id 对应成员的详细信息"""
        get_connect = GetConnect(f"/guilds/{guild_id}/members/{user_id}",
                   self.access_token,
                   self.public_url)
        await get_connect.apply()
        return Member(**get_connect.json())
    async def delete_channel_member(self,
                                    guild_id: str | int | Guild,
                                    user_id: str | int | User,
                                    add_blacklist: bool = False,
                                    delete_history_msg_days: int = 0) -> None:
        """用于删除 guild_id 指定的频道下的成员 user_id。

            需要使用的 token 对应的用户具备踢人权限。如果是机器人，要求被添加为管理员。
            操作成功后，会触发频道成员删除事件。
            无法移除身份为管理员的成员
            注意

                公域机器人暂不支持申请，仅私域机器人可用，选择私域机器人后默认开通。
                注意: 开通后需要先将机器人从频道移除，然后重新添加，方可生效。
        :param guild_id: 频道ID
        :param user_id: 用户ID
        :param add_blacklist: 删除成员的同时，将该用户添加到频道黑名单中
        :param delete_history_msg_days: 删除成员的同时，撤回该成员的消息，可以指定撤回消息的时间范围（消息撤回时间范围仅支持固定的天数：3，7，15，30。 特殊的时间范围：-1: 撤回全部消息。默认值为0不撤回任何消息。）"""
        if delete_history_msg_days not in [3, 7, 15, 30, -1, 0]:
            raise UnknownKwargs("delete_history_msg_days", [3, 7, 15, 30, -1, 0], delete_history_msg_days)
        delete_requests = DeleteRequests(f"/guilds/{guild_id}/members/{user_id}",
                                          self.access_token,
                                          self.public_url)
        await delete_requests.apply()
        delete_requests.verify_data()
        return


# 消息相关API
class MessageSendReceiveAPI(BaseBotApi):
    def __init__(self,
                 access_token: str,
                 is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def post_dms(self,
                       openid: str,
                       msg_type: MessageType,
                       content: str | None = None,
                       makedown: MakeDown | None = None,
                       keyboard: Keyboard | None = None,
                       ark: Ark | None = None,
                       media: MediaC2C | None = None,
                       message_reference: Optional[Any] = None,
                       event_id: str | None = None,
                       msg_id: str | None = None,
                       msg_seq: int | None = None
                       ) -> C2CMessageInfo:
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
        post_connect = PostConnect(f"/v2/users/{openid}/messages", self.access_token, data, self.public_url)
        await post_connect.apply()
        return C2CMessageInfo(
            **post_connect.json())

    async def post_channel_messages(self,
                                    channel_id: str | int | Channel,
                                    embed: Optional[MessageEmbed] = None,
                                    content: str | None = None,
                                    makedown: MakeDown | None = None,
                                    ark: Ark | None = None,
                                    message_reference: Optional[Any] = None,
                                    event_id: str | None = None,
                                    image: Optional[str] = None,
                                    msg_id: Optional[str] = None,
                                    mention: Optional[str] = None,
                                    mention_everyone: bool = False
                                    ) -> ChannelMessageInfo:
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
    :param mention: 要@的人的ID
    :param mention_everyone: 是否@所有人
"""
        if content is None and makedown is None and ark is None and embed is None:
            raise (
                WrongArgs("content, embed, ark, image/file_image, markdown 至少需要有一个字段，否则无法下发消息。"))
        else:
            data = {}
            if mention is not None:
                (warnings
                 .warn(UsingBetaFunction("mention")))
            if mention_everyone:
                (warnings
                 .warn(UsingBetaFunction("mention_everyone")))
            """if "@everyone" in content:
                (warnings
                 .warn(CompatibilityWillBeUnSuppose('@everyone', '<qqbot-at-everyone />')))"""
            """elif "<@" in content:
                (warnings
                 .warn(CompatibilityWillBeUnSuppose('<@userid>', '<qqbot-at-user id="" />')))"""
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
            if mention is not None:
                data = {
                    "content": f"<qqbot-at-user id=\"{mention}\" /> " + content
                }
            if mention_everyone:
                data = {
                    "content": "<qqbot-at-everyone /> " + content
                }
        post_connect = PostConnect(f"/channels/{channel_id}/messages", self.access_token, data, self.public_url)
        await post_connect.apply()
        response = post_connect.json()
        return ChannelMessageInfo(
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
            tts=response["tts"],
            mention_everyone=response["mention_everyone"],
            pinned=response["pinned"],
            flag=response["flags"],
            seq_in_channel=response["seq_in_channel"]
        )

    async def post_group_message(
            self,
            group_openid: str,
            content: str,
            msg_type: int,
            markdown: Optional[dict] = None,
            keyboard: Optional[dict] = None,
            media: Optional[dict] = None,
            ark: Optional[dict] = None,
            message_reference: Optional[Any] = None,
            event_id: Optional[str] = None,
            msg_id: Optional[str] = None,
            msg_seq: Optional[int] = None,
            mention: Optional[str] = None,
    ) -> GroupMessageInfo:
        """向指定群聊发送消息。
        :param group_openid: 群聊的 openid
        :param content: 文本内容
        :param msg_type: 消息类型：0 是文本，2 是 markdown，3 ark 消息，4 embed，7 media 富媒体
        :param markdown: Markdown对象
        :param keyboard: Keyboard对象
        :param media: 富媒体群聊的file_info
        :param ark: Ark对象
        :param message_reference: 【暂未支持】消息引用
        :param event_id: 前置收到的事件 ID，用于发送被动消息，支持事件："INTERACTION_CREATE"、"GROUP_ADD_ROBOT"、"GROUP_MSG_RECEIVE"
        :param msg_id: 前置收到的用户发送过来的消息 ID，用于发送被动消息（回复）
        :param msg_seq: 回复消息的序号，与 msg_id 联合使用，避免相同消息id回复重复发送，不填默认是 1。相同的 msg_id + msg_seq 重复发送会失败。
        :param mention: 要@的人的ID
        """

        data = {
            "content": content,
            "msg_type": msg_type
        }
        if mention is not None:
            warnings.warn(UsingBetaFunction("mention"))
        if mention is not None:
            data["content"] = f"<qqbot-at-user id=\"{mention}\" />" + content

        if "@everyone" in content:
            raise (
                WrongArgs("群聊不支持@所有人"))
        elif "<@" in content:
            (warnings
             .warn(CompatibilityWillBeUnSuppose('<@userid>', '<qqbot-at-user id="" />')))
        if message_reference is not None:
            raise UnSupposeUsage("message_reference")

        if msg_type == 0 and content is None:
            raise ParameterMappingFailed("content", "msg_type", content, msg_type)
        elif msg_type == 2 and markdown is None:
            raise ParameterMappingFailed("markdown", "msg_type", markdown, msg_type)
        elif msg_type == 3 and ark is None:
            raise ParameterMappingFailed("ark", "msg_type", ark, msg_type)
        elif msg_type == 4 and media is None:
            raise ParameterMappingFailed("media", "msg_type", media, msg_type)
        elif msg_type == 7 and content is None:
            data["content"] = " "

        if markdown is not None:
            data["markdown"] = markdown
        if keyboard is not None:
            data["keyboard"] = keyboard
        if media is not None:
            data["media"] = media
        if ark is not None:
            data["ark"] = ark
        if event_id is not None:
            data["event_id"] = event_id
        if msg_id is not None:
            data["msg_id"] = msg_id
        if msg_seq is not None:
            data["msg_seq"] = msg_seq
        post_connect = PostConnect(f"/v2/groups/{group_openid}/messages", self.access_token, data,
                               self.public_url)
        await post_connect.apply()
        return GroupMessageInfo(id=post_connect.json()["id"], timestamp=post_connect.json()["timestamp"])

    async def post_c2c_file(self, openid: str, file_type: FileType, url: str, srv_send_msg: bool,
                            file_data: Optional[Any] = None) -> MediaInfo:
        """
        用于单聊的富媒体消息上传和发送

        :param openid: QQ 用户的 openid
        :param file_type: 媒体类型：1 图片，2 视频，3 语音，4 文件（暂不开放）
        :param url: 需要发送媒体资源的 URL
        :param srv_send_msg: 设置 true 会直接发送消息到目标端，且会占用主动消息频次
        :param file_data: 【暂未支持】
        :return: 返回的文件信息
        """
        if file_data is not None:
            raise UnSupposeUsage("file_data")
        data = {
            "file_type": file_type,
            "url": url,
            "srv_send_msg": srv_send_msg
        }

        post_connect = PostConnect(f"/v2/users/{openid}/files", self.access_token, data, self.public_url)
        await post_connect.apply()
        return MediaInfo(**post_connect.json())

    async def post_group_file(self,
                              group_openid: str,
                              file_type: FileType,
                              url: str,
                              srv_send_msg: bool,
                              file_data: Optional[Any] = None) -> MediaInfo:
        """
        用于群聊的富媒体消息上传和发送

        :param group_openid: 群聊的 openid
        :param file_type: 媒体类型：1 图片，2 视频，3 语音，4 文件（暂不开放）
        :param url: 需要发送媒体资源的 URL
        :param srv_send_msg: 设置 true 会直接发送消息到目标端，且会占用主动消息频次
        :param file_data: 【暂未支持】
        :return: 返回的文件信息
        """
        if file_data is not None:
            raise UnSupposeUsage("file_data")
        data = {
            "file_type": file_type,
            "url": url,
            "srv_send_msg": srv_send_msg
        }

        post_connect = PostConnect(f"/v2/groups/{group_openid}/files", self.access_token, data, self.public_url)
        await post_connect.apply()
        return MediaInfo(**post_connect.json())

    async def recall_c2c_message(self,
                                 openid: str,
                                 message_id: str):
        """用于撤回机器人发送给当前用户 openid 的消息 message_id，发送超出2分钟的消息不可撤回
        :param openid: QQ 用户的 openid
        :param message_id: 消息ID"""
        delete_requests = DeleteRequests(f"/v2/users/{openid}/messages/{message_id}", self.access_token, self.public_url)
        await delete_requests.apply()
        delete_requests.verify_data()
        return

    async def recall_group_message(self,
                                   group_openid: str,
                                   message_id: str):
        """用于撤回机器人发送在当前群 group_openid 的消息 message_id，发送超出2分钟的消息不可撤回
        :param group_openid: 群聊的额 openid
        :param message_id: 消息ID"""
        delete_requrests = DeleteRequests(f"/v2/groups/{group_openid}/messages/{message_id}", self.access_token,
                                            self.public_url)
        await delete_requrests.apply()
        delete_requrests.verify_data()
        return

    async def recall_channel_message(self,
                                     channel_id: str,
                                     message_id: str,
                                     hidetip: bool = False):
        """用于撤回子频道 channel_id 下的消息 message_id

        管理员可以撤回普通成员的消息。
        频道主可以撤回所有人的消息。
        注意
        公域机器人暂不支持申请，仅私域机器人可用，选择私域机器人后默认开通。
        注意: 开通后需要先将机器人从频道移除，然后重新添加，方可生效。
        :param channel_id: 频道的 openid
        :param message_id: 消息ID
        :param hidetip: 选填，是否隐藏提示小灰条，true 为隐藏，false 为显示。默认为false"""
        delete_requests = DeleteRequests(f"/channels/{channel_id}/messages/{message_id}?hidetip={hidetip}",
                                            self.access_token, self.public_url)
        await delete_requests.apply()
        delete_requests.verify_data()
        return

    async def recall_dms_message(self,
                                 guild_id: str,
                                 message_id: str,
                                 hidetip: bool = False):
        """用于撤回私信频道 guild_id 中 message_id 指定的私信消息。只能用于撤回机器人自己发送的私信。

                管理员可以撤回普通成员的消息。
                频道主可以撤回所有人的消息。
                注意
                公域机器人暂不支持申请，仅私域机器人可用，选择私域机器人后默认开通。
                注意: 开通后需要先将机器人从频道移除，然后重新添加，方可生效。
                :param guild_id: 私信的 openid
                :param message_id: 消息ID
                :param hidetip: 选填，是否隐藏提示小灰条，true 为隐藏，false 为显示。默认为false"""
        delete_requests = DeleteRequests(f"/dms/{guild_id}/messages/{message_id}?hidetip={hidetip}",
                                            self.access_token, self.public_url)
        await delete_requests.apply()
        delete_requests.verify_data()
        return


class MessageExpressionInteraction(BaseBotApi):
    def __init__(self, access_token: str, is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)

    async def send_reaction_expression(self,
                                       channel_id: str,
                                       message_id: str,
                                       emoji: Emoji):
        """
        对消息 message_id 进行表情表态
        :param channel_id: 子频道ID
        :param message_id: 消息ID
        :param emoji: 包含type（表情类型）和id（表情ID）的Emoji对象
        """
        put_requests = PutRequests(f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji.type}/{emoji.id}",
                           self.access_token, self.public_url)
        await put_requests.apply()
        return

    async def delete_reaction_expression(self,
                                         channel_id: str,
                                         message_id: str,
                                         emoji: Emoji):
        """删除自己对消息 message_id 的表情表态
        :param channel_id: 子频道ID
        :param message_id: 消息ID
        :param emoji: Emoji类型，包含了type和id"""
        delete_requests = DeleteRequests(f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji.type}/{emoji.id}",
                              self.access_token, self.public_url)
        await delete_requests.apply()
        return

    async def get_reaction_users(self,
                                 channel_id: str,
                                 message_id: str,
                                 emoji: Emoji,
                                 cookie: Optional[str] = None,
                                 limit: int = 20) -> Reaction:
        """拉取对消息 message_id 指定表情表态的用户列表
        :param channel_id: 子频道ID
        :param message_id: 消息ID
        :param emoji: Emoji类型，
        :param cookie: 上次请求返回的cookie，第一次请求无需填写
        :param limit: 每次拉取数量，默认20，最多50，只在第一次请求时设置
        :return: 包含消息 message_id 指定表情表态的用户列表的Reaction类型"""
        if limit > 50 or limit < 1:
            raise UnknownKwargs("limit", "20和50间", limit)
        get_connect = GetConnect(f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji.type}/{emoji.id}",
                              self.access_token, self.public_url, query={"cookie": cookie, "limit": limit})
        await get_connect.apply()
        response = get_connect.json()
        return Reaction(
            users=[User(id=user["id"], username=user["username"], avatar=user["avatar"]) for user in response["users"]],
            cookie=response["cookie"], is_end=response["is_end"])


class BotAPI(WebSocketAPI,
             GuildManagementApi,
             MessageSendReceiveAPI,
             MessageExpressionInteraction,
             GuildMemberApi):
    """便于用户快速调用所有API，这是一个通用接口"""

    def __init__(self,
                 access_token: str,
                 is_sandbox: bool = False):
        super().__init__(access_token=access_token, is_sandbox=is_sandbox)
