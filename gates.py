import numpy as np

# Single-qubit base gates
GATES_1Q = {
    'X': np.array([[0, 1], [1, 0]], dtype=np.complex128),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
    'Z': np.array([[1, 0], [0, -1]], dtype=np.complex128),
    'H': (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)
}

# Color mapping rules for rendering the UI
GATE_STYLES = {
    'H': {'bg': '#ff4d4d', 'fg': '#ffffff'},
    'X': {'bg': '#801a24', 'fg': '#ffffff'},
    'Y': {'bg': '#801a24', 'fg': '#ffffff'},
    'Z': {'bg': '#0080ff', 'fg': '#ffffff'},
    'CX': {'bg': '#107c41', 'fg': '#ffffff'} # Placeholder layout for future 2-qubit expansion
}