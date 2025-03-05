from django.http import JsonResponse
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt

def google_login(request):
    """Generates Google OAuth login URL and returns it as a JSON response."""
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_AUTH_REDIRECT_URI}"
        "&scope=openid email profile"
        "&access_type=offline"
    )
    return JsonResponse({"auth_url": auth_url})

@csrf_exempt
def google_callback(request):
    """Handles Google OAuth callback, exchanges code for tokens, and returns user info."""
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    # Exchange authorization code for access token
    token_data = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_AUTH_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    ).json()

    if "access_token" not in token_data:
        return JsonResponse({"error": "Failed to get access token", "details": token_data}, status=400)

    # Fetch user info from Google
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token_data['access_token']}"},
    ).json()

    return JsonResponse({"user_info": user_info})
