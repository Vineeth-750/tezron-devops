# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Movie, WatchedMovie
import requests
from django.conf import settings


GENRES = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Horror": 27,
}


# ---------- AUTH ----------

def signup_view(request):
    if request.method == "POST":
        data = request.POST

        if data["password"] != data["confirm"]:
            messages.error(request, "Passwords mismatch")
            return redirect("signup")

        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            first_name=data["firstname"],
            last_name=data["lastname"],
            phone=data["phone"],
            country=data["country"]
        )
        login(request, user)
        return redirect("home")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["email"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------- HOME ----------

def home(request):
    data = {}

    for name, gid in GENRES.items():
        data[name] = fetch_movies_by_genre(gid)

    return render(request, "home.html", {"genres": data})


# ---------- SEARCH ----------

def search(request):
    q = request.GET.get("q")

    url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={q}"
    results = requests.get(url).json().get("results", [])

    # Removed Redis caching
    # If you want, you can save searches in DB here instead

    return render(request, "home.html", {"search_results": results})


# ---------- WATCH ----------

def watch_movie(request, tmdb_id):
    title = request.GET.get("title")
    poster = request.GET.get("poster")

    movie, _ = Movie.objects.get_or_create(
        tmdb_id=tmdb_id,
        defaults={"title": title, "poster": poster}
    )

    # Use get_or_create to avoid UNIQUE constraint error
    WatchedMovie.objects.get_or_create(user=request.user, movie=movie)

    return redirect("home")


# ---------- TMDB API function ----------

def fetch_movies_by_genre(genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []
