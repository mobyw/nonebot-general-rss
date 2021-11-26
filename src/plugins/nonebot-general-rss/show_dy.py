import copy

from nonebot import on_command
from nonebot import permission
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, permission, unescape
from nonebot.rule import to_me

from .RSS import rss_class

from nonebot_guild_patch import GuildMessageEvent

RSS_SHOW = on_command(
    "show",
    aliases={"查看订阅"},
    priority=5,
    permission=permission.GROUP_ADMIN | permission.GROUP_OWNER | SUPERUSER,
)


async def handle_rss_list(rss_list: list) -> str:
    rss_info_list = [f"{i.name}：{i.url}" for i in rss_list]
    rss_info_list.sort()
    msg_str = f"当前共有 {len(rss_info_list)} 条订阅：\n\n" + \
        "\n\n".join(rss_info_list)
    rss_stopped_info_list = [f"{i.name}：{i.url}" for i in rss_list if i.stop]
    if rss_stopped_info_list:
        rss_stopped_info_list.sort()
        msg_str += (
            f"\n----------------------\n"
            f"其中共有 {len(rss_stopped_info_list)} 条订阅已停止更新：\n\n"
            + "\n\n".join(rss_stopped_info_list)
        )
    return msg_str


# 不带订阅名称默认展示当前群组或账号的订阅，带订阅名称就显示该订阅的
@RSS_SHOW.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        rss_name = unescape(args)  # 如果用户发送了参数则直接赋值
    else:
        rss_name = None

    user_id = event.get_user_id()
    group_id = None
    guild_channel_id = None
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    if isinstance(event, GuildMessageEvent):
        group_id = None
        guild_channel_id = str(event.guild_id) + "@" + str(event.channel_id)

    rss = rss_class.Rss()
    if rss_name:
        rss = rss.find_name(rss_name)
        if not rss:
            await RSS_SHOW.send(f"❌ 订阅 {rss_name} 不存在！")
            return
        rss_msg = str(rss)
        if group_id:
            # 隐私考虑，不展示除当前群组外的
            if not str(group_id) in rss.group_id:
                await RSS_SHOW.send(f"❌ 当前群组未订阅 {rss_name} ")
                return
            rss_tmp = copy.deepcopy(rss)
            rss_tmp.guild_channel_id = ["*"]
            rss_tmp.group_id = [str(group_id), "*"]
            rss_tmp.user_id = ["*"]
            rss_msg = str(rss_tmp)
        elif guild_channel_id:
            # 隐私考虑，不展示除当前群组外的
            if not str(guild_channel_id) in rss.guild_channel_id:
                await RSS_SHOW.send(f"❌ 当前群组未订阅 {rss_name} ")
                return
            rss_tmp = copy.deepcopy(rss)
            rss_tmp.guild_channel_id = [str(guild_channel_id), "*"]
            rss_tmp.group_id = ["*"]
            rss_tmp.user_id = ["*"]
            rss_msg = str(rss_tmp)
        await RSS_SHOW.send(rss_msg)
        return

    if group_id:
        rss_list = rss.find_group(group=str(group_id))
        if not rss_list:
            await RSS_SHOW.send("❌ 当前群组没有任何订阅！")
            return
    elif guild_channel_id:
        rss_list = rss.find_guild_channel(guild_channel=str(guild_channel_id))
        if not rss_list:
            await RSS_SHOW.send("❌ 当前群组没有任何订阅！")
            return
    else:
        rss_list = rss.find_user(user=user_id)

    if rss_list:
        msg_str = await handle_rss_list(rss_list)
        await RSS_SHOW.send(msg_str)
    else:
        await RSS_SHOW.send("❌ 当前没有任何订阅！")
