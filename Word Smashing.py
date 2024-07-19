import pygame
import random
import sys

pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Snake settings
SNAKE_SIZE = 20

# Font
FONT = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)

# Obstacles
OBSTACLES = []

# Game modes
MODES = {
    'easy': {'speed': 10},
    'medium': {'speed': 20},
    'hard': {'speed': 30}
}

current_mode = 'easy'
current_obstacle_mode = None

def draw_welcome_screen():
    WINDOW.fill(BLACK)
    display_message("Welcome to Snake Game", BLUE, -200)
    display_message("Select Difficulty:", WHITE, -150)
    display_message("1. Easy", GREEN, -100)
    display_message("2. Medium", GREEN, -50)
    display_message("3. Hard", GREEN, 0)
    display_message("Select Obstacle Mode:", WHITE, 50)
    display_message("A. Plain", GREEN, 100)
    display_message("B. Wall", GREEN, 150)
    display_message("C. Dotted", GREEN, 200)
    display_message("D. Grid", GREEN, 250)
    display_message("Press Q to Quit", RED, 300)
    pygame.display.update()

def display_message(msg, color, y_displace=0):
    text_surface = FONT.render(msg, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_displace))
    WINDOW.blit(text_surface, text_rect)
    pygame.display.update()

def display_score(score):
    value = SCORE_FONT.render(f"Score: {score}", True, BLUE)
    WINDOW.blit(value, [10, 10])

def pause_game():
    paused = True
    display_message("Game Paused. Press P to Continue or Q to Quit.", RED, 50)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def generate_obstacles(num_obstacles):
    global OBSTACLES
    OBSTACLES = []
    for _ in range(num_obstacles):
        ob_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
        ob_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0
        OBSTACLES.append((ob_x, ob_y))

def game_loop():
    global current_mode, current_obstacle_mode

    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

    bonus_food = None
    bonus_timer = 0

    snake_speed = MODES[current_mode]['speed']

    while not game_over:

        while game_close:
            WINDOW.fill(BLACK)
            display_message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_SIZE
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        if current_obstacle_mode == 'wall':
            if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
                game_close = True
        else:
            x1 = x1 % WIDTH
            y1 = y1 % HEIGHT

        x1 += x1_change
        y1 += y1_change
        WINDOW.fill(BLACK)

        if current_obstacle_mode == 'dotted':
            for ob in OBSTACLES:
                pygame.draw.rect(WINDOW, RED, [ob[0], ob[1], SNAKE_SIZE, SNAKE_SIZE])

        elif current_obstacle_mode == 'grid':
            for i in range(0, WIDTH, SNAKE_SIZE * 2):
                for j in range(0, HEIGHT, SNAKE_SIZE * 2):
                    pygame.draw.rect(WINDOW, RED, [i, j, SNAKE_SIZE, SNAKE_SIZE])

        pygame.draw.rect(WINDOW, GREEN, [foodx, foody, SNAKE_SIZE, SNAKE_SIZE])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        if current_obstacle_mode == 'dotted':
            for ob in OBSTACLES:
                if x1 == ob[0] and y1 == ob[1]:
                    game_close = True

        for segment in snake_List:
            pygame.draw.rect(WINDOW, WHITE, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])

        display_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0
            length_of_snake += 1
            if length_of_snake % 6 == 0 and not bonus_food:
                bonus_food = [round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0,
                              round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0]
                bonus_timer = 100

        if bonus_food and x1 == bonus_food[0] and y1 == bonus_food[1]:
            bonus_food = None
            length_of_snake += 2

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    sys.exit()

def main_menu():
    global current_mode, current_obstacle_mode

    menu = True
    while menu:
        draw_welcome_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_mode = 'easy'
                    menu = False
                elif event.key == pygame.K_2:
                    current_mode = 'medium'
                    menu = False
                elif event.key == pygame.K_3:
                    current_mode = 'hard'
                    menu = False
                elif event.key == pygame.K_a:
                    current_obstacle_mode = None  # Plain mode (no obstacles)
                    menu = False
                elif event.key == pygame.K_b:
                    current_obstacle_mode = 'wall'
                    menu = False
                elif event.key == pygame.K_c:
                    current_obstacle_mode = 'dotted'
                    generate_obstacles(20)
                    menu = False
                elif event.key == pygame.K_d:
                    current_obstacle_mode = 'grid'
                    menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    game_loop()

if __name__ == "__main__":
    main_menu()
