from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import CrawlerProduct, CategoryCategories
from search.category_search.serializers import CategorySearchRequestSerializer, SampleListSerializer, \
    ProductResultSerializer, ProductVisitLogSerializer, ProductRecentViewSerializer
from search.category_search.tools import get_searched_data
from django.db.models import Case, When
from rest_framework.decorators import action

from tools.pagination import CategorySearchResultPagination
from user_activities.models import ProductViewLogs


class CursorListAPIView(GenericAPIView):
    serializer_class = SampleListSerializer
    queryset = CrawlerProduct.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = CategorySearchResultPagination

    def post(self, request, *args, **kwargs):

        pass


class CategorySearchViewSetV1(viewsets.GenericViewSet):
    queryset = CrawlerProduct.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = CategorySearchResultPagination
    serializer_class = CategorySearchRequestSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CategorySearchRequestSerializer
        elif self.action == 'visit':
            return ProductVisitLogSerializer
        return super(CategorySearchViewSetV1, self).get_serializer_class()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_request = serializer.save()  # 검색 요청 저장

        # category search
        categories_queryset = CategoryCategories.objects.all()
        categories = search_request.categories
        searched_product_ids = get_searched_data(categories_queryset, categories)

        # ordering
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(searched_product_ids)])
        searched_product = self.get_queryset().filter(pk__in=searched_product_ids).order_by(preserved)

        # PageNumberPagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(searched_product, request)
        serializer = ProductResultSerializer(paginated_queryset, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response

    @action(methods=['post'], detail=True)
    def visit(self, request, pk=None):

        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        info = self.get_product_info(pk)
        print(info)
        serializer.save(product_id=pk, **info)

        return Response(status=status.HTTP_201_CREATED)

    def get_product_info(self, pk):
        info = {}
        instance = CrawlerProduct.objects.filter(pk=pk).last()
        info['shopping_mall'] = instance.shopping_mall
        info['is_banned'] = instance.is_banned
        info['product_name'] = instance.product_name
        info['bag_url'] = instance.bag_url
        info['is_best'] = instance.is_best
        info['price'] = instance.price
        info['crawled_date'] = instance.crawled_date
        return info


class RecentViewLogViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    queryset = ProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductRecentViewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user).order_by('-created_at')
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

