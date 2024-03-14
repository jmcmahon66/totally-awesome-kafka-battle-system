from character import Character
from config import *
from helper import *
from battle.main import Battle
from weapons import create_weapons
import random
import pytest

# def run_main():
#     battle = Battle()
#     battle.run()

# @pytest.fixture
# def characters_and_weapons():
#     weapons = create_weapons()
#     heroWeapon = random.choice(weapons)
#     enemyWeapon = random.choice(weapons)

#     startingHealth = 100

#     hero = Character(name="Hero", health=startingHealth, weapon=heroWeapon)
#     enemy = Character(name="Enemy", health=startingHealth, weapon=enemyWeapon)

#     return hero, enemy, startingHealth

# def test_character_attack(characters_and_weapons):
#     hero, enemy, startingHealth = characters_and_weapons
    
#     # Testing the attack method
#     hero.attack(enemy)
#     # Assert that enemy has taken damage
#     assert enemy.health < startingHealth  # enemy health should decrease by hero's damage

# def test_character_health_limit(characters_and_weapons):
#     hero, enemy, startingHealth = characters_and_weapons
    
#     # Testing if health cannot go below 0
#     enemy.health = 2
#     hero.attack(enemy)
#     assert enemy.health == 0  # enemy health should not go below 0

# def test_battle(characters_and_weapons):
#     hero, enemy, startingHealth = characters_and_weapons

#     # Test battle function
#     battle = Battle(hero, enemy)
#     battle.run()
#     assert (
#         (hero.health > 0 and enemy.health >= 0) or
#         (enemy.health > 0 and hero.health >= 0)
#     ), "At least one character should have health greater than 0 after battle"
