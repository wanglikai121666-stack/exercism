# Globals for the directions
# Change the values as you see fit
EAST = "east"
NORTH = "north"
WEST = "west"
SOUTH = "south"


class Robot:
    def __init__(self, direction=NORTH, x_pos=0, y_pos=0):
        self.direction = direction
        self.coordinates = (x_pos, y_pos)
    def move(self, instructions):
        for instruction in instructions:
            if instruction == "R":
                self.turn_right()
            elif instruction == "L":
                self.turn_left()
            elif instruction == "A":
                self.advance()
    def turn_right(self):
        directions = [NORTH, EAST, SOUTH, WEST]

        current_index = directions.index(self.direction)
        next_index = (current_index + 1) % len(directions)

        self.direction = directions[next_index]
    def turn_left(self):
        directions = [NORTH, EAST, SOUTH, WEST]

        current_index = directions.index(self.direction)
        next_index = (current_index - 1) % len(directions)

        self.direction = directions[next_index]
    def advance(self):
        movement_vectors = {
            NORTH: (0, 1),
            EAST: (1, 0),
            SOUTH: (0, -1),
            WEST: (-1, 0),
        }
        x, y = self.coordinates
        dx, dy = movement_vectors[self.direction]

        self.coordinates = (x + dx, y + dy)
