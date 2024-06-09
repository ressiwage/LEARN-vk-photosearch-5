import os
import telebot
from  telebot import types
from PIL import Image
from ._imports import config
from ._imports import find as find_image

BOT_TOKEN = config.tg_token
ALLOWED_USERNAMES =config.allowed_ids
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['search'], func=lambda message:message.chat.username in ALLOWED_USERNAMES)
def sign_handler(message):
    text = "введите описание фотографии, которую вы хотите найти, на латинице. \nпоиск идёт по bag of words, так что старайтесь придерживаться лемматизированной версии слов."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    print()
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "введите количество фотографий, которые вы хотите получить.\nфотографии будут идти в порядке релевантности"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, photo_handler, sign)
    
def photo_handler(message, val):
    
    for i in find_image(val, int(message.text)):
        image = Image.open(i[0])
        bot.send_photo(message.chat.id, image, caption=i[1])
        


bot.infinity_polling()
