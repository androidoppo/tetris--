import pygame
import random

pygame.init()

# 画面設定
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# 色設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (255, 165, 0),  # L
    (0, 0, 255),    # J
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (128, 0, 128),  # T
]

# テトリスの形定義
SHAPES = [
    [[1, 1, 1, 1]],                  # I
    [[1, 0, 0], [1, 1, 1]],          # L
    [[0, 0, 1], [1, 1, 1]],          # J
    [[1, 1], [1, 1]],                # O
    [[0, 1, 1], [1, 1, 0]],          # S
    [[1, 1, 0], [0, 1, 1]],          # Z
    [[0, 1, 0], [1, 1, 1]],          # T
]

# 初期設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_blocks(self):
        positions = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    positions.append((self.x + j, self.y + i))
        return positions


class Tetris:
    def __init__(self):
        # 既存の初期化内容
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_tetromino = Tetromino()
        self.score = 0

        # 新しい属性の追加
        self.fall_speed = 1.3  # 初期の落下速度（秒単位）
        self.fall_time = 0     # タイマーの初期化
    def reset_game(self):
        # 初期化処理を呼び出してゲームの状態をリセット
        self.__init__()


    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLS):
                pygame.draw.rect(screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def draw_tetromino(self, tetromino):
        for x, y in tetromino.get_blocks():
            pygame.draw.rect(screen, tetromino.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def check_collision(self, dx=0, dy=0, rotate=False):
        shape = self.current_tetromino.shape if not rotate else [list(row) for row in zip(*self.current_tetromino.shape[::-1])]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_tetromino.x + j + dx
                    y = self.current_tetromino.y + i + dy
                    if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and self.grid[y][x] != BLACK):
                        return True
        return False

    def place_tetromino(self):
        for x, y in self.current_tetromino.get_blocks():
            self.grid[y][x] = self.current_tetromino.color
        self.clear_lines()
        self.current_tetromino = Tetromino()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        lines_cleared = len(lines_to_clear)
        
        # スコアの加算
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 200
        elif lines_cleared == 3:
            self.score += 300

        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [BLACK for _ in range(COLS)])

    def update(self, delta_time):
        # 時間経過でブロックを下に移動させる
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            if not self.check_collision(dy=1):
                self.current_tetromino.y += 1
            else:
                self.place_tetromino()
            self.fall_time = 0  # タイマーをリセット

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_tetromino(self.current_tetromino)
        
        # スコアの表示
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()


def main():
    tetris = Tetris()
    running = True

    while running:
        delta_time = clock.tick(30) / 1000  # フレーム間の経過時間（秒）
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tetris.reset_game()
                elif event.key == pygame.K_LEFT and not tetris.check_collision(dx=-1):
                    tetris.current_tetromino.x -= 1
                elif event.key == pygame.K_RIGHT and not tetris.check_collision(dx=1):
                    tetris.current_tetromino.x += 1
                elif event.key == pygame.K_DOWN and not tetris.check_collision(dy=1):
                    tetris.current_tetromino.y += 1
                elif event.key == pygame.K_UP and not tetris.check_collision(rotate=True):
                    tetris.current_tetromino.rotate()

        # ゲームの描画と更新
        tetris.update(delta_time)
        tetris.draw()

    pygame.quit()

if __name__ == "__main__":
    main()