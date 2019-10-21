from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from categories.views import ColorSelectListAPIView, HandBagCategoriesViewSetV1, \
    PatternSelectListAPIView, BagIllustCombineAPIView, TypeSelectListAPIView, MiniBagCategoriesViewSet, \
    CrossBagCategoriesViewSet

router = SimpleRouter()
router.register('handbag', HandBagCategoriesViewSetV1, base_name='handbag')
router.register('minibag', MiniBagCategoriesViewSet, base_name='handbag')
router.register('crossbag', CrossBagCategoriesViewSet, base_name='handbag')

urlpatterns = [
    url(r'', include(router.urls)),
    # path('shape/', ShapeSelectListAPIView.as_view()),
    path('color/', ColorSelectListAPIView.as_view()),
    path('type/', TypeSelectListAPIView.as_view()),
    # path('handle/', HandBagCategoriesViewSet.as_view()),
    # path('charm/', CharmDecoSelectListAPIView.as_view()),
    # path('deco/', DecoSelectListAPIView.as_view()),
    path('pattern/', PatternSelectListAPIView.as_view()),
    path('result/',BagIllustCombineAPIView.as_view())
]
