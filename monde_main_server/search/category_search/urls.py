from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from search.category_search.views import CategorySearchViewSetV1, RecentViewLogViewSet, ProductFavoriteViewSet

router = SimpleRouter()
router.register('search', CategorySearchViewSetV1, base_name='search')
router.register('views', RecentViewLogViewSet, base_name='views')
router.register('favorite', ProductFavoriteViewSet, base_name='favorites')

urlpatterns = [
    #test
    # path('searchresult/', SampleListAPIView.as_view()),
    url(r'', include(router.urls)),
]