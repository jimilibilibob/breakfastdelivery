import pymongo
import sys, getopt
import config

def local_to_atlas(coll):
    # Local :
    local = pymongo.MongoClient(host=['localhost:27017']).breakfastdelivery
    # Atlas :
    uri = 'mongodb+srv://'+ config.user +':'+ config.password +'@cluster.wnj7k.mongodb.net/' + config.cluster +'?retryWrites=true&w=majority'
    altas = pymongo.MongoClient(uri).breakfastdelivery
    orders=[]
    print("Get documents...")
    cursor = local[coll].find({})
    for document in cursor:
        orders.append(document)
    print("Upload document...")
    altas[coll].insert_many(orders)
    print("Done")

def main(argv):
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
            print("Collection name : " +coll)
            local_to_atlas(coll)

if __name__ == "__main__":
    main(sys.argv[1:])