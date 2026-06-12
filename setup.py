from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    json_path: Path
    default_ring: str
    api_keys: list[str] | None


def init_app() -> Config:
    settings = init_envs()

    api_key_list = settings.get("api_key")
    default_ring = settings.get("default_ring", "main")
    json_path = Path(settings.get("json_path", ""))

    if not json_path.is_file():
        import sys

        print(
            f"Json path configured to {json_path}. \nIt's either not set or configured isn't a valid path\n\nDo you want to create a JSON database in ./data/database.jsonl?"
        )

        answer = input("y/N: ")

        if answer.lower() == "y":
            try:
                f = open("data/database.jsonl", "x")
                f.close()
                print(
                    "Created the file for you. Use the example file to create your own webring"
                )
                sys.exit(1)
            except FileExistsError:
                print("\n./data/database.jsonl file already exists. Using that")
                json_path = Path("./data/database.jsonl")
            except Exception as e:
                import sys

                print(f"Encountered exceptioned {e}\nQuitting Early")
                sys.exit(1)
        else:
            sys.exit("User refused to create database, Exiting now.")

    if api_key_list is not None:
        api_keys = api_key_list.split(",")
        if len(api_keys) == 0:
            print("API_KEY env var is empty. Running without key protection")
            return Config(json_path, default_ring, api_keys)
        return Config(json_path, default_ring, api_keys)

    else:
        print("API_KEY env var not set. Running without key protection")
        config = Config(json_path, default_ring, None)

        return config


def init_envs() -> dict[str, str]:
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("API_KEYS", "")
    json_path = os.getenv("JSON_DATABASE", "")
    default_ring = os.getenv("DEFAULT_RING", "")

    config: dict[str, str] = dict()
    config["api_key"] = api_key
    config["json_path"] = json_path
    config["default_ring"] = default_ring

    return config
