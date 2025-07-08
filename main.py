
import json
import os
from sync_lists import get_category_list, fetch_items_for_list

def main():
    os.makedirs("catalogs", exist_ok=True)
    categories = get_category_list()

    for category in categories:
        print(f"📦 Processing {category['name']}")
        items = fetch_items_for_list(category)
        with open(f"catalogs/{category['slug']}.json", "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(items)} items to catalogs/{category['slug']}.json")

if __name__ == "__main__":
    main()
