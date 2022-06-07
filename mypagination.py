from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


# Page Number Pagination
class MyCustomPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page_no'
    page_size_query_param = 'page_size'
    max_page_size = 10

class MyCustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'of'


class MyCustomCursorPagination(CursorPagination):
    page_size = 1
