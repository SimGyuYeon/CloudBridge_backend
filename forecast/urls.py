from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"filelist", FileListViewSet, basename="filelist")
router.register(r"model", ModelListViewSet, basename="modellist")
router.register(r"pred", PredListViewSet, basename="predlist")
router.register(r"images", GraphListViewSet, basename="imageslist")


urlpatterns = [
    path("", include(router.urls)),
    path("upload/", UploadView.as_view(), name="upload"),
]
