"""
EC7 - Assignment 1 (todo1) - Item 3: weighted totals and radar for grid.md.

How to use it
  1. Fill SCORES first (-3 to +3), THEN WEIGHTS (0 to 5), in the order of CRITERIA.
  2. In a terminal, go to your course folder, activate the virtual environment, then run:
         python todo1/grid_radar.py
  3. Paste the tables it prints into grid.md. It also saves radar.png next to this file.

The radar needs matplotlib. If the script says it is missing, run:  pip install matplotlib
You can run it with the scores only (weights still at 0) to see the radar before weighting.
"""

from pathlib import Path

CRITERIA = [
    "Latency",
    "Total cost",
    "Energy",
    "Processing mode",
    "Deployment & sovereignty",
    "Robustness",
    "Explainability",
    "Confidentiality",
    "Maintainability",
    "Human control",
]

# Scores: -3 strong inadequacy ... 0 neither helps nor hurts ... +3 strong adequacy.
# For Total cost and Energy, +3 means CHEAP and FRUGAL, not "a big number".
# One score per criterion, in the order of CRITERIA above.
SCORES = {
    "A (closed grammar)":   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "B (local recogniser)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "C (hosted API)":       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

# Weights: 0 to 5, one per criterion, same order. Fill them AFTER the scores.
WEIGHTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

BASELINE = "A (closed grammar)"


def fmt(value):
    """+2, -1, 0 (a plus sign makes adequate and inadequate easy to tell apart)."""
    return f"{value:+d}" if value else "0"


def short(name):
    """'A (closed grammar)' -> 'A'."""
    return name.split()[0]


def check_inputs():
    problems = []
    for option, row in SCORES.items():
        if len(row) != len(CRITERIA):
            problems.append(f"{option}: {len(row)} scores, expected {len(CRITERIA)}")
        for criterion, s in zip(CRITERIA, row):
            if not isinstance(s, int) or not -3 <= s <= 3:
                problems.append(f"{option} / {criterion}: {s!r} is not a whole number from -3 to +3")
    if len(WEIGHTS) != len(CRITERIA):
        problems.append(f"WEIGHTS: {len(WEIGHTS)} values, expected {len(CRITERIA)}")
    for criterion, w in zip(CRITERIA, WEIGHTS):
        if not isinstance(w, int) or not 0 <= w <= 5:
            problems.append(f"weight of {criterion}: {w!r} is not a whole number from 0 to 5")
    return problems


def print_scores_table():
    names = list(SCORES)
    print("| Criterion | " + " | ".join(names) + " |")
    print("|---|" + "---:|" * len(names))
    for i, criterion in enumerate(CRITERIA):
        print(f"| {criterion} | " + " | ".join(fmt(SCORES[n][i]) for n in names) + " |")


def print_weighted_table():
    names = list(SCORES)
    print("| Criterion | Weight | " + " | ".join(f"{short(n)}: score x weight" for n in names) + " |")
    print("|---|---:|" + "---:|" * len(names))
    for i, criterion in enumerate(CRITERIA):
        cells = [fmt(SCORES[n][i] * WEIGHTS[i]) for n in names]
        print(f"| {criterion} | {WEIGHTS[i]} | " + " | ".join(cells) + " |")
    totals = {n: sum(s * w for s, w in zip(SCORES[n], WEIGHTS)) for n in names}
    print("| **Weighted total** | | " + " | ".join(f"**{fmt(totals[n])}**" for n in names) + " |")
    return totals


def print_ranking(totals):
    ranking = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    text = ""
    for k, (name, total) in enumerate(ranking):
        if k > 0:
            text += " = " if total == ranking[k - 1][1] else " > "
        text += f"{short(name)} ({fmt(total)})"
    print("Ranking on weighted score, before knock-outs: " + text)


def seven_ways_warnings():
    notes = []
    all_scores = [s for row in SCORES.values() for s in row]
    if 0 not in all_scores:
        notes.append("No score is 0 anywhere: 'every criterion made to matter, so none does'.")
    if any(WEIGHTS) and len(set(WEIGHTS)) == 1:
        notes.append(f"Every weight is {WEIGHTS[0]}: 'the case was not read'.")
    others = [row for name, row in SCORES.items() if name != BASELINE]
    if BASELINE in SCORES and others:
        base = SCORES[BASELINE]
        if all(base[i] <= min(row[i] for row in others) for i in range(len(CRITERIA))):
            notes.append("The baseline never beats another option on any criterion: "
                         "'filled in to be dismissed'.")
    return notes


def draw_radar(path):
    try:
        import matplotlib
        matplotlib.use("Agg")  # no window: the radar is written straight to an image file
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("\nmatplotlib is not installed, so no radar was drawn. Run:  pip install matplotlib")
        return

    # One colour AND one marker shape per option, so the lines can be told apart
    # without colour too (colour-blind readers, black-and-white printing).
    colours = ["#2a78d6", "#eb6834", "#1baf7a"]   # blue, orange, aqua
    markers = ["o", "s", "^"]                     # circle, square, triangle
    ink, soft_ink, grid = "#0b0b0b", "#52514e", "#e1e0d9"

    angles = np.linspace(0, 2 * np.pi, len(CRITERIA), endpoint=False).tolist()
    angles += angles[:1]  # repeat the first point to close each shape

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor("white")
    ax.set_theta_offset(np.pi / 2)   # first criterion at the top
    ax.set_theta_direction(-1)       # then clockwise
    ax.set_ylim(-3, 3)               # centre = -3, outer ring = +3
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticklabels(["-3", "-2", "-1", "0", "+1", "+2", "+3"], fontsize=8, color=soft_ink)
    ax.set_rlabel_position(18)       # score labels sit between the first two spokes
    for label in ax.get_yticklabels():
        label.set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1))
    ax.grid(color=grid, linewidth=0.8)
    ax.spines["polar"].set_color("#c3c2b7")
    ring = np.linspace(0, 2 * np.pi, 200)
    ax.plot(ring, [0] * len(ring), color=soft_ink, linewidth=1.2, linestyle="--")  # the 0 ring

    for k, (name, row) in enumerate(SCORES.items()):
        values = row + row[:1]
        colour = colours[k % len(colours)]
        ax.plot(angles, values, color=colour, linewidth=2, label=name,
                marker=markers[k % len(markers)], markersize=7)
        ax.fill(angles, values, color=colour, alpha=0.06)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([c.replace(" & ", " &\n") for c in CRITERIA], fontsize=10, color=ink)
    ax.tick_params(axis="x", pad=6)
    # push each criterion name away from the circle: right side left-aligned, left side right-aligned
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        if np.isclose(angle, 0) or np.isclose(angle, np.pi):
            label.set_horizontalalignment("center")
        elif angle < np.pi:
            label.set_horizontalalignment("left")
        else:
            label.set_horizontalalignment("right")
    ax.set_title("Reception robot: options A, B, C on the ten criteria\n"
                 "dashed ring = 0: outside it = adequate, inside it = inadequate",
                 pad=30, color=ink)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.14), frameon=False)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nRadar saved: {path}")


if __name__ == "__main__":
    problems = check_inputs()
    if problems:
        print("Fix these first:")
        for p in problems:
            print("  -", p)
        raise SystemExit(1)
    if not any(s for row in SCORES.values() for s in row):
        print("All scores are still 0: fill SCORES first, then WEIGHTS.")
        raise SystemExit(1)

    print("## Scores\n")
    print_scores_table()

    if any(WEIGHTS):
        print("\n## Weighted totals\n")
        totals = print_weighted_table()
        print()
        print_ranking(totals)
    else:
        print("\n(Weights are all 0 for now: fill WEIGHTS and run again to get the totals.)")

    print("\nAutomatic checks against 'Seven ways this grid goes wrong':")
    warnings = seven_ways_warnings()
    for w in warnings:
        print("  ! " + w)
    if not warnings:
        print("  no warning")
    print("Check by hand, the script cannot:")
    print("  - Cost and Energy: is the cheapest, most frugal option the one with the HIGHEST score?")
    print("  - Latency: is +3 given for 'inside the band', rather than for 'the fastest'?")
    print("  - Human control: did you score 'can someone stop it, take over, correct it in time',")
    print("    rather than 'is it easy to use'?")
    print("  - Knock-outs (item 4): does one remove an option, or do you give the value at which it would?")

    draw_radar(Path(__file__).with_name("radar.png"))
