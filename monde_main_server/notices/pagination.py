from tools.pagination import CursorPagination


class NoticePagination(CursorPagination):
    page_size = 15
    ordering = ('-important', '-created_at')

class EventNoticePagination(CursorPagination):
    page_size = 15
    ordering = ('-created_at')
