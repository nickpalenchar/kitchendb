import re
import typing as t


def fraction_match(m: str) -> t.Optional[t.Tuple[str, int]]:
    match = re.search("(\d?[\s&+]{0,4}?\d+\/\d+)(.*)", m)
    if not match:
        return None
    groups = match.groups()
    if len(match.groups() < 1):
        return None
    return (groups[0].strip(), len(groups[0]))


def decimal_match(m: str) -> t.Optional[t.Tuple[str, int]]:
    match = re.search("((\d\s)?\d*(\.\d)*)(.*)", m)
    if not match:
        return None
    groups = match.groups()
    if len(match.groups()) < 1:
        return None
    return (groups[0].strip(), len(groups[0]))
