from django.db.models import F
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from logs.models import ProductViewCount
from products.models import CrawlerProduct
from search.category_search.serializers import ProductResultSerializer
from tools.pagination import CategorySearchResultPagination
from monde.tools import get_tab_queryset
from tools.utils import get_product_info
from user_activities.models import UserProductViewLogs
from user_activities.serializers import ProductVisitLogSerializer


class ProductVisitAPIView(GenericAPIView):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProductVisitLogSerializer

    def post(self, request, *args, **kwargs):
        p_id = self.kwargs['product_id']
        product = CrawlerProduct.objects.get(pk=p_id)

        # TODO : FIX ME! (is not drf style?)
        serializer = self.get_serializer(data=request.data, context={'request': request}) #datq = dict product_id input

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #  product view count + 1
        product_logs = ProductViewCount.objects.filter(product_id=p_id).last()
        if product_logs:
            product_logs.view_count = F('view_count') + 1
            product_logs.save()
        else:
            ProductViewCount.objects.create(product_id=p_id)

        info = get_product_info(product)

        if not info:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        view_log = self.get_queryset().filter(user=request.user, product_id=p_id).last()

        if view_log:
            # user visit count + 1
            serializer.update(view_log, validated_data={'count': F('count') + 1})
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)

        serializer.save(product_id=product.id, **info)

        return Response(status=status.HTTP_201_CREATED)


class TabListAPIViewV1(GenericAPIView):
    #TODO : db sync 맞추기

    queryset = CrawlerProduct.objects.all()
    serializer_class = ProductResultSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CategorySearchResultPagination

    def get(self, request, *args, **kwargs):
        tab_no = self.kwargs['tab_no']
        tab_queryset = get_tab_queryset(tab_no, self.get_queryset())
        filter_param = int(request.query_params.get('filter', 1)) # filter 있으면 filter, 없으면 1

        if filter_param == 1:
            # 인기순

            pass
        elif filter_param == 2:
            # 최신순?
            tab_queryset = tab_queryset.order_by('updated_at')
        elif filter_param == 3:
            # 저가순
            tab_queryset = sorted(tab_queryset, key=lambda CrawlerProduct: int(CrawlerProduct.real_price))
        elif filter_param == 4:
            # 고가순
            tab_queryset = sorted(tab_queryset, key=lambda CrawlerProduct: int(CrawlerProduct.real_price), reverse=True)

        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(tab_queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response

def sort_by_famous(queryset):
    ids = list(map(lambda x: x.id, queryset))

