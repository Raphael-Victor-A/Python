import tkinter as tk
from tkinter import messagebox, filedialog
from kmp import kmp_search, compute_lps_array
from comparation import basic_search

def search_sequences():
    # Validar entrada de DNA e subsequência para conter apenas C, T, A, G
    valid_chars = {"C", "T", "A", "G"}
    if not set(dna_entry.get()).issubset(valid_chars) or not set(sub_entry.get()).issubset(valid_chars):
        messagebox.showerror("Erro de entrada", "As sequências devem conter apenas as letras C, T, A e G.")
        return
    
    dna_sequence = dna_entry.get()
    subsequence = sub_entry.get()

    basic_positions, basic_comparisons = basic_search(dna_sequence, subsequence)
    kmp_positions, kmp_comparisons = kmp_search(dna_sequence, subsequence)

    result_text = f"Basic Search:\nPositions: {basic_positions}\nComparisons: {basic_comparisons}\n\n"
    result_text += f"KMP Search:\nPositions: {kmp_positions}\nComparisons: {kmp_comparisons}\n"
    
    result_label.config(text=result_text)
    visualize_kmp(dna_sequence, subsequence)

def load_dna_from_file():
    # Função para carregar sequência de DNA de um arquivo
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                dna_sequence = file.read().strip()
                dna_entry.delete(0, tk.END)  # Limpa o campo de entrada
                dna_entry.insert(0, dna_sequence)  # Insere a sequência no campo de texto
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo: {e}")

def visualize_kmp(dna_sequence, subsequence):
    lps = compute_lps_array(subsequence)
    i = j = 0
    state_canvas.delete("all")
    
    while i < len(dna_sequence):
        draw_state(dna_sequence, subsequence, i, j)
        state_canvas.update()
        state_canvas.after(500)  # Pause for visualization
        
        if subsequence[j] == dna_sequence[i]:
            i += 1
            j += 1
        
        if j == len(subsequence):
            j = lps[j - 1]
        elif i < len(dna_sequence) and subsequence[j] != dna_sequence[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

def draw_state(dna_sequence, subsequence, i, j):
    state_canvas.delete("all")
    state_canvas.create_text(10, 10, anchor=tk.NW, text=f"DNA Sequence: {dna_sequence}", font=("Courier", 16))
    state_canvas.create_text(10, 40, anchor=tk.NW, text=f"Subsequence: {subsequence}", font=("Courier", 16))
    state_canvas.create_text(10, 70, anchor=tk.NW, text=f"Comparing index i: {i} (DNA) with index j: {j} (Subsequence)", font=("Courier", 14))

    dna_highlight = dna_sequence[:i] + "[" + dna_sequence[i:i+1] + "]" + dna_sequence[i+1:]
    sub_highlight = " " * j + "[" + subsequence[j:j+1] + "]" + subsequence[j+1:]
    
    state_canvas.create_text(10, 100, anchor=tk.NW, text=dna_highlight, font=("Courier", 16), fill="blue")
    state_canvas.create_text(10, 130, anchor=tk.NW, text=sub_highlight, font=("Courier", 16), fill="red")

root = tk.Tk()
root.title("DNA Sequence Search")

tk.Label(root, text="DNA Sequence:").grid(row=0, column=0, padx=10, pady=10)
dna_entry = tk.Entry(root, width=50)
dna_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Subsequence:").grid(row=1, column=0, padx=10, pady=10)
sub_entry = tk.Entry(root, width=50)
sub_entry.grid(row=1, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search", command=search_sequences)
search_button.grid(row=2, column=0, columnspan=2, pady=20)

load_button = tk.Button(root, text="Load DNA from File", command=load_dna_from_file)
load_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

state_canvas = tk.Canvas(root, width=800, height=200, bg="white")
state_canvas.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
