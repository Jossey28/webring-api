from dataclasses import dataclass


@dataclass
class Config:
    json_path: str
    api_key: str


def init_app() -> Config:
    config = 1

    init_envs()

    return config


def init_envs() -> dict[str, str]:
    import os

    pass


def init_config():
    pass
