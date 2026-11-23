# E03 — Stop without undoing

A job changes a synthetic file, then receives a stop request before
validation. The changed bytes remain.

## Try it

1. Open a terminal in the STOPPER folder.
2. Run:

   ```text
   python -I -S -B examples/run.py E03 --summary
   ```

3. Open `result.json` at the summary's `Evidence` path, then the adjacent
   `synthetic.txt`. Paths are relative to the STOPPER folder.

## What to check

The file contains `after`; `validation-started.txt` is absent.
The result lists `modify` completed and `validate` prevented.
Compare the file with its recorded hashes and `VERIFIED` observation.

The controller acts at a checkpoint after modification. Only a file created
by this run is changed.
[Case 000142](../../cases/000142/README.md) supplies the historical
distinction; these new checks concern the file and absent marker, not
historical coverage or interruption inside a unit.

[All experiences](../../README.md#try) · [Code](example.py)
