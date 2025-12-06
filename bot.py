import telebot # библиотека telebot
from config import token # импорт токена
import time

bot = telebot.TeleBot(token)  

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.reply_to_message:
        bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} получил предупреждение!")
    else:
        bot.reply_to(message, "Используйте команду в ответ на сообщение пользователя.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        
        # Мьют на 5 минут (300 секунд)
        bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+300)
        bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} заглушен на 5 минут.")
    else:
        bot.reply_to(message, "Используйте команду в ответ на сообщение.")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
    Доступные команды:
    /start - Приветствие
    /ban - Забанить пользователя (в ответ на сообщение)
    /warn - Выдать предупреждение
    /mute - Заглушить пользователя на 5 минут
    /help - Показать это сообщение
    """
    bot.reply_to(message, help_text)

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling(none_stop=True)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

bot.infinity_polling(none_stop=True)
