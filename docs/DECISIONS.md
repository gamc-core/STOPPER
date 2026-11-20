# Development decisions

## Cut 1 — scope before code
- Destination did not exist. The new repository is separate from the source.
- Chosen seam: conventional threading.Event, one cooperative execution and a
  finite ordered unit list. No private authority or persistence module is copied.
- Worker reports and physical checking remain distinct.
- The seven proposed invariants are retained with computable boundaries in the
  contract. "Prevented" excludes a unit once begun, even if not completed.
- No public remote, source Git objects, credentials, or raw conversations.
- Local Git attribution uses GAMC and a reserved .invalid email to avoid placing
  a personal email in candidate history. This is not identity authentication.
- The implementation executor for this delivery is Codex.
- New code and original project documentation/data: MIT (LICENSE).
  Historical summaries will be new, sanitized descriptions, not raw dumps.
