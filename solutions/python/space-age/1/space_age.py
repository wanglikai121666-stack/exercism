class SpaceAge:
    EARTH_YEAR_SECONDS = 31_557_600
    def __init__(self, seconds):
        self.seconds=seconds
    def on_earth(self):
        age=self.seconds/self.EARTH_YEAR_SECONDS
        return round(age,2)
    def on_mercury(self):
        age=self.seconds/ self.EARTH_YEAR_SECONDS / 0.2408467
        return round(age,2)
    def on_venus(self):
        age = self.seconds / self.EARTH_YEAR_SECONDS / 0.61519726
        return round(age,2)
    def on_mars(self):
        age=self.seconds/self.EARTH_YEAR_SECONDS/1.8808158
        return round(age,2)
    def on_jupiter(self):
        age = self.seconds / self.EARTH_YEAR_SECONDS / 11.862615
        return round(age, 2)

    def on_saturn(self):
        age = self.seconds / self.EARTH_YEAR_SECONDS / 29.447498
        return round(age, 2)

    def on_uranus(self):
        age = self.seconds / self.EARTH_YEAR_SECONDS / 84.016846
        return round(age, 2)

    def on_neptune(self):
        age = self.seconds / self.EARTH_YEAR_SECONDS / 164.79132
        return round(age, 2)

        
