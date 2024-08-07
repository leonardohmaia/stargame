import pygame
import math
import heapq

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
width, height = 600, 600
rows, cols = 20, 20
square_size = width // cols

# Cores
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "gray": (128, 128, 128)
}

# Tela do jogo
screen = pygame.display.set_mode((width, height))

# Posições iniciais
start = (0, 0)
goal = (cols-1, rows-1)
barriers = [
    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 2), (3, 1), (4, 2), (5, 3), (6, 4)
]
power_fruits = [(4, 4)]
enemy_position = [8, 8]  # Posições do inimigo como lista para permitir modificações

# Função de heurística (distância Euclidiana)
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Algoritmo A* para encontrar o caminho
def a_star(start, goal, barriers, power_fruits, has_power_fruit):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows:
                if neighbor in barriers and not has_power_fruit:
                    continue  # Não pode passar por barreiras sem a fruta

                tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)
                if neighbor in power_fruits:
                    has_power_fruit = True

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []

# Desenha a grade do jogo
def draw_grid():
    for x in range(0, width, square_size):
        for y in range(0, height, square_size):
            rect = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(screen, colors["black"], rect, 1)

# Desenha os elementos do jogo
def draw_elements():
    for barrier in barriers:
        rect = pygame.Rect(barrier[0] * square_size, barrier[1] * square_size, square_size, square_size)
        pygame.draw.rect(screen, colors["red"], rect)

    for fruit in power_fruits:
        rect = pygame.Rect(fruit[0] * square_size, fruit[1] * square_size, square_size, square_size)
        pygame.draw.rect(screen, colors["yellow"], rect)

    pygame.draw.rect(screen, colors["blue"], (start[0] * square_size, start[1] * square_size, square_size, square_size))
    pygame.draw.rect(screen, colors["green"], (goal[0] * square_size, goal[1] * square_size, square_size, square_size))
    pygame.draw.rect(screen, colors["gray"], (enemy_position[0] * square_size, enemy_position[1] * square_size, square_size, square_size))

# Atualiza a posição do inimigo
def update_enemy_position():
    global enemy_position
    # Movimenta o inimigo para cima e para baixo
    if enemy_position[1] % 2 == 0:
        enemy_position[1] = (enemy_position[1] + 1) % rows
    else:
        enemy_position[1] = (enemy_position[1] - 1) % rows

# Função principal do jogo
def main():
    running = True
    has_power_fruit = False
    path = a_star(start, goal, barriers, power_fruits, has_power_fruit)
    path_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza a posição do inimigo
        update_enemy_position()

        # Atualiza a posição do caminho
        if path_index < len(path):
            current_pos = path[path_index]
            if current_pos in power_fruits:
                has_power_fruit = True
            path_index += 1

        # Verifica se o caminho foi encontrado
        if not path:
            print("Nenhum caminho encontrado!")
            running = False
            continue

        screen.fill(colors["white"])
        draw_grid()
        draw_elements()

        if path_index < len(path):
            pygame.draw.rect(screen, colors["blue"], (path[path_index][0] * square_size, path[path_index][1] * square_size, square_size, square_size))
        
        pygame.display.flip()
        pygame.time.delay(500)  # Atraso para o movimento do inimigo

    pygame.quit()

if __name__ == "__main__":
    main()
