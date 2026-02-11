import requests
import redis
from django.conf import settings
import json

r = redis.Redis.from_url(settings.REDIS_URL)


def fetch_movies_by_genre(genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}"
    return requests.get(url).json()["results"]


def cache_recent_search(user_id, query):
    key = f"recent_search:{user_id}"
    r.lpush(key, query)
    r.ltrim(key, 0, 9)


def get_recent_search(user_id):
    return [x.decode() for x in r.lrange(f"recent_search:{user_id}", 0, 9)]


def cache_recent_watch(user_id, movie):
    key = f"recent_watch:{user_id}"
    r.lpush(key, json.dumps(movie))
    r.ltrim(key, 0, 9)

