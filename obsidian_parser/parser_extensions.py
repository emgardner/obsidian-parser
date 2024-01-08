import marko
import marko.md_renderer
from marko.parser import Parser
from marko.block import BlockElement
from marko.inline import InlineElement
from marko.helpers import MarkoExtension
import re


class ObsidianWiki(InlineElement):
    """WikiLink: [[FileName]]"""

    pattern = r"\[\[ *(.+?) *\]\]"
    parse_children = True

    def __init__(self, match):
        print("Ob Link: ", match)
        self.target = match.group(1)


class ObsidianWikiRenderer(object):
    def render_obsidian_wiki(self, element):
        print(element)
        print(dir(element))
        print(element.target)
        return "[{}]({})".format(element.target, element.target)


class ObsidianImage(InlineElement):
    """WikiLink: [[FileName]]"""

    pattern = r"\!\[\[ *(.+?) *\]\]"
    parse_children = True

    def __init__(self, match):
        # print("Ob Link: ", match)
        self.target = match.group(1)


class ObsidianImageRenderer(object):
    def render_obsidian_wiki(self, element):
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


FrontMatterExtension = MarkoExtension(
    elements=[FrontMatter, ObsidianWiki],
    renderer_mixins=[FrontMatterRenderer, ObsidianWikiRenderer],
)