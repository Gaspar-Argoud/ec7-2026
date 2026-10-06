# Timing the Option A baseline

## Command

    python time_option_a.py

## Machine

  platform         Windows-11-10.0.26200-SP0
  python           3.12.6 

## Raw output
```
  3.40 us  room_location  Where is room L120?
 17.10 us  room_location  where is the accounting & control office
 15.60 us  closing_hours  When does the IT department close?
  9.20 us  call_human     Can I speak to someone
  8.50 us  call_human     I want to talk to a person
  7.40 us  no_match       where is room 999
  7.30 us  closing_hours  what time do you close
  3.00 us  call_human     Get me a human!
  3.50 us  room_location  where is the cafeteria
 10.60 us  no_match       hi, nice weather today
median: 7.95 us over 10 decisions
```

## Comparison with the grid, and what would change

In `grid.md`, Option A's latency was scored **+3** on the assumption that a fixed-grammar match is "well inside the 1 s band". 
A measured median in the low microseconds (roughly five orders of magnitude under 1 s (1 s ~ 125,000 * 7.95µs)) confirms that assumption with a very wide margin — the real bottleneck inside 
Option A's 1-second acknowledgement budget is capturing and normalising the audio before the match ever runs, not the decision timed here.

If a real run disagreed by a lot — say tens of milliseconds instead of microseconds, 20 to 100 times under 1 s.
If a real run disagreed by a lot (say tens of milliseconds instead of microseconds, still 20 to 100 times under 1 s), I would keep the +3.
I would only lower the score if the median reached hundreds of milliseconds.
