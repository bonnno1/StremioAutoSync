import requests

def fetch_trending():
    res = requests.get("https://api.trakt.tv/shows/trending", headers={"trakt-api-version": "2", "trakt-api-key": "9d01f9efde9e85c30ce34e7a739ad3cf"})
    return [item["show"]["ids"]["trakt"] for item in res.json()[:25]]

def fetch_popular():
    res = requests.get("https://api.trakt.tv/shows/popular", headers={"trakt-api-version": "2", "trakt-api-key": "9d01f9efde9e85c30ce34e7a739ad3cf"})
    return [item["ids"]["trakt"] for item in res.json()[:25]]

def fetch_genre(genre):
    res = requests.get(f"https://api.trakt.tv/shows/popular?genres={genre}", headers={"trakt-api-version": "2", "trakt-api-key": "9d01f9efde9e85c30ce34e7a739ad3cf"})
    return [item["ids"]["trakt"] for item in res.json()[:25]]

def fetch_dummy_streaming(name):
    # Replace with real curated API later — this returns dummy list
    return fetch_trending()[:10]

LISTS_TO_SYNC = [
    {"slug": "netflix-weekly", "name": "Netflix Weekly", "description": "Weekly Netflix shows", "fetch_function": lambda: fetch_dummy_streaming("Netflix")},
    {"slug": "disney-weekly", "name": "Disney+ Weekly", "description": "Weekly Disney+ shows", "fetch_function": lambda: fetch_dummy_streaming("Disney+")},
    {"slug": "stan-weekly", "name": "Stan Weekly", "description": "Weekly Stan shows", "fetch_function": lambda: fetch_dummy_streaming("Stan")},
    {"slug": "prime-weekly", "name": "Prime Video Weekly", "description": "Weekly Prime shows", "fetch_function": lambda: fetch_dummy_streaming("Prime")},
    {"slug": "apple-weekly", "name": "Apple TV+ Weekly", "description": "Weekly Apple shows", "fetch_function": lambda: fetch_dummy_streaming("Apple")},

    {"slug": "trending-now", "name": "Trending Now", "description": "Top trending shows", "fetch_function": fetch_trending},
    {"slug": "popular-now", "name": "Most Popular", "description": "Top popular shows", "fetch_function": fetch_popular},

    {"slug": "genre-action", "name": "Action", "description": "Top Action shows", "fetch_function": lambda: fetch_genre("action")},
    {"slug": "genre-comedy", "name": "Comedy", "description": "Top Comedy shows", "fetch_function": lambda: fetch_genre("comedy")},
    {"slug": "genre-family", "name": "Family", "description": "Top Family shows", "fetch_function": lambda: fetch_genre("family")},
    {"slug": "genre-horror", "name": "Horror", "description": "Top Horror shows", "fetch_function": lambda: fetch_genre("horror")},
    {"slug": "genre-kids", "name": "Kids", "description": "Top Kids shows", "fetch_function": lambda: fetch_genre("kids")},
    {"slug": "genre-thriller", "name": "Thriller", "description": "Top Thriller shows", "fetch_function": lambda: fetch_genre("thriller")},
    {"slug": "genre-romance", "name": "Romance", "description": "Top Romance shows", "fetch_function": lambda: fetch_genre("romance")},
    {"slug": "genre-adventure", "name": "Adventure", "description": "Top Adventure shows", "fetch_function": lambda: fetch_genre("adventure")},
]
