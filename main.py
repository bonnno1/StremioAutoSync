from sync_lists import get_category_list, fetch_shows_for_list
import os
import json

def write_to_json(slug, items, content_type):
    folder = os.path.join(os.getcwd(), slug)
    os.makedirs(folder, exist_ok=True)
    out_path = os.path.join(folder, f"catalog-{content_type}.json")
    with open(out_path, "w") as f:
        json.dump(items, f, indent=2)
    print(f"✅ Saved {len(items)} items to {out_path}")

def main():
    categories = get_category_list()
    for cat in categories:
        print(f"🔄 Syncing: {cat['name']} [TV Shows]")
        shows = fetch_shows_for_list(cat, content_type="tv")
        write_to_json(cat["slug"], shows, content_type="series")

        print(f"🎬 Syncing: {cat['name']} [Movies]")
        movies = fetch_shows_for_list(cat, content_type="movie")
        write_to_json(cat["slug"], movies, content_type="movie")

if __name__ == "__main__":
    main()
