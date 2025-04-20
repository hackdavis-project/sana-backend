from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
JWT_ALGORITHM = 'HS256'

def get_current_user(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get('user_id')
        email = payload.get('email')
        name = payload.get('name')
        if not user_id or not email or not name:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return {'user_id': user_id, 'email': email, 'name': name}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
