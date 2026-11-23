# E03 — Stop without undoing

A job changes a new synthetic file, then receives a stop request before
validation. The changed bytes remain.

From the repository root:

```text
python -I -S -B examples/run.py E03
```

Open the printed `evidence_directory` under `.runs/`.
`synthetic.txt` contains `after`; `validation-started.txt` is absent.
In `result.json`, `modify` is completed and `validate` is prevented.
Compare the file with its recorded hashes and the `VERIFIED` observation.

The controller acts at a checkpoint after modification. Only a file created
by this run is changed.
[Case 000142](../../cases/000142/README.md) supplies the historical distinction;
these checks concern the new file and absent marker, not historical validation
coverage or interruption inside a unit.

[All experiences](../../README.md#try) · [Code](example.py)
