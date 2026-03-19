from __future__ import annotations

import os
from collections.abc import Iterable

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .converter import markdown_to_markdownv2_chunks


MAX_UTF16_LEN = 4096


def _iter_chunks(markdown: str) -> Iterable[str]:
    result = markdown_to_markdownv2_chunks(markdown, max_utf16_len=MAX_UTF16_LEN)
    return result.chunks


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    if update.message is None:
        return
    text = (
        "发送任意 Markdown 内容给我，我会转换成 Telegram MarkdownV2。\n"
        "也支持 LaTeX（会自动转为 Unicode 近似）。"
    )
    _ = await update.message.reply_text(text)


async def convert_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ = context
    if update.message is None or update.message.text is None:
        return
    for chunk in _iter_chunks(update.message.text):
        _ = await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN_V2)


def build_app():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment")
    app = Application.builder().token(token).build()
    if app.add_handler(CommandHandler("start", start)):
        pass
    if app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_message)):
        pass
    return app


def main() -> None:
    app = build_app()
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
