import json
from functools import partial

import asyncio
import websockets
from dateutil import parser

from .api import MessageSendReceiveAPI
from .Error import InvalidIntentsError, ExecutionSequenceError
from .api import WebSocketAPI, Token, GuildManagementApi, BotAPI
from .connection import get_authorization
from .log import get_logger
from .types import *

_log = get_logger()


class Intents:
    VALID_FLAGS = {
        'GUILDS',
        'GUILD_MEMBERS',
        'GUILD_MESSAGES',
        'GUILD_MESSAGE_REACTIONS',
        'DIRECT_MESSAGE',
        'GROUP_AND_C2C_EVENT',
        'INTERACTION',
        'MESSAGE_AUDIT',
        'FORUMS_EVENT',
        'AUDIO_ACTION',
        'PUBLIC_GUILD_MESSAGES',
    }

    DEFAULT_VALUE = 0

    def __init__(self, **kwargs: bool) -> None:
        self.value: int = self.DEFAULT_VALUE
        self.intents = {flag: False for flag in self.VALID_FLAGS}
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f"{key!r} 是无效的标志名称。")
            self.intents[key] = value
        self._update_bitwise_value()

    @classmethod
    def all(cls):
        """ 订阅所有事件 """
        self = cls.none()
        for key in self.VALID_FLAGS:
            self.intents[key] = True
        self._update_bitwise_value()
        return self

    @classmethod
    def none(cls):
        """ 不订阅任何事件 """
        self = cls()
        self.value = self.DEFAULT_VALUE
        self._update_bitwise_value()
        return self

    @classmethod
    def default(cls):
        """ 默认订阅所有公域事件 """
        self = cls.none()
        self.intents['GUILDS'] = True
        self.intents['GUILD_MEMBERS'] = True
        self.intents['PUBLIC_GUILD_MESSAGES'] = True
        self._update_bitwise_value()
        return self

    def set_intent(self, intent_name, value):
        if intent_name in self.VALID_FLAGS:
            self.intents[intent_name] = value
            self._update_bitwise_value()
        else:
            raise TypeError(f"{intent_name!r} 是无效的标志名称。")

    def _update_bitwise_value(self):
        bitwise_intents = 0
        for key, value in self.intents.items():
            if value:
                bitwise_intents |= getattr(self, f'_{key}_BIT')
        self.value = bitwise_intents

    _GUILDS_BIT = 1 << 0
    _GUILD_MEMBERS_BIT = 1 << 1
    _GUILD_MESSAGES_BIT = 1 << 9
    _GUILD_MESSAGE_REACTIONS_BIT = 1 << 10
    _DIRECT_MESSAGE_BIT = 1 << 12
    _GROUP_AND_C2C_EVENT_BIT = 1 << 25
    _INTERACTION_BIT = 1 << 26
    _MESSAGE_AUDIT_BIT = 1 << 27
    _FORUMS_EVENT_BIT = 1 << 28
    _AUDIO_ACTION_BIT = 1 << 29
    _PUBLIC_GUILD_MESSAGES_BIT = 1 << 30





class Client:
    def __init__(self, intents, is_sandbox=False):
        if not isinstance(intents, Intents):
            raise ValueError("intents 必须是 Intents 类型的对象。")
        self.intents = intents
        self.is_sandbox = is_sandbox
        self.websocket_api = None
        self.ws = None
        self.wss_url = None
        self.session_id = None
        self.heartbeat_interval = None
        self.heartbeat_task = None
        self.ready = False
        self.d = None
        self.token = None
        self.tasks = list()

    @property
    def robot(self):
        if self.token is None:
            raise ExecutionSequenceError("Client.run()获取AccessToken", "Client.robot获取机器人信息")
        else:
            return GuildManagementApi(self.token, self.is_sandbox).me()

    @property
    def api(self):
        return BotAPI(self.token, self.is_sandbox)

    def run(self, appid, secret):
        self.token = asyncio.run(Token(appid, secret).get_access_token())
        self.websocket_api = WebSocketAPI(self.token, is_sandbox=self.is_sandbox)
        asyncio.run(self.main())

    async def main(self):
        task = asyncio.create_task(self.connect())
        self.tasks.append(task)
        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            _log.info("任务被取消，开始处理善后流程")
            for task in self.tasks:
                task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)
            await self.close()
        except KeyboardInterrupt:
            _log.info("检测到键盘请求停止，开始善后")
            for task in self.tasks:
                task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)
            await self.close()

    async def connect(self):
        """ 连接到WebSocket服务器 """
        if self.ws is not None and not self.ws.closed:
            _log.info("已经连接到WebSocket服务器。")
            return

        if self.wss_url is None:
            self.wss_url = await self.websocket_api.get_wss_url()

        self.ws = await websockets.connect(self.wss_url)
        _log.info(f"已连接到WebSocket服务器: {self.wss_url}")
        await self.handle_messages()

    async def identify(self):
        """ 发送Identify消息进行鉴权 """
        identify_payload = {
            "op": 2,
            "d": {
                "token": get_authorization(self.token),  # 使用 get_authorization 函数
                "intents": self.intents.value,
                "shard": [0, 1],
                "properties": {
                    "$os": "linux",
                    "$browser": "my_library",
                    "$device": "my_library"
                }
            }
        }
        await self.ws.send(json.dumps(identify_payload))
        _log.debug(f"已发送Identify消息，内容：{identify_payload}")

    async def handle_ready_event(self, data):
        """ 处理Ready Event """
        if data["t"] == "READY":
            self.session_id = data["d"]["session_id"]
            self.d = data["s"]
            _log.info(f"收到Ready事件，session_id: {self.session_id}")
            self.ready = True
            await self.on_ready()

    async def send_message(self, message):
        """ 发送消息到WebSocket服务器 """
        if self.ws is None or self.ws.closed:
            _log.warning("未连接到WebSocket服务器。")
            return

        try:
            await self.ws.send(message)
            _log.debug(f"已发送消息: {message}")
        except Exception as e:
            _log.error(f"发送消息失败: {e}")

    async def receive_message(self):
        """ 接收来自WebSocket服务器的消息 """
        msg = None
        try:
            msg = await self.ws.recv()
            _log.debug(f"收到原始消息: {msg}")
            data = json.loads(msg)

            # 检查是否为Hello消息 (op=10)
            if data.get("op") == 10:
                self.heartbeat_interval = data["d"]["heartbeat_interval"]
                _log.debug(f"收到Hello消息，心跳间隔: {self.heartbeat_interval} ms")
                await self.start_heartbeat()
                await self.identify()  # 立即发送Identify消息
                return None

            # 检查是否为Invalid Intents消息 (op=9)
            if data.get("op") == 9:
                raise InvalidIntentsError(data)
            if data.get("op") == 11:
                return None

            _log.info(f"解析后的消息: {data}")
            return data
        except websockets.exceptions.ConnectionClosedError as e:
            # 捕获连接关闭异常
            _log.error(f"WebSocket连接已关闭: {e}")

            # 尝试从关闭原因中提取数据
            if self.ws.close_reason:
                close_data = json.loads(self.ws.close_reason)
                if close_data.get("op") == 9:
                    raise InvalidIntentsError(close_data)

            return None
        except json.JSONDecodeError as e:
            _log.error(f"JSON解析错误: {msg} - {e}")
            return None

    async def start_heartbeat(self):
        """ 启动心跳定时器 """
        if self.heartbeat_task is not None:
            self.heartbeat_task.cancel()

        async def send_heartbeat():
            while True:
                await asyncio.sleep(self.heartbeat_interval / 1000)
                await self.send_heartbeat()

        self.heartbeat_task = asyncio.create_task(send_heartbeat())

    async def send_heartbeat(self):
        """ 发送心跳消息 """
        heartbeat_payload = {
            "op": 1,
            "d": self.d
        }
        await self.send_message(json.dumps(heartbeat_payload))

    async def close(self):
        """ 关闭WebSocket连接 """
        if self.ws is not None and not self.ws.closed:
            if self.heartbeat_task is not None:
                self.heartbeat_task.cancel()
            await self.ws.close()
            _log.info("WebSocket连接已关闭。")
        else:
            _log.info("没有活动的WebSocket连接可关闭。")

    async def reconnect(self):
        """ 自动重连逻辑 """
        while True:
            try:
                await self.connect()
                break
            except Exception as e:
                _log.error(f"重连失败，等待5秒后重试: {e}")
                await asyncio.sleep(5)

    async def handle_messages(self):
        """ 处理WebSocket消息 """
        while True:
            # 确保WebSocket连接正常
            if self.ws is None or self.ws.closed:
                _log.warning("WebSocket连接不存在或已关闭，尝试重新连接...")
                await self.reconnect()
                continue

            data = await self.receive_message()
            if data is None:
                continue

            # 处理Ready事件
            if data.get("t") == "READY":
                await self.handle_ready_event(data)
                continue

            # 处理Resumed事件
            if data.get("t") == "RESUMED":
                _log.info("收到RESUMED事件，重连成功！")
                self.ready = True
                continue

            # 处理其他事件
            event_type = data.get("t")
            about_event = data.get("d", "")
            if event_type == "AT_MESSAGE_CREATE":
                message = Message(
                    id=about_event.get("id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    guild_id=about_event.get("guild_id", ""),
                    content=about_event.get("content", ""),
                    timestamp=parser.isoparse(about_event.get("timestamp", "")),
                    author=User(
                        id=about_event.get("author", {}).get("id", ""),
                        username=about_event.get("author", {}).get("username", ""),
                        avatar=about_event.get("author", {}).get("avatar", ""),
                        bot=about_event.get("author", {}).get("bot", False),
                        union_openid=about_event.get("author", {}).get("union_openid"),
                        union_user_account=about_event.get("author", {}).get("union_user_account"),
                        share_url=about_event.get("author", {}).get("share_url"),
                        welcome_msg=about_event.get("author", {}).get("welcome_msg")
                    ),
                    edited_timestamp=parser.isoparse(about_event.get("edited_timestamp", "")) if about_event.get(
                        "edited_timestamp") else None,
                    mention_roles=about_event.get("mention_roles", []),
                    mentions=[
                        User(
                            id=mention.get("id", ""),
                            username=mention.get("username", ""),
                            avatar=mention.get("avatar", ""),
                            bot=mention.get("bot", False),
                            union_openid=mention.get("union_openid"),
                            union_user_account=mention.get("union_user_account"),
                            share_url=mention.get("share_url"),
                            welcome_msg=mention.get("welcome_msg")
                        ) for mention in about_event.get("mentions", [])
                    ],
                    attachments=[
                        MessageAttachment(
                            id=attachment.get("id", ""),
                            filename=attachment.get("filename", ""),
                            size=attachment.get("size", 0),
                            url=attachment.get("url", ""),
                            proxy_url=attachment.get("proxy_url", ""),
                            height=attachment.get("height"),
                            width=attachment.get("width"),
                            description=attachment.get("description"),
                            content_type=attachment.get("content_type")
                        ) for attachment in about_event.get("attachments", [])
                    ],
                    embeds=about_event.get("embeds", []),
                    reactions=[
                        Reaction(
                            count=reaction.get("count", 0),
                            me=reaction.get("me", False),
                            emoji=reaction.get("emoji", {})
                        ) for reaction in about_event.get("reactions", [])
                    ]
                )
                message_api = MessageSendReceiveAPI(self.token, self.is_sandbox)
                message.api = message_api
                message.reply = partial(message_api.post_channel_messages, channel_id=message.channel_id, msg_id = message.id)
                await self.on_at_message_create(message)
            elif event_type == "AT_MESSAGE_UPDATE":
                message = Message(
                    id=about_event.get("id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    guild_id=about_event.get("guild_id", ""),
                    content=about_event.get("content", ""),
                    timestamp=parser.isoparse(about_event.get("timestamp", "")),
                    author=User(
                        id=about_event.get("author", {}).get("id", ""),
                        username=about_event.get("author", {}).get("username", ""),
                        avatar=about_event.get("author", {}).get("avatar", ""),
                        bot=about_event.get("author", {}).get("bot", False),
                        union_openid=about_event.get("author", {}).get("union_openid"),
                        union_user_account=about_event.get("author", {}).get("union_user_account"),
                        share_url=about_event.get("author", {}).get("share_url"),
                        welcome_msg=about_event.get("author", {}).get("welcome_msg")
                    ),
                    edited_timestamp=parser.isoparse(about_event.get("edited_timestamp", "")) if about_event.get(
                        "edited_timestamp") else None,
                    mention_roles=about_event.get("mention_roles", []),
                    mentions=[
                        User(
                            id=mention.get("id", ""),
                            username=mention.get("username", ""),
                            avatar=mention.get("avatar", ""),
                            bot=mention.get("bot", False),
                            union_openid=mention.get("union_openid"),
                            union_user_account=mention.get("union_user_account"),
                            share_url=mention.get("share_url"),
                            welcome_msg=mention.get("welcome_msg")
                        ) for mention in about_event.get("mentions", [])
                    ],
                    attachments=[
                        MessageAttachment(
                            id=attachment.get("id", ""),
                            filename=attachment.get("filename", ""),
                            size=attachment.get("size", 0),
                            url=attachment.get("url", ""),
                            proxy_url=attachment.get("proxy_url", ""),
                            height=attachment.get("height"),
                            width=attachment.get("width"),
                            description=attachment.get("description"),
                            content_type=attachment.get("content_type")
                        ) for attachment in about_event.get("attachments", [])
                    ],
                    embeds=about_event.get("embeds", []),
                    reactions=[
                        Reaction(
                            count=reaction.get("count", 0),
                            me=reaction.get("me", False),
                            emoji=reaction.get("emoji", {})
                        ) for reaction in about_event.get("reactions", [])
                    ]
                )
                await self.on_message_update(message)
            elif event_type == "GROUP_AT_MESSAGE_CREATE":
                message = GroupMessage(
                    id=about_event.get("id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    guild_id=about_event.get("guild_id", ""),
                    content=about_event.get("content", ""),
                    timestamp=parser.isoparse(about_event.get("timestamp", "")),
                    author=User(
                        id=about_event.get("author", {}).get("id", ""),
                        username="群聊暂不支持获取用户名",
                        avatar="群聊暂不支持获取头像",
                        union_openid=about_event.get("author", {}).get("union_openid"),
                        union_user_account=about_event.get("author", {}).get("union_user_account"),
                        share_url="群聊暂不支持获取分享链接"
                    ),
                    attachments=[
                        MessageAttachment(
                            url=attachment["url"],
                            content_type=attachment["content_type"],
                            filename=attachment["filename"],
                            height=attachment["height"],
                            size=attachment["size"],
                            width=attachment["width"],
                            id=attachment.get("id", ""),
                            proxy_url=attachment.get("proxy_url", "")
                        )
                        for attachment in about_event.get("attachments", [])
                    ])
                message_api = MessageSendReceiveAPI(self.token, self.is_sandbox)
                message.api = message_api
                message.reply = partial(message_api.post_channel_messages, channel_id=message.channel_id,
                                        msg_id=message.id)
                await self.on_group_at_message_create(message)
            elif event_type == "FORUM_THREAD_CREATE":
                message = Thread(
                    guild_id=about_event.get("guild_id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    author_id=about_event.get("author_id", ""),
                    thread_info=ThreadInfo(
                        content=[Paragraphs(
                            elems=[
                                Elems(text=elem.get("text", {}).get("text", ""),
                                      type=elem.get("type", "")
                                      ) for elem in paragraph.get("elems", [])
                            ],
                            props=paragraph.get("props", {})
                        ) for paragraph in
                            json.loads(about_event.get("thread_info", {}).get("content", [])).get("paragraphs", [{}])
                        ],
                        date_time=parser.isoparse(about_event.get("thread_info", {}).get("date_time", "")),
                        thread_id=about_event.get("thread_info", {}).get("thread_id", ""),
                        title=[Paragraphs(
                            elems=[
                                Elems(text=elem.get("text", {}).get("text", ""),
                                      type=elem.get("type", "")
                                      ) for elem in paragraph.get("elems", [{}])
                            ],
                            props=paragraph.get("props", {})
                        ) for paragraph in
                            json.loads(about_event.get("thread_info", {}).get("title", {})).get("paragraphs", [{}])]
                    )
                )
                await self.on_forum_thread_create(message)
            elif event_type == "FORUM_THREAD_UPDATE":
                message = Thread(
                    guild_id=about_event.get("guild_id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    author_id=about_event.get("author_id", ""),
                    thread_info=ThreadInfo(
                        content=[Paragraphs(
                            elems=[
                                Elems(text=elem.get("text", {}).get("text", ""),
                                      type=elem.get("type", "")
                                      ) for elem in paragraph.get("elems", [])
                            ],
                            props=paragraph.get("props", {})
                        ) for paragraph in
                            json.loads(about_event.get("thread_info", {}).get("content", [])).get("paragraphs", [{}])
                        ],
                        date_time=parser.isoparse(about_event.get("thread_info", {}).get("date_time", "")),
                        thread_id=about_event.get("thread_info", {}).get("thread_id", ""),
                        title=[Paragraphs(
                            elems=[
                                Elems(text=elem.get("text", {}).get("text", ""),
                                      type=elem.get("type", "")
                                      ) for elem in paragraph.get("elems", [{}])
                            ],
                            props=paragraph.get("props", {})
                        ) for paragraph in
                            json.loads(about_event.get("thread_info", {}).get("title", {})).get("paragraphs", [{}])]
                    )
                )
                await self.on_forum_thread_update(message)
            elif event_type == "MESSAGE_CREATE":
                message = Message(
                    id=about_event.get("id", ""),
                    channel_id=about_event.get("channel_id", ""),
                    guild_id=about_event.get("guild_id", ""),
                    content=about_event.get("content", ""),
                    timestamp=parser.isoparse(about_event.get("timestamp", "")),
                    author=User(
                        id=about_event.get("author", {}).get("id", ""),
                        username=about_event.get("author", {}).get("username", ""),
                        avatar=about_event.get("author", {}).get("avatar", ""),
                        bot=about_event.get("author", {}).get("bot", False),
                        union_openid=about_event.get("author", {}).get("union_openid"),
                        union_user_account=about_event.get("author", {}).get("union_user_account"),
                        share_url=about_event.get("author", {}).get("share_url"),
                    )
                )
                message_api = MessageSendReceiveAPI(self.token, self.is_sandbox)
                message.api = message_api
                message.reply = partial(message_api.post_channel_messages, channel_id=message.channel_id,
                                        msg_id=message.id)
                await self.on_message_create(message)
            elif event_type == "GROUP_ADD_ROBOT":
                message = GroupManageEvent(
                    group_openid=about_event.get("group_openid", ""),
                    op_member_openid=about_event.get("op_member_openid", ""),
                    timestamp=parser.isoparse(about_event.get("timestamp", ""))
                )
                await self.on_group_add_robot(message)
            else:
                _log.info(f"接收到未知事件类型 {event_type}，忽略...")

    async def on_ready(self):
        """ 处理Ready事件 """
        _log.info("已准备好接收事件。")

    # GUILD_MEMBERS 事件
    async def on_guild_member_add(self, member: Member):
        """当成员加入时"""
        _log.info(f"用户 {member.user.username} 加入了频道")

    async def on_guild_member_update(self, before: Member, after: Member):
        """当成员资料变更时"""
        _log.info(f"用户 {after.user.username} 在频道 {after.guild.name} 的资料已更新")

    async def on_guild_member_remove(self, member: Member):
        """当成员被移除时"""
        _log.info(f"用户 {member.user.username} 已从频道 {member.guild.name} 中移除")

    # GUILD_MESSAGES 事件

    async def on_message_delete(self, message: Message):
        """删除（撤回）消息事件"""
        _log.info(f"消息 {message.content} 在频道 {message.channel.guild.name} 被删除")

    # GUILD_MESSAGE_REACTIONS 事件
    async def on_message_reaction_add(self, reaction: Reaction):
        """为消息添加表情表态"""
        _log.info(f"表情 {reaction.emoji} 被添加到消息 {reaction.message_id}")

    async def on_message_reaction_remove(self, reaction: Reaction):
        """为消息删除表情表态"""
        _log.info(f"表情 {reaction.emoji} 从消息 {reaction.message_id} 中移除")

    # DIRECT_MESSAGE 事件
    async def on_direct_message_create(self, message: DirectMessage):
        """当收到用户发给机器人的私信消息时"""
        _log.info(f"收到私信消息：{message.content}")

    async def on_direct_message_delete(self, message: DirectMessage):
        """删除（撤回）消息事件"""
        _log.info(f"私信消息 {message.content} 被删除")

    # GROUP_AND_C2C_EVENT 事件
    async def on_c2c_message_create(self, message: C2CMessage):
        """用户单聊发消息给机器人时候"""
        _log.info(f"用户 {message.sender} 发送了单聊消息：{message.content}")

    async def on_friend_add(self, user: User):
        """用户添加使用机器人"""
        _log.info(f"用户 {user.username} 添加了机器人作为好友")

    async def on_friend_del(self, user: User):
        """用户删除机器人"""
        _log.info(f"用户 {user.username} 删除了机器人")

    async def on_c2c_msg_reject(self, user: User):
        """用户在机器人资料卡手动关闭'主动消息'推送"""
        _log.info(f"用户 {user.username} 关闭了主动消息推送")

    async def on_c2c_msg_receive(self, user: User):
        """用户在机器人资料卡手动开启'主动消息'推送开关"""
        _log.info(f"用户 {user.username} 开启了主动消息推送")

    async def on_group_at_message_create(self, message: GroupMessage):
        """用户在群里@机器人时收到的消息"""
        _log.info(f"用户 {message.author} 在群 {message.group.name} @了机器人：{message.content}")

    async def on_group_add_robot(self, group: GroupManageEvent):
        """机器人被添加到群聊"""
        _log.info(f"机器人被添加到群聊")

    async def on_group_del_robot(self, group: Group):
        """机器人被移出群聊"""
        _log.info(f"机器人被移出群聊 {group.name}")

    async def on_group_msg_reject(self, group: Group):
        """群管理员主动在机器人资料页操作关闭通知"""
        _log.info(f"群 {group.name} 关闭了机器人通知")

    async def on_group_msg_receive(self, group: Group):
        """群管理员主动在机器人资料页操作开启通知"""
        _log.info(f"群 {group.name} 开启了机器人通知")

    # INTERACTION 事件
    async def on_interaction_create(self, interaction: Interaction):
        """互动事件创建时"""
        _log.info(f"互动事件 {interaction.type} 创建")

    # MESSAGE_AUDIT 事件
    async def on_message_audit_pass(self, message: MessageAudit):
        """消息审核通过"""
        _log.info(f"消息 {message.content} 审核通过")

    async def on_message_audit_reject(self, message: MessageAudit):
        """消息审核不通过"""
        _log.info(f"消息 {message.content} 审核未通过")

    # FORUMS_EVENT 事件
    async def on_forum_thread_create(self, thread: ForumThread):
        """当用户创建主题时"""
        _log.info(f"用户创建了主题 {thread.title}")

    async def on_forum_thread_update(self, thread: ForumThread):
        """当用户更新主题时"""
        _log.info(f"用户更新了主题 {thread.title}")

    async def on_forum_thread_delete(self, thread: ForumThread):
        """当用户删除主题时"""
        _log.info(f"用户删除了主题 {thread.title}")

    async def on_forum_post_create(self, post: ForumPost):
        """当用户创建帖子时"""
        _log.info(f"用户创建了帖子 {post.title}")

    async def on_forum_post_delete(self, post: ForumPost):
        """当用户删除帖子时"""
        _log.info(f"用户删除了帖子 {post.title}")

    async def on_forum_reply_create(self, reply: ForumReply):
        """当用户回复评论时"""
        _log.info(f"用户回复了评论 {reply.content}")

    async def on_forum_reply_delete(self, reply: ForumReply):
        """当用户回复评论时"""
        _log.info(f"用户删除了评论 {reply.content}")

    async def on_forum_publish_audit_result(self, publish: ForumPublishAudit):
        """当用户发表审核通过时"""
        _log.info(f"用户发表的 {publish.post_title} 审核通过")

    # AUDIO_ACTION 事件
    async def on_audio_start(self, audio: AudioAction):
        """音频开始播放时"""
        _log.info(f"音频开始播放：{audio.url}")

    async def on_audio_finish(self, audio: AudioAction):
        """音频播放结束时"""
        _log.info(f"音频播放结束：{audio.url}")

    async def on_audio_on_mic(self, audio: AudioAction):
        """上麦时"""
        _log.info(f"用户上麦：{audio.user}")

    async def on_audio_off_mic(self, audio: AudioAction):
        """下麦时"""
        _log.info(f"用户下麦：{audio.user}")

    # PUBLIC_GUILD_MESSAGES 事件
    async def on_at_message_create(self, message: Message):
        """当收到@机器人的消息时"""
        _log.info(f"@机器人消息：{message.content}")

    async def on_public_message_delete(self, message: PublicMessage):
        """当频道的消息被删除时"""
        _log.info(f"频道消息 {message.content} 被删除")

    async def on_message_update(self, message):
        """当频道的消息被修改时"""
        _log.info(f"频道消息 {message.content} 被修改")

    async def on_message_create(self, message: Message):
        """发送消息事件，代表频道内的全部消息，而不只是 at 机器人的消息。内容与 AT_MESSAGE_CREATE 相同"""
        _log.info(f"收到消息：{message}")
        _log.info(f"消息 {message.content} 在频道 {message.channel_id} 创建")
