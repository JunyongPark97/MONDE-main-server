from django.db import models
import jsonfield

# Create your models here.


class Product(models.Model):
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    shopping_mall = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    product_url = models.URLField()
    price = models.IntegerField(max_length=50 ,help_text='db로 옮기면서 integer로 바꿈')
    is_on_sale = models.BooleanField(help_text="color tab에 있던걸 옮겨옴")
    crawler_created_at = models.DateTimeField(blank=True, null=True)
    crawler_updated_at = models.DateTimeField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    image = models.ImageField()
    origin_url = models.URLField()
    order = models.IntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE, help_text='onetoone으로 바꿈')


class ProductCategories(models.Model):
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    shape_result = jsonfield.JSONField()
    handle_result = jsonfield.JSONField()
    color_result = jsonfield.JSONField()
    charm_result = jsonfield.JSONField()
    deco_result = jsonfield.JSONField()
    pattern_result = jsonfield.JSONField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE, help_text='bag image를 통해 물려있던걸 바로 product와 연결함')


class ColorTab(models.Model):
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    color_tab_name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, related_name='color_tabs', on_delete=models.CASCADE)


class Colors(models.Model):
    db_id = models.PositiveIntegerField(unique=True, help_text="for sync")
    color = models.IntegerField()
    color_tab = models.ForeignKey(ColorTab, related_name='colors', on_delete=models.CASCADE)
