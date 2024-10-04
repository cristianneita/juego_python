import pygame
import sys
import random

# Inicializar PyGame
pygame.init()

# Configuraciones básicas de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego con pygame")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MORADO = (143, 0, 255)
AMARILLO = (255, 255, 0)

# Configuración del jugador
player_width = 70
player_height = 70
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Enemigos
enemy_width = 50
enemy_height = 50
enemy_speed = 10
enemies = []
enemy_spawn_time = 500  # Enemigos aparecen cada 1000 ms (1 segundo)
last_enemy_spawn = 0

# Vidas y niveles
lives = 3
level = 1
max_levels = 3
level_duration = [30, 45, 60]  # Duración en segundos por nivel
level_start_time = 0

# Menú principal
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Inicia el juego al presionar 1
                    menu_running = False
                    game_loop(1)
                elif event.key == pygame.K_2:  # Inicia el juego al presionar 2
                    menu_running = False
                    game_loop(2)
                elif event.key == pygame.K_3:  # Inicia el juego al presionar 3
                    menu_running = False
                    game_loop(3)
                elif event.key == pygame.K_x: #Salir del juego
                    pygame.quit()
                    sys.exit()
        
        # Renderiza el título y las opciones del menú
        font = pygame.font.Font("Games.ttf", 74)  # Cargar la fuente personalizada
        font_small = pygame.font.Font("Game Plan.ttf", 35)  # Fuente pequeña para las opciones
        
        title = font.render("BIENVENIDO", True, WHITE)
        screen.blit(title, (200, 100))
        
        option1 = font_small.render("- Presiona 1 para el nivel 1", True, WHITE)
        screen.blit(option1, (150, 250))
        
        option2 = font_small.render("- Presiona 2 para el nivel 2", True, WHITE)
        screen.blit(option2, (150, 320))
        
        option2 = font_small.render("- Presiona 3 para el nivel 3", True, WHITE)
        screen.blit(option2, (150, 390))
        

        option3 = font_small.render("- Presiona x para salir", True, WHITE)
        screen.blit(option3, (150, 460))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

# Función para crear enemigos
def spawn_enemy():
    x_pos = random.randint(0, screen_width - enemy_width)
    enemies.append(pygame.Rect(x_pos, 0, enemy_width, enemy_height))

# Función principal del juego
def game_loop(selected_level):
    global player_x, lives, enemies, enemy_speed, last_enemy_spawn, level_start_time
    
    enemy_speed = 5 + (selected_level - 1) * 2  # Aumenta la velocidad de los enemigos por nivel
    level_start_time = pygame.time.get_ticks() // 1000  # Tiempo de inicio del nivel
    last_enemy_spawn = pygame.time.get_ticks()  # Inicializa el tiempo del último enemigo spawn
    enemies.clear()
    
    # Duración del nivel en segundos
    level_time = level_duration[selected_level - 1]
    
    running = True
    while running:
        current_time = pygame.time.get_ticks() // 1000  # Tiempo actual en segundos
        elapsed_time = current_time - level_start_time  # Tiempo transcurrido
        remaining_time = level_time - elapsed_time  # Tiempo restante
        
        # Comprobar si se acabó el tiempo
        if remaining_time <= 0:
            level_complete()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Spawnear enemigos
        if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
            spawn_enemy()
            last_enemy_spawn = pygame.time.get_ticks()

        # Mover enemigos
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > screen_height:
                enemies.remove(enemy)

        # Detección de colisiones
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy in enemies:
            if player_rect.colliderect(enemy) and selected_level == 1:
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    game_over()
            elif(player_rect.colliderect(enemy) and selected_level == 2):
                lives -= 2
                enemies.remove(enemy)
                if lives <= 0:
                    game_over()
            elif(player_rect.colliderect(enemy) and selected_level == 3):
                lives -= 3
                enemies.remove(enemy)
                if lives <= 0:
                    game_over()

        # Dibujar el jugador
        screen.fill(BLACK)  # Limpiar la pantalla
        pygame.draw.rect(screen, WHITE, player_rect)

        # Dibujar enemigos
        for enemy in enemies:
            if(selected_level == 1):
                pygame.draw.rect(screen, AMARILLO, enemy)
            elif(selected_level == 2):
                pygame.draw.rect(screen, MORADO, enemy)
            elif(selected_level == 3):
                pygame.draw.ellipse(screen, RED, enemy)

        #Mostrar nivel
        font_small = pygame.font.Font("Game Plan.ttf", 25)
        lives_text = font_small.render(f'Nivel: {selected_level}', True, WHITE)
        screen.blit(lives_text, (180, 10))

        # Mostrar vidas
        font_small = pygame.font.Font("Game Plan.ttf", 25)
        lives_text = font_small.render(f'Vidas: {lives}', True, WHITE)
        screen.blit(lives_text, (10, 10))

        # Mostrar tiempo restante
        time_text = font_small.render(f'Tiempo restante: {remaining_time}', True, WHITE)
        screen.blit(time_text, (screen_width - 250, 10))

        pygame.display.flip()
        pygame.time.delay(10)  # Controlar la velocidad de fotogramas

# Función para manejar el fin del juego
def game_over():
    global lives
    lives = 3
    while True:
        screen.fill(BLACK)  # Limpiar la pantalla
        font = pygame.font.Font("Games.ttf", 55)
        game_over_text = font.render("¡Perdiste!", True, WHITE)
        restart_text = font.render("Presiona R para reiniciar", True, WHITE)
        exit_text = font.render("Presiona X para salir", True, WHITE)
        
        # Dibujar el texto en la pantalla
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 20))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar el juego
                    main_menu()
                elif event.key == pygame.K_x:  # Salir del juego
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Actualiza la pantalla



# Función para manejar la finalización de un nivel
# Función para manejar la finalización de un nivel
def level_complete():
    global level
    while True:
        screen.fill(BLACK)  # Limpiar la pantalla
        font = pygame.font.Font("Games.ttf", 35)
        level_complete_text = font.render(f"Nivel {level} completado!", True, WHITE)
        next_level_text = font.render("Presiona N para continuar al siguiente nivel", True, WHITE)
        exit_text = font.render("Presiona X para salir", True, WHITE)
        
        # Dibujar el texto en la pantalla
        screen.blit(level_complete_text, (screen_width // 2 - level_complete_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(next_level_text, (screen_width // 2 - next_level_text.get_width() // 2, screen_height // 2 + 20))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height // 2 + 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Continuar al siguiente nivel
                    if level < max_levels:
                        level += 1
                        game_loop(level)
                    else:
                        print("¡Felicidades, has completado todos los niveles!")
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_x:  # Salir del juego
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  # Actualiza la pantalla


if __name__ == "__main__":
    main_menu()
