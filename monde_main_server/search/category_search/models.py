import jsonfield
from django.conf import settings
from django.db import models
from categories.models import Category


class CategorySearchRequest(models.Model):
    """
    User가 검색을 시도할때 사용한 데이터를 저장합니다.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category_search_requests', on_delete=models.CASCADE)
    category_search_version = models.IntegerField()
    # categories = models.OneToOneField(Category, related_name="category_search_request", on_delete=models.CASCADE)
    categories = jsonfield.JSONField(default=dict, help_text="유저가 검색시 사용했던 카테고리 정보를 json형태로 저장합니다.")
    code = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class CategorySearchResultLog(models.Model):
    """
    User가 검색후 logic에 의해 검색된 상품의 카테고리정보와 상품정보를 저장해서 client에게 보여주는 모델입니다. *매우중요
    question : 매번 검색할때마다 데이터를 저장하는게 좋을까?
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="category_result_logs", on_delete=models.CASCADE)
    search_request = models.ForeignKey(CategorySearchRequest, related_name="category_result_logs", on_delete=models.CASCADE)
    matched_categories = jsonfield.JSONField(default=dict, help_text="상품이 검색될 때 사용된(matched) 카테고리를 저장합니다.") #matching된 모든 카테고리 정보를 저장합니다.??
    product_id = models.PositiveIntegerField(blank=True, null=True, help_text="검색된 가방의 id")
    invalid = models.BooleanField(default=False, help_text="이 가방이 더이상 팔리지 않거나 재고가 없는 경우 invalid=True")


class CategorySearchMatchData(models.Model):
    """
    매칭된 각각의 카테고리 정확도를 보기 위해 만든 모델입니다. 빠른 query를 위해 저장합니다.
    """
    result_log = models.ForeignKey(CategorySearchResultLog, related_name="datas", on_delete=models.CASCADE)
    match_category = jsonfield.JSONField(default=dict, help_text="검색된 상품의 각 카테고리들의 labeling accuracy를 저장합니다.")
    similarity = models.FloatField() #TODO : How to measure similarity?


class CategorySearchUserReview(models.Model):
    MATCH_TYPES = (
        (1, 'same'),
        (2, 'similar'),
        (3, 'different'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews',
                             on_delete=models.CASCADE, null=True)
    search_log = models.ForeignKey(CategorySearchResultLog, related_name="user_reviews", on_delete=models.CASCADE)
    match_type = models.IntegerField(choices=MATCH_TYPES)
    text = models.CharField(max_length=70, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class CategorySearchViewTimeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='view_time_logs', null=True, on_delete=models.SET_NULL)
    searched_question_log = models.ForeignKey(CategorySearchResultLog, related_name='view_time_logs', on_delete=models.CASCADE)
    elapsed = models.IntegerField(help_text='검색결과를 보면서 경과한 시간 (milliseconds)')
    state = models.CharField(max_length=30, help_text='검색결과를 볼 때 화면의 상태')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)

    def __unicode__(self):
        return u'%s - [%sms]' % (self.state, self.elapsed)

