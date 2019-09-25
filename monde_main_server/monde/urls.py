from django.conf.urls import url
from django.urls import path, include

from monde.views import ProductVisitAPIView, TabListAPIViewV1

urlpatterns = [
    path('visit/<int:product_id>/', ProductVisitAPIView.as_view()),
    path('shop/tab/<int:tab_no>/', TabListAPIViewV1.as_view()),
]