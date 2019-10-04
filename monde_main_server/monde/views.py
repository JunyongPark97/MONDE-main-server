from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from logs.models import ProductViewCount
from monde.models import Product, ProductCategories
from search.category_search.serializers import ProductResultSerializer
from tools.pagination import ProductListPagination
from monde.tools import get_tab_ids
from user_activities.models import UserProductViewLogs
from user_activities.serializers import UserProductVisitLogSerializer


class ProductVisitAPIView(CreateAPIView):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [TokenAuthentication, ]
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
    queryset = Product.objects.all().select_related('product_categories', 'favorite_count')
    serializer_class = ProductResultSerializer
    permission_classes = [AllowAny, ]
    pagination_class = ProductListPagination

    def get(self, request, *args, **kwargs):
        tab_no = self.kwargs['tab_no']
        categories_queryset = ProductCategories.objects.all()
        tab_product_ids = get_tab_ids(tab_no, categories_queryset)
        tab_product = self.get_queryset().filter(id__in=tab_product_ids)
        filter_param = int(request.query_params.get('filter', 1))  # filter 있으면 filter, 없으면 1
        if filter_param == 1:
            # 인기순
            tab_queryset = tab_product.order_by('favorite_count__favorite_count')
        elif filter_param == 2:
            # 최신순?
            tab_queryset = tab_product.order_by('updated_at')
        elif filter_param == 3:
            # 저가순
            tab_queryset = tab_product.order_by('price')
        elif filter_param == 4:
            # 고가순
            tab_queryset = tab_product.order_by('-price')
        else:
            tab_queryset = tab_product

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(tab_queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response
