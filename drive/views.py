import tempfile
import io
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

def authenticate_drive():
    """Authenticates Google Drive API using service account credentials."""
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)

@csrf_exempt
def upload_file_to_drive(request):
    """Uploads a file to Google Drive."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    drive_service = authenticate_drive()
    file_metadata = {
        "name": uploaded_file.name,
        "mimeType": uploaded_file.content_type,
    }

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name  

    try:
        media = MediaFileUpload(temp_file_path, mimetype=uploaded_file.content_type, resumable=True)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return JsonResponse({"message": "File uploaded successfully!", "file_id": file["id"]})
    except Exception as e:
        return JsonResponse({"error": "Failed to upload file", "details": str(e)}, status=500)

def list_drive_files(request):
    """Lists files in Google Drive."""
    drive_service = authenticate_drive()
    try:
        files = drive_service.files().list().execute()
        file_list = [{"id": file["id"], "name": file["name"]} for file in files.get("files", [])]
        return JsonResponse({"files": file_list})
    except Exception as e:
        return JsonResponse({"error": "Failed to fetch files", "details": str(e)}, status=500)

def download_drive_file(request, file_id):
    """Downloads a file from Google Drive."""
    drive_service = authenticate_drive()

    try:
        drive_request = drive_service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, drive_request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)

        # Get file metadata for naming
        file_metadata = drive_service.files().get(fileId=file_id).execute()
        filename = file_metadata.get("name", f"{file_id}.pdf")

        response = HttpResponse(file_stream.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return JsonResponse({"error": "Failed to download file", "details": str(e)}, status=500)
