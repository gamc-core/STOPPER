# E01 — The signal was not received
Run from the checkout:
```text
python -I -S -B examples/run.py E01
```
A request addressed to B is deliberately delivered to A. It is NOT_RECEIVED,
and neither worker observes a signal. Both complete their small local task.
This distinguishes wrong delivery from a received request with no effect (E04).

Check the receipt target, both outcomes, empty observed_at lists and actual
operation list in the printed/saved result. There is no file-copy dependency.
The evidence directory is under .runs; result.json remains available.

Origin: [historical 000129](../../cases/000129/README.md). This derived example
does not recreate the browser defect or establish a reliable message transport.
