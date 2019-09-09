from cursor_pagination import CursorPaginator
from django.core import serializers
from django.http import HttpResponse
from rest_framework import viewsets, mixins, status, generics
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from products.models import CrawlerProduct
from search.category_search.models import CategorySearchResultLog, CategorySearchRequest
from search.category_search.pagination import StandardResultsSetPagination
from search.category_search.serializers import CategorySearchRequestSerializer, SampleListSerializer, \
    CursorTestSerializer
from search.category_search.tools import category_search_v1
from tools.pagination import CursorPagination


class SearchResultListAPIView(GenericAPIView):
    serializer_class = CategorySearchRequestSerializer
    # permission_classes = [IsAuthenticated, ]
    queryset = CategorySearchResultLog.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Client에서 검색 시 data 에 category정보를 담아 보내주면
        data를 받아 CategorySearchRequest 모델을 생성하고 CategorySearchResultLog모델에 저장 후
        list형식으로 검색된 데이터를 return합니다.
        """
        print('ok')
        version = 1
        user = request.user
        print(user)
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
    # permission_classes = [IsAuthenticated, ]
    queryset = CrawlerProduct.objects.all()
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        paginator = Paginator(self.get_queryset(), 3)
        page = request.GET.get('page')
        post = paginator.get_page(page)
        print(post)
        print('--')
        # data = serializers.serialize('json', post)
        print(data)
        serializer = self.serializer_class(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CursorListAPIView(GenericAPIView):
    serializer_class = SampleListSerializer
    queryset = CrawlerProduct.objects.all()
    pagination_class = CursorPagination

    def post(self, request, *args, **kwargs):
        data = {}
        paginator = self.pagination_class()
        paginator_q = paginator.paginate_queryset(self.get_queryset(), self.request)
        paginator_r = paginator.get_paginated_response(self.get_queryset())
        serializer = self.serializer_class(paginator_q, many=True)
        data['bags'] = serializer.data
        data['prev'] = paginator_r['cursor-prev']
        data['next'] = paginator_r['cursor-next']

        return Response(data, status=status.HTTP_200_OK)


class MyListTestAPIView(generics.ListAPIView):
    queryset = CrawlerProduct.objects.all()
    serializer_class = SampleListSerializer
    pagination_class = CursorPagination
