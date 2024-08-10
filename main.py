from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "7133435881:AAEfmGZ9AbFN7LMyIDHkmBGRsi1UQt_1n-0"
BOT_USERNAME: Final = "@kritobate_bot"

# Commands

async def sample_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, just a sample to know it is responding.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Write something for me to respond!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

# Handling responses

def handle_response(text: str) -> str:
    lower: str = text.lower()
    if 'hello' in lower:
        return 'Hi!'
    if 'how are you' in lower:
        return 'I\'m good!'
    if 'koi' in lower:
        return "I'm a bot"
    return "I don't understand you."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():

    print('Program is started successfully!')

    app = Application.builder().token(TOKEN).build()

    # Commands

    app.add_handler(CommandHandler('start', sample_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors

    app.add_error_handler(error)

    # Polling the bot

    print('Polling...')
    app.run_polling(poll_interval=2)

main()

