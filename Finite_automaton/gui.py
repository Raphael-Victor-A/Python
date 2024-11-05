import tkinter as tk
from tkinter import filedialog, messagebox
from parser import load_automaton

class AutomatonSimulator:
    def __init__(self, root):
        self.automaton = None
        self.root = root

        # Criação dos elementos da interface
        self.load_button = tk.Button(root, text="Load Automaton", command=self.load_automaton)
        self.load_button.pack()

        self.input_label = tk.Label(root, text="Input string:")
        self.input_label.pack()

        self.input_entry = tk.Entry(root)
        self.input_entry.pack()

        self.simulate_button = tk.Button(root, text="Simulate", command=self.simulate)
        self.simulate_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def load_automaton(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.automaton = load_automaton(file_path)
            print(f"Autômato carregado: {self.automaton}")

    def simulate(self):
        input_string = self.input_entry.get()
        if self.automaton is None:
            messagebox.showerror("Erro", "Por favor, carregue um autômato antes de simular.")
            return

        if self.automaton.is_accepted(input_string):
            self.result_label.config(text="Accepted!")
        else:
            self.result_label.config(text="Rejected!")

if __name__ == "__main__":
    root = tk.Tk()
    gui = AutomatonSimulator(root)
    root.mainloop()
