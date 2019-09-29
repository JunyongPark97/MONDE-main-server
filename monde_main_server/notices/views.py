# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from notices.models import Notice, HiddenNotice, PopupNotice, EventNotice, TargetPopupNotice
from notices.pagination import NoticePagination, EventNoticePagination
from notices.serializers import (
    NoticeSerializer, HiddenNoticeSerializer, PopupNoticeSerializer,
    EventNoticeSerializer, TargetPopupNoticeSerializer)


class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = NoticePagination

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(hidden=False)
        return queryset.order_by('-important', '-created_at')

    def list(self, request, *args, **kwargs):
        """
        공지사항 list API입니다.
        """
        return super(NoticeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        공지사항 상세 API입니다.
        """
        return super(NoticeViewSet, self).retrieve(request, *args, **kwargs)


class HiddenNoticeViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    PLEASE, DO NOT IMPLEMENT list_route
    ('retrieve' uses string-based pk, so conflict may occur)
    """
    serializer_class = HiddenNoticeSerializer
    queryset = HiddenNotice.objects.all()
    lookup_field = 'key'

    def retrieve(self, request, *args, **kwargs):
        """
        key 값을 통해 숨겨진 특정한 공지사항 리스트를 보여주는 API입니다.
        """
        return super(HiddenNoticeViewSet, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def detail(self, requset, key=None):
        """
        key 값을 통해 숨겨진 특정한 공지사항 상세 내용을 보여주는 API입니다.
        """
        notice = HiddenNotice.objects.filter(key=key).first()
        return HttpResponse(notice.content)


class PopupNoticeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PopupNoticeSerializer
    queryset = PopupNotice.objects.all()

    def get_queryset(self):
        locale = self.request.service_locale
        queryset = PopupNotice.objects.filter(active=True, locale=locale)

        if self.request.is_ios:
            queryset = queryset.filter(ios_visible=True)

        if self.request.is_android:
            queryset = queryset.filter(android_visible=True)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        앱 시작 시 노출되는 팝업 공지사항 list API입니다.
        ---------------------
        * * *
        * view_set class   : PopupNoticeViewSet
        * serializer class : PopupNoticeSerializer
        * * *
        """
        return super(PopupNoticeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        앱 시작 시 노출되는 팝업 공지사항 상세 내용 API입니다.
        ---------------------
        * * *
        * view_set class   : PopupNoticeViewSet
        * serializer class : PopupNoticeSerializer
        * * *
        """
        return super(PopupNoticeViewSet, self).retrieve(request, *args, **kwargs)


class EventNoticeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventNoticeSerializer
    queryset = EventNotice.objects.all().order_by('-created_at')
    pagination_class = EventNoticePagination

    def list(self, request, *args, **kwargs):
        """
        이벤트 공지 리스트 API 입니다.
        """
        return super(EventNoticeViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        이벤트 공지 별 상세 내용 API 입니다.
        """
        return super(EventNoticeViewSet, self).retrieve(request, *args, **kwargs)


class TargetPopupNoticeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = TargetPopupNotice.objects.all()
    serializer_class = TargetPopupNoticeSerializer

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.queryset.filter(receivers__user=self.request.user,
                                        receivers__read_at__isnull=True)
        return None

    def get_serializer_class(self):
        if self.action == 'read':
            return serializers.Serializer
        return super(TargetPopupNoticeViewSet, self).get_serializer_class()

    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """
        팝업 공지를 "읽음" 상태로 변경하는 API입니다. (읽은 공지는 다시 보이지 않음)
        ---------------------
        * * *
        * view_set class   : TargetPopupNoticeViewSet
        * serializer class : TargetPopupNoticeSerializer
        * * *
        """
        instance = self.get_object()
        instance.receivers.filter(user=request.user).update(read_at=timezone.now())
        return Response()

    def list(self, request, *args, **kwargs):
        """
        해당 사용자에게만 보이는 팝업 공지의 리스트 API 입니다.
        ---------------------
        * * *
        * view_set class   : TargetPopupNoticeViewSet
        * serializer class : TargetPopupNoticeSerializer
        * * *
        """
        return super(TargetPopupNoticeViewSet, self).list(request, *args, **kwargs)
