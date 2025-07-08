
import requests
import os
import json

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json"}

def fetch_tmdb(url, params={}):
    params["api_key"] = TMDB_API_KEY
    params.setdefault("region", "AU")
    params.setdefault("language", "en-AU")

    print(f"🔍 Fetching: {url} | Params: {params}")
    res = requests.get(f"{TMDB_BASE}{url}", params=params, headers=HEADERS)

    try:
        data = res.json()
    except ValueError:
        print(f"❌ Invalid JSON from TMDb at {url}")
        return []

    if res.status_code != 200 or "results" not in data:
        print(f"⚠️ Error or no results for {url}: {data}")
        return []

    return data["results"]

def fetch_imdb_id(tmdb_id, content_type):
    url = f"/{content_type}/{tmdb_id}/external_ids"
    res = requests.get(f"{TMDB_BASE}{url}", params={"api_key": TMDB_API_KEY}, headers=HEADERS)
    try:
        return res.json().get("imdb_id")
    except ValueError:
        return None

def to_stremio_format(results, content_type):
    formatted = []
    for item in results:
        imdb_id = fetch_imdb_id(item["id"], content_type)
        if not imdb_id:
            continue
        formatted.append({
            "name": item.get("name") or item.get("title"),
            "type": "series" if content_type == "tv" else "movie",
            "imdb_id": imdb_id
        })
    return formatted

def fetch_items_for_list(list_def):
    endpoint = list_def.get("endpoint")
    content_type = list_def.get("type", "tv")
    params = list_def.get("tmdb_params", {})

    if list_def.get("special") == "trending":
        return to_stremio_format(fetch_tmdb(f"/trending/{content_type}/week"), content_type)
    if list_def.get("special") == "popular":
        return to_stremio_format(fetch_tmdb(f"/{content_type}/popular"), content_type)
    if list_def.get("special") == "now_playing":
        return to_stremio_format(fetch_tmdb("/movie/now_playing"), "movie")
    if list_def.get("special") == "airing_today":
        return to_stremio_format(fetch_tmdb("/tv/airing_today"), "tv")

    return to_stremio_format(fetch_tmdb(endpoint or f"/discover/{content_type}", params), content_type)

def get_category_list():
    return [
        {"slug": "netflix", "tmdb_params": {"with_networks": "213"}, "name": "Netflix Weekly", "type": "tv"},
        {"slug": "disney", "tmdb_params": {"with_networks": "2739"}, "name": "Disney+ Weekly", "type": "tv"},
        {"slug": "prime", "tmdb_params": {"with_networks": "1024"}, "name": "Prime Video Weekly", "type": "tv"},
        {"slug": "apple", "tmdb_params": {"with_networks": "2552"}, "name": "Apple TV+ Weekly", "type": "tv"},
        {"slug": "stan", "tmdb_params": {"with_keywords": "186729"}, "name": "Stan Weekly", "type": "tv"},
        {"slug": "trending", "special": "trending", "name": "Trending Shows", "type": "tv"},
        {"slug": "popular", "special": "popular", "name": "Popular Shows", "type": "tv"},
        {"slug": "cinema", "special": "now_playing", "name": "In Cinemas", "type": "movie"},
        {"slug": "newreleases", "special": "airing_today", "name": "New Releases", "type": "tv"},
        {"slug": "action", "tmdb_params": {"with_genres": "10759"}, "name": "Action", "type": "tv"},
        {"slug": "comedy", "tmdb_params": {"with_genres": "35"}, "name": "Comedy", "type": "tv"},
        {"slug": "family", "tmdb_params": {"with_genres": "10751"}, "name": "Family", "type": "tv"},
        {"slug": "horror", "tmdb_params": {"with_genres": "27"}, "name": "Horror", "type": "tv"},
        {"slug": "kids", "tmdb_params": {"with_genres": "10762"}, "name": "Kids", "type": "tv"},
        {"slug": "thriller", "tmdb_params": {"with_genres": "53"}, "name": "Thriller", "type": "tv"},
        {"slug": "romance", "tmdb_params": {"with_genres": "10749"}, "name": "Romance", "type": "tv"},
        {"slug": "adventure", "tmdb_params": {"with_genres": "12"}, "name": "Adventure", "type": "tv"},
        {"slug": "action-movies", "tmdb_params": {"with_genres": "28"}, "name": "Action Movies", "type": "movie"},
        {"slug": "comedy-movies", "tmdb_params": {"with_genres": "35"}, "name": "Comedy Movies", "type": "movie"},
        {"slug": "family-movies", "tmdb_params": {"with_genres": "10751"}, "name": "Family Movies", "type": "movie"},
        {"slug": "horror-movies", "tmdb_params": {"with_genres": "27"}, "name": "Horror Movies", "type": "movie"},
        {"slug": "romance-movies", "tmdb_params": {"with_genres": "10749"}, "name": "Romance Movies", "type": "movie"},
        {"slug": "thriller-movies", "tmdb_params": {"with_genres": "53"}, "name": "Thriller Movies", "type": "movie"},
        {"slug": "adventure-movies", "tmdb_params": {"with_genres": "12"}, "name": "Adventure Movies", "type": "movie"}
    ]
