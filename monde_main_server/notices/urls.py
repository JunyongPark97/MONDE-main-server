from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from notices.views import (
    EventNoticeViewSet, NoticeViewSet,
    HiddenNoticeViewSet, PopupNoticeViewSet, TargetPopupNoticeViewSet, FAQViewSet)

router = SimpleRouter()

router.register('event', EventNoticeViewSet, base_name='event')
router.register('notice', NoticeViewSet, base_name='notice')
router.register('hidden', HiddenNoticeViewSet)
router.register('faq', FAQViewSet)
router.register('popup', PopupNoticeViewSet, base_name='popup')
router.register('popup/target', TargetPopupNoticeViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]