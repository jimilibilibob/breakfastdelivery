#!/usr/bin/python3
import json
from kafka import KafkaConsumer
import sys, getopt

def consume_v7(kafka_uri):
    consumer = KafkaConsumer("orders", bootstrap_servers=kafka_uri)
    print(consumer.bootstrap_connected())
    print(consumer.metrics())
    print(consumer.partitions_for_topic("orders"))
    print(consumer.subscribe("orders"))
    print("-")
    print(consumer.topics())

    for message in consumer:
        order = json.loads(message.value.decode())
        print("Order : ")
        print(order)
        print("--------------------")
        print(order)


def main(argv):
    kafka_uri = 'localhost:9092'
    try:
        opts, args = getopt.getopt(argv,"hk:")
    except getopt.GetoptError:
        print('producer.py -k <kafka_producer>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('producer.py -k <kafka_producer>')
            sys.exit()
        elif opt in ("-k"):
            kafka_uri = arg
    consume_v7(kafka_uri)

if __name__ == "__main__":
    main(sys.argv[1:])