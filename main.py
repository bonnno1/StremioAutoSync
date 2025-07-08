import os
import json
from sync_lists import get_category_list, fetch_shows_for_list

OUTPUT_DIR = "catalogs"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for category in get_category_list():
        print(f"Fetching: {category['name']}")
        items = fetch_shows_for_list(category)

        if not items:
            print(f"⚠️ No data returned for {category['slug']}")
            continue

        filepath = os.path.join(OUTPUT_DIR, f"{category['slug']}.json")
        with open(filepath, "w") as f:
            json.dump(items, f, indent=2)
        print(f"✅ Saved {len(items)} items to {filepath}")

    # If no files created, make a dummy to prevent GitHub Action crash
    if not os.listdir(OUTPUT_DIR):
        with open(os.path.join(OUTPUT_DIR, "empty.json"), "w") as f:
            json.dump([], f)
        print("🪫 No valid data found — created empty.json as fallback.")

if __name__ == "__main__":
    main()
