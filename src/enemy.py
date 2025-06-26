import pygame
import random

# --- 定数 ---
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 3 # 速度に幅を持たせる
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_COLOR = (255, 0, 0) # 赤色 (画像ロード失敗時のフォールバック)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/images/enemy.png").convert_alpha()
        except pygame.error as e:
            print(f"Warning: Enemy image 'assets/images/enemy.png' not found or failed to load: {e}")
            self.original_image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT])
            self.original_image.fill(ENEMY_COLOR)

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 出現位置を画面上部のランダムなX座標に設定
        self.rect.x = random.randrange(0, self.screen_width - ENEMY_WIDTH)
        self.rect.y = random.randrange(-100, -ENEMY_HEIGHT) # 画面上部から徐々に見えるように

        self.speed_y = random.randrange(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX + 1)

    def update(self):
        self.rect.y += self.speed_y
        # 画面下部に出たら自動的に消滅
        if self.rect.top > self.screen_height:
            self.kill()
