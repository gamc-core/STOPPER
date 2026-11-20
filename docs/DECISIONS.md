# Development decisions

## Cut 1 â€” scope before code
- Destination did not exist. A new repository was initialized before implementation.
- Conventional threading.Event; one cooperative execution, finite ordered units.
- Worker reports and physical checking remain distinct.
- Seven invariants retain computable boundaries in the contract.
- No source Git history, private runtime, raw conversations or public remote.
- Local Git attribution uses GAMC and a reserved .invalid email; it does not
  authenticate identity or expose a personal email.
- The actual implementation executor is Codex.
- New code and original project documentation/data: MIT. Historical summaries
  will be new sanitized descriptions, not raw dumps.

## Cut 2 â€” first capability
- Implemented ordered begin/complete/finish, distinct receipts and immutable
  outcome snapshots. The caller owns its worker and must respect begin.
- Added read/write signal errors, late and duplicate receipt handling, and a
  separate physical-check result (VERIFIED / MISMATCH / ERROR).
- First execution of the core suite: 22 tests passed on Windows, Python 3.10.6.
  This result concerns the new code, not the historical AS implementation.
