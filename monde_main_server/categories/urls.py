from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from categories.views import ColorSelectListAPIView, HandBagCategoriesViewSetV1, \
    PatternSelectListAPIView, BagIllustCombineAPIView, TypeSelectListAPIView, MiniBagCategoriesViewSet, \
    CrossBagCategoriesViewSet, BigShoulderCategoriesViewSet, ClutchBagCategoriesViewSet, BackPackCategoriesViewSet

router = SimpleRouter()
router.register('hand_bag', HandBagCategoriesViewSetV1, base_name='handbag')
router.register('mini_bag', MiniBagCategoriesViewSet, base_name='handbag')
router.register('cross_bag', CrossBagCategoriesViewSet, base_name='handbag')
router.register('big_shoulder', BigShoulderCategoriesViewSet, base_name='handbag')
router.register('clutch_bag', ClutchBagCategoriesViewSet, base_name='handbag')
router.register('backpack', BackPackCategoriesViewSet, base_name='handbag')

urlpatterns = [
    url(r'', include(router.urls)),
    path('color/', ColorSelectListAPIView.as_view()),
    path('type/', TypeSelectListAPIView.as_view()),
    path('pattern/', PatternSelectListAPIView.as_view()),
    # path('result/',BagIllustCombineAPIView.as_view())

]
