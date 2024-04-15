import telebot
from config import TOKEN
from db import insert_row, is_tts_symbol_limit
from speechkit import text_to_speech

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['tts'])
def tts_handler(message):
    message.chat.id = message.from_user.id
    bot.send_message(message.chat.id, 'Отправь следующим сообщением текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)


def tts(message):
    if message.content_type != 'text':
        bot.send_message(message.chat.id, 'Отправь текстовое сообщение')
        bot.register_next_step_handler(message, tts)
        return

    text_symbols = is_tts_symbol_limit(message.chat.id, message.text)

    if text_symbols is str:
        bot.send_message(message.chat.id, text_symbols)
        bot.register_next_step_handler(message, tts)
        return

    insert_row(message.chat.id, message.text, text_symbols)
    status, content = text_to_speech(message.text)
    if status:
        bot.send_voice(message.chat.id, content)
    else:
        bot.send_message(message.chat.id, content)

