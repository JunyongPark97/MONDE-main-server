import jsonfield
from django.conf import settings
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from products.models import CrawlerProduct
from shopping_malls.models import ShoppingMall
# Create your models here.


class ActivityItem(models.Model): #TODO : sync to web crawler db
    product_id = models.PositiveIntegerField(help_text="crwaling db에 저장된 product의 id를 저장합니다.")
    product_url = models.URLField()
    bag_images = jsonfield.JSONField(help_text="image url from S3 를 key=order, value=url로 저장합니다.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductViewLogs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recent_view_logs', on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField(help_text='crawling server 의 product id')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, help_text='수정한 날짜', db_index=True, null=True)
    is_hidden = models.BooleanField(default=False)

    # db 공유가 되지 않아 최근 검색 목록 호출 query시 filter(id__in)으로 처리하다 보니 시간순으로 정렬이 어려워 info 저장함.
    shopping_mall = models.IntegerField()
    is_banned = models.BooleanField(default=False)
    product_name = models.CharField(null=True, max_length=100)
    bag_url = models.URLField()
    is_best = models.BooleanField(default=False)
    price = models.CharField(max_length=50)
    crawled_date = models.DateTimeField(null=True, blank=True)

    @property
    def product(self):
        product = CrawlerProduct.objects.filter(pk=self.product_id).last()
        if not product:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        return product
