from fastapi import FastAPI
from fastapi_globals import GlobalsMiddleware, g
import uvicorn

from setup import init_app
from helpers.json_helpers import load_data

# import helpers.json_models as json_models

app = FastAPI(title="Webring API")
app.add_middleware(GlobalsMiddleware)


@app.get("/")
def read_root():
    return {"Hello, World"}


@app.get("/webring/{url}")
def read_item(item_id: str, q: str | None = None):  # type: ignore
    return {"item_id": item_id, "q": q}  # type: ignore


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):  # type: ignore
    return {"item_name": item.name, "item_id": item_id}  # type: ignore


def main():
    config = init_app()

    g.api_key = config.api_keys
    g.json_path = config.json_path

    load_data()
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)


if __name__ == "__main__":
    main()
