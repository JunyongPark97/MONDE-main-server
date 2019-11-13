from django.contrib.auth import get_user_model
from rest_framework import serializers
from support.models import Official, MondeSupport


class OfficialSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Official
        fields = ('id', 'content', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        created_at = obj.created_at.strftime('%Y-%m-%d')
        return created_at

    def get_updated_at(self, obj):
        updated_at = obj.updated_at.strftime('%Y-%m-%d')
        return updated_at


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MondeSupport
        fields = ['user', 'contact_type', 'name', 'email', 'message', 'attached_file']


