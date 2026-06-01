"""Solution to Ellen's Alien Game exercise."""


class Alien:
    total_aliens_created=0
    def __init__(self,x_coordinate, y_coordinate):
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate
        self.health =3
        Alien.total_aliens_created+=1
    def hit(self):
        self.health-=1
    def is_alive(self):
        return self.health>0
    def teleport(self, x_coordinate, y_coordinate):
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate    
    def collision_detection(self, other_object):
        pass
        
    """Create an Alien object with location x_coordinate and y_coordinate.

    Attributes:
        (class) total_aliens_created (int): Total number of Alien instances.
        x_coordinate (int): Position on the x-axis.
        y_coordinate (int): Position on the y-axis.
        health (int): Number of health points.

    Methods:
        hit(): Decrement Alien health by one point.
        is_alive(): Return a boolean for if Alien is alive (if health is > 0).
        teleport(new_x_coordinate, new_y_coordinate): Move Alien object to new coordinates.
        collision_detection(other): Implementation TBD.

    """
def new_aliens_collection(alien_start_positions):
    aliens=[]
    for position in alien_start_positions: #(4, 7), (-1, 0) every location
        x_coordinate,y_coordinate=position
        aliens.append(Alien(x_coordinate,y_coordinate))
    return aliens
        


#TODO (Student): Create the new_aliens_collection() function below to call your Alien class with a list of coordinates

