# -*- encoding: utf-8 -*-
from rest_framework import viewsets, permissions

from versions.serializers import VersionSerializer
from versions.models import Version

class VersionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VersionSerializer
    queryset = Version.objects.all()
    permission_classes = (permissions.AllowAny, )

    def list(self, request, *args, **kwargs):
        """
        Version list API입니다.
        """
        return super(VersionViewSet, self).list(request, *args, **kwargs)
