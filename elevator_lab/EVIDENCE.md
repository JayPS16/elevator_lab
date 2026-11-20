# My experiment results

Fill in this template with actual observations. Short bullets are sufficient.

Name / student ID: Sorawich Pimsen / 6681297

Tool, visible software version and model(s): GitHub Copilot Chat in VS Code (Agent mode), "Copilot Fusion" selector, which chose model gpt-5.6-luna for the workers. Exact software version: unknown.

Route: automatic workers (two background agents launched from one coordinator chat), plus a separate fresh chat session for the reviewer.

## Agent outputs

| Role | What it delivered | Brief excerpt or screenshot link |
|---|---|---|
| Dispatcher builder | Edited dispatcher.py directly, implementing my 4-step rule (scheduled stop, then moving car <= 260 kg, then nearest, then A). | Worker entry "Build dispatcher policy" (gpt-5.6-luna); "Background agent Build dispatcher policy is complete"; "Dispatcher Builder edited dispatcher.py directly." |
| Display builder | Edited app.py directly: prints each scenario's state, request, decision and reason, and returns the decisions list. | Worker entry "Build scenario display" (gpt-5.6-luna); "Background agent Build scenario display is complete"; "Display Builder edited app.py directly." |
| Reviewer | Found no implementation defects. Flagged that S6 was missing from scenarios.py (my pasted file had not reached the repo), and named a tradeoff: S1 picks passing car A even though idle B is nearby. | "No implementation defects were found in the app/dispatcher interface."; "Policy tradeoff: accepted waiting-time increase." |

## Compare with my predictions

Run `python app.py` after adding S6. Compare with the predictions you wrote in POLICY.md before implementation.

| Scenario | Expected selection | Actual selection and reason | Matches my policy? |
|---|---|---|---|
| S1 | A | A: Rule 2, A is moving with load 130 kg (<= 260 kg limit) | Yes |
| S2 | B | B: Rule 3, B is nearest eligible car at 1 floor away (A has 325 kg, over the limit) | Yes |
| S6 | A | A: Rule 2, A is moving with load 260 kg (inclusive boundary) even though B is already on floor 5 | Yes |

- Supplied suite command and actual result: `python -m unittest -v` gave `Ran 6 tests in 0.004s OK`, both before and after adding S6.
- One review finding or concern I checked: the reviewer said POLICY.md requires S6 but SCENARIOS in scenarios.py ended at S5, so my 260 kg boundary prediction could not be run. I checked the file and confirmed S6 was missing. The reviewer labelled this a policy inconsistency, but it was really a missing scenario entry rather than a flaw in the policy. Decision: the fix was justified.
- Change made, if needed: I added the S6 scenario to scenarios.py (A at floor 7 moving down, 260 kg, stop at 1; B idle at floor 5, 0 kg; call at floor 5 down), re-ran the tests and `python app.py`. The policy and predictions were not changed.
- Does my policy serve my stated priority? Partly. In S6 it keeps idle car B from being woken, and A has only about four people aboard. But the cost is real: B is already on floor 5 and A must travel 2 floors, so the caller waits longer. The policy trades caller wait for not moving the idle car. Both are proxies, not measured waiting time or energy use. A minor limitation: the reason text always ends with "tie-breaker favors A when needed", even when there was no tie, which is slightly misleading.
- What did I have to coordinate between the agents? The two builders ran in parallel with exclusive file ownership (dispatcher.py and app.py), so there were no conflicts. I had to approve their terminal command prompts myself, and the review caught a gap neither builder could see (S6 missing), because the reviewer read the actual files instead of trusting the summaries.
