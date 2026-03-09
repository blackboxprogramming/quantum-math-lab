"""Comprehensive test suite for the quantum circuit simulator.

Tests cover single-qubit gates, multi-qubit entanglement, measurement
statistics, custom unitaries, error handling, and edge cases.
"""

import numpy as np
import pytest

from quantum_simulator import MeasurementResult, QuantumCircuit


# ── Single-qubit gates ──────────────────────────────────────────────────────

class TestHadamard:
    def test_creates_equal_superposition(self):
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        probs = circuit.probabilities()
        assert probs["0"] == pytest.approx(0.5, abs=1e-8)
        assert probs["1"] == pytest.approx(0.5, abs=1e-8)

    def test_double_hadamard_returns_to_ground(self):
        """H*H = I: applying Hadamard twice should return to |0>."""
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        circuit.hadamard(0)
        probs = circuit.probabilities()
        assert probs["0"] == pytest.approx(1.0, abs=1e-8)
        assert probs["1"] == pytest.approx(0.0, abs=1e-8)

    def test_hadamard_on_second_qubit(self):
        circuit = QuantumCircuit(2)
        circuit.hadamard(1)
        probs = circuit.probabilities()
        assert probs["00"] == pytest.approx(0.5, abs=1e-8)
        assert probs["01"] == pytest.approx(0.5, abs=1e-8)
        assert probs["10"] == pytest.approx(0.0, abs=1e-8)
        assert probs["11"] == pytest.approx(0.0, abs=1e-8)


class TestPauliX:
    def test_flips_ground_state(self):
        circuit = QuantumCircuit(1)
        circuit.pauli_x(0)
        probs = circuit.probabilities()
        assert probs["1"] == pytest.approx(1.0)
        assert probs["0"] == pytest.approx(0.0)

    def test_double_x_returns_to_ground(self):
        """X*X = I: flipping twice returns to |0>."""
        circuit = QuantumCircuit(1)
        circuit.pauli_x(0)
        circuit.pauli_x(0)
        probs = circuit.probabilities()
        assert probs["0"] == pytest.approx(1.0)

    def test_x_on_specific_qubit(self):
        circuit = QuantumCircuit(3)
        circuit.pauli_x(1)
        probs = circuit.probabilities()
        assert probs["010"] == pytest.approx(1.0)


# ── Two-qubit gates (CNOT) ─────────────────────────────────────────────────

class TestCNOT:
    def test_creates_bell_state(self):
        circuit = QuantumCircuit(2)
        circuit.hadamard(0)
        circuit.cnot(0, 1)
        probs = circuit.probabilities()
        assert probs["00"] == pytest.approx(0.5, abs=1e-8)
        assert probs["11"] == pytest.approx(0.5, abs=1e-8)
        assert probs["01"] == pytest.approx(0.0, abs=1e-8)
        assert probs["10"] == pytest.approx(0.0, abs=1e-8)

    def test_cnot_with_control_zero(self):
        """CNOT does nothing when control qubit is |0>."""
        circuit = QuantumCircuit(2)
        circuit.cnot(0, 1)
        probs = circuit.probabilities()
        assert probs["00"] == pytest.approx(1.0)

    def test_cnot_with_control_one(self):
        """CNOT flips target when control qubit is |1>."""
        circuit = QuantumCircuit(2)
        circuit.pauli_x(0)
        circuit.cnot(0, 1)
        probs = circuit.probabilities()
        assert probs["11"] == pytest.approx(1.0)

    def test_cnot_same_qubit_raises(self):
        circuit = QuantumCircuit(2)
        with pytest.raises(ValueError, match="different"):
            circuit.cnot(0, 0)

    def test_three_qubit_ghz_state(self):
        """Create a 3-qubit GHZ state: (|000> + |111>) / sqrt(2)."""
        circuit = QuantumCircuit(3)
        circuit.hadamard(0)
        circuit.cnot(0, 1)
        circuit.cnot(0, 2)
        probs = circuit.probabilities()
        assert probs["000"] == pytest.approx(0.5, abs=1e-8)
        assert probs["111"] == pytest.approx(0.5, abs=1e-8)
        for key in ["001", "010", "011", "100", "101", "110"]:
            assert probs[key] == pytest.approx(0.0, abs=1e-8)


# ── Custom unitaries ───────────────────────────────────────────────────────

class TestCustomUnitary:
    def test_pauli_z_gate(self):
        """Z gate: |0> -> |0>, |1> -> -|1>. Probabilities unchanged."""
        Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        circuit.apply_custom(Z, [0])
        # H then Z on |0> gives (|0> - |1>)/sqrt(2) — same probabilities
        probs = circuit.probabilities()
        assert probs["0"] == pytest.approx(0.5, abs=1e-8)
        assert probs["1"] == pytest.approx(0.5, abs=1e-8)

    def test_pauli_z_then_hadamard(self):
        """H*Z*H|0> = X|0> = |1>."""
        Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        circuit.apply_custom(Z, [0])
        circuit.hadamard(0)
        probs = circuit.probabilities()
        assert probs["1"] == pytest.approx(1.0, abs=1e-8)

    def test_identity_gate(self):
        I = np.eye(2, dtype=np.complex128)
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        circuit.apply_custom(I, [0])
        probs = circuit.probabilities()
        assert probs["0"] == pytest.approx(0.5, abs=1e-8)

    def test_swap_gate(self):
        """SWAP gate exchanges two qubits."""
        SWAP = np.array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ], dtype=np.complex128)
        circuit = QuantumCircuit(2)
        circuit.pauli_x(0)  # |10>
        circuit.apply_custom(SWAP, [0, 1])
        probs = circuit.probabilities()
        assert probs["01"] == pytest.approx(1.0)

    def test_wrong_dimension_raises(self):
        circuit = QuantumCircuit(1)
        with pytest.raises(ValueError, match="dimension"):
            circuit.apply_custom(np.eye(4), [0])


# ── Measurement ─────────────────────────────────────────────────────────────

class TestMeasurement:
    def test_partial_measurement_collapses_state(self):
        rng = np.random.default_rng(seed=7)
        circuit = QuantumCircuit(2)
        circuit.hadamard(0)
        circuit.cnot(0, 1)
        result = circuit.measure(qubits=[0], shots=1, rng=rng)
        assert result.total_shots() == 1

        probs = circuit.probabilities()
        if result.counts.get("0", 0) == 1:
            assert probs["00"] == pytest.approx(1.0)
        else:
            assert probs["11"] == pytest.approx(1.0)

    def test_measurement_statistics(self):
        """Many shots of a fair superposition should be ~50/50."""
        rng = np.random.default_rng(seed=42)
        circuit = QuantumCircuit(1)
        circuit.hadamard(0)
        result = circuit.measure(shots=1000, rng=rng)
        zero_frac = result.counts.get("0", 0) / 1000
        assert zero_frac == pytest.approx(0.5, abs=0.06)

    def test_deterministic_measurement(self):
        """Measuring |0> always gives 0."""
        circuit = QuantumCircuit(1)
        result = circuit.measure(shots=100, rng=np.random.default_rng(0))
        assert result.counts.get("0", 0) == 100

    def test_measurement_result_most_likely(self):
        result = MeasurementResult(counts={"00": 10, "01": 5, "10": 3, "11": 82})
        assert result.most_likely() == "11"
        assert result.total_shots() == 100

    def test_zero_shots_raises(self):
        circuit = QuantumCircuit(1)
        with pytest.raises(ValueError, match="positive"):
            circuit.measure(shots=0)


# ── Error handling ──────────────────────────────────────────────────────────

class TestErrorHandling:
    def test_zero_qubits_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            QuantumCircuit(0)

    def test_negative_qubits_raises(self):
        with pytest.raises(ValueError):
            QuantumCircuit(-1)

    def test_qubit_index_out_of_range(self):
        circuit = QuantumCircuit(2)
        with pytest.raises(IndexError):
            circuit.hadamard(5)

    def test_duplicate_qubits_in_custom(self):
        circuit = QuantumCircuit(2)
        with pytest.raises(ValueError, match="distinct"):
            circuit.apply_custom(np.eye(4), [0, 0])


# ── Probabilities sum to 1 ─────────────────────────────────────────────────

class TestProbabilityNormalization:
    def test_initial_state_normalized(self):
        circuit = QuantumCircuit(3)
        probs = circuit.probabilities()
        assert sum(probs.values()) == pytest.approx(1.0)

    def test_after_gates_normalized(self):
        circuit = QuantumCircuit(3)
        circuit.hadamard(0)
        circuit.hadamard(1)
        circuit.cnot(0, 2)
        probs = circuit.probabilities()
        assert sum(probs.values()) == pytest.approx(1.0)

    def test_partial_probabilities_normalized(self):
        circuit = QuantumCircuit(3)
        circuit.hadamard(0)
        circuit.hadamard(1)
        probs = circuit.probabilities(qubits=[0])
        assert sum(probs.values()) == pytest.approx(1.0)
