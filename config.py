import socket

battle_topic = "battle"
hero_topic = "hero"
enemy_topic = "enemy"

bootstrap_servers = 'kafka:9092'

kafka_conf = {'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname(),
        'group.id': "battle",
        'auto.offset.reset': "earliest", #"earliest/latest",    
        }

hero_kafka_conf = {'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname(),
        'group.id': "hero",
        'auto.offset.reset': "earliest", #"earliest/latest",    
        }

enemy_kafka_conf = {'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname(),
        'group.id': "enemy",
        'auto.offset.reset': "earliest", #"earliest/latest",    
        }
