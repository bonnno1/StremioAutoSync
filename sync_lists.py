import requests
import os
import json

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"

HEADERS = {"accept": "application/json"}

def fetch_tmdb(url, params={}):
    params["api_key"] = TMDB_API_KEY
    params.setdefault("region", "AU")       # 🇦🇺 Australian availability
    params.setdefault("language", "en-AU")

    print(f"🔍 Fetching: {url} | Params: {params}")
    res = requests.get(f"{TMDB_BASE}{url}", params=params, headers=HEADERS)

    try:
        data = res.json()
    except ValueError:
        print(f"❌ Invalid JSON from TMDb at {url}")
        return []

    print(f"📨 Response: {json.dumps(data, indent=2)}")

    if res.status_code != 200:
        print(f"❌ TMDb error {res.status_code} at {url}: {data.get('status_message')}")
        return []

    if "results" not in data:
        print(f"⚠️ No 'results' in TMDb response for {url}")
        return []

    return data["results"]

def fetch_imdb_id(tmdb_id):
    url = f"/tv/{tmdb_id}/external_ids"
    params = {"api_key": TMDB_API_KEY}
    print(f"🔍 Fetching IMDb ID for TMDb ID {tmdb_id}")
    
    res = requests.get(f"{TMDB_BASE}{url}", params=params, headers=HEADERS)
    try:
        data = res.json()
        print(f"📨 IMDb Response: {json.dumps(data, indent=2)}")
        return data.get("imdb_id")
    except ValueError:
        print(f"❌ Invalid JSON when fetching IMDb ID for {tmdb_id}")
        return None

def to_json_format(results):
    formatted = []
    for item in results:
        imdb_id = fetch_imdb_id(item["id"])
        if not imdb_id:
            print(f"⚠️ No IMDb ID for TMDb ID {item['id']} — skipping.")
            continue
        formatted.append({
            "title": item.get("name") or item.get("title"),
            "imdb_id": imdb_id
        })
    return formatted

def fetch_shows_for_list(list_def):
    if list_def.get("special") == "trending":
        return to_json_format(fetch_tmdb("/trending/tv/week"))
    if list_def.get("special") == "popular":
        return to_json_format(fetch_tmdb("/tv/popular"))
    if list_def.get("special") == "now_playing":
        return to_json_format(fetch_tmdb("/movie/now_playing"))
    if list_def.get("special") == "airing_today":
        return to_json_format(fetch_tmdb("/tv/airing_today"))

    return to_json_format(fetch_tmdb("/discover/tv", list_def["tmdb_params"]))

def get_category_list():
    return [
        {"slug": "netflix", "tmdb_params": {"with_networks": "213"}, "name": "Netflix Weekly"},
        {"slug": "disney", "tmdb_params": {"with_networks": "2739"}, "name": "Disney+ Weekly"},
        {"slug": "prime", "tmdb_params": {"with_networks": "1024"}, "name": "Prime Video Weekly"},
        {"slug": "apple", "tmdb_params": {"with_networks": "2552"}, "name": "Apple TV+ Weekly"},
        {"slug": "stan", "tmdb_params": {"with_keywords": "186729"}, "name": "Stan Weekly"},
        {"slug": "trending", "tmdb_params": {}, "special": "trending", "name": "Trending Shows"},
        {"slug": "popular", "tmdb_params": {}, "special": "popular", "name": "Popular Shows"},
        {"slug": "cinema", "tmdb_params": {}, "special": "now_playing", "name": "In Cinemas"},
        {"slug": "newreleases", "tmdb_params": {}, "special": "airing_today", "name": "New Releases"},
        {"slug": "action", "tmdb_params": {"with_genres": "10759"}, "name": "Action"},
        {"slug": "comedy", "tmdb_params": {"with_genres": "35"}, "name": "Comedy"},
        {"slug": "family", "tmdb_params": {"with_genres": "10751"}, "name": "Family"},
        {"slug": "horror", "tmdb_params": {"with_genres": "27"}, "name": "Horror"},
        {"slug": "kids", "tmdb_params": {"with_genres": "10762"}, "name": "Kids"},
        {"slug": "thriller", "tmdb_params": {"with_genres": "53"}, "name": "Thriller"},
        {"slug": "romance", "tmdb_params": {"with_genres": "10749"}, "name": "Romance"},
        {"slug": "adventure", "tmdb_params": {"with_genres": "12"}, "name": "Adventure"},
    ]
