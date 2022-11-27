from pymongo import MongoClient
import pandas as pd

class CvssDB:
  def __init__(self, client: str ='mongodb://localhost:27017/', db_name: str="test", collecntion: str="cwe"):
    self.client = MongoClient(client)
    self.mongo_db = self.client[db_name]
    self.collection = self.mongo_db[collecntion]
    
  def insert_list(self, csv_data: dict) -> bool:
    try:
      self.collection.insert_many(csv_data)
      return True
    except Exception as e:
      print(e)
      return False
    
    
if __name__ == "__main__":
  db = CvssDB()
  
  file = pd.read_csv("cvss-total.csv") 
  if db.insert_list(file.to_dict('records')):
    print("저장완료")