"""
topic_detector.py
--------------------
Detects specific topics/interests mentioned in the user's text (sports,
activities, occasions, weather, etc.) so recommendations can be more
targeted than pure emotion alone.

Example: "watching the football match tonight, so hyped" should surface
football/stadium-anthem style tracks, not just generic "energetic" pop.

This runs alongside emotion_detector.py, not instead of it - both
signals get combined when building the final search queries.
"""

import re

# Each topic: trigger keywords to detect it in text, and search queries
# that target that specific subject.
TOPIC_KEYWORDS = {
    "football": {
        "triggers": ["football", "soccer", "messi", "ronaldo", "world cup",
                     "champions league", "premier league", "fifa"],
        "queries": ["football anthems", "world cup songs", "stadium chants"],
        "label": "Football",
    },
    "cricket": {
        "triggers": ["cricket", "ipl", "world test championship", "virat kohli",
                     "wicket", "world cup cricket"],
        "queries": ["cricket anthems", "ipl songs", "sports stadium hits"],
        "label": "Cricket",
    },
    "gym_workout": {
        "triggers": ["gym", "workout", "exercise", "lifting", "cardio",
                     "training session", "leg day"],
        "queries": ["gym workout hype", "high energy training music", "pump up songs"],
        "label": "Workout",
    },
    "running": {
        "triggers": ["running", "run today", "jogging", "marathon", "5k", "10k"],
        "queries": ["running playlist beats", "cardio pace music", "high tempo running songs"],
        "label": "Running",
    },
    "travel_roadtrip": {
        "triggers": ["road trip", "roadtrip", "traveling", "travelling", "trip",
                     "vacation", "long drive", "highway"],
        "queries": ["road trip songs", "travel anthems", "driving playlist hits"],
        "label": "Travel",
    },
    "rain": {
        "triggers": ["rain", "rainy", "monsoon", "raining", "thunderstorm"],
        "queries": ["rainy day songs", "monsoon acoustic", "cozy rain playlist"],
        "label": "Rainy day",
    },
    "birthday": {
        "triggers": ["birthday", "bday"],
        "queries": ["birthday party songs", "celebration hits", "party anthems"],
        "label": "Birthday",
    },
    "breakup": {
        "triggers": ["breakup", "broke up", "ex-girlfriend", "ex-boyfriend",
                     "we broke up", "split up"],
        "queries": ["breakup songs", "moving on anthems", "heartbreak playlist"],
        "label": "Breakup",
    },
    "study_exam": {
        "triggers": ["exam", "studying", "study session", "assignment",
                     "revision", "finals week"],
        "queries": ["lofi study beats", "focus instrumental music", "deep work playlist"],
        "label": "Study",
    },
    "wedding": {
        "triggers": ["wedding", "sangeet", "marriage ceremony", "shaadi"],
        "queries": ["wedding songs", "sangeet dance hits", "celebration wedding playlist"],
        "label": "Wedding",
    },
    "festival": {
        "triggers": ["diwali", "holi", "navratri", "garba", "festival season"],
        "queries": ["festival dance hits", "diwali party songs", "festive celebration playlist"],
        "label": "Festival",
    },
    "motivation": {
        "triggers": ["motivation", "motivated", "hustle mode", "grind",
                     "success mindset", "level up"],
        "queries": ["motivational anthems", "success mindset music", "hustle playlist"],
        "label": "Motivation",
    },
    "rainy_gaming": {  # example of a niche combo, easy to extend further
        "triggers": ["gaming session", "video game", "esports", "gameplay"],
        "queries": ["gaming background music", "esports hype tracks"],
        "label": "Gaming",
    },
}


def detect_topics(text: str):
    """
    Returns a list of matched topic dicts (each with 'label' and 'queries'),
    in order of first appearance in the text. Empty list if nothing matches.
    """
    if not text:
        return []
    lowered = text.lower()
    matches = []
    for topic_key, data in TOPIC_KEYWORDS.items():
        for trigger in data["triggers"]:
            if re.search(re.escape(trigger), lowered):
                matches.append({"key": topic_key, "label": data["label"], "queries": data["queries"]})
                break  # one match per topic is enough
    return matches


if __name__ == "__main__":
    tests = [
        "watching the football match tonight, so hyped",
        "going for a long road trip this weekend",
        "it's raining so hard outside, feeling cozy",
        "studying for my exam tomorrow, need focus",
        "my birthday is today!",
        "just a normal day, nothing special",
    ]
    for t in tests:
        print(f"{t!r:55} -> {detect_topics(t)}")
