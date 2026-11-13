"""Firebase ID-token verification with google-auth (lightweight, no firebase-admin needed)."""
from fastapi import Header, HTTPException
from google.auth.transport import requests as g_requests
from google.oauth2 import id_token

from app.config import settings

_request = g_requests.Request()


def current_user(authorization: str = Header(default="")) -> dict:
    """Return the signed-in user, or an anonymous user when REQUIRE_AUTH is false."""
    if not settings.require_auth:
        return {"uid": "anonymous"}
    if not settings.firebase_project_id:
        raise HTTPException(status_code=500, detail="Server misconfigured: FIREBASE_PROJECT_ID is not set")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    try:
        claims = id_token.verify_firebase_token(
            authorization.split(" ", 1)[1], _request, audience=settings.firebase_project_id
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
    if not claims:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"uid": claims.get("user_id") or claims.get("sub"), **claims}
