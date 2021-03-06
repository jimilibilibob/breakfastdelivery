#!/usr/bin/python3
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys, getopt

def load_v6(elasticsearch_uri, mongo_uri, collection):
    _type = collection[0:len(collection)-1]
    es = Elasticsearch(elasticsearch_uri)
    es.indices.delete(index=collection, ignore=[400,404])
    es.indices.create(index=collection, ignore=[400])
    es.indices.put_mapping(
        index=collection,
        doc_type= _type,
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
    db = pymongo.MongoClient(host=[mongo_uri]).breakfastdelivery
    orders=[]
    projection = {"_id":0 }
    cur=db[collection].find({}, projection)
    nb_doc=db[collection].count_documents({})
    doc_count=0
    print("Start ... ")
    for doc in cur:
        orders.append({
            "_index": "orders",
            "_source": doc,
            "_type": _type
        })
        if len(orders) == 100000:
            doc_count+= 100000
            helpers.bulk(es, orders, request_timeout=30)
            pourcentage=(doc_count/nb_doc*100)//1
            print("Load ... "+ str(pourcentage)+"%")
            orders = []
    helpers.bulk(es, orders, request_timeout=30)
    print("Loaded ... ")

def load_v7(elasticsearch_uri, mongo_uri, collection):
    es = Elasticsearch(elasticsearch_uri)
    es.indices.delete(index=collection, ignore=[400,404])
    es.indices.create(index=collection, ignore=[400])
    es.indices.put_mapping(
        index=collection,
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
    db = pymongo.MongoClient(host=[mongo_uri]).breakfastdelivery
    orders=[]
    projection = {"_id":0 }
    cur=db[collection].find({}, projection)
    nb_doc=db[collection].count_documents({})
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

def main(argv):
    collection = 'orders'
    elasticsearch_uri = 'localhost:9200'
    mongo_uri = 'localhost:27017'
    version = 7
    try:
        opts, args = getopt.getopt(argv,"hc:e:m:v:")
    except getopt.GetoptError:
        print('mongo_to_elastic.py -c <collection> -e <elastic_endpoint> -v <elasticsearch_verion> -m <mongo_endpoint>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('mongo_to_elastic.py [args]')
            print('     -c, Collection MongoBD - Use to create Elasticsearch Index - default: "orders"')
            print('         For MongoAtlas use connection string')
            print('     -e, Elasticserch uri - default : "localhost:9200"')
            print('     -v, Major Elasticserch version - default : 7')
            print('     -m, Mongo uri - default : "localhost:27017"')
            sys.exit()
        elif opt in ("-c"):
            collection = arg
        elif opt in ("-e"):
            elasticsearch_uri = arg
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-m"):
            mongo_uri = arg
    if version < 7 :
        load_v6(elasticsearch_uri, mongo_uri, collection)
    else :
        load_v7(elasticsearch_uri, mongo_uri, collection)

if __name__ == "__main__":
    main(sys.argv[1:])