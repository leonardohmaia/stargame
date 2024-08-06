import math
import heapq

class Node:
    def __init__(self, x, y, walkable=True, fruit=False, enemy=False):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.fruit = fruit
        self.enemy = enemy
        self.g = float('inf')  # Inicialize g com infinito
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"({self.x}, {self.y})"

def heuristic(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def get_neighbors(node, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in directions:
        nx, ny = node.x + d[0], node.y + d[1]
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neighbors.append(grid[nx][ny])
    return neighbors

def a_star(start, goal, grid):
    open_set = []
    start.g = 0  # Inicialize g do nó inicial com 0
    heapq.heappush(open_set, start)
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = current.parent
            return path[::-1]

        closed_set.add(current)

        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set or not neighbor.walkable:
                continue

            tentative_g = current.g + 1

            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, neighbor)

    return None

def move_enemy(enemy, grid):
    directions = [(1, 0), (-1, 0)]
    for d in directions:
        nx, ny = enemy.x + d[0], enemy.y + d[1]
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny].walkable:
            grid[enemy.x][enemy.y].enemy = False
            enemy.x, enemy.y = nx, ny
            grid[enemy.x][enemy.y].enemy = True
            break

def print_grid(grid, start, goal):
    for row in grid:
        for node in row:
            if node == start:
                print("S", end=" ")
            elif node == goal:
                print("G", end=" ")
            elif node.enemy:
                print("E", end=" ")
            elif node.fruit:
                print("F", end=" ")
            elif not node.walkable:
                print("X", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

def main():
    grid = [
        [Node(0, 0), Node(0, 1), Node(0, 2), Node(0, 3)],
        [Node(1, 0, walkable=False), Node(1, 1), Node(1, 2, walkable=False), Node(1, 3)],
        [Node(2, 0), Node(2, 1, fruit=True), Node(2, 2), Node(2, 3)],
        [Node(3, 0), Node(3, 1), Node(3, 2), Node(3, 3)],
        [Node(4, 0, walkable=False), Node(4, 1), Node(4, 2), Node(4, 3, walkable=False)],
        [Node(5, 0), Node(5, 1, walkable=False), Node(5, 2), Node(5, 3)],
        [Node(6, 0), Node(6, 1), Node(6, 2), Node(6, 3)],
        [Node(7, 0), Node(7, 1), Node(7, 2), Node(7, 3)],
    ]

    start = grid[2][1]
    goal = grid[4][3]
    enemy = grid[2][2]
    enemy.enemy = True

    print("Initial grid:")
    print_grid(grid, start, goal)

    path = a_star(start, goal, grid)

    if path:
        for step in path:
            print(f"Step: {step}")
            start = step  # Move the start to the next step
            if step.fruit:
                start.fruit = True
            if step.enemy:
                print("Game Over! Hit an enemy.")
                break
            move_enemy(enemy, grid)
            print_grid(grid, start, goal)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
