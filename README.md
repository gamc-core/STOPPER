# STOPPER
*Cooperative stopping and observable outcomes*

**You asked it to stop. What actually stopped?**

A batch job may receive your stop request, finish its current unit, and leave
some work behind. STOPPER helps a cooperating worker report that difference:
request received, signal observed, units completed, and units not started.

For people writing local Python batch operations they can instrument. The
library does not run or kill threads. A worker checks before starting each unit.
No network, service, private runtime, or runtime dependency is required.

**Status: private publication candidate. Publication requires GAMC's decision.**

## Understand → Try → Use → Examine

### Try
From this checkout, with Python 3.10 or later:

```text
python -I -S -B examples/run.py all
python -I -S -B tests/run.py
```

No installation or download is needed. Actually tested on Windows 10 with
CPython 3.10.6; other platforms/versions are unverified.

Each example prints one JSON result. Synthetic files and saved results remain
inside `.runs/` in this checkout, with a new directory per execution.
Nothing is copied from your projects or private history.
Do not use a checkout whose files/parents another actor is replacing.

| Example | What to look for |
| --- | --- |
| [E01: signal not received](examples/01_signal_not_received/README.md) | Wrong target; both jobs complete. |
| [E02: interrupt a copy](examples/02_interrupt_copy/README.md) | Two files copied, three not started; bytes checked. |
| [E03: stopping is not undo](examples/03_stop_is_not_undo/README.md) | Modified file remains; validation never starts. |
| [E04: presentation is not execution](examples/04_presentation_is_not_execution/README.md) | Work completes although delivery is suppressed. |
| [E05: independent reuse](examples/05_independent_reuse/README.md) | A separate arithmetic batch uses the same library. |

The workers synchronize at explicit checkpoints. Timeout values only detect a
broken example; they do not choose when a request should arrive.

### Use
In your own environment, add this checkout's `src` to the module search path,
or install the local project with your existing pip/setuptools tools
(`pip install --no-index --no-build-isolation --no-deps .`).
The no-install commands above are the tested offline reproduction route.

```python
from stopper import Execution

job = Execution("my-distinct-job-id", ["first", "second"])
for unit in ("first", "second"):
    if not job.begin(unit):
        break
    do_your_unit(unit)  # Your operation; an active unit must finish or fail.
    job.complete(unit)
outcome = job.finish()

# A controller holding this object may call, while the worker is active:
# receipt = job.request_stop("my-request-id", job.execution_id)
```

If your operation raises, report `job.fail("operation failed")`; do not call
`complete` for work you cannot confirm. Keep the real exception in your own
appropriate logs. [E05](examples/05_independent_reuse/example.py) is a runnable,
caller-owned integration.

A receipt confirms intake, not interruption. Inspect the outcome; compare it
with the actual files/data you care about. `observe_effects(outcome, checker)`
keeps VERIFIED, MISMATCH and ERROR separate. A supplied checker is not an
independent certificate.

### Examine
- [Contract and seven bounded invariants](docs/CONTRACT.md)
- [Origin, derivation and historical cases](docs/ORIGIN.md)
- [Development decisions and real failed regression](docs/DECISIONS.md)
- [Candidate verification and reproduction](docs/VERIFICATION.md)
- [Tests](tests/) and [implementation](src/stopper/core.py)

### Limits
Cooperation happens between units. STOPPER does not interrupt an active file
copy, undo changes, cancel a remote model, terminate subprocesses, resume any
partial job, or guarantee a stopping time. IDs are local labels, not authority.
It relies on the worker respecting the protocol and reporting honestly.

## Origin and license
Derived from human experiences in Arquitectura Simbiotica / DOJO, with a new
implementation using Python's conventional `threading.Event`.
The private runtime and Git history were not imported. Historical summaries
and new experiments are explicitly separated.

Copyright 2026 Gonzalo Montero (GAMC). New code, project documentation and
synthetic example data are under [MIT](LICENSE). Underlying private source
records and conversations are not distributed or relicensed.
