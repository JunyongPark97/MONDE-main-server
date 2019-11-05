from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from logs.models import UserFeedback
from logs.serializers import UserFeedbackSerializer


class FeedbackCreateAPIView(CreateAPIView):
    queryset = UserFeedback.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFeedbackSerializer
