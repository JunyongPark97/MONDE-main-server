from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from notices.views import (
    EventNoticeViewSet, NoticeViewSet,
    HiddenNoticeViewSet, PopupNoticeViewSet, TargetPopupNoticeViewSet)

router = SimpleRouter()

router.register('event', EventNoticeViewSet, base_name='event-student')
router.register('notice', NoticeViewSet, base_name='student')
router.register('hidden', HiddenNoticeViewSet)
router.register('popup', PopupNoticeViewSet, base_name='popup-student')
router.register('popup/target', TargetPopupNoticeViewSet)

urlpatterns = [
    url(r'', include(router.urls, namespace='api')),
]