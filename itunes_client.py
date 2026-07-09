"""
itunes_client.py
-------------------
Client for Apple's free, public iTunes Search API.

Why this instead of the official Apple Music API:
The full Apple Music API (personalized recommendations, streaming,
library access) requires an Apple Developer Program membership
($99/year) plus a signed JWT developer token — a personal Apple Music
subscription alone does NOT grant API access.

The iTunes Search API (https://itunes.apple.com/search) is a separate,
free, public, unauthenticated Apple service. It returns track name,
artist, album art, and a 30-second preview URL for most tracks. No
credentials, no account, no sign-up required.

Trade-off vs. the full Apple Music API: no personalized recommendations
or valence/energy-style audio features (Apple doesn't expose these
either way) - same keyword/genre-mapping approach as we used for
Spotify Search applies here too.

Docs: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/
Rate limit: ~20 requests/minute (Apple's stated guidance, subject to change).
"""

import random
import requests

SEARCH_URL = "https://itunes.apple.com/search"


class ITunesClient:
    def __init__(self, country: str = "IN"):
        self.country = country

    def search_tracks(self, query: str, limit: int = 10):
        """Search for songs matching a query string."""
        limit = min(limit, 25)  # keep requests light/considerate of the free API
        params = {
            "term": query,
            "media": "music",
            "entity": "song",
            "limit": limit,
            "country": self.country,
        }
        resp = requests.get(SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("results", [])

        tracks = []
        for item in items:
            tracks.append({
                "name": item.get("trackName"),
                "artists": item.get("artistName"),
                "album": item.get("collectionName"),
                "image": item.get("artworkUrl100"),
                "store_url": item.get("trackViewUrl"),
                "preview_url": item.get("previewUrl"),  # 30-second AAC preview, usually present
            })
        return tracks

    def get_tracks_for_queries(self, queries, per_query: int = 4):
        """Run multiple queries and combine + de-dupe + shuffle results."""
        all_tracks = []
        seen = set()
        for q in queries:
            try:
                results = self.search_tracks(q, limit=per_query)
            except requests.HTTPError:
                continue
            for t in results:
                key = (t["name"], t["artists"])
                if key not in seen and t["store_url"]:
                    seen.add(key)
                    all_tracks.append(t)
        random.shuffle(all_tracks)
        return all_tracks
