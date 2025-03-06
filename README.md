# Assignment Project

## Project Overview
This is a Django-based project that integrates Google OAuth authentication, Google Drive API, and WebSockets using Django Channels. It allows users to authenticate via Google, interact with Google Drive, and use real-time WebSockets for communication.

## Features
- **Google OAuth Authentication**
- **Google Drive File Uploads**
- **WebSockets for Real-Time Communication**
- **Django REST Framework API**
- **Redis for Channel Layer**
- **Deployable on Render**

---

## Installation Steps

### **1 Clone the Repository**
```bash
git clone https://github.com/soham-gits/assignment.git
cd assignment
```

### **2 Create & Activate Virtual Environment**
```bash
python -m venv env
source env/bin/activate   # On macOS/Linux
env\Scripts\activate     # On Windows
```

### **3 Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4 Set Up Environment Variables**
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY="your-secret-key"
DEBUG=True
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_AUTH_REDIRECT_URI="http://localhost:8000/auth/callback/"
GOOGLE_DRIVE_SCOPES="https://www.googleapis.com/auth/drive.file"
REDIS_HOST="127.0.0.1"
REDIS_PORT="6379"
```

### **5 Run the Server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## API Endpoints & Testing in Postman

### **1 Google Authentication Flow**
#### Initiate Google Auth Flow
**Endpoint:** `GET /auth/google/login/`
- Redirects the user to the Google authentication page.

#### Google OAuth Callback
**Endpoint:** `GET /auth/google/callback/`
- Handles authentication response from Google and returns user data.

**Test in Postman:**
1. Import the Postman collection `Assignment.postman_collection.json`
2. Use the `Google Auth` requests to test authentication.

---

### **2⃣ Google Drive Integration**
#### Connect Google Drive
**Endpoint:** `GET /drive/connect/`
- Authorizes access to Google Drive.

#### Upload File to Google Drive
**Endpoint:** `POST /drive/upload/`
- Uploads a file to Google Drive.
- **Body:** `{ "file": "<file>" }`

#### Fetch and Download Files
**Endpoint:** `GET /drive/files/`
- Retrieves a list of files from Google Drive.

**Example:** `http://127.0.0.1:8000/drive/files/`

#### Download Specific File
**Endpoint:** `GET /drive/download/<file_id>/`
- Downloads a specific file from Google Drive.

**Example:** `http://127.0.0.1:8000/drive/download/file-id/`

**Test in Postman:**
- Use `Google Drive` requests in the Postman collection to test file upload/download.

---

### **3⃣ WebSocket for User Chat**
#### Real-Time Chat
- Connect via WebSocket at:
  ```
  ws://localhost:8000/ws/chat/
  ```
- Exchange real-time messages between users.

**Test using Postman:**
- Import `WebSocket_api.json` and test the WebSocket connection.