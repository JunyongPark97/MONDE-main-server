from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from logs.models import ProductViewCount, ProductFavoriteCount
from products.models import CrawlerProduct, CategoryCategories
from search.category_search.serializers import CategorySearchRequestSerializer, SampleListSerializer, \
    ProductResultSerializer, ProductVisitLogSerializer, ProductRecentViewSerializer, ProductFavoriteLogSerializer, \
    ProductFavoriteSerializer
from search.category_search.tools import get_searched_data
from django.db.models import Case, When, F
from rest_framework.decorators import action

from tools.pagination import CategorySearchResultPagination
from user_activities.models import UserProductViewLogs, UserProductFavoriteLogs


def get_product_info(product):
    info = {}
    info['shopping_mall'] = product.shopping_mall
    info['is_banned'] = product.is_banned
    info['product_name'] = product.product_name
    info['bag_url'] = product.bag_url
    info['is_best'] = product.is_best
    info['price'] = product.price
    info['crawled_date'] = product.crawled_date
    return info


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
        """
        DEPRECATED : RecentViewLogViewSet 에서 visit 으로 대체
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = CrawlerProduct.objects.get(pk=pk)
        info = get_product_info(product)
        serializer.save(product_id=pk, **info)

        return Response(status=status.HTTP_201_CREATED)



class RecentViewLogViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductRecentViewSerializer

    def get_serializer_class(self):
        if self.action == 'visit':
            return ProductVisitLogSerializer
        elif self.action == 'list':
            return ProductRecentViewSerializer
        return super(RecentViewLogViewSet, self).get_serializer_class()

    #TODO : fix me!
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        product = CrawlerProduct.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #  product view count + 1
        product_logs = ProductViewCount.objects.filter(product_id=pk).last()
        if product_logs:
            product_logs.view_count = F('view_count')+1
            product_logs.save()
        else:
            ProductViewCount.objects.create(product_id=pk)

        view_log = self.get_queryset().filter(user=request.user, product_id=pk).last()
        info = get_product_info(product)

        if not info:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if view_log:
            serializer.update(view_log, validated_data={'count': F('count')+1})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save(product_id=product.id, **info)

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, is_hidden=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def delete(self, request, pk=None):
        view_log = self.get_queryset().filter(product_id=pk, user=request.user).last()
        view_log.is_hidden = True
        view_log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductFavoriteViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin):
    queryset = UserProductFavoriteLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductFavoriteSerializer

    def get_serializer_class(self):
        if self.action == 'heart':
            return ProductFavoriteSerializer
        elif self.action == 'list':
            return ProductFavoriteLogSerializer
        return super(ProductFavoriteViewSet, self).get_serializer_class()

    @action(methods=['post'], detail=True)
    def heart(self, request, pk=None):
        product = CrawlerProduct.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #  favorite count + 1
        product_logs = ProductFavoriteCount.objects.filter(product_id=pk).last()
        if product_logs:
            product_logs.favorite_count = F('favorite_count') + 1
            product_logs.save()
        else:
            ProductFavoriteCount.objects.create(product_id=pk)

        favorite_log = self.get_queryset().filter(user=request.user, product_id=pk).last()
        info = get_product_info(product)

        if not info:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if favorite_log:
            serializer.update(favorite_log, validated_data={'count': F('count')+1})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save(product_id=product.id, **info)

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, is_hidden=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def delete(self, request, pk=None):
        favorite_log = self.get_queryset().filter(product_id=pk, user=request.user).last()
        favorite_log.is_hidden = True
        favorite_log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
