# google_drive_test_task

## Project Description

This project is an API service for uploading files to Google Drive. The service provides a single endpoint:

- **Endpoint:** http://18.193.86.9/api/upload-to-google-drive/
- **Method:** POST

The endpoint accepts two parameters:

1. `name` (string) - the name of the file.
2. `data` (string) - the file data.

The service responds with:

- `name` (string) - the name of the uploaded file.
- `data` (string) - the file data.
- `link` (string) - a direct link to the file uploaded to Google Drive.

## Example Request

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "example.txt", "data": "base64_encoded_data"}' http://18.193.86.9/api/upload-to-google-drive/
