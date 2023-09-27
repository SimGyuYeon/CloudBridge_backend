from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"filelist", FileListViewSet, basename="filelist")
router.register(r"model", ModelListViewSet, basename="model")
router.register(r"pred", PredListViewSet, basename="pred")
router.register(r"images", GraphListViewSet, basename="images")


urlpatterns = [
    path("", include(router.urls)),
    path("upload/", UploadView.as_view(), name="upload"),
    # path("create_model/", create_model, name="create_model"),
    path("create_model2/", CreateModelView.as_view(), name="create_model2"),
]
