#!/usr/bin/python3

import random
import pymongo
import time 
from datetime import datetime
import sys, getopt
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

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
        "datetime": datetime.fromtimestamp(order_time)
    }

# Create a fake streaming data source 
def fake_stream():
    clients=get_clients()
    while True: 
        order_time = time.time()// 1
        wait_time=abs(random.gauss(0,2))
        order=gen_order(order_time,clients)
        db.orders.insert_one(order)
        print("Order : ")
        print(order)
        print("--------------------")
        print("Next order in (sec) : " + str(wait_time))
        time.sleep(wait_time)

def gen_dataset_exp_chaos():
    db.orders.drop()
    # 2021/01/01 06:00:00 UTC+1
    day = 380
    multiplicateur_cible = 7
    coef = math.exp(math.log(multiplicateur_cible)/day)
    coef_n = coef
    # start_time= 1609477200
    # end_time = start_time + 24 * 60 * 60* day
    # 2021/01/03 04:00:00
    end_time = 1612324800
    start_time = end_time - 24 * 60 * 60 * day
    order_time=start_time
    records=1120604
    i=1
    orders=[]
    clients=get_clients()
    mu_command=60
    print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_n) )
    while i < day+1 :
        if  datetime.fromtimestamp(order_time).hour > 19  :
            # 86400 = 1 day in sec (24*60*60)
            # Disparité entre les journées
            # Calme 0.99/1.01
            inter_stop=coef_n*1.05
            inter_start=coef_n*0.95
            coef_n=random.uniform(inter_start,inter_stop)
            start_time+=86400
            order_time=start_time
            i+=1
            if coef_n < multiplicateur_cible*1.2 :
                coef_n=coef_n*coef
            else :
                coef_n=coef_n*random.uniform(0.9,1)
            print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_n) )
        #  abs(random.gauss(0,mu_command)) ~ 0.8 * mu_command si nb tirage très grand
        # nb_command ~ (14*60*60*coef_n)/(mu_command*0.8)
        order_time+=abs(random.gauss(0,mu_command))/coef_n
        order=gen_order(order_time,clients)
        orders.append(order)
    orders.pop()
    last_interval= orders[len(orders)-1]['datetime'] - orders[len(orders)-2]['datetime']
    print("Last order interval : %s" % last_interval)
    print("%s commands" % len(orders))
    print("dataset created")
    db.orders.insert_many(orders).inserted_ids
    print("dataset imported")

def gen_dataset_exp_calm(db, coll):
    db[coll].drop()
    # 380 --> 503.2 MB || 362 for MongoAtlas
    day = 362
    multiplicateur_cible = 7
    coef = math.exp(math.log(multiplicateur_cible)/day)
    coef_n = coef
    # start_time= 1609477200
    # end_time = start_time + 24 * 60 * 60* day
    # 2021/01/03 04:00:00
    end_time = 1612324800
    start_time = end_time - 24 * 60 * 60 * day
    order_time=start_time
    i=1
    orders=[]
    clients=get_clients(db)
    mu_command=60
    print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_n) )
    while i < day+1 :
        if  datetime.fromtimestamp(order_time).hour > 19  :
            # 86400 = 1 day in sec (24*60*60)
            # Disparité entre les journées 
            # Attetnion à la tendance
            # Calme 0.95/1.05 -> 5% 
            inter_stop=1.05
            inter_start=0.95
            coef_n=coef_n*random.uniform(inter_start,inter_stop)
            start_time+=86400
            order_time=start_time
            i+=1
            if coef_n < multiplicateur_cible*1.3 :
                coef_n=coef_n*coef
            else :
                coef_n=coef_n*random.uniform(0.9,1)
            print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_n) )
        #  abs(random.gauss(0,mu_command)) ~ 0.8 * mu_command si nb tirage très grand - A démontrer
        # nb_command ~ (14*60*60*coef_n)/(mu_command*0.8) - A démontrer
        order_time+=abs(random.gauss(0,mu_command))/coef_n
        order=gen_order(order_time,clients)
        orders.append(order)
    orders.pop()
    last_interval= orders[len(orders)-1]['datetime'] - orders[len(orders)-2]['datetime']
    print("Last order interval : %s" % last_interval)
    print("%s commands" % len(orders))
    print("dataset created")
    db[coll].insert_many(orders).inserted_ids
    print("dataset imported")

def gen_dataset_linear():
    db.orders.drop()
    # 2021/01/01 06:00:00 UTC+1
    day = 12*30
    period_number=4
    period_time=day/4
    multiplicateur = 3
    coef = multiplicateur/day
    coef_d = coef
    # start_time= 1609477200
    # end_time = start_time + 24 * 60 * 60* day
    # 2021/01/03 04:00:00
    end_time = 1612324800
    start_time = end_time - 24 * 60 * 60 * day
    order_time=start_time
    records=1120604
    i=1
    orders=[]
    clients=get_clients()
    mu_command=60
    mu_random=mu_command
    print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_d) )
    while i < day+1 :
        if  datetime.fromtimestamp(order_time).hour > 19  :
            coef_d=coef_d+coef
            # 86400 = 1 day in sec (24*60*60)
            # Disparité entre les journées 
            inter_stop=mu_command*1.1
            inter_start=mu_command*0.9
            mu_random=random.uniform(inter_start,inter_stop)
            start_time+=86400
            order_time=start_time
            i+=1
            print("Day : " + str(i)+"/"+str(day) + " - Coef : " + "{:.2f}".format(coef_d) )
        #  abs(random.gauss(0,mu_command)) ~ 0.8 * mu_command si nb tirage très grand
        # nb_command ~ (14*60*60*coef_n)/(mu_command*0.8)
        order_time+=abs(random.gauss(0,mu_random))/(coef_d)
        order=gen_order(order_time,clients)
        orders.append(order)
    orders.pop()
    last_interval= orders[len(orders)-1]['datetime'] - orders[len(orders)-2]['datetime']
    print("Last order interval : %s" % last_interval)
    print("%s commands" % len(orders))
    print("dataset created")
    db.orders.insert_many(orders).inserted_ids
    print("dataset imported")

def plot_order(db, coll):
    folder='plot'
    cur=db[coll].aggregate([
        {
            "$group":{
                "_id": { "day": {"$dayOfYear": "$datetime"}, "year": { "$year": "$datetime" }},
                "price": { "$sum": "$cart.prix_total" },
                "count": { "$sum": 1 },
                "date": { "$max": "$datetime" }
            }
        },
        {
            "$sort": { "date" : 1 }
        }
    ])
    prices=[]
    dates=[]
    counts=[]
    for doc in cur:
        day, year = doc['_id']['day'], doc['_id']['year']
        pd.to_datetime(day-1, unit='D', origin=str(year))
        prices.append(doc['price'])
        dates.append( pd.to_datetime(day-1, unit='D', origin=str(year) ))
        counts.append(doc['count'])
        print("Day %s - Amount %s - Commands %s" % (doc['_id']['day'], doc['price'],doc['count']))
    plt.plot_date(dates, prices)
    plt.gcf().autofmt_xdate()
    price_name = coll +'_price.png'
    file_price_name = folder + '/' + price_name
    plt.savefig(file_price_name)
    plt.clf() 
    plt.cla() 
    plt.plot_date(dates, counts, ls='-', marker='o')
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(500))
    count_name = coll +'_count.png'
    file_count_name = folder + '/' + count_name
    plt.savefig(file_count_name)

def main(argv):
    # gen_dataset()
    coll = ''
    try:
        opts, args = getopt.getopt(argv,"hc:")
    except getopt.GetoptError:
        print('create_data.py -c <collection>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('create_data.py -c <collection>')
            sys.exit()
        elif opt in ("-c"):
            coll = arg
            db = pymongo.MongoClient(host=['localhost:27017']).breakfastdelivery
            print("Collection name : " +coll)
            gen_dataset_exp_calm(db, coll)
            plot_order(db, coll)

if __name__ == "__main__":
    main(sys.argv[1:])