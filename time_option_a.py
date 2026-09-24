"""
todo1/time_option_a.py

Times ONE decision of Option A: matching a spoken (here: typed) utterance
against the closed grammar of twenty phrasings, and returning the intent.

This times the decision step only (the string match), not audio capture
or text-to-speech - those are the same for all three options and are not
what distinguishes the baseline.

Run:
    python time_option_a.py
"""

import time
import statistics

# The closed grammar: twenty phrasings -> one of the three intents the
# case describes (room location, closing hours, call a human).
GRAMMAR = {
    "where is room 204": "room_location",
    "where is room 118": "room_location",
    "where is room 301": "room_location",
    "where is the accounting office": "room_location",
    "where is the it department": "room_location",
    "where is the reception": "room_location",
    "where is the cafeteria": "room_location",
    "when does the accounting office close": "closing_hours",
    "when does the it department close": "closing_hours",
    "when does the library close": "closing_hours",
    "when does the building close": "closing_hours",
    "when do you close": "closing_hours",
    "what time do you close": "closing_hours",
    "is the office still open": "closing_hours",
    "can i speak to someone": "call_human",
    "i want to talk to a person": "call_human",
    "get me a human": "call_human",
    "call an agent please": "call_human",
    "i need help from a staff member": "call_human",
    "connect me with a receptionist": "call_human",
}

assert len(GRAMMAR) == 20, "the case specifies twenty phrasings"


def normalize(text: str) -> str:
    """Lowercase, strip punctuation-adjacent whitespace, collapse spaces."""
    cleaned = "".join(ch for ch in text.lower() if ch.isalnum() or ch.isspace())
    return " ".join(cleaned.split())


def match(utterance: str):
    """One decision: exact-match the normalised utterance against the grammar."""
    return GRAMMAR.get(normalize(utterance))


# At least ten sentences to match, including two that MISS the grammar on
# purpose (an out-of-list room, and small talk picked up by the open mic) -
# a closed grammar must still decide fast on those, it just decides "no match".
TEST_UTTERANCES = [
    "Where is room 204?",
    "where is the accounting office",
    "When does the IT department close?",
    "Can I speak to someone",
    "I want to talk to a person",
    "where is room 999",            # miss: not one of the twenty
    "what time do you close",
    "Get me a human!",
    "where is the cafeteria",
    "hi, nice weather today",       # miss: bystander speech, open mic
]

if __name__ == "__main__":
    durations = []
    print(f"{'time (us)':>10}  {'intent':<16}  utterance")
    print("-" * 60)
    for utt in TEST_UTTERANCES:
        start = time.perf_counter()
        result = match(utt)
        elapsed = time.perf_counter() - start
        durations.append(elapsed)
        print(f"{elapsed * 1e6:10.2f}  {str(result):<16}  {utt}")

    median = statistics.median(durations)
    print("-" * 60)
    print(f"n = {len(durations)} inputs")
    print(f"median match time: {median * 1e6:.2f} microseconds "
          f"({median * 1e3:.4f} ms)")
