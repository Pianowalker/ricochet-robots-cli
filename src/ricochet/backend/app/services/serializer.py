def serialize_game(game):
    return {
        "robots": {
            color: list(robot.position)
            for color, robot in game.robots.items()
        },
        "target": {
            "color": game.active_target.color,
            "position": list(game.active_target.position),
        } if game.active_target else None,
    }