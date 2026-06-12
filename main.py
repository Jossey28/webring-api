from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi_globals import GlobalsMiddleware, g
import uvicorn

from setup import init_app
from helpers.json_helpers import Member, MemberListModel, load_data, read_input_buffer


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = init_app()

    g.api_key = config.api_keys
    g.json_path = config.json_path
    g.default_ring = config.default_ring

    load_data()

    yield


app = FastAPI(title="Webring API", lifespan=lifespan)
app.add_middleware(GlobalsMiddleware)


@app.get("/")
def read_root(request: Request):
    return {
        f"Hello there! Navigate to {request.base_url}webring/all to get all members"
    }


@app.get("/webring/all")
def read_default_ring() -> list[Member]:
    input_buffer = read_input_buffer()
    members: list[Member] = MemberListModel.validate_json(input_buffer)
    members_valid = [member for member in members if member.ring_name == g.default_ring]
    print(f"default 1 is: {g.default_ring}")
    print(f"default 2 is: {g.json_path}")
    print(f"default 3 is: {g.api_key}")

    return members_valid


# @app.get("/webring/{url}")
# def read_item(item_id: str):
#     return {"item_id": item_id}


def main():
    uvicorn.run("main:app", host="localhost", port=8080, reload=False)


if __name__ == "__main__":
    main()
