# E02 — Interrupt a copy between files
Run:
```text
python -I -S -B examples/run.py E02
```
Five tiny source files are created in a new .runs directory. The worker
completes the first file, begins the second and signals an explicit active
checkpoint. The controller requests stop and releases the worker.

The second active file finishes. Before starting the third, begin observes
the signal. Exactly two files remain in destination; three never start.
The checker compares destination names/bytes with completed and source hashes,
and checks that sources are unchanged. Inspect source/, destination/ and
result.json in the evidence directory to contrast the report yourself.

The ordinary counterfactual uses this same worker with request_stop=False in
the test suite and completes all five files. No arbitrary sleep chooses the
request timing; timeouts only detect a broken coordination.

Origin: [historical 000132](../../cases/000132/README.md). The five synthetic
files are new data. This is not the historical 656-file copy, an interruption
inside a file, a resumable copy, or a latency guarantee.
