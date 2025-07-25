# Snake 2.0

This repository contains a small Pygame implementation of the classic Snake game. The game supports both solo and two-player modes with a simple retro look made entirely with basic rectangles. No external sprites are required.

## Requirements
* Python 3.11+
* Pygame 2.6+

Install dependencies with:

```bash
pip install pygame
```

## Usage
Run the game in single player mode:

```bash
python3 snake.py
```

Run in multiplayer mode and set player names:

```bash
python3 snake.py --mode multi --p1 Alice --p2 Bob
```

Controls:

* **Player 1** – Arrow keys
* **Player 2** – WASD keys (only in multiplayer)

The score for each player is displayed at the top of the window.
