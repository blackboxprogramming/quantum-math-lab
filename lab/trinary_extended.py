"""
BlackRoad Trinary Logic System — Extended Operations
Truth states: 1=True, 0=Unknown/Neutral, -1=False

Used in the PS-SHA∞ memory chain for epistemic reasoning.
Implements full Łukasiewicz three-valued logic.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# Truth values
TRUE = 1
UNKNOWN = 0
FALSE = -1

TruthValue = int  # one of {1, 0, -1}


def t_not(a: TruthValue) -> TruthValue:
    """Łukasiewicz negation: NOT a = -a"""
    return -a


def t_and(a: TruthValue, b: TruthValue) -> TruthValue:
    """Łukasiewicz conjunction: min(a, b)"""
    return min(a, b)


def t_or(a: TruthValue, b: TruthValue) -> TruthValue:
    """Łukasiewicz disjunction: max(a, b)"""
    return max(a, b)


def t_implies(a: TruthValue, b: TruthValue) -> TruthValue:
    """Łukasiewicz implication: min(1, 1 - a + b)"""
    raw = 1 - a + b
    return max(FALSE, min(TRUE, raw))


def t_equiv(a: TruthValue, b: TruthValue) -> TruthValue:
    """Equivalence: a ↔ b = (a → b) ∧ (b → a)"""
    return t_and(t_implies(a, b), t_implies(b, a))


def t_xor(a: TruthValue, b: TruthValue) -> TruthValue:
    """Exclusive or in trinary: differs from equivalence"""
    return t_not(t_equiv(a, b))


@dataclass
class TrinaryProposition:
    """A proposition with a truth state and confidence."""
    statement: str
    truth: TruthValue = UNKNOWN
    confidence: float = 0.5  # 0.0 – 1.0
    evidence: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return {TRUE: "TRUE", UNKNOWN: "UNKNOWN", FALSE: "FALSE"}[self.truth]

    def assert_true(self, confidence: float = 1.0, evidence: str = "") -> None:
        self.truth = TRUE
        self.confidence = confidence
        if evidence:
            self.evidence.append(evidence)

    def assert_false(self, confidence: float = 1.0, evidence: str = "") -> None:
        self.truth = FALSE
        self.confidence = confidence
        if evidence:
            self.evidence.append(evidence)

    def contradict(self, claim: str) -> None:
        """Mark this proposition as having a contradiction."""
        self.contradictions.append(claim)
        if self.truth != UNKNOWN:
            # Downgrade certainty when contradiction is detected
            self.confidence = max(0.0, self.confidence - 0.3)

    def quarantine(self) -> None:
        """Quarantine: set truth to UNKNOWN, flag for review."""
        self.truth = UNKNOWN
        self.confidence = 0.0

    def __repr__(self) -> str:
        return f"TrinaryProposition({self.statement!r}, {self.label}, conf={self.confidence:.2f})"


class TrinaryReasoner:
    """
    Paraconsistent reasoner using trinary logic.
    Preserves contradictions rather than resolving them.
    Implements the BlackRoad Z-framework: Z≠∅ means
    'contradictions are data, not errors.'
    """

    def __init__(self) -> None:
        self._props: dict[str, TrinaryProposition] = {}

    def assert_true(self, statement: str, confidence: float = 1.0, evidence: str = "") -> TrinaryProposition:
        prop = self._get_or_create(statement)
        if prop.truth == FALSE:
            prop.contradict(f"Previously FALSE, now asserted TRUE (conf={confidence})")
        prop.assert_true(confidence, evidence)
        return prop

    def assert_false(self, statement: str, confidence: float = 1.0, evidence: str = "") -> TrinaryProposition:
        prop = self._get_or_create(statement)
        if prop.truth == TRUE:
            prop.contradict(f"Previously TRUE, now asserted FALSE (conf={confidence})")
        prop.assert_false(confidence, evidence)
        return prop

    def query(self, statement: str) -> TrinaryProposition:
        return self._props.get(statement, TrinaryProposition(statement))

    def contradictions(self) -> list[TrinaryProposition]:
        return [p for p in self._props.values() if p.contradictions]

    def quarantine_contradicted(self) -> list[str]:
        """Quarantine all props with contradictions, return their statements."""
        quarantined = []
        for prop in self._props.values():
            if prop.contradictions:
                prop.quarantine()
                quarantined.append(prop.statement)
        return quarantined

    def evaluate(self, a_stmt: str, op: str, b_stmt: Optional[str] = None) -> TruthValue:
        """Evaluate a logical expression over known propositions."""
        a = self._props.get(a_stmt, TrinaryProposition(a_stmt)).truth
        ops = {
            "NOT": lambda: t_not(a),
            "AND": lambda: t_and(a, self._props.get(b_stmt or "", TrinaryProposition("")).truth),
            "OR":  lambda: t_or(a, self._props.get(b_stmt or "", TrinaryProposition("")).truth),
            "IMPLIES": lambda: t_implies(a, self._props.get(b_stmt or "", TrinaryProposition("")).truth),
        }
        if op not in ops:
            raise ValueError(f"Unknown op: {op}. Use: {list(ops)}")
        return ops[op]()

    def _get_or_create(self, statement: str) -> TrinaryProposition:
        if statement not in self._props:
            self._props[statement] = TrinaryProposition(statement)
        return self._props[statement]

    def summary(self) -> dict:
        counts = {1: 0, 0: 0, -1: 0}
        for p in self._props.values():
            counts[p.truth] += 1
        return {
            "total": len(self._props),
            "true": counts[TRUE],
            "unknown": counts[UNKNOWN],
            "false": counts[FALSE],
            "contradictions": len(self.contradictions()),
        }
