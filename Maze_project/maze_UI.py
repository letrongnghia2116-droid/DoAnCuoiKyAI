import pygame
import sys
import time
from datetime import datetime

# IMPORT CÁC THUẬT TOÁN TỪ FILE maze_algorithms.py
try:
    from maze_algorithms import BFS, DFS, AStar, Greedy, SteepestAscent, BeliefStateSearch, LocalBeamSearch, FogOfWarSearch, Backtracking, ForwardChecking,Minimax, AlphaBeta
except ImportError:
    print("Lỗi: Không tìm thấy file 'maze_algorithms.py'. Vui lòng để file thuật toán cùng thư mục.")
    sys.exit()

# Phân loại nhóm thuật toán
ALGO_CATEGORIES = {
    "Blind search": {"BFS": BFS, "DFS": DFS},
    "Heuristic Search": {"A*": AStar, "Greedy Best-First": Greedy},
    "Local Search": {"Steepest Ascent": SteepestAscent, "Local Beam Search": LocalBeamSearch},
    "Conformant Search": {"Belief State": BeliefStateSearch, "Fog Of War": FogOfWarSearch},
    "CSP": {"Backtracking": Backtracking, "Forward Checking": ForwardChecking},
    "Adversarial Search": {"Alpha-Beta": AlphaBeta, "Minimax": Minimax},
    "Optimal": {}
}

# =========================================
# KHỞI TẠO PYGAME
# =========================================
pygame.init()
WIDTH  = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME) 
pygame.display.set_caption("AI Maze Visualizer - Dark Mode")
clock = pygame.time.Clock()

# MÀU SẮC (DARK MODE)
BG            = (15,  23,  42 )
TITLE_BG      = (10,  15,  30 )
PANEL_BG      = (30,  41,  59 )
PANEL_BORDER  = (51,  65,  85 )
GRID_DOT      = (51,  65,  85 )
WALL          = (71,  85,  105)
WALL_SHADOW   = (15,  23,  42 )

PATH_GLOW     = (56,  189, 248, 80)
PATH_CORE     = (56,  189, 248)
VISITED_COLOR = (14,  116, 144)

START_COLOR   = (16,  185, 129)
START_GLOW    = (16,  185, 129, 60)
GOAL_COLOR    = (244, 63,  94 )
GOAL_GLOW     = (244, 63,  94,  60)

TEXT_MAIN     = (248, 250, 252)
TEXT_DIM      = (148, 163, 184)

MENU_ACTIVE   = (51,  65,  85 )
MENU_BORDER   = (56,  189, 248)

ALGO_BG       = (15,  23,  42 )
ALGO_ACTIVE   = (12,  74,  110)
ALGO_BORDER   = (56,  189, 248)

BTN_RUN_BG    = (2,   132, 199)
BTN_STOP_BG   = (220, 38,  38 )
BTN_RST_BG    = (71,  85,  105)
BTN_CLOSE_HOV = (220, 38,  38 )

LOG_BG        = (2,   6,   23 )
LOG_TEXT      = (52,  211, 153)
SCROLL_TRACK  = (30,  41,  59 )
SCROLL_THUMB  = (100, 116, 139)

# FONT
font_prefs  = ["segoeui", "tahoma", "arial", "sans-serif"]
title_font  = pygame.font.SysFont(font_prefs, 22, bold=True)
font_large  = pygame.font.SysFont(font_prefs, 18, bold=True)
font        = pygame.font.SysFont(font_prefs, 14)
font_bold   = pygame.font.SysFont(font_prefs, 14, bold=True)
small_font  = pygame.font.SysFont(font_prefs, 12, bold=True)
number_font = pygame.font.SysFont("consolas", 14, bold=True)

# KÍCH THƯỚC BỐ CỤC
ROWS     = 20
COLS     = 20
CELL     = 26
LEFT_W   = 280
RIGHT_W  = 340
TITLE_H  = 30 
MAZE_AREA_W = WIDTH - LEFT_W - RIGHT_W
MAZE_PIXEL_W = COLS * CELL
MAZE_PIXEL_H = ROWS * CELL
OFFSET_X = LEFT_W + (MAZE_AREA_W - MAZE_PIXEL_W) // 2
OFFSET_Y = 75 

# MAZE DEFINITIONS (DỮ LIỆU MÊ CUNG)
LEVELS = [
    {
        "name": "Mê cung cơ bản",
        "desc": "Đường đi ngắn, đi nhanh cả!",
        "recommended": "BFS",
        "reason": "BFS đảm bảo đường ngắn nhất\ntrên đồ thị không có trọng số.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0],
            [0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0],
            [0,1,1,0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,0],
            [0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0],
            [0,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],
            [1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0],
            [0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
            [0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1],
            [0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0],
            [1,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0],
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0],
            [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0],
            [0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0],
            [0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,0],
            [0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0],
        ],
    },
    {
        "name": "Ngã rẽ đơn giản",
        "desc": "Nhiều nhánh sai, goal ở góc xa",
        "recommended": "DFS",
        "reason": "DFS khám phá sâu nhanh,\nphù hợp maze nhiều ngõ cụt dài.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
            [0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
            [0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0],
            [0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0],
            [1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0],
            [0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0],
            [0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0],
            [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],
            [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0],
        ],
    },
    {
        "name": "Không gian mở rộng",
        "desc": "Ít tường, nhiều lựa chọn đường đi",
        "recommended": "A*",
        "reason": "A* dùng heuristic để hướng đích,\ntránh khám phá thừa trên maze thưa.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0],
            [0,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0],
            [1,0,1,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0],
            [0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,1,0],
            [0,1,1,0,1,1,1,0,0,1,1,1,1,0,1,1,1,0,1,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
            [1,0,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0],
            [0,1,1,1,1,1,0,1,1,0,0,0,1,1,1,0,1,0,1,0],
            [0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0],
            [1,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
            [0,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0],
            [0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0],
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
            [1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        ],
    },
    {
        "name": "Mê cung dày đặc",
        "desc": "Tường dày, cần tìm đường sâu",
        "recommended": "Greedy",
        "reason": "Greedy BFS chạy nhanh nhất\nkhi heuristic dẫn đúng hướng goal.",
        "start": (0, 0), "goal":  (19, 18),
        "maze": [
            [0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1],
            [1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1],
            [1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
            [1,1,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
            [0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0],
            [0,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,0],
            [0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0],
            [1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,0],
            [0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0],
            [0,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,0],
            [0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0],
            [1,1,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,0],
            [0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0],
            [0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,0],
            [0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
            [1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0],
            [1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
            [1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0],
            [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
            [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0],
        ],
    },
    {
        "name": "Dốc thẳng hướng đích",
        "desc": "Lợi thế vượt trội của Steepest Ascent",
        "recommended": "Steepest Ascent",
        "reason": "Mỗi bước đều tiến gần đích.\nPhát huy thế mạnh Steepest Ascent.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
        ]
    },
    {
        "name": "Mê cung Sương mù",
        "desc": "Bị lạc trong phòng tối. Cần ép góc để định vị trước khi tìm đích!",
        "recommended": "Belief State",
        "reason": "Các thuật toán thông thường sẽ thất bại \ndo không biết điểm bắt đầu. Belief State lợi dụng việc 'đụng tường đứng im' để thu hẹp tập niềm tin về một tọa độ thực tế duy nhất.",
        "start": [(1, 1), (1, 2), (2, 1), (2, 2), (1, 0), (1, 3), (2, 0), (2, 3)],
        "goal":  (18, 18),
        "maze": [
            [0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,0],
            [0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0],
            [0,0,0,0,0,0,1,0,1,1,1,1,0,1,0,1,1,0,1,0],
            [1,1,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,0,1,0],
            [0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
            [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
            [0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0],      
            [0,1,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,0],
            [0,1,0,0,0,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0],
            [0,1,1,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0],
            [0,0,0,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0],
            [1,1,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0], 
            [0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0], 
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0], 
        ],
    },
    {
        "name": "Nhiều nhánh song song",
        "desc": "Có nhiều nhánh rẽ đánh lừa heuristic",
        "recommended": "Local Beam Search",
        "reason": "Khám phá song song k trạng thái tốt nhất giúp\ntránh bị kẹt ở điểm mù cục bộ.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
            [0,1,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0],
            [0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
            [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
        ]
    },
    {
        "name": "Thám hiểm màn sương",
        "desc": "Tác tử bị mù môi trường, phải vừa đi vừa dò bản đồ",
        "recommended": "Fog Of War",
        "reason": "Thuật toán Online Search tự xây dựng bản đồ\nniềm tin dựa trên cảm biến thực tế khi di chuyển.",
        "start": (0, 0), "goal":  (19, 19),
        "maze": [
            [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0],
            [0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0],
            [0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,1,0,1,0],
            [0,1,1,1,1,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1],
            [0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,1,0],
            [0,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0],
            [1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0],
            [0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0],
            [0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,0,0,0,1,0],
            [0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,0],
            [0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0]
        ]
    },
    {
        "name": "Chuỗi phòng Hamiltonian",
        "desc": "Mê cung gồm hành lang chính và các phòng phụ. BFS/A* sẽ đi thẳng hành lang và bỏ sót phòng. Backtracking bị ép phải quay lui liên tục để đi dích dắc, vét sạch 100% ô trống.",
        "recommended": "Backtracking",
        "reason": "Thể hiện rõ cơ chế thử–sai của Backtracking \nkhi gặp lời giải không hợp lệ.",
        "start": (1, 1), "goal":  (18, 18),
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    },
    {
        "name": "Đấu trường Sinh tử",
        "desc": "Quái vật phục kích ở trung tâm. Hãy dùng mưu trí lừa nó khỏi vị trí để tẩu thoát!",
        "recommended": "Alpha-Beta",
        "reason": "Alpha-Beta đánh giá các nước đi tương lai \ncủa quái vật để chọn chiến lược an toàn.",
        "start": (0, 0),
        "monster_start": (9, 9),
        "goal":  (19, 19),
        "maze": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
    },
    {
        "name": "Trò chơi Mèo vờn Chuột",
        "desc": "Quái vật chặn đường ở giữa. Hãy đánh lạc hướng nó bằng thuật toán Minimax.",
        "recommended": "Minimax",
        "reason": "Minimax duyệt toàn bộ cây trò chơi để chọn ra bước đi an toàn nhất, nhưng sẽ chậm hơn Alpha-Beta do không có tính năng cắt tỉa nhánh.",
        "start": (1, 1),
        "monster_start": (9, 9),
        "goal":  (18, 18),
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1],
            [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1],
            [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1],
            [1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    },
    {
        "name": "Mê cung Forward Checking",
        "desc": "Thuật toán Backtracking kết hợp Forward Checking (Tầm nhìn = 5 bước).",
        "recommended": "Forward Checking",
        "reason": "Với tầm nhìn 5 bước, tác tử sẽ đi vào các bẫy sâu hơn 5 bước, nhưng khi cách ngõ cụt đúng 5 bước nó sẽ khựng lại và quay lui ngay lập tức!",
        "start": (1, 1),
        "goal":  (18, 18),
        "maze": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
    }
]

# QUẢN LÝ TRẠNG THÁI (APP STATE)
class AppState:
    def __init__(self):
        self.level_idx         = 0
        self.selected_category = "Blind search" 
        self.selected_algo     = "BFS"
        self.speed             = "Vừa"
        self.dropdown_open     = False
        
        self.is_running        = False
        self.stop_requested    = False
        
        self.level_scroll_y    = 0       
        self.log_scroll_y      = 0       
        self.path_scroll_y     = 0       
        self.deferred_action   = None
        
        # State để hỗ trợ Drag Scrollbar bằng chuột
        self.dragging_scrollbar = None
        self.drag_offset_y      = 0
        self.scroll_info        = {}
        
        self.run_completed     = False   
        self.visited_nodes     = []
        self.visited_cells     = set()
        self.current_search_nodes = []
        self.path_nodes        = []
        self.stats             = {}
        self.ui_rects          = {}
        self.logs              = [] 
        
        # Thêm các trường hỗ trợ đối kháng
        self.monster_pos       = None
        self.player_pos        = None
        self.monster_path_nodes = []
        
        self._reset_level()
        
        lvl = LEVELS[self.level_idx]
        rec_name = lvl["recommended"]
        if rec_name == "Greedy":
            rec_name = "Greedy Best-First"
        self.selected_category = "Optimal"
        self.selected_algo = rec_name

    def add_log(self, message):
        t = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{t}] {message}")
        if len(self.logs) > 100:  
            self.logs.pop(0)
        self.log_scroll_y = 999999 

    def _reset_level(self):
        lvl = LEVELS[self.level_idx]
        self.maze, self.start, self.goal = lvl["maze"], lvl["start"], lvl["goal"]
        self.visited_nodes, self.visited_cells, self.current_search_nodes, self.path_nodes, self.stats = [], set(), [], [], {}
        
        # Cập nhật thuộc tính quái vật
        self.monster_pos = lvl.get("monster_start")
        self.player_pos = self.start
        self.monster_path_nodes = []
        
        self.dropdown_open = False
        self.run_completed = False
        self.stop_requested = False
        self.deferred_action = None
        self.path_scroll_y = 0
        self.add_log(f"Đã tải màn: {lvl['name']}")
        
        # Cập nhật nhóm "Optimal" chứa thuật toán khuyên dùng (recommended) cho màn chơi hiện tại
        rec_name = lvl["recommended"]
        if rec_name == "Greedy":
            rec_name = "Greedy Best-First"
            
        ALGO_MAP = {
            "BFS": BFS,
            "DFS": DFS,
            "A*": AStar,
            "Greedy Best-First": Greedy,
            "Steepest Ascent": SteepestAscent,
            "Local Beam Search": LocalBeamSearch,
            "Belief State": BeliefStateSearch,
            "Fog Of War": FogOfWarSearch,
            "Backtracking": Backtracking,
            "Alpha-Beta": AlphaBeta,
            "Minimax": Minimax,
            "Forward Checking": ForwardChecking
        }
        
        rec_class = ALGO_MAP.get(rec_name)
        if rec_class:
            ALGO_CATEGORIES["Optimal"] = {rec_name: rec_class}
            
        pass

    def go_level(self, idx):
        self.level_idx = idx % len(LEVELS)
        self._reset_level()
        
        lvl = LEVELS[self.level_idx]
        rec_name = lvl["recommended"]
        if rec_name == "Greedy":
            rec_name = "Greedy Best-First"
        self.selected_category = "Optimal"
        self.selected_algo = rec_name

    def reset(self):
        self._reset_level()

    @property
    def level(self):
        return LEVELS[self.level_idx]

app = AppState()

# =========================================
# HÀM HỖ TRỢ VẼ
# =========================================
def cell_center(row, col): return (OFFSET_X + col*CELL + CELL//2, OFFSET_Y + row*CELL + CELL//2)
def cell_topleft(row, col): return (OFFSET_X + col*CELL, OFFSET_Y + row*CELL)

def draw_text(surface, text, font_, color, x, y, align="left"):
    img = font_.render(text, True, color)
    if align == "center": x -= img.get_width() // 2
    elif align == "right": x -= img.get_width()
    surface.blit(img, (x, y))

def draw_truncated_text(surface, text, font_, color, x, y, max_w):
    if font_.size(text)[0] <= max_w:
        surface.blit(font_.render(text, True, color), (x, y))
    else:
        while len(text) > 0 and font_.size(text + "...")[0] > max_w:
            text = text[:-1]
        surface.blit(font_.render(text + "...", True, color), (x, y))

def get_wrapped_lines(text, font_, max_w):
    words = text.split(" ")
    lines = []
    curr_line = ""
    for word in words:
        if font_.size(curr_line + word + " ")[0] < max_w:
            curr_line += word + " "
        else:
            if curr_line: lines.append(curr_line.strip())
            curr_line = word + " "
    if curr_line:
        lines.append(curr_line.strip())
    return lines

def draw_rounded_rect(surface, color, rect, radius, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)

def draw_custom_icon(surface, name, cx, cy, color):
    if name == "info":
        pygame.draw.circle(surface, color, (cx, cy), 7, 1)
        pygame.draw.line(surface, color, (cx, cy-3), (cx, cy-3), 2)
        pygame.draw.line(surface, color, (cx, cy-1), (cx, cy+3), 2)
    elif name == "check":
        pygame.draw.lines(surface, color, False, [(cx-4, cy), (cx-1, cy+3), (cx+5, cy-4)], 2)
    elif name == "dot":
        pygame.draw.circle(surface, color, (cx, cy), 3)
    elif name == "algo":
        pygame.draw.circle(surface, color, (cx, cy-4), 3)
        pygame.draw.circle(surface, color, (cx-5, cy+4), 3)
        pygame.draw.circle(surface, color, (cx+5, cy+4), 3)
        pygame.draw.line(surface, color, (cx, cy-4), (cx-5, cy+4), 2)
        pygame.draw.line(surface, color, (cx, cy-4), (cx+5, cy+4), 2)
    elif name == "visited":
        pygame.draw.rect(surface, color, (cx-6, cy-6, 4, 4))
        pygame.draw.rect(surface, color, (cx+2, cy-6, 4, 4))
        pygame.draw.rect(surface, color, (cx-6, cy+2, 4, 4))
        pygame.draw.rect(surface, color, (cx+2, cy+2, 4, 4))
    elif name == "path":
        pts = [(cx-6, cy+4), (cx-2, cy-4), (cx+2, cy+4), (cx+6, cy-4)]
        pygame.draw.lines(surface, color, False, pts, 2)
    elif name == "time":
        pygame.draw.circle(surface, color, (cx, cy), 6, 1)
        pygame.draw.line(surface, color, (cx, cy), (cx, cy-3), 2)
        pygame.draw.line(surface, color, (cx, cy), (cx+3, cy), 2)

# =========================================
# GIAO DIỆN (UI COMPONENTS)
# =========================================
def draw_title_bar(surface):
    bar_rect = pygame.Rect(0, 0, WIDTH, TITLE_H)
    pygame.draw.rect(surface, TITLE_BG, bar_rect)
    draw_text(surface, "AI Maze Visualizer", font_bold, TEXT_DIM, 15, 6)

    pos = pygame.mouse.get_pos()

    # Nút Close (X)
    close_r = pygame.Rect(WIDTH - 45, 0, 45, TITLE_H)
    app.ui_rects["btn_close"] = close_r
    if close_r.collidepoint(pos):
        pygame.draw.rect(surface, BTN_CLOSE_HOV, close_r)
    pygame.draw.line(surface, TEXT_MAIN, (close_r.centerx-5, close_r.centery-5), (close_r.centerx+5, close_r.centery+5), 2)
    pygame.draw.line(surface, TEXT_MAIN, (close_r.centerx-5, close_r.centery+5), (close_r.centerx+5, close_r.centery-5), 2)

    # Nút Maximize (Bị khóa)
    max_r = pygame.Rect(WIDTH - 90, 0, 45, TITLE_H)
    pygame.draw.rect(surface, WALL, (max_r.centerx-5, max_r.centery-5, 10, 10), 1)

    # Nút Minimize
    min_r = pygame.Rect(WIDTH - 135, 0, 45, TITLE_H)
    app.ui_rects["btn_min"] = min_r
    if min_r.collidepoint(pos): 
        pygame.draw.rect(surface, PANEL_BORDER, min_r)
    pygame.draw.line(surface, TEXT_MAIN, (min_r.centerx-6, min_r.centery+2), (min_r.centerx+6, min_r.centery+2), 2)

def draw_left_sidebar(surface):
    sb_y = TITLE_H + 10
    sb_h = HEIGHT - TITLE_H - 20
    sb_bottom = sb_y + sb_h
    
    draw_rounded_rect(surface, PANEL_BG, (10, sb_y, LEFT_W - 20, sb_h), 10)
    draw_rounded_rect(surface, PANEL_BORDER, (10, sb_y, LEFT_W - 20, sb_h), 10, 1)
    
    draw_text(surface, "PATHFINDER", title_font, TEXT_MAIN, 40, sb_y + 15)
    draw_text(surface, "DANH SÁCH MÀN CHƠI", small_font, TEXT_DIM, 25, sb_y + 55)
    
    # ---------------------------------------------------------
    # KÍCH THƯỚC KHUNG LOG VÀ PATH
    # ---------------------------------------------------------
    path_h = 130  
    path_y = sb_bottom - path_h - 15
    path_rect = pygame.Rect(20, path_y, LEFT_W - 40, path_h)
    
    log_h = 130   
    log_y = path_y - log_h - 15
    log_rect = pygame.Rect(20, log_y, LEFT_W - 40, log_h)
    
    app.ui_rects["log_area"] = log_rect
    app.ui_rects["path_area"] = path_rect

    sb_w = 8 # Độ rộng thanh Scrollbar

    # ==========================
    # VẼ KHUNG LOG (CÓ SCROLL KÉO THẢ)
    # ==========================
    draw_rounded_rect(surface, LOG_BG, log_rect, 8)
    draw_text(surface, "LOG HỆ THỐNG", small_font, TEXT_DIM, 35, log_rect.y + 8)

    log_clip_rect = pygame.Rect(log_rect.x, log_rect.y + 25, log_rect.w - 12, log_rect.h - 30)
    surface.set_clip(log_clip_rect)

    line_h_log = 18
    total_log_h = len(app.logs) * line_h_log
    max_log_scroll = max(0, total_log_h - log_clip_rect.h)
    app.log_scroll_y = max(0, min(app.log_scroll_y, max_log_scroll))

    start_log_y = log_clip_rect.y - app.log_scroll_y
    for i, msg in enumerate(app.logs):
        draw_truncated_text(surface, msg, font, LOG_TEXT, 30, start_log_y + i*line_h_log, log_clip_rect.w - 10)

    surface.set_clip(None)

    if max_log_scroll > 0:
        sb_x = log_rect.right - 10
        sb_hr = log_clip_rect.h / total_log_h
        h_h = max(20, log_clip_rect.h * sb_hr)
        h_y = log_clip_rect.y + (app.log_scroll_y / max_log_scroll) * (log_clip_rect.h - h_h)
        
        pygame.draw.rect(surface, SCROLL_TRACK, (sb_x, log_clip_rect.y, sb_w, log_clip_rect.h), border_radius=4)
        handle_rect = pygame.Rect(sb_x, h_y, sb_w, h_h)
        pygame.draw.rect(surface, SCROLL_THUMB, handle_rect, border_radius=4)
        
        app.ui_rects["scrollbar_handle_log"] = handle_rect
        app.scroll_info["log"] = {"max_scroll": max_log_scroll, "area_y": log_clip_rect.y, "area_h": log_clip_rect.h, "handle_h": h_h}
    else:
        app.ui_rects.pop("scrollbar_handle_log", None)

    # ==========================
    # VẼ KHUNG PATH (CÓ SCROLL KÉO THẢ)
    # ==========================
    draw_rounded_rect(surface, LOG_BG, path_rect, 8)
    draw_text(surface, "ĐƯỜNG ĐI (PATH)", small_font, TEXT_DIM, 35, path_rect.y + 8)

    if len(app.path_nodes) > 0:
        path_segments = []
        for node in app.path_nodes:
            if isinstance(node, (set, frozenset)):
                sorted_cells = sorted(list(node))
                cells_str = "{" + ",".join(f"({r},{c})" for r, c in sorted_cells) + "}"
                path_segments.append(cells_str)
            else:
                path_segments.append(f"({node[0]},{node[1]})")
        path_str = " → ".join(path_segments)
        path_clip_rect = pygame.Rect(path_rect.x, path_rect.y + 25, path_rect.w - 12, path_rect.h - 30)
        
        lines = get_wrapped_lines(path_str, small_font, path_clip_rect.w - 10)
        line_h_path = small_font.get_height() + 4
        total_path_h = len(lines) * line_h_path
        
        max_path_scroll = max(0, total_path_h - path_clip_rect.h)
        app.path_scroll_y = max(0, min(app.path_scroll_y, max_path_scroll))

        surface.set_clip(path_clip_rect)
        start_path_y = path_clip_rect.y - app.path_scroll_y
        for i, line in enumerate(lines):
            surface.blit(small_font.render(line, True, ALGO_BORDER), (25, start_path_y + i*line_h_path))
        surface.set_clip(None)

        if max_path_scroll > 0:
            sb_x = path_rect.right - 10
            sb_hr = path_clip_rect.h / total_path_h
            h_h = max(20, path_clip_rect.h * sb_hr)
            h_y = path_clip_rect.y + (app.path_scroll_y / max_path_scroll) * (path_clip_rect.h - h_h)
            
            pygame.draw.rect(surface, SCROLL_TRACK, (sb_x, path_clip_rect.y, sb_w, path_clip_rect.h), border_radius=4)
            handle_rect = pygame.Rect(sb_x, h_y, sb_w, h_h)
            pygame.draw.rect(surface, SCROLL_THUMB, handle_rect, border_radius=4)
            
            app.ui_rects["scrollbar_handle_path"] = handle_rect
            app.scroll_info["path"] = {"max_scroll": max_path_scroll, "area_y": path_clip_rect.y, "area_h": path_clip_rect.h, "handle_h": h_h}
        else:
            app.ui_rects.pop("scrollbar_handle_path", None)

    elif app.run_completed and app.stats.get("path_len", 0) == 0:
        draw_text(surface, "Không tìm thấy đường đi", font, GOAL_COLOR, 30, path_rect.y + 30)
    else:
        draw_text(surface, "Chưa có dữ liệu", font, TEXT_DIM, 30, path_rect.y + 30)

    # ==========================
    # VẼ DANH SÁCH MÀN CHƠI (CÓ SCROLL KÉO THẢ)
    # ==========================
    list_y = sb_y + 75
    list_h = log_rect.y - list_y - 10
    list_clip_rect = pygame.Rect(10, list_y, LEFT_W - 30, list_h)
    
    app.ui_rects["level_list_area"] = list_clip_rect
    
    item_h = 55
    total_h = len(LEVELS) * item_h
    max_scroll = max(0, total_h - list_h)
    app.level_scroll_y = max(0, min(app.level_scroll_y, max_scroll))
    
    surface.set_clip(list_clip_rect)
    
    start_y = list_y - app.level_scroll_y
    for i, lvl in enumerate(LEVELS):
        rect = pygame.Rect(20, start_y + i * item_h, LEFT_W - 45, 45)
        
        if rect.bottom > list_clip_rect.top and rect.top < list_clip_rect.bottom:
            app.ui_rects[f"level_{i}"] = rect
            is_selected = (i == app.level_idx)
            
            draw_rounded_rect(surface, MENU_ACTIVE if is_selected else PANEL_BG, rect, 8)
            draw_rounded_rect(surface, MENU_BORDER if is_selected else PANEL_BORDER, rect, 8, 2 if is_selected else 1)
            
            c_num, c_txt = (PATH_CORE, TEXT_MAIN) if is_selected else (TEXT_DIM, TEXT_MAIN)
            draw_text(surface, f"0{i+1}", font_large, c_num, 30, rect.y + 12)
            draw_text(surface, lvl["name"], font_bold, c_txt, 65, rect.y + 6)
            draw_text(surface, lvl["desc"], small_font, TEXT_DIM, 65, rect.y + 25)

    surface.set_clip(None) 
    
    if max_scroll > 0:
        sb_x = list_clip_rect.right + 2
        sb_height_ratio = list_h / total_h
        handle_h = max(20, list_h * sb_height_ratio)
        handle_y = list_y + (app.level_scroll_y / max_scroll) * (list_h - handle_h)
        
        pygame.draw.rect(surface, SCROLL_TRACK, (sb_x, list_y, sb_w, list_h), border_radius=4)
        handle_rect = pygame.Rect(sb_x, handle_y, sb_w, handle_h)
        pygame.draw.rect(surface, SCROLL_THUMB, handle_rect, border_radius=4)
        
        app.ui_rects["scrollbar_handle_level"] = handle_rect
        app.scroll_info["level"] = {"max_scroll": max_scroll, "area_y": list_y, "area_h": list_h, "handle_h": handle_h}
    else:
        app.ui_rects.pop("scrollbar_handle_level", None)


def draw_right_sidebar(surface):
    sb_y = TITLE_H + 10
    sb_h = HEIGHT - TITLE_H - 20
    rx = WIDTH - RIGHT_W + 10
    rw = RIGHT_W - 20
    
    draw_rounded_rect(surface, PANEL_BG, (rx, sb_y, rw, sb_h), 10)
    draw_rounded_rect(surface, PANEL_BORDER, (rx, sb_y, rw, sb_h), 10, 1)

    lvl = app.level
    opt_y = sb_y + 15
    opt_rect = pygame.Rect(rx + 20, opt_y, rw - 40, 95) 
    draw_rounded_rect(surface, ALGO_ACTIVE, opt_rect, 8)
    draw_rounded_rect(surface, ALGO_BORDER, opt_rect, 8, 1)
    
    draw_custom_icon(surface, "info", rx + 35, opt_y + 14, ALGO_BORDER)
    draw_text(surface, "GỢI Ý TỐI ƯU", small_font, ALGO_BORDER, rx + 45, opt_y + 8)
    draw_text(surface, lvl["recommended"], font_bold, TEXT_MAIN, rx + 30, opt_y + 25)
    
    for i, line in enumerate(lvl["reason"].split("\n")):
        draw_text(surface, line, font, TEXT_DIM, rx + 30, opt_y + 50 + i*20) 

    dd_y = opt_rect.bottom + 15
    draw_text(surface, "NHÓM THUẬT TOÁN", small_font, TEXT_DIM, rx + 20, dd_y)
    dd_rect = pygame.Rect(rx + 20, dd_y + 20, rw - 40, 35)
    
    app.ui_rects["btn_dropdown"] = dd_rect
    draw_rounded_rect(surface, PANEL_BG, dd_rect, 6)
    draw_rounded_rect(surface, MENU_BORDER if app.dropdown_open else PANEL_BORDER, dd_rect, 6, 1)
    draw_text(surface, app.selected_category, font, TEXT_MAIN, dd_rect.x + 10, dd_rect.y + 8)
    
    tx = dd_rect.right - 15
    ty = dd_rect.centery
    pygame.draw.polygon(surface, TEXT_DIM, [(tx-5, ty-2), (tx+5, ty-2), (tx, ty+3)])

    algo_y = dd_rect.bottom + 15
    algos = ALGO_CATEGORIES[app.selected_category]
    lvl_rec = lvl.get("recommended")
    is_special_lvl = lvl_rec in ["Belief State", "Fog Of War"]
    for i, algo_name in enumerate(algos.keys()):
        r = pygame.Rect(rx + 20, algo_y + i*40, rw - 40, 32)
        is_algo_allowed = not is_special_lvl or (algo_name == lvl_rec)
        if is_algo_allowed:
            app.ui_rects[f"algo_{algo_name}"] = r
            
        is_sel = (app.selected_algo == algo_name)
        if is_sel:
            bg_color = ALGO_ACTIVE
            border_color = ALGO_BORDER
            text_color = TEXT_MAIN
            icon_color = ALGO_BORDER
        elif not is_algo_allowed:
            bg_color = PANEL_BG
            border_color = PANEL_BORDER
            text_color = TEXT_DIM
            icon_color = PANEL_BORDER
        else:
            bg_color = PANEL_BG
            border_color = PANEL_BORDER
            text_color = TEXT_MAIN
            icon_color = TEXT_DIM
            
        draw_rounded_rect(surface, bg_color, r, 6)
        draw_rounded_rect(surface, border_color, r, 6, 1)
        
        icon_type = "check" if is_sel else "dot"
        draw_custom_icon(surface, icon_type, r.x + 15, r.centery, icon_color)
        draw_text(surface, algo_name, font, text_color, r.x+30, r.y+6)

    sp_y = algo_y + len(algos)*40 + 5
    draw_text(surface, "TỐC ĐỘ", small_font, TEXT_DIM, rx + 20, sp_y)
    speeds = ["Chậm", "Vừa", "Nhanh", "Tức thì"]
    sp_w = (rw - 55) // 4
    for i, sp in enumerate(speeds):
        r = pygame.Rect(rx + 20 + i*(sp_w + 5), sp_y + 20, sp_w, 32)
        app.ui_rects[f"speed_{sp}"] = r
        is_sel = (app.speed == sp)
        draw_rounded_rect(surface, ALGO_ACTIVE if is_sel else PANEL_BG, r, 6)
        draw_rounded_rect(surface, ALGO_BORDER if is_sel else PANEL_BORDER, r, 6, 1)
        draw_text(surface, sp, font, ALGO_BORDER if is_sel else TEXT_DIM, r.centerx, r.centery - 8, "center")

    run_r = pygame.Rect(rx + 20, sp_y + 70, 130, 40)
    rst_r = pygame.Rect(rx + 160, sp_y + 70, 130, 40)
    app.ui_rects["btn_run"], app.ui_rects["btn_rst"] = run_r, rst_r
    if app.is_running:
        draw_rounded_rect(surface, BTN_STOP_BG, run_r, 8)
        draw_text(surface, "DỪNG (STOP)", font_bold, TEXT_MAIN, run_r.centerx, run_r.centery-8, "center")
    else:
        draw_rounded_rect(surface, BTN_RUN_BG, run_r, 8)
        draw_text(surface, "CHẠY (RUN)", font_bold, TEXT_MAIN, run_r.centerx, run_r.centery-8, "center")
    draw_rounded_rect(surface, BTN_RST_BG, rst_r, 8)
    draw_text(surface, "LÀM LẠI", font_bold, TEXT_MAIN, rst_r.centerx, rst_r.centery-8, "center")

    leg_y = run_r.bottom + 20
    draw_text(surface, "CHÚ GIẢI", small_font, TEXT_DIM, rx + 20, leg_y)
    items = [(START_COLOR, "Điểm bắt đầu"), (GOAL_COLOR, "Đích đến"), (PATH_CORE, "Đường đi"), (VISITED_COLOR, "Đã duyệt"), (WALL, "Tường")]
    for i, (col, lab) in enumerate(items):
        y = leg_y + 20 + i*24
        draw_rounded_rect(surface, col, (rx + 20, y, 16, 16), 3)
        if col == WALL: 
            draw_rounded_rect(surface, WALL_SHADOW, (rx+20, y+2, 16, 14), 3)
            draw_rounded_rect(surface, WALL, (rx+20, y, 16, 16), 3)
        draw_text(surface, lab, font, TEXT_MAIN, rx + 45, y)

    if app.dropdown_open:
        cats = list(ALGO_CATEGORIES.keys())
        drop_h = len(cats) * 35
        drop_bg = pygame.Rect(dd_rect.x, dd_rect.bottom, dd_rect.w, drop_h)
        draw_rounded_rect(surface, PANEL_BG, drop_bg, 0)
        draw_rounded_rect(surface, PANEL_BORDER, drop_bg, 0, 1)
        
        lvl_rec = lvl.get("recommended")
        is_special_lvl = lvl_rec in ["Belief State", "Fog Of War"]
        for i, cat in enumerate(cats):
            item_r = pygame.Rect(drop_bg.x, drop_bg.y + i*35, drop_bg.w, 35)
            is_cat_allowed = not is_special_lvl or (lvl_rec in ALGO_CATEGORIES[cat])
            if not is_cat_allowed:
                draw_text(surface, cat, font, TEXT_DIM, item_r.x + 10, item_r.y + 8)
            else:
                app.ui_rects[f"cat_{cat}"] = item_r
                draw_text(surface, cat, font, TEXT_MAIN, item_r.x + 10, item_r.y + 8)
            pygame.draw.line(surface, PANEL_BORDER, (item_r.x, item_r.bottom-1), (item_r.right, item_r.bottom-1))

def draw_maze_area(surface):
    is_fog = (app.selected_algo == "Fog Of War")

    for r in range(ROWS):
        for c in range(COLS):
            cx, cy = cell_center(r, c)
            
            if is_fog and (r, c) not in app.visited_cells and (r, c) != app.start:
                x, y = cell_topleft(r, c)
                pygame.draw.rect(surface, PANEL_BG, (x, y+3, CELL, CELL), border_radius=4)
                pygame.draw.rect(surface, PANEL_BORDER, (x, y, CELL, CELL), border_radius=4)
                draw_text(surface, "?", font_bold, TEXT_DIM, x + CELL//2, y + CELL//2 - 6, align="center")
                continue

            if app.maze[r][c] == 0: pygame.draw.circle(surface, GRID_DOT, (cx, cy), 2)
            else:
                x, y = cell_topleft(r, c)
                pygame.draw.rect(surface, WALL_SHADOW, (x, y+3, CELL, CELL), border_radius=4)
                pygame.draw.rect(surface, WALL, (x, y, CELL, CELL), border_radius=4)

    for r, c in app.visited_cells:
        cx, cy = cell_center(r, c)
        if is_fog:
            # Highlight ô đã mở sương mù nhẹ nhàng hơn
            pygame.draw.rect(surface, (14, 116, 144, 100), (cx-8, cy-8, 16, 16), border_radius=3)
        else:
            pygame.draw.rect(surface, VISITED_COLOR, (cx-8, cy-8, 16, 16), border_radius=3)

    is_belief = (app.selected_algo == "Belief State")

    if is_belief:
        # Draw static Start Zone outline
        if isinstance(app.start, (list, set, frozenset)):
            start_points = list(app.start)
        else:
            start_points = [app.start]
        for p in start_points:
            x, y = cell_topleft(*p)
            pygame.draw.rect(surface, PANEL_BORDER, (x+3, y+3, CELL-6, CELL-6), width=1, border_radius=4)
    else:
        # Draw standard solid green Start Zone
        x, y = cell_topleft(*app.start); cx, cy = cell_center(*app.start)
        glow_s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, START_GLOW, (20, 20), 20); surface.blit(glow_s, (cx-20, cy-20))
        pygame.draw.rect(surface, START_COLOR, (x+3, y+3, CELL-6, CELL-6), border_radius=4)

    # Draw static Goal Zone (Hide in Fog Of War if not visited)
    if not is_fog or app.goal in app.visited_cells or app.run_completed:
        x, y = cell_topleft(*app.goal); cx, cy = cell_center(*app.goal)
        glow_s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, GOAL_GLOW, (20, 20), 20); surface.blit(glow_s, (cx-20, cy-20))
        pygame.draw.rect(surface, GOAL_COLOR, (x+3, y+3, CELL-6, CELL-6), border_radius=4)

    if len(app.path_nodes) > 1:
        pts = []
        all_path_cells = set()
        for node in app.path_nodes:
            if isinstance(node, (set, frozenset)):
                avg_r = sum(r for r, c in node) / len(node)
                avg_c = sum(c for r, c in node) / len(node)
                cx = OFFSET_X + avg_c * CELL + CELL // 2
                cy = OFFSET_Y + avg_r * CELL + CELL // 2
                pts.append((cx, cy))
                for cell in node:
                    all_path_cells.add(cell)
            else:
                pts.append(cell_center(*node))
                all_path_cells.add(node)
        path_s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(path_s, PATH_GLOW, False, pts, 10); surface.blit(path_s, (0, 0))
        pygame.draw.lines(surface, PATH_CORE, False, pts, 3)
        for cell in all_path_cells:
            pygame.draw.circle(surface, PATH_CORE, cell_center(*cell), 3)

    # Draw monster path for Alpha-Beta and Minimax
    is_adversarial = (app.selected_algo in ["Alpha-Beta", "Minimax"])
    if is_adversarial and len(app.monster_path_nodes) > 1:
        m_pts = [cell_center(*node) for node in app.monster_path_nodes]
        m_path_s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.lines(m_path_s, (249, 115, 22, 80), False, m_pts, 10)
        surface.blit(m_path_s, (0, 0))
        pygame.draw.lines(surface, (249, 115, 22), False, m_pts, 3)
        for cell in app.monster_path_nodes:
            pygame.draw.circle(surface, (249, 115, 22), cell_center(*cell), 3)

    # For Belief State, draw active robot positions
    if is_belief:
        # Determine current positions of the active agent(s) / robots
        if app.path_nodes:
            curr_p_val = app.path_nodes[-1]
        elif app.current_search_nodes:
            curr_p_val = app.current_search_nodes
        else:
            curr_p_val = app.start

        if isinstance(curr_p_val, (list, set, frozenset)):
            curr_points = list(curr_p_val)
        else:
            curr_points = [curr_p_val]
            
        if len(curr_points) > 1:
            # Phase 1: Still localizing (uncertainty). Draw hollow green squares for belief state.
            for p in curr_points:
                x, y = cell_topleft(*p)
                pygame.draw.rect(surface, START_COLOR, (x+3, y+3, CELL-6, CELL-6), width=2, border_radius=4)
        else:
            # Phase 2: Localized to 1 cell! Draw the actual solid robot.
            p = curr_points[0]
            x, y = cell_topleft(*p); cx, cy = cell_center(*p)
            glow_s = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow_s, START_GLOW, (20, 20), 20); surface.blit(glow_s, (cx-20, cy-20))
            pygame.draw.rect(surface, START_COLOR, (x+3, y+3, CELL-6, CELL-6), border_radius=4)
            pygame.draw.circle(surface, TEXT_MAIN, (cx, cy), 4)
    else:
        # Draw standard player
        if is_adversarial and app.player_pos:
            p = app.player_pos
        elif app.path_nodes:
            p = list(app.path_nodes[-1])[0] if isinstance(app.path_nodes[-1], (set, frozenset)) else app.path_nodes[-1]
        elif app.current_search_nodes:
            p = app.current_search_nodes[0]
        else:
            p = app.start

        x, y = cell_topleft(*p); cx, cy = cell_center(*p)
        glow_s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, START_GLOW, (20, 20), 20); surface.blit(glow_s, (cx-20, cy-20))
        pygame.draw.rect(surface, START_COLOR, (x+3, y+3, CELL-6, CELL-6), border_radius=4)
        pygame.draw.circle(surface, TEXT_MAIN, (cx, cy), 4)

        # Draw Monster Icon
        if is_adversarial and app.monster_pos:
            mx, my = cell_topleft(*app.monster_pos); mcx, mcy = cell_center(*app.monster_pos)
            m_glow_s = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(m_glow_s, (220, 38, 38, 60), (20, 20), 20); surface.blit(m_glow_s, (mcx-20, mcy-20))
            pygame.draw.circle(surface, (234, 88, 12), (mcx, mcy), CELL//2 - 2)
            pygame.draw.polygon(surface, TEXT_MAIN, [(mcx-5, mcy-6), (mcx-8, mcy-12), (mcx-2, mcy-8)])
            pygame.draw.polygon(surface, TEXT_MAIN, [(mcx+5, mcy-6), (mcx+8, mcy-12), (mcx+2, mcy-8)])
            pygame.draw.circle(surface, (220, 38, 38), (mcx-3, mcy-1), 2)
            pygame.draw.circle(surface, (220, 38, 38), (mcx+3, mcy-1), 2)

def draw_bottom_stats(surface):
    bw, bh = 150, 60
    sx = LEFT_W + (MAZE_AREA_W - (bw*4 + 30)) // 2
    sy = OFFSET_Y + MAZE_PIXEL_H + 20

    algo_name = app.selected_algo
    
    if app.run_completed:
        visited = str(app.stats.get("visited", "---"))
        path_len = str(app.stats.get("path_len", "---"))
        time_ms = f"{app.stats.get('time_ms', 0):.1f} ms"
    else:
        visited = "---"
        path_len = "---"
        time_ms = "---"

    data = [
        ("THUẬT TOÁN", algo_name, "algo"),
        ("SỐ BƯỚC THĂM", visited, "visited"),
        ("ĐỘ DÀI ĐƯỜNG", path_len, "path"),
        ("THỜI GIAN", time_ms, "time")
    ]

    for i, (title, val, icon_name) in enumerate(data):
        r = pygame.Rect(sx + i*(bw+10), sy, bw, bh)
        draw_rounded_rect(surface, PANEL_BG, r, 8)
        draw_rounded_rect(surface, PANEL_BORDER, r, 8, 1)
        
        draw_custom_icon(surface, icon_name, r.x + 22, r.centery, ALGO_BORDER if i==0 else TEXT_DIM)
        draw_text(surface, title, small_font, TEXT_DIM, r.x + 40, r.y + 12)
        draw_text(surface, val, font_bold if i==0 else number_font, ALGO_BORDER if i==0 else TEXT_MAIN, r.x + 40, r.y + 30)

def redraw():
    app.ui_rects.clear()
    screen.fill(BG)
    draw_title_bar(screen)
    draw_maze_area(screen)
    draw_bottom_stats(screen)
    draw_left_sidebar(screen)
    draw_right_sidebar(screen)
    pygame.display.update()

# =========================================
# XỬ LÝ LÔ-GIC & SỰ KIỆN
# =========================================
def get_delays():
    speed = app.speed
    if speed == "Tức thì":
        return 0, 0, 0, 0
    d_vis, d_path = {"Chậm": (20, 50), "Vừa": (5, 20), "Nhanh": (1, 10)}[speed]
    d_step = {"Chậm": 600, "Vừa": 300, "Nhanh": 150}[speed]
    d_ab = {"Chậm": 400, "Vừa": 200, "Nhanh": 50, "Tức thì": 0}[speed]
    return d_vis, d_path, d_step, d_ab

def process_event(e):
    global running
    mouse_pos = pygame.mouse.get_pos()
    
    if e.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()
        
    elif e.type == pygame.MOUSEWHEEL:
        list_area_rect = app.ui_rects.get("level_list_area", pygame.Rect(0,0,0,0))
        log_area_rect = app.ui_rects.get("log_area", pygame.Rect(0,0,0,0))
        path_area_rect = app.ui_rects.get("path_area", pygame.Rect(0,0,0,0))

        if list_area_rect.collidepoint(mouse_pos):
            app.level_scroll_y -= e.y * 30 
        elif log_area_rect.collidepoint(mouse_pos):
            app.log_scroll_y -= e.y * 20
        elif path_area_rect.collidepoint(mouse_pos):
            app.path_scroll_y -= e.y * 20
            
    elif e.type == pygame.MOUSEBUTTONUP:
        if e.button == 1:
            app.dragging_scrollbar = None

    elif e.type == pygame.MOUSEMOTION:
        if app.dragging_scrollbar:
            info = app.scroll_info.get(app.dragging_scrollbar)
            if info:
                max_s = info["max_scroll"]
                ay = info["area_y"]
                ah = info["area_h"]
                hh = info["handle_h"]
                
                new_y = e.pos[1] - app.drag_offset_y
                new_y = max(ay, min(new_y, ay + ah - hh))
                
                ratio = (new_y - ay) / (ah - hh) if ah > hh else 0
                new_scroll = ratio * max_s
                
                if app.dragging_scrollbar == "level":
                    app.level_scroll_y = new_scroll
                elif app.dragging_scrollbar == "log":
                    app.log_scroll_y = new_scroll
                elif app.dragging_scrollbar == "path":
                    app.path_scroll_y = new_scroll

    elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        pos = e.pos
        
        # 1. Scrollbars
        clicked_scrollbar = False
        for key, r in app.ui_rects.items():
            if key.startswith("scrollbar_handle_"):
                if r.collidepoint(pos):
                    app.dragging_scrollbar = key.split("_")[-1]
                    app.drag_offset_y = pos[1] - r.y
                    clicked_scrollbar = True
                    break
        if clicked_scrollbar:
            return

        # 2. Dropdown
        if app.dropdown_open:
            clicked_cat = False
            for key, r in app.ui_rects.items():
                if key.startswith("cat_") and r.collidepoint(pos):
                    cat_name = key.replace("cat_", "")
                    if app.is_running:
                        app.stop_requested = True
                        app.deferred_action = ("cat", (cat_name, list(ALGO_CATEGORIES[cat_name].keys())[0]))
                    else:
                        app.selected_category = cat_name
                        app.selected_algo = list(ALGO_CATEGORIES[cat_name].keys())[0]
                        if app.selected_algo in ["Alpha-Beta", "Minimax"]:
                            app.monster_pos = app.level.get("monster_start")
                            app.monster_path_nodes = []
                        app.reset()
                    app.dropdown_open = False
                    clicked_cat = True
                    break
            if not clicked_cat: 
                app.dropdown_open = False
            return
        
        # 3. Nút bấm khác
        for key, r in list(app.ui_rects.items()):
            if key in ["level_list_area", "log_area", "path_area"]: continue 
            
            if r.collidepoint(pos):
                if key == "btn_close": 
                    running = False
                    pygame.quit()
                    sys.exit()
                elif key == "btn_min": 
                    pygame.display.iconify()
                elif key == "btn_dropdown": 
                    app.dropdown_open = True
                elif key.startswith("level_"):
                    idx = int(key.split("_")[1])
                    if app.is_running:
                        app.stop_requested = True
                        app.deferred_action = ("level", idx)
                    else:
                        app.go_level(idx)
                elif key.startswith("algo_"):
                    algo_name = key.replace("algo_", "")
                    lvl_rec = app.level["recommended"]
                    if lvl_rec in ["Belief State", "Fog Of War"] and algo_name != lvl_rec:
                        continue
                    if app.is_running:
                        app.stop_requested = True
                        app.deferred_action = ("algo", algo_name)
                    else:
                        app.selected_algo = algo_name
                        if app.selected_algo in ["Alpha-Beta", "Minimax"]:
                            app.monster_pos = app.level.get("monster_start")
                            app.monster_path_nodes = []
                        app.reset()
                elif key.startswith("speed_"): 
                    app.speed = key.replace("speed_", "")
                elif key == "btn_run":
                    if app.is_running:
                        app.stop_requested = True
                        app.add_log("Đã dừng thuật toán.")
                    else:
                        run_algorithm()
                elif key == "btn_rst":
                    if app.is_running:
                        app.stop_requested = True
                        app.deferred_action = ("reset", None)
                        app.add_log("Đã dừng và làm lại.")
                    else:
                        app.reset()

def pump_events():
    for e in pygame.event.get():
        process_event(e)
        
    # Cập nhật cursor hover
    mouse_pos = pygame.mouse.get_pos()
    is_hover = False
    if app.dragging_scrollbar:
        is_hover = True
    else:
        for key, r in app.ui_rects.items():
            if key in ["level_list_area", "log_area", "path_area"]: continue 
            if r.collidepoint(mouse_pos):
                is_hover = True
                break
    if is_hover:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

def animate(result, is_resuming=False):
    if not is_resuming:
        app.visited_nodes, app.visited_cells, app.path_nodes = [], set(), []
        app.current_search_nodes = []
        app.monster_path_nodes = []
    
    if app.speed == "Tức thì":
        app.visited_nodes = result["visited"]
        app.path_nodes = result["path"]
        for node in result["visited"]:
            if isinstance(node, (set, frozenset)):
                app.visited_cells.update(node)
            else:
                app.visited_cells.add(node)
        if result["path"]:
            last_node = result["path"][-1]
            app.current_search_nodes = list(last_node) if isinstance(last_node, (set, frozenset)) else [last_node]
        if app.selected_algo in ["Alpha-Beta", "Minimax"]:
            app.monster_path_nodes = result.get("monster_path", [])
            if result["path"]:
                app.player_pos = result["path"][-1]
            if result.get("monster_path"):
                app.monster_pos = result["monster_path"][-1]
        return

    # HỖ TRỢ HIỂN THỊ ĐỐI KHÁNG CHO ALPHA-BETA & MINIMAX
    if app.selected_algo in ["Alpha-Beta", "Minimax"]:
        path = result["path"]
        m_path = result["monster_path"]
        
        start_idx = len(app.path_nodes)
        for i in range(start_idx, len(path)):
            pump_events()
            if app.stop_requested:
                return
            d_vis, d_path, d_step, d_ab = get_delays()
            app.player_pos = path[i]
            app.monster_pos = m_path[i]
            app.path_nodes.append(path[i])
            app.monster_path_nodes.append(m_path[i])
            app.visited_cells.add(path[i])
            app.current_search_nodes = [path[i]]
            
            # Cần redraw để cập nhật giao diện
            redraw()
            if d_ab > 0:
                pygame.time.delay(d_ab)
        return

    # HỖ TRỢ HIỂN THỊ 2 PHA CHO THUẬT TOÁN BELIEF STATE
    if app.selected_algo == "Belief State":
        path = result["path"]
        visited = result["visited"]
        
        # Tìm vị trí đầu tiên của đường đi mà Belief State đã thu về 1 ô duy nhất
        first_single_idx = 0
        for i, node in enumerate(path):
            if len(node) == 1:
                first_single_idx = i
                break
                
        loc_path = path[:first_single_idx + 1]
        bfs_path = [list(node)[0] for node in path[first_single_idx:]]
        bfs_visited = [list(node)[0] for node in visited if len(node) == 1]

        # --- PHA 1: DI CHUYỂN GỘP Ô ĐỂ ĐỊNH VỊ (LOCALIZATION PATH) ---
        start_loc_idx = len(app.path_nodes)
        if start_loc_idx < len(loc_path):
            for node in loc_path[start_loc_idx:]:
                pump_events()
                if app.stop_requested:
                    return
                d_vis, d_path, d_step, d_ab = get_delays()
                app.path_nodes.append(node)
                app.current_search_nodes = list(node)
                redraw()
                if d_step > 0:
                    pygame.time.delay(d_step)
                
            if not app.stop_requested:
                d_vis, d_path, d_step, d_ab = get_delays()
                if d_step > 0:
                    pygame.time.delay(300) # Dừng một chút khi gộp thành 1 ô thành công

        # --- PHA 2: CHẠY BFS TÌM ĐƯỜNG (BFS VISITED) ---
        total_visited = len(bfs_visited)
        max_steps = 100
        batch_size = max(1, total_visited // max_steps)
        
        already_visited_count = sum(1 for cell in bfs_visited if cell in app.visited_cells)
        if already_visited_count < total_visited:
            count = already_visited_count
            for cell in bfs_visited[already_visited_count:]:
                pump_events()
                if app.stop_requested:
                    return
                d_vis, d_path, d_step, d_ab = get_delays()
                app.visited_cells.add(cell)
                count += 1
                if count % batch_size == 0 or count == total_visited:
                    redraw()
                    if d_vis > 0:
                        pygame.time.delay(d_vis)
                    
            if not app.stop_requested:
                d_vis, d_path, d_step, d_ab = get_delays()
                if d_vis > 0:
                    pygame.time.delay(100)

        # --- PHA 3: ROBOT CHẠY THEO BFS ĐẾN ĐÍCH (BFS PATH) ---
        start_bfs_path_idx = max(0, len(app.path_nodes) - len(loc_path))
        for cell in bfs_path[1 + start_bfs_path_idx:]:
            pump_events()
            if app.stop_requested:
                return
            d_vis, d_path, d_step, d_ab = get_delays()
            app.path_nodes.append(frozenset([cell]))
            app.current_search_nodes = [cell]
            redraw()
            if d_path > 0:
                pygame.time.delay(d_path)
        return

    # MẶC ĐỊNH CHO CÁC THUẬT TOÁN KHÁC
    total_visited = len(result["visited"])
    max_steps = 100
    batch_size = max(1, total_visited // max_steps)

    count = len(app.visited_nodes)
    if count < total_visited:
        for node in result["visited"][count:]:
            pump_events()
            if app.stop_requested:
                return
            d_vis, d_path, d_step, d_ab = get_delays()
            app.visited_nodes.append(node)
            if isinstance(node, (set, frozenset)):
                app.visited_cells.update(node)
            else:
                app.visited_cells.add(node)
            
            count += 1
            if count % batch_size == 0 or count == total_visited:
                app.current_search_nodes = list(node) if isinstance(node, (set, frozenset)) else [node]
                redraw()
                if d_vis > 0:
                    pygame.time.delay(d_vis)
        
    start_path_idx = len(app.path_nodes)
    for node in result["path"][start_path_idx:]:
        pump_events()
        if app.stop_requested:
            return
        d_vis, d_path, d_step, d_ab = get_delays()
        app.path_nodes.append(node)
        app.current_search_nodes = list(node) if isinstance(node, (set, frozenset)) else [node]
        redraw()
        if d_path > 0:
            pygame.time.delay(d_path)

def run_algorithm():
    is_resuming = (not app.run_completed) and (len(app.visited_cells) > 0 or len(app.path_nodes) > 0)
    
    app.is_running = True
    app.stop_requested = False
    app.run_completed = False 
    app.path_scroll_y = 0 
    if is_resuming:
        app.add_log(f"> Tiếp tục chạy {app.selected_algo}...")
    else:
        app.add_log(f"> Chạy {app.selected_algo}...")
    redraw()
    
    algo_class = ALGO_CATEGORIES[app.selected_category][app.selected_algo]
    if app.selected_algo in ["Alpha-Beta", "Minimax"]:
        algo = algo_class(app.maze, app.start, app.goal, app.level.get("monster_start"))
    else:
        algo = algo_class(app.maze, app.start, app.goal)
    
    t0 = time.perf_counter()
    res = algo.solve()
    t1 = time.perf_counter()
    
    time_ms = (t1 - t0) * 1000
    app.stats = {
        "algo": app.selected_algo, 
        "visited": len(res["visited"]), 
        "path_len": len(res["path"]), 
        "time_ms": time_ms
    }
    
    animate(res, is_resuming)
    
    # Process deferred action if any was requested during animate loop
    if app.deferred_action:
        action_type, action_val = app.deferred_action
        app.deferred_action = None
        app.is_running = False
        app.run_completed = False
        if action_type == "reset":
            app.reset()
        elif action_type == "level":
            app.go_level(action_val)
        elif action_type == "algo":
            app.selected_algo = action_val
            if app.selected_algo in ["Alpha-Beta", "Minimax"]:
                app.monster_pos = app.level.get("monster_start")
                app.monster_path_nodes = []
            app.reset()
        elif action_type == "cat":
            cat_name, algo_name = action_val
            app.selected_category = cat_name
            app.selected_algo = algo_name
            if app.selected_algo in ["Alpha-Beta", "Minimax"]:
                app.monster_pos = app.level.get("monster_start")
                app.monster_path_nodes = []
            app.reset()
        redraw()
        return

    if app.stop_requested:
        app.run_completed = False
        app.is_running = False
        app.stats = {
            "algo": app.selected_algo, 
            "visited": len(app.visited_cells), 
            "path_len": len(app.path_nodes), 
            "time_ms": time_ms
        }
        redraw()
        return

    app.run_completed = True
    app.is_running = False
    
    if res["found"]:
        app.add_log(f"Path: {len(res['path'])} ô - {time_ms:.1f}ms")
        if app.selected_algo in ["Alpha-Beta", "Minimax"]:
            app.add_log(f"Kết quả: {res.get('msg', 'Win')}")
    elif app.selected_algo in ["Alpha-Beta", "Minimax"]:
        app.add_log(f"Kết quả: {res.get('msg', 'Lost')} - {time_ms:.1f}ms")
    else:
        app.add_log(f"Không thể tìm thấy đích!")
        
    redraw()

running = True

if __name__ == "__main__":
    while running:
        clock.tick(60)
        
        mouse_pos = pygame.mouse.get_pos()
        is_hover = False
        
        # CHUỘT HOVER: Ưu tiên các thanh cuộn
        if app.dragging_scrollbar:
            is_hover = True
        else:
            for key, r in app.ui_rects.items():
                if key in ["level_list_area", "log_area", "path_area"]: continue 
                if r.collidepoint(mouse_pos):
                    is_hover = True
                    break
                
        if is_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        redraw()
        
        for e in pygame.event.get():
            process_event(e)

    pygame.quit()
    sys.exit()