import telebot
from telebot import types
import time
from threading import Timer

TOKEN = '6920632678:AAEYkZXsMgddiW7EmL7tiabZvyQembTV624'
bot = telebot.TeleBot(TOKEN)

# This dictionary will hold the messages and their deletion timers
messages_to_delete = {}

def schedule_message_deletion(chat_id, message_id, delay):
    # Schedule the deletion of a specific message after 'delay' seconds
    Timer(delay, delete_message, args=(chat_id, message_id)).start()

def delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id, )
    except Exception as e:
        print(f"1 + 1")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that will delete messages after a given time period. Use /settimer to set the deletion interval.")

@bot.message_handler(commands=['settimer'])
def set_timer(message):
    try:
        # Split the message text to get the timer value
        parts = message.text.split()
        if len(parts) > 1:
            delay = int(parts[1])
            bot.reply_to(message, f"Timer set to {delay} seconds. Messages will now be deleted after this interval.")
            # Store the delay with the chat id
            messages_to_delete[message.chat.id] = delay
        else:
            bot.reply_to(message, "Please specify the time in seconds after /settimer command.")
    except ValueError:
        bot.reply_to(message, "Please enter a valid number of seconds after /settimer command.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Echo the received message
#    bot.reply_to(message, message.text)

    # Check if the chat has a deletion timer set
    if message.chat.id in messages_to_delete:
        delay = messages_to_delete[message.chat.id]
        # Schedule this message to be deleted after the specified delay
        schedule_message_deletion(message.chat.id, message.message_id, delay)

bot.polling()
