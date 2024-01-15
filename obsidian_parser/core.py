import os
from pathlib import Path
import marko
import shutil
from parser_extensions import ObsidianRenderer, create_extension, ObsidianExtension
from helpers import slugify_filename
from settings import Settings, parse_settings


def update_links(settings: Settings, source_path: str, target_path: str):
    ObsidianRenderer.file_data = {
        "settings": settings,
        "source_path": source_path,
        "target_path": target_path,
    }
    _mdParser = marko.Markdown(
        renderer=ObsidianRenderer,
        extensions=[create_extension(settings, source_path, target_path)],
    )
    content = ""
    with open(source_path) as f:
        content = f.read()
    document = _mdParser.parse(content)
    with open(target_path, "w+") as f:
        f.write(_mdParser.render(document))


def process_file(settings, file_path):
    output = settings.outDirectory
    rel_dir = file_path.split(settings.vaultDirectory)
    new_path = slugify_filename(rel_dir[1].split(".")[0])
    new_dir = output
    for directory in new_path.split("/"):
        if len(directory):
            new_dir += "/" + directory
            if os.path.exists(new_dir):
                pass
            else:
                os.mkdir(new_dir)
    update_links(settings, file_path, new_dir + "/index.md")


def get_files(settings: Settings):
    base = settings.vaultDirectory
    output = settings.outDirectory
    if output == base:
        raise Exception("outputDirectory and vault must be different")
    if os.path.exists(output):
        pass
        # shutil.rmtree(output)
        # os.mkdir(output)
    else:
        os.mkdir(output)
    for root, dirs, files in os.walk(base):
        for name in files:
            filepath = os.path.join(root, name)
            process_file(settings, filepath)
