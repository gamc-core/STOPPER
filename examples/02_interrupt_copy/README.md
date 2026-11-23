# E02 — Interrupt a copy

This example copies real files containing synthetic text. A controller requests
stop while the second file's unit is active. That file finishes; the remaining
three never start. The destination is a partial copy you can inspect.

## Run and inspect

1. Open a terminal in the repository root, containing `README.md` and
   `examples/`.
2. Run:

   ```text
   python -I -S -B examples/run.py E02
   ```

3. Find `status` and `evidence_directory` in the printed JSON. The expected
   status is `PASS`; the directory has a name such as `.runs/e02-...`.
   Use your actual returned path, relative to the repository root.
4. Open its `source/` and `destination/` folders. Source contains
   `sample-0.txt` through `sample-4.txt`; destination contains only
   `sample-0.txt` and `sample-1.txt`.
5. Open `result.json`. Under `outcomes.copy`, check `completed`,
   `prevented`, `state: STOPPED` and `effect: INTERRUPTED`.
6. Compare the listed files with the folders. The example also checks copied
   bytes against source SHA-256 values and verifies that every source is
   unchanged. Its `physical_observation` should be `VERIFIED`.

No manual stop timing is involved. The worker announces an active checkpoint;
the controller requests stop and releases it. The ten-second waits only detect
broken coordination. The [tests](../../tests/test_examples.py) include a control
using the same copy worker without a stop request: all five files complete.

[Historical case 000132](../../cases/000132/README.md) motivated this experiment.
The five synthetic files have their own results; they do not recreate the
historical 656-file partial. This example checks cooperation between files,
not interruption inside one file, resumability or maximum stopping latency.

[All experiences](../../README.md#try) · [Code](example.py) ·
[Result meanings](../../docs/CONTRACT.md#outcome)
