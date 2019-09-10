import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_auth.views import LoginView as RestAuthLoginView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login as django_login

from accounts.serializers import LoginSerializer
from accounts.tools import loginlog_on_login


class LoginView(RestAuthLoginView):
    """
    이메일 로그인 API입니다. (TODO: 문서화)
    """
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)
        self.serializer = None
        self.user = None

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.serializer_class(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            self.login()
            print(self.serializer.validated_data)
        except Exception:
            return Response({"non_field_errors": ['Unable to log in with provided credentials.']},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer.data, status=status.HTTP_200_OK)
    #
    def login(self):
        user = self.serializer.validated_data['user']
        setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')
        django_login(self.request, user)
        loginlog_on_login(request=self.request, user=user)


#TODO : FIX ME!!!!
from monde_main_server.loader import load_credential
app_id = load_credential("FACEBOOK_APP_ID", ""),
app_secret = load_credential("FACEBOOK_APP_SECRET", ""),

def index(request):
    context = {
        "app_id": app_id,
    }
    print(request.META['HTTP_HOST'])
    return render(request, 'login.html', context)

def login(request):
    code = request.GET['code']
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('login')}"
    url_access_token = "https://graph.facebook.com/v2.8/oauth/access_token"

    params_access_token = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "client_secret": app_secret,
        "code": code,
    }
    response = requests.get(url_access_token, params=params_access_token)
    access_token = response.json()['access_token']

    url_user_info = 'https://graph.facebook.com/me'
    user_info_fields = [
        'id',  # 아이디
        'first_name',  # 이름
        'last_name',  # 성
        'picture',  # 프로필 사진
        'email',  # 이메일
    ]
    params_user_info = {
        "fields": ','.join(user_info_fields),
        "access_token": access_token
    }
    user_info = requests.get(url_user_info, params=params_user_info)

    return Response(user_info, status=status.HTTP_200_OK)
