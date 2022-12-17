from .mongoHandler import MongoHandler

class DashboardOWASP:
    owasp10 = [
        [22, 23, 35, 59, 200, 201, 219, 264, 275, 284, 285, 352, 359, 377, 402, 425, 441, 497, 538, 540, 548, 552, 566, 601, 639, 651, 668, 706, 862, 863, 913, 922, 1275],
        [261, 296, 310, 319, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 335, 336, 337, 338, 340, 347, 523, 720, 757, 759, 760, 780, 818, 916],
        [20, 74, 75, 77, 78, 79, 80, 83, 87, 88, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 113, 116, 138, 184, 470, 471, 564, 610, 643, 644, 652, 917],
        [73, 183, 209, 213, 235, 256, 257, 266, 269, 280, 311, 312, 313, 316, 419, 430, 434, 444, 451, 472, 501, 522, 525, 539, 579, 598, 602, 642, 646, 650, 653, 656, 657, 799, 807, 840, 841, 927, 1021, 1173],
        [2, 11, 13, 15, 16, 260, 315, 520, 526, 537, 541, 547, 611, 614, 756, 776, 942, 1004, 1032, 1174],
        [937, 1035, 1104],
        [255, 259, 287, 288, 290, 294, 295, 297, 300, 302, 304, 306, 307, 346, 384, 521, 613, 620, 640, 798, 940, 1216],
        [345, 353, 426, 494, 502, 565, 784, 829, 830, 915],
        [117, 223, 532, 778],
        [918]
    ]
    query = [ 
        { "$project" : { "data" : 1 } }, 
        { "$unwind" : '$data' }, 
        { "$match" : { "$or" :[] } }, # { "data.cweId" : 0 }
        { "$group" : { "_id": None, "count" : { "$sum" : 1 } } }
    ]

    def __init__(self):
        database = 'test'
        collection = 'bibimresults'
        self.mongo = MongoHandler(database, collection)
        
    def getDashboardOWASP(self):
        index = 0
        result = {}
        for i in DashboardOWASP.owasp10:
            index += 1
            ret = self._aggregate(i)
            if ret==None:
                result[index] = 0
            else:
                result[index] = ret['count']

        return result
        
    def _aggregate(self, cweList: list):
        query = [ 
            { "$project" : { "data" : 1 } }, 
            { "$unwind" : '$data' }, 
            { "$match" : { "$or" :[] } }, # { "data.cweId" : 0 }
            { "$group" : { "_id": None, "count" : { "$sum" : 1 } } }
        ]
        for item in cweList:
            query[2]['$match']['$or'].append({ "data.cweId" : item })
        
        ret = self.mongo.aggregate(query)
        for i in ret:
            return i
        
    def __del__(self):
        del self.mongo
    

if __name__=='__main__':
    dash = DashboardOWASP()
    print(dash.getDashboardOWASP())
    del dash