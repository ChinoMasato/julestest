import pygame

# --- 定数 ---
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 255, 0) # 黄色 (画像ロード失敗時のフォールバック)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.original_image = pygame.image.load("assets/images/bullet.png").convert_alpha()
        except pygame.error as e:
            print(f"Warning: Bullet image 'assets/images/bullet.png' not found or failed to load: {e}")
            self.original_image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
            self.original_image.fill(BULLET_COLOR)

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y # プレイヤーの少し上から発射されるように調整

    def update(self):
        self.rect.y -= BULLET_SPEED
        # 画面外に出たら自動的に消滅
        if self.rect.bottom < 0:
            self.kill() # Spriteグループから自身を削除
