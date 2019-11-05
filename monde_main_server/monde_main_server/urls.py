from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

# from accounts.social import FacebookLogin, GoogleLogin
# from accounts.views import index, login, LoginView
from django.conf import settings
from django.conf.urls.static import static

from manage.sites import staff_panel

urlpatterns = [

    # Admin
    url(r'^staff/', staff_panel.urls),
    url(r'^admin/', admin.site.urls),

    # login
    url(r'^api/auth/', include('accounts.urls')),

    # ckeditor
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
    url(r'^api/v1/category/', include('categories.urls')),

    # user feedback (search result)
    url(r'^api/v1/', include('logs.urls')),


    # all auth [DEPRECATED]
    url(r'^accounts/', include('allauth.urls')),

    # jwt url [DEPRECATED]
    url(r'^api/token/', obtain_jwt_token),
    url(r'^api/token/verify/', verify_jwt_token),
    url(r'^api/refresh/', refresh_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
