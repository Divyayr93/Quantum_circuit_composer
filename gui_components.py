import tkinter as tk
from gates import GATE_STYLES

class SidebarComponent(tk.Frame):
    def __init__(self, parent, on_gate_select_callback):
        super().__init__(parent, bg="#f5f5f5", width=220, bd=1, relief=tk.SOLID)
        self.pack_propagate(False)
        self.on_select = on_gate_select_callback
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Operations", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(anchor=tk.W, padx=20, pady=(20, 15))
        grid_frame = tk.Frame(self, bg="#f5f5f5")
        grid_frame.pack(anchor=tk.W, padx=20)
        
        coords = [('H', 0, 0), ('X', 0, 1), ('Y', 1, 0), ('Z', 1, 1)]
        for gate, row, col in coords:
            style = GATE_STYLES.get(gate, {'bg': '#b5b5b5', 'fg': '#ffffff'})
            btn = tk.Button(
                grid_frame, text=gate, font=("Arial", 14, "bold"),
                bg=style['bg'], fg=style['fg'], activebackground=style['bg'], activeforeground=style['fg'],
                width=4, height=2, bd=0, cursor="hand2",
                command=lambda g=gate: self.on_select(g)
            )
            btn.grid(row=row, column=col, padx=6, pady=6)
            self.buttons[gate] = btn
            
        self.status_lbl = tk.Label(self, text="Select a gate.", font=("Arial", 10, "italic"), bg="#f5f5f5", fg="#777777", wraplength=180, justify=tk.LEFT)
        self.status_lbl.pack(anchor=tk.W, padx=20, pady=30)

    def highlight_button(self, selected_gate: str):
        for g, btn in self.buttons.items():
            btn.config(relief=tk.SUNKEN if g == selected_gate else tk.FLAT, bd=2 if g == selected_gate else 0)


class TimelineComponent(tk.Canvas):
    def __init__(self, parent, num_qubits, max_columns, on_click_callback):
        super().__init__(parent, bg="#ffffff", bd=0, highlightthickness=0)
        self.num_qubits = num_qubits
        self.max_columns = max_columns
        self.on_click_callback = on_click_callback
        self.wire_y_coords = {}
        self.start_x = 80
        self.slot_width = 50
        self.spacing_y = 60
        self.start_y = 50
        
        self.bind("<Button-1>", self.on_click_callback)

    def render(self, placed_gates):
        self.delete("all")
        line_length = self.max_columns * self.slot_width
        
        # Draw wires
        for i in range(self.num_qubits):
            y = self.start_y + (i * self.spacing_y)
            self.wire_y_coords[i] = y
            self.create_text(self.start_x - 30, y, text=f"q[{i}]", font=("Arial", 11), fill="#333333", anchor=tk.W)
            self.create_line(self.start_x, y, self.start_x + line_length, y, fill="#cccccc", width=1.5)
            
        # Draw Classical Register
        c_y = self.start_y + (self.num_qubits * self.spacing_y) + 20
        self.create_text(self.start_x - 30, c_y, text=f"c{self.num_qubits}", font=("Arial", 11), fill="#333333", anchor=tk.W)
        self.create_line(self.start_x, c_y - 2, start_x + line_length if 'start_x' in locals() else self.start_x + line_length, c_y - 2, fill="#b5b5b5", width=1.5)
        self.create_line(self.start_x, c_y + 2, start_x + line_length if 'start_x' in locals() else self.start_x + line_length, c_y + 2, fill="#b5b5b5", width=1.5)
        
        # Draw placed gates
        box_size = 36
        for item in placed_gates:
            qubit, col, gate = item["qubit"], item["col"], item["gate"]
            cx = self.start_x + 25 + (col * self.slot_width)
            cy = self.wire_y_coords[qubit]
            style = GATE_STYLES.get(gate, {'bg': '#b5b5b5', 'fg': '#ffffff'})
            
            self.create_rectangle(cx - box_size/2, cy - box_size/2, cx + box_size/2, cy + box_size/2, fill=style['bg'], outline="")
            self.create_text(cx, cy, text=gate, font=("Arial", 11, "bold"), fill=style['fg'])