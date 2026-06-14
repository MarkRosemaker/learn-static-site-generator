from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    def __repr__(self) -> str:
        return str(self)


# Pre‑compile all patterns (module‑level constants)
RE_HEADING = re.compile(r"^(#{1,6}) .")
RE_CODE = re.compile(r"(?s)^```\n.*\n```$")
RE_QUOTE = re.compile(r"^(> {0,1}.*(?:\n|$))+$")
RE_UNORDERED_LIST = re.compile(r"^(- .*(?:\n|$))+$")
RE_ORDERED_NUMBER = re.compile(r"^(\d+)\. ")


def block_to_block_type(txt: str) -> BlockType:
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if RE_HEADING.match(txt):
        return BlockType.HEADING
    # Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    if RE_CODE.match(txt):
        return BlockType.CODE
    # Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required.
    if RE_QUOTE.match(txt):
        return BlockType.QUOTE
    # Every line in an unordered list block must start with a - character, followed by a space.
    if RE_UNORDERED_LIST.match(txt):
        return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if is_ordered_list(txt):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_ordered_list(txt: str) -> bool:
    i = 1
    for line in txt.splitlines():
        m = RE_ORDERED_NUMBER.match(line)
        if not m or int(m.group(1)) != i:
            return False
        i += 1
    return True
