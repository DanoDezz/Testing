import logging
import time
from telegram.ext import Updater, MessageHandler, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Define the token for your bot
TOKEN = "your_token_here"

# Define the function to delete messages after 30 minutes
def delete_messages(update, context):
    # Get the message object
    message = update.message
    # Get the chat ID of the group
    chat_id = message.chat_id
    # Get the current timestamp
    current_time = time.time()
    # Get the timestamp of the message
    message_time = message.date.timestamp()
    # Calculate the time difference in seconds
    time_difference = current_time - message_time
    # If the time difference is greater than 30 minutes (1800 seconds), delete the message
    if time_difference >= 3600:
        context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

# Define the main function to start the bot
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Add a handler to listen for new messages in the group
    dispatcher.add_handler(MessageHandler(Filters.all, delete_messages))
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C
    updater.idle()

if name == 'main':
    main()
