#!/usr/bin/python3
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def main():
    es = Elasticsearch()
    es.indices.delete(index='orders', ignore=[400,404])
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
    db = pymongo.MongoClient(host=['localhost:27017']).breakfastdelivery
    orders=[]
    projection = {"_id":0 }
    cur=db.orders.find({}, projection)
    nb_doc=db.orders.count_documents({})
    doc_count=0
    print("Start ... ")
    for doc in cur:
        orders.append({
            "_index": "orders",
            "_source": doc
        })
        if len(orders) == 100000:
            doc_count+= 100000
            helpers.bulk(es, orders, request_timeout=30)
            pourcentage=(doc_count/nb_doc*100)//1
            print("Load ... "+ str(pourcentage)+"%")
            orders = []
    helpers.bulk(es, orders, request_timeout=30)
    print("Loaded ... ")

if __name__ == "__main__":
    main()