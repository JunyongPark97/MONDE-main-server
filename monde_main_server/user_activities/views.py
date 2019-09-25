from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from logs.models import ProductFavoriteCount
from products.models import CrawlerProduct
from django.db.models import F
from rest_framework.decorators import action

from tools.utils import get_product_info
from user_activities.models import UserProductViewLogs, UserProductFavoriteLogs
from user_activities.serializers import ProductRecentViewSerializer, \
    ProductFavoriteSerializer, ProductFavoriteLogSerializer


class RecentViewLogViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductRecentViewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, is_hidden=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        view_log = self.get_queryset().filter(product_id=pk, user=request.user).last()
        view_log.is_hidden = True
        view_log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteLogViewSet(viewsets.ReadOnlyModelViewSet, mixins.ListModelMixin):
    queryset = UserProductFavoriteLogs.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductFavoriteLogSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user, is_hidden=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductFavoriteAPIView(GenericAPIView, mixins.DestroyModelMixin, mixins.CreateModelMixin,):
    queryset = UserProductFavoriteLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductFavoriteSerializer

    def create(self, request, *args, **kwargs):
        pk = self.kwargs['product_id']
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
            serializer.update(favorite_log, validated_data={'count': F('count') + 1})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save(product_id=product.id, **info)

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['product_id']
        favorite_log = self.get_queryset().filter(product_id=pk, user=request.user).last()
        favorite_log.is_hidden = True
        favorite_log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
