import time
import logging
from helper import *
from character import Character
from config import *
from weapons import create_weapons

from confluent_kafka import Producer, Consumer, OFFSET_BEGINNING
import socket

# Kafka configuration
bootstrap_servers = 'kafka:9092'
topic_hero_actions = 'hero_actions'
topic_enemy_actions = 'enemy_actions'
topic = "topic_new"

conf = {'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname(),
        'group.id': "battle",
        'auto.offset.reset': "earliest",    
        }
producer = Producer(conf)
consumer = Consumer(conf)

def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

# Set up a callback to handle the '--reset' flag. - needs args!
def reset_offset(consumer, partitions):
    # if args.reset:
    for p in partitions:
        p.offset = OFFSET_BEGINNING
    consumer.assign(partitions)

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
        
        producer.produce(topic, key="key3", value="value11", callback=delivery_callback)
        consumer.subscribe([topic], on_assign=reset_offset) 

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    print("Waiting...")
                elif msg.error():
                    print("ERROR: %s".format(msg.error()))
                else:
                    # Extract the (optional) key and value, and print.

                    print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                        
        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()

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
