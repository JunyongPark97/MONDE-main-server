import jsonfield
from django.db import models

from products.tools import make_integer_price


class CrawlerProduct(models.Model):
    """
    crawler 저장하는 모델로써,
    valid 값을 참고하기 위해 사용합니다.
    """
    shopping_mall = models.IntegerField()
    is_banned = models.IntegerField()
    product_name = models.CharField(max_length=100, blank=True, null=True)
    bag_url = models.CharField(max_length=200)
    is_best = models.BooleanField()
    price = models.CharField(max_length=50)
    crawled_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_valid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'crawler_product'

    @property
    def real_price(self):
        price = self.price
        return make_integer_price(price)
