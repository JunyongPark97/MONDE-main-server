from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from categories.models import Shape, Color, Handle, Charm, Deco, Pattern
from categories.serializers import ShapeSelectListSerializer, ColorSelectListSerializer, HandleSelectListSerializer, \
    CharmSelectListSerializer, DecoSelectListSerializer, PatternSelectListSerializer


class ShapeSelectListAPIView(ListAPIView):
    serializer_class = ShapeSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Shape.objects.all()


class ColorSelectListAPIView(ListAPIView):
    serializer_class = ColorSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Color.objects.all()


class HandleSelectListAPIView(ListAPIView):
    serializer_class = HandleSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Handle.objects.all()


class CharmSelectListAPIView(ListAPIView):
    serializer_class = CharmSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Charm.objects.all()


class DecoSelectListAPIView(ListAPIView):
    serializer_class = DecoSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Deco.objects.all()


class PatternSelectListAPIView(ListAPIView):
    serializer_class = PatternSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Pattern.objects.all()
