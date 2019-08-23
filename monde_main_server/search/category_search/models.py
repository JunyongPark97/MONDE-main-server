from django.conf import settings
from django.db import models
from categories.models import Category


class CategorySearchRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_search_requests', on_delete=models.CASCADE)
    category_search_version = models.IntegerField()
    categories = models.OneToOneField(Category, related_name="category_search_request", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)