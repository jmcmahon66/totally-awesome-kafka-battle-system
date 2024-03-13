from weapons import *
import random

class Character:
    def __init__(self, name: str, health: int, weapon: Weapon) -> None:
        self.name = name # This is telling the code we want to assign values to the object
        self.health = health
        self.weapon = weapon
        # self.damage = damage

    def attack2(self) -> None:
        damage = random.randint(self.weapon.min_damage, self.weapon.max_damage)
        # logger.debug(f"{self.weapon.name} does {damage} to {target.name}")
        return damage

    def attack(self, target) -> None:
        damage = random.randint(self.weapon.min_damage, self.weapon.max_damage)
        print(f"{self.weapon.name} does {damage} to {target.name}")
        target.health -= damage
        target.health = max(target.health, 0)