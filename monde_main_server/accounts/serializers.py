from rest_framework import serializers

from accounts.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # key = serializers.CharField(read_only=True)

    def validate(self, attrs):
        from django.contrib.auth.hashers import check_password
        from rest_framework.authtoken.models import Token
        super(LoginSerializer, self).validate(attrs)
        email = attrs.get('email')
        password = attrs.get('password')

        if email is None:
            return

        user = User.objects.filter(email=email).first()
        attrs['user'] = user
        if user:
            valid_password = check_password(password, user.password)
            valid_temp_password = user.temporary_password and check_password(password, user.temporary_password)
            # TODO: 이메일-임시비밀번호 관련 기능들 (UI, 만료일 등)
            if valid_password or valid_temp_password:
                token, _ = Token.objects.get_or_create(user=user)
                attrs['key'] = token.key
                return attrs
            raise Exception("invalid Password")
        raise Exception("invalid Email (No User)")

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
