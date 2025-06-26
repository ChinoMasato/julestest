const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Canvasのサイズを設定 (要件に合わせて変更)
canvas.width = 1280;
canvas.height = 720;

// --- ゲーム設定 ---
const GAME_BG_COLOR = '#000000'; // 黒背景
let score = 0; // スコア変数
const SCORE_PER_ENEMY = 100; // 敵1体あたりのスコア

// --- UI設定 ---
// const SCORE_FONT = "24px Arial"; // 古い定義は削除またはコメントアウト
// const SCORE_COLOR = "white";    // 古い定義は削除またはコメントアウト
// const SCORE_X = 10;             // 古い定義は削除またはコメントアウト
// const SCORE_Y = 30;             // 古い定義は削除またはコメントアウト
const UI_FONT_SIZE = 24;
const UI_FONT_FAMILY = "Arial";
const UI_FONT = `${UI_FONT_SIZE}px ${UI_FONT_FAMILY}`; // UI全体の基本フォント
const UI_COLOR = "white";    // UI全体の基本色
const UI_MARGIN_X = 20;      // UI要素の左右マージン
const UI_MARGIN_Y = 30;      // UI要素の上マージン (テキストベースラインからのオフセットとして使う)
const UI_LINE_HEIGHT = UI_FONT_SIZE * 1.2; // UI要素の行の高さ（フォントサイズ基準で調整）


// --- アセットのロード ---
const playerImg = new Image();
playerImg.src = 'assets/images/player.png';
// 実際の幅と高さは画像がロードされてから設定するのが望ましいが、一旦固定値を入れておく
const PLAYER_WIDTH = 50; // 仮。画像に合わせて調整
const PLAYER_HEIGHT = 50; // 仮。画像に合わせて調整

const enemyImg = new Image();
enemyImg.src = 'assets/images/enemy.png';
const ENEMY_WIDTH = 50; // 仮
const ENEMY_HEIGHT = 50; // 仮

const bulletImg = new Image();
bulletImg.src = 'assets/images/bullet.png';
const BULLET_WIDTH = 10; // 仮
const BULLET_HEIGHT = 20; // 仮

// 画像のロード完了を待つ処理（簡易版：エラーハンドリングやロード画面は省略）
let assetsLoaded = 0;
const totalAssets = 3; // player, enemy, bullet
function assetLoaded() {
    assetsLoaded++;
    if (assetsLoaded === totalAssets) {
        // すべてのアセットがロードされたらゲームループを開始
        // ただし、現在の構造ではgameLoopは既にグローバルで呼び出されている。
        // 本来はここで gameLoop() を呼び出すように変更すべき。
        // 今回は、画像がロードされていなくてもエラーにならないように drawImage を修正する。
        console.log("All assets loaded (basic check).");
    }
}
playerImg.onload = assetLoaded;
enemyImg.onload = assetLoaded;
bulletImg.onload = assetLoaded;


// 自機の設定
const PLAYER_SPEED = 5;
const PLAYER_SLOW_SPEED_MULTIPLIER = 0.5; // 低速時の速度倍率
const PLAYER_HITBOX_RADIUS = 5; // 当たり判定コアの半径 (描画用)
const PLAYER_HITBOX_COLOR = 'rgba(255, 0, 0, 0.7)'; // 赤色、半透明

const player = {
    x: canvas.width / 2 - PLAYER_WIDTH / 2,
    y: canvas.height - PLAYER_HEIGHT - 10, // 少し上に表示
    width: PLAYER_WIDTH,
    height: PLAYER_HEIGHT,
    speed: PLAYER_SPEED,
    slowSpeed: PLAYER_SPEED * PLAYER_SLOW_SPEED_MULTIPLIER,
    isSlowMode: false,
    // dx, dy は updatePlayerPosition で毎フレーム計算する
    // dx: 0,
    // dy: 0,
    moveLeft: false,  // 左移動フラグ
    moveRight: false, // 右移動フラグ
    moveUp: false,    // 上移動フラグ
    moveDown: false,  // 下移動フラグ
    img: playerImg // 画像オブジェクトを保持
};

// 敵キャラクターの設定
// enemyProto は createEnemy で使うので、img プロパティを追加
const enemyProto = {
    width: ENEMY_WIDTH,
    height: ENEMY_HEIGHT,
    // color: 'red', // 画像を使うので不要に
    speed: 2,
    img: enemyImg // 画像オブジェクトを保持
};

let enemies = []; // 敵を格納する配列

// 新しい敵を作成する関数
function createEnemy() {
    const enemy = {
        x: Math.random() * (canvas.width - enemyProto.width),
        y: 0 - enemyProto.height,
        width: enemyProto.width,
        height: enemyProto.height,
        // color: enemyProto.color, // 不要
        speed: enemyProto.speed,
        img: enemyProto.img // 画像を共有
    };
    enemies.push(enemy);
}

// 敵を描画する関数
function drawEnemies() {
    enemies.forEach(enemy => {
        if (enemy.img.complete && enemy.img.naturalHeight !== 0) { // 画像がロード済みかチェック
            ctx.drawImage(enemy.img, enemy.x, enemy.y, enemy.width, enemy.height);
        } else { // フォールバック描画 (色が定義されていれば)
            // ctx.fillStyle = 'red'; // 仮の色
            // ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        }
    });
}

// 敵の位置を更新する関数
function updateEnemyPositions() {
    enemies = enemies.filter(enemy => {
        enemy.y += enemy.speed;
        return enemy.y < canvas.height;
    });
}

// 一定間隔で敵を生成するタイマー
setInterval(createEnemy, 2000);

// 弾の設定
// bulletProto も同様に img プロパティを追加
const bulletProto = {
    width: BULLET_WIDTH,
    height: BULLET_HEIGHT,
    // color: 'green', // 画像を使うので不要に
    speed: 7,
    img: bulletImg // 画像オブジェクトを保持
};

let bullets = []; // 弾を格納する配列

// 弾を描画する関数
function drawBullets() {
    bullets.forEach(bullet => {
        if (bullet.img.complete && bullet.img.naturalHeight !== 0) { // 画像がロード済みかチェック
            ctx.drawImage(bullet.img, bullet.x, bullet.y, bullet.width, bullet.height);
        } else {
            // フォールバック描画
            // ctx.fillStyle = 'green'; // 仮の色
            // ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        }
    });
}

// 弾の位置を更新する関数
function updateBulletPositions() {
    bullets = bullets.filter(bullet => {
        bullet.y -= bullet.speed;
        return bullet.y + bullet.height > 0;
    });
}

// 弾を発射する関数
function shootBullet() {
    const bullet = {
        x: player.x + player.width / 2 - bulletProto.width / 2,
        y: player.y,
        width: bulletProto.width,
        height: bulletProto.height,
        // color: bulletProto.color, // 不要
        speed: bulletProto.speed,
        img: bulletProto.img // 画像を共有
    };
    bullets.push(bullet);
}

// 自機を描画する関数
function drawPlayer() {
    // 自機画像の描画
    if (player.img.complete && player.img.naturalHeight !== 0) {
        ctx.drawImage(player.img, player.x, player.y, player.width, player.height);
    } else {
        // フォールバック描画（画像ロード失敗時など）
        // ctx.fillStyle = 'blue';
        // ctx.fillRect(player.x, player.y, player.width, player.height);
    }

    // 低速移動時に当たり判定コアを描画
    if (player.isSlowMode) {
        ctx.fillStyle = PLAYER_HITBOX_COLOR;
        ctx.beginPath();
        // プレイヤーの中心座標
        const centerX = player.x + player.width / 2;
        const centerY = player.y + player.height / 2;
        ctx.arc(centerX, centerY, PLAYER_HITBOX_RADIUS, 0, Math.PI * 2); // 円を描画
        ctx.fill();
    }
}

// キーボードイベントリスナー
document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);

function keyDown(e) {
    const key = e.key.toLowerCase();
    if (key === 'arrowright' || key === 'right' || key === 'd') {
        player.moveRight = true;
    } else if (key === 'arrowleft' || key === 'left' || key === 'a') {
        player.moveLeft = true;
    } else if (key === 'arrowup' || key === 'up' || key === 'w') {
        player.moveUp = true;
    } else if (key === 'arrowdown' || key === 'down' || key === 's') {
        player.moveDown = true;
    } else if (key === ' ' || key === 'spacebar') {
        shootBullet();
    } else if (e.key === 'Shift') { // e.key は大文字小文字区別するのでそのまま 'Shift'
        player.isSlowMode = true;
    }
}

function keyUp(e) {
    const key = e.key.toLowerCase();
    if (key === 'arrowright' || key === 'right' || key === 'd') {
        player.moveRight = false;
    } else if (key === 'arrowleft' || key === 'left' || key === 'a') {
        player.moveLeft = false;
    } else if (key === 'arrowup' || key === 'up' || key === 'w') {
        player.moveUp = false;
    } else if (key === 'arrowdown' || key === 'down' || key === 's') {
        player.moveDown = false;
    } else if (e.key === 'Shift') {
        player.isSlowMode = false;
    }
}

// 自機の位置を更新する関数
function updatePlayerPosition() {
    let dx = 0;
    let dy = 0;
    const currentSpeed = player.isSlowMode ? player.slowSpeed : player.speed;

    if (player.moveLeft) {
        dx -= currentSpeed;
    }
    if (player.moveRight) {
        dx += currentSpeed;
    }
    if (player.moveUp) {
        dy -= currentSpeed;
    }
    if (player.moveDown) {
        dy += currentSpeed;
    }

    // 斜め移動時の速度調整
    if (dx !== 0 && dy !== 0) {
        dx /= 1.414;
        dy /= 1.414;
    }

    player.x += dx;
    player.y += dy;

    // 画面端での移動制限 (左右)
    if (player.x < 0) {
        player.x = 0;
    }
    if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
    }
    // 画面端での移動制限 (上下)
    if (player.y < 0) {
        player.y = 0;
    }
    if (player.y + player.height > canvas.height) {
        player.y = canvas.height - player.height;
    }
}

// 画面をクリアする関数 (指定色で塗りつぶし)
function clearCanvas() {
    ctx.fillStyle = GAME_BG_COLOR;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// ゲームループ
function gameLoop() {
    clearCanvas();
    drawPlayer();
    updatePlayerPosition();
    drawEnemies(); // 敵を描画
    updateEnemyPositions(); // 敵の位置を更新
    drawBullets(); // 弾を描画
    updateBulletPositions(); // 弾の位置を更新
    checkCollisions(); // 当たり判定をチェック
    drawUI(); // UIを描画 (drawScoreから変更)
    requestAnimationFrame(gameLoop);
}

// UIを描画する関数 (旧drawScoreを統合・拡張)
function drawUI() {
    ctx.font = UI_FONT;
    ctx.fillStyle = UI_COLOR;

    // スコア表示 (右上)
    ctx.textAlign = "right";
    ctx.fillText("Score: " + score, canvas.width - UI_MARGIN_X, UI_MARGIN_Y);

    // 残機表示 (左上 - プレースホルダー)
    ctx.textAlign = "left";
    ctx.fillText("Lives: 3", UI_MARGIN_X, UI_MARGIN_Y);

    // ボムストック表示 (左上 - 残機の下 - プレースホルダー)
    ctx.fillText("Bombs: 2", UI_MARGIN_X, UI_MARGIN_Y + UI_LINE_HEIGHT);

    // textAlignをデフォルトに戻しておく (必要であれば)
    // ctx.textAlign = "left";
}

// 当たり判定をチェックする関数
function checkCollisions() {
    // ループを逆順で行うことで、spliceによるインデックス問題を回避
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        for (let j = enemies.length - 1; j >= 0; j--) {
            const enemy = enemies[j];

            if (
                bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y
            ) {
                // 衝突した場合、敵と弾を削除
                enemies.splice(j, 1); // 先に内部ループの要素を削除
                bullets.splice(i, 1);
                score += SCORE_PER_ENEMY; // スコアを加算
                // 重要: 弾が複数の敵に当たることはないので、
                // この弾に関する内部ループはここで抜けて良い
                break;
            }
        }
    }
}

// ゲーム開始
gameLoop();
