from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from VenomX.helpers.basic import edit_or_reply
from VenomX.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


@Client.on_message(filters.command(["intake", "ptl"], cmd) & filters.me)
async def intake_cmd(client: Client, message: Message):
     Man = await edit_or_reply(message, "`Wait a minute...`")
     await gather(
         Man.delete(),
         client.send_video(
             message.chat.id,
             choice(
                 [
                     intake.video.file_id
                     async for intake in client.search_messages(
                         "tedeintakecache", filter=enums.MessagesFilter.VIDEO
                     )
                 ]
             ),
             reply_to_message_id=ReplyCheck(message),
         ),
     )


add_command_help(
     "intake",
     [
         [
             f"intake or {cmd}ptl",
             "To Send intake videos randomly.",
         ]
     ],
)