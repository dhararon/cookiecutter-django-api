# coding: utf8
import json
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None,
               renderer_context=None):
        response = (super(CustomJSONRenderer, self)
                    .render(data, accepted_media_type=accepted_media_type,
                            renderer_context=renderer_context))

        results = json.loads(
            response.decode('utf-8'))

        if type(results) is dict:
            results = [results]

        errors = []
        body = {}
        if renderer_context['response'].status_code >= 400:
            errors = results
        else:
            body = {
                'links': {
                    'next': None,
                    'previous': None
                },
                'count': len(results),
                "results": results
            }

        data = {
            "errors": errors,
            "body": body
        }
        data = json.dumps(data)
        return data.encode('utf-8')
