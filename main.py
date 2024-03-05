import time
import logging
from helper import *
from character import Character
from config import *
# import sys

logging.basicConfig(level=logging.DEBUG) #, stream=sys.stdout)
logger = logging.getLogger(__name__)

i = 0

# class Hero:

# class Enemy:
#     def __init__(self, )

# hero = Character(name = "Hero", health = 100, damage = 10)
# enemy = Character(name = "Enemy", health = 90, damage = 5)

# def battle(hero, enemy):
#     global i
#     while True:
#         hero.attack(enemy)
#         if enemy.health <= 0:
#             logger.debug("Hero wins!")
#             break
#         enemy.attack(hero)
#         if hero.health <= 0:
#             logger.debug("Enemy wins!")
#             break

#         logger.debug(f"turn: {i}")
#         logger.debug(f"Hero health: {hero.health}")
#         logger.debug(f"Enemy health: {enemy.health}")

#         i += 1

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

    # while i < 5:
    #     i += 1
    #     print(i)
    #     string = myfunction()
    #     logger.debug(f"test {string} {i}")
    #     time.sleep(5)