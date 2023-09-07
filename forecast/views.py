from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UploadFileForm
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets


class FileListViewSet(viewsets.ModelViewSet):
    queryset = FileList.objects.all()
    serializer_class = FileListSerializer


class UploadView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(request.data)

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 업로드 파일 정보 DB 저장
            title = request.POST["title"]
            uploaded_file = request.FILES["file"]
            user_instance = User.objects.get(username="root")
            모델_인스턴스 = FileList(
                name=title, 파일=uploaded_file, user=user_instance, 진행현황="진행중"
            )
            모델_인스턴스.save()  # 데이터베이스에 저장

            return Response("파일 업로드 및 저장 성공")

        return Response("유효하지 않은 폼 데이터")
