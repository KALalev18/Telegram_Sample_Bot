from typing import Final
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import random
from datetime import datetime
import asyncio

TOKEN: Final = "7133435881:AAEfmGZ9AbFN7LMyIDHkmBGRsi1UQt_1n-0"
BOT_USERNAME: Final = "@kritobate_bot"
CHAT_ID: Final = 5722946215, -4276753376
SELECTING_DAY = 1

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

# Event Schedule - Orientation days for SSE students

events = [
    {"datetime": datetime(2024, 8, 20, 10, 0), "text": "Welcome to Land of the Curious, auditorium 2 or online.\n\nWelcome greetings, introduction to electronic key cards & Meet a Local Friend Programme. - 10:30"},
    {"datetime": datetime(2024, 8, 20, 10, 30), "text": "Studies @ LUT, auditorium 2 or online.\n\nIntroduction to practicalities of studying and student services at LUT. - 11:30"},
    {"datetime": datetime(2024, 8, 20, 11, 30), "text": "Campus tour, on campus (tutor informs where to meet).\n\nGetting to know how to find classrooms, services, and hang-around-spots at campus. - 12:30"},
    {"datetime": datetime(2024, 8, 20, 12, 30), "text": "Lunch with tutors. - 13:30"},
    {"datetime": datetime(2024, 8, 20, 14, 0), "text": "Introduction to Finnish Culture (participation not recommended for those already familiar with Finnish Culture), auditorium 2 or online.\n\nThis introduction helps you to overcome possible culture shock and to understand the Finns around you. - 15:00"},
    {"datetime": datetime(2024, 8, 21, 9, 0), "text": "Introduction to Student Union and Guilds, auditorium 2 or online.\n\nStudent Union and Guilds play a vital role in Finnish university life. Learn about benefits, support, and activities. - 11:30"},
    {"datetime": datetime(2024, 8, 21, 11, 30), "text": "Lunch with tutors. - 13:00"},
    {"datetime": datetime(2024, 8, 21, 13, 0), "text": "Group activities with tutors, on campus (tutor informs where to meet).\n\nFun activities to get to know your new study friends. Comfortable clothing recommended. - 15:30"},
    {"datetime": datetime(2024, 8, 22, 11, 0), "text": "Lunch with tutors. - 12:00"},
    {"datetime": datetime(2024, 8, 22, 12, 0), "text": "Introduction to Studies, Personal study plan and course enrolments, Auditorium 1.\n\nWith study counsellor Lotta Meriläinen and tutors. - 14:00"},
    {"datetime": datetime(2024, 8, 22, 14, 30), "text": "Introduction to DD Programs with HEBUT, Auditorium 2. - 15:30"},
    {"datetime": datetime(2024, 8, 23, 9, 0), "text": "Personal Study Plan Workshop, Course enrolments & Q&A with tutors, M19_D247+D250. - 10:30"},
    {"datetime": datetime(2024, 8, 23, 10, 45), "text": "Introduction to the SSE program, M19_D247+D250. - 12:15"},
    {"datetime": datetime(2024, 8, 23, 12, 30), "text": "Lunch with SSE teachers and tutors, M19_D247+D250. - 14:00"},
    {"datetime": datetime(2024, 8, 23, 14, 0), "text": "Introduction to Software Engineering Department. - 14:45"},
    {"datetime": datetime(2024, 8, 23, 14, 45), "text": "Games and hangout, M19_D247+D250. - as much as you want"},
    {"datetime": datetime(2024, 8, 30, 10, 0), "text": "Student Welcome Fair, Event Arena.\n\nCollect services and support providers to help with a smooth start for studies. - 13:00"},
    {"datetime": datetime(2024, 9, 5, 9, 0), "text": "Newcomers can complete DVV registration on campus.\n\nSee further details in the checklist for new degree students. - 12:00 and 13:00 - 15:30"},
    {"datetime": datetime(2024, 9, 5, 16, 30), "text": "Welcome Event for international students by City of Lahti, Lahti City Hall (Harjukatu 31, Lahti). - 17:30"}
]

# Commands

async def send_initial_message(app: Application):

    chat_id = CHAT_ID       # Replace CHAT_ID with the actual chat ID (row 8)
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Sample bot response\n"
        "/help - See the list of commands\n"
        "/custom - Execute a custom command\n"
        "/quiz - Start a trivia quiz\n"
        "/events - See upcoming events\n"
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
        "/events - See upcoming events\n"
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
    else: # non-general responses, just instances
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

# Events by day 20 August - 5 September

async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("20 August")],
        [KeyboardButton("21 August")],
        [KeyboardButton("22 August")],
        [KeyboardButton("23 August")],
        [KeyboardButton("30 August")],
        [KeyboardButton("5 September")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please choose a day for the events:", reply_markup=reply_markup)
    return SELECTING_DAY

# string dates conversion to datetime

async def process_day_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    day_mapping = {
        "20 august": datetime(2024, 8, 20),
        "21 august": datetime(2024, 8, 21),
        "22 august": datetime(2024, 8, 22),
        "23 august": datetime(2024, 8, 23),
        "30 august": datetime(2024, 8, 30),
        "5 september": datetime(2024, 9, 5),
    }

    selected_day = update.message.text.strip().lower()
    selected_date = day_mapping.get(selected_day)

    if selected_date:
        upcoming_events = [event for event in events if event["datetime"].date() == selected_date.date()]

        if not upcoming_events:
            await update.message.reply_text(f"No events found for {selected_day}.")
        else:
            events_text = f"Events on {selected_day}:\n\n"
            for event in upcoming_events:
                event_datetime = event["datetime"].strftime("%Y-%m-%d %H:%M")
                events_text += f"{event_datetime}: {event['text']}\n\n"

            await update.message.reply_text(events_text)
    else:
        await update.message.reply_text("Invalid selection. Please use the provided buttons.")

    return ConversationHandler.END

def main():

    print('Program is started successfully!')

    app = Application.builder().token(TOKEN).build()

    # app.post_init(lambda: send_initial_message(app)) - start message should be fixed

    # Commands

    # Calling by day main process

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('events', list_events)],
        states={
            SELECTING_DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_day_selection)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler('start', sample_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('quiz', start_quiz))

    app.add_handler(conversation_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    # Errors

    app.add_error_handler(error)

    # Polling the bot

    print('Polling...')
    asyncio.run(app.run_polling(poll_interval=2))

main()

