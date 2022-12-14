import re
import typing as t


def number_match(m: str) -> t.Optional[t.Tuple[float, int]]:
    """
    simply matches for whole numbers at the beginning.
    **THIS SHOULD BE FIRST**, it safeguards against more
    complicated parsers interpreting a simple value incorrectly
    """
    match = re.search("^(\d+)[^.](.*)", m)
    if not match:
        return None
    groups = match.groups()
    if len(match.groups()) < 1:
        return None
    return (float(groups[0].strip()), len(groups[0]))


def fraction_match(m: str) -> t.Optional[t.Tuple[float, int]]:
    match = re.search("(\d?[\s&+]{0,4}?\d+\/\d+)(.*)", m)
    if not match:
        # try to look for a whole number first i.e. "1 1/2"
        return None
    groups = match.groups()
    if len(match.groups()) < 1:
        return None
    leading = "0"
    num, denom = groups[0].strip().split("/")
    if " " in num:
        leading, num = num.split(" ")
    return (int(leading) + int(num) / int(denom), len(groups[0]))


def decimal_match(m: str) -> t.Optional[t.Tuple[float, int]]:
    match = re.search("((\d\s)?\d*(\.\d*))(.*)", m)
    if not match:
        return None
    groups = match.groups()
    if len(match.groups()) < 1:
        return None
    return (float(groups[0].strip()), len(groups[0]))
