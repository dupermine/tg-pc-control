#!/usr/bin/env python3
import telebot
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", 0))
USE_WAYLAND = os.getenv("USE_WAYLAND", "False").lower() == "true"

bot = telebot.TeleBot(TOKEN)

def is_allowed(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ Доступ запрещён.")
        return False
    return True

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard.add('📋 Получить буфер', '📋 Отправить буфер')
keyboard.add('🔄 Перезагрузить', '⏻ Выключить')

@bot.message_handler(commands=['start'])
def start(message):
    if is_allowed(message):
        bot.reply_to(message, "✅ **Бот управления ПК запущен**", reply_markup=keyboard, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == '📋 Получить буфер')
def get_clipboard(message):
    if not is_allowed(message): return
    try:
        if USE_WAYLAND:
            text = subprocess.check_output("wl-paste", text=True).strip()
        else:
            text = subprocess.check_output("xclip -selection clipboard -o", text=True).strip()
        bot.reply_to(message, f"📋 **Буфер:**\n\n{text[:4000]}", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Не удалось получить буфер.")

@bot.message_handler(func=lambda m: m.text == '📋 Отправить буфер')
def request_text(message):
    if not is_allowed(message): return
    msg = bot.reply_to(message, "Отправь текст для буфера обмена:")
    bot.register_next_step_handler(msg, set_clipboard)

def set_clipboard(message):
    if not is_allowed(message): return
    try:
        if USE_WAYLAND:
            subprocess.run("wl-copy", input=message.text, text=True)
        else:
            subprocess.run("xclip -selection clipboard", input=message.text, text=True, shell=True)
        bot.reply_to(message, "✅ Записано в буфер обмена")
    except:
        bot.reply_to(message, "❌ Ошибка записи")

@bot.message_handler(func=lambda m: m.text == '🔄 Перезагрузить')
def reboot(message):
    if not is_allowed(message): return
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Да, перезагрузить", callback_data="reboot"))
    bot.reply_to(message, "⚠️ Перезагрузить ПК?", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '⏻ Выключить')
def shutdown(message):
    if not is_allowed(message): return
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Да, выключить", callback_data="shutdown"))
    bot.reply_to(message, "⚠️ Выключить ПК?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "reboot":
        subprocess.call(["shutdown", "-r", "now"])
    elif call.data == "shutdown":
        subprocess.call(["shutdown", "now"])

print("🤖 Telegram PC Bot запущен...")
bot.infinity_polling()
