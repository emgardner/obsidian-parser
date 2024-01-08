import os
import json
from dataclasses import dataclass
from pathlib import Path
import marko
import shutil
import re
from parser_extensions import FrontMatterExtension
from helpers import slugify_filename


@dataclass
class Settings:
    vaultRoot: str
    vaultDirectory: str
    outDirectory: str


def parse_settings(file: str):
    with open(file) as f:
        settings = json.loads(f.read())
        return Settings(**settings)


def update_links(filepath: str):
    print(filepath)
    _mdParser = marko.Markdown(
        renderer=marko.md_renderer.MarkdownRenderer, extensions=[FrontMatterExtension]
    )
    content = ""
    with open(filepath) as f:
        content = f.read()
    # document = marko.parse(content)
    document = _mdParser.parse(content)
    with open(filepath, "w+") as f:
        f.write(_mdParser.render(document))


def process_file(settings, file_path):
    output = os.path.abspath(
        os.path.expanduser(os.path.expandvars(settings.outDirectory))
    )
    fp = os.path.split(file_path)
    new_dir_name = sluggify_filename(fp[1].split(".")[0])
    new_dir = output + "/" + new_dir_name
    if os.path.exists(new_dir):
        pass
    else:
        os.mkdir(new_dir)
    shutil.copy(file_path, new_dir + "/index.md")

    update_links(new_dir + "/index.md")


def get_files(settings: Settings):
    base = os.path.abspath(
        os.path.expanduser(os.path.expandvars(settings.vaultDirectory))
    )
    output = os.path.abspath(
        os.path.expanduser(os.path.expandvars(settings.outDirectory))
    )
    if output == base:
        raise Exception("outputDirectory and vault must be different")
    if os.path.exists(output):
        pass
        #    os.rmdir(output)
        #    os.mkdir(output)
    else:
        os.mkdir(output)
    for root, dirs, files in os.walk(base):
        for name in files:
            filepath = os.path.join(root, name)
            process_file(settings, filepath)
        # for name in dirs:
        #    print(os.path.join(root, name))


if __name__ == "__main__":
    settings = parse_settings("./settings.json")
    get_files(settings)
