import json
from dataclasses import dataclass
import os


@dataclass
class Settings:
    vaultRoot: str
    vaultDirectory: str
    outDirectory: str
    imageDirectory: str
    linkBase: str
    assetBase: str
    assetOutput: str


def parse_settings(file: str):
    with open(file) as f:
        settings = json.loads(f.read())
        for k in ["vaultDirectory", "vaultRoot", "outDirectory", "assetOutput"]:
            settings[k] = os.path.abspath(
                os.path.expanduser(os.path.expandvars(settings[k]))
            )
        return Settings(**settings)
