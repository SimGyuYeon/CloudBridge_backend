from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"filelist", FileListViewSet, basename="filelist")


urlpatterns = [
    path("", include(router.urls)),
    path("api/upload/", UploadView.as_view(), name="upload"),
]
