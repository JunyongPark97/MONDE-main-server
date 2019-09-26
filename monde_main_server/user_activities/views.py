from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from logs.models import ProductFavoriteCount
from monde.models import Product
from django.db.models import F

from search.category_search.serializers import ProductResultSerializer
from user_activities.models import UserProductViewLogs, UserProductFavoriteLogs
from user_activities.serializers import ProductRecentViewSerializer, \
    ProductFavoriteLogSerializer, UserProductFavoriteLogSerializer


class RecentViewLogViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    queryset = Product.objects.all().prefetch_related('user_view_logs')
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductResultSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_view_logs__user=request.user,
                                              user_view_logs__is_hidden=False).order_by('-user_view_logs__updated_at')

        # #queryset 이 UserProductViewLogs일 때 : 이때는 애초에 queryset 선언시 order_by()[:10]처럼 선언할 수 있는 장점.
        # #하지만 Product queryset 을 만들려면 작업이 한번 더 필요
        # queryset = self.get_queryset().filter(user=request.user, is_hidden=False).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        # get Product
        product = self.get_queryset().filter(pk=pk).last()
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        view_log = UserProductViewLogs.objects.filter(product=product, user=request.user).last()
        view_log.is_hidden = True
        view_log.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteLogViewSet(viewsets.ReadOnlyModelViewSet, mixins.ListModelMixin):
    queryset = Product.objects.all().prefetch_related('user_favorite_logs')
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductResultSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_favorite_logs__user=request.user,
                                              user_favorite_logs__is_hidden=False)\
                                              .order_by('-user_favorite_logs__updated_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductFavoriteAPIView(GenericAPIView, mixins.DestroyModelMixin,):
    queryset = UserProductFavoriteLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UserProductFavoriteLogSerializer

    def post(self, request, *args, **kwargs):
        product = self.get_product()
        serializer = self.get_serializer(data={'product': product.id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #  favorite count + 1
        # TODO : Change .filter() to .get()
        product_logs = ProductFavoriteCount.objects.filter(product=product).last()
        if product_logs:
            product_logs.favorite_count = F('favorite_count') + 1
            product_logs.save()
        else:
            ProductFavoriteCount.objects.create(product=product)

        # TODO : queryset 을 Product로 바꿔서?
        favorite_log = self.get_queryset().filter(user=request.user, product=product).last()

        if favorite_log:
            serializer.update(favorite_log, validated_data={'count': F('count') + 1,
                                                            'is_hidden': False})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product = self.get_product()

        favorite_log = self.get_queryset().filter(product=product, user=request.user).last()
        favorite_log.is_hidden = True
        favorite_log.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_product(self):
        pk = self.kwargs['product_id']
        product = Product.objects.get(pk=pk)
        return product
