# E02 — Interrupt a copy

A controller requests stop while the second file's unit is active. That file
finishes; three others never start. The destination is a partial copy of
synthetic text files you can inspect.

## Try it

1. Open a terminal in the STOPPER folder containing `README.md` and
   `examples/`.
2. Run:

   ```text
   python -I -S -B examples/run.py E02
   ```

3. Find `evidence_directory` in the result. Open that folder, relative to
   the STOPPER folder.
4. Open `source/`, `destination/` and `result.json` inside it.

## What to check

Source contains `sample-0.txt` through `sample-4.txt`. Destination
contains only `sample-0.txt` and `sample-1.txt`.

In `result.json`, `outcomes.copy` lists two `completed` files and
three `prevented` files. `STOPPED / INTERRUPTED` means the job left
its loop at a cooperation boundary, not inside the active file copy.

The expected result is `PASS`, with a `VERIFIED` physical observation:
the supplied checker compares copied bytes with source hashes and checks
that all sources are unchanged. Compare the listed names with the actual
folders yourself.

The request is automatic at an explicit checkpoint; no manual timing is
needed. Ten-second waits detect broken coordination.
The [tests](../../tests/test_examples.py) include the same copy without
a request, which completes all five files.

[Case 000132](../../cases/000132/README.md) motivated this new experiment.
These five files do not recreate its 656-file partial or inherit its tests.
The example checks cooperation between files, not resumability or maximum
stopping latency.

[All experiences](../../README.md#try) · [Code](example.py) ·
[Result meanings](../../docs/CONTRACT.md#outcome)
