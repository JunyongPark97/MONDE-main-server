from rest_framework import serializers

from accounts.models import MondeUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MondeUser
        fields = ("id", "uid", "age")
        extra_kwargs = {"uid": {"write_only": True}}

    def create(self, validated_data):
        user = MondeUser.objects.create_user(validated_data["uid"], validated_data['age'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MondeUser
        fields = ("id", "uid")


class LoginUserSerializer(serializers.Serializer):
    uid = serializers.CharField()

    def validate(self, attrs):
        super(LoginUserSerializer, self).validate(attrs)
        uid = attrs.get('uid')
        if uid is None:
            return
        user = MondeUser.objects.filter(uid=uid).first()
        if user:
            return user
        raise Exception("invalid Uid (No User)")
