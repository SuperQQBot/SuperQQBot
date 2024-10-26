from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

from .Error import UnknownKwargs, UnSupposeUsage, UnknownError


# 定义基本的事件对象
@dataclass
class Event:
    id: str
    time: float
    type: str
    detail_type: str
    self: Optional['Self'] = None
    sub_type: Optional[str] = None


# 定义 Self 对象
@dataclass
class Self:
    platform: str
    user_id: str


# 定义消息事件对象
@dataclass
class MessageEvent:
    message_id: str
    message: List[Dict[str, Any]]
    alt_message: str
    user_id: str
    nickname: Optional[str] = None


# 定义频道对象
@dataclass
class Channel:
    guild_id: str
    id: str
    name: str
    owner_id: str
    type: int
    sub_type: int
    position: int
    permissions: str
    speak_permission: int
    private_type: int
    application_id: Optional[str] = None
    parent_id: Optional[str] = None


# 定义用户对象
@dataclass
class User:
    id: str
    username: str
    avatar: str
    bot: bool = False
    union_openid: Optional[str] = None
    union_user_account: Optional[str] = None
    share_url: Optional[str] = None
    welcome_msg: Optional[str] = None


# 定义频道对象
@dataclass
class Guild:
    id: str
    name: str
    description: str
    icon: str
    owner_id: str
    member_count: int
    max_members: int
    joined_at: str
    owner: bool


# 定义成员对象
@dataclass
class Member:
    user: User
    nick: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    joined_at: Optional[str] = None
    premium_since: Optional[str] = None
    deaf: bool = False
    mute: bool = False
    pending: bool = False
    permissions: Optional[str] = None
    communication_disabled_until: Optional[str] = None


# 定义消息附件对象
@dataclass
class MessageAttachment:
    id: str
    filename: str
    size: int
    url: str
    proxy_url: str
    height: Optional[int] = None
    width: Optional[int] = None
    description: Optional[str] = None
    content_type: Optional[str] = None


# 定义反应对象
@dataclass
class Reaction:
    count: int
    me: bool
    emoji: dict


# 定义消息对象
@dataclass
class BaseMessage:
    id: str
    channel_id: str
    guild_id: str
    content: str
    timestamp: datetime
    author: User
    edited_timestamp: Optional[datetime] = None
    mention_roles: List[str] = field(default_factory=list)
    mentions: List[User] = field(default_factory=list)
    attachments: List[MessageAttachment] = field(default_factory=list)
    embeds: List[Dict[str, Any]] = field(default_factory=list)
    reactions: List[Reaction] = field(default_factory=list)


# 定义消息对象
@dataclass
class Message(BaseMessage):

    def reply(self, **kwargs):
        raise UnknownError("R P N C")


@dataclass
class GroupMessageInfo:
    id: str
    timestamp: datetime


# 定义群管理事件
@dataclass
class GroupManageEvent:
    group_openid: str
    op_member_openid: str
    timestamp: datetime


# 定义群消息对象
@dataclass
class GroupMessage(BaseMessage):
    pass


# 定义私聊消息对象
@dataclass
class C2CMessage(BaseMessage):
    pass


# 定义论坛主题信息
@dataclass
class Elems:
    text: str
    type: int


@dataclass
class Paragraphs:
    elems: List[Elems]
    props: Dict[Any, Any]


@dataclass
class ThreadInfo:
    content: List[Paragraphs]
    date_time: datetime
    thread_id: str
    title: List[Paragraphs]


@dataclass
class Thread:
    author_id: str
    channel_id: str
    guild_id: str
    thread_info: ThreadInfo


# 定义 DirectMessage 类型
@dataclass
class DirectMessage:
    recipient_id: str
    message: str
    timestamp: datetime


# 定义 Group 类型
@dataclass
class Group:
    id: str
    name: str
    description: str
    owner_id: str
    member_count: int
    max_members: int
    joined_at: str
    owner: bool


# 定义 Interaction 类型
@dataclass
class Interaction:
    id: str
    application_id: str
    token: str
    version: int
    type: int
    data: Dict[str, Any]
    member: Member


# 定义 MessageAudit 类型
@dataclass
class MessageAudit:
    audit_id: str
    message_id: str
    result: bool
    reason: Optional[str] = None


# 定义 ForumThread 类型
@dataclass
class ForumThread:
    id: str
    author_id: str
    title: str
    content: str
    timestamp: datetime


# 定义 ForumPost 类型
@dataclass
class ForumPost:
    id: str
    thread_id: str
    author_id: str
    content: str
    timestamp: datetime


# 定义 ForumReply 类型
@dataclass
class ForumReply:
    id: str
    post_id: str
    author_id: str
    content: str
    timestamp: datetime


# 定义 ForumPublishAudit 类型
@dataclass
class ForumPublishAudit:
    audit_id: str
    thread_id: str
    result: bool
    reason: Optional[str] = None


# 定义 AudioAction 类型
@dataclass
class AudioAction:
    action: str
    duration: Optional[int] = None


# 定义 PublicMessage 类型
@dataclass
class PublicMessage(BaseMessage):
    pass


@dataclass
class MakeDown_params:
    key: str
    values: List[str]


@dataclass
class MakeDown:
    content: str
    custom_template_id: str
    params: List[MakeDown_params]

    def to_dict(self):
        return {
            "content": self.content,
            "custom_template_id": self.custom_template_id,
            "params": self.params
        }


@dataclass
class ChannelType:
    """子频道类型\n
    注：由于QQ频道还在持续的迭代中，经常会有新的子频道类型增加，文档更新不一定及时，开发者识别 ChannelType 时，请注意相关的未知 ID 的处理。\n
    值	描述\n
    0	文字子频道\n
    1	保留，不可用\n
    2	语音子频道\n
    3	保留，不可用\n
    4	子频道分组\n
    10005	直播子频道\n
    10006	应用子频道\n
    10007	论坛子频道\n"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2, 3, 4, 10005, 10006, 10007]
        self.Keep_so_can_not_use = [1, 3]
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("ChannelType", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


@dataclass
class ChannelSubType:
    """子频道类型\n
    目前只有文字子频道具有 ChannelSubType 二级分类，同时二级分类也可能会不断增加，开发者也需要注意对未知 ID 的处理。\n
    值	描述\n
    0	闲聊\n
    1	公告\n
    2	攻略\n
    3	开黑\n"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2, 3]
        self.Keep_so_can_not_use = None
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("ChannelSubType", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class PrivateType:
    """子频道私密类型\n
        值	描述\n
        0	公开频道\n
        1	群主管理员可见\n
        2	群主管理员+指定成员，可使用 修改子频道权限接口 指定成员"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2]
        self.Keep_so_can_not_use = None
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("PrivateType", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class SpeakPermission:
    """子频道发言权限\n
            值	描述\n
            0	无效类型\n
            1	所有人\n
            2	群主管理员+指定成员，可使用 修改子频道权限接口 指定成员"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2]
        self.Keep_so_can_not_use = [0]
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("SpeakPermission", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class MessageType:
    """消息类型\n
            值	描述\n
            0	文本\n
            1	markdown\n
            2	ark 富媒体"""

    def __init__(self, type: int):
        self.type = type
        self.SHOULD_IN = [0, 1, 2]
        self.Keep_so_can_not_use = []
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("MessageType", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class render_style:
    """按钮样式\n
            值	描述\n
            0	灰色线框\n
            1	蓝色线框"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1]
        self.Keep_so_can_not_use = []
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("render_style", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class action_type:
    """按钮操作设置\n
            值	描述\n
            0	跳转按钮：http 或 小程序 客户端识别 scheme\n
            1	回调按钮：回调后台接口, data 传给后台\n
            2   指令按钮：自动在输入框插入 @bot data"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2]
        self.Keep_so_can_not_use = []
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("action_type", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


class permission_type:
    """按钮操作设置\n
                值	描述\n
                0	指定用户可操作\n
                1	仅管理者可操作\n
                2   所有人可操作\n
                3   指定身份组可操作（仅频道可用）"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [0, 1, 2, 3]
        self.Keep_so_can_not_use = []
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("action_type", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


@dataclass
class permission:
    type: permission_type
    user_ids: List[str] = field(default_factory=list)
    role_ids: List[str] = field(default_factory=list)


@dataclass
class render_data:
    label: str
    visited_label: str
    style: render_style

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "visited_label": self.visited_label,
            "style": self.style
        }


@dataclass
class action:
    type: action_type
    permission: permission
    data: str
    reply: bool
    enter: bool
    anchor: int
    unsupport_tips: str
    click_limit: int | None = None
    at_bot_show_channel_list: bool | None = None

    def __init__(self):
        if self.click_limit is not None:
            raise (
                UnSupposeUsage("click_limit"))
        if self.at_bot_show_channel_list is not None:
            raise (
                UnSupposeUsage("at_bot_show_channel_list"))


@dataclass
class Button:
    id: Optional[str] = None
    render_data: render_data = field(default_factory=dict)
    action: action = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "render_data": self.render_data.to_dict(),
            "action": self.action
        }


@dataclass
class Keyboard:
    rows: List[List[Button]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows": [[button.to_dict() for button in row] for row in self.rows]
        }


@dataclass
class Ark:
    template_id: int
    kv: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "kv": self.kv
        }


class file_type:
    """文件类型\n
                    值	描述\n
                    1	图片 [png/jpg]\n
                    2	视频 [mp4]\n
                    3   语音 [silk]\n
                    4   文件（暂不开放）"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [1, 2, 3, 4]
        self.Keep_so_can_not_use = [4]
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("file_type", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


@dataclass
class C2C_file_Send:
    file_type: file_type
    url: str
    srv_send_msg: bool
    file_data: Optional[Any]

    def __init__(self):
        if self.file_data is not None:
            raise (
                UnSupposeUsage("file_data"))


@dataclass
class Media_C2C:
    file_uuid: str
    file_info: str
    ttl: int
    id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_uuid": self.file_uuid,
            "file_info": self.file_info,
            "ttl": self.ttl,
            "id": self.id
        }


@dataclass
class C2C_Message_Info:
    message_id: str
    timestamp: datetime


@dataclass
class MessageEmbedThumbnail:
    url: str

    def to_dict(self):
        return {
            "url": self.url
        }


@dataclass
class MessageEmbedField:
    name: str

    def to_dict(self):
        return {
            "name": self.name
        }


@dataclass
class MessageEmbed:
    title: str
    prompt: str
    thumbnail: MessageEmbedThumbnail
    fields: List[MessageEmbedField]

    def to_dict(self):
        return {
            "title": self.title,
            "prompt": self.prompt,
            "thumbnail": self.thumbnail.to_dict(),
            "fields": [field.to_dict() for field in self.fields]
        }


@dataclass
class ChannelMessageInfo:
    id: str
    channel_id: str
    guild_id: str
    content: str
    timestamp: datetime
    tts: bool
    mention_everyone: bool
    author: User
    pinned: bool
    type: MessageType
    flag: int
    seq_in_channel: int


@dataclass
class MediaInfo:
    file_uuid: str
    file_info: str
    ttl: int
    id: Optional[str]


@dataclass
class EmojiType:
    """表情类型\n
                        值	描述\n
                        1	系统表情\n
                        2	系统表情"""
    type: int

    def __init__(self):
        self.SHOULD_IN = [1, 2]
        self.Keep_so_can_not_use = []
        if self.type not in self.SHOULD_IN:
            raise (
                UnknownKwargs("Emoji_type", self.SHOULD_IN, self.type))
        elif self.type in self.Keep_so_can_not_use:
            raise (
                UnSupposeUsage(self.type))


@dataclass
class Emoji:
    """详见：https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#emoji%E5%88%97%E8%A1%A8"""
    id: str
    type: EmojiType


@dataclass
class Reaction:
    users: List[User]
    cookie: str
    is_end: bool
