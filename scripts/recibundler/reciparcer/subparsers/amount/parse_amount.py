from collections import OrderedDict
import typing as t
import re
from recibundler.constants import DASHES
from .matchers import fraction_match, number_match, decimal_match
import logging as log

def parse_amount(m: str) -> t.Optional[t.Tuple[t.List[float], int]]:
    """
    Returns the match, and a number indicating the characters
    consumed from the string. The char should be used to
    slice off what was used in the calling function
    """
    matchers = OrderedDict(
        (
            ("FRACTION_MATCH", fraction_match),
            ("NUMBER_MATCH", number_match),
            ("DECIMAL_MATCH", decimal_match),
        )
    )
    if re_match := re.match('([^a-zA-Z]*)([a-zA-Z].*)', m):
        amount, ing = re_match.groups()
    else:
        return None
    
    for dash in DASHES:
        if dash in amount:
            min, max = amount.split(dash)
            min, max = f"{min} cup devnull", f"{max} cup devnull"
            parsed_min = parse_amount(min)
            parsed_max = parse_amount(max)
            if parsed_min and parsed_max:
                if len(parsed_min[0]) > 1 or len(parsed_max[0]) > 1:
                    return None
                return (
                    [parsed_min[0][0], parsed_max[0][0]],
                    parsed_min[1] + parsed_max[1] + 1,
                )

    for matcher, fn in matchers.items():
        match = fn(amount + ing)
        if match:
            log.debug(f"matched on {matcher}")
            return ([match[0]], match[1])

    return None