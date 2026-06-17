from fastapi import Depends, HTTPException, status, Security
from starlette.requests import Request
from sqlmodel import Session, select

from fastapi.security import APIKeyHeader, APIKeyQuery
from sqladmin.authentication import AuthenticationBackend

from helpers.db import Ring, get_db_session

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


class AdminPageBackend(
    AuthenticationBackend
):  # https://stackoverflow.com/questions/79869816/how-to-work-sqladmin-token-and-secret-key-management#
    def __init__(
        self, secret_key: str, admin_username: str, admin_password: str
    ) -> None:
        super().__init__(secret_key)

        self.admin_username = admin_username
        self.admin_password = admin_password

        print(f"username: {self.admin_username}")
        print(f"password: {self.admin_password}")

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == self.admin_username and password == self.admin_password:
            request.session.update({"token": "admin_authenticated"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if token == "admin_authenticated":
            return True
        return False


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
