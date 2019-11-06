from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from monde.models import ProductCategories
from search.category_search.serializers import CategorySearchRequestSerializer, ProductResultSerializer
from search.category_search.tools import search
from manage.pagination import ProductListPagination
from search.category_search.models import CategorySearchRequest


class CategorySearchViewSetV1(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ProductCategories.objects.filter(product__is_valid=True, product__image_info__isnull=False).\
        select_related('product', 'product__image_info')
    permission_classes = [IsAuthenticated, ]
    pagination_class = ProductListPagination
    serializer_class = CategorySearchRequestSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO : FIX ME!
        # 매번 페이지네이션 할 때 마다 검색 요청이 중복 저장되는 것을 막기 위해 page 1인 경우에만 저장, 나머지 경우는 존재하는 검색기록 쿼리
        page = int(request.query_params.get('page', 1))
        if page == 1:
            search_request = serializer.save()  # 검색 요청 저장 : CategorySearchRequest
            user_input = search_request.categories
            search_id = search_request.id
        else:
            search_request = request.data
            user_input = search_request['categories']
            pre_request = CategorySearchRequest.objects.filter(user=user, categories=user_input)
            if not pre_request.exists():
                search_id = None
            else:
                search_id = pre_request.last().id

        # category search
        searched_product = search(user_input, self.get_queryset())  # list 형태, ordered

        # PageNumberPagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(searched_product, request)
        serializer = ProductResultSerializer(paginated_queryset, many=True, context={'request': request})
        combined_data = {'search_id': search_id, 'data': serializer.data}

        paginated_response = paginator.get_paginated_response(combined_data)

        return paginated_response

