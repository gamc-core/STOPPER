# E05 — Reuse in a caller-owned batch
Run:
```text
python -I -S -B examples/run.py E05
```
The square_batch function in example.py uses Execution around a small arithmetic
loop. It imports no file-copy worker and requires no private state.

The ordinary run returns five squared values. In the second run, a controller
requests stop after two completed values; the next begin cooperates. The two
values remain, and the other three are prevented. Inspect both outcomes and
the value lists. Execution IDs distinguish the two runs.

To adapt the integration: declare a finite unit list, assign a distinct run ID,
call begin before your operation and complete only after success. Keep your
controller's reference to that job. Handle your operation's failures explicitly.
The core protocol is shared; the arithmetic loop belongs to its caller.

This is a derived reuse example, not an additional historical case. It
demonstrates local integration and an ordinary control, not usefulness already
validated by outside users or suitability for noncooperative operations.
