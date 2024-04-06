import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 300
GROUND_HEIGHT = 50
GRAVITY = 0.5
JUMP_HEIGHT = 10
DINO_WIDTH, DINO_HEIGHT = 40, 50
CACTUS_WIDTH, CACTUS_HEIGHT = 20, 50
BIRD_WIDTH, BIRD_HEIGHT = 60, 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()

# Load images
dino_img = pygame.image.load('dino.png')
cactus_img = pygame.image.load('cactus.png')
bird_img = pygame.image.load('bird.png')

# Scale images
dino_img = pygame.transform.scale(dino_img, (DINO_WIDTH, DINO_HEIGHT))
cactus_img = pygame.transform.scale(cactus_img, (CACTUS_WIDTH, CACTUS_HEIGHT))
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dino_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
        self.vel_y = 0
        self.on_ground = True

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.y >= SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_HEIGHT
            self.on_ground = False

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - CACTUS_HEIGHT

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - CACTUS_HEIGHT

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(20, 100)

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(20, 100)

# Create sprites groups
all_sprites = pygame.sprite.Group()
cacti = pygame.sprite.Group()
Birds = pygame.sprite.Group()

# Create player
dino = Dino()
all_sprites.add(dino)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()

    # Update
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(dino, cacti, False)
    if hits:
        running = False

    # Spawn cactus
    if random.randint(0, 100) < 2:
        cactus = Cactus()
        all_sprites.add(cactus)
        cacti.add(cactus)

    # Spawn Birds
    if random.randint(0, 100) < 1:
        bird = bird()
        all_sprites.add(bird)
        Birds.add(bird)

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
