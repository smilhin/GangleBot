import json

from openai.types.chat import ChatCompletionUserMessageParam
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import client
from helpers import get_movie_poster

async def recommend_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["seen_movies"] = []
    await ask_mood(update, context)

async def ask_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Happy!!", "Sad :("],
        ["Nostalgic.", "Angry!!!"]
    ]
    await update.message.reply_text(
        "Whats your mood?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def ask_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Movie", "Anime"],
        ["Cartoon", "Series"]
    ]
    await update.message.reply_text(
        "What do you want to watch?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def mood_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Mood
    if text == "Happy!!":
        context.user_data["mood"] = "happy"
    elif text == "Sad :(":
        context.user_data["mood"] = "sad"
    elif text == "Nostalgic.":
        context.user_data["mood"] = "nostalgic"
    elif text == "Angry!!!":
        context.user_data["mood"] = "angry"
    await ask_genre(update, context)

async def genre_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Movie":
        context.user_data["genre"] = "movie"
    elif text == "Anime":
        context.user_data["genre"] = "anime"
    elif text == "Cartoon":
        context.user_data["genre"] = "cartoon"
    elif text == "Series":
        context.user_data["genre"] = "series"
    await gpt_movie_recommendation(update, context)


async def gpt_movie_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_recommendation_prompt = f"""
    You are a film curator.

    TASK:
    Recommend 1 movie based on the user's genre and mood.

    STYLE:
    - Respond in English.
    - Try to be creative and imaginative.
    - Make interesting descriptions without many spoilers.

    INPUT:
    Genre: {context.user_data["genre"]}
    Mood: {context.user_data["mood"]}
    Already recommended (DO NOT suggest these again): {context.user_data["seen_movies"]}

    OUTPUT FORMAT:
    Return ONLY valid JSON. No markdown. No extra text.

    {{
      "title_en": "Movie Title in English",
      "year": 2020,
      "description": "Description here",
      "poster_url": "direct working image URL"
    }}
    """

    loading = await update.message.reply_text("Thinking... 🤔", reply_markup=ReplyKeyboardRemove())

    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[ChatCompletionUserMessageParam(role="user", content=movie_recommendation_prompt)],
            temperature=1,
            top_p=0.95,
            max_tokens=1024,
        )

        data = json.loads(response.choices[0].message.content)
        caption = f"""
        🎬 <b>Title:</b> {data['title_en']}\n<b>Year: </b> {data['year']}\n\n<b>Description:</b>\n{data['description']}
        """
        poster_url = get_movie_poster(data['title_en'])
        print(poster_url)
        await loading.delete()

        try:
            await update.message.reply_photo(photo=poster_url, caption=caption, parse_mode="HTML")
        except Exception:
            await update.message.reply_text(caption, parse_mode="HTML")
        await ask_more_movies(update, context)
        seen = context.user_data.get("seen_movies", [])
        seen.append(data["title_en"])
        context.user_data["seen_movies"] = seen

    except Exception as e:
        await loading.edit_text(f"Something went wrong :((\n {e}")

async def ask_more_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["No", "Yes!!"]
    ]
    await update.message.reply_text(
        "Recommend more movies?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def ask_more_movies_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Mood
    if text == "Yes!!":
        await gpt_movie_recommendation(update, context)
    elif text == "No":
        await update.message.reply_text("Alright! 😴", reply_markup=ReplyKeyboardRemove())
