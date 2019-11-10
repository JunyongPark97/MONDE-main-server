from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from monde.models import ProductCategories
from search.category_search.serializers import CategorySearchRequestSerializer, ProductResultSerializer
from search.category_search.tools import search
from manage.pagination import ProductListPagination
from search.category_search.models import CategorySearchRequest
from collections import OrderedDict


class CategorySearchViewSetV1(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ProductCategories.objects.filter(product__is_valid=True, product__image_info__isnull=False).\
        select_related('product', 'product__image_info')
    permission_classes = [IsAuthenticated, ]
    # pagination_class = ProductListPagination
    serializer_class = CategorySearchRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_request = serializer.save()  # 검색 요청 저장 : CategorySearchRequest
        user_input = search_request.categories
        search_id = search_request.id

        # category search
        searched_product = search(user_input, self.get_queryset())  # list 형태, ordered
        serializer = ProductResultSerializer(searched_product, many=True, context={'request': request})
        combined_data = OrderedDict([('search_id', search_id), ('data', serializer.data)])

        return Response(combined_data, status=status.HTTP_201_CREATED)

