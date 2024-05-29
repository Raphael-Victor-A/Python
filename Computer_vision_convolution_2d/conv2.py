import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def criar_interface():
    global imagem, imagem_tk, canvas_original, canvas_convolucao, imagem_original
    janela = tk.Tk()
    janela.title("Núcleo de Convolução")
    janela.geometry("1200x500")
    janela.configure(bg='#f0f0f0')

    canvas_original = tk.Canvas(janela, bg='#ffffff', highlightthickness=1, highlightbackground='#d3d3d3')
    canvas_original.grid(row=0, column=0, rowspan=4, padx=20, pady=20)

    canvas_convolucao = tk.Canvas(janela, bg='#ffffff', highlightthickness=1, highlightbackground='#d3d3d3')
    canvas_convolucao.grid(row=0, column=1, rowspan=4, padx=20, pady=20)

    def processar_valores(nucleo=None):
        if nucleo is None:
            nucleo = [[float(entry.get()) for entry in entradas[i:i+3]] for i in range(0, len(entradas), 3)]
        imagem_convolucao = aplicar_convolucao(nucleo)
        global imagem
        imagem = imagem_convolucao
        atualizar_imagem()

    def selecionar_imagem():
        global imagem, imagem_original
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg;*.png;*.bmp")])
        if caminho_imagem:
            imagem_original = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
            imagem = imagem_original.copy()
            if imagem is None:
                messagebox.showerror("Erro", "Imagem não pode ser carregada.")
            else:
                messagebox.showinfo("Sucesso", "Imagem carregada com sucesso.")
                atualizar_imagem()
        else:
            messagebox.showwarning("Aviso", "Seleção de imagem cancelada.")

    def atualizar_imagem():
        global imagem, imagem_tk, imagem_original_tk
        altura, largura = imagem.shape

        canvas_original.config(width=largura, height=altura)
        canvas_convolucao.config(width=largura, height=altura)

        imagem_tk = ImageTk.PhotoImage(image=Image.fromarray(imagem))
        canvas_convolucao.create_image(largura // 2, altura // 2, anchor=tk.CENTER, image=imagem_tk)

        imagem_original_tk = ImageTk.PhotoImage(image=Image.fromarray(imagem_original))
        canvas_original.create_image(largura // 2, altura // 2, anchor=tk.CENTER, image=imagem_original_tk)

    def reset_imagem():
        global imagem, imagem_original
        imagem = imagem_original.copy()
        atualizar_imagem()

    def carregar_nucleo():
        try:
            caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")], title="Selecione o arquivo de núcleo")
            if caminho_arquivo:
                with open(caminho_arquivo, 'r') as arquivo:
                    nucleo_str = arquivo.read().strip()
                    nucleo = [float(valor) for valor in nucleo_str.split()]
                    nucleo = [nucleo[i:i+3] for i in range(0, len(nucleo), 3)]
                    processar_valores(nucleo)
            else:
                messagebox.showwarning("Aviso", "Seleção de arquivo cancelada.")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de núcleo não encontrado.")

    entradas = []
    for i in range(9):
        entrada = tk.Entry(janela, width=5, bg='#ffffff', fg='#333333', font=('Arial', 14), justify='center')
        entrada.grid(row=i//3, column=3 + (i%3), padx=5, pady=5)
        entradas.append(entrada)

    estilo_botao = {'bg': '#4caf50', 'fg': 'white', 'font': ('Arial', 12), 'activebackground': '#45a049'}
    botao_aplicar = tk.Button(janela, text="Aplicar Convolução", command=processar_valores, **estilo_botao)
    botao_aplicar.grid(row=3, column=3, columnspan=3, padx=10, pady=10)

    botao_selecionar = tk.Button(janela, text="Selecionar Imagem", command=selecionar_imagem, **estilo_botao)
    botao_selecionar.grid(row=4, column=3, columnspan=3, padx=10, pady=10)

    botao_reset = tk.Button(janela, text="Reset Imagem", command=reset_imagem, **estilo_botao)
    botao_reset.grid(row=5, column=3, columnspan=3, padx=10, pady=10)

    botao_carregar_nucleo = tk.Button(janela, text="Carregar Núcleo", command=carregar_nucleo, **estilo_botao)
    botao_carregar_nucleo.grid(row=6, column=3, columnspan=3, padx=10, pady=10)

    janela.mainloop()

def aplicar_convolucao(nucleo):
    altura, largura = imagem.shape
    imagem_convolucao = np.zeros((altura, largura), dtype=np.float32)

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            soma = 0
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    soma += imagem[y + ky, x + kx] * nucleo[ky + 1][kx + 1]
            imagem_convolucao[y, x] = soma

    imagem_convolucao = np.clip(imagem_convolucao, 0, 255).astype(np.uint8)
    return imagem_convolucao

if __name__ == "__main__":
    criar_interface()
