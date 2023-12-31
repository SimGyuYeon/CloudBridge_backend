from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import *


class RegisterView(generics.CreateAPIView):  # CreateAPIView(generics) 사용 구현
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴
        queryset = User.objects.filter(auth_token=token.key)
        user = queryset.get()
        user_id = user.id  # 유저의 ID를 가져옵니다.
        print({"token": token.key, "user_id": user_id})
        return Response(
            {"token": token.key, "user_id": user_id}, status=status.HTTP_200_OK
        )
