#!/usr/bin/python3

import random
import pymongo
import time 
from datetime import datetime
import sys, getopt
import math
from kafka import KafkaProducer
import json

# Create a cart
def gen_cart():
    articles = [
        {"label" :"pain au chocolat", "quantite":0, "prix_unitaire":1.30 },
        {"label" :"croissant", "quantite":0, "prix_unitaire":1.15 },
        {"label" :"crêpe", "quantite":0, "prix_unitaire":1.0 },
        {"label" :"baguette", "quantite":0, "prix_unitaire":1.0 },
        {"label" :"demi-baguette", "quantite":0, "prix_unitaire":0.6 },
        {"label" :"brioche", "quantite":0, "prix_unitaire":1.4 },
        {"label" :"pain aux raisins", "quantite":0, "prix_unitaire":1.35 },
        {"label" :"Chausson aux pommes", "quantite":0, "prix_unitaire":1.35 },
        {"label" :"lait", "quantite":0, "prix_unitaire":1.5 },
        {"label" :"café", "quantite":0, "prix_unitaire":2.0 },
        {"label" :"eau", "quantite":0, "prix_unitaire":1.0 },
        {"label" :"jus de pomme", "quantite":0, "prix_unitaire":1.6 },
        {"label" :"jus d'orange", "quantite":0, "prix_unitaire":1.8 },
    ]
    cart = {}
    cart["articles"] = []
    prix_total=0
    count_article=0
    # Number of different articles in the cart 
    nb_article = int(abs(random.gauss(0,1.8)//1)+1)
    for i in range(0,nb_article):
        index_article = random.randrange(0,len(articles))
        article = articles[index_article]
        articles.pop(index_article)
        # Quantity of "this" article 
        qte_article = abs(random.gauss(0,0.8)//1)+1
        article["quantite"] = qte_article
        prix_total+= qte_article*article["prix_unitaire"]
        count_article+= qte_article
        cart["articles"].append(article)
    cart["prix_total"]=float(prix_total)
    cart["nombre_article"]=int(count_article)
    return cart

# Get a Random client from https://opendata.paris.fr/explore/dataset/adresse_paris/information/
def get_clients(db):
    projection = { "recordid": 1, "geometry": 1, "fields.l_adr": 1, "fields.c_ar": 1, "_id":0 } 
    clients=[]
    cur=db.clients.find({}, projection)
    for doc in cur:
        clients.append(doc)
    return clients

# Create an order, with a cart, a client and a datetime
def gen_order(order_time, clients):
    client=clients[random.randrange(0,len(clients))]
    return {
        "cart": gen_cart(),
        "client": client,
        "datetime": datetime.fromtimestamp(order_time).strftime("%Y-%m-%dT%H:%M:%S+01:00") 
    }

# Create a fake streaming data source 
def fake_stream(max_time, db, producer):
    clients=get_clients(db)
    while True: 
        order_time = time.time()// 1
        wait_time=abs(random.gauss(0,max_time))
        order=gen_order(order_time,clients)
        # db.orders.insert_one(order)
        print("Order : ")
        print(order)
        producer.send("orders", json.dumps(order).encode())
        print("--------------------")
        print("Next order in (sec) : " + str(wait_time))
        time.sleep(wait_time)

def main(argv):
    median_time = 5
    kafka_uri = 'localhost:9092'
    mongo_uri = 'localhost:27017'
    try:
        opts, args = getopt.getopt(argv,"ht:k:m:")
    except getopt.GetoptError:
        print('producer.py -t <median_wait_time> -k <kafka_producer> -m <mongo_endpoint>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('producer.py -t <median_wait_time> -k <kafka_producer> -m <mongo_endpoint>')
            sys.exit()
        elif opt in ("-t"):
            median_time = int(arg)
        elif opt in ("-k"):
            kafka_uri = arg
        elif opt in ("-m"):
            mongo_uri = arg
    db = pymongo.MongoClient(host=[mongo_uri]).breakfastdelivery
    producer = KafkaProducer(bootstrap_servers=kafka_uri)
    fake_stream(median_time, db, producer)

if __name__ == "__main__":
    main(sys.argv[1:])