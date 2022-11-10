from pymongo import MongoClient
from flask import current_app
from bson import json_util
from bson.objectid import ObjectId

from app.utils.response import resp

client = MongoClient('mongodb://localhost:27017/')
mongo_db = client["test"] # 사용하는 db 명
collection = mongo_db["securityresults"]

class SecurityResultService:
    def find(id):
        try:            
            result = collection.find_one({ "_id": ObjectId(id) })    
            return resp(200, "success", result)
        except Exception as e:
            current_app.logger.debug("securityresult find service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def project_total_aggregate(id):
        query = [
            { "$match" : { "_id" : id  } },
            { "$unwind" : "$data" },
            { "$group" : { "_id" : "$data.properties.precision", "count" : { "$sum" : 1 } }}
        ]
        result = collection.aggregate(query)
        
        import pprint
        pprint.pprint(list(result))
        

    def all_list():
        try:
            result = collection.find()
            # bson데이터 파싱
            result = json_util.dumps(result)
            return resp(200, "success", result)
        except Exception as e:
            return resp(500, "failed")