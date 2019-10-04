from django.db import models
from notices.tools import GiveRandomFileName

category_upload_dir = GiveRandomFileName(path='uploads/category_image')
bagillust_upload_dir = GiveRandomFileName(path='uploads/bag_illust')


class Shape(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Color(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Handle(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Charm(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Deco(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Pattern(models.Model):
    image = models.ImageField(upload_to=category_upload_dir)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class BagIllustration(models.Model):
    version = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=bagillust_upload_dir, null=True, help_text="bag illustration이 있으면 보여주기")
    shape = models.ForeignKey(Shape, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    handle = models.ForeignKey(Handle, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    charm = models.ForeignKey(Charm, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    deco = models.ForeignKey(Deco, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    pattern = models.ForeignKey(Pattern, related_name="bag_illustrations", null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
