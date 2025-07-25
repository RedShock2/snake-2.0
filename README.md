# Snake 2.0

This repository contains a small Pygame implementation of the classic Snake game. It now features a retro **neon** look built entirely with rectangles—no external sprites needed. The game supports both solo and two-player modes and shows player scores onscreen.

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

Controls
-------

* **Player 1** – Arrow keys
* **Player 2** – WASD keys (only in multiplayer)

Each player's score is displayed in a neon font at the top of the window.
