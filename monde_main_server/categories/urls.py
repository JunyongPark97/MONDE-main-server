from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from categories.views import ColorSelectListAPIView, HandBagCategoriesViewSetV1, \
    PatternSelectListAPIView, BagIllustCombineAPIView, TypeSelectListAPIView, MiniBagCategoriesViewSet, \
    CrossBagCategoriesViewSet, BigShoulderCategoriesViewSet, ClutchBagCategoriesViewSet, BackPackCategoriesViewSet

router = SimpleRouter()
router.register('handbag', HandBagCategoriesViewSetV1, base_name='handbag')
router.register('minibag', MiniBagCategoriesViewSet, base_name='handbag')
router.register('crossbag', CrossBagCategoriesViewSet, base_name='handbag')
router.register('bigshoulderbag', BigShoulderCategoriesViewSet, base_name='handbag')
router.register('clutchbag', ClutchBagCategoriesViewSet, base_name='handbag')
router.register('backpack', BackPackCategoriesViewSet, base_name='handbag')

urlpatterns = [
    url(r'', include(router.urls)),
    path('color/', ColorSelectListAPIView.as_view()),
    path('type/', TypeSelectListAPIView.as_view()),
    path('pattern/', PatternSelectListAPIView.as_view()),
    path('result/',BagIllustCombineAPIView.as_view())
]
