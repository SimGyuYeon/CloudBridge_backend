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
import os 
import threading
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import *


# @api_view(["GET"])
# def create_model(request):
#     # TODO: 오래 걸리는 작업 수행
#     def do_task(file_id):
#         df = pd.read_csv("./script/temp_data2.csv", index_col="dt", parse_dates=["dt"])
#         # 모델생성 로직
#         sarima_learn(df, file_id)
#         print("모델 생성 완료")
#         # 이미지 생성 로직
#         print("이미지생성완료")
#         # 이미지 생성 완료 후 DB에 경로 저장
#         image1 = images_to_today("", "temp_data2.csv", "boxplot.png")
#         image2 = images_to_today("", "temp_data2.csv", "histogram.png")
#         image3 = images_to_today("", "temp_data2.csv", "scatter.png")
#         image4 = images_to_today("", "temp_data2.csv", "violinplot.png")
#         model_instance = GraphList(
#             image1=image1,
#             image2=image2,
#             image3=image3,
#             image4=image4,
#             model_id=1,
#             file_id=file_id,
#         )
#         model_instance.save()

#     # 스레드 생성 및 작업 시작
#     thread = threading.Thread(target=do_task, args=38)
#     thread.demon = True
#     thread.start()

#     return Response({"message": "작업이 시작되었습니다."})


def do_task(file_id):
    file_instance = FileList.objects.get(id=file_id)
    file_path = file_instance.파일
    print("file_path:", file_path)
    folder_path = os.path.dirname(str(file_path))
    df = pd.read_csv(file_path, index_col="dt", parse_dates=["dt"])
    # 모델생성 로직
    sarima_learn(df, file_id)
    print("모델 생성 완료")
    # 이미지 생성 로직
    print("이미지생성완료")
    # 이미지 생성 완료 후 DB에 경로 저장
    image0 = images_to_today("", folder_path, "lineplot.png")
    image1 = images_to_today("", folder_path, "boxplot.png")
    image2 = images_to_today("", folder_path, "histogram.png")
    image3 = images_to_today("", folder_path, "scatter.png")
    image4 = images_to_today("", folder_path, "violinplot.png")
    model_instance = GraphList(
        image0=image0,
        image1=image1,
        image2=image2,
        image3=image3,
        image4=image4,
        model_id=1,
        file_id=13,
    )
    model_instance.save()


class CreateModelView(APIView):
    def get(self, request, *args, **kwargs):
        file_id = request.query_params["file_id"]

        # 스레드 생성 및 작업 시작
        thread = threading.Thread(target=do_task, args=(file_id,))
        thread.demon = True
        thread.start()

        return Response(file_id + "번 파일 모델링 작업 시작")


class FileListViewSet(viewsets.ModelViewSet):
    queryset = FileList.objects.all()
    serializer_class = FileListSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("id", 1)  # URL 쿼리에서 사용자 ID를 가져옵니다.
        print(user_id)
        if user_id:
            queryset = FileList.objects.filter(user=user_id)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
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
            file_instance = FileList(
                name=title, 파일=uploaded_file, user=user_instance, 진행현황="진행중"
            )
            file_instance.save()  # 데이터베이스에 저장
            model_instance = ModelList(name="SARIMA", file_id=file_instance.id)
            model_instance.save()
            return Response("파일 업로드 및 저장 성공")

        return Response("유효하지 않은 폼 데이터")
