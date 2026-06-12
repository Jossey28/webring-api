from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    json_path: Path
    default_ring: str
    api_keys: list[str] | None


def init_app() -> Config:
    import os, dotenv, typing

    dotenv.load_dotenv(dotenv_path=".env")

    api_keys = os.getenv("API_KEYS")
    json_path = os.getenv("JSON_DATABASE")
    default_ring = os.getenv("DEFAULT_RING", "main")

    json_path = Path(typing.cast(str, json_path))
    if not json_path.is_file():
        raise SystemExit(
            f"Unable to validate the provided path: {json_path} using env var. Make sure to follow the example file"
        )

    if api_keys is None:
        print("API_KEY env var is empty. Running without key protection")
    else:
        api_keys = [key for key in api_keys.split(",")]
        assert len(api_keys) != 0

    return Config(json_path=json_path, default_ring=default_ring, api_keys=api_keys)
