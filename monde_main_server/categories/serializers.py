from rest_framework import serializers

from categories.models import Shape, Color, Handle, Charm, Deco, Pattern


class ShapeSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shape
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class ColorSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class HandleSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Handle
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class CharmSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Charm
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class DecoSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deco
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class PatternSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pattern
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']
