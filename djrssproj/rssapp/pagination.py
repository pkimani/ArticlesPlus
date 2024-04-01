# rssapp/pagination.py
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs

class ArticleCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'i'
    cursor_query_param = 'c'
    ordering = '-publication_date'

    def get_ordering(self, request, queryset, view):
        sort_by = request.query_params.get('s')
        if sort_by == 'score':
            return ['-score', '-publication_date', '-id']
        return [self.ordering, '-id']

    def get_paginated_response(self, data):
        return Response({
            'next_cursor': self.get_cursor_from_link(self.get_next_link()),
            'previous_cursor': self.get_cursor_from_link(self.get_previous_link()),
            'results': data
        })

    def get_cursor_from_link(self, link):
        if link:
            query_params = parse_qs(urlparse(link).query)
            return query_params.get(self.cursor_query_param, [None])[0]
        return None