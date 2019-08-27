import json

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from search.category_search.models import CategorySearchResultLog, CategorySearchRequest
from search.category_search.serializers import CategorySearchRequestSerializer


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def category_search_v1(categories):
    if not is_json(categories):
        return (None)


class SearchResultListAPIView(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            categories = serializer.validated_data
            category_search_request = CategorySearchRequest.objects.create(user=user,
                                                 category_search_version=version,
                                                 categories=categories)
            #TODO : func fix
            result_list = category_search_v1(categories)
            objs = CategorySearchResultLog(search_request=category_search_request
                                           (matched_categories=product.matched_categories,
                                           product_id=product.id,
                                           invalid=product.invalid) for product in result_list)
            #TODO : Make me async
            CategorySearchResultLog.objects.bulk_create(objs, user)
            return Response(result_list, status=status.HTTP_201_CREATED)
        CategorySearchRequest.objects.create(user=user,
                                             category_search_version=version,
                                             categories=request.data,
                                             code=0)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



