import jsonfield
from django.db import models

from products.tools import make_integer_price


class ProductMaster(models.Model):
    """
    앞으로는 이 모델을 기준으로 상품 정보 보여줍니다.
    """
    db_id = models.PositiveIntegerField(unique=True, help_text="crawler id")
    name = models.CharField(max_length=100, null=True, blank=True)
    is_valid = models.BooleanField(help_text='크롤링 시 삭제되면 is_valid=False')
    is_best = models.BooleanField(help_text='best 상품')
    crawler_created_at = models.DateTimeField(blank=True, null=True)
    crawler_updated_at = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shopping_mall = models.IntegerField()
    product_image = models.ImageField(help_text='s3 image')
    product_url = models.URLField(help_text='상품 url')
    price = models.IntegerField()
    is_available = models.BooleanField(default=True, help_text="카테고리 쌓으면서 사용 가능한 상품인지 저장하는 필드")
    ready_for_service = models.BooleanField(default=False, help_text="crop, categories 까지 나오면 True")

    class Meta:
        managed = False
        db_table = 'bro_manager_productmaster'

    @property
    def product_image_url(self):
        url = 'https://monde-web-crawler.s3.ap-northeast-2.amazonaws.com/'
        name = self.product_image.name
        url = url + name
        return url


class ProductColors(models.Model):
    product = models.OneToOneField(ProductMaster, on_delete=models.CASCADE, related_name="colors")
    colors = jsonfield.JSONField()
    need_training_result = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'bro_manager_productcolors'


class ProductManager(models.Model):
    master = models.OneToOneField(ProductMaster, on_delete=models.CASCADE, related_name='manager')
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'bro_manager_productmanager'


class ImageInfo(models.Model):
    product = models.OneToOneField(ProductMaster, on_delete=models.CASCADE, related_name="image_info")
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bro_manager_productimageinfo'


class Categories(models.Model):
    master = models.OneToOneField(ProductMaster, on_delete=models.CASCADE, related_name="categories")
    shape_result = jsonfield.JSONField() # detail 포함, cover 포함.
    type_result = jsonfield.JSONField()
    charm_result = jsonfield.JSONField()
    deco_result = jsonfield.JSONField()
    pattern_result = jsonfield.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'bro_manager_categories'
