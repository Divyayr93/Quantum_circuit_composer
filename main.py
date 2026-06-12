import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np

from simulator import QuantumSimulator
from gui_components import SidebarComponent, TimelineComponent

class QuantumComposerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Quantum Circuit Composer")
        self.root.configure(bg="#ffffff")
        
        # Initialization inputs
        self.num_qubits = self.ask_user_input("Circuit Rows", "Enter number of qubits (1-16):", 4, 1, 16)
        self.max_columns = self.ask_user_input("Circuit Columns", "Enter timeline steps (4-30):", 10, 4, 30)
        
        window_width = max(600, 320 + (self.max_columns * 52))
        window_height = max(450, 180 + (self.num_qubits * 60))
        self.root.geometry(f"{window_width}x{window_height}")
        
        self.selected_gate = None
        self.placed_gates = []
        
        self.setup_menu()
        self.setup_layout()

    def ask_user_input(self, title, prompt, default, min_v, max_v):
        val = simpledialog.askinteger(title, prompt, initialvalue=default, minvalue=min_v, maxvalue=max_v, parent=self.root)
        return val if val is not None else default

    def setup_menu(self):
        menu_frame = tk.Frame(self.root, bg="#ffffff", height=40)
        menu_frame.pack(fill=tk.X, side=tk.TOP, padx=15, pady=5)
        
        tk.Label(menu_frame, text="Dynamic Circuit | File Edit View Help", font=("Arial", 11), bg="#ffffff", fg="#333333").pack(side=tk.LEFT)
        
        tk.Button(
            menu_frame, text="▶ Run Circuit", font=("Arial", 10, "bold"),
            bg="#0066ff", fg="#ffffff", bd=0, padx=15, pady=5, cursor="hand2",
            command=self.run_simulation
        ).pack(side=tk.RIGHT)

    def setup_layout(self):
        main_container = tk.Frame(self.root, bg="#ffffff")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Mount modular UI components
        self.sidebar = SidebarComponent(main_container, self.handle_gate_selection)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        canvas_container = tk.Frame(main_container, bg="#ffffff")
        canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.timeline = TimelineComponent(canvas_container, self.num_qubits, self.max_columns, self.handle_timeline_click)
        self.timeline.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.timeline.render(self.placed_gates)

    def handle_gate_selection(self, gate: str):
        self.selected_gate = gate
        self.sidebar.status_lbl.config(text=f"Gate {gate} selected. Click on a wire to place it.")
        self.sidebar.highlight_button(gate)

    def handle_timeline_click(self, event):
        if not self.selected_gate:
            return
            
        clicked_qubit = None
        for qubit, y in self.timeline.wire_y_coords.items():
            if abs(event.y - y) <= 20:
                clicked_qubit = qubit
                break
                
        if clicked_qubit is not None and event.x >= self.timeline.start_x:
            col = int((event.x - self.timeline.start_x) // self.timeline.slot_width)
            if 0 <= col < self.max_columns:
                # Remove any gate currently blocking the slot
                self.placed_gates = [g for g in self.placed_gates if not (g["qubit"] == clicked_qubit and g["col"] == col)]
                
                self.placed_gates.append({"gate": self.selected_gate, "qubit": clicked_qubit, "col": col})
                self.placed_gates.sort(key=lambda x: (x["col"], x["qubit"]))
                
                self.timeline.render(self.placed_gates)
                self.sidebar.status_lbl.config(text="Gate placed. Select another gate.")
                self.selected_gate = None
                self.sidebar.highlight_button(None)

    def run_simulation(self):
        if not self.placed_gates:
            messagebox.showinfo("Circuit Empty", "Please place gates on the timeline first.")
            return
            
        execution_steps = [(item["gate"], item["qubit"]) for item in self.placed_gates]
        
        sim = QuantumSimulator(num_qubits=self.num_qubits)
        final_state = sim.run_circuit(execution_steps)
        
        result_str = f"Simulation complete ({self.num_qubits} Qubits)!\n\nNon-zero Amplitudes:\n"
        for idx, amp in enumerate(final_state):
            if np.abs(amp) > 1e-6:
                bin_str = format(idx, f'0{self.num_qubits}b')
                result_str += f"|{bin_str}⟩: {amp.real:+.4f} {amp.imag:+.4f}j  (Prob: {np.abs(amp)**2:.2%})\n"
                
        messagebox.showinfo("Execution Outputs", result_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumComposerApp(root)
    root.mainloop()
