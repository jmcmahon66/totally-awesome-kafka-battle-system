import time
import logging
from helper import *
from character import Character
from config import *
from weapons import create_weapons

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

class Battle:
    def __init__(self, hero: Character, enemy: Character) -> None:
        self.hero = hero
        self.enemy = enemy
        self.turn = 1

    def run(self) -> None:
        while True:
            print(f"==== Turn: {self.turn} ====")

            print(f"Hero health: {self.hero.health}")
            print(f"Enemy health: {self.enemy.health}")
            
            self.hero.attack(self.enemy)
            if self.enemy.health <= 0:
                print("Hero wins!")
                break
            
            self.enemy.attack(self.hero)
            if self.hero.health <= 0:
                print("Enemy wins!")
                break
                
            self.turn += 1

if __name__ == '__main__':
    weapons = create_weapons()
    hero_weapon = random.choice(weapons)
    enemy_weapon = random.choice(weapons)
    print(f"Hero weapon: {hero_weapon.name}")
    print(f"Enemy weapon: {enemy_weapon.name}")

    hero = Character(name = "Hero", health = 100, weapon = hero_weapon)
    enemy = Character(name = "Enemy", health = 100, weapon = enemy_weapon)

    battle = Battle(hero, enemy)
    battle.run()
