const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Canvasのサイズを設定
canvas.width = 800;
canvas.height = 600;

// 自機の設定
const player = {
    x: canvas.width / 2 - 25,
    y: canvas.height - 60,
    width: 50,
    height: 50,
    color: 'blue',
    speed: 5,
    dx: 0 // X軸方向の移動量
};

// 敵キャラクターの設定
const enemyProto = {
    width: 50,
    height: 50,
    color: 'red',
    speed: 2
};

let enemies = []; // 敵を格納する配列

// 新しい敵を作成する関数
function createEnemy() {
    const enemy = {
        x: Math.random() * (canvas.width - enemyProto.width),
        y: 0 - enemyProto.height, // 画面上部から出現
        width: enemyProto.width,
        height: enemyProto.height,
        color: enemyProto.color,
        speed: enemyProto.speed
    };
    enemies.push(enemy);
}

// 敵を描画する関数
function drawEnemies() {
    enemies.forEach(enemy => {
        ctx.fillStyle = enemy.color;
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    });
}

// 敵の位置を更新する関数
function updateEnemyPositions() {
    enemies = enemies.filter(enemy => {
        enemy.y += enemy.speed;
        return enemy.y < canvas.height; // 画面下部まで到達したら消滅
    });
}

// 一定間隔で敵を生成するタイマー
setInterval(createEnemy, 2000); // 2秒ごとに新しい敵を生成

// 弾の設定
const bulletProto = {
    width: 5,
    height: 10,
    color: 'green',
    speed: 7
};

let bullets = []; // 弾を格納する配列

// 弾を描画する関数
function drawBullets() {
    bullets.forEach(bullet => {
        ctx.fillStyle = bullet.color;
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
}

// 弾の位置を更新する関数
function updateBulletPositions() {
    bullets = bullets.filter(bullet => {
        bullet.y -= bullet.speed;
        return bullet.y + bullet.height > 0; // 画面上部に到達したら消滅
    });
}

// 弾を発射する関数
function shootBullet() {
    const bullet = {
        x: player.x + player.width / 2 - bulletProto.width / 2,
        y: player.y,
        width: bulletProto.width,
        height: bulletProto.height,
        color: bulletProto.color,
        speed: bulletProto.speed
    };
    bullets.push(bullet);
}

// 自機を描画する関数
function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

// キーボードイベントリスナー
document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);

function keyDown(e) {
    if (e.key === 'ArrowRight' || e.key === 'Right') {
        player.dx = player.speed;
    } else if (e.key === 'ArrowLeft' || e.key === 'Left') {
        player.dx = -player.speed;
    } else if (e.key === ' ' || e.key === 'Spacebar') { // スペースキーで弾を発射
        shootBullet();
    }
}

function keyUp(e) {
    if (
        e.key === 'ArrowRight' ||
        e.key === 'Right' ||
        e.key === 'ArrowLeft' ||
        e.key === 'Left'
    ) {
        player.dx = 0;
    }
}

// 自機の位置を更新する関数
function updatePlayerPosition() {
    player.x += player.dx;

    // 画面端での移動制限
    if (player.x < 0) {
        player.x = 0;
    }
    if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
    }
}

// 画面をクリアする関数
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
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
    requestAnimationFrame(gameLoop);
}

// 当たり判定をチェックする関数
function checkCollisions() {
    bullets.forEach((bullet, bulletIndex) => {
        enemies.forEach((enemy, enemyIndex) => {
            if (
                bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y
            ) {
                // 衝突した場合、敵と弾を削除
                enemies.splice(enemyIndex, 1);
                bullets.splice(bulletIndex, 1);
            }
        });
    });
}

// ゲーム開始
gameLoop();
