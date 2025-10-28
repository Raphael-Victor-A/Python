# --------------------------
# 8-Puzzle: BFS, DFS e IDS
# --------------------------
import time
from collections import deque

# Estado objetivo
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Funções auxiliares
def valid_moves(state):
    """Retorna os movimentos possíveis: 'up', 'down', 'left', 'right'"""
    moves = []
    idx = state.index(0)
    row, col = idx // 3, idx % 3
    if row > 0: moves.append('up')
    if row < 2: moves.append('down')
    if col > 0: moves.append('left')
    if col < 2: moves.append('right')
    return moves

def apply_move(state, move):
    """Aplica movimento e retorna novo estado"""
    idx = state.index(0)
    new_state = list(state)
    if move == 'up': swap_idx = idx - 3
    elif move == 'down': swap_idx = idx + 3
    elif move == 'left': swap_idx = idx - 1
    elif move == 'right': swap_idx = idx + 1
    else: return None
    new_state[idx], new_state[swap_idx] = new_state[swap_idx], new_state[idx]
    return tuple(new_state)

def reconstruct_path(parent, start, goal):
    """Reconstrói o caminho de start até goal"""
    path = []
    state = goal
    while state is not None:
        path.append(state)
        state = parent[state]
    path.reverse()
    return path

# --------------------------
# BFS
# --------------------------
def bfs_with_metrics(start, goal=GOAL):
    start_time = time.time()
    frontier = deque([start])
    parent = {start: None}
    expanded = 0
    max_frontier = 1

    while frontier:
        state = frontier.popleft()
        expanded += 1

        if state == goal:
            elapsed = time.time() - start_time
            path = reconstruct_path(parent, start, goal)
            return {
                "path": path,
                "depth": len(path)-1,
                "expanded": expanded,
                "max_frontier": max_frontier,
                "time": elapsed
            }

        for move in valid_moves(state):
            child = apply_move(state, move)
            if child and child not in parent:
                parent[child] = state
                frontier.append(child)

        if len(frontier) > max_frontier:
            max_frontier = len(frontier)

    return None

# --------------------------
# DFS
# --------------------------
def dfs_with_metrics(start, goal=GOAL, depth_limit=50):
    start_time = time.time()
    stack = [(start, 0)]
    parent = {start: None}
    expanded = 0
    max_frontier = 1

    while stack:
        state, depth = stack.pop()
        expanded += 1

        if state == goal:
            elapsed = time.time() - start_time
            path = reconstruct_path(parent, start, goal)
            return {
                "path": path,
                "depth": depth,
                "expanded": expanded,
                "max_frontier": max_frontier,
                "time": elapsed
            }

        if depth < depth_limit:
            for move in valid_moves(state):
                child = apply_move(state, move)
                if child and child not in parent:
                    parent[child] = state
                    stack.append((child, depth + 1))
            if len(stack) > max_frontier:
                max_frontier = len(stack)

    return None

# --------------------------
# IDS
# --------------------------
def ids_with_metrics(start, goal=GOAL, max_depth=50):
    start_time_total = time.time()
    total_expanded = 0
    max_frontier_overall = 0
    final_parent = None
    final_depth = None
    
    for limit in range(max_depth + 1):
        stack = [(start, 0)]
        parent = {start: None}
        expanded = 0
        frontier_max = 1

        while stack:
            state, depth = stack.pop()
            expanded += 1

            if state == goal:
                final_parent = parent.copy()
                final_depth = depth
                break

            if depth < limit:
                for move in valid_moves(state):
                    child = apply_move(state, move)
                    if child and child not in parent:
                        parent[child] = state
                        stack.append((child, depth + 1))
                if len(stack) > frontier_max:
                    frontier_max = len(stack)

        total_expanded += expanded
        if frontier_max > max_frontier_overall:
            max_frontier_overall = frontier_max

        if final_parent is not None:
            elapsed_total = time.time() - start_time_total
            path = reconstruct_path(final_parent, start, goal)
            return {
                "path": path,
                "depth": final_depth,
                "expanded": total_expanded,
                "max_frontier": max_frontier_overall,
                "time": elapsed_total,
                "ids_last_limit": limit
            }

    return None

# --------------------------
# Casos de teste
# --------------------------
cases = [
    ("Fácil", (1, 2, 3, 4, 5, 6, 7, 0, 8)),
    ("Médio", (1, 2, 3, 4, 5, 6, 0, 7, 8)),
    ("Desafiador", (1, 2, 3, 5, 0, 6, 4, 7, 8))
]

results = []
for name, start in cases:
    bfs_res = bfs_with_metrics(start)
    dfs_res = dfs_with_metrics(start)
    ids_res = ids_with_metrics(start)
    results.append((name, bfs_res, dfs_res, ids_res))

# --------------------------
# Impressão da tabela
# --------------------------
print(f"{'Caso':<12} | {'Algoritmo':<5} | {'Profundidade':<10} | {'Expandidos':<10} | {'Fronteira Máx':<14} | {'Tempo (s)':<8}")
print("-"*70)
for name, bfs_res, dfs_res, ids_res in results:
    for algo, res in zip(["BFS", "DFS", "IDS"], [bfs_res, dfs_res, ids_res]):
        print(f"{name:<12} | {algo:<5} | {res['depth']:<10} | {res['expanded']:<10} | {res['max_frontier']:<14} | {res['time']:<8.4f}")
