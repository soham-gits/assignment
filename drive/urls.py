from django.urls import path
from .views import download_drive_file, list_drive_files, upload_file_to_drive

urlpatterns = [
    path("upload/", upload_file_to_drive, name="upload_drive_file"),
    path("files/", list_drive_files, name="list_drive_files"),
    path("download/<str:file_id>/", download_drive_file, name="download_drive_file"),
]
