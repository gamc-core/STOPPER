# 000132 — The copy stopped and left a partial workspace

19 September 2026

An operator authorized a harmless proposed change, then double-clicked to stop
while the system was preparing an isolated workspace. The copy was abandoned
between files, leaving an invalid partial workspace containing 656 files.
The mechanism that would apply the proposed change did not run.

The record called the partial workspace quarantined: it was marked invalid,
but no physical move of the directory was established.
The incomplete workspace remained something to account for, rather than a
ready result.

The request and settlement timestamps differ by 0.010006 seconds. That is an
interval between recorded events, not the person's total waiting time or a
general latency guarantee. The later 44-test result applies to the historical
code revision.

This episode showed a useful boundary: preparation could be abandoned while
its partial output remained visible and unusable as a complete workspace.
[E02](../../examples/02_interrupt_copy/README.md) builds a new, synthetic copy
experiment around that distinction. Its own file counts and byte checks do
not reproduce the private tree or inherit the historical test result.

[Origin and source record](../../docs/ORIGIN.md#source-record) ·
[All experiences](../../README.md#try)
