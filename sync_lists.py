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

    if res.status_code != 200:
        print(f"❌ TMDb error {res.status_code} at {url}: {data.get('status_message')}")
        return []

    if "results" not in data:
        print(f"⚠️ No 'results' in TMDb response for {url}")
        return []

    return data["results"]

def fetch_imdb_id(tmdb_id, content_type="tv"):
    url = f"/{content_type}/{tmdb_id}/external_ids"
    print(f"🔍 Fetching IMDb ID for {content_type.upper()} ID {tmdb_id}")
    try:
        res = requests.get(f"{TMDB_BASE}{url}", params={"api_key": TMDB_API_KEY}, headers=HEADERS)
        data = res.json()
        return data.get("imdb_id")
    except Exception as e:
        print(f"❌ Failed to fetch IMDb ID for {tmdb_id}: {e}")
        return None

def to_json_format(results, content_type="tv"):
    formatted = []
    for item in results:
        imdb_id = fetch_imdb_id(item["id"], content_type=content_type)
        if not imdb_id:
            print(f"⚠️ No IMDb ID for TMDb ID {item['id']} — skipping.")
            continue
        formatted.append({
            "title": item.get("name") or item.get("title"),
            "imdb_id": imdb_id
        })
    return formatted

def fetch_shows_for_list(list_def, content_type="tv"):
    if list_def.get("special"):
        if list_def["special"] == "trending":
            endpoint = f"/trending/{content_type}/week"
        elif list_def["special"] == "popular":
            endpoint = f"/{content_type}/popular"
        elif list_def["special"] == "now_playing" and content_type == "movie":
            endpoint = "/movie/now_playing"
        elif list_def["special"] == "airing_today" and content_type == "tv":
            endpoint = "/tv/airing_today"
        else:
            return []
        return to_json_format(fetch_tmdb(endpoint), content_type=content_type)
    else:
        return to_json_format(fetch_tmdb(f"/discover/{content_type}", list_def["tmdb_params"]), content_type=content_type)

def get_category_list():
    return [
        {"slug": "netflix", "tmdb_params": {"with_networks": "213"}, "name": "Netflix Weekly"},
        {"slug": "disney", "tmdb_params": {"with_networks": "2739"}, "name": "Disney+ Weekly"},
        {"slug": "prime", "tmdb_params": {"with_networks": "1024"}, "name": "Prime Video Weekly"},
        {"slug": "apple", "tmdb_params": {"with_networks": "2552"}, "name": "Apple TV+ Weekly"},
        {"slug": "stan", "tmdb_params": {"with_keywords": "186729"}, "name": "Stan Weekly"},
        {"slug": "trending", "tmdb_params": {}, "special": "trending", "name": "Trending"},
        {"slug": "popular", "tmdb_params": {}, "special": "popular", "name": "Popular"},
        {"slug": "cinema", "tmdb_params": {}, "special": "now_playing", "name": "In Cinemas"},
        {"slug": "newreleases", "tmdb_params": {}, "special": "airing_today", "name": "New Releases"},
        {"slug": "action", "tmdb_params": {"with_genres": "28"}, "name": "Action"},
        {"slug": "comedy", "tmdb_params": {"with_genres": "35"}, "name": "Comedy"},
        {"slug": "family", "tmdb_params": {"with_genres": "10751"}, "name": "Family"},
        {"slug": "horror", "tmdb_params": {"with_genres": "27"}, "name": "Horror"},
        {"slug": "kids", "tmdb_params": {"with_genres": "10762"}, "name": "Kids"},
        {"slug": "thriller", "tmdb_params": {"with_genres": "53"}, "name": "Thriller"},
        {"slug": "romance", "tmdb_params": {"with_genres": "10749"}, "name": "Romance"},
        {"slug": "adventure", "tmdb_params": {"with_genres": "12"}, "name": "Adventure"}
    ]
