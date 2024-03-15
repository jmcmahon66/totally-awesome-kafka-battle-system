import sys
sys.path.append("/app")  # Add parent directory to search path
print(sys.path)

from character import Character
from config import *
import logging
import time
import random
from weapons import create_weapons

from confluent_kafka import Producer, Consumer, OFFSET_BEGINNING #, AdminClient
from confluent_kafka.admin import AdminClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# topic = "battle"
character_name = "hero"
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

consumer = Consumer(hero_kafka_conf)
consumer.subscribe([battle_topic], on_assign=reset_offset) # subscribe to 'battle' for turns

producer = Producer(kafka_conf)

def do_action(turn):
    logger.debug(f"Doing action for turn {turn}")

    hero_damage = random.randint(10, 15)
    enemy_damage = random.randint(10, 15)

    if "ended" in turn:
        producer.produce(character_name, key="action", value=f"{turn}")
        producer.produce("enemy", key="action", value=f"{turn}")
    else:
        producer.produce(character_name, key="action", value=f"turn {turn} - hero deals {hero_damage} damage to enemy") #str(self.turn))
        producer.produce("enemy", key="action", value=f"turn {turn} - enemy deals {enemy_damage} damage to hero") #str(self.turn))

while True:
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                logger.debug("Waiting for turn...")
                print("Waiting for turn...")
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
