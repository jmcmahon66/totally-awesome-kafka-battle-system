import time
import logging
from helper import myfunction
from character import Character
# import sys

logging.basicConfig(level=logging.DEBUG) #, stream=sys.stdout)
logger = logging.getLogger(__name__)

i = 0

# class Hero:

# class Enemy:
#     def __init__(self, )

hero = Character(name = "Hero", health = 100, damage = 10)
enemy = Character(name = "Enemy", health = 90, damage = 5)

def battle():
    global i
    while True:
        hero.attack(enemy)
        if enemy.health <= 0:
            logger.debug("Hero wins!")
            break
        enemy.attack(hero)
        if hero.health <= 0:
            logger.debug("Enemy wins!")
            break

        logger.debug(f"turn: {i}")
        logger.debug(f"Hero health: {hero.health}")
        logger.debug(f"Enemy health: {enemy.health}")

        i += 1

if __name__ == '__main__':
    battle()

    # while i < 5:
    #     i += 1
    #     print(i)
    #     string = myfunction()
    #     logger.debug(f"test {string} {i}")
    #     time.sleep(5)