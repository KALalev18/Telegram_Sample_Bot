from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN: Final = "7133435881:AAEfmGZ9AbFN7LMyIDHkmBGRsi1UQt_1n-0"
BOT_USERNAME: Final = "@kritobate_bot"
CHAT_ID: Final = 5722946215, -4276753376

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

async def send_initial_message(app: Application):

    chat_id = CHAT_ID       # Replace CHAT_ID with the actual chat ID (row 8)
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Sample bot response\n"
        "/help - See the list of commands\n"
        "/custom - Execute a custom command\n"
        "/quiz - Start a trivia quiz\n"
    )

    await app.bot.send_message(chat_id=chat_id, text=help_text)

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

    user_data[chat_id] = {
        "score": 0,
        "current_question": 0,
        "questions": random.sample(trivia_questions, len(trivia_questions))  # Shuffle questions
    } # User data being initialized


    await ask_question(update) # Ask 1st question


async def ask_question(update: Update):
    chat_id = update.message.chat.id
    user_info = user_data.get(chat_id)

    if user_info is None:
        await update.message.reply_text("Please start the quiz by typing /quiz.")
        return

    current_question_index = user_info["current_question"]

    # Simple check whether everything is answered

    if current_question_index < len(user_info["questions"]):
        question = user_info["questions"][current_question_index]["question"]
        await update.message.reply_text(f"Question {current_question_index + 1}: {question}")
    else:
        # Showing for final score
        score = user_info["score"]
        total_questions = len(user_info["questions"])
        await update.message.reply_text(f"Quiz finished! Your final score is {score}/{total_questions}.")
        del user_data[chat_id]

# Handling responses

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    text = update.message.text.strip().lower()

    print(f"Received message from chat ID: {chat_id}")
    print(f"Message text: {text}")

    if chat_id in user_data:
        user_info = user_data[chat_id]
        current_question_index = user_info["current_question"]

        # Get correct answer
        correct_answer = user_info["questions"][current_question_index]["answer"].strip().lower()

        # Check if the user's answer is correct

        if text == correct_answer:
            user_info["score"] += 1
            await update.message.reply_text("Correct answer!")
        else:
            await update.message.reply_text(f"Incorrect. The correct answer was: {correct_answer}.")

        # Go to the next question

        user_info["current_question"] += 1
        await ask_question(update)
    else:
        if 'hello' in text:
            await update.message.reply_text('Hi! How can I assist you today?')
        elif 'how are you' in text:
            await update.message.reply_text('I\'m good! How about you?')
        elif 'koi' in text:
            await update.message.reply_text('I\'m just a bot, but I\'m here to help!')
        else:
            await update.message.reply_text("I don't understand you. You can type /help to see what I can do.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")



def main():

    print('Program is started successfully!')

    app = Application.builder().token(TOKEN).build()

    # app.post_init(lambda: send_initial_message(app))

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

