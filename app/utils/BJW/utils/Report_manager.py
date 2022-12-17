# input: metadata & report data
# behavior: send report to database

import argparse
import requests
import json
import sys

API_URL = 'http://222.234.124.57:52201/security_result/createSecurityResult'

def readJsonFromFile(filepath):
    with open(filepath, 'r') as f:
        json_data = json.load(f)
    
    return json_data

def postJson(pipeline_name, stage, tool, json_data):
    global API_URL
    data = {
        "pipeline_name": pipeline_name,
        "stage": stage,
        "tool": tool,
        "data": [json_data]
    }
    response = requests.post(API_URL, json=data)
    return response

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("usage: Report_manager.py pipeline_name stage tool json_file_path")
        sys.exit()
        
    pipeline_name = sys.argv[1]
    stage = sys.argv[2]
    tool = sys.argv[3]
    json_file_path = sys.argv[4]
    
    json_data = readJsonFromFile(json_file_path)
    res = postJson(pipeline_name, stage, tool, json_data)
    
    print(f"Report_manager posted report to database, response: {res}")