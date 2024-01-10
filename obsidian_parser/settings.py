import json
from dataclasses import dataclass


@dataclass
class Settings:
    vaultRoot: str
    vaultDirectory: str
    outDirectory: str
    linkBase: str
    assetBase: str
    assetOutput: str


def parse_settings(file: str):
    with open(file) as f:
        settings = json.loads(f.read())
        return Settings(**settings)
