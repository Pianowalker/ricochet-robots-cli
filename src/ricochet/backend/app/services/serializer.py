def serialize_game(game):
    return {
        "board": {
            "rows": game.height,
            "cols": game.width,
        },
        "robots": {
            color: list(robot.position)
            for color, robot in game.robots.items()
        },
        "target": {
            "color": game.active_target.color,
            "position": list(game.active_target.position),
        } if game.active_target else None,
        "walls": [
            [list(cell1), list(cell2)]
            for wall in game.walls
            for cell1, cell2 in [tuple(wall)]
        ],
        "bumpers": [
            {
                "position": list(b.position),
                "diagonal": b.diagonal,
                "color": b.color
            }
            for b in game.bumpers.values()   # 👈 ojo acá también
        ],
        "blocked_cells": [
            list(cell) for cell in game.blocked_cells
        ],
    }