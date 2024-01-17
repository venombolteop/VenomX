

import sys
from os import environ, execle, remove

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from VenomX import BOTLOG_CHATID, LOGGER
from VenomX.helpers.basic import edit_or_reply
from VenomX.helpers.misc import HAPP

from .help import add_command_help


@Client.on_message(filters.command("restart", cmd) & filters.me)
async def restart_bot(_, message: Message):
    try:
        msg = await edit_or_reply(message, "`Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("✅ Bot has restarted !\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "VenomX"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command("shutdown", cmd) & filters.me)
async def shutdown_bot(client: Client, message: Message):
    if BOTLOG_CHATID:
        await client.send_message(
            BOTLOG_CHATID,
            "**#SHUTDOWN** \n"
            "**VenomX-Userbot** has been turned off!\nIf you want to turn it back on, please open heroku",
        )
    await edit_or_reply(message, "**VenomX-Userbot Successfully turned it off!**")
    if HAPP is not None:
        HAPP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@Client.on_message(filters.command("logs", cmd) & filters.me)
async def logs_ubot(client: Client, message: Message):
    if HAPP is None:
        return await edit_or_reply(
            message,
            "Make sure your `HEROKU_API_KEY` and `HEROKU_APP_NAME` are configured correctly in your heroku config vars",
        )
    Man = await edit_or_reply(message, "**Getting Heroku Logs**")
    with open("Logs-Heroku.txt", "w") as log:
        log.write(HAPP.get_log())
    await client.send_document(
        message.chat.id,
        "Logs-Heroku.txt",
        thumb="VenomX/resources/logo.jpg",
        caption="**This is Heroku Logs**",
    )
    await Man.delete()
    remove("Logs-Heroku.txt")


add_command_help(
     "system",
     [
         ["restart", "To restart the userbot."],
         ["shutdown", "To turn off the userbot."],
         ["logs", "To view userbot logs."],
     ],
)
