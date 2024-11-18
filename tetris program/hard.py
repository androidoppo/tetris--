import pygame
import random

from medium import Tetromino

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

# 初期設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Tetris:
    def __init__(self):
        # クラスの初期化コード
        self.grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
        self.current_tetromino = Tetromino()
        self.score = 0
        self.next_block_score = 500  # 妨害ブロックがせり上がるスコアの基準
        self.garbage_rows_added = 0  # 追加された妨害行のカウント

    def reset_game(self):
        self.__init__()  # ゲームを初期化（インスタンスを再初期化）

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
        self.add_garbage_rows_based_on_score()

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

    def add_garbage_rows_based_on_score(self):
        # 現在のスコアに応じてせり上がる行数を決定
        if self.score >= 3000:
            rows_to_add = 3
        elif self.score >= 1000:
            rows_to_add = 2
        elif self.score >= 500:
            rows_to_add = 1
        else:
            rows_to_add = 0

        # 行を追加し、次のスコア基準を更新
        for _ in range(rows_to_add):
            self.add_garbage_row()
        self.next_block_score += 500

    def add_garbage_row(self):
        garbage_row = [random.choice(COLORS) for _ in range(COLS)]
        hole_indices = random.sample(range(COLS), 2)
        for hole in hole_indices:
            garbage_row[hole] = BLACK

        self.grid.pop(0)
        self.grid.append(garbage_row)

    def update(self):
        if not self.check_collision(dy=1):
            self.current_tetromino.y += 1
        else:
            self.place_tetromino()

    def draw(self):
        screen.fill(BLACK)
        self.draw_grid()
        self.draw_tetromino(self.current_tetromino)
        
        # スコアの表示
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

def main():
    tetris = Tetris()  # Tetris クラスのインスタンスを作成
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tetris.reset_game()  # インスタンスのメソッドを使用してゲームをリセット
                elif event.key == pygame.K_LEFT and not tetris.check_collision(dx=-1):
                    tetris.current_tetromino.x -= 1
                elif event.key == pygame.K_RIGHT and not tetris.check_collision(dx=1):
                    tetris.current_tetromino.x += 1
                elif event.key == pygame.K_DOWN and not tetris.check_collision(dy=1):
                    tetris.current_tetromino.y += 1
                elif event.key == pygame.K_UP and not tetris.check_collision(rotate=True):
                    tetris.current_tetromino.rotate()

        # ゲームの描画と更新
        tetris.update()
        tetris.draw()
        clock.tick(4)

    pygame.quit()

if __name__ == "__main__":
    main()
