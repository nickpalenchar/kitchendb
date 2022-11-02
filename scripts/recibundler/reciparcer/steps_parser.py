import enum
import typing as t
import string


def parse_steps(text: str) -> t.List[str]:
    # TODO - sections
    steps = [strip_number_prefix(t) for t in text.split("\n") if t]
    return [{"sectionTitle": "", "steps": steps}]


def strip_number_prefix(text: str) -> str:
    for i, letter in enumerate(text):
        if letter in string.ascii_letters:
            return text[i:]
