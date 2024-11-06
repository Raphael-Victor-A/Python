# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from nucleo import CFGGenerator
import json

class TextGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Texto CFG - Português")
        self.root.geometry("600x500")

        # Configurações iniciais de gramática padrão
        self.grammar = {
            "S": ["NP VP", "S S", "VP NP"],
            "NP": ["Det N", "N"],
            "VP": ["V NP", "V"],
            "Det": ["o", "a", "os", "as", "um", "uma", "uns", "umas"],
            "N": ["homem", "mulher", "crianca", "cachorro", "gato", "cidade", "livro"],
            "V": ["corre", "come", "fala", "le", "pula"],
            "Extras": ["com", "para", "e", "mas", "ou"]
        }
        
        self.generator = CFGGenerator(self.grammar)
        
        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Botão para carregar gramática de um arquivo
        self.load_button = tk.Button(self.root, text="Carregar Gramática de Arquivo", command=self.load_grammar_from_file)
        self.load_button.pack()

        # Campo de entrada para a gramática em formato JSON
        self.grammar_label = tk.Label(self.root, text="Insira a gramática (JSON):")
        self.grammar_label.pack()

        self.grammar_entry = tk.Text(self.root, height=8, width=50)
        self.grammar_entry.insert(tk.END, json.dumps(self.grammar, indent=4))
        self.grammar_entry.pack()

        # Botão para atualizar a gramática
        self.update_button = tk.Button(self.root, text="Atualizar Gramática", command=self.update_grammar)
        self.update_button.pack()

        # Botão para gerar texto
        self.generate_button = tk.Button(self.root, text="Gerar Texto", command=self.generate_text)
        self.generate_button.pack()

        # Campo de saída para o texto gerado
        self.output_label = tk.Label(self.root, text="Texto Gerado:")
        self.output_label.pack()

        self.output_text = tk.Text(self.root, height=10, width=50, wrap="word")
        self.output_text.pack()

    def load_grammar_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                try:
                    grammar = json.load(f)
                    self.generator.set_grammar(grammar)
                    self.grammar_entry.delete("1.0", tk.END)
                    self.grammar_entry.insert(tk.END, json.dumps(grammar, indent=4))
                    messagebox.showinfo("Sucesso", "Gramática carregada com sucesso!")
                except json.JSONDecodeError:
                    messagebox.showerror("Erro", "Formato inválido. Por favor, carregue um arquivo JSON válido.")

    def update_grammar(self):
        try:
            new_grammar = json.loads(self.grammar_entry.get("1.0", tk.END))
            self.generator.set_grammar(new_grammar)
            messagebox.showinfo("Sucesso", "Gramática atualizada com sucesso!")
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Gramática inválida. Por favor, insira um JSON válido.")

    def generate_text(self):
        text = self.generator.generate()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
    
    def generate_text(self):
    # Usa a nova função para gerar múltiplas frases concatenadas
        text = self.generator.generate_infinite_text(symbol='S', sentence_count=10, max_depth=10)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextGeneratorApp(root)
    root.mainloop()
