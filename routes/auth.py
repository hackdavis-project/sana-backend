from fastapi import APIRouter, status, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.config import Config
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import jwt
import os
from modules import database
from datetime import datetime, timedelta
from utils.auth import get_current_user

router = APIRouter()

# Config for OAuth
config = Config(".env")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key")
JWT_ALGORITHM = "HS256"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = None
        if "userinfo" in token:
            user_info = token["userinfo"]
        elif "id_token" in token:
            user_info = await oauth.google.parse_id_token(request, token)
        else:
            # fallback: fetch userinfo from Google endpoint
            resp = await oauth.google.get("userinfo", token=token)
            user_info = resp.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth failed: {str(e)}")

    # user_info contains 'sub' (Google user id), 'email', 'name', etc.
    google_id = user_info.get("sub") or user_info.get("id")
    email = user_info.get("email")
    name = user_info.get("name")

    user = await database.get_user_by_google_id(google_id)
    if not user:
        user_id = await database.create_user_with_google(
            google_id=google_id, email=email, name=name
        )
    else:
        user_id = user["user_id"]

    payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "exp": datetime.utcnow() + timedelta(days=7),  # token valid for 7 days
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Create a redirect response to the frontend
    response = RedirectResponse(url=f"{FRONTEND_URL}/")

    # Set the auth token as a cookie
    # Use SameSite=None and Secure=True for cross-origin cookies in HTTPS environments
    # For development, we might not have HTTPS, so adjust accordingly
    is_secure = os.getenv("ENVIRONMENT", "development") == "production"

    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        samesite="lax" if not is_secure else "none",
        secure=is_secure,
        path="/",
    )

    # Set user information in cookies (non-httponly so frontend JavaScript can access)
    response.set_cookie(
        key="user_id",
        value=user_id,
        httponly=False,
        max_age=7 * 24 * 60 * 60,
        samesite="lax" if not is_secure else "none",
        secure=is_secure,
        path="/",
    )

    response.set_cookie(
        key="user_email",
        value=email,
        httponly=False,
        max_age=7 * 24 * 60 * 60,
        samesite="lax" if not is_secure else "none",
        secure=is_secure,
        path="/",
    )

    response.set_cookie(
        key="user_name",
        value=name,
        httponly=False,
        max_age=7 * 24 * 60 * 60,
        samesite="lax" if not is_secure else "none",
        secure=is_secure,
        path="/",
    )

    return response


@router.get("/auth/me")
async def get_me(user=Depends(get_current_user)):
    """
    Example route that demonstrates using the Depends(get_current_user) pattern.
    Returns the current user's information.
    """
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "name": user["name"],
        "voice_id": await database.get_voice_id(user["user_id"]),
    }
