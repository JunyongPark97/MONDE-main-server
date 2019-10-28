from manage.pagination import MondeCursorPagination


class NoticePagination(MondeCursorPagination):
    page_size = 15
    ordering = ('-important', '-created_at')


class EventNoticePagination(MondeCursorPagination):
    page_size = 15
    ordering = ('-created_at', )

