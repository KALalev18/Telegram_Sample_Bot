from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN: Final = "7133435881:AAEfmGZ9AbFN7LMyIDHkmBGRsi1UQt_1n-0"
BOT_USERNAME: Final = "@kritobate_bot"

# Trivia sample questions

trivia_questions = [
    {"question": "What is 9 + 10? (think)?", "answer": "21"},
    {"question": "Who wrote \"Diary of a Wimpy Kid\"?", "answer": "Jeff Kinney"},
    {"question": "Where is Lahti located?", "answer": "Finland"},
    {"question": "Does Lionel Messi play football?", "answer": "Yes"},
    {"question": "Who is the best Kristian?", "answer": "Lalev"},
]

# Store question and answer

user_data = {}

# Commands

async def sample_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, just a sample to know it is responding.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Sample bot response\n"
        "/help - See the list of commands\n"
        "/custom - Execute a custom command\n"
        "/quiz - Start a trivia quiz\n"
    )
    await update.message.reply_text(help_text)

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    question_data = random.choice(trivia_questions)
    question = question_data['question']
    answer = question_data['answer']

    user_data[chat_id] = answer

    await update.message.reply_text(f"Trivia question: {question}")

# Handling responses

def handle_response(chat_id: int, text: str) -> str:
    lower: str = text.lower()
    if chat_id in user_data:
        correct_answer = user_data[chat_id].lower()
        if lower == correct_answer:
            del user_data[chat_id]
            return "Correct answer!"
        else:
            return "Incorrect! Try again."
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

    response: str = handle_response(update.message.chat.id, text)

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
    app.add_handler(CommandHandler('quiz', start_quiz))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors

    app.add_error_handler(error)

    # Polling the bot

    print('Polling...')
    app.run_polling(poll_interval=2)

main()

