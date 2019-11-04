from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from monde.models import ProductCategories
from search.category_search.serializers import CategorySearchRequestSerializer, ProductResultSerializer
from search.category_search.tools import search
from manage.pagination import ProductListPagination


class CategorySearchViewSetV1(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ProductCategories.objects.filter(product__is_valid=True).select_related('product')
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProductListPagination
    serializer_class = CategorySearchRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_request = serializer.save()  # 검색 요청 저장 : CategorySearchRequest

        # category search
        user_input = search_request.categories
        searched_product = search(user_input, self.get_queryset())  # list 형태, ordered

        # PageNumberPagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(searched_product, request)
        serializer = ProductResultSerializer(paginated_queryset, many=True, context={'request': request})
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response

