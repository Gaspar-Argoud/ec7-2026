# time_option_a.py - times one decision of option A (closed grammar, no learning); standard library only
import statistics  # median() of the measured durations
import time        # perf_counter(): Python's most precise clock for short durations

grammar = {  # Step 1 - the closed grammar: 20 fixed phrasings, grouped under the intent each one maps to
    "room_location": ["where is room L120", "where is room S129", "where is the accounting & control office",
                      "where is the HR department", "where is the IT department", "where is the reception",
                      "where is the cafeteria"],
    "closing_hours": ["when does the accounting & control office close", "when does the IT department close",
                      "when does the library close", "when does the building close", "when do you close",
                      "what time do you close", "is the office still open"],
    "call_human": ["can i speak to someone", "i want to talk to a person", "get me a human",
                   "call an agent please", "i need help from a staff member", "connect me with a receptionist"],
}

def normalize(text):  # Step 2 - ignore capitals and punctuation
    spaced = "".join(ch if ch.isalnum() else " " for ch in text.lower())  # lowercase; punctuation -> space
    return " ".join(spaced.split())  # squeeze repeated spaces and trim both ends

lookup = {}  # Step 3 - a "cleaned phrasing -> intent" table, built once, before any timing
for intent, phrasings in grammar.items():  # for each of the 3 intents...
    for phrasing in phrasings:  # ...and each of its phrasings,
        lookup[normalize(phrasing)] = intent  # store the cleaned phrasing with its intent

def match(sentence):  # Step 4 - ONE decision: clean the sentence, then look it up exactly
    return lookup.get(normalize(sentence), "no_match")  # not one of the 20 phrasings -> "no_match"

tests = ["Where is room L120?", "where is the accounting & control office", "When does the IT department close?",
         "Can I speak to someone", "I want to talk to a person", "where is room 999", "what time do you close",
         "Get me a human!", "where is the cafeteria", "hi, nice weather today"]  # Step 5 - 2 must NOT match

times = []  # Step 6 - time each decision, keep it, print it
for sentence in tests:  # one decision per test sentence
    start = time.perf_counter()  # read the clock just before the decision
    intent = match(sentence)  # the decision being timed
    elapsed_us = (time.perf_counter() - start) * 1_000_000  # read it again; seconds -> microseconds (us)
    times.append(elapsed_us)  # keep it for the median
    print(f"{elapsed_us:6.2f} us  {intent:13}  {sentence}")  # time, intent found, input sentence
print(f"median: {statistics.median(times):.2f} us over {len(times)} decisions")  # Step 7 - then the median
