import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto con Enemigos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tamaño de las celdas
CELL_SIZE = 50

# Laberinto: 1 es pared, 0 es camino libre
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Posiciones del jugador (inicio) y meta (final)
start_pos = [1, 1]  # Posición inicial
end_pos = [8, 8]  # Posición final
player_pos = list(start_pos)

# Enemigos
enemies = [{'x': 3, 'y': 3}, {'x': 6, 'y': 5}]

# Reloj para controlar la velocidad
clock = pygame.time.Clock()

# Puntuación
score = 0
last_score_time = time.time()

# Control de velocidad de los enemigos
enemy_move_interval = 20  # Número de ciclos del juego antes de que un enemigo se mueva
enemy_move_counter = 0  # Contador de ciclos

# Función para dibujar el laberinto
def draw_maze():
    for row in range(len(laberinto)):
        for col in range(len(laberinto[row])):
            color = WHITE if laberinto[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE + 3, row * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6))

    # Dibujar el inicio (en verde)
    pygame.draw.rect(screen, GREEN, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dibujar el final (en rojo)
    pygame.draw.rect(screen, RED, (end_pos[1] * CELL_SIZE, end_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dibujar al jugador (círculo azul)
    pygame.draw.circle(screen, BLUE, (player_pos[1] * CELL_SIZE + CELL_SIZE // 2, player_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

    # Dibujar los enemigos (círculos amarillos)
    for enemy in enemies:
        pygame.draw.circle(screen, YELLOW, (enemy['x'] * CELL_SIZE + CELL_SIZE // 2, enemy['y'] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# Comprobar si el jugador ha llegado a la meta
def check_win():
    return player_pos == end_pos

# Mover enemigos hacia el jugador
def move_enemy(enemy):
    if player_pos[0] < enemy['y']:
        enemy['y'] -= 1
    elif player_pos[0] > enemy['y']:
        enemy['y'] += 1

    if player_pos[1] < enemy['x']:
        enemy['x'] -= 1
    elif player_pos[1] > enemy['x']:
        enemy['x'] += 1

# Comprobar si un enemigo ha alcanzado al jugador
def check_collision():
    for enemy in enemies:
        if enemy['x'] == player_pos[1] and enemy['y'] == player_pos[0]:
            return True
    return False

# Mostrar puntuación
def show_score():
    font = pygame.font.SysFont('Arial', 30)
    score_text = font.render(f'Puntuación: {score}', True, BLACK)
    screen.blit(score_text, (10, 10))

# Bucle principal
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_pos = [player_pos[0], player_pos[1] - 1]
        if laberinto[new_pos[0]][new_pos[1]] == 0:
            player_pos = new_pos
    if keys[pygame.K_RIGHT]:
        new_pos = [player_pos[0], player_pos[1] + 1]
        if laberinto[new_pos[0]][new_pos[1]] == 0:
            player_pos = new_pos
    if keys[pygame.K_UP]:
        new_pos = [player_pos[0] - 1, player_pos[1]]
        if laberinto[new_pos[0]][new_pos[1]] == 0:
            player_pos = new_pos
    if keys[pygame.K_DOWN]:
        new_pos = [player_pos[0] + 1, player_pos[1]]
        if laberinto[new_pos[0]][new_pos[1]] == 0:
            player_pos = new_pos

    # Mover enemigos cada cierto número de ciclos
    enemy_move_counter += 1
    if enemy_move_counter >= enemy_move_interval:
        for enemy in enemies:
            move_enemy(enemy)
        enemy_move_counter = 0  # Reiniciar el contador de movimientos de los enemigos

    # Comprobar colisión con enemigos
    if check_collision():
        print("¡Te atraparon! Game Over")
        running = False

    # Comprobar si se ha ganado
    if check_win():
        print("¡Ganaste!")
        running = False

    # Gestionar puntuación
    current_time = time.time()
    if current_time - last_score_time >= 20:
        score += 1
        last_score_time = current_time

    # Mostrar el laberinto, la puntuación y los enemigos
    draw_maze()
    show_score()

    pygame.display.flip()
    clock.tick(10)  # Reducir la velocidad de la actualización del juego

pygame.quit()
