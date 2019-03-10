from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 300

    def get_paginated_response(self, data):

        next_link = self.get_next_link()
        previous_link = self.get_previous_link()
        count = self.page.paginator.count
        return Response({
            'errors': [],
            'body': {
                'links': {
                    'next': next_link,
                    'previous': previous_link
                },
                'count': count,
                'results': data
            }
        })
