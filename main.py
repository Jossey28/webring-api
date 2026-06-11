from fastapi import FastAPI
import uvicorn

from setup import init_app

# import helpers.json_models as json_models

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello, World"}


@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None):  # type: ignore
    return {"item_id": item_id, "q": q}  # type: ignore


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):  # type: ignore
    return {"item_name": item.name, "item_id": item_id}  # type: ignore


def main():
    init_app()

    uvicorn.run("main:app", host="localhost", port=8080, reload=True)


if __name__ == "__main__":
    main()
