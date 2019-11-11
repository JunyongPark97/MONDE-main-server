from django.contrib.auth import get_user_model
from rest_framework import serializers
from support.models import Official, MondeSupport


class OfficialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Official
        fields = ('id', 'content', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MondeSupport
        fields = ['user', 'contact_type', 'name', 'email', 'message', 'attached_file']


