from knox.models import AuthToken
# from rest_auth.views import LoginView as RestAuthLoginView
# from rest_auth.registration.views import RegisterView as RestAuthRegisterView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from accounts.tools import loginlog_on_login
from accounts.models import MondeUser
from accounts.serializers import UserSerializer, LoginUserSerializer, CreateUserSerializer


class RegistrationAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer
    queryset = MondeUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'message': 'invalid uid'}, status=status.HTTP_204_NO_CONTENT)

        user = serializer.validated_data

        # log
        loginlog_on_login(request=self.request, user=user)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
