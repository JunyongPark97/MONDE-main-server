from rest_framework import serializers
from logs.models import UserFeedback


class UserFeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    opinion = serializers.CharField(default=None)

    class Meta:
        model = UserFeedback
        fields = ['user', 'satisfaction', 'opinion']


