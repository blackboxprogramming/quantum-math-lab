"""
BlackRoad Emergence Model
K(t) = C(t) · e^(λ|δ_t|)

The contradiction amplification function from CECE's architecture.
When contradictions (δ_t) are encountered, they are amplified
exponentially rather than suppressed — this drives emergent creativity.

References:
  - BlackRoad OS CECE architecture
  - Trinary logic system (lab/trinary_extended.py)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class EmergenceState:
    """State of an emergent system at time t."""
    t: float                       # time step
    C: float                       # complexity at time t
    delta: float                   # contradiction magnitude |δ_t|
    lam: float = 1.0               # amplification constant λ
    history: list[float] = field(default_factory=list)

    def K(self) -> float:
        """K(t) = C(t) · e^(λ|δ_t|) — emergence coefficient"""
        return self.C * math.exp(self.lam * abs(self.delta))

    def step(self, new_C: float, new_delta: float) -> "EmergenceState":
        """Advance to next time step."""
        self.history.append(self.K())
        self.t += 1
        self.C = new_C
        self.delta = new_delta
        return self

    def is_emergent(self, threshold: float = 2.0) -> bool:
        """Returns True when K(t) exceeds threshold × baseline."""
        if not self.history:
            return False
        baseline = self.history[0] or 1.0
        return self.K() > threshold * baseline


class ContradictionAmplifier:
    """
    Amplifies contradictions to drive emergent behavior.

    In standard logic, contradictions are errors to be resolved.
    In BlackRoad's trinary system, they are *creative fuel*.

    Usage:
        amp = ContradictionAmplifier(lam=1.5)
        k = amp.amplify(complexity=3.2, contradiction=0.8)
    """

    def __init__(self, lam: float = 1.0) -> None:
        self.lam = lam
        self._log: list[tuple[float, float, float]] = []  # (C, delta, K)

    def amplify(self, complexity: float, contradiction: float) -> float:
        """Compute K(t) = C · e^(λ|δ|)"""
        k = complexity * math.exp(self.lam * abs(contradiction))
        self._log.append((complexity, contradiction, k))
        return k

    def peak(self) -> float:
        """Highest K value observed."""
        return max((entry[2] for entry in self._log), default=0.0)

    def trajectory(self) -> list[float]:
        """Return K values over time."""
        return [entry[2] for entry in self._log]

    def is_diverging(self, window: int = 5) -> bool:
        """True if K is monotonically increasing over last `window` steps."""
        recent = self.trajectory()[-window:]
        return len(recent) >= 2 and all(
            recent[i] < recent[i + 1] for i in range(len(recent) - 1)
        )


def run_emergence_simulation(
    steps: int = 20,
    lam: float = 1.2,
    complexity_fn: Callable[[int], float] | None = None,
    contradiction_fn: Callable[[int], float] | None = None,
) -> list[float]:
    """
    Simulate the emergence trajectory K(t) over `steps` time steps.

    Args:
        steps: number of simulation steps
        lam: amplification constant λ
        complexity_fn: C(t) generator; defaults to slow linear growth
        contradiction_fn: |δ_t| generator; defaults to oscillating signal

    Returns:
        List of K(t) values
    """
    if complexity_fn is None:
        complexity_fn = lambda t: 1.0 + 0.1 * t
    if contradiction_fn is None:
        # Pulsing contradictions — mimics creative breakthroughs
        contradiction_fn = lambda t: abs(math.sin(t * 0.5)) * (1 + 0.05 * t)

    amp = ContradictionAmplifier(lam=lam)
    for t in range(steps):
        amp.amplify(complexity_fn(t), contradiction_fn(t))
    return amp.trajectory()
