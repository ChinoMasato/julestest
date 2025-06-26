import pygame
import sys

# --- 定数 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
PROJECT_NAME = "CodeName: ASTRAL DIVER"

from src.player import Player # Playerクラスをインポート

# --- Pygameの初期化 ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(PROJECT_NAME)
clock = pygame.time.Clock()

from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy # Enemyクラスをインポート

# --- 定数 ---
# (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PROJECT_NAME は変更なし)
ENEMY_SPAWN_RATE = 1000  # 敵の出現頻度(ミリ秒) - 例: 1秒ごと
SCORE_FONT_SIZE = 30
UI_FONT_SIZE = 24 # スコア以外のUI用フォントサイズ
# SCORE_COLOR は UI_COLOR に統合
UI_COLOR = (255, 255, 255) # 白色
INITIAL_SCORE_PER_ENEMY = 100 # 敵1体あたりの基本スコア
BOMB_DAMAGE_SCORE_MULTIPLIER = 5 # ボムで倒した敵のスコア倍率 (仮)

# --- Pygameの初期化 ---
pygame.init()
# フォントの準備
# score_font は不要にし、draw_text内で都度生成またはui_fontを共用
ui_font = pygame.font.Font(None, UI_FONT_SIZE) # UI共通フォント
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(PROJECT_NAME)
clock = pygame.time.Clock()

# --- スプライトグループ ---
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()     # 弾用のスプライトグループ
enemies = pygame.sprite.Group()     # 敵用のスプライトグループ
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, all_sprites, bullets)
all_sprites.add(player)

# --- 敵の生成制御 ---
last_enemy_spawn_time = pygame.time.get_ticks()
score = 0 # スコアの初期化

def spawn_enemy():
    enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(enemy)
    enemies.add(enemy)

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if x < SCREEN_WIDTH / 2: # X座標で左右どちらに寄せるか簡易的に判定
        text_rect.topleft = (x,y)
    else:
        text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)

# --- ゲームループ ---
running = True
bomb_effect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # ボムエフェクト用

while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力の処理
    player.handle_input()

    # ボム効果の処理 (playerがフラグを立てた次のフレームで発動)
    if player.consume_bomb_effect_flag(): # フラグをチェックし、消費する
        # 敵にダメージ（今回は即死＆スコア加算）
        for enemy_sprite in enemies: # enemiesグループ内の全敵に対して
            enemy_sprite.kill()
            score += INITIAL_SCORE_PER_ENEMY * BOMB_DAMAGE_SCORE_MULTIPLIER
        # TODO: 敵弾消去処理 (敵弾実装後)
        print("Bomb effect triggered: Enemies cleared (simulated)")


    # 敵の生成
    now = pygame.time.get_ticks()
    if now - last_enemy_spawn_time > ENEMY_SPAWN_RATE:
        last_enemy_spawn_time = now
        spawn_enemy()

    # ゲームロジックの更新
    all_sprites.update() # Player, Bullet, Enemy が更新される

    # --- 衝突判定 ---
    # 弾と敵の衝突
    # pygame.sprite.groupcollide(group1, group2, dokill1, dokill2)
    # dokill1: group1の要素を衝突時にkillするか (True/False)
    # dokill2: group2の要素を衝突時にkillするか (True/False)
    # 戻り値: 衝突したgroup1の要素をキーとし、衝突したgroup2の要素のリストを値とする辞書
    bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit_bullet in bullet_hits:
        score += len(bullet_hits[hit_bullet]) * INITIAL_SCORE_PER_ENEMY

    # レーザーと敵の衝突判定 (レーザーは貫通)
    if player.is_firing_laser: # is_firing_laser フラグではなく、実際にレーザーが存在するかで見るべき
        for laser_sprite in player.lasers: # player.lasers は player が持つべき
            # spritecollide(sprite, group, dokill) -> list_collided_sprites
            # dokill=Falseなので敵は自動では消えない
            enemies_hit_by_laser = pygame.sprite.spritecollide(laser_sprite, enemies, False)
            for enemy_hit in enemies_hit_by_laser:
                # ここで敵にダメージを与える処理（EnemyクラスにHPがあればそれを減らす）
                # 今回はHPがないので即死させる
                enemy_hit.kill() # 敵を消滅させる
                score += INITIAL_SCORE_PER_ENEMY * laser_sprite.get_damage() # レーザーの威力に応じてスコア加算 (仮)
                # TODO: EnemyクラスにHPとダメージ処理を実装する際にここを修正

    # 画面描画
    screen.fill((0, 0, 0))  # 初期は黒で塗りつぶし
    all_sprites.draw(screen) # Player, Bullet, Enemy, Laser が描画される
    draw_text(screen, f"Score: {score}", SCORE_FONT_SIZE, SCREEN_WIDTH - 10, 10, UI_COLOR) # 右上にスコア
    draw_text(screen, f"Bombs: {player.bomb_stock}", UI_FONT_SIZE, 10, 10, UI_COLOR)     # 左上にボムストック

    # ボムエフェクト描画
    if player.is_bomb_active:
        # Playerクラスの定数を参照するには player オブジェクト経由
        bomb_effect_surface.fill(player.BOMB_SCREEN_COLOR)
        screen.blit(bomb_effect_surface, (0,0))

    pygame.display.flip()  # 画面を更新
    clock.tick(FPS)        # フレームレートを制御

# --- Pygameの終了処理 ---
pygame.quit()
sys.exit()
