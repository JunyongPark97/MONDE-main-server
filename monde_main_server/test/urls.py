from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

# from accounts.social import FacebookLogin
from accounts.social import FacebookLogin
from accounts.views import LoginView

#test
from test.views import home, ListTestAPIView, ZIGZAGListTestAPIView

urlpatterns = [
    #test
    path('listexample', ListTestAPIView.as_view()),
    path('zigzaglist', ZIGZAGListTestAPIView.as_view())
]