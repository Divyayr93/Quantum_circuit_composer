# Quantum Circuit Composer & Simulator

An interactive, modular desktop application built with Python and `tkinter` to visually compose quantum circuits and simulate state vectors in real-time.

---

## 📂 File Architecture

The codebase is split into decoupled, dedicated modules to make maintainability, testing, and expansion simple:

```text
├── gates.py           # Single source of truth for gate matrices and UI styles.
├── simulator.py       # Math backend; manages state vectors and Kronecker operations.
├── gui_components.py  # Visual presentation layouts (Sidebar and Grid Timeline frames).
└── main.py            # Main application controller orchestration & user lifecycle entry point.
```

---

## ⚡ Setup & Execution

### Prerequisites
Make sure you have `numpy` installed in your current Python environment:
```bash
pip install numpy
```

### Running the Application
Launch the editor by running the main entry point:
```bash
python main.py
```

---

## 🧩 User Guide

1. **Configuration**: On startup, modals will prompt you for your desired number of Qubit Wires (Rows) and Timeline Steps (Columns). The UI scales its window dimensions automatically to accommodate large grids.
2. **Placing Gates**: Click a gate button in the left **Operations** sidebar (e.g., `X`, `H`), then click on a wire channel intersection within the canvas area to drop the element into place.
3. **Execution**: Click **▶ Run Circuit** in the top right menu bar. A window will display non-zero computational basis states (\(\vert{}\psi\rangle\)), amplitudes, and their measurement probabilities.

---

## 🛠 Extension Manual: Adding New Gates

Because the project is fully modular, adding new gates does not require changing any UI rendering code. Here is how to add them:

### Example 1: Adding a Single-Qubit Identity or Phase Gate
To add a Phase Gate (\(S\)), modify only **`gates.py`**:

1. Open `gates.py` and register the matrix inside `GATES_1Q`:
   ```python
   GATES_1Q = {
       # ... existing gates ...
       'S': np.array([[1, 0], [0, 1j]], dtype=np.complex128)
   }
   ```
2. Add a custom display style block in `GATE_STYLES`:
   ```python
   GATE_STYLES = {
       # ... existing styles ...
       'S': {'bg': '#9c27b0', 'fg': '#ffffff'}
   }
   ```
3. To display the button in the UI toolbar, append your label tracking key to the layout coordinate mapping matrix array inside `gui_components.py` (`SidebarComponent.setup_ui` configuration list):
   ```python
   coords = [('H', 0, 0), ('X', 0, 1), ('Y', 1, 0), ('Z', 1, 1), ('S', 2, 0)]
   ```

### Example 2: Hooking Up Multi-Qubit Operators (e.g., CNOT / CX)
When upgrading the application to support 2-qubit operations:

1. Add your standard multi-qubit 4x4 array structure under a specialized category matrix dictionary inside `gates.py`.
2. Update `simulator.py` inside `run_circuit`:
   ```python
   def run_circuit(self, circuit_steps):
       # ... loop initialization ...
       for gate, target in circuit_steps:
           if gate in GATES_1Q:
               self.apply_single_qubit_gate(gate, target)
           elif gate == 'CX':
               # Implement custom CNOT multi-qubit mapping logic here
               pass
   ```
3. Update `gui_components.py` to capture dual clicks or configure control/target registers dynamically when a multi-qubit button operation flag is active.