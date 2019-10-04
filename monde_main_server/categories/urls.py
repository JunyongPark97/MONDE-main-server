from django.urls import path

from categories.views import ShapeSelectListAPIView, ColorSelectListAPIView, HandleSelectListAPIView, \
    CharmSelectListAPIView, DecoSelectListAPIView, PatternSelectListAPIView

urlpatterns = [
    path('shape/', ShapeSelectListAPIView.as_view()),
    path('color/', ColorSelectListAPIView.as_view()),
    path('handle/', HandleSelectListAPIView.as_view()),
    path('charm/', CharmSelectListAPIView.as_view()),
    path('deco/', DecoSelectListAPIView.as_view()),
    path('pattern/', PatternSelectListAPIView.as_view()),
]