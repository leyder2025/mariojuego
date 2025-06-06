# mariobros/utils/Constants.py

# Screen dimensions (based on existing Game.py)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Asset directory
ASSETS_DIR = "assets/images/"

# Object Spawning
OBJECT_FLOOR_Y_LIMIT = SCREEN_HEIGHT - 50  # Min Y, objects won't spawn below this

# Player constants
PLAYER_INITIAL_LIVES = 3
PLAYER_STEP_X = 10
PLAYER_JUMP_HEIGHT = 100
PLAYER_JUMP_STEPS = 10 # Number of steps in jump animation

# Star PowerUp
STAR_DURATION_S = 8  # Duration of star immunity in seconds [cite: 6]
STAR_DURATION_MS = STAR_DURATION_S * 1000

# Goomba (Enemy) constants
MAX_GOOMBAS_ON_SCREEN = 2  # Maximum Goombas at the same time [cite: 12]
TOTAL_GOOMBAS_TO_SPAWN = 10 # Total Goombas that can be generated in the game [cite: 13]
GOOMBA_SPAWN_X_OFFSET = 20 # Spawn slightly off-screen to the right
GOOMBA_SPEED = 2 # Speed of Goombas moving left

# Coin constants
TOTAL_COINS = 10 # Total coins to appear on screen [cite: 2]
COIN_COUNT_FOR_EXTRA_LIFE = 10 # Number of coins to collect for an extra life [cite: 3]

# Mushroom constants
MUSHROOM_APPEAR_TIME_S = 5 # Time special mushrooms stay visible in seconds
MUSHROOM_APPEAR_TIME_MS = MUSHROOM_APPEAR_TIME_S * 1000
FIXED_GROWTH_MUSHROOM_POS = (100, SCREEN_HEIGHT - 70) # Example fixed position (x,y)
FIXED_LIFE_MUSHROOM_POS = (700, SCREEN_HEIGHT - 70) # Example fixed position (x,y)


# Image file names (centralized for easier management if names change)
IMG_MARIO_SMALL_R = "1.png"
IMG_MARIO_SMALL_L = "1i.png"
IMG_MARIO_MOVE_R = "2.png"
IMG_MARIO_MOVE_L = "2i.png"
IMG_MARIO_BIG_R = "3.png" # Assuming 3.png is big Mario right
IMG_MARIO_BIG_L = "3i.png" # Assuming a big Mario left exists or is same as 3.png if no specific sprite
IMG_MARIO_STAR = "4.png"
IMG_MARIO_JUMP = "5.png"
IMG_HONGO_ROJO = "hongoRojo.png" # Growth mushroom [cite: 4]
IMG_HONGO_VERDE = "hongoVerde.png" # Life mushroom [cite: 4]
IMG_ESTRELLA = "estrella.png" # Star [cite: 6]
IMG_MONEDA = "moneda.png" # Coin [cite: 2]
IMG_GOOMBA_CAFE = "goomba_cafe.png" # Brown Goomba [cite: 8]
IMG_GOOMBA_NEGRO = "goomba_negro.png" # Black Goomba [cite: 8]

# Object sizes (width, height) - useful for collision and rendering
PLAYER_SMALL_SIZE = (50, 50)
PLAYER_BIG_SIZE = (50, 70) # Example, adjust as needed
ITEM_SIZE = (30, 30)
GOOMBA_SIZE = (40, 40)

# Game States
GAME_STATE_RUNNING = "running"
GAME_STATE_GAME_OVER = "game_over"
GAME_STATE_MENU = "menu"

# Time
GAME_UPDATE_INTERVAL = 50 # ms, for game loop updates (e.g., enemy movement, timers)