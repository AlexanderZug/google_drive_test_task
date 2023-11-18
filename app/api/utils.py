import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient import errors

from io import BytesIO


class GoogleDriveUploader:
    def __init__(self, data: str, name: str):
        """
        Initializes a GoogleDriveUploader object.

        Args:
            data (str): The data to be uploaded.
            name (str): The name of the file to be created.

        Returns:
            None
        """
        self.credentials_file = os.environ.get('TOKEN_FILE')
        self.scope = ["https://www.googleapis.com/auth/drive"]
        self.data = data
        self.name = name

    def authenticate(self) -> build:
        """
        Authenticates with Google Drive and returns a service object.

        Returns:
            build: An instance of the Google Drive service.

        Raises:
            errors.HttpError: If there is an issue with authentication.
        """
        try:
            credentials: Credentials = Credentials.from_service_account_file(
                self.credentials_file
            ).with_scopes(self.scope)
            service = build("drive", "v3", credentials=credentials)
            return service
        except errors.HttpError as e:
            raise errors.HttpError(e)

    def upload_to_drive(self) -> str:
        """
        Uploads data to Google Drive and returns the file ID.

        Returns:
            str: The ID of the uploaded file.
        """
        metadata: dict[str, str] = {
            "name": self.name,
            "mimeType": "application/vnd.google-apps.document",
        }
        bytes_buffer: BytesIO = BytesIO(self.data.encode())
        media: MediaIoBaseUpload = MediaIoBaseUpload(
            bytes_buffer, mimetype="text/plain"
        )
        file = (
            self.authenticate()
            .files()
            .create(body=metadata, media_body=media, fields="id")
            .execute()
        )
        self.make_public_permissions(file.get("id"), self.authenticate())
        return file.get("id")

    def response_to_user(self) -> dict[str, str]:
        """
        Generates a response dictionary for the user.

        Returns:
            dict[str, str]: A dictionary containing data, name, and a link to the uploaded file.
        """
        return {
            "data": self.data,
            "name": self.name,
            "link": f"https://docs.google.com/document/d/{self.upload_to_drive()}",
        }

    @staticmethod
    def make_public_permissions(file_id: str, service: build):
        """
        Sets public permissions for the specified file.

        Args:
            file_id (str): The ID of the file.
            service (build): The Google Drive service.

        Returns:
            None
        """
        public_permission: dict[str, str] = {
            "type": "anyone",
            "role": "reader",
        }
        service.permissions().create(
            fileId=file_id,
            body=public_permission,
            fields="id",
        ).execute()
