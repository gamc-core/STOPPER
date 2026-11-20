"""Cooperative stopping. Worker reports are not independent physical proof."""
from .core import (
    ContractError, Execution, Observation, Outcome, Receipt, SignalError,
    observe_effects,
)

__version__ = "0.1.0"
__all__ = [
    "ContractError", "Execution", "Observation", "Outcome", "Receipt",
    "SignalError", "observe_effects",
]
