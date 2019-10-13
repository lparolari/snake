def wasd_to_direction(wasd):
    direction = None
    if wasd == "w":
        direction = "up"
    if wasd == "s":
        direction = "down"
    if wasd == "a":
        direction = "left"
    if wasd == "d":
        direction = "right"
    return direction
