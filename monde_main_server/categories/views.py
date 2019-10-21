from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from categories.models import Shape, Color, Type, CharmDeco, Pattern, BagIllustration, TypeTag
from categories.serializers import ShapeSelectListSerializer, ColorSelectListSerializer, HandleSelectListSerializer, \
    CharmDecoSelectListSerializer, PatternSelectListSerializer, BagIllustCombineSerializer
from categories.tools import get_filtered_queryset


class TypeSelectListAPIView(ListAPIView):
    """
    처음 검색 페이지 클릭시 호출되는 API입니다.
    Type(Handle) 선택시 사용하는 일러스트와 이름을 return합니다.
    """
    serializer_class = HandleSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Type.objects.all()


class HandBagCategoriesViewSetV1(viewsets.GenericViewSet):
    # queryset = TypeTag.objects.filter(is_handbag=True)
    permission_classes = [AllowAny, ]
    # serializer_class = ShapeSelectListSerializer

    def get_serializer_class(self):
        if self.action == 'shape':
            print('---')
            return ShapeSelectListSerializer
        elif self.action == 'charmdeco':
            return CharmDecoSelectListSerializer
        return super(HandBagCategoriesViewSetV1, self).get_serializer_class()

    @action(detail=False, methods=['GET'])
    def shape(self, request):
        print('---')
        queryset = Shape.objects.filter(type__is_handbag=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def charmdeco(self, request):
        queryset = CharmDeco.objects.filter(type__is_handbag=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BigShoulderCategoriesViewSet(viewsets.GenericViewSet):
    pass


# class ShapeSelectListAPIView(ListAPIView):
#     serializer_class = ShapeSelectListSerializer
#     permission_classes = [AllowAny, ]
#     queryset = Shape.objects.all()


class ColorSelectListAPIView(ListAPIView):
    serializer_class = ColorSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Color.objects.all()


# class CharmDecoSelectListAPIView(ListAPIView):
#     serializer_class = CharmDecoSelectListSerializer
#     permission_classes = [AllowAny, ]
#     queryset = CharmDeco.objects.all()


# class DecoSelectListAPIView(ListAPIView):
#     serializer_class = DecoSelectListSerializer
#     permission_classes = [AllowAny, ]
#     queryset = Deco.objects.all()


class PatternSelectListAPIView(ListAPIView):
    serializer_class = PatternSelectListSerializer
    permission_classes = [AllowAny, ]
    queryset = Pattern.objects.all()


class BagIllustCombineAPIView(GenericAPIView):
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