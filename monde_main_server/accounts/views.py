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
