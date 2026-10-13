"""Fetch Apple Reminders App Store reviews from Apple's public RSS feed.

Writes data/raw_reviews.csv with columns:
review_id, country, date, rating, version, title, text
"""

import csv
import time
from collections import Counter
from pathlib import Path

import requests

APP_ID = "1108187841"
COUNTRIES = ["us", "gb", "ca", "au"]
PAGES = range(1, 11)
FEED_URL = (
    "https://itunes.apple.com/{country}/rss/customerreviews/"
    "page={page}/id={app_id}/sortby=mostrecent/json"
)
COLUMNS = ["review_id", "country", "date", "rating", "version", "title", "text"]
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_reviews.csv"


def label(entry, key):
    return entry.get(key, {}).get("label", "")


def fetch_page(session, country, page):
    """Return the list of raw feed entries for one page (empty if none/failed)."""
    url = FEED_URL.format(country=country, page=page, app_id=APP_ID)
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=20)
            if resp.status_code == 200:
                entries = resp.json().get("feed", {}).get("entry", [])
                # A page with a single entry comes back as a dict, not a list.
                if isinstance(entries, dict):
                    entries = [entries]
                # The feed occasionally returns an empty page transiently; retry.
                if entries or attempt == 2:
                    return entries
            if resp.status_code in (400, 404):
                return []  # past the last available page
        except (requests.RequestException, ValueError) as exc:
            print(f"  {country} page {page}: attempt {attempt + 1} failed ({exc})")
        if attempt < 2:
            time.sleep(2 ** attempt)
    print(f"  {country} page {page}: giving up")
    return []


def parse_entry(entry, country):
    """Convert a feed entry to a review row, or None if it isn't a review."""
    # The app-metadata entry (and anything else non-review) has no rating.
    if "im:rating" not in entry or "content" not in entry:
        return None
    return {
        "review_id": label(entry, "id"),
        "country": country,
        "date": label(entry, "updated"),
        "rating": int(label(entry, "im:rating")),
        "version": label(entry, "im:version"),
        "title": label(entry, "title"),
        "text": label(entry, "content"),
    }


def main():
    reviews = {}
    session = requests.Session()

    for country in COUNTRIES:
        for page in PAGES:
            entries = fetch_page(session, country, page)
            for entry in entries:
                row = parse_entry(entry, country)
                if row and row["review_id"] not in reviews:
                    reviews[row["review_id"]] = row
            time.sleep(0.5)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(reviews.values())

    counts = Counter(r["country"] for r in reviews.values())
    print("Reviews per country:")
    for country in COUNTRIES:
        print(f"  {country}: {counts[country]}")
    print(f"Total unique reviews: {len(reviews)} -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
