from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from sqlmodel import Session, select
from helpers.db import Ring, get_db_session
import main

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

ADMIN_DASHBOARD_API_KEYS = main.config.api_keys


def get_api_key_admin(  # https://joshdimella.com/blog/adding-api-key-auth-to-fast-api#understanding-api-key-authentication
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str | None:

    if ADMIN_DASHBOARD_API_KEYS is None:
        return ""

    if api_key_query in ADMIN_DASHBOARD_API_KEYS:
        return api_key_query

    if api_key_header in ADMIN_DASHBOARD_API_KEYS:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key"
    )


def get_api_key_ring(
    ring_name: str,
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    session: Session = Depends(get_db_session),
) -> str | None:
    ring = session.exec(select(Ring).where(Ring.ring_name == ring_name)).first()
    if ring is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ring does not exist"
        )

    if ring.api_keys is None:
        return None

    if api_key_query in ring.api_keys:
        return api_key_query

    if api_key_header in ring.api_keys:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid or missing API Key for ring: {ring_name}",
    )
