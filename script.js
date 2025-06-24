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
    requestAnimationFrame(gameLoop);
}

// ゲーム開始
gameLoop();
