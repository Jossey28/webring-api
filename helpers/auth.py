from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

API_KEYS = ["TMP1", "TMP2"]


def get_api_key(  # https://joshdimella.com/blog/adding-api-key-auth-to-fast-api#understanding-api-key-authentication
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:

    if api_key_header in API_KEYS:
        return api_key_header
    if api_key_query in API_KEYS:
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key"
    )
