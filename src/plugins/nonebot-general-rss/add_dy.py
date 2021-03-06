from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from .nonebot_guild_patch import GuildMessageEvent
from .RSS import my_trigger as tr
from .RSS import rss_class

RSS_ADD = on_command(
    "add",
    aliases={"添加订阅", "sub"},
    rule=to_me(),
    priority=5,
    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,
)


@RSS_ADD.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("RSS_ADD", args)


prompt = """\
请输入
    名称 [订阅地址]
空格分割、[]表示可选
私聊默认订阅到当前账号，群聊默认订阅到当前群组
更多信息可通过 change 命令修改\
"""


@RSS_ADD.got("RSS_ADD", prompt=prompt)
async def handle_rss_add(event: Event, rss_dy_link: str = ArgPlainText("RSS_ADD")):

    user_id = event.get_user_id()
    group_id = None
    guild_channel_id = None

    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    if isinstance(event, GuildMessageEvent):
        user_id = None
        guild_channel_id = str(event.guild_id) + "@" + str(event.channel_id)

    dy = rss_dy_link.split(" ")

    rss = rss_class.Rss()
    # 判断是否有该名称订阅，有就将当前qq或群加入订阅
    try:
        name = dy[0]
    except IndexError:
        await RSS_ADD.finish("❌ 输入的订阅名为空！")

    async def add_group_or_user(_group_id, _user_id, _guild_channel_id):
        if rss is not None:
            if _group_id:
                rss.add_user_or_group(group=str(_group_id))
                await tr.add_job(rss)
                await RSS_ADD.finish("👏 订阅到当前群组成功！")
            elif _user_id:
                rss.add_user_or_group(user=_user_id)
                await tr.add_job(rss)
                await RSS_ADD.finish("👏 订阅到当前账号成功！")
            else:
                rss.add_user_or_group(guild_channel=_guild_channel_id)
                await tr.add_job(rss)
                await RSS_ADD.finish("👏 订阅到当前子频道成功！")

    if rss.find_name(name=name):
        rss = rss.find_name(name=name)
        await add_group_or_user(group_id, user_id, guild_channel_id)
        return

    try:
        url = dy[1]
    except IndexError:
        await RSS_ADD.send("❌ 输入的订阅地址为空！")
        return

    # 当前名称、url都不存在
    rss.name = name
    rss.url = url
    await add_group_or_user(group_id, user_id, guild_channel_id)
