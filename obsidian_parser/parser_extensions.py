import marko
import marko.md_renderer
from marko.parser import Parser
from marko.block import BlockElement
from marko.inline import InlineElement
from marko.helpers import MarkoExtension
import re
from helpers import slugify_filename
import os
import shutil


class ObsidianWiki(InlineElement):
    """WikiLink: [[FileName]]"""

    pattern = r"\[\[ *(.+?) *\]\]"
    parse_children = True

    def __init__(self, match):
        self.target = match.group(1)


class ObsidianWikiRenderer(object):
    def render_obsidian_wiki(self, element):
        return "[{}]({})".format(element.target, element.target)


class ObsidianImage(InlineElement):
    """WikiLink: [[FileName]]"""

    pattern = r"\!\[\[ *(.+?) *\]\]"
    parse_children = True

    def __init__(self, match):
        self.target = match.group(1)


class ObsidianImageRenderer(object):
    def render_obsidian_image(self, element):
        return "[{}]({})".format(element.target, element.target)


class FrontMatter(BlockElement):
    priority = 100  # High priority to parse it before other elements
    pattern = re.compile(r"( {,3})(-{3,}|~{3,})[^\n\S]*(.*?)$", re.DOTALL)
    parse_children = False

    def __init__(self, match):
        self.content = match

    @classmethod
    def match(cls, source):
        m = source.expect_re(cls.pattern)
        if not m:
            return None
        prefix, leading, info = m.groups()
        if leading[0] == "`" and "`" in info:
            return None
        return m

    @classmethod
    def parse(cls, source):
        source.next_line()
        source.consume()
        lines = []
        while not source.exhausted:
            line = source.next_line()
            if line is None:
                break
            source.consume()
            m = re.match(r"( {,3})(-{3,}|~{3,})[^\n\S]*(.*?)$", line, re.DOTALL)
            if m:
                break
            lines.append(line)
        return "".join(lines)


class FrontMatterParser(Parser):
    def parse(self, block):
        match = FrontMatter.pattern.match(block)
        if match:
            self.consume(len(match.group(0)))
            return FrontMatter(match)


class FrontMatterRenderer(object):
    def render_front_matter(self, element):
        return "---\n{}---\n".format(element.content)


class ObsidianExtension(MarkoExtension):
    elements = [FrontMatter, ObsidianWiki, ObsidianImage]

    def extend(self, parser):
        parser.inline_parsers.insert(0, FrontMatterParser())
        parser.inline_parsers.insert(1, ObsidianImageParser())
        parser.inline_parsers.insert(2, ObsidianWikiParser())


def create_extension(settings, source_path, target_path):
    return MarkoExtension(
        elements=[FrontMatter, ObsidianWiki, ObsidianImage],
    )


class ObsidianRenderer(marko.md_renderer.MarkdownRenderer):
    file_data = {}

    def __init__(self):
        super().__init__()

    def render_obsidian_wiki(self, element):
        settings = self.file_data.get("settings")
        target_path = self.file_data.get("target_path")
        fp = os.path.split(target_path)
        return "[{}]({})".format(
            element.target, settings.linkBase + slugify_filename(element.target)
        )

    def render_obsidian_image(self, element):
        settings = self.file_data.get("settings")
        target_path = self.file_data.get("target_path")
        fp = os.path.split(target_path)
        shutil.copy(
            os.path.expanduser(os.path.expandvars(settings.vaultRoot + element.target)),
            slugify_filename(
                os.path.expanduser(
                    os.path.expandvars(settings.assetOutput + element.target)
                )
            ),
        )
        return "![{}]({})".format(
            element.target.split(".")[0],
            slugify_filename(settings.assetBase + element.target),
        )

    def render_front_matter(self, element):
        return "---\n{}---\n".format(element.content)
