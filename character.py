class Character:
    def __init__(self, name: str, health: int, damage: int) -> None:
        self.name = name # This is telling the code we want to assign values to the object
        self.health = health
        self.damage = damage

    def attack(self, target) -> None:
        target.health -= self.damage
        target.health = max(target.health, 0)