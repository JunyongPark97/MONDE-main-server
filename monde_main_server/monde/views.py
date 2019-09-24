from django.db.models import F
from rest_framework import viewsets, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from logs.models import ProductViewCount
from products.models import CrawlerProduct
from tools.utils import get_product_info
from user_activities.models import UserProductViewLogs
from user_activities.serializers import ProductVisitLogSerializer


class ProductVisitAPIView(GenericAPIView):
    queryset = UserProductViewLogs.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductVisitLogSerializer

    def post(self, request, *args, **kwargs):
        p_id = self.kwargs['product_id']
        print(p_id)
        product = CrawlerProduct.objects.get(pk=p_id)

        # TODO : FIX ME! (is not drf style?)
        serializer = self.get_serializer(data=request.data, context={'request': request})

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
