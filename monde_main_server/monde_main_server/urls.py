from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from accounts.social import FacebookLogin
from accounts.views import  index, login
from django.conf import settings
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^accounts/',include('allauth.urls')),

    # social login test 1
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/',include('rest_auth.registration.urls')),
    url(r'^api/v1/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    # knox token login
    url(r'^api/auth/', include('accounts.urls')),

    # social login test 2
    url(r'^$', index, name='index'),
    url(r'^fb-login/$', login, name='login'),

    #ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # richtextfield
    path('djrichtextfield/', include('djrichtextfield.urls')),

    # client test
    url(r'^',include('test.urls')),

    # notice
    url(r'^api/v1/notice/', include('notices.urls')),

    # category search
    url(r'^api/v1/category/', include('search.category_search.urls')),

    # TODO : url pattern 정리
    # recent view, favorite
    url(r'^api/v1/', include('user_activities.urls')),
    # visit
    url(r'^api/v1/', include('monde.urls')),]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
