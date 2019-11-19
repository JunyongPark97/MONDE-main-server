from rest_framework import serializers
from monde.models import MainPageImage


class MainPageImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainPageImage
        fields = ['image_url']
