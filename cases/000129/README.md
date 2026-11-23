# 000129 — A stop gesture did not reach the receiver

19 September 2026 (UTC records)

An operator was trying a small authorized edit and attempted to stop it through
the interface. The preserved diagnosis says the double-click gesture never
reached the stop receiver. No corresponding intake or settlement record was
identified. The isolated edit ran, and its validation failed.

Those are two different outcomes: the stop channel failed to receive the
gesture, and validation later found a problem. The validation failure cannot
be counted as an effective stop.

The exact gesture time is not recoverable from an intake record. The later
diagnosis and the execution record support different parts of the account;
neither fills that gap.

[E01](../../examples/01_signal_not_received/README.md) makes failed receipt
observable with a request sent to the wrong execution object. Its new
wrong-target and isolation checks express the distinction without recreating
the historical interface defect.

[Origin and source record](../../docs/ORIGIN.md#source-record) ·
[All experiences](../../README.md#try)
