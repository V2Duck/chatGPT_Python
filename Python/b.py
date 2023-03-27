import openai
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Load OpenAI API key
openai.api_key = "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"

# Define a function to get response from OpenAI API
def get_response(question: str, language: str, model: str) -> str:
    try:
        response = openai.Completion.create(
            model=model,
            prompt=f"""{question} {language}""",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Define message handler
def handle_message(update, context):
    # Get user input
    question = update.message.text
    language = "Python"
    model = "text-davinci-002"
    # Get response from OpenAI API
    reply = get_response(question, language, model)
    # Send reply back to user
    if reply:
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

# Define main function
def main():
    updater = Updater(token="6170545126:AAF726GZ3nMhSo7RnDsOGw6XYsGHxbhhNlk", use_context=True)
    dispatcher = updater.dispatcher
    # Add message handler
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
    dispatcher.add_handler(message_handler)
    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
