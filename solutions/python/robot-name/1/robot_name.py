import random
import string
class Robot:
    used_names = set()
    def __init__(self):
        self.name = self.generate_name()
    def generate_name(self):
        while True:
            letters = ""
            for _ in range(2):
                letters += random.choice(string.ascii_uppercase)
                numbers = ""

            for _ in range(3):
                numbers += random.choice(string.digits)

            name = letters + numbers
            if name not in Robot.used_names:
                Robot.used_names.add(name)
                return name
    def reset(self):
        self.name = self.generate_name()