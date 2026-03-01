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

python cli.py

You will be prompted to choose the number of rounds.
During each round:

Declare how many moves you believe are needed.

Enter moves in the format:

R r

Where:

First letter = Robot color (R, B, G, Y)

Second letter = Direction (r, l, u, d)



🧪 Debug Mode

For development and verification purposes:

python debug_board.py

This prints quadrants and their rotations to validate geometry and wall placement.



📌 Current Scope

Core engine complete

Random board generation implemented

Multiple official-style quadrants digitalized

Color-sensitive bumper reflection

CLI-based gameplay



🔮 Future Improvements

Additional official quadrant maps

Refactoring of movement logic for clarity

Unit testing

Optional graphical interface

Game state persistence

Multiplayer mode



📖 About

This project was developed as a structured exercise in:

Object-oriented design

Board game modeling

Geometric transformations

Clean architecture principles

Incremental feature development

Feedback and suggestions are welcome.
