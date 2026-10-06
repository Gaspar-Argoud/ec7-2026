"""
EC7 - Assignment 1 (todo1) - Item 6: time ONE decision of option A.

Option A is a closed grammar: the robot accepts only a fixed list of 20 phrasings.
This script times the DECISION step only: the text of what the visitor said is
cleaned up and compared with the 20 phrasings. There is no learning anywhere.

How to use it
  1. Put this file in your todo1/ folder.
  2. Replace GRAMMAR with your own 20 phrasings, and INPUTS with at least 10 inputs of your choosing.
  3. In a terminal, go to your course folder, activate the virtual environment, then run:
         python todo1/time_grammar.py
  4. Copy the command AND everything it prints, unedited, into todo1/measure.md.
"""

import platform
import statistics
import string
import time
from datetime import datetime

# 1. The closed grammar: 20 phrasings, each tied to one of the 3 kinds of request.
#    Write them in lower case, without punctuation (the inputs are cleaned the same way).
#    These are EXAMPLES: replace them with your own option A.
GRAMMAR = [
    ("where is room a12", "WHERE_ROOM"),
    ("where is room b24", "WHERE_ROOM"),
    ("how do i get to room a12", "WHERE_ROOM"),
    ("how do i get to room b24", "WHERE_ROOM"),
    ("where is the registry office", "WHERE_ROOM"),
    ("where is the housing office", "WHERE_ROOM"),
    ("where are the toilets", "WHERE_ROOM"),
    ("where is the lift", "WHERE_ROOM"),
    ("when does the registry office close", "WHEN_CLOSES"),
    ("when does the housing office close", "WHEN_CLOSES"),
    ("what time does the registry office close", "WHEN_CLOSES"),
    ("what time does the housing office close", "WHEN_CLOSES"),
    ("until when is the registry office open", "WHEN_CLOSES"),
    ("until when is the housing office open", "WHEN_CLOSES"),
    ("call a human", "CALL_HUMAN"),
    ("i want to talk to a person", "CALL_HUMAN"),
    ("i want to speak to someone", "CALL_HUMAN"),
    ("can i talk to an agent", "CALL_HUMAN"),
    ("i need help", "CALL_HUMAN"),
    ("get me a human", "CALL_HUMAN"),
]

# 2. At least 10 inputs of your choosing: text the recogniser could hand over.
#    Mix inputs that ARE in the grammar with inputs that are not.
INPUTS = [
    "Where is room A12?",                     # in the grammar, once cleaned up
    "When does the registry office close?",   # in the grammar
    "Call a human!",                          # in the grammar
    "I want to talk to a person.",            # in the grammar
    "Where's room B24?",                      # small variant, not in the list
    "Excuse me, how do I find room A12?",     # polite variant, not in the list
    "Is the registry still open?",            # short variant, not in the list
    "Can someone help me, please?",           # asks for a human in words the grammar lacks
    "Did you see the match last night?",      # bystander conversation
    "Two coffees, please.",                   # bystander at the coffee machine
]

# One decision lasts about a microsecond, close to what the clock can resolve,
# so each input is decided REPEATS times and the median duration is kept.
REPEATS = 1000

_PUNCTUATION = str.maketrans("", "", string.punctuation)


def normalise(text):
    """'Where is room A12?' -> 'where is room a12' (lower case, no punctuation, single spaces)."""
    return " ".join(text.lower().translate(_PUNCTUATION).split())


def decide(text):
    """ONE decision of option A: the kind of request, or NO_MATCH if the phrasing is not in the grammar."""
    cleaned = normalise(text)
    for phrasing, kind in GRAMMAR:
        if cleaned == phrasing:
            return kind
    return "NO_MATCH"


def median_decision_time(text):
    """Median duration, in seconds, of one decision on this input."""
    durations = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        decide(text)
        durations.append(time.perf_counter() - start)
    return statistics.median(durations)


if __name__ == "__main__":
    print("Run at:", datetime.now().isoformat(timespec="seconds"))
    print("Machine:", platform.platform(), "| CPU:", platform.machine(), "| Python", platform.python_version())
    print(f"Grammar: {len(GRAMMAR)} phrasings | inputs: {len(INPUTS)} | repeats per input: {REPEATS}")
    if len(GRAMMAR) != 20:
        print("Note: option A is defined with 20 phrasings; this grammar has", len(GRAMMAR))
    if len(INPUTS) < 10:
        print("Note: the assignment asks for at least 10 inputs; there are", len(INPUTS))
    print()

    medians = []
    for text in INPUTS:
        kind = decide(text)
        median_s = median_decision_time(text)
        medians.append(median_s)
        print(f"{text:<40} -> {kind:<11} {median_s * 1e6:7.2f} us")

    overall = statistics.median(medians)
    print()
    print(f"Median duration of one decision over {len(INPUTS)} inputs: "
          f"{overall * 1e6:.2f} us = {overall * 1e3:.4f} ms")
