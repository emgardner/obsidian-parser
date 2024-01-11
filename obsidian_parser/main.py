import os
from pathlib import Path
import marko
import shutil
import re
from parser_extensions import ObsidianRenderer, create_extension, ObsidianExtension
from helpers import slugify_filename
from settings import Settings, parse_settings
from core import update_links, process_file, get_files
import sys

if __name__ == "__main__":
    settings_file = "settings.json"
    if len(sys.argv) >= 2:
        settings_file = sys.argv[1]
    settings = parse_settings(settings_file)
    get_files(settings)
