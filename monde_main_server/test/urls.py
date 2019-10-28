from django.urls import path

from test.views import ListTestAPIView, ZIGZAGListTestAPIView

urlpatterns = [
    path('listexample', ListTestAPIView.as_view()),
    path('zigzaglist', ZIGZAGListTestAPIView.as_view())
]