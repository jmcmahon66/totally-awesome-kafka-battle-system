import time
import logging
from helper import *
from character import Character
from config import *

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

class Battle:
    def __init__(self, hero: Character, enemy: Character) -> None:
        self.hero = hero
        self.enemy = enemy
        self.turn = 0

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
    heroDamage = randomise_damage()
    enemyDamage = randomise_damage()

    hero = Character(name = "Hero", health = 100, damage = heroDamage)
    enemy = Character(name = "Enemy", health = 90, damage = enemyDamage)

    battle = Battle(hero, enemy)
    battle.run()
