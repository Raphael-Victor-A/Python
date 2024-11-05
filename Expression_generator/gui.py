import tkinter as tk
from tkinter import scrolledtext
from nucleo import gerar_texto, atualizar_gramatica, gramatica
from tkinter import messagebox

# Função para organizar e exibir a gramática
def exibir_gramatica():
    nomes = []
    verbos = []
    cidades = []

    for regra in gramatica:
        if regra[0] == 'NP':  # Nomes
            nomes.append(regra[1])
        elif regra[0] == 'VP':  # Verbos
            verbos.append(' '.join(regra[1:]))
        elif regra[0] == 'Cidade':  # Cidades
            cidades.append(regra[1])

    # Monta o texto organizado
    texto_gramatica = "Nomes:\n" + ', '.join(nomes) + "\n\n"
    texto_gramatica += "Verbos:\n" + '\n'.join(verbos) + "\n\n"
    texto_gramatica += "Cidades:\n" + ', '.join(cidades)

    saida_gramatica.config(state=tk.NORMAL)
    saida_gramatica.delete(1.0, tk.END)
    saida_gramatica.insert(tk.END, texto_gramatica)

def atualizar_gramatica_gui():
    try:
        texto_atualizado = saida_gramatica.get(1.0, tk.END).strip()
        partes = texto_atualizado.split("\n\n")

        if len(partes) < 3:
            raise ValueError("Formato de gramática inválido. Certifique-se de que todas as seções (Nomes, Verbos, Cidades) estão presentes.")

        novos_nomes = partes[0].replace("Nomes:\n", "").split(", ") if "Nomes:\n" in partes[0] else []
        novos_verbos = partes[1].replace("Verbos:\n", "").split("\n") if "Verbos:\n" in partes[1] else []
        novas_cidades = partes[2].replace("Cidades:\n", "").split(", ") if "Cidades:\n" in partes[2] else []

        nova_gramatica = []

        for nome in novos_nomes:
            nova_gramatica.append(['NP', nome])

        for verbo in novos_verbos:
            nova_gramatica.append(['VP'] + verbo.split())

        for cidade in novas_cidades:
            nova_gramatica.append(['Cidade', cidade])

        if not any(regra[0] == 'S' for regra in nova_gramatica):
            nova_gramatica.insert(0, ['S', 'NP', 'VP'])

        atualizar_gramatica(nova_gramatica)
        atualizar_gramatica_sem_tratamento()
        exibir_gramatica()
        messagebox.showinfo("Sucesso", "Gramática tratada atualizada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar gramática: {e}")




def atualizar_gramatica_sem_tratamento():
    try:
        texto_atualizado = saida_gramatica.get(1.0, tk.END).strip().splitlines()
        nova_gramatica = []

        for linha in texto_atualizado:
            if linha.startswith("[") and linha.endswith("]"):  # Verifica se é uma lista válida
                try:
                    regra = eval(linha)  # Avalia a linha como uma lista
                    nova_gramatica.append(regra)
                except SyntaxError:
                    raise ValueError(f"Sintaxe inválida na linha: {linha}")

        if not any(regra[0] == 'S' for regra in nova_gramatica):
            nova_gramatica.insert(0, ['S', 'NP', 'VP'])

        atualizar_gramatica(nova_gramatica)
        exibir_gramatica()  # Atualiza a exibição da gramática tratada
        messagebox.showinfo("Sucesso", "Gramática sem tratamento atualizada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar gramática sem tratamento: {e}")


def gerar_texto_gui(event=None):
    try:
        if not entrada_quantidade.get().strip():
            raise ValueError("O campo de quantidade está vazio!")

        quant = int(entrada_quantidade.get())

        if quant <= 0:
            raise ValueError("A quantidade deve ser um número maior que zero.")

        saida_texto.config(state=tk.NORMAL)
        saida_texto.delete(1.0, tk.END)

        textos = gerar_texto(quant)  
        for i, texto in enumerate(textos, start=1):
            saida_texto.insert(tk.END, f'Texto {i}: {texto}\n')

        saida_texto.config(state=tk.DISABLED)

    except ValueError as e:
        messagebox.showerror("Erro", str(e))

def mostrar_gramatica_sem_tratamento():
    saida_gramatica.config(state=tk.NORMAL)
    saida_gramatica.delete(1.0, tk.END)
    
    saida_gramatica.insert(tk.END, "Gramática sem tratamento:\n")
    for regra in gramatica:
        saida_gramatica.insert(tk.END, f"{regra}\n")

def mostrar_gramatica_com_tratamento():
    saida_gramatica.config(state=tk.NORMAL)
    saida_gramatica.delete(1.0, tk.END)
    
    # Exibindo a gramática tratada
    exibir_gramatica()  # Chama a função que já formata a gramática tratada

# Criando a janela principal da interface
janela = tk.Tk()
janela.title("Gerador de Textos Aleatórios")

# Definindo o tamanho da janela e centralizando
largura_janela = 800
altura_janela = 500
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Campo para entrada da quantidade de textos
label_quantidade = tk.Label(janela, text="Quantidade de textos:")
label_quantidade.pack()

entrada_quantidade = tk.Entry(janela)
entrada_quantidade.pack()

# Botão para gerar os textos
botao_gerar = tk.Button(janela, text="Gerar Textos", command=gerar_texto_gui)
botao_gerar.pack()

# Associa a tecla Enter ao botão de gerar textos
janela.bind('<Return>', gerar_texto_gui)

# Área de texto para mostrar a saída dos textos gerados
saida_texto = scrolledtext.ScrolledText(janela, width=95, height=10)
saida_texto.pack()
saida_texto.config(state=tk.DISABLED)

# Área de texto para editar a gramática
saida_gramatica = scrolledtext.ScrolledText(janela, width=95, height=10)
saida_gramatica.pack()

# Botão para atualizar a gramática
botao_atualizar = tk.Button(janela, text="Atualizar Gramática", command=atualizar_gramatica_gui)
botao_atualizar.pack()

# Botão para mostrar a gramática sem tratamento
botao_mostrar_gramatica = tk.Button(janela, text="Mostrar Gramática sem Tratamento", command=mostrar_gramatica_sem_tratamento)
botao_mostrar_gramatica.pack()

# Botão para mostrar a gramática com tratamento
botao_mostrar_gramatica_com_tratamento = tk.Button(janela, text="Mostrar Gramática com Tratamento", command=mostrar_gramatica_com_tratamento)
botao_mostrar_gramatica_com_tratamento.pack()

# Exibir a gramática automaticamente ao abrir a interface
exibir_gramatica()

# Iniciar a interface
janela.mainloop()
