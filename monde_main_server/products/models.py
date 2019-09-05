# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CrawlerBagimage(models.Model):
    bag_image = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    product = models.ForeignKey('CrawlerProduct', related_name='bag_images',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_bagimage'
        app_label = 'web_crawler'


class CrawlerColortab(models.Model):
    is_mono = models.IntegerField()
    on_sale = models.IntegerField()
    colors = models.CharField(max_length=50)
    product = models.ForeignKey('CrawlerProduct', related_name='color_tabs',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_colortab'
        app_label = 'web_crawler'


class CrawlerColortag(models.Model):
    color = models.IntegerField()
    colortab = models.ForeignKey('CrawlerColortab', related_name='color_tags',on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'crawler_colortag'
        app_label = 'web_crawler'


class CrawlerProduct(models.Model):
    shopping_mall = models.IntegerField()
    is_banned = models.IntegerField()
    image_url = models.CharField(max_length=200)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    bag_url = models.CharField(max_length=200)
    is_best = models.IntegerField()
    price = models.CharField(max_length=50)
    crawled_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_product'
        app_label = 'web_crawler'

