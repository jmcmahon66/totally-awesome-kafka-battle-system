from character import Character
from config import *
from helper import *
from main import battle
import random

# lower_damage = 5
# upper_damager = 15

# def randomise_damage():
#     return random.randint(lower_damage, upper_damager)

def test_randomise_damage():
    for i in range(20):
        random_damage = randomise_damage()
        assert lower_damage <= random_damage <= upper_damager

def test_character_attack():
    heroDamage = randomise_damage()
    enemyDamage = randomise_damage()

    startingHealth = 100

    hero = Character(name="Hero", health=startingHealth, damage=heroDamage)
    enemy = Character(name="Enemy", health=startingHealth, damage=enemyDamage)
    
    # Testing the attack method
    hero.attack(enemy)
    # Assert that enemy has taken damage
    assert enemy.health < startingHealth  # enemy health should decrease by hero's damage

def test_character_health_limit():
    heroDamage = 100
    enemyHealth = 90
    enemyDamage = randomise_damage()

    hero = Character(name="Hero", health=100, damage=heroDamage)
    enemy = Character(name="Enemy", health=enemyHealth, damage=enemyDamage)
    
    # Testing if health cannot go below 0
    hero.attack(enemy)
    assert enemy.health == 0  # enemy health should not go below 0

def test_battle():
    hero = Character(name="Hero", health=100, damage=10)
    enemy = Character(name="Enemy", health=90, damage=5)
    
    # Test battle function
    battle(hero, enemy)
    assert hero.health >= 0 or enemy.health >= 0  # At least one character should have health greater than 0 after battle
