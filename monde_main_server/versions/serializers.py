# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import Version


class VersionSerializer(serializers.ModelSerializer):
    version = serializers.SerializerMethodField()

    class Meta:
        model = Version
        fields = ('name', 'version')

    def get_version(self, instance):
        return instance.version

