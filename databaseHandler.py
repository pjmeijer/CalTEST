import pymongo
import json

def connect(database):
    myclient = pymongo.MongoClient("mongodb://fsdkma018:27017/")
    #database = myclient["rbaDB"]
    database = myclient["rbaDB"]

def write_to_database(database, json_str):
    record = json.dumps(json_str)
    #print(record)
    dbCollection = database['CalQC']
    #x = dbCollection.replace_one({ } ,record,upsert=True)
    
#def search_database(database, json_obj):