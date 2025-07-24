# Quantum Math Lab

Quantum Math Lab is an educational project that combines a **simple quantum‑computing simulator** with an exploration of some of the most famous unsolved problems in mathematics.  The goal of this repository is two‑fold:

1. **Quantum Computing Simulation** – provide a minimal yet functional simulator for quantum circuits.  The code in `quantum_simulator.py` models a register of qubits using a complex state vector and implements a handful of basic gates (Hadamard, Pauli‑X and controlled‑NOT).  You can create circuits, apply gates and measure the qubits to observe the probabilistic outcomes associated with quantum mechanics.
2. **Unsolved Mathematical Problems** – collect descriptions of ten open problems that continue to challenge mathematicians.  These descriptions, along with references to authoritative sources, are provided in `problems.md`.  The list includes the seven Clay Mathematics Institute (CMI) Millennium Prize Problems and a few other long‑standing conjectures from number theory and analysis.

## Why this project?

Mathematics and quantum computing share a common theme: profound questions whose answers unlock entirely new possibilities.  While this project is purely **simulative** – nothing here can harness particles or energy in the physical world – it offers a platform for learning and experimentation.  The simulator illustrates key quantum concepts such as superposition and entanglement, and the problem summaries point readers toward some of the deepest unsolved questions in modern mathematics.

## Getting started

1. **Clone this repository** and install the only required dependency (NumPy) with `pip install numpy`.
2. **Explore `quantum_simulator.py`** – this module defines a `QuantumCircuit` class with methods to apply gates and perform measurements.  The included docstrings provide examples.
3. **Read `problems.md`** – each section describes an unsolved problem and cites a primary source or well‑known reference for further reading.

## Disclaimer

This project does not attempt to solve any of the unsolved problems listed here.  It provides succinct descriptions for educational purposes and a simple code base for playing with quantum circuits.  For real‑world quantum computation, consider using established frameworks such as [Qiskit](https://qiskit.org/) or [Cirq](https://quantumai.google/cirq).
