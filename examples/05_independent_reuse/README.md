# E05 — Use STOPPER in another operation

The `square_batch` function wraps an arithmetic loop with `Execution`,
independently of the copy worker.

## Try it

1. Open a terminal in the STOPPER folder.
2. Run:

   ```text
   python -I -S -B examples/run.py E05
   ```

3. Open `result.json` in the printed `evidence_directory`.

## What to check

The ordinary run returns `[4, 9, 16, 25, 36]`. A second run requests
stop after two completed values and returns `[4, 9]`; three units are
prevented. Compare the outcomes, distinct IDs and completed counts.
The supplied checker examines returned data rather than files.

To adapt [the loop](example.py), declare finite units and a distinct execution
ID. Call `begin` before each operation, `complete` after success, and
leave when `begin` returns false. A controller holding the job can request
stop; report operation failures explicitly.
The [contract](../../docs/CONTRACT.md) gives the details.

This derived example has no separate historical episode. It demonstrates a
local integration and control; other operations need their own cooperation
points.

[All experiences](../../README.md#try) · [Implementation](../../src/stopper/core.py)
