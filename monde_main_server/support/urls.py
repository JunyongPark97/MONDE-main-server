from django.conf.urls import url
from django.urls import path, include
from support.views import OfficialViewSet, ContactViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('official', OfficialViewSet)
router.register('contact', ContactViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]