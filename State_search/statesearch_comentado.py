import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from queue import Queue, PriorityQueue
import time
import tracemalloc
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from copy import deepcopy
import heapq

# =============================================================================
# ESTRUTURAS DE DADOS E CLASSES BASE
# =============================================================================

@dataclass
class SearchMetrics:
    """Métricas de desempenho da busca
    - Armazena resultados de tempo, memória e eficiência
    - Usa dataclass para simplificar a criação e acesso aos dados
    """
    execution_time: float        # Tempo total de execução
    memory_used: float           # Memória RAM utilizada em MB
    nodes_expanded: int          # Número de nós explorados
    path_length: int             # Comprimento do caminho solução
    solution_found: bool         # Indica se solução foi encontrada

class PuzzleState:
    """Estado do 8-Puzzle - Representa uma configuração do tabuleiro"""
    
    def __init__(self, board: List[List[int]], parent=None, move=""):
        # Inicialização do estado com board, estado pai e movimento realizado
        self.board = board        # Matriz 3x3 representando o tabuleiro
        self.parent = parent      # Referência ao estado anterior (para reconstruir caminho)
        self.move = move          # Descrição do movimento feito ("Cima", "Baixo", etc.)
        self.g = 0 if parent is None else parent.g + 1  # Custo do caminho do início até este nó
        self.h = self.calculate_heuristic()  # Heurística (estimativa para o objetivo)
        self.f = self.g + self.h  # Função de avaliação total (g + h)
    
    def calculate_heuristic(self) -> int:
        """Heurística de distância Manhattan
        - Calcula a soma das distâncias de cada peça até sua posição final
        - É admissível (não superestima o custo real)
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:  # Ignora o espaço vazio
                    value = self.board[i][j]
                    target_row = (value - 1) // 3  # Linha destino na solução
                    target_col = (value - 1) % 3   # Coluna destino na solução
                    distance += abs(i - target_row) + abs(j - target_col)  # Distância Manhattan
        return distance
    
    def get_blank_position(self) -> Tuple[int, int]:
        """Encontra a posição do espaço vazio (0)
        - Retorna coordenadas (linha, coluna) do espaço vazio
        - Essencial para gerar movimentos válidos
        """
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1  # Caso de erro (não deveria acontecer)
    
    def get_neighbors(self) -> List['PuzzleState']:
        """Gera estados vizinhos válidos
        - Cria novos estados movendo o espaço vazio nas 4 direções
        - Verifica limites do tabuleiro para movimentos válidos
        """
        neighbors = []
        blank_row, blank_col = self.get_blank_position()
        
        # Movimentos possíveis: cima, baixo, esquerda, direita
        # (delta_linha, delta_coluna, descrição)
        moves = [
            (-1, 0, "Cima"),
            (1, 0, "Baixo"),
            (0, -1, "Esquerda"),
            (0, 1, "Direita")
        ]
        
        for dr, dc, move_name in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            # Verifica se o movimento está dentro do tabuleiro
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Cria cópia do tabuleiro para não modificar o original
                new_board = [row[:] for row in self.board]
                # Troca o espaço vazio com a peça adjacente
                new_board[blank_row][blank_col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[blank_row][blank_col]
                neighbors.append(PuzzleState(new_board, self, move_name))
        
        return neighbors
    
    def is_goal(self) -> bool:
        """Verifica se é o estado objetivo
        - Compara com a configuração final padrão do 8-Puzzle
        """
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal
    
    def __hash__(self):
        """Hash baseado no tabuleiro para uso em conjuntos"""
        return hash(str(self.board))
    
    def __eq__(self, other):
        """Comparação de igualdade baseada no tabuleiro"""
        return self.board == other.board
    
    def __lt__(self, other):
        """Comparação menor que para ordenação na fila de prioridade"""
        return self.f < other.f
    
    def __str__(self):
        """Representação em string para exibição"""
        return '\n'.join([' '.join([str(cell) if cell != 0 else '_' for cell in row]) 
                         for row in self.board])

class MissionaryState:
    """Estado do problema dos Missionários e Canibais
    - Representa a distribuição de pessoas entre as margens do rio
    """
    
    def __init__(self, left_m: int, left_c: int, boat_left: bool, parent=None, move=""):
        self.left_m = left_m      # Missionários na margem esquerda
        self.left_c = left_c      # Canibais na margem esquerda  
        self.boat_left = boat_left  # Posição do barco (True = esquerda, False = direita)
        self.parent = parent      # Estado anterior no caminho
        self.move = move          # Descrição do movimento
        self.g = 0 if parent is None else parent.g + 1  # Custo do caminho
        self.h = self.calculate_heuristic()  # Heurística
        self.f = self.g + self.h  # Função de avaliação
    
    def calculate_heuristic(self) -> int:
        """Heurística: número de pessoas na margem esquerda
        - Estimativa simples: quanto mais pessoas na esquerda, mais longe do objetivo
        """
        return self.left_m + self.left_c
    
    def is_valid(self) -> bool:
        """Verifica se o estado é válido
        - Canibais não podem superar missionários em nenhuma margem
        - Números não podem ser negativos
        """
        right_m = 3 - self.left_m  # Missionários na direita
        right_c = 3 - self.left_c  # Canibais na direita
        
        # Verifica limites (números não negativos)
        if self.left_m < 0 or self.left_c < 0 or right_m < 0 or right_c < 0:
            return False
        
        # Verifica se canibais não superam missionários em qualquer margem
        # Apenas aplica a regra se houver missionários na margem
        if self.left_m > 0 and self.left_m < self.left_c:
            return False
        if right_m > 0 and right_m < right_c:
            return False
        
        return True
    
    def get_neighbors(self) -> List['MissionaryState']:
        """Gera estados vizinhos válidos
        - Simula todas as combinações possíveis de movimentos do barco
        """
        neighbors = []
        
        # Possíveis movimentos: (missionários, canibais) no barco
        # Capacidade máxima: 2 pessoas
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        for m, c in moves:
            if self.boat_left:
                # Barco vai para direita: remove pessoas da margem esquerda
                new_state = MissionaryState(
                    self.left_m - m, self.left_c - c, False, 
                    self, f"{m}M {c}C →"  # Seta indica direção do movimento
                )
            else:
                # Barco volta para esquerda: adiciona pessoas na margem esquerda
                new_state = MissionaryState(
                    self.left_m + m, self.left_c + c, True, 
                    self, f"{m}M {c}C ←"  # Seta indica direção do movimento
                )
            
            # Só adiciona se o estado gerado for válido
            if new_state.is_valid():
                neighbors.append(new_state)
        
        return neighbors
    
    def is_goal(self) -> bool:
        """Verifica se todos estão na margem direita"""
        return self.left_m == 0 and self.left_c == 0
    
    def __hash__(self):
        """Hash baseado na configuração completa do estado"""
        return hash((self.left_m, self.left_c, self.boat_left))
    
    def __eq__(self, other):
        """Comparação de igualdade entre estados"""
        return (self.left_m == other.left_m and 
                self.left_c == other.left_c and 
                self.boat_left == other.boat_left)
    
    def __lt__(self, other):
        """Comparação para ordenação na fila de prioridade do A*"""
        return self.f < other.f
    
    def __str__(self):
        """Representação amigável do estado"""
        right_m = 3 - self.left_m
        right_c = 3 - self.left_c
        boat = "🚤" if self.boat_left else "  "  # Emoji para visualização
        return f"Esq: {self.left_m}M {self.left_c}C {boat} | Dir: {right_m}M {right_c}C"

# =============================================================================
# ALGORITMOS DE BUSCA
# =============================================================================

class SearchAlgorithms:
    """Implementação dos algoritmos de busca
    - Classe estática (não precisa de instância)
    - Métodos independentes que operam em estados genéricos
    """
    
    @staticmethod
    def bfs(initial_state) -> Tuple[Optional[List], SearchMetrics]:
        """Busca em Largura (BFS)
        - Explora todos os nós de um nível antes de ir para o próximo
        - Garante solução ótima (menor número de passos)
        - Pode ser ineficiente em espaço para problemas complexos
        """
        # Inicia medição de memória
        tracemalloc.start()
        start_time = time.time()  # Marca tempo inicial
        
        # Estruturas para BFS
        queue = Queue()           # Fila FIFO para nós a explorar
        queue.put(initial_state)
        visited = {initial_state} # Conjunto para estados visitados (evita repetição)
        nodes_expanded = 0        # Contador de nós expandidos
        
        # Loop principal da busca
        while not queue.empty():
            current = queue.get()  # Pega próximo nó da fila
            nodes_expanded += 1    # Incrementa contador
            
            # Verifica se encontrou solução
            if current.is_goal():
                path = SearchAlgorithms._reconstruct_path(current)
                execution_time = time.time() - start_time
                memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024  # Converte para MB
                tracemalloc.stop()  # Para medição de memória
                
                return path, SearchMetrics(
                    execution_time=execution_time,
                    memory_used=memory_used,
                    nodes_expanded=nodes_expanded,
                    path_length=len(path),
                    solution_found=True
                )
            
            # Expande o nó atual - gera todos os vizinhos
            for neighbor in current.get_neighbors():
                if neighbor not in visited:  # Evita estados já visitados
                    visited.add(neighbor)
                    queue.put(neighbor)
        
        # Caso não encontre solução
        execution_time = time.time() - start_time
        memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
        tracemalloc.stop()
        
        return None, SearchMetrics(
            execution_time=execution_time,
            memory_used=memory_used,
            nodes_expanded=nodes_expanded,
            path_length=0,
            solution_found=False
        )
    
    @staticmethod
    def a_star(initial_state) -> Tuple[Optional[List], SearchMetrics]:
        """Busca A*
        - Algoritmo informado que usa heurística para guiar a busca
        - Combina custo real (g) com estimativa (h) para priorizar nós promissores
        - Ótimo e completo com heurística admissível
        """
        tracemalloc.start()
        start_time = time.time()
        
        # Fila de prioridade para A* - ordena por f = g + h
        open_set = []
        # Usa heapq com tupla (prioridade, id, estado) para evitar comparação direta
        heapq.heappush(open_set, (initial_state.f, id(initial_state), initial_state))
        visited = set()  # Conjunto de estados já expandidos
        nodes_expanded = 0
        
        while open_set:
            # Pega o nó com menor f da fila de prioridade
            _, _, current = heapq.heappop(open_set)
            
            # Pula se já foi visitado (pode acontecer com diferentes caminhos)
            if current in visited:
                continue
            
            visited.add(current)
            nodes_expanded += 1
            
            if current.is_goal():
                path = SearchAlgorithms._reconstruct_path(current)
                execution_time = time.time() - start_time
                memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
                tracemalloc.stop()
                
                return path, SearchMetrics(
                    execution_time=execution_time,
                    memory_used=memory_used,
                    nodes_expanded=nodes_expanded,
                    path_length=len(path),
                    solution_found=True
                )
            
            # Expande vizinhos
            for neighbor in current.get_neighbors():
                if neighbor not in visited:
                    # Adiciona à fila de prioridade ordenada por f
                    heapq.heappush(open_set, (neighbor.f, id(neighbor), neighbor))
        
        # Caso não encontre solução
        execution_time = time.time() - start_time
        memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
        tracemalloc.stop()
        
        return None, SearchMetrics(
            execution_time=execution_time,
            memory_used=memory_used,
            nodes_expanded=nodes_expanded,
            path_length=0,
            solution_found=False
        )
    
    @staticmethod
    def _reconstruct_path(state) -> List:
        """Reconstrói o caminho da solução
        - Segue as referências aos pais desde o estado final até o inicial
        - Inverte a lista para ter a ordem correta (início -> fim)
        """
        path = []
        current = state
        while current is not None:
            path.append(current)
            current = current.parent  # Vai para o estado pai
        return list(reversed(path))  # Inverte para ordem cronológica

# =============================================================================
# INTERFACE GRÁFICA
# =============================================================================

class SearchGUI:
    """Interface Gráfica Principal
    - Gerencia toda a interação com o usuário
    - Coordena a execução dos algoritmos e exibição dos resultados
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Busca em Espaço de Estados")
        self.root.geometry("900x700")  # Tamanho inicial da janela
        
        self.setup_ui()  # Configura todos os componentes da interface
    
    def setup_ui(self):
        """Configura a interface - Divide em seções lógicas"""
        
        # =====================================================================
        # SEÇÃO 1: CONFIGURAÇÃO (seleção de problema e algoritmo)
        # =====================================================================
        select_frame = ttk.LabelFrame(self.root, text="Configuração", padding=10)
        select_frame.pack(fill="x", padx=10, pady=5)  # Preenche horizontalmente
        
        # Seleção de problema
        ttk.Label(select_frame, text="Problema:").grid(row=0, column=0, sticky="w", padx=5)
        self.problem_var = tk.StringVar(value="8-Puzzle")
        problem_combo = ttk.Combobox(select_frame, textvariable=self.problem_var, 
                                     values=["8-Puzzle", "Missionários e Canibais"],
                                     state="readonly", width=25)
        problem_combo.grid(row=0, column=1, padx=5)
        
        # Seleção de algoritmo
        ttk.Label(select_frame, text="Algoritmo:").grid(row=0, column=2, sticky="w", padx=5)
        self.algorithm_var = tk.StringVar(value="A*")
        algorithm_combo = ttk.Combobox(select_frame, textvariable=self.algorithm_var,
                                       values=["A*", "Busca em Largura (BFS)"],
                                       state="readonly", width=25)
        algorithm_combo.grid(row=0, column=3, padx=5)
        
        # =====================================================================
        # SEÇÃO 2: ENTRADA DO 8-PUZZLE 
        # =====================================================================
        self.puzzle_frame = ttk.LabelFrame(self.root, text="Estado Inicial do 8-Puzzle", padding=10)
        self.puzzle_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.puzzle_frame, 
                 text="Digite os números de 0-8 (0 = espaço vazio):").pack()
        
        # Cria grade 3x3 para entrada do puzzle
        self.puzzle_entries = []
        grid_frame = ttk.Frame(self.puzzle_frame)
        grid_frame.pack(pady=5)
        
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(grid_frame, width=5, justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.puzzle_entries.append(row_entries)
        
        # Preencher valores padrão (puzzle solucionável)
        default_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        for i in range(3):
            for j in range(3):
                self.puzzle_entries[i][j].insert(0, str(default_puzzle[i][j]))
        
        # =====================================================================
        # SEÇÃO 3: BOTÕES DE CONTROLE
        # =====================================================================
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Botões principais
        ttk.Button(button_frame, text="Executar Busca", 
                  command=self.execute_search).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Comparar Algoritmos", 
                  command=self.compare_algorithms).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", 
                  command=self.clear_output).pack(side="left", padx=5)
        
        # =====================================================================
        # SEÇÃO 4: ÁREA DE RESULTADOS
        # =====================================================================
        result_frame = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Área de texto com scroll para exibir resultados detalhados
        self.result_text = scrolledtext.ScrolledText(result_frame, height=25, width=100)
        self.result_text.pack(fill="both", expand=True)
    
    def get_puzzle_state(self) -> Optional[PuzzleState]:
        """Obtém o estado inicial do puzzle da interface
        - Valida a entrada do usuário
        - Converte texto para matriz numérica
        - Verifica se é um puzzle válido
        """
        try:
            board = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = int(self.puzzle_entries[i][j].get())
                    if value < 0 or value > 8:
                        raise ValueError("Número fora do intervalo")
                    row.append(value)
                board.append(row)
            
            # Verificar se todos os números de 0-8 estão presentes exatamente uma vez
            flat = [num for row in board for num in row]  # Achata a matriz
            if sorted(flat) != list(range(9)):
                messagebox.showerror("Erro", "Use todos os números de 0 a 8 exatamente uma vez!")
                return None
            
            return PuzzleState(board)
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números de 0 a 8!")
            return None
    
    def execute_search(self):
        """Executa a busca selecionada
        - Coordena toda a execução: entrada -> processamento -> saída
        """
        problem = self.problem_var.get()
        algorithm = self.algorithm_var.get()
        
        # Obter estado inicial baseado no problema selecionado
        if problem == "8-Puzzle":
            initial_state = self.get_puzzle_state()
            if initial_state is None:  # Se houve erro na validação
                return
        else:  # Missionários e Canibais - estado inicial fixo
            initial_state = MissionaryState(3, 3, True)  # Todos na esquerda
        
        # Cabeçalho dos resultados
        self.result_text.insert(tk.END, f"\n{'='*80}\n")
        self.result_text.insert(tk.END, f"Problema: {problem}\n")
        self.result_text.insert(tk.END, f"Algoritmo: {algorithm}\n")
        self.result_text.insert(tk.END, f"{'='*80}\n\n")
        
        # Executa o algoritmo selecionado
        if algorithm == "A*":
            path, metrics = SearchAlgorithms.a_star(initial_state)
        else:
            path, metrics = SearchAlgorithms.bfs(initial_state)
        
        # Exibe os resultados
        self.display_results(path, metrics, problem)
        self.result_text.see(tk.END)  # Rola para o final
    
    def display_results(self, path, metrics: SearchMetrics, problem: str):
        """Exibe os resultados da busca de forma organizada
        - Métricas de desempenho
        - Caminho da solução (se encontrado)
        """
        self.result_text.insert(tk.END, "MÉTRICAS DE DESEMPENHO:\n")
        self.result_text.insert(tk.END, f"  Solução encontrada: {'Sim' if metrics.solution_found else 'Não'}\n")
        self.result_text.insert(tk.END, f"  Tempo de execução: {metrics.execution_time:.4f} segundos\n")
        self.result_text.insert(tk.END, f"  Memória utilizada: {metrics.memory_used:.2f} MB\n")
        self.result_text.insert(tk.END, f"  Nós expandidos: {metrics.nodes_expanded}\n")
        self.result_text.insert(tk.END, f"  Comprimento da solução: {metrics.path_length}\n\n")
        
        if path:
            self.result_text.insert(tk.END, "CAMINHO DA SOLUÇÃO:\n")
            for i, state in enumerate(path):
                self.result_text.insert(tk.END, f"\nPasso {i}:")
                if state.move:  # Se houve movimento (não no estado inicial)
                    self.result_text.insert(tk.END, f" [{state.move}]")
                self.result_text.insert(tk.END, f"\n{state}\n")
        else:
            self.result_text.insert(tk.END, "Nenhuma solução encontrada!\n")
    
    def compare_algorithms(self):
        """Compara os dois algoritmos no mesmo problema
        - Executa ambos e exibe tabela comparativa
        - Útil para análise de desempenho
        """
        problem = self.problem_var.get()
        
        # Obter estado inicial
        if problem == "8-Puzzle":
            initial_state = self.get_puzzle_state()
            if initial_state is None:
                return
        else:
            initial_state = MissionaryState(3, 3, True)
        
        self.result_text.insert(tk.END, f"\n{'='*80}\n")
        self.result_text.insert(tk.END, f"COMPARAÇÃO DE ALGORITMOS - {problem}\n")
        self.result_text.insert(tk.END, f"{'='*80}\n\n")
        
        # Executa A* (usa deepcopy para não interferir no estado original)
        self.result_text.insert(tk.END, "Executando A*...\n")
        path_astar, metrics_astar = SearchAlgorithms.a_star(deepcopy(initial_state))
        
        # Executa BFS
        self.result_text.insert(tk.END, "Executando BFS...\n\n")
        path_bfs, metrics_bfs = SearchAlgorithms.bfs(deepcopy(initial_state))
        
        # Exibe tabela comparativa
        self.result_text.insert(tk.END, f"{'Métrica':<30} {'A*':<20} {'BFS':<20}\n")
        self.result_text.insert(tk.END, f"{'-'*70}\n")
        self.result_text.insert(tk.END, 
            f"{'Tempo (s)':<30} {metrics_astar.execution_time:<20.4f} {metrics_bfs.execution_time:<20.4f}\n")
        self.result_text.insert(tk.END, 
            f"{'Memória (MB)':<30} {metrics_astar.memory_used:<20.2f} {metrics_bfs.memory_used:<20.2f}\n")
        self.result_text.insert(tk.END, 
            f"{'Nós expandidos':<30} {metrics_astar.nodes_expanded:<20} {metrics_bfs.nodes_expanded:<20}\n")
        self.result_text.insert(tk.END, 
            f"{'Comprimento da solução':<30} {metrics_astar.path_length:<20} {metrics_bfs.path_length:<20}\n")
        
        self.result_text.see(tk.END)  # Rola para mostrar resultados
    
    def clear_output(self):
        """Limpa a área de resultados"""
        self.result_text.delete(1.0, tk.END)

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal que inicia a aplicação"""
    root = tk.Tk()  # Cria a janela principal
    app = SearchGUI(root)  # Cria a aplicação
    root.mainloop()  # Inicia o loop de eventos da interface

# Ponto de entrada do programa
if __name__ == "__main__":
    main()