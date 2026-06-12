from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi_globals import g

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    API_KEYS: list[str] = g.api_keys

    if api_key_header in API_KEYS:
        return api_key_header
    if api_key_query in API_KEYS:
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key"
    )
