import time
import sys
sys.path.append("/app")  # Add container parent directory to search path
print(sys.path)
import logging
from helper import *
from character import Character
from config import *
from weapons import create_weapons
import threading
import re
from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer, Consumer, OFFSET_BEGINNING

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# while True:
#     admin_client = AdminClient(kafka_conf)
#     topic_exists = admin_client.list_topics(timeout=5).topics.get("__consumer_offsets") is not None
#     # admin_client.close()

#     if topic_exists:
#         consumer = Consumer(kafka_conf)
#         consumer.subscribe(["hero"]) #, on_assign=reset_offset) # subscribe to 'battle' for turns
#         break
#     else:
#         logger.debug("WAITING FOR KAFKA TOPIC TO BE AVAILABLE")
#         time.sleep(1)

import socket

# Kafka configuration
# bootstrap_servers = 'kafka:9092'
# topic_hero_actions = 'hero_actions'
# topic_enemy_actions = 'enemy_actions'
# topic = "topic_new"
battle_number = 1  # we want to hold this in a db
turn_time = 5  # seconds
latest_actions = []
startup = True

def create_consumer(topic):
    consumer = Consumer(kafka_conf)
    consumer.subscribe([topic])
    return consumer

producer = Producer(kafka_conf)
admin_client = AdminClient(kafka_conf)

hero_consumer = create_consumer(hero_topic)
enemy_consumer = create_consumer(enemy_topic)
# consumer = Consumer(kafka_conf)

# def delivery_callback(err, msg):
#     if err:
#         print('ERROR: Message failed delivery: {}'.format(err))
#     else:
#         print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
#             topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

# Set up a callback to handle the '--reset' flag. - optional(args)?
def reset_offset(consumer, partitions):
    # if args.reset:
    for p in partitions:
        p.offset = OFFSET_BEGINNING
    consumer.assign(partitions)

def consumer_get_value(topic, turn, action, consumer):
    logger.debug(f"Getting action from topic: {topic}")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            logger.debug(f"Waiting for {topic} action...")
            print(f"Waiting for {topic} action...")
        else:
            msg_value = msg.value().decode('utf-8')
            logger.debug(f"GOT MESSAGE: {msg_value}")

            turn_value = f"turn {turn}"
            if turn_value in msg_value:
                logger.debug(f"Got turn from {topic}")
                print(f"Got turn from {topic}")
                break

    # return msg_value
    logger.debug(f"returning {topic} action: {msg_value}")
    action.append(msg_value)
    # consumer.close()

def update_health(hero_health, enemy_health, latest_actions):
    for action in latest_actions:
        # Extract target and damage from action
        damage_pattern = r'(\d+) damage'
        match = re.search(damage_pattern, action)
        damage = int(match.group(1))
        target = action.split()[-1]
        logger.debug(f"target: {target}")
        logger.debug(f"damage: {damage}")

        # Update health based on target and damage
        if target == "hero":
            hero_health -= int(damage)
        elif target == "enemy":
            enemy_health -= int(damage)
        else:
            print(f"Invalid target: {target} in action: {action}")

    return hero_health, enemy_health

class Battle:
    def __init__(self) -> None:
        self.hero_health = 100
        self.enemy_health = 100
        self.turn = 1

    def run(self) -> None:
        hero_health = self.hero_health
        enemy_health = self.enemy_health
        # global startup
        # if startup:
        #     logger.debug("First startup, waiting before starting turns")
        #     time.sleep(50)
        #     startup = False
        #     logger.debug("DONE WAITING STARTUP")
        while True:
            print(f"==== Turn: {self.turn} ====")
            latest_actions = []

            # topic = "battle"
            logger.debug(f"PRODUCING TURN {self.turn}")
            producer.produce(battle_topic, key="turn", value=str(self.turn))

            # Multi-thread to listen for messages from both hero and enemy
            thread1 = threading.Thread(target=consumer_get_value, args=("hero", self.turn, latest_actions, hero_consumer))
            thread2 = threading.Thread(target=consumer_get_value, args=("enemy", self.turn, latest_actions, enemy_consumer))
            thread1.start()
            thread2.start()

            # wait until both threads complete
            thread1.join()
            thread2.join()
            
            logger.debug(f"latest_actions: {latest_actions}")

            # TODO: get winner by first recieved attack
            hero_health, enemy_health = update_health(hero_health, enemy_health, latest_actions)

            logger.debug(f"Hero health: {hero_health}")
            logger.debug(f"Enemy health: {enemy_health}")
            
            if enemy_health <= 0:
                winner = "Hero"
                print("Hero wins!")
                break
            
            if hero_health <= 0:
                winner = "Enemy"
                print("Enemy wins!")
                break
                
            self.turn += 1
            time.sleep(turn_time)

        producer.produce(battle_topic, key="turn", value=f"ended after {self.turn} turns - {winner.upper()} WINS!")

        # Delete topic contents after battle end??
        # topics = ["battle","hero","enemy"]
        # logger.debug("Deleting topics")
        # admin_client.delete_topics(list(topics))

if __name__ == '__main__':
    while True:
        logger.debug(f"Battle #{battle_number}")
        print(f"Battle #{battle_number}")

        # weapons = create_weapons()
        # hero_weapon = random.choice(weapons)
        # enemy_weapon = random.choice(weapons)
        # print(f"Hero weapon: {hero_weapon.name}")
        # print(f"Enemy weapon: {enemy_weapon.name}")

        # hero = Character(name = "Hero", health = 100, weapon = hero_weapon)
        # enemy = Character(name = "Enemy", health = 100, weapon = enemy_weapon)

        battle = Battle() #hero, enemy)
        battle.run()
        battle_number += 1
