from character import Character

def test_character_attack():
    hero = Character(name="Hero", health=100, damage=10)
    enemy = Character(name="Enemy", health=90, damage=5)
    
    # Testing the attack method
    hero.attack(enemy)
    print("test")
    assert enemy.health == 80  # enemy health should decrease by hero's damage