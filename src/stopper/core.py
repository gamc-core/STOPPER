"""Small in-process protocol using a conventional threading.Event."""
from dataclasses import asdict, dataclass, replace
from threading import Event, RLock
from typing import Callable, Iterable


class ContractError(ValueError):
    """The worker attempted an operation outside its declared protocol."""


class SignalError(RuntimeError):
    """A signal read or write failed; no successful stop is inferred."""


@dataclass(frozen=True)
class Receipt:
    request_id: str
    target_id: str
    received: bool
    status: str
    signal_set: bool


@dataclass(frozen=True)
class Outcome:
    execution_id: str
    state: str
    effect: str
    planned: tuple[str, ...]
    started: tuple[str, ...]
    completed: tuple[str, ...]
    not_started: tuple[str, ...]
    prevented: tuple[str, ...]
    request_ids: tuple[str, ...]
    observed_at: tuple[str, ...]
    error: str | None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Observation:
    status: str
    detail: str

    @property
    def confirmed(self) -> bool:
        return self.status == "VERIFIED"

    def to_dict(self) -> dict:
        return asdict(self)


def _label(value: str, kind: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(kind + " must be a nonempty string")
    return value


class Execution:
    """One ordered cooperative job. The caller owns its worker and effects.

    A custom signal_factory must return a fresh per-execution adapter implementing
    set() and is_set(). The default Event does so. It is not a security boundary.
    """

    def __init__(
        self, execution_id: str, units: Iterable[str], *, signal_factory=Event
    ):
        self.execution_id = _label(execution_id, "execution_id")
        self._units = tuple(units)
        if not self._units:
            raise ContractError("declare at least one unit")
        for unit in self._units:
            _label(unit, "unit")
        if len(set(self._units)) != len(self._units):
            raise ContractError("unit names must be unique")
        self._signal = signal_factory()
        self._lock = RLock()
        self._started: list[str] = []
        self._completed: list[str] = []
        self._active: str | None = None
        self._requests: dict[str, Receipt] = {}
        self._observed: list[str] = []
        self._terminal: Outcome | None = None

    def _snapshot(self, state="RUNNING", effect="PENDING", error=None) -> Outcome:
        not_started = self._units[len(self._started):]
        return Outcome(
            self.execution_id, state, effect, self._units,
            tuple(self._started), tuple(self._completed), not_started,
            not_started if state == "STOPPED" else (),
            tuple(self._requests), tuple(self._observed), error,
        )

    def snapshot(self) -> Outcome:
        with self._lock:
            return self._terminal or self._snapshot()

    def _fail(self, where: str, exc: Exception) -> None:
        self._terminal = self._snapshot(
            "FAILED", "UNKNOWN", where + ": " + type(exc).__name__ + ": " + str(exc)
        )

    def request_stop(self, request_id: str, target_id: str) -> Receipt:
        request_id = _label(request_id, "request_id")
        target_id = _label(target_id, "target_id")
        with self._lock:
            if target_id != self.execution_id:
                return Receipt(request_id, target_id, False, "NOT_RECEIVED", False)
            if request_id in self._requests:
                return replace(self._requests[request_id], status="DUPLICATE")
            if self._terminal is not None:
                return Receipt(request_id, target_id, True, "TOO_LATE", False)
            receipt = Receipt(request_id, target_id, True, "RECEIVED", False)
            self._requests[request_id] = receipt
            try:
                self._signal.set()
            except Exception as exc:
                self._fail("signal.set", exc)
                raise SignalError(self._terminal.error) from exc
            receipt = replace(receipt, signal_set=True)
            self._requests[request_id] = receipt
            return receipt

    def _read_signal(self, point: str) -> bool:
        try:
            pending = self._signal.is_set()
            if type(pending) is not bool:
                raise TypeError("is_set must return bool")
        except Exception as exc:
            self._fail("signal.is_set", exc)
            raise SignalError(self._terminal.error) from exc
        if pending:
            self._observed.append(point)
        return pending

    def begin(self, unit: str) -> bool:
        with self._lock:
            if self._terminal is not None:
                return False
            if self._active is not None:
                raise ContractError("complete the active unit before starting another")
            index = len(self._started)
            if index >= len(self._units) or self._units[index] != unit:
                raise ContractError("begin must follow the declared unit order")
            if self._read_signal("before:" + unit):
                effect = "INTERRUPTED" if self._completed else "PREVENTED_FUTURE"
                self._terminal = self._snapshot("STOPPED", effect)
                return False
            self._active = unit
            self._started.append(unit)
            return True

    def complete(self, unit: str) -> None:
        with self._lock:
            if self._terminal is not None or self._active != unit:
                raise ContractError("only the active unit may be completed")
            self._completed.append(unit)
            self._active = None

    def finish(self) -> Outcome:
        with self._lock:
            if self._terminal is not None:
                return self._terminal
            if self._active is not None or len(self._completed) != len(self._units):
                raise ContractError("unfinished work cannot be declared complete")
            self._read_signal("terminal_boundary")
            effect = "NO_EFFECT" if self._requests else "NONE"
            self._terminal = self._snapshot("COMPLETED", effect)
            return self._terminal

    def fail(self, detail: str) -> Outcome:
        with self._lock:
            if self._terminal is None:
                self._fail("worker", RuntimeError(detail))
            return self._terminal


def observe_effects(
    outcome: Outcome, check: Callable[[Outcome], bool]
) -> Observation:
    """Run a caller-supplied checker without upgrading a failed observation."""
    if outcome.state == "RUNNING":
        raise ContractError("observe terminal effects after the worker has settled")
    try:
        result = check(outcome)
        if type(result) is not bool:
            raise TypeError("physical checker must return bool")
        return Observation(
            "VERIFIED" if result else "MISMATCH",
            "The supplied checker returned " + str(result) + ".",
        )
    except Exception as exc:
        return Observation("ERROR", type(exc).__name__ + ": " + str(exc))
