# todo1/measure.md — timing the Option A baseline

## Command

    python time_option_a.py

## Raw output

 time (us)  intent            utterance
------------------------------------------------------------
     13.90  room_location     Where is room 204?
     21.80  room_location     where is the accounting office
     11.40  closing_hours     When does the IT department close?
      8.70  call_human        Can I speak to someone
      8.80  call_human        I want to talk to a person
      7.80  None              where is room 999
      7.80  closing_hours     what time do you close
      6.80  call_human        Get me a human!
      7.40  room_location     where is the cafeteria
      7.40  None              hi, nice weather today
------------------------------------------------------------
n = 10 inputs
median match time: 8.25 microseconds (0.0083 ms)
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
