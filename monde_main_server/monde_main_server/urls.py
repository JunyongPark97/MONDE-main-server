from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from accounts.social import FacebookLogin, GoogleLogin
from accounts.views import index, login, LoginView
from django.conf import settings
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # all auth
    url(r'^accounts/',include('allauth.urls')),

    # jwt login
    url(r'^api/v1/rest-auth/login/$', LoginView.as_view(), name='rest_auth_login'),
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/',include('rest_auth.registration.urls')),
    # social login : 소셜 로그인 성공시 클라이언트에서 access token (and code :fb)를 받아 server 에게 밑의 api로 post 보내면 jwt return
    url(r'^api/v1/rest-auth/google/$', GoogleLogin.as_view(), name='gg_login'),
    url(r'^api/v1/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    # knox token login # DEPRECATED
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
    url(r'^api/v1/', include('monde.urls')),

    # category search select list
    url(r'^api/v1/category/', include('categories.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
