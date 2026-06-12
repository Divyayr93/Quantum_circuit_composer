import numpy as np
from typing import List, Tuple
from gates import GATES_1Q

class QuantumSimulator:
    def __init__(self, num_qubits: int):
        if (num_qubits < 1) or (num_qubits > 24):
            raise ValueError("Number of qubits must be between 1 and 24.")
        self.num_qubits = num_qubits
        self.dim = 2**num_qubits
        self.state_vector = np.zeros(self.dim, dtype=np.complex128)
        self.state_vector[0] = 1.0 + 0.0j

    def apply_single_qubit_gate(self, gate_name: str, target: int):
        gate_mat = GATES_1Q[gate_name.upper()]
        iden = np.eye(2, dtype=np.complex128)
        
        if target == 0:
            full_mat = gate_mat
        else:
            full_mat = iden
            
        for q in range(1, self.num_qubits):
            if q == target:
                full_mat = np.kron(full_mat, gate_mat)
            else:
                full_mat = np.kron(full_mat, iden)
                
        self.state_vector = np.dot(full_mat, self.state_vector)

    def run_circuit(self, circuit_steps: List[Tuple[str, int]]):
        self.state_vector = np.zeros(self.dim, dtype=np.complex128)
        self.state_vector[0] = 1.0 + 0.0j
        
        for gate, target in circuit_steps:
            # Expand this condition block when adding 2-qubit operations
            if gate in GATES_1Q:
                self.apply_single_qubit_gate(gate, target)
        return self.state_vector