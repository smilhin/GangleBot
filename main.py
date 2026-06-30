import os

from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from movie import mood_button_handler, genre_button_handler, ask_more_movies_button_handler, recommend_movie

load_dotenv()

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start Bot"),
        BotCommand("help", "Need Help?"),
        BotCommand("recommend_movie", "Need a movie recommendation?"),
        BotCommand("recommend_food", "Need a food recommendation?"),
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    user = update.effective_user
    await update.message.reply_text(f"Hey {user.first_name}! Welcome to the GangleBot!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "<b>Help:</b>\n\n"
        "<b>Commands:</b>\n"
        "/start - Start bot\n"
        "/help - Help\n"
        "/recommend_movie - Recommend a movie based on the mood and genre\n"
        "/recommend_food - Recommend food\n",
        parse_mode = "HTML"
    )

def main():
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).post_init(set_commands).build()

    # Message Handlers
    application.add_handler(MessageHandler(filters.Text(["Happy!!", "Sad :(", "Nostalgic.", "Angry!!!"]), mood_button_handler))
    application.add_handler(MessageHandler(filters.Text(["Movie", "Anime", "Cartoon", "Series"]), genre_button_handler))
    application.add_handler(MessageHandler(filters.Text(["No", "Yes!!"]), ask_more_movies_button_handler))

    # Function Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("recommend_movie", recommend_movie))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()