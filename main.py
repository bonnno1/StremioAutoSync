import os
import json
from sync_lists import get_category_list, fetch_shows_for_list

def write_json_file(slug, data):
    filename = f"{slug}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Created: {filename} with {len(data)} items")

def main():
    categories = get_category_list()
    for category in categories:
        print(f"Fetching: {category['name']}")
        items = fetch_shows_for_list(category)
        if items:
            write_json_file(category["slug"], items)
        else:
            print(f"⚠️ No data returned for {category['slug']}")

if __name__ == "__main__":
    main()
