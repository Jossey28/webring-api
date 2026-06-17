from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
import uvicorn

from setup import init_app
from helpers.db import Member, Ring, get_all_members, get_member_index, get_member_owner
import helpers.db

config = init_app()
app = FastAPI(title="Webring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.api_key = config.api_keys
app.state.default_ring = config.default_ring

admin = Admin(app, helpers.db.engine)


class RingAdmin(ModelView, model=Ring):
    column_list = [Ring.id, Ring.ring_name, Ring.members]  # type: ignore


admin.add_view(RingAdmin)


@app.get("/")
def read_root(request: Request) -> set[str]:
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
    return prev


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
    return prev


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
    return prev


def main():
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)


if __name__ == "__main__":
    main()
