# Quantum Math Lab

Quantum Math Lab pairs a lightweight quantum circuit simulator with concise
summaries of landmark unsolved problems in mathematics.  The project is designed
for experimentation and self-study: you can build and inspect quantum states in
pure Python while browsing short descriptions of famous conjectures.

## Features

- **State-vector simulator** implemented in [`quantum_simulator.py`](quantum_simulator.py)
  with Hadamard, Pauli-X and controlled-NOT gates, custom unitaries and
  measurement utilities.
- **Problem compendium** in [`problems.md`](problems.md) covering ten influential
  open problems such as the Riemann Hypothesis, P vs NP and the Navier–Stokes
  regularity question.
- **Automated tests** demonstrating the simulator’s behaviour, built with
  `pytest`.

## Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # see below if the file is absent
   ```

   If a `requirements.txt` file is not present, simply install NumPy and pytest:

   ```bash
   pip install numpy pytest
   ```

2. **Experiment with the simulator**

   ```python
   from quantum_simulator import QuantumCircuit

   circuit = QuantumCircuit(2)
   circuit.hadamard(0)
   circuit.cnot(0, 1)
   print(circuit.probabilities())  # {'00': 0.5, '11': 0.5}
   result = circuit.measure(rng=np.random.default_rng())
   print(result.counts)
   ```

3. **Review the unsolved problems** by opening [`problems.md`](problems.md) for
   high-level summaries and references.

## Running the tests

Use `pytest` to execute the simulator tests:

```bash
pytest
```

The test suite verifies single-qubit gates, entanglement via the controlled-NOT
operation and measurement statistics.

## Disclaimer

This project does not attempt to solve the problems listed in `problems.md` and
is not a substitute for full-featured quantum computing frameworks such as
[Qiskit](https://qiskit.org/) or [Cirq](https://quantumai.google/cirq).  It is an
educational sandbox for experimenting with qubit states and learning about open
questions in mathematics.
