from pymongo import MongoClient
from flask import current_app
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps

from app.utils.response import resp

client = MongoClient('mongodb://localhost:27017/')
mongo_db = client["test"] # 사용하는 db 명
collection = mongo_db["securityresults"]

class SecurityResultService:
    def find(id):
        try:            
            result = collection.find_one({ "_id": ObjectId(id) })
            print(result)
            return resp(200, "success", result)
        except Exception as e:
            current_app.logger.debug("securityresult find service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def project_id_total_aggregate(id):
        # 특정 objectid 값에 대하여, very-high, high등의 count를 계산하는 쿼리
        query = [
            { "$match" : { "_id" : ObjectId(id)  } },
            { "$unwind" : "$data" },
            { "$group" : { "_id" : "$data.description.properties.precision", "count" : { "$sum" : 1 } }}
        ]
        
        try:
            result = collection.aggregate(query)
        except Exception as e:
            current_app.logger.debug("project_id collection aggregate error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
        return resp(200, "success", list(result))
    
    def all_pipeline_total_aggregate():
        query = [
            { "$unwind" : "$data" },
            { "$group" : { "_id" : "$data.description.properties.precision", "count" : { "$sum" : 1 } }}
        ]
        
        try:
            result = collection.aggregate(query)
        except Exception as e:
            current_app.logger.debug("all_pipeline collection aggregate error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
        return resp(200, "success", list(result))
    
    def pipeline_name_total_aggregate(name):
        query = [
            { "$match" : { "pipelineName" : name  } },
            { "$unwind" : "$data" },
            { "$group" : { "_id" : "$data.description.properties.precision", "count" : { "$sum" : 1 } }}
        ]
        
        try:
            result = collection.aggregate(query)
        except Exception as e:
            current_app.logger.debug("pipeline_name collection aggregate error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
        return resp(200, "success", list(result))
        
    def stage_total_aggregate():
        
        return resp(200, "success", list())
        
    def all_list():
        try:
            result = collection.find()
            # bson데이터 파싱
            result = json_util.dumps(result)
            return resp(200, "success", result)
        except Exception as e:
            return resp(500, "failed")
        
    def bibim_result_all_list():
        try:
            bibim_collection = mongo_db["bibimresults"]
            result = bibim_collection.find()
            
            return resp(200, "success", dumps(result))
        except Exception as e:
            return resp(500, "failed")
        
    def stage_issue_count():
        try:
            bibim_collection = mongo_db["bibimresults"]
            
            query = [
                { "$unwind" : "$data" },
                { "$group" : { "_id" : "$stage", "count" : { "$sum" : 1 } }}
            ]
            
            result = bibim_collection.aggregate(query)
            return resp(200, "success", list(result))
            
        except Exception as e:
            current_app.logger.debug("stage_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def project_stage_issue_count(name):
        try:
            bibim_collection = mongo_db["bibimresults"]
            
            query = [
                { "$match" : { "pipelineName" : name  } },
                { "$unwind" : "$data" },
                { "$group" : { "_id" : "$stage", "count" : { "$sum" : 1 } }}
            ]
            
            result = bibim_collection.aggregate(query)
            return resp(200, "success", list(result))
            
        except Exception as e:
            current_app.logger.debug("stage_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def accumulate_precision():
        try:
            bibim_collection = mongo_db["bibimresults"]
            
            query = [
                { "$unwind" : "$data" },
                { "$group" : { "_id" : "$data.bibimPrecision", "count" : { "$sum" : 1 } }}
            ]
            
            result = bibim_collection.aggregate(query)
            
            # 없는 값 대비
            precision_reference = {
                "Critical": 0,
                "Major": 0,
                "Minor": 0,
                "Info": 0,
                "None": 0
            }
            for row in result:
                precision_reference[row["_id"]] = row["count"]
                
            return resp(200, "success", precision_reference)
            
        except Exception as e:
            current_app.logger.debug("stage_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def project_precision(name):
        try:
            bibim_collection = mongo_db["bibimresults"]
            
            query = [
                { "$match" : { "pipelineName" : name  } },
                { "$unwind" : "$data" },
                { "$group" : { "_id" : "$data.bibimPrecision", "count" : { "$sum" : 1 } }}
            ]
            
            result = bibim_collection.aggregate(query)
            
            # 없는 값 대비
            precision_reference = {
                "Critical": 0,
                "Major": 0,
                "Minor": 0,
                "Info": 0,
                "None": 0
            }
            
            for row in result:
                precision_reference[row["_id"]] = row["count"]
                
            return resp(200, "success", precision_reference)
        
        except Exception as e:
            current_app.logger.debug("stage_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
        
    def project_date_issue_count(name):
        try:
            bibim_collection = mongo_db["bibimresults"]
            
            query = [
                { "$match" : { "pipelineName" : name  } },
                { "$sort" : { "createAt": -1 } },
                { "$unwind" : "$data" },
                { "$group" : { "_id" : "$bibimPrecision", "count" : { "$sum" : 1 } }}
            ]
            
            result = bibim_collection.aggregate(query)
            return resp(200, "success", list(result))
        
        except Exception as e:
            current_app.logger.debug("stage_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")