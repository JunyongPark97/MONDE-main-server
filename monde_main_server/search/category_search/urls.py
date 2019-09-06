from django.urls import path, include
from search.category_search.views import SampleListAPIView

urlpatterns = [
    #test
    path('searchresult/', SampleListAPIView.as_view()),
]