from rest_framework import viewsets, mixins, status, generics
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from products.models import CrawlerProduct, CategoryCategories
from search.category_search.models import CategorySearchResultLog, CategorySearchRequest
from search.category_search.pagination import StandardResultsSetPagination
from search.category_search.serializers import CategorySearchRequestSerializer, SampleListSerializer
from search.category_search.tools import get_searched_data
from tools.pagination import CursorPagination


class SearchResultListAPIView(GenericAPIView):
    serializer_class = CategorySearchRequestSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = CategorySearchResultLog.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Client에서 검색 시 data 에 category정보를 담아 보내주면
        data를 받아 CategorySearchRequest 모델을 생성하고 CategorySearchResultLog모델에 저장 후
        list형식으로 검색된 데이터를 return합니다.
        """
        version = 1
        user = request.user
        serializer = self.get_serializer(data=request.data) #context 넘겨줌 : request 등
        if serializer.is_valid():
            category_search_request = serializer.save()
            categories = category_search_request.categories
            # category_search_request = CategorySearchRequest.objects.create(user=user,
            #                                      category_search_version=version,
            #                                      categories=categories)
            #TODO : func fix
            result_list = category_search_v1(categories) #이 안에서 pagination 구현. 자동으로 django가 api 생성
            objs = [CategorySearchResultLog(search_request=category_search_request,
                                            user=user,
                                            matched_categories=product.matched_categories,
                                            product_id=product.id,
                                            invalid=product.invalid) for product in result_list]
            #100개는 너무 많다. 10개만 저장?
            #TODO : Make me async
            CategorySearchResultLog.objects.bulk_create(objs)
            return Response(result_list, status=status.HTTP_201_CREATED)
        CategorySearchRequest.objects.create(user=user,
                                             category_search_version=version,
                                             categories=request.data,
                                             code=0)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SampleListAPIView(GenericAPIView):
    serializer_class = SampleListSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = CrawlerProduct.objects.all()
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        data = request.data
        temp_product = category_search_v1(data)

        serializer = self.serializer_class(temp_product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CursorListAPIView(GenericAPIView):
    serializer_class = SampleListSerializer
    queryset = CategoryCategories.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = CursorPagination

    def post(self, request, *args, **kwargs):
        user_input = request.data
        print(user_input)
        #TODO : MAKE queryset ,not list to pagination ordering
        searched_list = get_searched_data(self.get_queryset(), user_input)
        paginator = self.pagination_class()
        paginator_q = paginator.paginate_queryset(searched_list, self.request)
        paginator_r = paginator.get_paginated_response(searched_list)
        serializer = self.serializer_class(paginator_q, many=True)
        searched_list['bags'] = serializer.data
        searched_list['prev'] = paginator_r['cursor-prev']
        searched_list['next'] = paginator_r['cursor-next']

        return Response(searched_list, status=status.HTTP_200_OK)


class MyListTestAPIView(generics.ListAPIView):
    queryset = CrawlerProduct.objects.all()
    serializer_class = SampleListSerializer
    pagination_class = CursorPagination
