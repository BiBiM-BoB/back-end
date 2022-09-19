from flask import Response
import json

msgDict = {
    200: 'OK',
    201: 'Created',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    409: 'Conflict',
    500: 'Internal Server Error'
}

def resp(status_code:int, msg:str = "", data:str = ""):
    data_format = {
        'msg': None,
        'status': None,
        'result': None
    }

    try:
        if(msg):
            data_format['msg'] = msg
            data_format['status'] = status_code
            data_format['result'] = data
        else:
            data_format['msg'] = msgDict[status_code]
            data_format['status'] = status_code
            data_format['result'] = data
    except Exception as e:
        print(e)
        data_format['msg'] = msgDict[500]
        data_format['status'] = 500
        data_format['result'] = None
    finally:
        return Response(json.dumps(data_format, indent=4, default=str), mimetype='application/json')


