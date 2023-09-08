from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.contrib.auth import login, authenticate


from api.serializers.users import UserSerializer, UserLoginSerializer, VerifyOTPSerializer


class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
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
        response = {
            'email': user.email,
            'joined': user.joined,
        }
        return Response(response, status=HTTP_200_OK)
