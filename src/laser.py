import pygame

# --- 定数 ---
LASER_COLOR = (0, 255, 255, 200)  # シアン、少し透明
LASER_WIDTH = 10                 # レーザーの幅
LASER_DURATION = 500           # レーザーの表示時間 (ミリ秒)
LASER_SPEED_PENALTY = 0.3      # レーザー発射中のプレイヤーの速度低下率 (元の速度の30%になる)

class Laser(pygame.sprite.Sprite):
    def __init__(self, player_rect_centerx, player_rect_top, screen_height):
        super().__init__()
        self.screen_height = screen_height
        # image と rect は update でプレイヤーの位置に合わせて動的に生成・更新する
        self.image = pygame.Surface([LASER_WIDTH, self.screen_height]) # 仮の高さで初期化
        self.image.set_alpha(LASER_COLOR[3] if len(LASER_COLOR) > 3 else 255) # 透明度設定
        self.image.fill((LASER_COLOR[0], LASER_COLOR[1], LASER_COLOR[2]))
        self.rect = self.image.get_rect()

        self.rect.centerx = player_rect_centerx
        self.rect.bottom = player_rect_top # プレイヤーの先端からレーザーが出る

        self.spawn_time = pygame.time.get_ticks()
        self.player_rect_centerx = player_rect_centerx # 発射時のX座標
        # self.player_rect_top = player_rect_top # 発射時のY座標、レーザーの底辺になる

        # レーザーの初期形状を画面上端まで伸びるように設定
        self.rect.height = player_rect_top # 発射点から画面上端までの高さ
        self.rect.top = 0 # 画面上端に到達
        self.image = pygame.Surface([LASER_WIDTH, self.rect.height], pygame.SRCALPHA)
        self.image.fill(LASER_COLOR)


    def update(self):
        # レーザーは発射後、その場に留まり続ける（上下にも移動しない）
        # X座標は発射時のプレイヤーのX座標で固定
        # Y座標（bottom）は発射時のプレイヤーのY座標で固定
        # 高さは発射時のプレイヤーのY座標から画面上端まで

        # 時間経過で消滅
        if pygame.time.get_ticks() - self.spawn_time > LASER_DURATION:
            self.kill()

    def get_damage(self):
        # レーザーのダメージ量を返す（後で調整可能にする）
        return 50 # 通常ショットより高威力に (仮に10倍)
