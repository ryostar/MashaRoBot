from MashaRoBot import telethn as bot
from MashaRoBot import telethn as tbot
from MashaRoBot.events import register
from telethon import *
from telethon import Button, custom, events, functions
from MashaRoBot.helper_extra.badmedia import is_nsfw
import requests
import string 
import random 
from MashaRoBot.modules.sql_extended.nsfw_watch_sql import add_nsfwatch, rmnsfwatch, get_all_nsfw_enabled_chat, is_nsfwatch_indb
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )
@register(pattern="^/nsfw")
async def nsfw(event):
    if event.is_private:
       return   
    if event.is_group:
            pass
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("Trò chuyện này đã Bật đồng hồ NSFW")
    else:
        await event.reply("NSfw Watch đã tắt cho cuộc trò chuyện này")

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
@register(pattern="^/addnsfw")
async def nsfw_watch(event):
    if event.is_private:
       return   
    if event.is_group:
        if not await can_change_info(message=event):
            return
        else:
            pass
    if is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("Trò chuyện này đã được bật Nsfw Watch.")
        return
    add_nsfwatch(str(event.chat_id))
    await event.reply(f"**Đã thêm trò chuyện {event.chat.title} Với ID {event.chat_id} vào Cơ sở dữ liệu. Nhóm này Nội dung Nsfw sẽ bị xóa và đăng nhập vào nhóm ghi nhật ký**")

@register(pattern="^/rmnsfw ?(.*)")
async def disable_nsfw(event):
    if event.is_private:
       return   
    if event.is_group:
        if not await can_change_info(message=event):
            return
        else:
            pass
    if not is_nsfwatch_indb(str(event.chat_id)):
        await event.reply("Trò chuyện này chưa bật Nsfw Watch.")
        return
    rmnsfwatch(str(event.chat_id))
    await event.reply(f"**Đã xóa trò chuyện {event.chat.title} Với Id {event.chat_id} Của Nsfw Watch**")
    
@bot.on(events.NewMessage())        
async def ws(event):
    warner_starkz = get_all_nsfw_enabled_chat()
    if len(warner_starkz) == 0:
        return
    if not is_nsfwatch_indb(str(event.chat_id)):
        return
    if not event.media:
        return
    if not (event.gif or event.video or event.video_note or event.photo or event.sticker):
        return
    hmmstark = await is_nsfw(event)
    his_id = event.sender_id
    if hmmstark is True:
        try:
            await event.delete()
            await event.client(EditBannedRequest(event.chat_id, his_id, MUTE_RIGHTS))
        except:
            pass
        lolchat = await event.get_chat()
        ctitle = event.chat.title
        if lolchat.username:
            hehe = lolchat.username
        else:
            hehe = event.chat_id
        wstark = await event.client.get_entity(his_id)
        if wstark.username:
            ujwal = wstark.username
        else:
            ujwal = wstark.id
        try:
            await tbot.send_message(event.chat_id, f"**#NSFW_WATCH** \n**Nhóm :** `{hehe}` \n**Nsfw Sender - Người dùng / Bot :** `{ujwal}` \n**Tiêu đề trò chuyện:** `{ctitle}`")  
            return
        except:
            return


__help__ = """
Thổ dân có thể bảo vệ nhóm của bạn khỏi những người gửi NSFW
 ❍ /addnsfw*:* Thêm Nhóm vào Danh sách Xem nsfw
 ❍ /rmnsfw*:* Xóa nhóm khỏi danh sách xem nsfw
"""

__mod_name__ = "Lọc 🔞"
