"""AFK Plugin for @UniBorg
Syntax: .afk REASON"""
import asyncio
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from userbot import CMD_HELP
from userbot.utils import admin_cmd

global USER_AFK 
global afk_time 
global last_afk_message
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@borg.on(events.NewMessage(outgoing=True)) 
async def set_not_afk(event):
    global USER_AFK
    global afk_time 
    global last_afk_message 
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in USER_AFK: 
        shite = await borg.send_message(
            event.chat_id,
            "__Back alive!__\n**No Longer afk.**\n `Was afk for:``"
            + total_afk_time
            + "`",
        )
        try:
            await borg.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID, 
                "#AFKFALSE \nSet AFK mode to False\n"
                + "__Back alive!__\n**No Longer afk.**\n `Was afk for:``"
                + total_afk_time
                + "`",
            )
        except Exception as e:
            await borg.send_message( 
                event.chat_id,
                "Please set `PRIVATE_GROUP_BOT_API_ID` "
                + "for the proper functioning of afk functionality "
                + "check pinned message in @catuserbot17.\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True,
            )
        await asyncio.sleep(5)
        await shite.delete()
        USER_AFK = {} 
        afk_time = None


@borg.on(
    events.NewMessage( 
        incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
    )
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK
    global afk_time
    global last_afk_message 
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot: 
        msg = None
        message_to_reply = (
            f"__My Master Has Been In afk For__ `{total_afk_time}`\nWhere He Is: ONLY GOD KNOWS "
            + f"\n\n__I promise He'll back in a few light years__\n**REASON**: {reason}"
            if reason
            else f"**Heya!**\n__I am currently unavailable. Since when, you ask? For {total_afk_time} I guess.__\n\nWhen will I be back? Soon __Whenever I feel like it__**( ಠ ʖ̯ ಠ)**  "
        )
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in last_afk_message: 
            await last_afk_message[event.chat_id].delete()  
        last_afk_message[event.chat_id] = msg 


@borg.on(admin_cmd(pattern=r"afk ?(.*)", outgoing=True)) 
async def _(event):
    if event.fwd_from:
        return
    global USER_AFK  
    global afk_time 
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    if not USER_AFK: 
        last_seen_status = await borg(  
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USER_AFK = f"yes: {reason}" 
        if reason:
            await borg.send_message(
                event.chat_id, f"**I shall be Going afk!** __because ~ {reason}__"
            )
        else:
            await borg.send_message(event.chat_id, f"**I am Going afk!**")
        await asyncio.sleep(5)
        await event.delete()
        try:
            await borg.send_message(  
                Config.PRIVATE_GROUP_BOT_API_ID, 
                f"#AFKTRUE \nSet AFK mode to True, and Reason is {reason}",
            )
        except Exception as e: 
            logger.warn(str(e))  


CMD_HELP.update(
    {
        "afk": ".afk [Optional Reason]\
\n**Usage : **Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
\nafk means away from keyboard/keypad.\
"
    }
)
