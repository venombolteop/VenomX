

from gpytranslate import Translator
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from VenomX.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.me & filters.command(["tr", "trt", "translate"], cmd))
async def translate(client: Client, message: Message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        input_str = (
            message.text.split(None, 1)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        target = input_str or "hi"
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message,
                f"**ERROR:** `{str(err)}`",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            return
    else:
        input_str = (
            message.text.split(None, 2)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        text = message.text.split(None, 2)[2]
        target = input_str or "hi"
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edit_or_reply(
                message,
                "**ERROR:** `{}`".format(str(err)),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            return
    await edit_or_reply(
        message,
        f"**Translated to:** `{target}`\n```{tekstr.text}```\n\n**Detected Language:** `{(await trl.detect(text))}`",
        parse_mode=enums.ParseMode.MARKDOWN,
    )


add_command_help(
     "translate",
     [
         [
             "tr <language code> <text/reply>",
             "Translates text to the set language. (Default Indian code)",
         ],
     ],
)
