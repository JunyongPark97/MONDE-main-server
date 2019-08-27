# -*- encoding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from . import FILESERVER_HOST


class FileServerViewSet(viewsets.GenericViewSet):
    @list_route(methods=['get'])
    def host(self, request):
        """
        현재 사용중인 file server의 주소를 돌려주는 API입니다.
        """
        return Response(FILESERVER_HOST, status=status.HTTP_200_OK)
