# E04 — Withhold a result

A local operation has begun when the controller requests stop and suppresses
delivery. The operation still writes its result and completes.

From the repository root:

```text
python -I -S -B examples/run.py E04
```

In the printed `evidence_directory`, `computed.txt` contains the result.
In `result.json`, `delivered` is null, while the outcome is
`COMPLETED / NO_EFFECT` with no prevented units.
A second request after completion receives `TOO_LATE` without rewriting
that outcome. Compare both receipts with the file.

The worker and controller use an explicit checkpoint.
[Cases 000144–147](../../cases/000144_000147/README.md) involved late
conversational stops and later local suppression. This local run and its
separate late request are new experiments. No provider or network is involved;
they establish no remote cancellation or billing effect.

[All experiences](../../README.md#try) · [Code](example.py)
