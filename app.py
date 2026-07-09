"""
app.py
-------
Flask app: user types how they feel -> emotion detected -> matching
tracks (via Apple's free iTunes Search API) are shown.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000

No API keys, accounts, or credentials needed - the iTunes Search API
is free and public.
"""

from flask import Flask, render_template, request

from emotion_detector import detect_emotion
from emotion_music_map import get_queries_for_emotion
from itunes_client import ITunesClient

app = Flask(__name__)
music_client = ITunesClient(country="IN")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None, spotify_error=None)


@app.route("/recommend", methods=["POST"])
def recommend():
    user_text = request.form.get("feeling", "").strip()

    if not user_text:
        return render_template(
            "index.html",
            result=None,
            error="Please describe how you're feeling first.",
            spotify_error=None,
        )

    emotion_result = detect_emotion(user_text)
    emotion = emotion_result["emotion"]
    mapping = get_queries_for_emotion(emotion)

    tracks = []
    search_error = None
    try:
        tracks = music_client.get_tracks_for_queries(mapping["queries"], per_query=4)
    except Exception as e:
        search_error = f"Couldn't fetch tracks right now: {e}"

    result = {
        "input_text": user_text,
        "emotion": emotion,
        "confidence": emotion_result["confidence"],
        "description": mapping["description"],
        "tracks": tracks,
    }

    return render_template("index.html", result=result, error=search_error, spotify_error=None)


if __name__ == "__main__":
    app.run(debug=True)
