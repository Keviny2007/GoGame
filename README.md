# Go Game Implementation

This project implements a playable version of the game **Go** using Python and Pygame. It includes a graphical user interface (GUI) for interacting with the game board, managing game state, and tracking player moves and captures.

## Features

- **19x19 Go Board:** A standard 19x19 board layout with grid lines and star points.
- **Stone Placement:** Players can place stones on the board by clicking on valid grid points.
- **Game Rules:**
  - Detects captures and removes captured stones.
  - Prevents suicide moves unless the move also captures the opponent's stones.
  - Enforces Kos (prevents board states from repeating).
- **Undo, Pass, and Resign Buttons:** Players can undo the last move, pass their turn, or resign the game.
- **Player Turns:** Alternates between the Black and White player.
- **Capture Count:** Tracks the number of stones captured by each player.
- **Recent Move Indicator:** Highlights the most recent move on the board.

## Installation

### Prerequisites

1. Python 3.8+
2. Required Python packages:
   - `pygame`
   - `pygame-widgets`
   - `numpy`

### Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install pygame pygame-widgets numpy
   ```

3. Run the game:
   ```bash
   python go_game.py
   ```

## How to Play

1. Start the game by running the script.
2. Use your mouse to click on the board to place a stone.
3. Black goes first, followed by White. The game alternates turns.
4. Use the buttons on the left for additional actions:
   - **Undo:** Reverts the last move.
   - **Pass:** Skips the current player's turn.
   - **Resign:** Ends the game with the current player resigning.
5. Captures are automatically handled, and capture counts are displayed on the right side of the board.

## File Overview

- `go_game.py`: The main script containing all logic for game state, GUI, and rules enforcement.
- `GameState`: Class to encapsulate the game state, including the board, player turns, captures, and recent moves.
- `GoGame`: Class to manage game logic, including move validation, captures, and state transitions.
- `GameGUI`: Class to handle the graphical interface and user interactions.

## Key Bindings and Controls

- **Mouse Click:** Place a stone on the board.
- **Undo Button:** Undo the most recent move.
- **Pass Button:** Skip the current player's turn.
- **Resign Button:** Resign the game.

## Future Enhancements

- Implement end-game scoring based on territory and captures.
- Incorporate AI opponents with different strengths.
- Enhance GUI with better visual and sound effects.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- Inspired by the ancient game of Go.
- Developed using Python and Pygame for educational purposes.

---

Enjoy playing Go!

