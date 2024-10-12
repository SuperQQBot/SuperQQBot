from dataclasses import field, dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import warnings
from .Error import CompatibilityWillBeUnSuppose

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

    @property
    def name(self):
        warnings.warn(CompatibilityWillBeUnSuppose("self.robot.name", "self.robot.username"))
        return self.username

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
    pass

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
