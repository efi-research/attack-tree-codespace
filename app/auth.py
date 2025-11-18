"""Authentication module for Google SSO."""
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import HTTPException, Request, status
from authlib.integrations.starlette_client import OAuth

load_dotenv()

# OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:8000/auth/callback')

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    print("WARNING: Google OAuth credentials not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file")

# Initialize OAuth
oauth = OAuth()

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def get_current_user(request: Request) -> Optional[dict]:
    """Get the current authenticated user from session."""
    return request.session.get('user')


def require_auth(request: Request) -> dict:
    """Require authentication. Raises HTTPException if not authenticated."""
    user = get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in with Google."
        )
    return user
