import pygame
import sys
import subprocess
import os

# ウィンドウ設定
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
FONT_COLOR = BLACK

# pygameの初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("テトリス - ランチャー")

# 相対パスで日本語対応フォントを指定
script_dir = os.path.dirname(__file__)  # 現在のスクリプトがあるディレクトリ
font_path = os.path.join("fonts", "IBMPlexSansJP-Medium.ttf")

# フォントの読み込み
try:
    font = pygame.font.Font(font_path, 40)
except FileNotFoundError:
    print(f"指定したフォントが見つかりませんでした: {font_path}。デフォルトフォントを使用します。")
    font = pygame.font.Font(None, 40)

# ボタンの定義（相対パス指定）
buttons = [
    {"label": "kind", "file": os.path.join(script_dir, "kind.py"), "rect": pygame.Rect(50, 150, 200, 50)},
    {"label": "medium", "file": os.path.join(script_dir, "medium.py"), "rect": pygame.Rect(50, 220, 200, 50)},
    {"label": "hard", "file": os.path.join(script_dir, "hard.py"), "rect": pygame.Rect(50, 290, 200, 50)},
    {"label": "custom", "file": os.path.join(script_dir, "Custom.py"), "rect": pygame.Rect(50, 360, 200, 50)},
]

# ボタン描画関数
def draw_button(button, is_hovered):
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, button["rect"])
    label = font.render(button["label"], True, FONT_COLOR)
    screen.blit(label, (button["rect"].x + 40, button["rect"].y + 10))

# メインループ
running = True
while running:
    screen.fill(WHITE)
    
    # タイトル描画
    title_text = font.render("TETRIS v1.2.0 ", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        # 選択したファイルを実行
                        file_path = os.path.join(os.getcwd(), button["file"])
                        if not os.path.exists(file_path):
                            print(f"エラー: ファイルが見つかりません: {file_path}")
                        else:
                            subprocess.Popen(["python", file_path])
                            running = False  # ランチャーを閉じる

    # ボタン描画
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        draw_button(button, button["rect"].collidepoint(mouse_pos))

    pygame.display.flip()

pygame.quit()
sys.exit()
