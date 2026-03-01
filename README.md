# Ricochet Robots (CLI Version)

A fully functional digital implementation of the board game Ricochet Robots,
featuring:

- Random board assembly
- Rotating quadrants
- Colored bumpers with correct reflection rules
- Single-player scoring mode
- Complete CLI interface

## Features

- 16x16 board assembled from real game quadrants
- Correct central blocked zone
- Accurate bumper reflection mechanics (color-sensitive)
- Random board generation
- Single-player round system
- Text-based board rendering

## How to Run

```bash
python cli.py

**## Architecture Overview**

- `game.py` – Core game engine and movement logic
- `quadrant.py` – Quadrant model with rotation mechanics
- `models.py` – Robot, Target and Bumper entities
- `maps.py` – Quadrant definitions and board assembly
- `sessions.py` – Single-player session logic
- `cli.py` – Command-line interface
- `debug_board.py` – Development debugging tool

**## Future Improvements**

- Additional official maps
- Code refactoring of movement logic
- Unit testing
- Optional graphical interface
