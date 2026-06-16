from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
import uvicorn

from setup import init_app
from helpers.db import Member, get_all_members, get_member_index, get_member_owner


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


@app.get("/webring/{ring_name}", response_model=list[Member])
def read_item(ring_name: str, all_members: list[Member] = Depends(get_all_members)):
    return all_members


@app.get("/next/owner/{ring_name}/{owner}", response_model=Member)
def read_next_from_owner(
    request: Request,
    ring_name: str,
    owner: str,
    next: Member = Depends(get_member_owner),
):
    return next


@app.get("/prev/owner/{ring_name}/{owner}", response_model=Member)
def read_prev_from_owner(
    request: Request,
    ring_name: str,
    owner: str,
    prev: Member = Depends(get_member_owner),
):
    return next


@app.get("/next/index/{ring_name}/{index}", response_model=Member)
def read_next_from_index(
    request: Request,
    ring_name: str,
    index: int,
    next: Member = Depends(get_member_index),
):
    return next


@app.get("/prev/index/{ring_name}/{index}", response_model=Member)
def read_prev_from_index(
    request: Request,
    ring_name: str,
    index: int,
    prev: Member = Depends(get_member_index),
):
    return next


@app.get("/next/site/{ring_name}/{site}", response_model=Member)
def read_next_from_site(
    request: Request,
    ring_name: str,
    site: str,
    next: Member = Depends(get_member_index),
):
    return next


@app.get("/prev/site/{ring_name}/{site}", response_model=Member)
def read_prev_from_site(
    request: Request,
    ring_name: str,
    site: str,
    prev: Member = Depends(get_member_index),
):
    return next


def main():
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)


if __name__ == "__main__":
    main()
