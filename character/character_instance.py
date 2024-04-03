import sys
sys.path.append("/app")  # Add parent directory to search path
print(sys.path)
import os
from character import Character
from config import *
import logging
# import time
import random
# from weapons import create_weapons

from confluent_kafka import Producer, Consumer, OFFSET_BEGINNING #, AdminClient
# from confluent_kafka.admin import AdminClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set container's role in battle
character_selection = os.environ.get('CHAR_SELECTION')

if character_selection == 'hero':
    kafka_conf = hero_kafka_conf
    target = "enemy"
    logger.debug("EXECUTING HERO CODE")
    print("EXECUTING HERO CODE")
elif character_selection == 'enemy':
    kafka_conf = enemy_kafka_conf
    target = "hero"
    logger.debug("EXECUTING ENEMY CODE")
    print("EXECUTING ENEMY CODE")
else:
    logger.debug("Unrecognised character type - exiting")
    print("Unrecognised character type - exiting")
    exit(1)

# topic = "battle"
character_name = character_selection
# consumer = Consumer(hero_kafka_conf)

def reset_offset(consumer, partitions):
    # if args.reset:
    for p in partitions:
        p.offset = OFFSET_BEGINNING
    consumer.assign(partitions)

# while True:
#     admin_client = AdminClient(hero_kafka_conf)
#     topic_exists = admin_client.list_topics().topics is not None #(timeout=5).topics.get("battle") is not None
#     # admin_client.close()

#     if topic_exists:
#         consumer = Consumer(hero_kafka_conf)
#         consumer.subscribe(["battle"]) #, on_assign=reset_offset) # subscribe to 'battle' for turns
#         break
#     else:
#         logger.debug("WAITING FOR KAFKA TOPIC TO BE AVAILABLE")
#         time.sleep(1)

startup = True

# if startup:
#     logger.debug("First startup, waiting before starting turns")
#     time.sleep(10)
#     startup = False
#     logger.debug("DONE WAITING STARTUP")

consumer = Consumer(kafka_conf)
consumer.subscribe([battle_topic]) # , on_assign=reset_offset) # subscribe to 'battle' for turns

producer = Producer(kafka_conf)

def do_action(turn):
    logger.debug(f"Doing action for turn {turn}")

    # TODO: Equip weapon and generate damage from it
    damage = random.randint(10, 15)
    # enemy_damage = random.randint(10, 15)

    if "ended" in turn:
        producer.produce(character_name, key="action", value=f"{turn}")
        # producer.produce("enemy", key="action", value=f"{turn}")
    else:
        logger.debug(f"turn {turn} - {character_name} deals {damage} damage to {target}")
        producer.produce(character_name, key="action", value=f"turn {turn} - {character_name} deals {damage} damage to {target}") #str(self.turn))
        # producer.produce("enemy", key="action", value=f"turn {turn} - enemy deals {enemy_damage} damage to hero") #str(self.turn))

turn = ""

while True:
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                if turn:
                    next_turn = int(turn) + 1
                    # next_turn_str = str(next_turn)
                    logger.debug(f"Waiting for turn {next_turn}...")
                    print(f"Waiting for turn {next_turn}...")
                else:
                    logger.debug("Waiting for first turn...")
                    print("Waiting for first turn")
            elif msg.error():
                logger.debug("ERROR: %s".format(msg.error()))
                print("ERROR: %s".format(msg.error()))
            else:
                logger.debug("GOT TURN FROM BATTLE")
                # Extract the (optional) key and value, and print.
                logger.debug("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))                

                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

                turn = value=msg.value().decode('utf-8')

                do_action(turn)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
