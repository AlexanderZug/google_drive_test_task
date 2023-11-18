import json
from typing import Any
from pydantic import BaseModel, ValidationError, field_validator

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from api.utils import GoogleDriveUploader


class UploadData(BaseModel):
    """
    Represents data for uploading to Google Drive.

    Attributes:
        data: The data to be uploaded as a string.
        name: The name of the file to be created in Google Drive.

    Methods:
        check_string_type: Validates that the attribute values are of type string.

    Raises:
        ValueError: If any attribute value is not a string."""

    data: str
    name: str

    @field_validator("data", "name")
    def check_string_type(cls, value: Any) -> str | ValueError:
        if not isinstance(value, str):
            raise ValueError("Field must be a string.")
        return value


@method_decorator(csrf_exempt, name="dispatch")
class UploadToGoogleDriveView(View):
    """
    Handles a POST request by parsing JSON data from the request body,
    validating and creating an UploadData object,
    uploading the data to Google Drive, and returning a JSON response.

    Args:
        self: The instance of the class.
        request: The HTTP request object.
        args: Additional positional arguments.
        kwargs: Additional keyword arguments.

    Returns:
        A JSON response with the uploaded data and name.

    Raises:
        ValidationError: If the payload data is invalid.
        Exception: If an error occurs during the upload process.
    """

    http_method_names: list[str] = ["post"]

    def dispatch(self, request, *args, **kwargs) -> JsonResponse | HttpResponse:
        if request.method.lower() in self.http_method_names:
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse(
            {"error": "Method Not Allowed. Use POST method."}, status=405
        )

    def post(self, request, *args, **kwargs) -> JsonResponse:
        payload: dict[str, Any] = json.loads(request.body.decode("utf-8"))
        try:
            upload_data = UploadData(**payload)
        except ValidationError as error:
            return JsonResponse({"error": str(error)}, status=400)

        try:
            response = GoogleDriveUploader(
                upload_data.data, upload_data.name
            ).response_to_user()
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
