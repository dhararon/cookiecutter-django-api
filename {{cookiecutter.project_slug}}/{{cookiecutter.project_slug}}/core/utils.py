# coding: utf8
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    if 'detail' in response.data:
        if hasattr(response.data['detail'], 'code'):
            code = response.data['detail'].code
        else:
            code = 100

        response.data = {
            "body": {},
            "errors": [{
                "message": response.data['detail'],
                "code": code
            }]
        }

    else:
        error_list = []
        for field in response.data.keys():
            error = {
                "field": field,
                "message": response.data[field].get(
                    'message', 'Internal Error 1.'),
                "code": int(response.data[field].get('code', 500))
            }
            error_list.append(error)

        response.data = {
            "body": {},
            "errors": error_list
        }

    return response
