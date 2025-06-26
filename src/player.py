import pygame
from .bullet import Bullet
from .laser import Laser, LASER_SPEED_PENALTY # Laserクラスと速度ペナルティ定数をインポート

# --- 定数 ---
PLAYER_SPEED = 5
PLAYER_SLOW_SPEED = 2  # 低速移動時の速度
PLAYER_HITBOX_RADIUS = 5 # 当たり判定コアの半径
PLAYER_HITBOX_COLOR = (255, 0, 0, 180) # 当たり判定の色 (赤、少し透明)
PLAYER_WIDTH = 50  # 仮のサイズ (画像サイズに依存するようになる)
PLAYER_HEIGHT = 50 # 仮のサイズ (画像サイズに依存するようになる)
PLAYER_COLOR = (0, 128, 255) # 青色 (画像ロード失敗時のフォールバック)
PLAYER_LASER_COOLDOWN = 1500 # レーザーのクールダウンタイム (ミリ秒)
INITIAL_BOMB_STOCK = 2 # ボムの初期ストック数
BOMB_EFFECT_DURATION = 300 # ボムエフェクトの表示時間(ミリ秒)
BOMB_SCREEN_COLOR = (200, 200, 200, 100) # ボム使用時の画面色 (白っぽく半透明)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, all_sprites_group, bullets_group):
        super().__init__()
        self.is_slow_mode = False # 低速モードフラグ
        self.lasers = pygame.sprite.Group() # レーザー用のスプライトグループ
        self.last_laser_time = -PLAYER_LASER_COOLDOWN # 最初からレーザーを撃てるように
        self.is_firing_laser = False # レーザー発射中フラグ
        self.bomb_stock = INITIAL_BOMB_STOCK
        self.is_bomb_active = False # ボムエフェクト中フラグ
        self.bomb_start_time = 0
        self.should_activate_bomb_effect = False # ボム効果発動フラグ
        try:
            self.original_image = pygame.image.load("assets/images/player.png").convert_alpha()
            # ここで .convert_alpha() を使うと透明度を扱える
        except pygame.error as e:
            print(f"Warning: Player image 'assets/images/player.png' not found or failed to load: {e}")
            self.original_image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
            self.original_image.fill(PLAYER_COLOR)
            # エラーメッセージをより具体的に

        self.image = self.original_image # 表示用の画像
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20  # 画面下部に配置
        self.speed_x = 0
        self.speed_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.all_sprites = all_sprites_group
        self.bullets = bullets_group
        self.shoot_delay = 250
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        # 水平方向の移動
        self.rect.x += self.speed_x
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

        # 垂直方向の移動
        self.rect.y += self.speed_y
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
        if self.rect.top < 0:
            self.rect.top = 0

    def handle_movement_keys(self):
        keys = pygame.key.get_pressed()
        # self.speed_x = 0 # updateメソッドで再計算するのでここでは不要
        # self.speed_y = 0 # updateメソッドで再計算するのでここでは不要

        # 低速移動モードの切り替え
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.is_slow_mode = True
        else:
            self.is_slow_mode = False

        # 移動方向の決定は update メソッド内で行うため、ここでは is_slow_mode の設定のみ
        # if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #     self.speed_x = -current_speed # current_speed を使うように変更
        # if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #     self.speed_x = current_speed
        # if keys[pygame.K_UP] or keys[pygame.K_w]:
        #     self.speed_y = -current_speed
        # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #     self.speed_y = current_speed

        # if self.speed_x != 0 and self.speed_y != 0:
        #     self.speed_x /= 1.414
        #     self.speed_y /= 1.414
        # この速度計算ロジックはupdateメソッドに移動

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.handle_movement_keys() # is_slow_mode を更新
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_x]: # Xキーでレーザー発射
            self.shoot_laser()
        if keys[pygame.K_c]: # Cキーでボム使用
            self.use_bomb()

    def use_bomb(self):
        if self.bomb_stock > 0 and not self.is_bomb_active:
            self.bomb_stock -= 1
            self.is_bomb_active = True # エフェクト表示開始
            self.bomb_start_time = pygame.time.get_ticks()
            self.should_activate_bomb_effect = True # main.pyで効果を発動させる
            print(f"Bomb used! Stock: {self.bomb_stock}") # デバッグ用

    def consume_bomb_effect_flag(self):
        """ボム効果発動フラグを消費（Falseに設定）する"""
        triggered = self.should_activate_bomb_effect
        self.should_activate_bomb_effect = False
        return triggered

    def shoot_laser(self):
        now = pygame.time.get_ticks()
        if now - self.last_laser_time > PLAYER_LASER_COOLDOWN and not self.is_firing_laser:
            self.last_laser_time = now
            self.is_firing_laser = True
            # Laserクラスのコンストラクタに合わせて引数を渡す
            new_laser = Laser(self.rect.centerx, self.rect.top, self.screen_height)
            self.all_sprites.add(new_laser)
            self.lasers.add(new_laser)

    def draw_hitbox(self, surface):
        if self.is_slow_mode:
            # 当たり判定のコアを自機の中心に描画
            # pygame.draw.circle(surface, PLAYER_HITBOX_COLOR, self.rect.center, PLAYER_HITBOX_RADIUS)
            # 四角い当たり判定にする場合（より正確なピクセルアート風）
            hitbox_rect = pygame.Rect(0, 0, PLAYER_HITBOX_RADIUS * 2, PLAYER_HITBOX_RADIUS * 2)
            hitbox_rect.center = self.rect.center
            pygame.draw.rect(surface, PLAYER_HITBOX_COLOR, hitbox_rect)


    # Spriteグループのdrawメソッドが呼ばれる前に個別の描画処理を行いたい場合は、
    # all_sprites.draw(screen) の前に player.draw_hitbox(screen) のように呼び出す必要がある。
    # もしくは、Playerクラスのimage自体を更新して当たり判定を描画に含める方法もある。
    # ここでは、main.py側で描画時に呼び出す方式を想定する。
    #
    # Playerのimageに直接描画するアプローチも考えられるが、
    # original_imageを保持しておき、毎フレームimageを再生成する形になる。
    # self.image = self.original_image.copy()
    # if self.is_slow_mode:
    #     pygame.draw.circle(self.image, PLAYER_HITBOX_COLOR, self.image.get_rect().center, PLAYER_HITBOX_RADIUS)
    # この方がSpriteグループの描画に任せられるためシンプルかもしれない。今回は後者のアプローチで試す。

    def update(self):
        # レーザー発射状態の管理
        if self.is_firing_laser and not self.lasers: # レーザーが消滅したらフラグをリセット
            self.is_firing_laser = False

        # ボムエフェクト状態の管理
        if self.is_bomb_active:
            if pygame.time.get_ticks() - self.bomb_start_time > BOMB_EFFECT_DURATION:
                self.is_bomb_active = False

        # 移動速度の決定
        current_base_speed = PLAYER_SLOW_SPEED if self.is_slow_mode else PLAYER_SPEED
        if self.is_firing_laser:
            current_speed = current_base_speed * LASER_SPEED_PENALTY
        else:
            current_speed = current_base_speed

        # speed_x, speed_y の計算 (ここを修正)
        move_x_normalized = 0
        move_y_normalized = 0
        keys = pygame.key.get_pressed() # updateでもキー状態を見る必要がある
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x_normalized -=1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x_normalized +=1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y_normalized -=1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y_normalized +=1

        # 速度の再計算
        self.speed_x = 0
        self.speed_y = 0
        if move_x_normalized != 0 or move_y_normalized != 0:
            if move_x_normalized != 0 and move_y_normalized != 0: # 斜めの場合
                self.speed_x = (move_x_normalized * current_speed) / 1.414
                self.speed_y = (move_y_normalized * current_speed) / 1.414
            else: # 上下左右の場合
                self.speed_x = move_x_normalized * current_speed
                self.speed_y = move_y_normalized * current_speed

        self.rect.x += self.speed_x
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

        # 垂直方向の移動
        self.rect.y += self.speed_y
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
        if self.rect.top < 0:
            self.rect.top = 0

        # 当たり判定表示のためにimageを更新
        self.image = self.original_image.copy() # 毎フレーム元画像からコピー
        if self.is_slow_mode:
            # 四角い当たり判定を描画
            hitbox_surface = pygame.Surface((PLAYER_HITBOX_RADIUS * 2, PLAYER_HITBOX_RADIUS * 2), pygame.SRCALPHA)
            hitbox_surface.fill(PLAYER_HITBOX_COLOR)
            # self.imageの中央にhitbox_surfaceをblitする
            blit_rect = hitbox_surface.get_rect(center=self.image.get_rect().center)
            self.image.blit(hitbox_surface, blit_rect)
