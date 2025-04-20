from fastapi import APIRouter, status, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.config import Config
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from jose import jwt
import os
from modules import database
from datetime import datetime, timedelta

router = APIRouter()

# Config for OAuth
config = Config('.env')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
JWT_ALGORITHM = 'HS256'

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/auth/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google/callback')
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
        raise HTTPException(status_code=400, detail=f'Google OAuth failed: {str(e)}')

    # user_info contains 'sub' (Google user id), 'email', 'name', etc.
    google_id = user_info.get('sub') or user_info.get('id')
    email = user_info.get('email')
    name = user_info.get('name')

    user = await database.get_user_by_google_id(google_id)
    if not user:
        user_id = await database.create_user_with_google(google_id=google_id, email=email, name=name)
    else:
        user_id = user['user_id']

    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': datetime.utcnow() + timedelta(days=7)  # token valid for 7 days
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return JSONResponse({
        'access_token': token,
        'token_type': 'bearer',
        'user_id': user_id,
        'email': email,
        'name': name
    })