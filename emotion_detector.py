"""
emotion_detector.py
--------------------
Lightweight, fully-offline emotion classifier for free-text input.

Why not a transformer model?
Downloading pretrained weights (e.g. from HuggingFace) requires network
access to model hubs, which isn't guaranteed in every deployment
environment (college labs, offline demos, restricted networks). This
lexicon-based approach works anywhere Python runs, with zero downloads,
and is transparent enough to explain in a viva.

Approach:
1. Score input text against curated keyword lists for 8 emotion classes.
2. Apply simple negation handling ("not happy" should NOT count as happy).
3. If no keywords match, fall back to a general positive/negative word
   count to pick the closest broad emotion.
"""

import re
from collections import defaultdict

# ---- Emotion keyword lexicons -------------------------------------------
# Keep these lowercase; matching is done on lowercase, whitespace-tokenized text.

EMOTION_KEYWORDS = {
    "happy": [
        "happy", "joy", "joyful", "excited", "great", "awesome", "good mood",
        "cheerful", "glad", "delighted", "wonderful", "fantastic", "elated",
        "smiling", "grateful", "blessed", "content", "thrilled", "amazing day",
        "celebration", "celebrate", "proud",
    ],
    "sad": [
        "sad", "down", "depressed", "unhappy", "heartbroken", "crying",
        "cry", "lonely", "alone", "grief", "miss", "missing", "hurt",
        "blue", "gloomy", "sorrow", "upset", "low", "empty", "hopeless",
        "tears", "broke up", "breakup",
    ],
    "angry": [
        "angry", "furious", "mad", "annoyed", "irritated", "rage",
        "pissed", "frustrated", "hate", "resentful", "livid", "outraged",
        "fed up", "seething",
    ],
    "anxious": [
        "anxious", "nervous", "worried", "stressed", "stress", "overwhelmed",
        "panic", "panicking", "scared", "afraid", "fear", "tense", "restless",
        "on edge", "uneasy", "dread",
    ],
    "calm": [
        "calm", "peaceful", "relaxed", "relax", "chill", "at ease",
        "serene", "tranquil", "mellow", "unwind", "meditative", "cozy",
    ],
    "romantic": [
        "romantic", "love", "in love", "crush", "affection", "sweetheart",
        "date night", "valentine", "loving", "adore",
    ],
    "energetic": [
        "energetic", "pumped", "hyped", "workout", "gym", "motivated",
        "energy", "power", "unstoppable", "focused", "grinding", "hustle",
    ],
    "nostalgic": [
        "nostalgic", "nostalgia", "memories", "throwback", "old times",
        "childhood", "reminisce", "remember when", "used to",
    ],
}

# Generic polarity lists used only as a fallback when no specific
# emotion keyword is found at all.
POSITIVE_WORDS = {"good", "nice", "fine", "okay", "ok", "well", "better", "fun"}
NEGATIVE_WORDS = {"bad", "terrible", "awful", "not good", "rough", "hard", "tired", "exhausted"}

NEGATIONS = {"not", "no", "never", "n't", "cant", "can't", "won't", "wont", "isn't", "aren't", "don't", "dont"}


def _tokenize(text: str):
    text = text.lower()
    # keep words and simple contractions together
    tokens = re.findall(r"[a-z']+", text)
    return text, tokens


def _is_negated(tokens, idx, window=2):
    """Check up to `window` tokens before position idx for a negation word."""
    start = max(0, idx - window)
    return any(tok in NEGATIONS for tok in tokens[start:idx])


def detect_emotion(text: str) -> dict:
    """
    Returns:
        {
            "emotion": <top emotion label, str>,
            "scores": {emotion: score, ...},   # all raw scores, for transparency
            "confidence": float (0-1, relative share of top score),
        }
    """
    if not text or not text.strip():
        return {"emotion": "neutral", "scores": {}, "confidence": 0.0}

    lowered, tokens = _tokenize(text)
    scores = defaultdict(int)

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            for match in re.finditer(re.escape(kw), lowered):
                # find the token index roughly at the match start for negation check
                prefix_tokens = re.findall(r"[a-z']+", lowered[:match.start()])
                idx = len(prefix_tokens)
                if kw in NEGATIONS:
                    continue
                if _is_negated(tokens, idx):
                    # negated positive emotion -> nudge toward its rough opposite
                    opposite = {
                        "happy": "sad", "calm": "anxious", "energetic": "sad",
                        "romantic": "sad", "sad": "happy", "angry": "calm",
                        "anxious": "calm", "nostalgic": "neutral",
                    }.get(emotion)
                    if opposite:
                        scores[opposite] += 1
                    continue
                scores[emotion] += 1

    if not scores:
        # fallback: generic polarity
        pos = sum(1 for w in POSITIVE_WORDS if w in lowered)
        neg = sum(1 for w in NEGATIVE_WORDS if w in lowered)
        if pos > neg:
            scores["happy"] = pos
        elif neg > pos:
            scores["sad"] = neg
        else:
            scores["neutral"] = 1

    total = sum(scores.values()) or 1
    top_emotion = max(scores, key=scores.get)
    confidence = round(scores[top_emotion] / total, 2)

    return {
        "emotion": top_emotion,
        "scores": dict(scores),
        "confidence": confidence,
    }


if __name__ == "__main__":
    # quick manual sanity tests
    tests = [
        "I'm feeling really happy and excited today, everything is great!",
        "I feel so sad and lonely, I've been crying all night",
        "I am not happy at all right now, work has been rough",
        "I'm so anxious about my exam tomorrow, I can't stop worrying",
        "just chilling, feeling calm and relaxed",
        "I really miss her, thinking about old memories from college",
        "let's gooo, pumped for the gym session, feeling unstoppable",
        "I hate this, so frustrated and angry right now",
        "thinking about my crush, feeling romantic tonight",
        "meh, nothing special today",
    ]
    for t in tests:
        print(f"{t!r:70} -> {detect_emotion(t)}")
