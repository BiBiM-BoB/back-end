from pymongo import MongoClient
from flask import current_app
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps
from dotenv import load_dotenv
import os

from app.utils.response import resp
from ..utils.mongoHandler import MongoHandler
from ..utils.dashboardOwasp import DashboardOWASP

client = MongoClient('mongodb://localhost:27017/')
mongo_db = client["test"] # 사용하는 db 명
collection = mongo_db["securityresults"]

load_dotenv()
JENKINS_URL = os.environ.get("JENKINS_URL")
JENKINS_ID = os.environ.get("JENKINS_ID")
JENKINS_PW = os.environ.get("JENKINS_PW")

def _getProjectPrecisions(name):
    bibim_collection = mongo_db["bibimresults"]
    query = [
        { "$match" : { "pipelineName" : name  } },
        { "$unwind" : "$data" },
        { "$group" : { "_id" : "$data.bibimPrecision", "count" : { "$sum" : 1 } }}
    ]
        
    result = bibim_collection.aggregate(query)
    
    # 없는 값 대비
    precision_reference = {
        "precision" : {
            "Critical": 0,
            "Major": 0,
            "Minor": 0,
            "Info": 0,
            "None": 0
        },
        "grade": ""
    }
    
    sigma_s = 0
    
    for row in result:
        precision_reference["precision"][row["_id"]] = row["count"]
        sigma_s += row["count"]
        
    epsilon_e = 0.2
    epsilon_d = 0.2
    epsilon_c = 0.2
    epsilon_b = 0.2
    otherwise = 1 - (epsilon_e + epsilon_d + epsilon_c + epsilon_b)
    
    if(sigma_s == 0):
        sigma_s = 0.00001
    
    if(epsilon_e <= (precision_reference["precision"]["Critical"] / sigma_s)):
        precision_reference["grade"] = "E"
    elif(epsilon_d <= (precision_reference["precision"]["Major"] / sigma_s)):
        precision_reference["grade"] = "D"
    elif(epsilon_c <= (precision_reference["precision"]["Minor"] / sigma_s)):
        precision_reference["grade"] = "C"
    elif(epsilon_b <= (precision_reference["precision"]["Info"] / sigma_s)):
        precision_reference["grade"] = "B"
    elif(otherwise <= (precision_reference["precision"]["None"] / sigma_s)):
        precision_reference["grade"] = "A"
    
    return precision_reference

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
            
            from app.utils.BJW.core.jenkins import Jenkins

            jen = Jenkins(JENKINS_URL, JENKINS_ID, JENKINS_PW)
            pipeline_names = jen.get_pipelines(simple=True)
            
            precision_reference = {
                "precision" : {
                    "Critical": 0,
                    "Major": 0,
                    "Minor": 0,
                    "Info": 0,
                    "None": 0
                },
                "grade": {
                    "A": 0,
                    "B": 0,
                    "C": 0,
                    "D": 0,
                    "E": 0
                },
            }
            
            sigma_s = 0
            
            # 전체 precision 구하기
            for row in result:
                precision_reference["precision"][row["_id"]] = row["count"]
                sigma_s += row["count"]
            
            # 각 파이프라인별 grade 개수 추가
            for name in pipeline_names:
                pipeline_precision = _getProjectPrecisions(name)
                if(pipeline_precision["grade"] == ""):
                    pass
                else:
                    precision_reference["grade"][pipeline_precision["grade"]] += 1
                
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
                "precision" : {
                    "Critical": 0,
                    "Major": 0,
                    "Minor": 0,
                    "Info": 0,
                    "None": 0
                },
                "grade": "",
                "qualityGate": False
            }
            
            sigma_s = 0
            
            for row in result:
                precision_reference["precision"][row["_id"]] = row["count"]
                sigma_s += row["count"]
            
            epsilon_e = 0.2
            epsilon_d = 0.2
            epsilon_c = 0.2
            epsilon_b = 0.2
            otherwise = 1 - (epsilon_e + epsilon_d + epsilon_c + epsilon_b)
            epsilon_p = 0.2
            
            if(epsilon_e <= (precision_reference["precision"]["Critical"] / sigma_s)):
                precision_reference["grade"] = "E"
            elif(epsilon_d <= (precision_reference["precision"]["Major"] / sigma_s)):
                precision_reference["grade"] = "D"
            elif(epsilon_c <= (precision_reference["precision"]["Minor"] / sigma_s)):
                precision_reference["grade"] = "C"
            elif(epsilon_b <= (precision_reference["precision"]["Info"] / sigma_s)):
                precision_reference["grade"] = "B"
            elif(otherwise <= (precision_reference["precision"]["None"] / sigma_s)):
                precision_reference["grade"] = "A"
            
            quality = ((precision_reference["precision"]["Critical"] + precision_reference["precision"]["Major"]) / sigma_s)
            
            if(epsilon_p >= quality):
                precision_reference["qualityGate"] = True
            else:
                precision_reference["qualityGate"] = False
                
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
            current_app.logger.debug("project_date_issue_count service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
    
    def dashboard_cwe25():
        try:
            database = 'test'
            collection = 'bibimresults'
            mongo = MongoHandler(database, collection)
            
            result = {}
            cwe25 = [787, 79, 89, 20, 125, 78, 416, 22, 352, 434, 476, 502, 190, 287, 798, 862, 77, 306, 119, 276, 918, 362, 400, 611, 94]
            
            for i in cwe25:
                result[i] = 0
                
            class test:
                def cwe(data: list) -> dict:
                    # top25 = [0 for i in range(len(test.cwe25))]
                    for item in data:
                        if item['cweId'] in cwe25:
                            index = item['cweId']
                            result[index] += 1
                            
                    # result = { key:value for key, value in zip(test.cwe25, top25) }
                    return True
                
            for i in mongo._getFindIterator():
                test.cwe(i['data'])
                
            del mongo
            return resp(200, "success", result)
        except Exception as e:
            current_app.logger.debug("dashboard_cwe25() service error")
            current_app.logger.debug(e)
            return resp(500, "failed")
    
    def dashboard_owasp10():
        try:
            dash = DashboardOWASP()
            result = dash.getDashboardOWASP()
            
            return resp(200, "success", result)
        except Exception as e:
            current_app.logger.debug("dashboard_owasp10() service error")
            current_app.logger.debug(e)
            return resp(500, "failed")