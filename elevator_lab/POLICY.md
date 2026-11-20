# My dispatch policy

Fill in this template yourself before asking the builders to implement it. Short bullets and a small table are enough. You may discuss ideas or ask AI to challenge them, but make and explain your own choices.

## Priorities

- What I prioritise: people already aboard first (don't add stops for a busy car), then avoiding waking up the idle car, then pickup distance. This balances aboard-passenger disruption and overall movement. These are proxies only, not measured waiting time or energy use.
- My exact selection rule: applied only to cars returned by `eligible_ids`:
  1. If an eligible car already has the caller's floor as a scheduled stop, choose it (no extra stop for anyone aboard).
  2. Else, if an eligible moving car has load <= 260 kg (about 4 passenger-equivalents), choose it (it is already travelling past the caller, so the idle car stays idle).
  3. Else choose the eligible car with the smallest floor distance to the caller.
  4. If still tied, use the tie-breaker below.
  If neither car is eligible, return `Decision(None, reason)` (WAIT).
- My deterministic tie-breaker: choose elevator A (earlier ID), so identical inputs always give the same decision.
- A tradeoff I accept: a lightly loaded passing car can be chosen even when the idle car is physically closer, so the caller may wait longer. I accept this to avoid moving the idle car, and because the extra stop only affects a few passengers. Once a car holds more than 260 kg I stop adding stops to it and use distance instead.

## Predictions before implementation

Use S1, one of S2/S3, and one valid scenario you create in scenarios.py. For your own case, change something meaningful: location, direction, load or scheduled stops. Name it S6.

| Scenario | My expected selection | Why it follows my policy | Benefit and cost / who is affected |
|---|---|---|---|
| S1 | A | A is eligible, moving down past floor 5 with 130 kg (<= 260), so rule 2 picks A. | Benefit: B stays idle. Cost: the caller at 5 may wait longer than if nearer B (1 floor away) came; the ~2 people aboard A get one extra stop. |
| S2 or S3 | B (S2) | A is eligible but carries 325 kg (> 260), so rule 2 does not apply. Rule 3: B is 1 floor away, A is 3 floors away, so B. | Benefit: ~5 people aboard A are not delayed. Cost: B is activated although A was already travelling that way. |
| S6: my scenario | A | S6 = A at floor 7 moving down, 260 kg, stop at 1; B idle at floor 5, 0 kg; call at floor 5 down. Both are eligible. A has no stop at 5 (rule 1 fails), but is moving with load exactly 260 kg (<= 260), so rule 2 picks A even though B is already on floor 5. | Benefit: tests the boundary that 260 kg still counts as "light". Cost: the caller waits for A to travel 2 floors although B is already there, and ~4 people aboard A get an extra stop. |

## Another defensible policy

- An alternative priority: always send the nearest eligible car (minimise pickup distance), ignoring load and existing journeys.
- A scenario where it could choose differently, and why: S1. Nearest-car picks B (1 floor away) while my policy picks A (3 floors away, but already travelling past floor 5). Nearest-car gives the caller a shorter pickup distance, but activates the idle car.

If your predicted choices contradict your general rule, resolve that before implementation. If review later changes your mind, note the revision in EVIDENCE.md and update the policy and code together.