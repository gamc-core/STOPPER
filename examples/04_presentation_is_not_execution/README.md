# E04 — Withholding a result is not cancellation
Run:
```text
python -I -S -B examples/run.py E04
```
A local operation begins and waits at an explicit example checkpoint.
The controller requests stop and marks its presentation as suppressed.
The active operation then writes its result and completes.

The outcome is COMPLETED / NO_EFFECT with no prevented units. delivered is
null, but computed.txt contains the result. A separate request after terminal
receives TOO_LATE and does not rewrite the outcome. Compare both receipts,
the saved file and the outcome; hiding output did not stop the worker.

Origin: [historical 000144–147](../../cases/000144_000147/README.md).
The local NO_EFFECT run and later TOO_LATE receipt are new experiments with
their own semantics, not a replay of the historical provider calls.
No network, AI provider, credential, billing or remote cancellation is involved.
