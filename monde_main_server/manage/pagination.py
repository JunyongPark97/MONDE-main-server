from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from urllib import parse as urlparse
from base64 import b64decode, b64encode


def _reverse_ordering(ordering_tuple):
    """
    Given an order_by tuple such as `('-created', 'uuid')` reverse the
    ordering and return a new tuple, eg. `('created', '-uuid')`.
    """

    def invert(x):
        return x[1:] if x.startswith('-') else '-' + x

    return tuple([invert(item) for item in ordering_tuple])


class ProductListPagination(PageNumberPagination):
<<<<<<< Updated upstream
    page_size = 30  # 한페이지에 담기는 개수
=======
    page_size = 50  # 한페이지에 담기는 개수
>>>>>>> Stashed changes

    def get_next_page_num(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_prev_page_num(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('current', self.page.number),
             ('next', self.get_next_page_num()),
             ('previous', self.get_prev_page_num()),
             ('products', data)
         ]))


class FavoriteLogPagination(ProductListPagination):
    page_size = 100


class MondeCursorPagination(CursorPagination):
    # page_size = ...
    # ordering = ...

    def get_paginated_response(self, data):
        response = Response(data)
        response['cursor-prev'] = self.get_previous_link()
        response['cursor-next'] = self.get_next_link()
        return response

    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded


def paginate(page_size=None, ordering=None):

    class _Pagination(MondeCursorPagination):
        def __init__(self):
            self.page_size = page_size
            self.ordering = ordering

    def decorator(_class):
        _class.pagination_class = _Pagination
        return _class

    return decorator


from django.core.paginator import Paginator
class FixedCountAdminPaginator(Paginator):
    '''
    Admin에서 user등 row count가 매우 많은 경우, count를 세는데 걸리는 시간이 오래걸려 페이징 과정에 시간이 오래 걸립니다.
    이를 줄이기 위해 count를 강제로 500으로 고정함.
    '''
    @property
    def count(self):
        return 500
