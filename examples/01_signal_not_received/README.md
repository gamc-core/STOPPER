# E01 — The signal did not reach its target

A request addressed to job B is delivered to job A, which rejects the target
mismatch. Both jobs complete without observing a stop signal.

## Try it

1. Open a terminal in the STOPPER folder containing `README.md` and
   `examples/`.
2. Run:

   ```text
   python -I -S -B examples/run.py E01 --summary
   ```

3. Read the summary, then open `result.json` at its `Evidence` path
   under `.runs/`. The path is relative to the STOPPER folder.

## What to check

The receipt is `NOT_RECEIVED`, with `received: false`. Both outcomes
are `COMPLETED`, and their `observed_at` lists are empty.
`actual_operations` names both jobs. Compare this with
[E04](../04_presentation_is_not_execution/README.md), where a received
request prevents no work.

[Case 000129](../../cases/000129/README.md) concerned a gesture that did not
reach intake. E01 makes failed receipt reproducible through a wrong target;
it does not recreate the browser defect or implement a message transport.

[All experiences](../../README.md#try) · [Contract](../../docs/CONTRACT.md)
