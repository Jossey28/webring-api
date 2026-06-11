from pathlib import Path
from pydantic import BaseModel, Field
from fastapi_globals import g


class Member(BaseModel):
    index: int = Field(gt=0)
    owner: str
    site: str

    prev_site: Member | None
    next_site: Member | None


def save_data():
    path: Path = g.json_path

    pass
