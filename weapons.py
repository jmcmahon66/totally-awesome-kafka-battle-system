import random

class Weapon:
    def __init__(self, name: str, min_damage: int, max_damage: int, value: int) -> None:
        self.name = name
        self.min_damage = min_damage
        self.max_damage = max_damage
        # self.damage = random.randint(min_damage, max_damage)
        self.value = value

def create_weapons():
    sword = Weapon(name="Sword",
               min_damage=10,
               max_damage=12,
               value=5)

    spear = Weapon(name="Spear",
               min_damage=5,
               max_damage=15,
               value=6)

    axe = Weapon(name="Axe",
             min_damage=9,
             max_damage=14,
             value=8)
    
    return [sword, spear, axe]

#TODO: Add ranged and melee type