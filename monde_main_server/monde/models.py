from django.db import models
import jsonfield
from products.models import CrawlerProduct
from products.helper import SITE_CHOICES

class Product(models.Model):
    """
    mondebro , crawler를 참고하여 sync 맞춘 후 서비스에서 이 모델을 기준으로 사용합니다.
    """
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    shopping_mall = models.IntegerField(choices=SITE_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True)
    product_url = models.URLField()
    product_image_url = models.URLField(help_text="상품 이미지 url", null=True)
    price = models.IntegerField(help_text='db로 옮기면서 integer로 바꿈')
    # is_on_sale = models.BooleanField(help_text="color tab에 있던걸 옮겨옴")
    is_banned = models.BooleanField(default=False)
    is_best = models.BooleanField(default=False)
    is_valid = models.BooleanField()
    crawler_created_at = models.DateTimeField(blank=True, null=True, help_text="crawler 와 sync 맞춰야함")
    crawler_updated_at = models.DateTimeField(blank=True, null=True, help_text="crawler 와 sync 맞춰야함")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImageInfo(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="image_info")
    width = models.IntegerField()
    height = models.IntegerField()


class ProductCategories(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="categories")
    shape_result = jsonfield.JSONField()  # detail 포함, cover 포함.
    type_result = jsonfield.JSONField()
    charm_result = jsonfield.JSONField()
    deco_result = jsonfield.JSONField()
    pattern_result = jsonfield.JSONField()
    colors = jsonfield.JSONField()
