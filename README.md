# Moodstream — Emotion-Based Music Recommender (Apple / iTunes)

Type how you're feeling in plain text; the app detects your emotion and
recommends tracks to match (or gently counter) that mood, using Apple's
free iTunes Search API.

## Why the iTunes Search API (important context for your report/viva)

Two different Apple APIs get confused often, worth stating clearly:

- **Apple Music API** (personalized recommendations, streaming, library
  access) requires an **Apple Developer Program membership ($99/year)**
  plus a signed JWT developer token. A personal Apple Music subscription
  does **not** grant API access — that's a separate paid enrollment.
- **iTunes Search API** (`https://itunes.apple.com/search`) is a
  completely separate, free, public, unauthenticated Apple service. No
  account, no API key, no sign-up. It returns track name, artist, album
  art, and (for most tracks) a 30-second audio preview URL.

This project uses the iTunes Search API for exactly that reason — it
gets you a fully working, zero-cost demo. The trade-off: no personalized
recommendation engine and no audio-feature data (valence/energy/etc.) —
but Spotify no longer exposes that either for new developer apps, so
this project uses the same design either way: map each detected emotion
to **genre/mood search keywords** and let the catalog's own search
relevance do the work, rather than scoring by audio features.

One more deliberate choice: for **angry** and **anxious** inputs, the app
recommends *calming* music rather than matching the intensity — a common
practice in mood-regulation-aware recommender design. Easy to flip to
intensity-matching in `emotion_music_map.py` if your project brief wants
that instead — worth a sentence in your report either way.

## Project structure

```
emotion_music_app/
├── app.py                  # Flask routes
├── emotion_detector.py     # Keyword/lexicon-based emotion classifier (offline)
├── emotion_music_map.py    # Emotion -> search query mapping
├── itunes_client.py        # iTunes Search API wrapper (no auth needed)
├── templates/index.html
├── static/style.css
└── requirements.txt
```

## How emotion detection works

No external model download required (keeps it demo-able without internet
access to model hubs, and easy to explain line-by-line in a viva):

1. Curated keyword lists for 8 emotions: happy, sad, angry, anxious, calm,
   romantic, energetic, nostalgic.
2. Basic negation handling — "I am **not** happy" doesn't get scored as happy.
3. Falls back to generic positive/negative word counting if no specific
   emotion keyword is found, defaulting to "neutral" if nothing matches.

Test it standalone, no Flask/network setup needed:
```bash
python emotion_detector.py
```

Good "future work" material for your report:
- Swap in a pretrained transformer emotion classifier for higher accuracy
  on ambiguous/sarcastic text
- Evaluate against a labelled emotion dataset (e.g. ISEAR, GoEmotions) to
  quantify accuracy

## Setup (no API keys needed at all)

```bash
cd emotion_music_app
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

That's it — no developer account, no credentials, no `.env` file. The
iTunes Search API is public and free to use as-is.

Note: Apple's stated guidance is roughly 20 requests/minute on this API,
which is more than enough for a class demo, but avoid hammering it with
rapid repeated submissions.

## Notes for your report
- Emotion categories, keyword lists, and the emotion→genre mapping are all
  in plain Python dicts (`emotion_detector.py`, `emotion_music_map.py`) —
  easy to screenshot and explain, and easy to extend with more emotions.
- Album art, track name/artist, a direct store link, and a 30-second audio
  preview (playable right in the browser) are shown for each result.
- Worth mentioning in your report: this project deliberately compares two
  real streaming-platform APIs (Spotify vs. Apple/iTunes) and documents
  why each one's current access model shaped the final architecture —
  that's a legitimate, citable design decision, not a workaround to hide.
