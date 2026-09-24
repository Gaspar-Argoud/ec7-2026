# todo1/measure.md — timing the Option A baseline

## Command

    python time_option_a.py

## Machine

`>>> REPLACE THIS LINE with the one line from your own todo1/env.txt (produced by
check_env.py in item 2) that identifies your platform — e.g. the Python version,
OS and architecture line. Do not use the line below: it is from a demo container,
not your own machine, and the assignment asks for your machine's own line. <<<`

## Raw output

Below is an **illustrative example run** (produced while drafting this file, in a
disposable Linux container — not the graded artefact). Replace it with the raw
output `time_option_a.py` prints on your own machine; keep the command above it.

```
 time (us)  intent            utterance
------------------------------------------------------------
     28.96  room_location     Where is room 204?
      7.12  room_location     where is the accounting office
     21.97  closing_hours     When does the IT department close?
      5.78  call_human        Can I speak to someone
      3.22  call_human        I want to talk to a person
      2.97  None              where is room 999
      2.86  closing_hours     what time do you close
      1.97  call_human        Get me a human!
      2.01  room_location     where is the cafeteria
      2.14  None              hi, nice weather today
------------------------------------------------------------
n = 10 inputs
median match time: 3.09 microseconds (0.0031 ms)
```

## Comparison with the grid, and what would change

In `grid.md`, Option A's latency was scored **+3** on the assumption that a
fixed-grammar match is "near-instant, well under the 1-second bar." A measured
median in the low microseconds (roughly five orders of magnitude under 1 s)
confirms that assumption with a very wide margin — the real bottleneck inside
Option A's 1-second acknowledgement budget is capturing and normalising the
audio before the match ever runs, not the decision timed here.

If a real run disagreed by a lot — say tens of milliseconds instead of
microseconds, still three orders of magnitude under 1 s — I would not change
the +3 score, since it would still clear the bar comfortably; I would only
revisit it if the median got close to the same order of magnitude as the
1-second budget itself (hundreds of milliseconds), which nothing about a
20-entry dictionary lookup should ever produce on ordinary hardware.
