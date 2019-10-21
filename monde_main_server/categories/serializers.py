from rest_framework import serializers

from categories.models import Shape, Color, Type, CharmDeco, Pattern, BagIllustration


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
        model = Type
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']


class CharmDecoSelectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharmDeco
        fields = ['id', 'image', 'name']
        read_only_fields = ['image', 'name']

#
# class DecoSelectListSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Deco
#         fields = ['id', 'image', 'name']
#         read_only_fields = ['image', 'name']


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
