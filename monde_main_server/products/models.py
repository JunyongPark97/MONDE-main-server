import jsonfield
from django.db import models

from products.tools import make_integer_price


class CrawlerBagimage(models.Model):
    bag_image = models.ImageField(upload_to='crawled-image', blank=True)
    image_url = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    product = models.ForeignKey('CrawlerProduct', related_name='bag_images',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_bagimage'


class CrawlerColortab(models.Model):
    is_mono = models.IntegerField()
    on_sale = models.IntegerField()
    colors = models.CharField(max_length=50)
    product = models.ForeignKey('CrawlerProduct', related_name='color_tabs',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_colortab'


class CrawlerColortag(models.Model):
    color = models.IntegerField()
    colortab = models.ForeignKey('CrawlerColortab', related_name='color_tags',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_colortag'


class CrawlerProduct(models.Model):
    shopping_mall = models.IntegerField()
    is_banned = models.IntegerField()
    product_name = models.CharField(max_length=100, blank=True, null=True)
    bag_url = models.CharField(max_length=200)
    is_best = models.IntegerField()
    price = models.CharField(max_length=50)
    crawled_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_product'
        # app_label = 'web_crawler' # router 에서 쓰기 위해

    @property
    def real_price(self):
        price = self.price
        return make_integer_price(price)


class CategoryCategories(models.Model):
    bag_image = models.OneToOneField('CrawlerBagimage', related_name='categories',on_delete=models.CASCADE)
    shape_result = jsonfield.JSONField()
    handle_result = jsonfield.JSONField()
    color_result = jsonfield.JSONField()
    charm_result = jsonfield.JSONField()
    deco_result = jsonfield.JSONField()
    pattern_result = jsonfield.JSONField()

    class Meta:
        managed = False
        db_table = 'category_categories'
