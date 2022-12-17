import pymongo

class MongoHandler:
    def __init__(self, database, collection, host='localhost', port=27017):
        self._host = host
        self._port = port
        self._database = database
        self._collection = collection
        self._mongo_client = None
        self._mongo_db = None
        self._mongo_collection = None
        self._connect_db()

    def _connect_db(self):
        self._mongo_client = pymongo.MongoClient(self._host, self._port)
        self._mongo_db = self._mongo_client[self._database]
        self._mongo_collection = self._mongo_db[self._collection]

    # condition
    def count_documents(self, condition=None):
        return self._mongo_collection.count_documents()

    def estimated_document_count(self):
        return self._mongo_collection.estimated_document_count()

    def get_recent_N_Iterator(self, N):
        return self._mongo_collection.find().sort("_id", pymongo.DESCENDING).limit(N)
        
    def insert(self, data):
        if isinstance(data, list):
            self._mongo_collection.insert(data)
        elif isinstance(data, dict):
            self._mongo_collection.insert_one(data)

    def find(self, condition):
        return self._mongo_collection.find(condition)

    def _getFindIterator(self):
        return self._mongo_collection.find()
    
    def aggregate(self, pipeline):
        return self._mongo_collection.aggregate(pipeline)

    def __del__(self):
        self._mongo_client.close()

'''
    def delete(self, condition):
        self._mongo_collection.remove(condition)

    def update(self, condition, data):
        self._mongo_collection.update(condition, {"$set": data})

    def get_recent_N(collection, N):
        # collection : pymongo.collection.Collection 객체
        # N : 조회할 데이터 개수

        cursor = collection.find().sort("_id", pymongo.DESCENDING).limit(N)
        return list(cursor)
'''