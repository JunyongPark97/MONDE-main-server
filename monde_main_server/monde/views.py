from django.db.models import F, Sum, Q, Value as V
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from logs.models import ProductViewCount
from monde.models import Product, ProductCategories, MainPageImage
from monde.serializers import MainPageImageSerializer
from monde.syncdb import product_sync
from search.category_search.serializers import ProductResultSerializer
from manage.pagination import ProductListPagination
from monde.tools import get_tab_ids
from user_activities.models import UserProductViewLogs
from user_activities.serializers import UserProductVisitLogSerializer
import datetime
from django.db.models.functions import Coalesce


class SyncDBAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        product_sync()
        return Response(status=status.HTTP_201_CREATED)


class MondeMainListAPIView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = MainPageImage.objects.all()
    serializer_class = MainPageImageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('order')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductVisitAPIView(CreateAPIView):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProductVisitLogSerializer

    def post(self, request, *args, **kwargs):
        product = self.get_product()
        serializer = self.get_serializer(data={'product': product.id})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #  product view count + 1
        product_logs = ProductViewCount.objects.filter(product=product).last()
        if product_logs:
            product_logs.view_count = F('view_count') + 1
            product_logs.save()
        else:
            ProductViewCount.objects.create(product=product)

        # update user view log
        user_view_log = self.get_queryset().filter(user=request.user, product=product).last()

        if user_view_log:
            # user visit count + 1
            serializer.update(user_view_log, validated_data={'count': F('count') + 1,
                                                             'is_hidden': False})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_product(self):
        pk = self.kwargs['product_id']
        product = Product.objects.get(pk=pk)
        return product


class TabListAPIViewV1(GenericAPIView):
    queryset = Product.objects.filter(is_valid=True, image_info__isnull=False).\
        select_related('favorite_count', 'view_count', 'categories', 'image_info')
    serializer_class = ProductResultSerializer
    permission_classes = [AllowAny, ]
    pagination_class = ProductListPagination

    def get(self, request, *args, **kwargs):
        tab_no = self.kwargs['tab_no']
        categories_queryset = ProductCategories.objects.all()

        # tab
        tab_product_ids = get_tab_ids(tab_no, categories_queryset)
        tab_product = self.get_queryset().filter(id__in=tab_product_ids)

        # filter
        filter_param = int(request.query_params.get('filter', 1))  # filter 있으면 filter, 없으면 1
        if filter_param == 1:
            # 인기순 # for test
            tab_queryset = self._best_product_by_day(tab_product)
        elif filter_param == 4:
            # 최신순 DEPRECATED
            tab_queryset = tab_product.order_by('crawler_updated_at')
        elif filter_param == 2:
            # 저가순
            print('저가순')
            tab_queryset = tab_product.order_by('price')
            # print(tab_product)
        elif filter_param == 3:
            # 고가순
            tab_queryset = tab_product.order_by('-price')
        else:
            tab_queryset = tab_product

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(tab_queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response

    def _best_product_by_day(self, queryset):
        today = datetime.datetime.now().day
        if today % 6 == 0:
            # luzzibag
            qs = self._filtered_qs(queryset, 1)
            return qs
        elif today % 6 == 1:
            # mclanee
            qs = self._filtered_qs(queryset, 10, 5)
            return qs
        elif today % 6 == 2:
            # jade
            qs = self._filtered_qs(queryset, 3)
            return qs
        elif today % 6 == 3:
            # pinkbag
            qs = self._filtered_qs(queryset, 12, 6)
            return qs
        else:
            qs = self._order_famous(queryset)
            return qs

    def _filtered_qs(self, queryset, num, num2=None):
        if num2:
            best_qs = queryset.filter(Q(shopping_mall=num) | Q(shopping_mall=num2)).filter(is_best=True)
        else:
            best_qs = queryset.filter(shopping_mall=num, is_best=True)
        best_ids = self._ids(best_qs)
        qs = queryset.exclude(id__in=best_ids).annotate(favorite=Coalesce('favorite_count__favorite_count', V(0)))\
            .annotate(view=Coalesce('view_count__view_count', V(0)))\
            .annotate(total=Sum(F('favorite') * 1.5 + F('view') * 1))\
            .order_by('total')
        if best_qs.exists():
            filtered_qs = best_qs.union(qs)
        else:
            filtered_qs = qs
        return filtered_qs

    def _order_famous(self, queryset):
        qs = queryset.annotate(favorite=Coalesce('favorite_count__favorite_count', V(0)))\
                     .annotate(view=Coalesce('view_count__view_count', V(0)))\
                     .annotate(total=Sum(F('favorite') * 1.5 + F('view') * 1))\
            .order_by('total')
        return qs

    def _ids(self, qs):
        ids = qs.values_list('id', flat=True)
        ids = list(ids)
        return ids

