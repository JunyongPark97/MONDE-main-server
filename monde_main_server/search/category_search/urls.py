from django.urls import path, include
from search.category_search.views import SampleListAPIView, CursorListAPIView, MyListTestAPIView

urlpatterns = [
    #test
    path('searchresult/', SampleListAPIView.as_view()),
    path('cursor/', CursorListAPIView.as_view()),
    path('list/', MyListTestAPIView.as_view()),
]