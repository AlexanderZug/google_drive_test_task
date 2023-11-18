from django.urls import URLPattern, path
from .views import UploadToGoogleDriveView

urlpatterns: list[URLPattern] = [
    path(
        "upload-to-google-drive/",
        UploadToGoogleDriveView.as_view(),
        name="upload_to_google_drive",
    ),
]
