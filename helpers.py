import os

import requests
from dotenv import load_dotenv

load_dotenv()

def get_movie_poster(title):

    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": os.getenv("TMDB_API_KEY"),
        "query": title
    }

    r = requests.get(url, params=params).json()

    if not r["results"]:
        return "No results found."

    movie = r["results"][0]
    poster_path = movie.get("poster_path")

    if not poster_path:
        return "No poster path available."

    return "https://image.tmdb.org/t/p/original" + poster_path