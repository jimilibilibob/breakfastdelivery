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

def main():
    db = pymongo.MongoClient(host=['localhost:27017']).breakfastdelivery
    cur=db.orders.aggregate([
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
    plt.savefig('foo.png')
    plt.clf() 
    plt.cla() 
    plt.plot_date(dates, counts, ls='-', marker='o')
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(500))
    plt.savefig('bar_random15.png')

if __name__ == "__main__":
    main()