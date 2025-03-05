from google_auth_oauthlib.flow import Flow
from django.conf import settings

def get_google_auth_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_AUTH_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=settings.GOOGLE_AUTH_SCOPE
    )
    flow.redirect_uri = settings.GOOGLE_AUTH_REDIRECT_URI
    return flow.authorization_url()[0]

def fetch_google_user_info(token):
    import requests
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
