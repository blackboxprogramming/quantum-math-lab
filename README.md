# Quantum Framework

**Circuits, not slides. Real quantum computing.**

A state-vector quantum circuit simulator with implementations of fundamental quantum algorithms, unsolved math problem compendium, and experimental emergence research. Built in Python with NumPy.

## Features

- **State-Vector Simulator** — Dense complex NumPy arrays. Hadamard, Pauli-X/Y/Z, CNOT gates, custom unitaries, measurement with collapse.
- **Bell States** — Create and measure entangled qubit pairs.
- **Probability Distributions** — Inspect full probability distributions for any subset of qubits at any point.
- **Measurement** — Projective measurement with state collapse, configurable RNG for reproducibility.
- **Problem Compendium** — 10 landmark unsolved problems: Riemann Hypothesis, P vs NP, Navier-Stokes, and more.
- **Emergence Research** — Experimental trinary and emergence simulations in the lab.
- **Automated Tests** — Full pytest suite verifying simulator behavior.

## Quickstart

```bash
git clone https://github.com/blackboxprogramming/quantum-math-lab.git
cd quantum-math-lab
pip install -r requirements.txt

# Run the simulator
python -c "
from quantum_simulator import QuantumCircuit
import numpy as np

# Create a Bell state
qc = QuantumCircuit(2)
qc.hadamard(0)
qc.cnot(0, 1)
print(qc.measure(rng=np.random.default_rng(42)))
"

# Run tests
pytest tests/
```

## Simulator API

```python
from quantum_simulator import QuantumCircuit
import numpy as np

qc = QuantumCircuit(3)       # 3-qubit register

# Gates
qc.hadamard(0)               # Hadamard on qubit 0
qc.pauli_x(1)                # Pauli-X (NOT) on qubit 1
qc.pauli_y(2)                # Pauli-Y on qubit 2
qc.pauli_z(0)                # Pauli-Z on qubit 0
qc.cnot(0, 1)                # CNOT: control=0, target=1

# Inspect
probs = qc.probabilities()   # Full probability distribution
result = qc.measure()         # Measure with collapse
```

## Project Structure

```
quantum-math-lab/
├── quantum_simulator.py     # Core simulator: QuantumCircuit class
├── problems.md              # 10 unsolved math problems
├── requirements.txt         # numpy, pytest
├── lab/
│   ├── emergence.py         # Emergence simulation experiments
│   └── trinary_extended.py  # Trinary computing extensions
└── tests/
    ├── conftest.py
    └── test_quantum_simulator.py
```

## Unsolved Problems Covered

1. Riemann Hypothesis
2. P vs NP
3. Navier-Stokes Regularity
4. Birch and Swinnerton-Dyer Conjecture
5. Hodge Conjecture
6. Yang-Mills Existence and Mass Gap
7. Goldbach's Conjecture
8. Twin Prime Conjecture
9. Collatz Conjecture
10. ABC Conjecture

## Related Projects

- **[Simulation Theory](https://github.com/blackboxprogramming/simulation-theory)** — SHA-256 hash chains and computational reality
- **[Native AI Quantum Energy](https://github.com/blackboxprogramming/native-ai-quantum-energy)** — AI quantum computing and energy simulation
- **[BlackRoad OS](https://github.com/blackboxprogramming/BlackRoad-Operating-System)** — The operating system for governed AI

## Live Tools

- **[circuits.blackroad.io](https://circuits.blackroad.io)** — Visual circuit designer
- **[simulator.blackroad.io](https://simulator.blackroad.io)** — Browser-based quantum simulator

## License

Copyright 2026 BlackRoad OS, Inc. — Alexa Amundson. All rights reserved.
