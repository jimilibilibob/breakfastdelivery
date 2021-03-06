#!/usr/bin/python3
import json
from kafka import KafkaConsumer
import sys, getopt
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def consume_v7(kafka_uri, elasticsearch_uri):
    es = Elasticsearch([elasticsearch_uri])
    es.indices.create(index='orders', ignore=[400])
    es.indices.put_mapping(
        index='orders',
        body={
            "properties": {
                "cart": {
                    "properties": {
                        "articles": {
                            "type": "nested",
                            "properties": {
                                "label": { 
                                    "type": "keyword" 
                                },
                                "quantite": { 
                                    "type": "integer" 
                                },
                                "prix_unitaire": { 
                                    "type": "float" 
                                },
                            }
                        },
                        "prix_total": {
                            "type": "integer"
                        },
                        "nombre_article": {
                            "type": "integer"
                        }
                    }
                },
                "client": {
                    "properties": {
                        "recordid": {
                            "type": "text"
                        },
                        "fields": {
                            "properties": {
                                "l_adr": {
                                    "type": "keyword"
                                },
                                "c_ar": {
                                    "type": "integer"
                                }
                            }
                        },
                        "geometry": {
                            "properties": {
                                "type": {
                                    "type": "text"
                                },
                                "coordinates": {
                                    "type": "geo_point"
                                }
                            }
                        }
                    }
                },
                "datetime": {
                    "type": "date",
                    "format": "strict_date_optional_time"
                }
            }
        }
    )
    consumer = KafkaConsumer("orders", bootstrap_servers=kafka_uri)
    for message in consumer:
        order = json.loads(message.value.decode())
        print("Order : ")
        print(json.dumps(order).encode('utf8'))
        print("--------------------")
        es.index('orders',order)

def main(argv):
    kafka_uri = 'localhost:9092'
    elasticsearch_uri = 'localhost:9200'
    try:
        opts, args = getopt.getopt(argv,"he:k:")
    except getopt.GetoptError:
        print('producer.py -e <elastic_endpoint> -k <kafka_producer>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('producer.py -e <elastic_endpoint> -k <kafka_producer>')
            sys.exit()
        elif opt in ("-k"):
            kafka_uri = arg
        elif opt in ("-e"):
            elasticsearch_uri = arg
    consume_v7(kafka_uri, elasticsearch_uri)

if __name__ == "__main__":
    main(sys.argv[1:])