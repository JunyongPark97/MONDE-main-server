# -*- encoding: utf-8 -*-
from django.db import models


class Version(models.Model):
    """
    버전 관리 모델입니다.
    각종 버전들(안드로이드, loading message등)이 바뀌었을 때 업데이트 할 수 있도록 합니다.
    """
    name = models.CharField(max_length=30, help_text="각종 버전의 이름입니다.", db_index=True, unique=True)
    version = models.IntegerField(default=1, help_text="각종 버전의 버전 정보입니다.")

    def __unicode__(self):
        return u'name: %s, version: %d' % (self.name, self.version)
