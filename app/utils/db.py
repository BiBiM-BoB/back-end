from ..models import db
import json
import pandas as pd


def db_apply(data_list:list):
    try:
        for i in data_list:
            db.session.add(i)
        db.session.commit()
    except Exception as e:
        print(e)

def query2json(query):
    query_df = pd.read_sql(query.statement, query.session.bind).to_json(orient='records')
    jsonstringify_data = json.loads(query_df)
    return jsonstringify_data