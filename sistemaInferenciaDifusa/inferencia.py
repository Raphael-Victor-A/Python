import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk


class SistemaAvaliacaoRestaurante:
    """Sistema de Inferência Difusa para avaliação de gorjetas"""

    def __init__(self):
        # Variáveis de entrada e saída
        self.qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade')
        self.servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
        self.ambiente = ctrl.Antecedent(np.arange(0, 11, 1), 'ambiente')
        self.gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

        # Funções de pertinência
        for var in [self.qualidade, self.servico, self.ambiente]:
            var['ruim'] = fuzz.trimf(var.universe, [0, 0, 5])
            var['aceitavel'] = fuzz.trimf(var.universe, [0, 5, 10])
            var['excelente'] = fuzz.trimf(var.universe, [5, 10, 10])

        self.gorjeta['baixa'] = fuzz.trimf(self.gorjeta.universe, [0, 0, 13])
        self.gorjeta['media'] = fuzz.trimf(self.gorjeta.universe, [0, 13, 25])
        self.gorjeta['alta'] = fuzz.trimf(self.gorjeta.universe, [13, 25, 25])

        # Regras difusas
        self.regras = [
            ctrl.Rule(self.qualidade['ruim'] | self.servico['ruim'], self.gorjeta['baixa']),
            ctrl.Rule(self.servico['aceitavel'], self.gorjeta['media']),
            ctrl.Rule(self.qualidade['aceitavel'], self.gorjeta['media']),
            ctrl.Rule(self.qualidade['excelente'] & self.servico['excelente'], self.gorjeta['alta']),
            ctrl.Rule(self.ambiente['excelente'] & (self.qualidade['excelente'] | self.servico['excelente']),
                      self.gorjeta['alta']),
            ctrl.Rule(self.qualidade['aceitavel'] & self.servico['ruim'] & self.ambiente['ruim'],
                      self.gorjeta['baixa']),
            ctrl.Rule(self.qualidade['excelente'] & self.ambiente['excelente'], self.gorjeta['alta'])
        ]

        self.sistema_ctrl = ctrl.ControlSystem(self.regras)
        self.simulacao = ctrl.ControlSystemSimulation(self.sistema_ctrl)

    def calcular_gorjeta(self, qualidade_val, servico_val, ambiente_val):
        """Calcula a gorjeta"""
        self.simulacao.input['qualidade'] = qualidade_val
        self.simulacao.input['servico'] = servico_val
        self.simulacao.input['ambiente'] = ambiente_val
        self.simulacao.compute()
        return self.simulacao.output['gorjeta']

    def mostrar_graficos_unicos(self, qualidade_val, servico_val, ambiente_val, gorjeta_val):
        """Mostra todas as funções de pertinência em uma tela única com as notas destacadas"""
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        # Qualidade
        axs[0, 0].plot(self.qualidade.universe, self.qualidade['ruim'].mf, 'r', label='Ruim')
        axs[0, 0].plot(self.qualidade.universe, self.qualidade['aceitavel'].mf, 'g', label='Aceitável')
        axs[0, 0].plot(self.qualidade.universe, self.qualidade['excelente'].mf, 'b', label='Excelente')
        axs[0, 0].axvline(qualidade_val, color='k', linestyle='--')
        axs[0, 0].text(qualidade_val + 0.2, 0.6, f"Nota: {qualidade_val:.1f}", color='k', fontsize=10)
        axs[0, 0].set_title('Qualidade da Comida')
        axs[0, 0].legend()

        # Serviço
        axs[0, 1].plot(self.servico.universe, self.servico['ruim'].mf, 'r', label='Ruim')
        axs[0, 1].plot(self.servico.universe, self.servico['aceitavel'].mf, 'g', label='Aceitável')
        axs[0, 1].plot(self.servico.universe, self.servico['excelente'].mf, 'b', label='Excelente')
        axs[0, 1].axvline(servico_val, color='k', linestyle='--')
        axs[0, 1].text(servico_val + 0.2, 0.6, f"Nota: {servico_val:.1f}", color='k', fontsize=10)
        axs[0, 1].set_title('Qualidade do Serviço')
        axs[0, 1].legend()

        # Ambiente
        axs[1, 0].plot(self.ambiente.universe, self.ambiente['ruim'].mf, 'r', label='Ruim')
        axs[1, 0].plot(self.ambiente.universe, self.ambiente['aceitavel'].mf, 'g', label='Aceitável')
        axs[1, 0].plot(self.ambiente.universe, self.ambiente['excelente'].mf, 'b', label='Excelente')
        axs[1, 0].axvline(ambiente_val, color='k', linestyle='--')
        axs[1, 0].text(ambiente_val + 0.2, 0.6, f"Nota: {ambiente_val:.1f}", color='k', fontsize=10)
        axs[1, 0].set_title('Qualidade do Ambiente')
        axs[1, 0].legend()

        # Gorjeta
        axs[1, 1].plot(self.gorjeta.universe, self.gorjeta['baixa'].mf, 'r', label='Baixa')
        axs[1, 1].plot(self.gorjeta.universe, self.gorjeta['media'].mf, 'g', label='Média')
        axs[1, 1].plot(self.gorjeta.universe, self.gorjeta['alta'].mf, 'b', label='Alta')
        axs[1, 1].axvline(gorjeta_val, color='k', linestyle='--')
        axs[1, 1].text(gorjeta_val + 0.2, 0.6, f"Gorjeta: {gorjeta_val:.1f}%", color='k', fontsize=10)
        axs[1, 1].set_title('Gorjeta Sugerida')
        axs[1, 1].legend()

        plt.tight_layout()
        plt.show()

    def superficie_controle(self, ambiente_fixo=5):
        """Gera gráfico 3D"""
        qualidade_range = np.arange(0, 11, 1)
        servico_range = np.arange(0, 11, 1)
        z = np.zeros((len(servico_range), len(qualidade_range)))

        for i, s in enumerate(servico_range):
            for j, q in enumerate(qualidade_range):
                z[i, j] = self.calcular_gorjeta(q, s, ambiente_fixo)

        X, Y = np.meshgrid(qualidade_range, servico_range)
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, z, cmap='viridis', edgecolor='none', alpha=0.9)
        ax.set_xlabel('Qualidade da Comida')
        ax.set_ylabel('Qualidade do Serviço')
        ax.set_zlabel('Gorjeta (%)')
        ax.set_title(f'Superfície de Controle (Ambiente={ambiente_fixo})')
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()


# ====================== INTERFACE GRÁFICA ======================

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Difuso - Avaliação de Restaurante")
        self.root.geometry("520x630")
        self.root.resizable(False, False)
        self.sistema = SistemaAvaliacaoRestaurante()

        ttk.Label(root, text="🍽️ Avaliação de Restaurante", font=("Arial", 16, "bold")).pack(pady=10)

        self.qualidade = tk.DoubleVar(value=5)
        self.servico = tk.DoubleVar(value=5)
        self.ambiente = tk.DoubleVar(value=5)
        self.gorjeta_calculada = None

        self._criar_slider_com_botoes("Qualidade da Comida:", self.qualidade)
        self._criar_slider_com_botoes("Qualidade do Serviço:", self.servico)
        self._criar_slider_com_botoes("Qualidade do Ambiente:", self.ambiente)

        ttk.Button(root, text="💰 Calcular Gorjeta", command=self.calcular).pack(pady=10)
        ttk.Button(root, text="📊 Mostrar Gráficos das Avaliações", command=self.mostrar_graficos).pack(pady=10)
        ttk.Button(root, text="🌐 Mostrar Gráfico 3D", command=self.mostrar_grafico_3d).pack(pady=10)

        self.resultado_label = ttk.Label(root, text="Gorjeta sugerida: -- %", font=("Arial", 14, "bold"))
        self.resultado_label.pack(pady=20)

    def _criar_slider_com_botoes(self, texto, variavel):
        frame = ttk.Frame(self.root)
        frame.pack(pady=5)

        ttk.Label(frame, text=texto, font=("Arial", 11)).grid(row=0, column=1, columnspan=3)

        # Botão diminuir
        btn_menos = ttk.Button(frame, text="◀", width=3, command=lambda v=variavel: self._ajustar_valor(v, -0.5))
        btn_menos.grid(row=1, column=0, padx=5)

        # Slider
        slider = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=variavel, length=300)
        slider.grid(row=1, column=1)

        # Botão aumentar
        btn_mais = ttk.Button(frame, text="▶", width=3, command=lambda v=variavel: self._ajustar_valor(v, 0.5))
        btn_mais.grid(row=1, column=2, padx=5)

        ttk.Label(frame, textvariable=variavel).grid(row=2, column=1)

    def _ajustar_valor(self, variavel, incremento):
        novo_valor = round(variavel.get() + incremento, 1)
        if 0 <= novo_valor <= 10:
            variavel.set(novo_valor)

    def calcular(self):
        q = self.qualidade.get()
        s = self.servico.get()
        a = self.ambiente.get()
        gorjeta = self.sistema.calcular_gorjeta(q, s, a)
        self.gorjeta_calculada = gorjeta
        self.resultado_label.config(text=f"💰 Gorjeta sugerida: {gorjeta:.2f}%")

    def mostrar_graficos(self):
        """Mostra os gráficos das funções de pertinência"""
        if self.gorjeta_calculada is None:
            self.calcular()
        q = self.qualidade.get()
        s = self.servico.get()
        a = self.ambiente.get()
        g = self.gorjeta_calculada
        self.sistema.mostrar_graficos_unicos(q, s, a, g)

    def mostrar_grafico_3d(self):
        """Mostra o gráfico 3D"""
        a = self.ambiente.get()
        self.sistema.superficie_controle(a)


# ====================== EXECUÇÃO ======================

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
