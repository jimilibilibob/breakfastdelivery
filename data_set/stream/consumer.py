#!/usr/bin/python3
import json
from kafka import KafkaConsumer
import sys
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def consume():
    es = Elasticsearch()
    consumer = KafkaConsumer("Orders", bootstrap_servers='127.0.0.1:9092')
    for message in consumer:
        order = json.loads(message.value.decode())
        print(order)
        es.index('orders',order)


def main(argv):
    consume()

if __name__ == "__main__":
    main(sys.argv[1:])