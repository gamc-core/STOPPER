# E04 — Withhold a result

A local operation has begun when the controller requests stop and suppresses
delivery. The operation still writes its result and completes.

## Try it

1. Open a terminal in the STOPPER folder.
2. Run:

   ```text
   python -I -S -B examples/run.py E04 --summary
   ```

3. Open `result.json` at the summary's `Evidence` path and compare it with
   the adjacent `computed.txt`. Paths are relative to the STOPPER folder.

## What to check

The file contains the result although `delivered` is null.
`COMPLETED / NO_EFFECT` records that the request prevented no work.
A second request after completion receives `TOO_LATE` without rewriting
the outcome. Compare both receipts with the saved file.

The worker and controller use an explicit checkpoint.
[Cases 000144–147](../../cases/000144_000147/README.md) involved late
conversational stops and later local suppression. This run and its separate
late request are new, local experiments. No provider or network is involved;
they establish no remote cancellation or billing effect.

[All experiences](../../README.md#try) · [Code](example.py)
