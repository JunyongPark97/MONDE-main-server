from rest_framework import serializers

from categories.models import Shape, Color, Type, Pattern, BagIllustration, Charm, Deco


class ShapeSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shape
        fields = ['id', 'image', 'name', 'detail']
        read_only_fields = ['image', 'name', 'detail']


class ColorSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class HandleSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class CharmSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Charm
        fields = ['id', 'image', 'name', 'detail']
        read_only_fields = ['image', 'name', 'detail']


class DecoSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deco
        fields = ['id', 'image', 'name', 'detail']
        read_only_fields = ['image', 'name', 'detail']


class PatternSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pattern
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class BagIllustCombineSerializer(serializers.ModelSerializer):

    class Meta:
        model = BagIllustration
        fields = ['id', 'image']
        read_only_fields = ['image']
