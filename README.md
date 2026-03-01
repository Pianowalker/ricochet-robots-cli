# Ricochet Robots – CLI Edition

A fully functional digital implementation of the board game **Ricochet Robots**, developed in Python with a modular architecture and command-line interface.

This project recreates the core mechanics of the original game, including rotating quadrants, random board assembly, colored bumpers with accurate reflection behavior, and a single-player scoring mode.

---

## 🎮 Features

- 16x16 board assembled from 4 official-style quadrants
- Correct central 2x2 blocked zone
- Random board generation with valid quadrant rotations
- Accurate bumper reflection mechanics (color-sensitive)
- Support for wildcard (multi-color spiral) targets
- Single-player round system with scoring
- Text-based CLI board rendering
- Debug mode for inspecting quadrants and rotations

---

## 🧠 Game Mechanics Implemented

- Robots slide in a straight line until hitting:
  - A wall
  - Another robot
  - The board edge
- Bumpers (`/` and `\`) reflect robots correctly
- Robots **do not reflect** on bumpers of their own color
- Targets include colored objectives and a wildcard target
- Quadrants rotate geometrically correctly (walls, targets, bumpers and borders)

---

## 🏗 Architecture Overview

The project follows a modular and domain-oriented structure:

- `game.py` – Core game engine and movement logic
- `quadrant.py` – Quadrant model with rotation mechanics
- `models.py` – Domain entities (`Robot`, `Target`, `Bumper`)
- `maps.py` – Quadrant definitions and random board assembly
- `sessions.py` – Single-player session logic and scoring
- `cli.py` – Main command-line interface
- `debug_board.py` – Development tool for inspecting boards and rotations

The board is built by selecting four distinct quadrants at random and applying constrained rotations so that their inner blocked cells align correctly in the center of the 16x16 board.

---

## 🚀 How to Run

Make sure you have Python 3.10+ installed.

```bash
python cli.py
