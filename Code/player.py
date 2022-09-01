import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple, size: tuple) -> None:
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill('#F94892')
        self.rect = self.image.get_rect(topleft=position)

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16

    def getEvent(self) -> None:
        # Get event
        keys = pygame.key.get_pressed()

        # Move event
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        # Jump event
        if keys[pygame.K_w]:
            self.jump()

    def move(self) -> None:
        self.rect.x += self.direction.x * self.speed


    def jump(self) -> None:
        self.direction.y = self.jumpSpeed

    def applyGravity(self) -> None:
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self) -> None:
        self.getEvent()
