
# Tetris-Inspired Game with Hand Tracking

This project is a Tetris-inspired game that utilizes OpenCV and Mediapipe for real-time hand tracking. Players can control the falling blocks using hand gestures detected by their webcam. The game supports basic Tetris functionalities like clearing rows, tracking scores, and displaying a game-over screen.

## Features

- **Hand Tracking:** Control the position of falling blocks using your index finger.
- **Tetris Blocks:** Various Tetris-like block shapes are included (e.g., L-shapes, T-shape, square).
- **Dynamic Difficulty:** The game starts with simpler blocks and increases in difficulty as the score progresses.
- **Game Over Screen:** Displays the score, best score, and options to restart or quit.
- **Row Clearing:** Fully filled rows are cleared, adding to the player's score.

## Requirements

To run this game, you need the following Python libraries:

- OpenCV (`cv2`)
- Mediapipe (`mediapipe`)

You also need a webcam to play the game.

## How to Play

1. **Launch the Game:**
   - Run the Python script (`game.py`).

2. **Control Blocks:**
   - Use your index finger to move the block left or right.
   - Blocks fall automatically.

3. **Game Over:**
   - The game ends when a block reaches the top-center of the grid.

4. **Restart or Quit:**
   - Press `R` to restart the game.
   - Press `Q` to quit the game.

## Key Controls

- **Move Block Left:** Move your index finger to the left.
- **Move Block Right:** Move your index finger to the right.
- **Restart Game:** Press `R` on your keyboard.
- **Quit Game:** Press `Q` on your keyboard.

## Screenshots

Here are some screenshots of the game in action.
![image](https://github.com/user-attachments/assets/5c0baaba-896d-4487-8fe2-ee2881147b6c)

![image](https://github.com/user-attachments/assets/0ccee572-799f-4f22-8b05-50f5e0d13f64)


## Customization

- You can adjust the grid size, block shapes, and other settings by modifying the script variables.
- The list of blocks (`blocks` and `blocks_easy`) can be customized for different gameplay experiences.

## Setup

1. Clone this repository or download the script.
2. Install the required Python libraries using pip:
   ```bash
   pip install opencv-python mediapipe
   ```
3. Run the script:
   ```bash
   python game.py
   ```

## Future Enhancements

- Add more block shapes for variety.
- Implement a scoring system based on cleared rows and game difficulty.
- Add a pause feature.

## Acknowledgments

- **OpenCV:** For providing powerful image and video processing capabilities.
- **Mediapipe:** For enabling real-time hand tracking.

---

Enjoy the game and have fun!

