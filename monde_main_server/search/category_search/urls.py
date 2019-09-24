from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from search.category_search.views import CategorySearchViewSetV1

router = SimpleRouter()
router.register('search', CategorySearchViewSetV1, base_name='search')

urlpatterns = [
    url(r'', include(router.urls)),
]