from ..models import db

def db_apply(data_list:list):
    try:
        for i in data_list:
            db.session.add(i)
        db.session.commit()
    except Exception as e:
        print(e)