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

## First physical example
- E01 distinguishes delivery to a wrong target from receipt without effect.
- E02 copied two of five synthetic files, stopped before the remaining three,
  and verified destination bytes and unchanged source hashes. The second
  active unit completed; no within-file interruption is claimed.
- Core plus first file examples: 26 tests passed. No timing sleeps were used.

## Negative finding before correction
- The additional identity regression failed: execution_id was assignable after
  construction. The 27-test run had one failure. This is a real protocol gap
  in the new code, not a historical AS failure.
- The regression and finding are recorded before fixing the binding. The raw
  local test log remains under .runs/identity_negative_before_fix.txt and is
  excluded from distribution. No source history is imported.

## Correction and file boundary
- execution_id now has a read-only public property. The negative regression
  passes; private attribute tampering remains outside the trusted-worker model.
- Reviewed workspace helpers: reject parent traversal before mkdir and reject
  reparse/link flags. Reparse-flag rejection has a controlled unit test; no
  Windows ACLs or real system links were changed to test it.
- The resulting focused suite passed 29 tests.

## Remaining scenarios and reuse
- E03 preserves a completed file modification and prevents validation.
- E04 completes local work, suppresses presentation, records NO_EFFECT, and
  demonstrates a later TOO_LATE receipt. No remote call is made.
- E05 uses the core in a separate arithmetic loop, with a full control run
  and a two-item partial. Control and stopped executions have distinct IDs.
- The first five-scenario execution passed, and the expanded suite passed
  34 tests. Final clean-copy verification is still pending at this stage.

## Packaging and lifecycle review
- A metadata probe found that wheel is absent. It did not install or run a
  package build. Removed the unverified offline pip command from README;
  retained the tested no-install source route and conventional metadata.
- The earlier metadata probe ended before reporting its navigation summary;
  the focused link check was completed separately. No product failure is
  inferred from a missing optional build tool.
- Added teardown checks for live example workers after every file-example test.

## First clean-copy finding
- Original and clean-copy runs each passed 34 tests; all five clean-copy
  examples passed and imported only the copied package.
- The byte-identity assertion nevertheless failed on 27 tracked files. The
  copy inherited system Git core.autocrlf=true; all differences were CRLF/LF.
  The earlier run and byte-mismatch evidence are retained, not relabeled PASS.
- Added repository-local .gitattributes with LF checkout policy and normalized
  candidate text. No global Git or canonical configuration was changed.
- A new copy must confirm the corrected bytes before reproduction is closed.

## Cut 4 — corrected clean reproduction and closure
- The corrected fresh Git copy matched tracked bytes before and after tests.
- Original and clean copies passed 34 tests each; the five clean-copy CLI
  scenarios passed. Import resolution pointed inside the new copy.
- Runtime remains standard-library-only and offline. No packaging build or
  external dependency installation was attempted.
- Focused history/path/import review found no private-pattern matches,
  linked tracked paths, private imports, Git alternates or remotes. Six
  consulted source-file hashes remained unchanged.
- Closing changes are documentary; executable hashes are compared with the
  tested revision rather than rerunning unchanged code for the closing prose.
- Final status is PRIVATE PUBLICATION CANDIDATE, never published.
