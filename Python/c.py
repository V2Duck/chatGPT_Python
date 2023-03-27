import telegram
from telegram.ext import Updater, CommandHandler
from PIL import Image

# Define function to convert image to webp format
def convert_image_to_webp(image_path):
    # Open image file
    with Image.open(image_path) as image:
        # Convert image to RGB mode if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        # Save the converted image in WEBP format
        image.save(f"{image_path}.webp", "WEBP")

# Define command handler for '/start' command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Welcome to my bot.")

# Define main function
def main():
    # Create an instance of Updater and pass your bot's token
    updater = Updater(token='6170545126:AAF726GZ3nMhSo7RnDsOGw6XYsGHxbhhNlk', use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # Add the command handler to the dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    # Start the bot
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
