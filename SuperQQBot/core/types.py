from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

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

# 群管理事件
@dataclass
class GroupManageEvent:
    group_openid: str
    op_member_openid: str
    timestamp: datetime

@dataclass
class GroupMessage(BaseMessage):
    pass

@dataclass
class C2CMessage(BaseMessage):
    pass

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
class Message:
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


@dataclass
class Elems:
    text: str
    type: int

@dataclass
class Paragraphs:
    elems:List[Elems]
    props:dict[Any, Any]


@dataclass
class ThreadInfo:
    content: List[Paragraphs]
    date_time: datetime
    thread_id: str
    title:List[Paragraphs]


@dataclass
class Thread:
    author_id: str
    channel_id: str
    guild_id: str
    thread_info:ThreadInfo


