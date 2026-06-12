from contextlib import asynccontextmanager
import select

from fastapi import FastAPI, Request, Depends, status, HTTPException
from sqlmodel import Session, select
import uvicorn

from setup import init_app
from helpers.db import Member, Ring, get_all_members, get_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = init_app()

    app.state.api_key = config.api_keys
    app.state.default_ring = config.default_ring

    yield


app = FastAPI(title="Webring API", lifespan=lifespan)


@app.get("/")
def read_root(request: Request):
    return {
        f"Hello there! Navigate to {request.base_url}webring/{request.app.state.default_ring} to get all members of the default ring"
    }


@app.get("/webring/all", response_model=list[Member])
def read_default_ring(
    request: Request, all_members: list[Member] = Depends(get_all_members)
):
    return all_members


@app.get("/webring/{ring_name}")
def read_item(ring_name: str, all_members: list[Member] = Depends(get_all_members)):
    return all_members


# @app.get("/next/{ring_name}/{owner}", response_model=Member)
# def read_next_from_owner(
#     ring_name: str, owner: str, session: Session = Depends(get_db_session)
# ):
#     current_index = session.exec(
#         select(Member.index).where(Member.owner == owner)
#     ).first()

#     if current_index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="")

#     return session.exec(select(Member).where(Member.index == current_index))


# @app.get("/prev/{ring_name}/{owner}", response_model=Member)
# def read_prev_from_owner(
#     ring_name: str, owner: str, session: Session = Depends(get_db_session)
# ):
#     pass


def main():
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)


if __name__ == "__main__":
    main()
