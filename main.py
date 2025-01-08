import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
GROUND_HEIGHT = 400
FPS = 60

pygame.init()

FONT = pygame.font.SysFont('arial', 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino LOGIKA")

dino_image = pygame.image.load("C:\\Users\\Admin\\PycharmProjects\\Chrome_Dino\\res\\dino.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))

cactus_image = pygame.image.load("C:\\Users\\Admin\\PycharmProjects\\Chrome_Dino\\res\\cactus.png")
cactus_image = pygame.transform.scale(cactus_image, (30, 50))

bonus_image = pygame.image.load("C:\\Users\\Admin\\PycharmProjects\\Chrome_Dino\\res\\bonus.png")
bonus_image = pygame.transform.scale(bonus_image, (30, 30))

background_images = [
    pygame.transform.scale(
        pygame.image.load(f"C:\\Users\\Admin\\PycharmProjects\\Chrome_Dino\\res\\{i}.jpg"),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    ) for i in range(1, 7)
]


class Dino:
    def __init__(self):
        self.image = dino_image
        self.rect = self.image.get_rect(midbottom=(100, GROUND_HEIGHT))
        self.gravity = 0
        self.jump_force = -15
        self.jump_count = 0
        self.double_jumps_left = 3  # Ліміт на подвійні стрибки

    def jump(self):
        if self.rect.bottom >= GROUND_HEIGHT:  # Стрибок один раз
            self.gravity = self.jump_force
        elif self.jump_count < 1 and self.double_jumps_left > 0:
            self.gravity = self.jump_force
            self.double_jumps_left -= 1
            self.jump_count += 1

    def update(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.jump_count = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class Cactus:
    def __init__(self, x):
        self.image = cactus_image
        self.rect = self.image.get_rect(midbottom=(x, GROUND_HEIGHT))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.rect.left = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300)

    def draw(self):
        screen.blit(self.image, self.rect)


class Bonus:
    def __init__(self, x):
        self.image = bonus_image
        self.rect = self.image.get_rect(midbottom=(x, random.randint(GROUND_HEIGHT - 100, GROUND_HEIGHT - 50)))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.rect.left = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300)

    def draw(self):
        screen.blit(self.image, self.rect)


def display_text(text, x, y):
    surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(surface, (x, y))


def choose_difficulty():
    while True:
        screen.fill((255, 255, 255))
        display_text("Choose Difficulty:", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
        display_text("1. Easy", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)
        display_text("2. Normal", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
        display_text("3. Hard", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 5
                if event.key == pygame.K_2:
                    return 7
                if event.key == pygame.K_3:
                    return 10

        pygame.display.flip()


def choose_timer():
    while True:
        screen.fill((255, 255, 255))
        display_text("Choose Timer (seconds):", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)
        display_text("1. 30 seconds", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)
        display_text("2. 60 seconds", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
        display_text("3. 90 seconds", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 30
                if event.key == pygame.K_2:
                    return 60
                if event.key == pygame.K_3:
                    return 90

        pygame.display.flip()


def game_over_menu(score):
    while True:
        screen.fill((255, 255, 255))
        display_text(f"Game Over! Score: {int(score)}", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
        display_text("Press R to Restart or C to Continue", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_c:
                    return "continue"

        pygame.display.flip()


def main_game():
    dino = Dino()
    cactuses = [Cactus(random.randint(800, 1200)) for _ in range(3)]
    bonuses = [Bonus(random.randint(1000, 1400)) for _ in range(1)]  # обмеження кількості бонусів
    clock = pygame.time.Clock()

    lives = 3
    score = 0
    timer = choose_timer()
    obstacle_speed = choose_difficulty()

    background_index = 0
    background_timer = 0
    background_speed = 100

    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        dino.update()
        for cactus in cactuses:
            cactus.update(obstacle_speed)
            if dino.rect.colliderect(cactus.rect):
                lives -= 1
                cactus.rect.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
                if lives > 0:
                    continue_choice = game_over_menu(score)
                    if continue_choice == "restart":
                        return score, "restart"
                    elif continue_choice == "continue":
                        continue  # Continue the game
                else:
                    return score, "game over"

        for bonus in bonuses:
            bonus.update(obstacle_speed)
            if dino.rect.colliderect(bonus.rect):
                dino.double_jumps_left += 1
                bonus.rect.left = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 400)

        background_timer += 1
        if background_timer >= background_speed:
            background_timer = 0
            background_index = (background_index + 1) % len(background_images)

        screen.blit(background_images[background_index], (0, 0))
        pygame.draw.rect(screen, (150, 75, 0), (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        dino.draw()
        for cactus in cactuses:
            cactus.draw()
        for bonus in bonuses:
            bonus.draw()

        display_text(f"Score: {int(score)}", 10, 10)
        display_text(f"Lives: {lives}", 10, 40)
        display_text(f"Double Jumps: {dino.double_jumps_left}", 10, 70)
        display_text(f"Time: {int(timer)}", 10, 100)

        score += 0.1
        timer -= 1 / FPS
        if timer <= 0:
            return score, "game over"

        pygame.display.flip()
        clock.tick(FPS)


def start_menu():
    while True:
        screen.fill((255, 255, 255))
        display_text("Dino T-LOGIKA", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        display_text("Press SPACE to Start", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        pygame.display.flip()


while True:
    start_menu()
    final_score, game_status = main_game()

    if game_status == "restart":
        continue
    elif game_status == "game over":
        restart_or_continue = game_over_menu(final_score)
        if restart_or_continue == "restart":
            continue
        elif restart_or_continue == "continue":
            continue
