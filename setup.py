from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    json_path: Path
    api_key: str | None


def init_app() -> Config:
    settings = init_envs()

    api_key = settings.get("api_key")
    json_path = Path(settings.get("json_path", ""))

    if not json_path.is_file():
        import sys

        print(
            f"Json path configured to {json_path}. \nIt's either not set or configured isn't a valid path\n\nDo you want to create a JSON database in ./data/database.json?"
        )

        answer = input("y/N: ")

        if answer.lower == "y":
            try:
                f = open("data/database.json", "x")
                f.close()
            except FileExistsError:
                print("./data/database.json file already exists. Using that instead")
            except Exception as e:
                import sys

                print(f"Encountered exceptioned {e}\nQuitting Early")
                sys.exit(1)
        else:
            sys.exit("Refused to create database, Exiting now.")

    if api_key is None or api_key == "":
        print("API_KEY env var not set. Running without key protection")
        api_key = None

    config = Config(json_path, api_key)

    return config


def init_envs() -> dict[str, str]:
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("API_KEY", "")
    json_path = os.getenv("JSON_DATABASE", "")

    config: dict[str, str] = dict()
    config["api_key"] = api_key
    config["json_path"] = json_path

    return config
