from django.urls import path
from logs.views import FeedbackCreateAPIView


urlpatterns = [
    path('feedback/', FeedbackCreateAPIView.as_view()),
]
