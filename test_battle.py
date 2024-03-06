from character import Character
from config import *
from helper import *
from main import Battle
from weapons import create_weapons
import random

# lower_damage = 5
# upper_damager = 15

# def randomise_damage():
#     return random.randint(lower_damage, upper_damager)

# def test_randomise_damage():
#     for i in range(20):
#         random_damage = randomise_damage()
#         assert lower_damage <= random_damage <= upper_damage

def test_character_attack():
    weapons = create_weapons()
    heroWeapon = random.choice(weapons)
    enemyWeapon = random.choice(weapons)

    startingHealth = 100

    hero = Character(name="Hero", health=startingHealth, weapon=heroWeapon)
    enemy = Character(name="Enemy", health=startingHealth, weapon=enemyWeapon)
    
    # Testing the attack method
    hero.attack(enemy)
    # Assert that enemy has taken damage
    assert enemy.health < startingHealth  # enemy health should decrease by hero's damage

def test_character_health_limit():
    weapons = create_weapons()
    heroWeapon = random.choice(weapons)
    enemyWeapon = random.choice(weapons)

    startingHealth = 100

    hero = Character(name="Hero", health=startingHealth, weapon=heroWeapon)
    enemy = Character(name="Enemy", health=2, weapon=enemyWeapon)
    
    # Testing if health cannot go below 0
    hero.attack(enemy)
    assert enemy.health == 0  # enemy health should not go below 0

def test_battle():
    weapons = create_weapons()
    heroWeapon = random.choice(weapons)
    enemyWeapon = random.choice(weapons)

    startingHealth = 100

    hero = Character(name="Hero", health=startingHealth, weapon=heroWeapon) 
    enemy = Character(name="Enemy", health=startingHealth, weapon=enemyWeapon)
    
    # Test battle function
    battle = Battle(hero, enemy)
    battle.run()
    assert (
        (hero.health > 0 and enemy.health >= 0) or
        (enemy.health > 0 and hero.health >= 0)
    ), "At least one character should have health greater than 0 after battle"
