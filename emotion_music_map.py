"""
emotion_music_map.py
---------------------
Maps a detected emotion to Spotify Search API queries.

NOTE ON DESIGN CHOICE:
Spotify's /recommendations and /audio-features endpoints (which used to
let you target valence/energy directly) are deprecated for new apps
(Nov 2024). The Search endpoint is still available, so instead of
scoring tracks by audio features, we search using genre + mood keywords
that Spotify's own search/indexing already associates with each emotion.

For emotions like "anxious" or "angry", we deliberately search for
*calming/soothing* music rather than reinforcing the feeling -- this is
a common, evidence-informed choice in mood-based recommender systems
(match energy down, not up, for distress states) but you can flip this
in EMOTION_QUERIES if your project brief wants energy-matching instead.
"""

EMOTION_QUERIES = {
    "happy": {
        "queries": ["feel good pop hits", "happy upbeat songs", "sunshine pop"],
        "description": "Upbeat, feel-good tracks to match your good mood",
    },
    "sad": {
        "queries": ["sad acoustic songs", "melancholy indie", "emotional piano ballads"],
        "description": "Gentle, reflective songs for when you need to feel it out",
    },
    "angry": {
        "queries": ["calming instrumental music", "soft acoustic chill", "soothing piano"],
        "description": "Calming tracks to help take the edge off",
    },
    "anxious": {
        "queries": ["calm ambient music", "relaxing lofi", "soothing acoustic"],
        "description": "Soothing, low-tempo music to ease anxious energy",
    },
    "calm": {
        "queries": ["chill lofi beats", "acoustic relaxation", "peaceful instrumental"],
        "description": "Mellow tracks to keep that calm going",
    },
    "romantic": {
        "queries": ["romantic love songs", "soulful R&B love", "acoustic love ballads"],
        "description": "Love songs to match the mood",
    },
    "energetic": {
        "queries": ["workout hype songs", "upbeat edm", "high energy pop"],
        "description": "High-energy tracks to keep you pumped",
    },
    "nostalgic": {
        "queries": ["throwback classic hits", "2000s nostalgia hits", "old school favorites"],
        "description": "Throwback tracks for a trip down memory lane",
    },
    "neutral": {
        "queries": ["popular hits mix", "top global tracks", "trending songs"],
        "description": "A general mix of popular tracks",
    },
}


def get_queries_for_emotion(emotion: str):
    return EMOTION_QUERIES.get(emotion, EMOTION_QUERIES["neutral"])
