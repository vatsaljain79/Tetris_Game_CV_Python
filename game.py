import cv2
import mediapipe as mp
import random

# Initialize Mediapipe Hands and Drawing utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# Grid settings
grid_size = 50  # Size of each grid cell
grid_color = (200, 200, 200)
num_columns = 10  # Number of columns in the reduced grid (adjust as needed)

# Define Tetris-like blocks (dimensions in grid units)
blocks = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # 1x4 vertical
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # 4x1 horizontal
    [(0, 0), (0, 1), (0, 2), (1, 0)],  # L
    [(0, 0), (0, 1), (0, 2), (1, 2)],  # L mirrored
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # 2x2 square
    [(0, 0), (0, 1), (1, 1), (1, 2)],  # S
    [(0, 1), (0, 2), (1, 0), (1, 1)],  # S mirrored
    [(0, 0), (0, 1), (0, 2), (1, 1)]   # T
]
blocks_easy = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # 1x4 vertical
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # 4x1 horizontal
    [(0, 0), (0, 1), (0, 2), (1, 2)],  # L mirrored
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # 2x2 square
]

# Block settings
current_block = random.choice(blocks)
block_color = (0, 255, 255)  # Yellow color
block_y = 0  # Initial y-position of the block
block_x_grid = 0  # Initial x-position of the block
fallen_blocks = []  # Store positions of blocks that have already fallen

# Initialize block counter and game state
block_counter = 0
desired_width = 800
game_over = False
best_score = 0

# Function to draw a block on the frame
def draw_block(frame, block, x_grid, y_pixel, color):
    for bx, by in block:
        top_left = (x_grid * grid_size + bx * grid_size, y_pixel + by * grid_size)
        bottom_right = (top_left[0] + grid_size, top_left[1] + grid_size)
        cv2.rectangle(frame, top_left, bottom_right, color, -1)

# Function to check if the block has reached the bottom or collided
def check_collision(block, x_grid, y_pixel, direction=None):
    global fallen_blocks
    for bx, by in block:
        # Check if the block has hit the bottom of the frame
        if y_pixel + (by + 1) * grid_size >= height:
            return True
        # Check for collisions with fallen blocks
        for fx, fy, _ in fallen_blocks:
            if direction == "left":  # Check for left movement
                if (x_grid + bx - 1, (y_pixel // grid_size) + by) == (fx, fy):
                    return True
            elif direction == "right":  # Check for right movement
                if (x_grid + bx + 1, (y_pixel // grid_size) + by) == (fx, fy):
                    return True
            elif (x_grid + bx, (y_pixel // grid_size) + by + 1) == (fx, fy):
                return True
    return False

# Function to check if the block is within horizontal boundaries
def is_within_boundaries(block, x_grid, direction):
    for bx, by in block:
        if direction == "left" and x_grid + bx - 1 < 0:
            return False
        if direction == "right" and x_grid + bx + 1 >= width // grid_size:
            return False
    return True

# Function to check for and clear complete rows
def check_and_clear_rows():
    global fallen_blocks
    row_counts = {}
    for _, fy, _ in fallen_blocks:
        if fy not in row_counts:
            row_counts[fy] = 0
        row_counts[fy] += 1

    rows_to_clear = [row for row, count in row_counts.items() if count == width // grid_size]
    if not rows_to_clear:
        return

    rows_to_clear.sort(reverse=True)
    for row in rows_to_clear:
        fallen_blocks = [(fx, fy, color) for fx, fy, color in fallen_blocks if fy != row]
        fallen_blocks = [
            (fx, fy + 1, color) if fy < row else (fx, fy, color) for fx, fy, color in fallen_blocks
        ]

# Function to check if the game is over
def check_game_over():
    for fx, fy, _ in fallen_blocks:
        if fy == 0 and fx == (width // grid_size) // 2 - 2:  # Top center position
            return True
    return False

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    scale_ratio = desired_width / frame.shape[1]
    frame = cv2.resize(frame, (desired_width, 700))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, _ = frame.shape

    # Draw the grid
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            cv2.rectangle(frame, (x, y), (x + grid_size, y + grid_size), grid_color, 1)
            
    if game_over:
        best_score=max(best_score,block_counter)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        cv2.putText(frame, "GAME OVER", (width // 4, int(height // 5)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)
        cv2.putText(frame, f"Score: {block_counter}", (width // 4, int(height // 3.5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Best Score: {best_score}", (width // 4, int(height // 2.5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 'R' to Restart", (width // 5, int(height //1.8) ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press 'Q' to Quit", (width // 5, int(height // 1.5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow("Tetris Game", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') or key==ord('R'):  # Restart the game
            fallen_blocks = []
            current_block = random.choice(blocks)
            block_color = (0, 255, 255)
            block_y = 0
            block_x_grid = (width // grid_size) // 2 - 2
            game_over = False
            block_counter=0
        elif key == ord('q') or key==ord('Q'):  # Quit the game
            break
        continue

    # Draw fallen blocks
    for (fx, fy, color) in fallen_blocks:
        draw_block(frame, [(0, 0)], fx, fy * grid_size, color)

    if block_y == 0:
        block_x_grid = (width // grid_size) // 2 - 2
        block_counter += 1

    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            x_pixel = int(x * width)
            finger_x_grid = x_pixel // grid_size
            if finger_x_grid < block_x_grid and is_within_boundaries(current_block, block_x_grid, "left"):
                if not check_collision(current_block, block_x_grid, block_y, "left"):
                    block_x_grid -= 1
            elif finger_x_grid > block_x_grid and is_within_boundaries(current_block, block_x_grid, "right"):
                if not check_collision(current_block, block_x_grid, block_y, "right"):
                    block_x_grid += 1
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    if not check_collision(current_block, block_x_grid, block_y):
        block_y += 5
    else:
        for bx, by in current_block:
            fallen_blocks.append((block_x_grid + bx, (block_y // grid_size) + by, block_color))
        for j in range(30):
            check_and_clear_rows()
        block_y = 0
        if block_counter<15:
            current_block = random.choice(blocks_easy)
        else:
            current_block = random.choice(blocks)
        block_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if check_game_over():
            game_over = True

    draw_block(frame, current_block, block_x_grid, block_y, block_color)
    cv2.putText(frame, f"Blocks: {block_counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Tetris Game", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
