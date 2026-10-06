# Timing the Option A baseline

## Command

    python time_option_a.py

## Machine

  platform         Windows-11-10.0.26200-SP0
  python           3.12.6 

## Raw output

 time (us)  intent            utterance
------------------------------------------------------------
  3.90 us  room_location  Where is room L120?
 18.00 us  room_location  where is the accounting & control office
  9.80 us  closing_hours  When does the IT department close?
  6.10 us  call_human     Can I speak to someone
  6.60 us  call_human     I want to talk to a person
 18.50 us  no_match       where is room 999
 11.00 us  closing_hours  what time do you close
  9.30 us  call_human     Get me a human!
 10.90 us  room_location  where is the cafeteria
  5.90 us  no_match       hi, nice weather today
------------------------------------------------------------
median: 9.55 us over 10 decisions
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
