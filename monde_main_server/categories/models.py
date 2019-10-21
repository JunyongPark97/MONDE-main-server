from django.db import models
from notices.tools import GiveRandomFileName

category_upload_dir = GiveRandomFileName(path='uploads/category_image')
bagillust_upload_dir = GiveRandomFileName(path='uploads/bag_illust')


class TypeTag(models.Model):
    is_handbag = models.BooleanField(default=False)
    is_big_shoulder = models.BooleanField(default=False)
    is_mini = models.BooleanField(default=False)
    is_cross = models.BooleanField(default=False)
    is_clutch = models.BooleanField(default=False)
    is_backpack = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100, help_text="admin에서 참조하기 위한 필드", null=True)

    def __str__(self):
        return self.description


class Shape(models.Model):
    type = models.ForeignKey(TypeTag, null=True, on_delete=models.CASCADE, related_name='shape')
    image = models.ImageField(upload_to=category_upload_dir)
    description = models.CharField(max_length=100, help_text='설명', null=True)
    name = models.CharField(max_length=100, help_text='실제 가방 shape name', null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return self.name

    def __str__(self):
        if self.name:
            return self.name


class CharmDeco(models.Model):
    type = models.ForeignKey(TypeTag, null=True, on_delete=models.CASCADE, related_name='charm_deco')
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return self.name


class Color(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    type(handle) illustration 저장하는 모델
    """
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# class Deco(models.Model):
#     image = models.ImageField(upload_to=category_upload_dir)
#     name = models.CharField(max_length=100)
#     active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return self.name
#
#     def __str__(self):
#         return self.name


class Pattern(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class BagIllustration(models.Model):
    version = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=bagillust_upload_dir, null=True, help_text="bag illustration이 있으면 보여주기")
    shape = models.ForeignKey(Shape, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    handle = models.ForeignKey(Type, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    charm_deco = models.ForeignKey(CharmDeco, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    # deco = models.ForeignKey(Deco, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    pattern = models.ForeignKey(Pattern, related_name="bag_illustrations", null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
