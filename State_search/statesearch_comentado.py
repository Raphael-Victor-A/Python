import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from queue import Queue, PriorityQueue
import time
import tracemalloc
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from copy import deepcopy
import heapq
import threading

# =============================================================================
# ESTRUTURAS DE DADOS E CLASSES BASE
# =============================================================================

@dataclass
class SearchMetrics:
    """Métricas de desempenho da busca"""
    execution_time: float
    memory_used: float
    nodes_expanded: int
    path_length: int
    solution_found: bool
    cancelled: bool = False

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
        """Encontra a posição do espaço vazio"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def get_neighbors(self) -> List['PuzzleState']:
        """Gera estados vizinhos válidos"""
        neighbors = []
        blank_row, blank_col = self.get_blank_position()
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
        return '\n'.join([' '.join([str(cell) if cell != 0 else '_' for cell in row]) for row in self.board])

class MissionaryState:
    """Estado do problema dos Missionários e Canibais"""
    def __init__(self, left_m: int, left_c: int, boat_left: bool, parent=None, move=""):
        self.left_m = left_m
        self.left_c = left_c
        self.boat_left = boat_left
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
        
        if self.left_m < 0 or self.left_c < 0 or right_m < 0 or right_c < 0:
            return False
        if self.left_m > 0 and self.left_m < self.left_c:
            return False
        if right_m > 0 and right_m < right_c:
            return False
        return True

    def get_neighbors(self) -> List['MissionaryState']:
        """Gera estados vizinhos válidos"""
        neighbors = []
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        for m, c in moves:
            if self.boat_left:
                new_state = MissionaryState(
                    self.left_m - m, self.left_c - c, False, self, f"{m}M {c}C →"
                )
            else:
                new_state = MissionaryState(
                    self.left_m + m, self.left_c + c, True, self, f"{m}M {c}C ←"
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
        return (self.left_m == other.left_m and self.left_c == other.left_c and self.boat_left == other.boat_left)

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        right_m = 3 - self.left_m
        right_c = 3 - self.left_c
        boat = "🚤" if self.boat_left else "    "
        return f"Esq: {self.left_m}M {self.left_c}C {boat} | Dir: {right_m}M {right_c}C"

# =============================================================================
# ALGORITMOS DE BUSCA COM CANCELAMENTO
# =============================================================================

class SearchAlgorithms:
    """Implementação dos algoritmos de busca com suporte a cancelamento"""

    @staticmethod
    def bfs(initial_state, max_nodes=100000, cancel_flag=None, progress_callback=None) -> Tuple[Optional[List], SearchMetrics]:
        """Busca em Largura com limite de nós e cancelamento"""
        tracemalloc.start()
        start_time = time.time()
        queue = Queue()
        queue.put(initial_state)
        visited = {initial_state}
        nodes_expanded = 0

        while not queue.empty():
            # Verifica cancelamento
            if cancel_flag and cancel_flag.is_set():
                execution_time = time.time() - start_time
                memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
                tracemalloc.stop()
                return None, SearchMetrics(
                    execution_time=execution_time,
                    memory_used=memory_used,
                    nodes_expanded=nodes_expanded,
                    path_length=0,
                    solution_found=False,
                    cancelled=True
                )

            # Verifica limite de nós
            if nodes_expanded >= max_nodes:
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

            current = queue.get()
            nodes_expanded += 1

            # Atualiza progresso a cada 100 nós
            if progress_callback and nodes_expanded % 100 == 0:
                progress_callback(nodes_expanded, max_nodes)

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
    def a_star(initial_state, max_nodes=100000, cancel_flag=None, progress_callback=None) -> Tuple[Optional[List], SearchMetrics]:
        """Busca A* com limite de nós e cancelamento"""
        tracemalloc.start()
        start_time = time.time()
        open_set = []
        heapq.heappush(open_set, (initial_state.f, id(initial_state), initial_state))
        visited = set()
        nodes_expanded = 0

        while open_set:
            # Verifica cancelamento
            if cancel_flag and cancel_flag.is_set():
                execution_time = time.time() - start_time
                memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
                tracemalloc.stop()
                return None, SearchMetrics(
                    execution_time=execution_time,
                    memory_used=memory_used,
                    nodes_expanded=nodes_expanded,
                    path_length=0,
                    solution_found=False,
                    cancelled=True
                )

            # Verifica limite de nós
            if nodes_expanded >= max_nodes:
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

            _, _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            nodes_expanded += 1

            # Atualiza progresso a cada 100 nós
            if progress_callback and nodes_expanded % 100 == 0:
                progress_callback(nodes_expanded, max_nodes)

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

# =============================================================================
# INTERFACE GRÁFICA COM BARRA DE PROGRESSO
# =============================================================================

class SearchGUI:
    """Interface Gráfica com barra de progresso e cancelamento"""

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Busca em Espaço de Estados")
        self.root.geometry("900x750")
        self.cancel_flag = threading.Event()
        self.search_thread = None
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface"""
        # SEÇÃO 1: CONFIGURAÇÃO
        select_frame = ttk.LabelFrame(self.root, text="Configuração", padding=10)
        select_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(select_frame, text="Problema:").grid(row=0, column=0, sticky="w", padx=5)
        self.problem_var = tk.StringVar(value="8-Puzzle")
        problem_combo = ttk.Combobox(select_frame, textvariable=self.problem_var, 
                                    values=["8-Puzzle", "Missionários e Canibais"], 
                                    state="readonly", width=25)
        problem_combo.grid(row=0, column=1, padx=5)
        problem_combo.bind('<<ComboboxSelected>>', self.on_problem_change)

        ttk.Label(select_frame, text="Algoritmo:").grid(row=0, column=2, sticky="w", padx=5)
        self.algorithm_var = tk.StringVar(value="A*")
        algorithm_combo = ttk.Combobox(select_frame, textvariable=self.algorithm_var, 
                                      values=["A*", "Busca em Largura (BFS)"], 
                                      state="readonly", width=25)
        algorithm_combo.grid(row=0, column=3, padx=5)

        # Limite de nós
        ttk.Label(select_frame, text="Limite de nós:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.max_nodes_var = tk.StringVar(value="50000")
        max_nodes_entry = ttk.Entry(select_frame, textvariable=self.max_nodes_var, width=15)
        max_nodes_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(select_frame, text="(Reduzir para buscas mais rápidas)", font=("Arial", 8)).grid(row=1, column=2, columnspan=2, sticky="w", padx=5)

        # SEÇÃO 2: ENTRADA DO 8-PUZZEL (sempre visível)
        self.puzzle_frame = ttk.LabelFrame(self.root, text="Estado Inicial do 8-Puzzle", padding=10)
        self.puzzle_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.puzzle_frame, text="Digite os números de 0-8 (0 = espaço vazio):").pack()
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
        
        default_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
        for i in range(3):
            for j in range(3):
                self.puzzle_entries[i][j].insert(0, str(default_puzzle[i][j]))

        # SEÇÃO 3: BARRA DE PROGRESSO
        progress_frame = ttk.LabelFrame(self.root, text="Progresso da Busca", padding=10)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Aguardando execução...")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(pady=5)

        # SEÇÃO 4: BOTÕES DE CONTROLE
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.execute_btn = ttk.Button(button_frame, text="Executar Busca", command=self.execute_search)
        self.execute_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancelar", command=self.cancel_search, state="disabled")
        self.cancel_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Comparar Algoritmos", command=self.compare_algorithms).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar", command=self.clear_output).pack(side="left", padx=5)

        # SEÇÃO 5: ÁREA DE RESULTADOS
        result_frame = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=20, width=100, state="normal")
        self.result_text.pack(fill="both", expand=True)
        
        # Torna a área de resultados somente leitura
        self.result_text.config(state="disabled")

        # Inicializa o estado dos campos
        self.on_problem_change()

    def on_problem_change(self, event=None):
        """Ativa/desativa os campos do 8-Puzzle baseado no problema selecionado"""
        if self.problem_var.get() == "8-Puzzle":
            # Ativa todos os campos do 8-Puzzle
            for i in range(3):
                for j in range(3):
                    self.puzzle_entries[i][j].config(state="normal")
            self.puzzle_frame.configure(text="Estado Inicial do 8-Puzzle (Ativo)")
        else:
            # Desativa todos os campos do 8-Puzzle
            for i in range(3):
                for j in range(3):
                    self.puzzle_entries[i][j].config(state="disabled")
            self.puzzle_frame.configure(text="Estado Inicial do 8-Puzzle (Inativo - Selecione 8-Puzzle para usar)")

    def get_puzzle_state(self) -> Optional[PuzzleState]:
        """Obtém o estado inicial do puzzle"""
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
            
            flat = [num for row in board for num in row]
            if sorted(flat) != list(range(9)):
                messagebox.showerror("Erro", "Use todos os números de 0 a 8 exatamente uma vez!")
                return None
            
            return PuzzleState(board)
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números de 0 a 8!")
            return None

    def update_progress(self, current, maximum):
        """Atualiza a barra de progresso"""
        percentage = min(100, (current / maximum) * 100)
        self.progress_bar['value'] = percentage
        self.progress_label.config(text=f"Processando: {current}/{maximum} nós expandidos ({percentage:.1f}%)")
        self.root.update_idletasks()

    def execute_search(self):
        """Executa a busca em thread separada"""
        if self.search_thread and self.search_thread.is_alive():
            messagebox.showwarning("Aviso", "Uma busca já está em execução!")
            return

        problem = self.problem_var.get()
        algorithm = self.algorithm_var.get()
        
        try:
            max_nodes = int(self.max_nodes_var.get())
            if max_nodes <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Digite um limite de nós válido (número positivo)!")
            return

        if problem == "8-Puzzle":
            initial_state = self.get_puzzle_state()
            if initial_state is None:
                return
        else:
            initial_state = MissionaryState(3, 3, True)

        # Prepara interface para execução
        self.execute_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.cancel_flag.clear()
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Iniciando busca...")

        # Executa em thread separada
        self.search_thread = threading.Thread(
            target=self._run_search,
            args=(initial_state, algorithm, max_nodes, problem)
        )
        self.search_thread.start()

    def _run_search(self, initial_state, algorithm, max_nodes, problem):
        """Executa a busca (rodando em thread)"""
        # Habilita temporariamente para escrever
        self.root.after(0, self._enable_result_text)
        self.root.after(0, self._append_result, f"\n{'='*80}\n")
        self.root.after(0, self._append_result, f"Problema: {problem}\n")
        self.root.after(0, self._append_result, f"Algoritmo: {algorithm}\n")
        self.root.after(0, self._append_result, f"Limite de nós: {max_nodes}\n")
        self.root.after(0, self._append_result, f"{'='*80}\n\n")

        if algorithm == "A*":
            path, metrics = SearchAlgorithms.a_star(
                initial_state, max_nodes, self.cancel_flag, self.update_progress
            )
        else:
            path, metrics = SearchAlgorithms.bfs(
                initial_state, max_nodes, self.cancel_flag, self.update_progress
            )

        # Atualiza interface no thread principal
        self.root.after(0, self._finish_search, path, metrics, problem)

    def _enable_result_text(self):
        """Habilita temporariamente a área de resultados para escrita"""
        self.result_text.config(state="normal")

    def _disable_result_text(self):
        """Desabilita a área de resultados para escrita"""
        self.result_text.config(state="disabled")

    def _append_result(self, text):
        """Adiciona texto à área de resultados"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)

    def _finish_search(self, path, metrics, problem):
        """Finaliza a busca e exibe resultados"""
        self.display_results(path, metrics, problem)
        self.result_text.see(tk.END)
        self.execute_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        
        # Desabilita a área de resultados após escrever
        self.result_text.config(state="disabled")
        
        if metrics.cancelled:
            self.progress_label.config(text="Busca cancelada pelo usuário")
        elif metrics.solution_found:
            self.progress_label.config(text="✓ Solução encontrada!")
            self.progress_bar['value'] = 100
        else:
            self.progress_label.config(text="✗ Nenhuma solução encontrada no limite de nós")

    def cancel_search(self):
        """Cancela a busca em execução"""
        self.cancel_flag.set()
        self.progress_label.config(text="Cancelando busca...")

    def display_results(self, path, metrics: SearchMetrics, problem: str):
        """Exibe os resultados da busca"""
        self._append_result("MÉTRICAS DE DESEMPENHO:\n")
        
        if metrics.cancelled:
            self._append_result(" Status: CANCELADO PELO USUÁRIO\n")
        else:
            self._append_result(f" Solução encontrada: {'Sim' if metrics.solution_found else 'Não'}\n")
            self._append_result(f" Tempo de execução: {metrics.execution_time:.4f} segundos\n")
            self._append_result(f" Memória utilizada: {metrics.memory_used:.2f} MB\n")
            self._append_result(f" Nós expandidos: {metrics.nodes_expanded}\n")
            self._append_result(f" Comprimento da solução: {metrics.path_length}\n\n")

        if path:
            self._append_result("CAMINHO DA SOLUÇÃO:\n")
            for i, state in enumerate(path):
                self._append_result(f"\nPasso {i}:")
                if state.move:
                    self._append_result(f" [{state.move}]")
                self._append_result(f"\n{state}\n")
        elif not metrics.cancelled:
            self._append_result("Nenhuma solução encontrada no limite de nós especificado!\n")
            self._append_result("Dica: Tente aumentar o limite ou usar o algoritmo A*\n")

    def compare_algorithms(self):
        """Compara os dois algoritmos"""
        problem = self.problem_var.get()
        try:
            max_nodes = int(self.max_nodes_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um limite de nós válido!")
            return

        if problem == "8-Puzzle":
            initial_state = self.get_puzzle_state()
            if initial_state is None:
                return
        else:
            initial_state = MissionaryState(3, 3, True)

        # Habilita temporariamente para escrever
        self.result_text.config(state="normal")
        self._append_result(f"\n{'='*80}\n")
        self._append_result(f"COMPARAÇÃO DE ALGORITMOS - {problem}\n")
        self._append_result(f"Limite de nós: {max_nodes}\n")
        self._append_result(f"{'='*80}\n\n")

        self.progress_label.config(text="Executando A*...")
        path_astar, metrics_astar = SearchAlgorithms.a_star(deepcopy(initial_state), max_nodes)
        
        self.progress_label.config(text="Executando BFS...")
        path_bfs, metrics_bfs = SearchAlgorithms.bfs(deepcopy(initial_state), max_nodes)
        
        self.progress_label.config(text="Comparação concluída")

        self._append_result(f"{'Métrica':<30} {'A*':<20} {'BFS':<20}\n")
        self._append_result(f"{'-'*70}\n")
        self._append_result(f"{'Solução encontrada':<30} {'Sim' if metrics_astar.solution_found else 'Não':<20} {'Sim' if metrics_bfs.solution_found else 'Não':<20}\n")
        self._append_result(f"{'Tempo (s)':<30} {metrics_astar.execution_time:<20.4f} {metrics_bfs.execution_time:<20.4f}\n")
        self._append_result(f"{'Memória (MB)':<30} {metrics_astar.memory_used:<20.2f} {metrics_bfs.memory_used:<20.2f}\n")
        self._append_result(f"{'Nós expandidos':<30} {metrics_astar.nodes_expanded:<20} {metrics_bfs.nodes_expanded:<20}\n")
        self._append_result(f"{'Comprimento da solução':<30} {metrics_astar.path_length:<20} {metrics_bfs.path_length:<20}\n")
        
        # Desabilita a área de resultados após escrever
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)

    def clear_output(self):
        """Limpa a área de resultados"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Aguardando execução...")

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal"""
    root = tk.Tk()
    app = SearchGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()