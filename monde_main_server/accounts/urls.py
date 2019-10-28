from django.urls import path

import accounts.views as account_views

urlpatterns = [
    path('register', account_views.RegistrationAPI.as_view()),
    path('login', account_views.LoginAPI.as_view()),
    path('user', account_views.UserAPI.as_view()),
    ]