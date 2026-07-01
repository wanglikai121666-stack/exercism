import random
def modifier(score):
    return (score - 10) // 2
class Character:
    def __init__(self):
        self.strength = self.ability()
        self.dexterity = self.ability()
        self.constitution = self.ability()
        self.intelligence = self.ability()
        self.wisdom = self.ability()
        self.charisma = self.ability()
        self.hitpoints = 10 + modifier(self.constitution)
    def ability(self):
        rolls = []
        for _ in range(4):
            rolls.append(random.randint(1, 6))
        rolls.sort()
        return rolls[1] + rolls[2] + rolls[3]
