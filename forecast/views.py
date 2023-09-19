from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UploadFileForm
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from script.model_learn import sarima_learn
import pandas as pd

import threading
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time


@api_view(["GET"])
def create_model(request):
    # 오래 걸리는 작업 수행
    def do_task():
        # time.sleep(5)
        df = pd.read_csv("./script/temp_data.csv", index_col="dt", parse_dates=["dt"])
        sarima_learn(df)
        print("작업 완료")

    # 스레드 생성 및 작업 시작
    thread = threading.Thread(target=do_task)
    thread.demon = True
    thread.start()

    return Response({"message": "작업이 시작되었습니다."})


class FileListViewSet(viewsets.ModelViewSet):
    queryset = FileList.objects.all()
    serializer_class = FileListSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("id", 1)  # URL 쿼리에서 사용자 ID를 가져옵니다.
        if user_id:
            queryset = FileList.objects.filter(user=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 기본적인 CRUD 엔드포인트가 있고, 여기에 추가할 커스텀 엔드포인트를 정의합니다.
    @action(detail=True, methods=["GET"], url_path="detail")
    def custom_detail(self, request, pk=None):
        # 예측 차트 데이터
        file_list_instance = self.get_object()
        print(file_list_instance.id)
        queryset = PredList.objects.filter(file_id=file_list_instance.id).order_by(
            "pred_dt"
        )
        serializer = PredListSerializer(queryset, many=True)

        # IMAGE 데이터
        queryset2 = GraphList.objects.filter(file_id=file_list_instance.id)
        serializer2 = GraphListSerializer(queryset2, many=True)

        responseJson = {
            "pred_list": serializer.data,
            "graph_list": serializer2.data,
        }

        return Response(responseJson)


class ModelListViewSet(viewsets.ModelViewSet):
    queryset = ModelList.objects.all()
    serializer_class = ModelListSerializer


class PredListViewSet(viewsets.ModelViewSet):
    queryset = PredList.objects.all()
    serializer_class = PredListSerializer


class GraphListViewSet(viewsets.ModelViewSet):
    queryset = GraphList.objects.all()
    serializer_class = GraphListSerializer


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
            moedl_instance = FileList(
                name=title, 파일=uploaded_file, user=user_instance, 진행현황="진행중"
            )
            moedl_instance.save()  # 데이터베이스에 저장

            return Response("파일 업로드 및 저장 성공")

        return Response("유효하지 않은 폼 데이터")
