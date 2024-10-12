from datetime import datetime
from typing import List, Type
from dataclasses import dataclass


class User:
    """用户对象(User)"""

    def __init__(self,
                 id: str,
                 username: str,
                 avatar: str,
                 share_url: str,
                 welcome_msg: str,
                 bot: bool = True,
                 union_openid: str | None = None,
                 union_user_account: str | None = None):
        """
        用户对象(User)\n
        用户对象中所涉及的 ID 类数据，都仅在机器人场景流通，与真实的 ID 无关。请不要理解为真实的 ID
        :param id: 用户 id
        :param username: 用户名
        :param avatar: 用户头像地址
        :param bot: 是否是机器人
        :param share_url: 官方文档未给。推测为机器人分享链接
        :param welcome_msg: 官方文档未给，无法推测作用
        :param union_openid: 特殊关联应用的 openid，需要特殊申请并配置后才会返回。如需申请（新版API好像会直接提供），请联系平台运营人员。（否则为None）
        :param union_user_account: 机器人关联的互联应用的用户信息，与union_openid关联的应用是同一个。如需申请，请联系平台运营人员。（否则为None）
        """
        self.welcome_msg = welcome_msg
        self.union_openid = union_openid
        self.union_user_account = union_user_account
        self.share_url = share_url
        self.bot = bot
        self.avatar = avatar
        self.username = username
        self.id = id


class Channel:
    """子频道对象(Channel)"""

    def __init__(self,
                 id: str,
                 guild_id: str,
                 name: str,
                 type: int,
                 sub_type: int,
                 position: int,
                 parent_id: str,
                 owner_id: str,
                 private_type: int,
                 speak_permission: int,
                 application_id: str,
                 permissions: str):
        """
        子频道对象(Channel)\n
        子频道对象中所涉及的 ID 类数据，都仅在机器人场景流通，与真实的 ID 无关。请不要理解为真实的 ID
        :param id: 子频道 id
        :param guild_id: 频道 id
        :param name: 子频道名
        :param type: 子频道类型
        :param sub_type: 子频道子类型
        :param position: 排序值，具体请参考
        :param parent_id: 所属分组 id，仅对子频道有效，对 子频道分组（ChannelType=4） 无效
        :param owner_id: 创建人 id
        :param private_type: 子频道私密类型
        :param speak_permission: 子频道发言权限
        :param application_id: 用于标识应用子频道应用类型，仅应用子频道时会使用该字段，具体定义请参考
        :param permissions: 用户拥有的子频道权限
        """
        self.id = id
        self.guild_id = guild_id
        self.name = name
        self.type = type
        self.sub_type = sub_type
        self.position = position
        self.parent_id = parent_id
        self.owner_id = owner_id
        self.private_type = private_type
        self.speak_permission = speak_permission
        self.application_id = application_id
        self.permissions = permissions


class Guild:
    """频道对象(Guild)"""

    def __init__(self,
                 id: str,
                 name: str,
                 icon: str,
                 owner_id: str,
                 owner: str,
                 member_count: int,
                 max_member: int,
                 description: str,
                 joined_at: str):
        """
        频道对象(Guild)\n
        频道对象中所涉及的 ID 类数据，都仅在机器人场景流通，与真实的 ID 无关。请不要理解为真实的 ID -私信场景下的 guild_id 为私信临时频道的 ID，获取私信来源频道信息请使用 src_guild_id
        :param id: 频道ID
        :param name: 频道名称
        :param icon: 频道头像地址
        :param owner_id: 创建人用户ID
        :param owner: 当前人是否是创建人
        :param member_count: 成员数
        :param max_member: 最大成员数
        :param description: 描述
        :param joined_at: 加入时间
        """
        self.id = id
        self.name = name
        self.icon = icon
        self.owner_id = owner_id
        self.owner = owner
        self.member_count = member_count
        self.max_member = max_member
        self.description = description
        self.joined_at = joined_at
    def __str__(self):
        return self.id


class Role:
    """身份组对象(Role)"""

    def __init__(self,
                 id: str,
                 name: str,
                 color: int,
                 hoist: int,
                 number: int,
                 member_limit: int):
        """
        身份组对象(Role)\n
        :param id: 身份组ID
        :param name: 名称
        :param color: ARGB的HEX十六进制颜色值转换后的十进制数值
        :param hoist: 是否在成员列表中单独展示: 0-否1-是
        :param number: 人数
        :param member_limit: 成员上限
        """
        self.id = id
        self.name = name
        self.color = color
        self.hoist = hoist
        self.number = number
        self.member_limit = member_limit


class Member:
    """成员对象(Member)"""

    def __init__(self,
                 user: User,
                 nick: str,
                 roles: List[Role],
                 joined_at: datetime):
        """
        成员对象(Member)\n
        :param user: 用户的频道基础信息
        :param nick: 用户的昵称
        :param roles: 用户在频道内的身份组对象列表
        :param joined_at: 用户加入频道的时间，ISO8601格式的timestamp
        """
        self.user = user
        self.nick = nick
        self.roles = roles if roles is not None else []
        self.joined_at = joined_at


class MemberWithGuildID:
    """带频道ID的成员对象(MemberWithGuildID)"""

    def __init__(self,
                 guild_id: str,
                 user: User,
                 nick: str,
                 roles: List[str],
                 joined_at: datetime):
        """
        带频道ID的成员对象(MemberWithGuildID)\n
        :param guild_id: 频道ID
        :param user: 用户的频道基础信息
        :param nick: 用户的昵称
        :param roles: 用户在频道内的身份组ID列表
        :param joined_at: 用户加入频道的时间，ISO8601格式的timestamp
        """
        self.guild_id = guild_id
        self.user = user
        self.nick = nick
        self.roles = roles if roles is not None else []
        self.joined_at = joined_at


class ChannelPermissions:
    """子频道权限对象(ChannelPermissions)"""

    def __init__(self, channel_id: str, user_id_role_id: str, permissions: str):
        """
        子频道权限对象(ChannelPermissions)
        :param channel_id: 子频道 id
        :param user_id_role_id: 用户 id 或 身份组 id，只会返回其中之一
        :param permissions: 用户拥有的子频道权限
        """
        self.channel_id = channel_id
        self.user_id_role_id = user_id_role_id
        self.permissions = permissions


class MessageAttachment:
    """代表消息中附带的附件"""

    def __init__(self, attachment_url: str):
        """
        初始化消息附件实例
        :param attachment_url: 附件的下载链接
        """
        self.attachment_url = attachment_url


class MessageEmbedThumbnail:
    """代表消息嵌入的缩略图"""

    def __init__(self, thumbnail_url: str):
        """
        初始化消息嵌入缩略图实例
        :param thumbnail_url: 缩略图的图片地址
        """
        self.url = thumbnail_url


class MessageEmbedField:
    """代表消息嵌入中的字段"""

    def __init__(self, field_name: str):
        """
        初始化消息嵌入字段实例
        :param field_name: 字段名
        """
        self.name = field_name


class MessageArkObjKv:
    """代表消息结构中的键值对对象"""

    def __init__(self, key: str, value: str):
        """
        初始化消息键值对实例
        :param key: 键
        :param value: 值
        """
        self.key = key
        self.value = value


class MessageArkObj:
    """代表消息结构中的Ark对象"""

    def __init__(self, obj_kv: MessageArkObjKv):
        """
        初始化消息Ark对象实例
        :param obj_kv: MessageArkObjKv类型的数组，ark objkv列表
        """
        self.obj_kv = obj_kv


class MessageArkKv:
    """代表消息结构中的键值对，可能包含Ark对象"""

    def __init__(self, key: str, value: str, obj: MessageArkObj):
        """
        初始化消息键值对实例，可能包含Ark对象
        :param key: 键
        :param value: 值
        :param obj: MessageArkObj类型的列表，ark obj列表
        """
        self.key = key
        self.value = value
        self.obj = obj


class MessageArk:
    """代表消息结构中的Ark模板"""

    def __init__(self, template_id: int, kv: list):
        """
        初始化消息Ark模板实例
        :param template_id: int，ark模板id（需要先申请）
        :param kv: list，MessageArkKv类型的数组，kv值列表
        """
        self.template_id = template_id
        self.kv = kv


class MessageEmbed:
    """代表消息嵌入对象"""

    def __init__(self, title: str, prompt: str, thumbnail: MessageEmbedThumbnail, fields: MessageEmbedField):
        """
        初始化消息嵌入对象实例
        :param title: 标题
        :param prompt: 消息弹窗内容
        :param thumbnail: MessageEmbedThumbnail对象，缩略图
        :param fields: MessageEmbedField对象数组，embed字段数据
        """
        self.title = title
        self.prompt = prompt
        self.thumbnail = thumbnail
        self.fields = fields


class MessageReference:
    """代表消息引用对象"""

    def __init__(self, message_id: str, ignore_get_message_error: bool = False):
        """
        初始化消息引用对象实例
        :param message_id: 需要引用回复的消息 id
        :param ignore_get_message_error: 是否忽略获取引用消息详情错误，默认为False
        """
        self.message_id = message_id
        self.ignore_get_message_error = ignore_get_message_error


class MessageAudited:
    """消息审核对象(MessageAudited)"""

    def __init__(self, audit_id: str, message_id: str, guild_id: str, channel_id: str, audit_time: datetime,
                 create_time: datetime, seq_in_channel: str):
        """
        初始化消息审核对象实例
        :param audit_id: 消息审核 id
        :param message_id: 消息 id，只有审核通过事件才会有值
        :param guild_id: 频道 id
        :param channel_id: 子频道 id
        :param audit_time: ISO8601 timestamp，消息审核时间
        :param create_time: ISO8601 timestamp，消息创建时间
        :param seq_in_channel: 子频道消息 seq，用于消息间的排序，seq 在同一子频道中按从先到后的顺序递增，不同的子频道之间消息无法排序
        """
        self.audit_id = audit_id
        self.message_id = message_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.audit_time = audit_time
        self.create_time = create_time
        self.seq_in_channel = seq_in_channel


class InlineKeyboard:
    """代表内联键盘对象，用于展示消息按钮组件"""

    def __init__(self, rows: list):
        """
        初始化内联键盘对象实例
        :param rows: InlineKeyboardRow消息按钮组件行对象数组，数组的一项代表消息按钮组件的一行，最多含有5行
        """
        self.rows = rows


class InlineKeyboardRow:
    """代表内联键盘的一行，包含多个按钮"""

    def __init__(self, buttons: list):
        """
        初始化内联键盘行对象实例
        :param buttons: Button按钮对象数组，数组的一项代表一个按钮，每个InlineKeyboardRow最多含有5个Button
        """
        self.buttons = buttons


class RenderStyle:
    """代表渲染样式的枚举类"""

    def __init__(self, style: int):
        """
        初始化渲染样式实例
        :param style: int，渲染样式的值，0代表灰色线框，1代表蓝色线框
        """
        if style not in [0, 1]:
            raise ValueError("无效的渲染样式. 要求：0 (灰色线框) 或 1 (蓝色线框).")
        self.style = style


class RenderData:
    """代表按钮的渲染数据"""

    def __init__(self, label: str, visited_label: str, style: int):
        """
        初始化按钮渲染数据实例
        :param label: string，按钮上的文字
        :param visited_label: string，点击后按钮上的文字
        :param style: int，按钮样式，参考 RenderStyle
        """
        self.label = label
        self.visited_label = visited_label
        self.style = style


class PermissionType:
    """代表权限类型的枚举类"""

    SPECIFIED_USER = 0
    MANAGER_ONLY = 1
    EVERYONE = 2
    SPECIFIED_ROLE = 3

    def __init__(self, permission_type: int):
        """
        初始化权限类型实例
        :param permission_type: int，权限类型的值
        """
        if permission_type not in [self.SPECIFIED_USER, self.MANAGER_ONLY, self.EVERYONE, self.SPECIFIED_ROLE]:
            raise ValueError("无效的权限类型。必须是0（指定用户）、1（仅管理员）、2（所有人）或3（指定角色）。")
        self.permission_type = permission_type


class Permission:
    """代表权限配置对象"""

    def __init__(self, type: int, specify_role_ids: list = None, specify_user_ids: list = None):
        """
        初始化权限配置实例
        :param type: int，权限类型，参考 PermissionType
        :param specify_role_ids: string数组，有权限的身份组id的列表
        :param specify_user_ids: string数组，有权限的用户id的列表
        """
        self.type = type
        self.specify_role_ids = specify_role_ids if specify_role_ids is not None else []
        self.specify_user_ids = specify_user_ids if specify_user_ids is not None else []


class ActionType:
    """代表动作类型的枚举类"""

    HTTP_OR_MINI_PROGRAM = 0
    CALLBACK_BACKEND_INTERFACE = 1
    AT_BOT = 2

    def __init__(self, action_type: int):
        """
        初始化动作类型实例
        :param action_type: int，动作类型的值
        """
        if action_type not in [self.HTTP_OR_MINI_PROGRAM, self.CALLBACK_BACKEND_INTERFACE, self.AT_BOT]:
            raise ValueError("无效的操作类型。必须是0（http或小程序）、1（回调后端接口）或2（@机器人）。")
        self.action_type = action_type


class Action:
    """代表操作按钮的行为配置对象"""

    def __init__(self, type: int, permission: Permission, click_limit: int = None, data: str = "",
                 at_bot_show_channel_list: bool = False):
        """
        初始化操作按钮的行为配置实例
        :param type: int，操作类型，参考 ActionType
        :param permission: Permission对象，用于设定操作按钮所需的权限
        :param click_limit: int，可点击的次数，默认不限
        :param data: string，操作相关数据
        :param at_bot_show_channel_list: bool，false:不弹出子频道选择器 true:弹出子频道选择器
        """
        self.type = type
        self.permission = permission
        self.click_limit = click_limit
        self.data = data
        self.at_bot_show_channel_list = at_bot_show_channel_list


class Button:
    """代表消息按钮组件的按钮对象"""

    def __init__(self, button_id: str, render_data: RenderData, action: Action):
        """
        初始化消息按钮组件的按钮实例
        :param button_id: string，按钮 id
        :param render_data: RenderData，按钮渲染展示对象，用于设定按钮的显示效果
        :param action: Action，该按钮操作相关字段，用于设定按钮点击后的操作
        """
        self.id = button_id
        self.render_data = render_data
        self.action = action


class Message:
    """代表消息对象"""

    def __init__(self, id: str, channel_id: str, guild_id: str, content: str, timestamp: datetime,
                 edited_timestamp: datetime,
                 mention_everyone: bool, author: User, attachments: list, embeds: list, mentions: List[User],
                 member: Member, ark: MessageArk, seq: int, seq_in_channel: str, message_reference: 'MessageReference',
                 src_guild_id: str):
        """
        初始化消息对象实例
        :param id: string，消息 id
        :param channel_id: string，子频道 id
        :param guild_id: string，频道 id
        :param content: string，消息内容
        :param timestamp: ISO8601 timestamp，消息创建时间
        :param edited_timestamp: ISO8601 timestamp，消息编辑时间
        :param mention_everyone: bool，是否是@全员消息
        :param author: User对象，消息创建者
        :param attachments: MessageAttachment对象数组，附件
        :param embeds: MessageEmbed对象数组，embed
        :param mentions: User对象数组，消息中@的人
        :param member: Member对象，消息创建者的member信息
        :param ark: MessageArk对象，ark消息
        :param seq: int，用于消息间的排序，seq在同一子频道中按从先到后的顺序递增，不同的子频道之间消息无法排序。(目前只在消息事件中有值，2022年8月1日后续废弃)
        :param seq_in_channel: string，子频道消息 seq，用于消息间的排序，seq在同一子频道中按从先到后的顺序递增，不同的子频道之间消息无法排序
        :param message_reference: MessageReference对象，引用消息对象
        :param src_guild_id: string，用于私信场景下识别真实的来源频道id
        """
        self.id = id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.content = content
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.mention_everyone = mention_everyone
        self.author = author
        self.attachments = attachments
        self.embeds = embeds
        self.mentions = mentions
        self.member = member
        self.ark = ark
        self.seq = seq
        self.seq_in_channel = seq_in_channel
        self.message_reference = message_reference
        self.src_guild_id = src_guild_id


class MessageMarkdownParams:
    """代表消息Markdown参数对象"""

    def __init__(self, key: str, values: list[str]):
        """
        初始化消息Markdown参数实例
        :param key: string，markdown模版key
        :param values: string类型的数组，markdown模版key对应的values，列表长度大小为1，传入多个会报错
        """
        if len(values) != 1:
            raise ValueError("列表的长度必须是1。")
        self.key = key
        self.values = values


class MessageMarkdown:
    """代表消息Markdown对象"""

    def __init__(self, template_id: int, custom_template_id: str, params: MessageMarkdownParams, content: str):
        """
        初始化消息Markdown实例
        :param template_id: int，markdown模板id
        :param custom_template_id: string，markdown自定义模板id
        :param params: MessageMarkdownParams，markdown模板参数
        :param content: string，原生markdown内容,与上面三个参数互斥,参数都传值将报错。
        """
        if template_id and custom_template_id and params and content:
            raise ValueError("只能提供template_id、custom_template_id、params或content中的一个。")
        self.template_id = template_id
        self.custom_template_id = custom_template_id
        self.params = params
        self.content = content


class MessageDelete:
    """代表消息删除事件的对象"""

    def __init__(self, message: Message, op_user: User):
        """
        初始化消息删除事件实例
        :param message: Message对象，被删除的消息内容
        :param op_user: User对象，执行删除操作的用户
        """
        self.message = message
        self.op_user = op_user


class MessageKeyboard:
    """定义消息中的键盘布局"""

    def __init__(self, keyboard_id: str, content: 'InlineKeyboard'):
        """
        初始化消息键盘实例
        :param keyboard_id: str，键盘模板的ID
        :param content: InlineKeyboard，自定义键盘内容
        """
        if keyboard_id and content:
            raise ValueError("keyboard_id和content参数不能同时提供。")
        self.keyboard_id = keyboard_id
        self.content = content


class MessageSetting:
    """频道消息频率设置对象 (MessageSetting)"""

    def __init__(self, disable_create_dm: str, disable_push_msg: str, channel_ids: list, channel_push_max_num: int):
        """
        初始化频道消息频率设置实例
        :param disable_create_dm: string，是否允许创建私信
        :param disable_push_msg: string，是否允许发主动消息
        :param channel_ids: list，子频道id数组
        :param channel_push_max_num: int，每个子频道允许主动推送消息的最大消息条数
        """
        self.disable_create_dm = disable_create_dm
        self.disable_push_msg = disable_push_msg
        self.channel_ids = channel_ids
        self.channel_push_max_num = channel_push_max_num


class DMS:
    """私信会话对象（DMS）"""

    def __init__(self, guild_id: str, channel_id: str, create_time: str):
        """
        初始化私信会话对象实例
        :param guild_id: string，私信会话关联的频道id
        :param channel_id: string，私信会话关联的子频道id
        :param create_time: string，创建私信会话的时间戳
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.create_time = create_time


class Announce:
    """公告对象(Announces)"""

    def __init__(self, guild_id: str, channel_id: str, message_id: str, announces_type: int, recommend_channels: list):
        """
        初始化公告对象实例
        :param guild_id: string，频道id
        :param channel_id: string，子频道id
        :param message_id: string，消息id
        :param announces_type: int，公告类别 0:成员公告 1:欢迎公告，默认成员公告
        :param recommend_channels: list，RecommendChannel数组，推荐子频道详情列表
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.announces_type = announces_type
        self.recommend_channels = recommend_channels


class RecommendChannel:
    """推荐子频道对象(RecommendChannel)"""

    def __init__(self, channel_id: str, introduce: str):
        """
        初始化推荐子频道对象实例
        :param channel_id: string，子频道id
        :param introduce: string，推荐语
        """
        self.channel_id = channel_id
        self.introduce = introduce


class PinsMessage:
    """精华消息对象(PinsMessage)"""

    def __init__(self, guild_id: str, channel_id: str, message_ids: list):
        """
        初始化精华消息对象实例
        :param guild_id: string，频道id
        :param channel_id: string，子频道id
        :param message_ids: list，子频道内精华消息id数组
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_ids = message_ids


class RemindType:
    """提醒类型枚举类"""

    NO_REMIND = 0
    BEGIN_REMIND = 1
    FIVE_MINUTES_BEFORE_BEGIN = 2
    FIFTEEN_MINUTES_BEFORE_BEGIN = 3
    THIRTY_MINUTES_BEFORE_BEGIN = 4
    SIXTY_MINUTES_BEFORE_BEGIN = 5

    def __init__(self, remind_type_id: int):
        """
        初始化提醒类型实例
        :param remind_type_id: int，提醒类型id
        """
        if remind_type_id not in [self.NO_REMIND, self.BEGIN_REMIND, self.FIVE_MINUTES_BEFORE_BEGIN,
                                  self.FIFTEEN_MINUTES_BEFORE_BEGIN, self.THIRTY_MINUTES_BEFORE_BEGIN,
                                  self.SIXTY_MINUTES_BEFORE_BEGIN]:
            raise ValueError(
                "无效的提醒类型。必须是0（不提醒）、1（开始时提醒）、2（开始前5分钟提醒）、3（开始前15分钟提醒）、4（开始前30分钟提醒）或5（开始前60分钟提醒）。")
        self.remind_type_id = remind_type_id


class Schedule:
    """日程对象(Schedule)"""

    def __init__(self, id: str, name: str, description: str, start_timestamp: str, end_timestamp: str,
                 creator: 'Member', jump_channel_id: str, remind_type: str):
        """
        初始化日程对象实例
        :param id: string，日程id
        :param name: string，日程名称
        :param description: string，日程描述
        :param start_timestamp: string，日程开始时间戳(ms)
        :param end_timestamp: string，日程结束时间戳(ms)
        :param creator: Member，创建者
        :param jump_channel_id: string，日程开始时跳转到的子频道id
        :param remind_type: string，日程提醒类型，取值参考RemindType
        """
        self.id = id
        self.name = name
        self.description = description
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.creator = creator
        self.jump_channel_id = jump_channel_id
        self.remind_type = remind_type


class Emoji:
    """表情对象(Emoji)"""

    def __init__(self, id: str, type: int):
        """
        初始化表情对象实例
        :param id: string，表情ID，系统表情使用数字为ID，emoji使用emoji本身为id
        :param type: uint32，表情类型，参考EmojiType
        """
        self.id = id
        self.type = type


class MessageReaction:
    """消息表态对象(MessageReaction)"""

    def __init__(self, user_id: str, guild_id: str, channel_id: str, target: 'ReactionTarget', emoji: 'Emoji'):
        """
        初始化消息表态对象实例
        :param user_id: string，用户ID
        :param guild_id: string，频道ID
        :param channel_id: string，子频道ID
        :param target: ReactionTarget，表态对象
        :param emoji: Emoji，表态所用表情
        """
        self.user_id = user_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.target = target
        self.emoji = emoji


class ReactionTarget:
    """表态对象类型(ReactionTarget)"""

    def __init__(self, id: str, type: int):
        """
        初始化表态对象类型实例
        :param id: string，表态对象ID
        :param type: ReactionTargetType，表态对象类型，参考 ReactionTargetType
        """
        self.id = id
        self.type = type


class STATUS:
    """播放状态枚举类"""

    START = 0
    PAUSE = 1
    RESUME = 2
    STOP = 3

    def __init__(self, status_value: int):
        """
        初始化播放状态实例
        :param status_value: int，播放状态值
        """
        if status_value not in [self.START, self.PAUSE, self.RESUME, self.STOP]:
            raise ValueError("无效的状态。必须是0（开始）、1（暂停）、2（继续）或3（停止）。")
        self.status_value = status_value


class AudioAction:
    """音频操作对象(AudioAction)"""

    def __init__(self, guild_id: str, channel_id: str, audio_url: str = None, text: str = None, status: int = None):
        """
        初始化音频操作对象实例
        :param guild_id: string，频道id
        :param channel_id: string，子频道id
        :param audio_url: string，音频数据的url，status为0时传
        :param text: string，状态文本（比如：简单爱-周杰伦），可选，status为0时传，其他操作不传
        :param status: int，播放状态，参考STATUS
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.audio_url = audio_url
        self.text = text
        self.status = status


class AudioControl:
    """音频控制对象(AudioControl)"""

    def __init__(self, audio_url: str = None, text: str = None, status: int = None):
        """
        初始化音频控制对象实例
        :param audio_url: string，音频数据的url，status为0时传
        :param text: string，状态文本（比如：简单爱-周杰伦），可选，status为0时传，其他操作不传
        :param status: int，播放状态，参考STATUS
        """
        self.audio_url = audio_url
        self.text = text
        self.status = status


class ThreadInfo:
    """帖子事件包含的主帖内容相关信息类"""

    def __init__(self, thread_id: str, title: str, content: str, date_time: datetime):
        """
        初始化帖子事件包含的主帖内容相关信息实例
        :param thread_id: string，主帖ID
        :param title: string，帖子标题
        :param content: string，帖子内容
        :param date_time: ISO8601 timestamp，发表时间
        """
        self.thread_id = thread_id
        self.title = title
        self.content = content
        self.date_time = date_time


class Post:
    """帖子对象(Post)"""

    def __init__(self, guild_id: str, channel_id: str, author_id: str, post_info: object):
        """
        初始化帖子对象实例
        :param guild_id: string，频道ID
        :param channel_id: string，子频道ID
        :param author_id: string，作者ID
        :param post_info: object，PostInfo对象，帖子内容
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.author_id = author_id
        self.post_info = post_info


class ReplyInfo:
    """回复事件包含的回复内容信息类"""

    def __init__(self, thread_id: str, post_id: str, reply_id: str, content: str, date_time: str):
        """
        初始化回复事件包含的回复内容信息实例
        :param thread_id: string，主题ID
        :param post_id: string，帖子ID
        :param reply_id: string，回复ID
        :param content: string，回复内容
        :param date_time: string，回复时间
        """
        self.thread_id = thread_id
        self.post_id = post_id
        self.reply_id = reply_id
        self.content = content
        self.date_time = date_time


class Reply:
    """回复对象(Reply)"""

    def __init__(self, guild_id: str, channel_id: str, author_id: str, reply_info: ReplyInfo):
        """
        初始化回复对象实例
        :param guild_id: string，频道ID
        :param channel_id: string，子频道ID
        :param author_id: string，作者ID
        :param reply_info: object，ReplyInfo对象，回复内容
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.author_id = author_id
        self.reply_info = reply_info


class Thread:
    """主题对象(Thread)"""

    def __init__(self, guild_id: str, channel_id: str, author_id: str, thread_info: object):
        """
        初始化主题对象实例
        :param guild_id: string，频道ID
        :param channel_id: string，子频道ID
        :param author_id: string，作者ID
        :param thread_info: object，ThreadInfo对象，主帖内容
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.author_id = author_id
        self.thread_info = thread_info


class AuditResult:
    """论坛帖子审核结果事件类"""

    def __init__(self, guild_id: str, channel_id: str, author_id: str, thread_id: str, post_id: str, reply_id: str,
                 type: int, result: int, err_msg: str):
        """
        初始化论坛帖子审核结果事件实例
        :param guild_id: string，频道ID
        :param channel_id: string，子频道ID
        :param author_id: string，作者ID
        :param thread_id: string，主题ID
        :param post_id: string，帖子ID
        :param reply_id: string，回复ID
        :param type: uint32，AuditType审核的类型
        :param result: uint32，审核结果. 0:成功 1:失败
        :param err_msg: string，result不为0时错误信息
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.author_id = author_id
        self.thread_id = thread_id
        self.post_id = post_id
        self.reply_id = reply_id
        self.type = type
        self.result = result
        self.err_msg = err_msg


class RichType:
    """富文本类型枚举类"""

    TEXT = 1
    AT = 2
    URL = 3
    EMOJI = 4
    CHANNEL = 5
    VIDEO = 10
    IMAGE = 11

    def __init__(self, rich_type_value: int):
        """
        初始化富文本类型实例
        :param rich_type_value: int，富文本类型值
        """
        if rich_type_value not in [self.TEXT, self.AT, self.URL, self.EMOJI, self.CHANNEL, self.VIDEO, self.IMAGE]:
            raise ValueError("无效的富文本类型。必须是1（文本）、2（@提及）、3（链接）、4（表情）、5（频道）、10（视频）或11（图片）。")
        self.rich_type_value = rich_type_value


class TextInfo:
    """富文本 - 普通文本类"""

    def __init__(self, text: str):
        """
        初始化富文本 - 普通文本实例
        :param text: string，普通文本
        """
        self.text = text


class AtUserInfo:
    """@用户信息类"""

    def __init__(self, id: str, nick: str):
        """
        初始化@用户信息实例
        :param id: string，身份组ID
        :param nick: string，用户昵称
        """
        self.id = id
        self.nick = nick


class AtGuildInfo:
    """@频道信息类"""

    def __init__(self, guild_id: str, guild_name: str):
        """
        初始化@频道信息实例
        :param guild_id: string，频道ID
        :param guild_name: string，频道名称
        """
        self.guild_id = guild_id
        self.guild_name = guild_name


class AtRoleInfo:
    """@身份组信息类"""

    def __init__(self, role_id: int, name: str, color: int):
        """
        初始化@身份组信息实例
        :param role_id: uint64，身份组ID
        :param name: string，身份组名称
        :param color: uint32，颜色值
        """
        self.role_id = role_id
        self.name = name
        self.color = color


class URLInfo:
    """富文本 - 链接信息类"""

    def __init__(self, url: str, display_text: str):
        """
        初始化富文本 - 链接信息实例
        :param url: string，链接地址
        :param display_text: string，链接显示文本
        """
        self.url = url
        self.display_text = display_text


class EmojiInfo:
    """富文本 - Emoji信息类"""

    def __init__(self, id: str, type: str, name: str, url: str):
        """
        初始化富文本 - Emoji信息实例
        :param id: string，表情id
        :param type: string，表情类型
        :param name: string，名称
        :param url: string，链接
        """
        self.id = id
        self.type = type
        self.name = name
        self.url = url


class ChannelInfo:
    """富文本 - 子频道信息类"""

    def __init__(self, channel_id: int, channel_name: str):
        """
        初始化富文本 - 子频道信息实例
        :param channel_id: uint64，子频道id
        :param channel_name: string，子频道名称
        """
        self.channel_id = channel_id
        self.channel_name = channel_name


class AtInfo:
    """富文本 - @内容类"""

    def __init__(self, type: int, user_info: AtUserInfo, role_info: AtRoleInfo, guild_info: AtGuildInfo):
        """
        初始化富文本 - @内容实例
        :param type: AtType，at类型
        :param user_info: AtUserInfo，用户信息
        :param role_info: AtRoleInfo，角色组信息
        :param guild_info: AtGuildInfo，频道信息
        """
        self.type = type
        self.user_info = user_info
        self.role_info = role_info
        self.guild_info = guild_info


class ElemType:
    """元素类型枚举类"""

    ELEM_TYPE_TEXT = 1
    ELEM_TYPE_IMAGE = 2
    ELEM_TYPE_VIDEO = 3
    ELEM_TYPE_URL = 4

    def __init__(self, elem_type_value: int):
        """
        初始化元素类型实例
        :param elem_type_value: int，元素类型值
        """
        if elem_type_value not in [self.ELEM_TYPE_TEXT, self.ELEM_TYPE_IMAGE, self.ELEM_TYPE_VIDEO, self.ELEM_TYPE_URL]:
            raise ValueError("无效的元素类型。必须是1（文本）、2（图片）、3（视频）或4（链接）。")
        self.elem_type_value = elem_type_value


class TextProps:
    """富文本 - 文本段落属性类"""

    def __init__(self, font_bold: bool, italic: bool, underline: bool):
        """
        初始化富文本 - 文本段落属性实例
        :param font_bold: bool，加粗
        :param italic: bool，斜体
        :param underline: bool，下划线
        """
        self.font_bold = font_bold
        self.italic = italic
        self.underline = underline


class TextElem:
    """富文本 - 文本属性类"""

    def __init__(self, text: str, props: TextProps):
        """
        初始化富文本 - 文本属性实例
        :param text: string，正文
        :param props: TextProps，文本属性
        """
        self.text = text
        self.props = props


class ImageElem:
    """富文本 - 图片属性类"""

    def __init__(self, third_url: str, width_percent: float):
        """
        初始化富文本 - 图片属性实例
        :param third_url: string，第三方图片链接
        :param width_percent: float，宽度比例（缩放比，在屏幕里显示的比例）
        """
        self.third_url = third_url
        self.width_percent = width_percent


class PlatImage:
    """富文本 - 平台图片属性类"""

    def __init__(self, url: str, width: int, height: int, image_id: str):
        """
        初始化富文本 - 平台图片属性实例
        :param url: string，架平图片链接
        :param width: uint32，图片宽度
        :param height: uint32，图片高度
        :param image_id: string，图片ID
        """
        self.url = url
        self.width = width
        self.height = height
        self.image_id = image_id


class VideoElem:
    """富文本 - 视频属性类"""

    def __init__(self, third_url: str):
        """
        初始化富文本 - 视频属性实例
        :param third_url: string，第三方视频文件链接
        """
        self.third_url = third_url


class PlatVideo:
    """富文本 - 平台视频属性类"""

    def __init__(self, url: str, width: int, height: int, video_id: str, duration: int, cover: object):
        """
        初始化富文本 - 平台视频属性实例
        :param url: string，架平图片链接
        :param width: uint32，图片宽度
        :param height: uint32，图片高度
        :param video_id: string，视频ID
        :param duration: uint32，视频时长
        :param cover: PlatImage，视频封面图属性
        """
        self.url = url
        self.width = width
        self.height = height
        self.video_id = video_id
        self.duration = duration
        self.cover = cover


class ParagraphProps:
    """富文本 - 段落属性类"""

    def __init__(self, alignment: int):
        """
        初始化富文本 - 段落属性实例
        :param alignment: int，段落对齐方向属性，数值可以参考Alignment
        """
        self.alignment = alignment


class URLElem:
    """富文本 - URL属性类"""

    def __init__(self, url: str, desc: str):
        """
        初始化富文本 - URL属性实例
        :param url: string，URL链接
        :param desc: string，URL描述
        """
        self.url = url
        self.desc = desc


class RichObject:
    """富文本内容类"""

    def __init__(self, type: int, text_info: object, at_info: object, url_info: object, emoji_info: object,
                 channel_info: object):
        """
        初始化富文本内容实例
        :param type: int，RichType富文本类型
        :param text_info: TextInfo对象，文本
        :param at_info: AtInfo对象，@内容
        :param url_info: URLInfo对象，链接
        :param emoji_info: EmojiInfo对象，表情
        :param channel_info: ChannelInfo对象，提到的子频道
        """
        self.type = type
        self.text_info = text_info
        self.at_info = at_info
        self.url_info = url_info
        self.emoji_info = emoji_info
        self.channel_info = channel_info


class APIPermission:
    """接口权限对象"""

    def __init__(self, path: str, method: str, desc: str, auth_status: int):
        """
        初始化接口权限对象实例
        :param path: string，API接口名，例如 /guilds/{guild_id}/members/{user_id}
        :param method: string，请求方法，例如 GET
        :param desc: string，API接口名称，例如 获取频道信
        :param auth_status: int，授权状态，auth_status为1时已授权
        """
        self.path = path
        self.method = method
        self.desc = desc
        self.auth_status = auth_status


class APIPermissionDemandIdentify:
    """接口权限需求标识对象（APIPermissionDemandIdentify）"""

    def __init__(self, path: str, method: str):
        """
        初始化接口权限需求标识对象实例
        :param path: string，API接口名，例如 /guilds/{guild_id}/members/{user_id}
        :param method: string，请求方法，例如 GET
        """
        self.path = path
        self.method = method


class APIPermissionDemand:
    """接口权限需求对象（APIPermissionDemand）"""

    def __init__(self, guild_id: str, channel_id: str, api_identify: APIPermissionDemandIdentify, title: str,
                 desc: str):
        """
        初始化接口权限需求对象实例
        :param guild_id: string，申请接口权限的频道id
        :param channel_id: string，接口权限需求授权链接发送的子频道id
        :param api_identify: APIPermissionDemandIdentify，权限接口唯一标识
        :param title: string，接口权限链接中的接口权限描述信息
        :param desc: string，接口权限链接中的机器人可使用功能的描述信息
        """
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.api_identify = api_identify
        self.title = title
        self.desc = desc
