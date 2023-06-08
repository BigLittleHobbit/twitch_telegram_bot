import asyncio
import requests
import telegram
import logging
import yaml
from yaml.loader import SafeLoader

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
    text="Привет, кожаный. Меня зовут FS_TB, так что считай, что наши разговоры прослушиваются.")
    
async def get_sticker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.get_updates(
        allowed_updates=update,
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
    text="Сорян, я ничо не понял, спаситипамагити")
    await context.bot.send_sticker(chat_id=update.effective_chat.id,
    )


if __name__=="__main__":
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    token = config["BOT_TOKEN"]
    

    application = ApplicationBuilder().token(token).build()
    
    #handlers
    start_handler = CommandHandler('start', start)
    sticker_handler = MessageHandler(filters.Sticker.ALL, get_sticker_id)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(sticker_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

    
