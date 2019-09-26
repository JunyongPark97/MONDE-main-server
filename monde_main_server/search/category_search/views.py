from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from monde.models import ProductCategories
from search.category_search.serializers import CategorySearchRequestSerializer, ProductResultSerializer
from search.category_search.tools import get_searched_data

from tools.pagination import ProductListPagination


class CategorySearchViewSetV1(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ProductCategories.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProductListPagination
    serializer_class = CategorySearchRequestSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return CategorySearchRequestSerializer
    #     elif self.action == 'visit':
    #         return UserProductVisitLogSerializer
    #     return super(CategorySearchViewSetV1, self).get_serializer_class()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        search_request = serializer.save()  # 검색 요청 저장 : CategorySearchRequest

        # category search
        categories = search_request.categories
        searched_product = get_searched_data(self.get_queryset(), categories) # list 형태, ordered

        # ordering
        # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(searched_product_ids)])
        # searched_product = self.get_queryset().filter(pk__in=searched_product_ids).order_by(preserved)

        # PageNumberPagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(searched_product, request)
        serializer = ProductResultSerializer(paginated_queryset, many=True, context={'request': request})
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response

