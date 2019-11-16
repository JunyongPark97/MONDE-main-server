from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from categories.models import Shape, Color, Type, Pattern, BagIllustration, TypeTag, Charm, Deco
from categories.serializers import ShapeSelectListSerializer, ColorSelectListSerializer, HandleSelectListSerializer, \
    CharmSelectListSerializer, PatternSelectListSerializer, BagIllustCombineSerializer, DecoSelectListSerializer
from categories.tools import get_filtered_queryset

"""
일러스트 뿌려줄 때 사용하는 API
"""


class TypeSelectListAPIView(ListAPIView):
    """
    처음 검색 페이지 클릭시 호출되는 API입니다.
    Type(Handle) 선택시 사용하는 일러스트와 이름을 return합니다.
    """
    serializer_class = HandleSelectListSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Type.objects.filter(active=True).order_by('order')


class HandBagCategoriesViewSetV1(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(HandBagCategoriesViewSetV1, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_handbag=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_handbag=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_handbag=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MiniBagCategoriesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(MiniBagCategoriesViewSet, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_mini=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_mini=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_mini=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CrossBagCategoriesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(CrossBagCategoriesViewSet, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_cross=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_cross=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_cross=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BigShoulderCategoriesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(BigShoulderCategoriesViewSet, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_big_shoulder=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_big_shoulder=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_big_shoulder=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClutchBagCategoriesViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(ClutchBagCategoriesViewSet, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_clutch=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_clutch=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_clutch=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BackPackCategoriesViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    """
    [DEPRECATED]
    """

    def get_serializer_class(self):
        if self.action == 'shape':
            return ShapeSelectListSerializer
        elif self.action == 'charm':
            return CharmSelectListSerializer
        elif self.action == 'deco':
            return DecoSelectListSerializer
        return super(BackPackCategoriesViewSet, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        queryset = Shape.objects.filter(type__is_backpack=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charm(self, request):
        queryset = Charm.objects.filter(type__is_backpack=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def deco(self, request):
        queryset = Deco.objects.filter(type__is_backpack=True).order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ColorSelectListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ColorSelectListSerializer
    queryset = Color.objects.all()


class PatternSelectListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PatternSelectListSerializer
    queryset = Pattern.objects.all()


class BagIllustCombineAPIView(GenericAPIView):
    """
    [DEPRECATED]
    """
    queryset = BagIllustration.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = BagIllustCombineSerializer

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # categories update by input
        temp = self._whole_categories()
        categories = request.data['categories']
        temp.update(categories)

        for key, value in temp.items():
            queryset = get_filtered_queryset(queryset, key, value)

        bag_illust = queryset.last()
        if not bag_illust:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(bag_illust)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def _whole_categories():
        categories = {}
        categories['shape'] = None
        categories['color'] = None
        categories['handle'] = None
        categories['charm'] = None
        categories['deco'] = None
        categories['pattern'] = None
        return categories
