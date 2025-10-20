import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from queue import Queue, PriorityQueue
import time
import tracemalloc
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from copy import deepcopy
import heapq

@dataclass
class SearchMetrics:
    """Métricas de desempenho da busca"""
    execution_time: float
    memory_used: float
    nodes_expanded: int
    path_length: int
    solution_found: bool

class PuzzleState:
    """Estado do 8-Puzzle"""
    def __init__(self, board: List[List[int]], parent=None, move=""):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = 0 if parent is None else parent.g + 1
        self.h = self.calculate_heuristic()
        self.f = self.g + self.h
    
    def calculate_heuristic(self) -> int:
        """Heurística de distância Manhattan"""
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    target_row = (value - 1) // 3
                    target_col = (value - 1) % 3
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance
    
    def get_blank_position(self) -> Tuple[int, int]:
        """Encontra a posição do espaço vazio (0)"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1
    
    def get_neighbors(self) -> List['PuzzleState']:
        """Gera estados vizinhos válidos"""
        neighbors = []
        blank_row, blank_col = self.get_blank_position()
        
        # Movimentos possíveis: cima, baixo, esquerda, direita
        moves = [
            (-1, 0, "Cima"),
            (1, 0, "Baixo"),
            (0, -1, "Esquerda"),
            (0, 1, "Direita")
        ]
        
        for dr, dc, move_name in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = [row[:] for row in self.board]
                new_board[blank_row][blank_col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[blank_row][blank_col]
                neighbors.append(PuzzleState(new_board, self, move_name))
        
        return neighbors
    
    def is_goal(self) -> bool:
        """Verifica se é o estado objetivo"""
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal
    
    def __hash__(self):
        return hash(str(self.board))
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __str__(self):
        return '\n'.join([' '.join([str(cell) if cell != 0 else '_' for cell in row]) 
                         for row in self.board])

class MissionaryState:
    """Estado do problema dos Missionários e Canibais"""
    def __init__(self, left_m: int, left_c: int, boat_left: bool, parent=None, move=""):
        self.left_m = left_m  # Missionários à esquerda
        self.left_c = left_c  # Canibais à esquerda
        self.boat_left = boat_left  # Barco à esquerda
        self.parent = parent
        self.move = move
        self.g = 0 if parent is None else parent.g + 1
        self.h = self.calculate_heuristic()
        self.f = self.g + self.h
    
    def calculate_heuristic(self) -> int:
        """Heurística: número de pessoas na margem esquerda"""
        return self.left_m + self.left_c
    
    def is_valid(self) -> bool:
        """Verifica se o estado é válido"""
        right_m = 3 - self.left_m
        right_c = 3 - self.left_c
        
        # Verifica limites
        if self.left_m < 0 or self.left_c < 0 or right_m < 0 or right_c < 0:
            return False
        
        # Verifica se canibais não superam missionários em qualquer margem
        if self.left_m > 0 and self.left_m < self.left_c:
            return False
        if right_m > 0 and right_m < right_c:
            return False
        
        return True
    
    def get_neighbors(self) -> List['MissionaryState']:
        """Gera estados vizinhos válidos"""
        neighbors = []
        
        # Possíveis movimentos: (missionários, canibais)
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        for m, c in moves:
            if self.boat_left:
                # Barco vai para direita
                new_state = MissionaryState(
                    self.left_m - m, self.left_c - c, False, 
                    self, f"{m}M {c}C →"
                )
            else:
                # Barco volta para esquerda
                new_state = MissionaryState(
                    self.left_m + m, self.left_c + c, True, 
                    self, f"{m}M {c}C ←"
                )
            
            if new_state.is_valid():
                neighbors.append(new_state)
        
        return neighbors
    
    def is_goal(self) -> bool:
        """Verifica se todos estão na margem direita"""
        return self.left_m == 0 and self.left_c == 0
    
    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat_left))
    
    def __eq__(self, other):
        return (self.left_m == other.left_m and 
                self.left_c == other.left_c and 
                self.boat_left == other.boat_left)
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __str__(self):
        right_m = 3 - self.left_m
        right_c = 3 - self.left_c
        boat = "🚤" if self.boat_left else "  "
        return f"Esq: {self.left_m}M {self.left_c}C {boat} | Dir: {right_m}M {right_c}C"

class SearchAlgorithms:
    """Implementação dos algoritmos de busca"""
    
    @staticmethod
    def bfs(initial_state) -> Tuple[Optional[List], SearchMetrics]:
        """Busca em Largura (BFS)"""
        tracemalloc.start()
        start_time = time.time()
        
        queue = Queue()
        queue.put(initial_state)
        visited = {initial_state}
        nodes_expanded = 0
        
        while not queue.empty():
            current = queue.get()
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
            
            for neighbor in current.get_neighbors():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put(neighbor)
        
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
        """Busca A*"""
        tracemalloc.start()
        start_time = time.time()
        
        open_set = []
        heapq.heappush(open_set, (initial_state.f, id(initial_state), initial_state))
        visited = set()
        nodes_expanded = 0
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
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
            
            for neighbor in current.get_neighbors():
                if neighbor not in visited:
                    heapq.heappush(open_set, (neighbor.f, id(neighbor), neighbor))
        
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
        """Reconstrói o caminho da solução"""
        path = []
        current = state
        while current is not None:
            path.append(current)
            current = current.parent
        return list(reversed(path))

class SearchGUI:
    """Interface Gráfica Principal"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Busca em Espaço de Estados")
        self.root.geometry("900x700")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface"""
        
        # Frame de seleção
        select_frame = ttk.LabelFrame(self.root, text="Configuração", padding=10)
        select_frame.pack(fill="x", padx=10, pady=5)
        
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
        
        # Frame de entrada (8-Puzzle)
        self.puzzle_frame = ttk.LabelFrame(self.root, text="Estado Inicial do 8-Puzzle", padding=10)
        self.puzzle_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.puzzle_frame, 
                 text="Digite os números de 0-8 (0 = espaço vazio):").pack()
        
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
        
        # Preencher valores padrão
        default_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        for i in range(3):
            for j in range(3):
                self.puzzle_entries[i][j].insert(0, str(default_puzzle[i][j]))
        
        # Botões
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Executar Busca", 
                  command=self.execute_search).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Comparar Algoritmos", 
                  command=self.compare_algorithms).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", 
                  command=self.clear_output).pack(side="left", padx=5)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=25, width=100)
        self.result_text.pack(fill="both", expand=True)
    
    def get_puzzle_state(self) -> Optional[PuzzleState]:
        """Obtém o estado inicial do puzzle"""
        try:
            board = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = int(self.puzzle_entries[i][j].get())
                    if value < 0 or value > 8:
                        raise ValueError
                    row.append(value)
                board.append(row)
            
            # Verificar se todos os números de 0-8 estão presentes
            flat = [num for row in board for num in row]
            if sorted(flat) != list(range(9)):
                messagebox.showerror("Erro", "Use todos os números de 0 a 8 exatamente uma vez!")
                return None
            
            return PuzzleState(board)
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números de 0 a 8!")
            return None
    
    def execute_search(self):
        """Executa a busca selecionada"""
        problem = self.problem_var.get()
        algorithm = self.algorithm_var.get()
        
        # Obter estado inicial
        if problem == "8-Puzzle":
            initial_state = self.get_puzzle_state()
            if initial_state is None:
                return
        else:  # Missionários e Canibais
            initial_state = MissionaryState(3, 3, True)
        
        # Executar busca
        self.result_text.insert(tk.END, f"\n{'='*80}\n")
        self.result_text.insert(tk.END, f"Problema: {problem}\n")
        self.result_text.insert(tk.END, f"Algoritmo: {algorithm}\n")
        self.result_text.insert(tk.END, f"{'='*80}\n\n")
        
        if algorithm == "A*":
            path, metrics = SearchAlgorithms.a_star(initial_state)
        else:
            path, metrics = SearchAlgorithms.bfs(initial_state)
        
        self.display_results(path, metrics, problem)
        self.result_text.see(tk.END)
    
    def display_results(self, path, metrics: SearchMetrics, problem: str):
        """Exibe os resultados da busca"""
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
                if state.move:
                    self.result_text.insert(tk.END, f" [{state.move}]")
                self.result_text.insert(tk.END, f"\n{state}\n")
        else:
            self.result_text.insert(tk.END, "Nenhuma solução encontrada!\n")
    
    def compare_algorithms(self):
        """Compara os dois algoritmos"""
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
        
        # Executar A*
        self.result_text.insert(tk.END, "Executando A*...\n")
        path_astar, metrics_astar = SearchAlgorithms.a_star(deepcopy(initial_state))
        
        # Executar BFS
        self.result_text.insert(tk.END, "Executando BFS...\n\n")
        path_bfs, metrics_bfs = SearchAlgorithms.bfs(deepcopy(initial_state))
        
        # Exibir comparação
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
        
        self.result_text.see(tk.END)
    
    def clear_output(self):
        """Limpa a área de resultados"""
        self.result_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = SearchGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()