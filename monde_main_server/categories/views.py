from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from categories.models import Shape, Color, Handle, Charm, Deco, Pattern, BagIllustration
from categories.serializers import ShapeSelectListSerializer, ColorSelectListSerializer, HandleSelectListSerializer, \
    CharmSelectListSerializer, DecoSelectListSerializer, PatternSelectListSerializer, BagIllustCombineSerializer
from categories.tools import get_filtered_queryset


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


class BagIllustCombineAPIView(GenericAPIView):
    queryset = BagIllustration.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = BagIllustCombineSerializer

    def post(self, request, *args, **kwargs):
        categories = request.data['categories']
        queryset = self.get_queryset()
        for key, value in categories.items():
            queryset = get_filtered_queryset(queryset, key, value)
        bag_illust = queryset.last()
        if not bag_illust:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(bag_illust)

        return Response(serializer.data, status=status.HTTP_200_OK)
