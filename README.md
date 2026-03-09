# Quantum Math Lab

[![CI](https://github.com/blackboxprogramming/quantum-math-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/blackboxprogramming/quantum-math-lab/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Proprietary-9c27b0)](LICENSE)

Pure-Python quantum circuit simulator with a companion catalog of unsolved problems in mathematics.

## Simulator

The `QuantumCircuit` class implements a state-vector simulator that stores the full 2^n complex amplitude vector and applies gates as matrix operations. No external quantum framework required — just NumPy.

### Supported Gates

| Gate | Method | Matrix |
|------|--------|--------|
| Hadamard | `hadamard(q)` | (1/sqrt(2)) [[1,1],[1,-1]] |
| Pauli-X | `pauli_x(q)` | [[0,1],[1,0]] |
| CNOT | `cnot(c, t)` | 4x4 controlled-NOT |
| Custom | `apply_custom(U, qubits)` | Any unitary matrix |

### Quick Start

```bash
pip install numpy
```

```python
from quantum_simulator import QuantumCircuit
import numpy as np

# Create a Bell state: (|00> + |11>) / sqrt(2)
circuit = QuantumCircuit(2)
circuit.hadamard(0)
circuit.cnot(0, 1)

print(circuit.probabilities())
# {'00': 0.5, '01': 0.0, '10': 0.0, '11': 0.5}

result = circuit.measure(shots=1000, rng=np.random.default_rng(42))
print(result.counts)
# {'00': 494, '01': 0, '10': 0, '11': 506}
```

### 3-Qubit GHZ State

```python
circuit = QuantumCircuit(3)
circuit.hadamard(0)
circuit.cnot(0, 1)
circuit.cnot(0, 2)
# |000> + |111> with equal probability, all other states zero
```

### Custom Unitaries

```python
# Pauli-Z gate
Z = np.array([[1, 0], [0, -1]], dtype=complex)
circuit = QuantumCircuit(1)
circuit.apply_custom(Z, [0])

# SWAP gate
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)
circuit = QuantumCircuit(2)
circuit.apply_custom(SWAP, [0, 1])
```

## Architecture

```
QuantumCircuit(n)
  |
  |-- _state: np.ndarray[complex128]   # 2^n amplitude vector
  |-- hadamard(q) / pauli_x(q)         # Single-qubit gates
  |-- cnot(c, t)                        # Two-qubit gate
  |-- apply_custom(U, qubits)           # Arbitrary unitary
  |-- probabilities(qubits?)            # |amplitude|^2 distribution
  |-- measure(qubits?, shots, rng)      # Sample + collapse
       |
       +-- MeasurementResult
             |-- counts: {bitstring: int}
             |-- most_likely() -> str
             |-- total_shots() -> int
```

State is stored as a dense vector reshaped into a tensor for gate application via permutation and matrix multiplication. Measurement collapses the state vector by projecting onto the observed subspace and renormalizing.

## Unsolved Problems

[`problems.md`](problems.md) covers ten influential open problems:

1. Riemann Hypothesis
2. P vs NP
3. Navier-Stokes regularity
4. Hodge Conjecture
5. Yang-Mills mass gap
6. Birch and Swinnerton-Dyer
7. Goldbach's Conjecture
8. Twin Prime Conjecture
9. Collatz Conjecture
10. abc Conjecture

Each entry includes a problem statement, known progress, and references.

## Development

```bash
# Install
pip install -r requirements.txt

# Run tests (35+ tests)
make test

# Lint
make lint

# Coverage report
make coverage
```

## License

Proprietary — BlackRoad OS, Inc. See [LICENSE](LICENSE).
