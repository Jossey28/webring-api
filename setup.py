from dataclasses import dataclass
from pathlib import Path
from helpers.db import init_db


@dataclass
class Config:
    default_ring: str
    admin_username: str
    admin_password: str


def init_app() -> Config:
    import os, dotenv

    dotenv.load_dotenv(dotenv_path=".env", override=True)

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "password")

    db_path = os.getenv("SQL_DATABASE")
    default_ring = os.getenv("DEFAULT_RING", "main")

    if not db_path:
        raise SystemExit(
            "db_path environment variable isn't set. make sure to add it into your environment file"
        )

    db_path = Path(db_path)
    if not db_path.is_file():
        raise SystemExit(
            f"Unable to validate the provided path: {db_path} using env var. Make sure to create the sqlite file before running the program"
        )

    init_db(db_path)

    return Config(
        default_ring=default_ring,
        admin_username=admin_username,
        admin_password=admin_password,
    )
