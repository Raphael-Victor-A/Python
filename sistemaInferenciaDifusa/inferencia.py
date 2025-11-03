"""
SISTEMA DE INFERÊNCIA DIFUSA - AVALIAÇÃO DE RESTAURANTE

INSTALAÇÃO DAS DEPENDÊNCIAS:
Execute os seguintes comandos no terminal:

pip install numpy
pip install scipy
pip install networkx
pip install scikit-fuzzy
pip install matplotlib

OU instale tudo de uma vez:
pip install numpy scipy networkx scikit-fuzzy matplotlib
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SistemaAvaliacaoRestaurante:
    """
    Sistema de Inferência Difusa para avaliar gorjeta baseado em:
    - Qualidade da comida
    - Qualidade do serviço
    - Ambiente do restaurante
    """
    
    def __init__(self):
        print("🔧 Inicializando sistema difuso...")
        
        # Definir variáveis do universo
        self.qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade')
        self.servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
        self.ambiente = ctrl.Antecedent(np.arange(0, 11, 1), 'ambiente')
        self.gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')
        
        # Definir funções de pertinência para Qualidade
        self.qualidade['ruim'] = fuzz.trimf(self.qualidade.universe, [0, 0, 5])
        self.qualidade['aceitavel'] = fuzz.trimf(self.qualidade.universe, [0, 5, 10])
        self.qualidade['excelente'] = fuzz.trimf(self.qualidade.universe, [5, 10, 10])
        
        # Definir funções de pertinência para Serviço
        self.servico['ruim'] = fuzz.trimf(self.servico.universe, [0, 0, 5])
        self.servico['aceitavel'] = fuzz.trimf(self.servico.universe, [0, 5, 10])
        self.servico['excelente'] = fuzz.trimf(self.servico.universe, [5, 10, 10])
        
        # Definir funções de pertinência para Ambiente
        self.ambiente['ruim'] = fuzz.trimf(self.ambiente.universe, [0, 0, 5])
        self.ambiente['aceitavel'] = fuzz.trimf(self.ambiente.universe, [0, 5, 10])
        self.ambiente['excelente'] = fuzz.trimf(self.ambiente.universe, [5, 10, 10])
        
        # Definir funções de pertinência para Gorjeta (saída)
        self.gorjeta['baixa'] = fuzz.trimf(self.gorjeta.universe, [0, 0, 13])
        self.gorjeta['media'] = fuzz.trimf(self.gorjeta.universe, [0, 13, 25])
        self.gorjeta['alta'] = fuzz.trimf(self.gorjeta.universe, [13, 25, 25])
        
        # Criar regras difusas
        self._criar_regras()
        
        # Criar sistema de controle
        self.sistema_ctrl = ctrl.ControlSystem(self.regras)
        self.simulacao = ctrl.ControlSystemSimulation(self.sistema_ctrl)
        
        print("✅ Sistema inicializado com sucesso!\n")
    
    def _criar_regras(self):
        """Define as regras do sistema difuso"""
        self.regras = [
            # Regra 1: Se tudo é ruim, gorjeta baixa
            ctrl.Rule(self.qualidade['ruim'] | self.servico['ruim'], 
                     self.gorjeta['baixa']),
            
            # Regra 2: Se serviço é aceitável
            ctrl.Rule(self.servico['aceitavel'], self.gorjeta['media']),
            
            # Regra 3: Se qualidade é aceitável
            ctrl.Rule(self.qualidade['aceitavel'], self.gorjeta['media']),
            
            # Regra 4: Se tudo é excelente, gorjeta alta
            ctrl.Rule(self.qualidade['excelente'] & self.servico['excelente'], 
                     self.gorjeta['alta']),
            
            # Regra 5: Ambiente influencia positivamente
            ctrl.Rule(self.ambiente['excelente'] & 
                     (self.qualidade['excelente'] | self.servico['excelente']), 
                     self.gorjeta['alta']),
            
            # Regra 6: Combinação ruim
            ctrl.Rule(self.qualidade['aceitavel'] & self.servico['ruim'] & 
                     self.ambiente['ruim'], self.gorjeta['baixa']),
            
            # Regra 7: Qualidade + Ambiente excelentes
            ctrl.Rule(self.qualidade['excelente'] & self.ambiente['excelente'], 
                     self.gorjeta['alta']),
        ]
        
        print(f"📋 {len(self.regras)} regras difusas criadas:")
        for i, regra in enumerate(self.regras, 1):
            print(f"   Regra {i}: {regra}")
        print()
    
    def calcular_gorjeta(self, qualidade_val, servico_val, ambiente_val):
        """
        Calcula a gorjeta baseada nos valores de entrada
        """
        self.simulacao.input['qualidade'] = qualidade_val
        self.simulacao.input['servico'] = servico_val
        self.simulacao.input['ambiente'] = ambiente_val
        
        # Computar resultado
        self.simulacao.compute()
        
        return self.simulacao.output['gorjeta']
    
    def visualizar_funcoes_pertinencia(self):
        """Visualiza todas as funções de pertinência"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Funções de Pertinência do Sistema Difuso', 
                    fontsize=16, fontweight='bold')
        
        # Qualidade
        self.qualidade.view(ax=axes[0, 0])
        axes[0, 0].set_title('Qualidade da Comida', fontweight='bold')
        axes[0, 0].set_xlabel('Nota (0-10)')
        axes[0, 0].set_ylabel('Grau de Pertinência')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend(['Ruim', 'Aceitável', 'Excelente'], loc='upper right')
        
        # Serviço
        self.servico.view(ax=axes[0, 1])
        axes[0, 1].set_title('Qualidade do Serviço', fontweight='bold')
        axes[0, 1].set_xlabel('Nota (0-10)')
        axes[0, 1].set_ylabel('Grau de Pertinência')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend(['Ruim', 'Aceitável', 'Excelente'], loc='upper right')
        
        # Ambiente
        self.ambiente.view(ax=axes[1, 0])
        axes[1, 0].set_title('Qualidade do Ambiente', fontweight='bold')
        axes[1, 0].set_xlabel('Nota (0-10)')
        axes[1, 0].set_ylabel('Grau de Pertinência')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend(['Ruim', 'Aceitável', 'Excelente'], loc='upper right')
        
        # Gorjeta (saída)
        self.gorjeta.view(ax=axes[1, 1])
        axes[1, 1].set_title('Gorjeta Sugerida (%)', fontweight='bold')
        axes[1, 1].set_xlabel('Gorjeta (%)')
        axes[1, 1].set_ylabel('Grau de Pertinência')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend(['Baixa', 'Média', 'Alta'], loc='upper right')
        
        plt.tight_layout()
        plt.show()
    
    def calcular_pertinencias(self, valor, tipo_variavel):
        """Calcula graus de pertinência para um valor"""
        if tipo_variavel == 'qualidade':
            var = self.qualidade
        elif tipo_variavel == 'servico':
            var = self.servico
        elif tipo_variavel == 'ambiente':
            var = self.ambiente
        else:
            return {}
        
        pertinencias = {}
        for termo in var.terms:
            nivel = fuzz.interp_membership(var.universe, 
                                          var[termo].mf, 
                                          valor)
            pertinencias[termo] = nivel
        
        return pertinencias
    
    def visualizar_inferencia(self, qualidade_val, servico_val, ambiente_val):
        """
        Visualiza o processo de inferência para valores específicos
        """
        gorjeta_val = self.calcular_gorjeta(qualidade_val, servico_val, ambiente_val)
        
        # Calcular pertinências
        pert_qual = self.calcular_pertinencias(qualidade_val, 'qualidade')
        pert_serv = self.calcular_pertinencias(servico_val, 'servico')
        pert_amb = self.calcular_pertinencias(ambiente_val, 'ambiente')
        
        print("\n" + "="*60)
        print("ANÁLISE DE PERTINÊNCIA")
        print("="*60)
        print(f"\nQualidade = {qualidade_val}:")
        for termo, valor in pert_qual.items():
            print(f"  {termo}: {valor:.3f}")
        
        print(f"\nServiço = {servico_val}:")
        for termo, valor in pert_serv.items():
            print(f"  {termo}: {valor:.3f}")
        
        print(f"\nAmbiente = {ambiente_val}:")
        for termo, valor in pert_amb.items():
            print(f"  {termo}: {valor:.3f}")
        print("="*60 + "\n")
        
        # Criar visualização em uma única figura
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle(f'Processo de Inferência Difusa\n'
                    f'Qualidade={qualidade_val}, Serviço={servico_val}, '
                    f'Ambiente={ambiente_val} → Gorjeta={gorjeta_val:.1f}%',
                    fontsize=12, fontweight='bold')
        
        # Criar subplot layout
        ax1 = plt.subplot(2, 2, 1)
        ax2 = plt.subplot(2, 2, 2)
        ax3 = plt.subplot(2, 2, 3)
        ax4 = plt.subplot(2, 2, 4)
        
        # Visualizar ativação - Qualidade
        ax1.plot(self.qualidade.universe, 
                fuzz.trimf(self.qualidade.universe, [0, 0, 5]), 
                'b', linewidth=1.5, label='Ruim')
        ax1.plot(self.qualidade.universe, 
                fuzz.trimf(self.qualidade.universe, [0, 5, 10]), 
                'g', linewidth=1.5, label='Aceitável')
        ax1.plot(self.qualidade.universe, 
                fuzz.trimf(self.qualidade.universe, [5, 10, 10]), 
                'r', linewidth=1.5, label='Excelente')
        ax1.axvline(qualidade_val, color='black', linestyle='--', 
                   linewidth=2, label=f'Entrada: {qualidade_val}')
        ax1.set_title('Qualidade da Comida', fontweight='bold')
        ax1.set_xlabel('Nota')
        ax1.set_ylabel('Pertinência')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([-0.1, 1.1])
        
        # Visualizar ativação - Serviço
        ax2.plot(self.servico.universe, 
                fuzz.trimf(self.servico.universe, [0, 0, 5]), 
                'b', linewidth=1.5, label='Ruim')
        ax2.plot(self.servico.universe, 
                fuzz.trimf(self.servico.universe, [0, 5, 10]), 
                'g', linewidth=1.5, label='Aceitável')
        ax2.plot(self.servico.universe, 
                fuzz.trimf(self.servico.universe, [5, 10, 10]), 
                'r', linewidth=1.5, label='Excelente')
        ax2.axvline(servico_val, color='black', linestyle='--', 
                   linewidth=2, label=f'Entrada: {servico_val}')
        ax2.set_title('Qualidade do Serviço', fontweight='bold')
        ax2.set_xlabel('Nota')
        ax2.set_ylabel('Pertinência')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([-0.1, 1.1])
        
        # Visualizar ativação - Ambiente
        ax3.plot(self.ambiente.universe, 
                fuzz.trimf(self.ambiente.universe, [0, 0, 5]), 
                'b', linewidth=1.5, label='Ruim')
        ax3.plot(self.ambiente.universe, 
                fuzz.trimf(self.ambiente.universe, [0, 5, 10]), 
                'g', linewidth=1.5, label='Aceitável')
        ax3.plot(self.ambiente.universe, 
                fuzz.trimf(self.ambiente.universe, [5, 10, 10]), 
                'r', linewidth=1.5, label='Excelente')
        ax3.axvline(ambiente_val, color='black', linestyle='--', 
                   linewidth=2, label=f'Entrada: {ambiente_val}')
        ax3.set_title('Qualidade do Ambiente', fontweight='bold')
        ax3.set_xlabel('Nota')
        ax3.set_ylabel('Pertinência')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([-0.1, 1.1])
        
        # Visualizar saída - Gorjeta (manualmente para evitar nova figura)
        ax4.plot(self.gorjeta.universe, 
                fuzz.trimf(self.gorjeta.universe, [0, 0, 13]), 
                'b', linewidth=1.5, label='Baixa')
        ax4.plot(self.gorjeta.universe, 
                fuzz.trimf(self.gorjeta.universe, [0, 13, 25]), 
                'g', linewidth=1.5, label='Média')
        ax4.plot(self.gorjeta.universe, 
                fuzz.trimf(self.gorjeta.universe, [13, 25, 25]), 
                'r', linewidth=1.5, label='Alta')
        
        # Adicionar linha vertical da saída
        ax4.axvline(gorjeta_val, color='black', linestyle='--', 
                   linewidth=2, label=f'Saída: {gorjeta_val:.1f}%')
        
        # Visualizar área agregada (simulação da defuzzificação)
        gorjeta_activation = fuzz.interp_membership(self.gorjeta.universe, 
                                                    self.gorjeta['baixa'].mf, 
                                                    gorjeta_val)
        ax4.fill_between(self.gorjeta.universe, 0, 
                        np.minimum(gorjeta_activation, self.gorjeta['baixa'].mf), 
                        alpha=0.3, color='blue')
        
        ax4.set_title('Gorjeta Calculada (Defuzzificação)', fontweight='bold')
        ax4.set_xlabel('Gorjeta (%)')
        ax4.set_ylabel('Pertinência')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim([-0.1, 1.1])
        
        plt.tight_layout()
        plt.show()
        
        return gorjeta_val
    
    def superficie_controle(self):
        """
        Gera superfície de controle 3D mostrando como as entradas 
        afetam a saída
        """
        print("📊 Gerando superfície de controle 3D...")
        
        # Criar grade de valores
        qualidade_range = np.arange(0, 11, 1)
        servico_range = np.arange(0, 11, 1)
        
        # Fixar ambiente em valor médio
        ambiente_fixo = 5
        
        # Calcular gorjeta para cada combinação
        z = np.zeros((len(servico_range), len(qualidade_range)))
        
        for i, servico_val in enumerate(servico_range):
            for j, qualidade_val in enumerate(qualidade_range):
                z[i, j] = self.calcular_gorjeta(qualidade_val, 
                                                servico_val, 
                                                ambiente_fixo)
        
        # Plotar superfície
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        X, Y = np.meshgrid(qualidade_range, servico_range)
        surf = ax.plot_surface(X, Y, z, cmap='viridis', 
                              edgecolor='none', alpha=0.8)
        
        ax.set_xlabel('Qualidade da Comida', fontsize=10, fontweight='bold')
        ax.set_ylabel('Qualidade do Serviço', fontsize=10, fontweight='bold')
        ax.set_zlabel('Gorjeta (%)', fontsize=10, fontweight='bold')
        ax.set_title(f'Superfície de Controle\n(Ambiente fixo em {ambiente_fixo})', 
                    fontsize=12, fontweight='bold')
        
        fig.colorbar(surf, shrink=0.5, aspect=5, label='Gorjeta (%)')
        
        plt.show()


# ============= EXEMPLO DE USO =============

def main():
    print("=" * 70)
    print(" " * 10 + "SISTEMA DE INFERÊNCIA DIFUSA")
    print(" " * 15 + "AVALIAÇÃO DE RESTAURANTE")
    print("=" * 70)
    
    try:
        # Criar sistema
        sistema = SistemaAvaliacaoRestaurante()
        
        # 1. Visualizar todas as funções de pertinência
        print("\n📊 PASSO 1: Visualizando funções de pertinência...")
        print("(Feche a janela do gráfico para continuar)\n")
        sistema.visualizar_funcoes_pertinencia()
        
        # 2. Testar diferentes cenários
        cenarios = [
            {"nome": "🔴 Experiência Ruim", "qualidade": 3, "servico": 2, "ambiente": 2},
            {"nome": "🟡 Experiência Média", "qualidade": 6, "servico": 5, "ambiente": 6},
            {"nome": "🟢 Experiência Excelente", "qualidade": 9, "servico": 9, "ambiente": 8},
            {"nome": "🟠 Comida Boa, Serviço Ruim", "qualidade": 8, "servico": 3, "ambiente": 5},
        ]
        
        print("\n" + "=" * 70)
        print("📋 PASSO 2: Testando cenários diferentes")
        print("=" * 70 + "\n")
        
        for cenario in cenarios:
            gorjeta = sistema.calcular_gorjeta(
                cenario["qualidade"], 
                cenario["servico"], 
                cenario["ambiente"]
            )
            print(f"{cenario['nome']}:")
            print(f"  📊 Qualidade: {cenario['qualidade']}/10")
            print(f"  👔 Serviço: {cenario['servico']}/10")
            print(f"  🏠 Ambiente: {cenario['ambiente']}/10")
            print(f"  💰 → Gorjeta sugerida: {gorjeta:.1f}%")
            print()
        
        # 3. Visualizar inferência detalhada para um caso específico
        print("=" * 70)
        print("🔍 PASSO 3: Visualizando processo de inferência detalhado")
        print("=" * 70)
        print("(Feche a janela do gráfico para continuar)\n")
        sistema.visualizar_inferencia(7, 8, 6)
        
        # 4. Mostrar superfície de controle
        print("\n" + "=" * 70)
        print("🌐 PASSO 4: Gerando superfície de controle 3D")
        print("=" * 70)
        print("(Feche a janela do gráfico para continuar)\n")
        sistema.superficie_controle()
        
        # 5. Modo interativo
        print("\n" + "=" * 70)
        print(" " * 20 + "MODO INTERATIVO")
        print("=" * 70)
        
        while True:
            print("\n" + "-" * 70)
            print("Digite os valores de 0 a 10 ou 'sair' para encerrar:")
            print("-" * 70)
            
            entrada = input("\n📊 Qualidade da comida (0-10): ")
            if entrada.lower() in ['sair', 'exit', 'quit', 's']:
                break
                
            try:
                qualidade = float(entrada)
                servico = float(input("👔 Qualidade do serviço (0-10): "))
                ambiente = float(input("🏠 Qualidade do ambiente (0-10): "))
                
                if not (0 <= qualidade <= 10 and 0 <= servico <= 10 and 0 <= ambiente <= 10):
                    print("\n❌ Valores devem estar entre 0 e 10!")
                    continue
                
                gorjeta = sistema.calcular_gorjeta(qualidade, servico, ambiente)
                
                print("\n" + "=" * 50)
                print(f"💰  GORJETA SUGERIDA: {gorjeta:.2f}%")
                print("=" * 50)
                
                visualizar = input("\n🔍 Deseja visualizar a inferência detalhada? (s/n): ")
                if visualizar.lower() in ['s', 'sim', 'y', 'yes']:
                    sistema.visualizar_inferencia(qualidade, servico, ambiente)
                    
            except ValueError:
                print("\n❌ Entrada inválida! Digite números entre 0 e 10.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}")
        
        print("\n" + "=" * 70)
        print("✅ Sistema encerrado. Obrigado por usar!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        print("\nVerifique se todas as dependências estão instaladas:")
        print("  pip install numpy scipy networkx scikit-fuzzy matplotlib")


if __name__ == "__main__":
    main()