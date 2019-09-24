from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user_activities.views import RecentViewLogViewSet, ProductFavoriteViewSet

router = SimpleRouter()
router.register('views', RecentViewLogViewSet, base_name='views')
router.register('favorite', ProductFavoriteViewSet, base_name='favorites')

urlpatterns = [
    url(r'', include(router.urls)),
]