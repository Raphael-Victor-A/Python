from collections import deque

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

def show(state: tuple) -> None:
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

MOVES = {"up": -3, "down": 3, "left": -1, "right": 1}

def find_zero(state: tuple) -> int:
    return state.index(0)

def valid_moves(z: int) -> list:
    r, c = divmod(z, 3)
    moves = []
    if r > 0: moves.append("up")
    if r < 2: moves.append("down")
    if c > 0: moves.append("left")
    if c < 2: moves.append("right")
    return moves

def apply_moves(state: tuple, move: str) -> tuple:
    z = find_zero(state)
    nz = z + MOVES[move]
    s = list(state)
    s[z], s[nz] = s[nz], s[z]
    return tuple(s)

def bfs_metrics(start: tuple):
    frontier = deque([[start]])
    visited = {start}

    nodes_expanded = 0
    frontier_max = 1
    solution = None

    while frontier:
        path = frontier.popleft()
        state = path[-1]

        nodes_expanded += 1

        if state == GOAL:
            solution = path
            break

        z = find_zero(state)
        for m in valid_moves(z):
            new_state = apply_moves(state, m)
            if new_state not in visited:
                visited.add(new_state)
                frontier.append(path + [new_state])

        frontier_max = max(frontier_max, len(frontier))

    if solution is None:
        return None, {
            "nodes_expanded": nodes_expanded,
            "frontier_max": frontier_max,
            "solution_len": None
        }

    return solution, {
        "nodes_expanded": nodes_expanded,
        "frontier_max": frontier_max,
        "solution_len": len(solution) - 1
    }

start = (0, 6, 7,
         8, 5, 2,
         1, 3, 4)

print("Estado inicial:")
show(start)

solution, metrics = bfs_metrics(start)

if solution is None:
    print("Nenhuma solução encontrada.")
else:
    print(f"Solução encontrada em {metrics['solution_len']} passo(s).")
    print(f"Nós expandidos: {metrics['nodes_expanded']}")
    print(f"Tamanho máximo da fronteira: {metrics['frontier_max']}")
    print("\nReproduzindo caminho:")
    for st in solution:
        show(st)
