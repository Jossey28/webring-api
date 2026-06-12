from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from sqlalchemy import func
from sqlmodel import Session, select
import uvicorn

from setup import init_app
from helpers.db import Member, get_db_session


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
        f"Hello there! Navigate to {request.base_url}webring/all to get all members"
    }


@app.get("/webring/all", response_model=list[Member])
def read_default_ring(request: Request, session: Session = Depends(get_db_session)):
    all_members = session.exec(
        select(Member)
    ).all()  # I can't get where to work with JSON T-T
    default_members: list[Member] = list()
    for member in all_members:
        if request.app.state.default_ring in member.rings:
            default_members.append(member)
        else:
            print(f"{member} not in default ring: {request.app.state.default_ring}")
    return default_members


# @app.get("/webring/{url}")
# def read_item(item_id: str):
#     return {"item_id": item_id}


def main():
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)


if __name__ == "__main__":
    main()
