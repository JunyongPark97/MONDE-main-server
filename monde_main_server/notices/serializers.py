# -*- encoding: utf-8 -*-
from django.contrib.auth import get_user_model
from datetime import datetime
from rest_framework import serializers

from notices.models import (Notice, PopupNotice, EventNotice, TargetPopupNotice, FAQ)

User = get_user_model()


class NoticeSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'important', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        created_at = obj.created_at.strftime('%Y-%m-%d')
        return created_at

    def get_updated_at(self, obj):
        updated_at = obj.updated_at.strftime('%Y-%m-%d')
        return updated_at


class FAQSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ('id', 'title', 'content', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')

    def get_created_at(self, obj):
        created_at = obj.created_at.strftime('%Y-%m-%d')
        return created_at

    def get_updated_at(self, obj):
        updated_at = obj.updated_at.strftime('%Y-%m-%d')
        return updated_at


class HiddenNoticeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='key')

    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')


class PopupNoticeSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = PopupNotice
        fields = ('id', 'title', 'content', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'created_at', 'updated_at')

    def get_content(self, obj):
        request = self.context['request']
        token = ''
        if request.user is not None and hasattr(request.user, 'auth_token'):
            token = request.user.auth_token.pk
        return obj.content.replace('##USER_TOKEN##', token)


class EventNoticeSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = EventNotice
        fields = ('id', 'title', 'content', 'banner', 'due_date', 'created_at', 'updated_at')
        read_only_field = ('title', 'content', 'banner', 'due_date', 'created_at', 'updated_at')

    def get_content(self, obj):
        request = self.context['request']
        token = ''
        if request.user is not None and hasattr(request.user, 'auth_token'):
            token = request.user.auth_token.pk
        return obj.content.replace('##USER_TOKEN##', token)


class TargetPopupNoticeSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = TargetPopupNotice
        fields = ('id', 'key', 'title', 'content', 'created_at', 'updated_at')
        read_only_field = ('id', 'key', 'title', 'content', 'created_at', 'updated_at')

    def get_content(self, obj):
        request = self.context['request']
        token = ''
        if request.user is not None and hasattr(request.user, 'auth_token'):
            token = request.user.auth_token.pk
        return obj.content.replace('##USER_TOKEN##', token)
