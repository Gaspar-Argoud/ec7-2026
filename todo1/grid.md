# todo1/grid.md — EC7 multicriteria grid: the reception robot

## Grid: score (weight) and the one-sentence why, per option

| Criterion — weight, because | **A** — closed grammar | **B** — local ASR + rules | **C** — hosted API |
|---|---|---|---|
| **Latency** — w=5, because 200 people/h at peak and the case's own rule: show it heard within 1 s or voices overlap | **+3** — a local exact match runs in microseconds, far inside the 1 s bar | **+2** — local streaming ASR is comfortably under 1 s but noisier than a fixed match | **−2** — a network round trip risks crossing 1 s under load or a weak link |
| **Total cost** — w=2, because the case gives no budget figure, only a two-person IT team | **+3** — a one-off local script, no licence, no per-call fee | **+1** — an upfront model/box cost, but no per-call fee afterwards | **−1** — cheap per call, but the bill scales with every query, forever |
| **Energy** — w=1, because the case states no energy constraint at all | **+3** — a small box doing string matching draws almost nothing | **+1** — local inference needs real on-site compute, more draw than A | **0** — the draw happens off-site; nothing in the case scores it either way |
| **Streaming vs complete info** — w=5, because the "heard within 1 s" rule needs an incremental signal, not a finished answer | **+2** — matches short fixed templates fast, but is not true streaming | **+3** — a modern local ASR emits partial output as speech arrives | **+1** — can stream too, but only after audio has already left the building |
| **Deployment & sovereignty** — w=5, because IT blocks unapproved outbound traffic and approval takes about a month | **+3** — fully on-device, nothing to approve, works with no network link | **+3** — stays on the hall's own hardware, no new outbound service needed | **−3** — needs a newly-approved outbound service; dead on arrival for a fast rollout |
| **Robustness** — w=4, because the glass ceiling rings and the coffee machine masks input for 30 s bursts | **−1** — exact matching has no acoustic tolerance; noise makes it miss rather than degrade | **+2** — a trained recogniser tolerates reverb and noise better than a fixed script | **+2** — plausibly the most noise-tolerant model, but this can't be verified before approval |
| **Explainability** — w=3, because the supervisor must justify the exact answer given last Tuesday | **+3** — an exact phrase list; the "why" is a direct table lookup | **+1** — transcript + fired rule is traceable; the ASR step itself is not | **−1** — not inspectable, and a silent vendor model update can break replay entirely |
| **Confidentiality** — w=4, because the open mic hears conversations never addressed to it | **+3** — audio is matched and discarded on the box; nothing to leak | **+2** — stays on-site, but a local transcript log still needs guarding | **−3** — sends non-consenting bystanders' speech to a third party |
| **Maintainability** — w=4, because a two-person IT team maintains whatever gets installed | **+2** — adding an entry is a text edit; more entries still means more manual upkeep | **+1** — a model plus a runtime on a box: heavier, but still fully in-house | **+2** — the vendor handles upgrades — lightest day-to-day load, if it were ever approved |
| **Human control** — w=5, because failing to fetch a human is explicitly what gets the robot switched off | **+2** — a guaranteed trigger, but only for its twenty exact phrasings | **+3** — free phrasing plus a hard keyword override catches far more real requests | **0** — as capable in principle, but the outcome depends on a link nobody here controls |
| **Coverage of the user population** *(additional)* — w=3, because ~30 different visitors an hour is not a uniform crowd | **−2** — assumes every visitor already knows one of the twenty magic phrasings | **+2** — a general recogniser handles varied accents and phrasings better | **+3** — the broadest training data of the three, its clearest strength |

## Weighted totals

Sum of weights = 41 (theoretical range = −123 to +123).

| | **A** | **B** | **C** |
|---|---|---|---|
| **Weighted score** | 78 | **87** | −12 |

## Radar

![Radar chart of the ten criteria plus coverage, for options A, B and C](radar.png)

The shapes say more than the totals: **A** is a wide, confident disc everywhere except robustness and coverage — spiky where a script can't bend. **C** is the mirror image: strong on coverage and robustness, hollow and often negative exactly where the hall's own constraints (deployment, confidentiality, latency) bite. **B** is the roundest of the three — never the single best on any one axis, never badly hollow on any either, which is why it leads on the total without depending on one fragile strength.

## Recommendation
I recommend **Option B** — the local pre‑trained recogniser with a rule-based intent layer. It scores highest (87/123) and avoids all the hard blockers.
It stands out because it stays fully on‑site, doesn’t require any new IT‑approved outbound service, and still meets the 1‑second acknowledgement requirement.
**Option A** (78) is a workable backup if B’s model can’t be obtained in time, but its limit of ~20 fixed phrases makes it fragile for real visitor speech.
**Option C** (−12) isn’t just the lowest score — it’s ruled out entirely due to deployment delays and confidentiality issues that no future accuracy improvement can fix.
The main risk to manage in B is escalation: “call a human” must be a strict keyword override outside the classifier’s confidence logic, since missing an escalation is the one failure the case says gets the robot shut down.

## Knock‑out
**Deployment & sovereignty.**  
The case states that getting IT approval for a new outbound service takes **about a month**. Given the robot must be operational roughly **two weeks** after installation, anything requiring new outbound traffic can’t be ready in time. Option C depends on exactly that, so it’s blocked regardless of its other scores — this isn’t a performance penalty, it’s a hard stop.

**Confidentiality.**  
The microphone picks up speech from bystanders who never intended to interact with the device. Any solution that streams that raw hall audio to an external service violates confidentiality outright. Even if IT approval were instant, this alone removes Option C from consideration.
Option C was already last (−12), so these knock‑outs don’t change the ranking — they simply confirm that C can never be made viable later. No accuracy improvement can fix an approval delay or a sovereignty breach.
Option B remains the choice. Even though its recogniser isn’t fully inspectable, it offers strong free‑form understanding, keeps all data local, and avoids the cost and risk of external calls — exactly what the two‑person IT team can support.

## The context moves
*Same three options, same criteria, but now the product is a consumer mobile app: no hall, no IT department, a million users.*

**Which weight changes first, and why?**
Cost becomes the dominant factor. At a million users, even a few cents per cloud call becomes a major recurring expense, so its weight should increase (e.g., from 2 to 5). As a consequence, Deployment & sovereignty becomes less important (no internal IT gatekeeping), and Coverage becomes more important because the user base is now global.

**Does the winner change?**
No — **Option B still wins**, and even more clearly. In a mobile context, “local” means on‑device recognition, which has zero marginal cost and keeps user audio private. Option C becomes even less competitive because its per‑call cost scales with usage. Option A’s rigid phrase list becomes even more limiting for a general audience.

**Which constraints survive, and which disappear?**
The **1‑second acknowledgement** constraint stays — mobile users abandon apps quickly if feedback isn’t immediate.
The **escalation constraint** survives but changes form: instead of paging staff, it becomes handing off to live support.
The **IT‑approval delay** disappears entirely — there’s no internal network to protect, so outbound calls aren’t blocked. Cost becomes the new practical limiter for Option C instead.
