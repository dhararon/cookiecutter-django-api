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
        for field, values in response.data.items():
            if isinstance(values, list):
                values = values[0]
                error = {
                    "field": field,
                    "message": str(values),
                    "code": getattr(values, 'code', 500)
                }
                error_list.append(error)

            else:
                error = {
                    "field": field,
                    "message": values.get(
                        'message', 'Internal Error 1.'),
                    "code": int(values.get('code', 500))
                }
                error_list.append(error)

        response.data = {
            "body": {},
            "errors": error_list
        }

    return response
