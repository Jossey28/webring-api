from dataclasses import dataclass
from pathlib import Path
from helpers.db import init_db


@dataclass
class Config:
    default_ring: str
    api_keys: list[str] | None


def init_app() -> Config:
    import os, dotenv, typing

    dotenv.load_dotenv(dotenv_path=".env", override=True)

    api_keys = os.getenv("API_KEYS")
    db_path = os.getenv("SQL_DATABASE")
    default_ring = os.getenv("DEFAULT_RING", "main")

    db_path = Path(typing.cast(str, db_path))
    if not db_path.is_file():
        raise SystemExit(
            f"Unable to validate the provided path: {db_path} using env var. Make sure to create the sqlite file before running the program"
        )

    if api_keys is None:
        print("API_KEY env var is empty. Running without key protection")
    else:
        api_keys = [key for key in api_keys.split(",")]
        assert len(api_keys) != 0

    init_db(db_path)

    return Config(default_ring=default_ring, api_keys=api_keys)
