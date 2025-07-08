import requests
import time
import json
from sync_lists import LISTS_TO_SYNC

import os

# Get secrets from GitHub Actions
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

TRAKT_BASE_URL = "https://api.trakt.tv"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "trakt-api-version": "2",
    "trakt-api-key": CLIENT_ID,
}

def refresh_access_token():
    print("Refreshing access token...")
    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token"
    }
    res = requests.post(f"{TRAKT_BASE_URL}/oauth/token", json=data)
    if res.status_code == 200:
        tokens = res.json()
        print("Token refreshed.")
        # NOTE: This won't persist to GitHub Secrets. You must update manually if changed.
        return tokens["access_token"]
    else:
        raise Exception(f"Token refresh failed: {res.text}")

def create_or_update_list(username, slug, display_name, description, items):
    print(f"Creating/updating list: {display_name}")
    list_url = f"{TRAKT_BASE_URL}/users/{username}/lists/{slug}"

    payload = {
        "name": display_name,
        "description": description,
        "privacy": "public",
        "display_numbers": True,
        "allow_comments": False
    }

    res = requests.post(list_url, headers=HEADERS, json=payload)
    if res.status_code in [201, 409]:  # Created or already exists
        # Clear existing items
        print(f"Clearing list '{display_name}'...")
        requests.delete(f"{list_url}/items/remove", headers=HEADERS, json={"movies": [], "shows": [{"ids": {"trakt": 0}}]})
        time.sleep(1)

        # Add new items
        print(f"Adding {len(items)} items to '{display_name}'...")
        add_payload = {"shows": [{"ids": {"trakt": trakt_id}} for trakt_id in items]}
        add_res = requests.post(f"{list_url}/items", headers=HEADERS, json=add_payload)

        if add_res.status_code in [201, 200]:
            print(f"List '{display_name}' updated.")
        else:
            print(f"Failed to add items to '{display_name}': {add_res.text}")
    else:
        print(f"Failed to create/update list '{display_name}': {res.text}")

def main():
    try:
        username_res = requests.get(f"{TRAKT_BASE_URL}/users/settings", headers=HEADERS)
        if username_res.status_code != 200:
            raise Exception("Token expired or invalid. Try refreshing it.")

        username = username_res.json()["user"]["ids"]["slug"]

        for sync_item in LISTS_TO_SYNC:
            trakt_ids = sync_item["fetch_function"]()
            if trakt_ids:
                create_or_update_list(
                    username=username,
                    slug=sync_item["slug"],
                    display_name=sync_item["name"],
                    description=sync_item["description"],
                    items=trakt_ids
                )
            else:
                print(f"No items returned for {sync_item['name']}")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()
