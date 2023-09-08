from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from api.serializers.users import (UserCreateSerializer, UserDeleteSerializer,
                                   UserLoginSerializer, VerifyOTPSerializer)


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            clean_data = serializer.validated_data
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            user.verified = True
            user.save()
            return Response('User verified', status=HTTP_200_OK)


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            user = authenticate(username=validated_data.get('email'), password=validated_data.get('password'))
            if user and user.verified:
                login(request, user)
                return Response(serializer.data, status=HTTP_200_OK)
        return Response('User not found or not verified', status=HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        return Response({'email': user.email}, status=HTTP_200_OK)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request):
        user = request.user
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            user.delete()
            return Response('User deleted', status=HTTP_204_NO_CONTENT)
        return Response('Is not valid', status=HTTP_400_BAD_REQUEST)
