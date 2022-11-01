from ..models import db

def db_apply(data_list:list):
    try:
        for i in data_list:
            db.session.add(i)
        db.session.commit()
    except Exception as e:
        print(e)

def join_to_json(data, name, singular_schema_1, singular_schema_2) -> list:
    result = []
    
    for row_tuple in data:
        model_1, model_2  = row_tuple
        model_1 = singular_schema_1.dump(model_1)
        model_2 = singular_schema_2.dump(model_2)
        model_1[f"{name}"] = model_2

        result.append(model_1)
    
    return result