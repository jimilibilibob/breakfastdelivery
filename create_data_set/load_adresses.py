#!/usr/bin/python3

import pymongo
import json

def main():
    nb_req = 150
    size=1000
    db = pymongo.MongoClient(host=['localhost:27017']).breakfastdelivery
    db.clients.drop()
    with open('./data/adresse_paris.json') as json_file:
        data = json.load(json_file)
        db.clients.insert_many(data).inserted_ids


if __name__ == "__main__":
    main()