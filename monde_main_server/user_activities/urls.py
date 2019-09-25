from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user_activities.views import RecentViewLogViewSet, FavoriteLogViewSet, ProductFavoriteAPIView

router = SimpleRouter()
router.register('view-logs', RecentViewLogViewSet, base_name='views')
router.register('favorite-logs', FavoriteLogViewSet, base_name='favorites')

urlpatterns = [
    url(r'', include(router.urls)),
    path('favorite/<int:product_id>/', ProductFavoriteAPIView.as_view()),
]