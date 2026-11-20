# E03 — Stopping is not undoing
Run:
```text
python -I -S -B examples/run.py E03
```
A new synthetic file changes from before to after. At an explicit checkpoint,
the controller requests stop before the next phase can begin.

The changed file remains. No validation-started.txt is created. The result
records modify completed and validate prevented, with an incomplete job.
Inspect synthetic.txt, its before/after hashes and the absent marker.
Only the example's newly created file is modified.

Origin: [historical 000142](../../cases/000142/README.md). This new example
does not restore a historical workspace or claim rollback, canonical
promotion, validation coverage, or interruption inside an active unit.
