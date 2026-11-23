# E01 — The signal did not reach its target

A request addressed to job B is deliberately delivered to job A, which rejects
the target mismatch. Both jobs complete without observing a stop signal.

From the repository root:

```text
python -I -S -B examples/run.py E01
```

Open `result.json` in the printed `evidence_directory` under `.runs/`.
The receipt is `NOT_RECEIVED`, with `received: false`. Both outcomes
are `COMPLETED`, their `observed_at` lists are empty, and
`actual_operations` names both jobs.
Compare this with [E04](../04_presentation_is_not_execution/README.md),
where receipt produces no prevention.

[Case 000129](../../cases/000129/README.md) concerned a gesture that did not
reach intake. E01 makes failed receipt reproducible through a wrong target;
it does not recreate the browser defect or implement a message transport.

[All experiences](../../README.md#try) · [Contract](../../docs/CONTRACT.md)
