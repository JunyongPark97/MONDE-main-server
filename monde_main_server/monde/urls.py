from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from monde.views import ProductVisitAPIView
from search.category_search.views import CategorySearchViewSetV1

router = SimpleRouter()
router.register('search', CategorySearchViewSetV1, base_name='search')

urlpatterns = [
    path('visit/<int:product_id>/', ProductVisitAPIView.as_view())
]