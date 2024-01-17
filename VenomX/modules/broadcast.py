

import asyncio

import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from requests import get

from config import BLACKLIST_GCAST
from config import CMD_HANDLER as cmd
from VenomX.helpers.adminHelpers import DEVS
from VenomX.helpers.basic import edit_or_reply
from VenomX.helpers.misc import HAPP, in_heroku
from VenomX.helpers.tools import get_arg
from VenomX.utils.misc import restart

from .help import add_command_help

while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/venombolteop/Reforestation/main/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001649838443]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST


@Client.on_message(filters.command("gcast", cmd) & filters.me)
async def gcast_cmd(client: Client, message: Message):
     if message.reply_to_message or get_arg(message):
         Man = await edit_or_reply(message, "`Started global broadcast...`")
     else:
         return await message.edit_text("**Give a Message or Reply**")
     done = 0
     error = 0
     async for dialog in client.get_dialogs():
         if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
             if message.reply_to_message:
                 msg = message. reply_to_message
             elif get_arg:
                 msg = get_arg(message)
             chat = dialog.chat.id
             if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                 try:
                     if message.reply_to_message:
                         await msg.copy(chat)
                     elif get_arg:
                         await client.send_message(chat, msg)
                     done += 1
                     await asyncio.sleep(0.3)
                 except Exception:
                     error += 1
                     await asyncio.sleep(0.3)
     await Man.edit_text(
         f"**Successful Sending Message To** `{done}` **Group, Failed To Send Message To** `{error}` **Group**"
     )


@Client.on_message(filters.command("gucast", cmd) & filters.me)
async def gucast_cmd(client: Client, message: Message):
     if message.reply_to_message or get_arg(message):
         Man = await edit_or_reply(message, "`Started global broadcast...`")
     else:
         return await message.edit_text("**Give a Message or Reply**")
     done = 0
     error = 0
     async for dialog in client.get_dialogs():
         if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
             if message.reply_to_message:
                 msg = message. reply_to_message
             elif get_arg:
                 msg = get_arg(message)
             chat = dialog.chat.id
             if chat not in DEVS:
                 try:
                     if message.reply_to_message:
                         await msg.copy(chat)
                     elif get_arg:
                         await client.send_message(chat, msg)
                     done += 1
                     await asyncio.sleep(0.3)
                 except Exception:
                     error += 1
                     await asyncio.sleep(0.3)
     await Man.edit_text(
         f"**Successful Sending Message To** `{done}` **chat, Failed To Send Message To** `{error}` **chat**"
     )


@Client.on_message(filters.command("blchat", cmd) & filters.me)
async def blchatgcast(client: Client, message: Message):
     blacklistgc = "True" if BLACKLIST_GCAST else "False"
     list = BLACKLIST_GCAST.replace(" ", "\n» ")
     if blacklistgc == "True":
         await edit_or_reply(
             message,
             f"🔮 **Blacklist GCAST:** `Enabled`\n\n📚 **Blacklist Group:**\n» {list}\n\nType `{cmd}addblacklist` in the group you want to add to the blacklist gcast.",
         )
     else:
         await edit_or_reply(message, "🔮 **Blacklist GCAST:** `Disabled`")


@Client.on_message(filters.command("addblacklist", cmd) & filters.me)
async def addblacklist(client: Client, message: Message):
     xxnx = await edit_or_reply(message, "`Processing...`")
     if HAPP is None:
         return await xxnx.edit(
             "**Please Add Var** `HEROKU_APP_NAME` **to add blacklist**",
         )
     blgc = f"{BLACKLIST_GCAST}{message.chat.id}"
     blacklistgroup = (
         blgc.replace("{", "")
         .replace("}", "")
         .replace(",", "")
         .replace("[", "")
         .replace("]", "")
         .replace("set() ", "")
     )
     await xxnx.edit(
         f"**Successfully Added** `{message.chat.id}` **to gcast blacklist.**\n\nRestarting Heroku to Apply Changes."
     )
     if await in_myhero():
         heroku_var = HAPP.config()
         heroku_var["BLACKLIST_GCAST"] = blacklistgroup
     else:
         path = dotenv.find_dotenv("config.env")
         dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgroup)
     restart()


@Client.on_message(filters.command("delblacklist", cmd) & filters.me)
async def delblacklist(client: Client, message: Message):
     xxnx = await edit_or_reply(message, "`Processing...`")
     if HAPP is None:
         return await xxnx.edit(
             "**Please Add Var** `HEROKU_APP_NAME` **to add blacklist**",
         )
     gett = str(message.chat.id)
     if gett in blchat:
         blacklistgroup = blchat.replace(gett, "")
         await xxx.edit(
             f"**Successfully Removed** `{message.chat.id}` **from gcast blacklist.**\n\nRestarting Heroku to Apply Changes."
         )
         if await in_myhero():
             heroku_var = HAPP.config()
             heroku_var["BLACKLIST_GCAST"] = blacklistgroup
         else:
             path = dotenv.find_dotenv("config.env")
             dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgroup)
         restart()
     else:
         await xxnx.edit("**This group is not on gcast's blacklist.**")

add_command_help(
     "broadcast",
     [
         [
             "gcast <text/reply>",
             "Send Global Broadcast messages to all Groups you are in. (Can Send Media/Stickers)",
         ],
         [
             "gucast <text/reply>",
             "Sending Global Broadcast messages to all incoming Private Message / PCs. (Can Send Media/Stickers)",
         ],
         [
             "blchat",
             "To check gcast blacklist information.",
         ],
         [
             "addblacklist",
             "To Add the group to the gcast blacklist.",
         ],
         [
             "delblacklist",
             f"To delete the group from the gcast blacklist.\n\n • **Note: **Type the command** `{cmd}addblacklist` **and** `{cmd}delblacklist` **in the group you are blacklisting. ",
         ],
     ],
)