# 000132 — a partial copy remained
**Historical checked evidence:** 19 September 2026. A human authorized an
innocuous proposed change and then used a double-click stop gesture while its
isolated environment was being prepared. The copy was abandoned between files.
A partial containing 656 files remained invalid; the mutation backend did not
run. "Quarantine" was a logical invalidation, not a demonstrated directory move.

The request and settlement timestamps differ by 0.010006 seconds. This is an
interval between recorded events, not total human response time or a general
latency guarantee. The later 44-test historical result concerns its old bytes.

**Interpretation:** interruption can be effective within a bounded cooperative
operation while leaving a partial that must not be treated as ready.

**Derived example:** [E02](../../examples/02_interrupt_copy/README.md) copies
synthetic data with its own counts. It does not copy the private tree or
reproduce the 656-file number.
**New tests:** compare the new reports with destination bytes and source hashes.

[Provenance and omissions](../../docs/ORIGIN.md)
