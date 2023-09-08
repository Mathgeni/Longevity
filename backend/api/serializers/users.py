import random
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import serializers

from api.tasks import send_otp

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password']

    def create(self, validated_data):
        otp = random.randint(100_000, 999_999)
        send_otp.delay(validated_data.get('email'), otp)
        user = UserModel.objects.create_user(**validated_data)
        user.otp = otp
        user.otp_expiry = timezone.now() + timedelta(hours=1)
        user.save()
        return user

    def validate(self, cleaned_data):
        if len(cleaned_data['password']) < 6:
            raise serializers.ValidationError('Password must be longer than 6 letters')
        return cleaned_data


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, cleaned_data):
        email = cleaned_data.get('email')
        otp = cleaned_data.get('otp')
        user = UserModel.objects.get(email=email)
        if not (email and otp):
            raise serializers.ValidationError('Email and otp required')
        if user.otp != otp:
            raise serializers.ValidationError('Incorrect OTP')
        if timezone.now() > user.otp_expiry:
            raise serializers.ValidationError('OTP expired')
        cleaned_data['user'] = user
        return cleaned_data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, max_length=128, write_only=True)

    def validate(self, cleaned_data):
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not (email and password):
            raise serializers.ValidationError('Email or password required')
        return cleaned_data


class UserDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, max_length=128, write_only=True)

    def validate(self, cleaned_data):
        if not authenticate(username=cleaned_data.get('email'), password=cleaned_data.get('password')):
            raise serializers.ValidationError('Email or password is incorrect')
        return cleaned_data
