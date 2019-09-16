"""monde_main_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

# from accounts.social import FacebookLogin
from accounts.social import FacebookLogin
from accounts.views import  index, login

#test
from test.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^accounts/',include('allauth.urls')),

    # url(r'^api/v1/rest-auth/login/$', LoginView.as_view(), name='rest_auth_login_v2'),

    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/',include('rest_auth.registration.urls')),
    url(r'^api/v1/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),

    #knox token login
    url(r'^api/auth/', include('accounts.urls')),

    #social login test
    url(r'^$', index, name='index'),
    url(r'^fb-login/$', login, name='login'),

    #client test
    url(r'^',include('test.urls')),

    #searchresults
    url(r'^api/v1/category/', include('search.category_search.urls')),
]
