from parser import expr
import re
import logging as log
import typing as t

UNPARSABLE_INGREDIENT = object()
UNPARSABLE_UNIT = object()

FRAC_CHARS_TO_DEC = {
    "⅘": 0.8,
    "½": 0.5,
    "⅔": 0.67,
    "¾": 0.75,
    "⅝": 0.62,
    "⅗": 0.6,
    "⅜": 0.375,
    "⅖": 0.4,
    "⅕": 0.20,
    "⅐": 0.14,
    "⅑": 0.11,
    "⅒": 0.10,
}


def parse_ingredients(s: str):

    ## TODO (1) - section titles
    result = []
    section = {
        "name": "",
    }
    for line in s.split("\n"):
        ing = _parse_ingredient(line)
        if ing == UNPARSABLE_INGREDIENT:
            continue
        result.append(ing)
    from pprint import pprint

    pprint(result)


def _parse_ingredient(m: str):
    log.debug(f"parsing ingredient: {m}")
    result = {}

    m = _convert_frac_chars(m).strip()
    try:
        amount, slicepoint = parse_amount(m)
        amount = _format_amount(amount)
        rest = m[slicepoint:]
        log.debug(f"parsed amount: {amount}")
        result["amount"] = float(amount)
    except:
        log.warn(f"Unparsable Ingredient: {m}")
        return UNPARSABLE_INGREDIENT

    possible_unit, *rest = rest.strip().split(" ", 1)
    if not rest:
        # there is only one word so it must be an ingredient with no unit
        result["customUnit"] = ""
        result["ingredient"] = possible_unit
        return result

    unit = _parse_unit(possible_unit)
    if unit == UNPARSABLE_UNIT:
        result["customUnit"] = ""
    else:
        result["unit"] = unit

    ingredient, *modifier = rest[0].split(",", 1)
    result["ingredient"] = ingredient
    if modifier:
        result["modifier"] = modifier[0]

    log.debug(result)
    return result


def _parse_unit(m: str):
    """
    Attempts to parse a unit of measurement.
    """
    log.debug(f"parsing unit: {m}")
    # NB: These acceptable enums come from the `data/schemase/recipes.json` schema.
    # keep the min sync
    valid_units = (
        "lb",
        "oz",
        "g",
        "cup",
        "fl oz",
        "ml",
        "pint",
        "tsp",
        "tbsp",
        "kg",
        "gal",
        "liter",
    )

    parsed = m.strip().replace(".", "").lower()
    if parsed in valid_units:
        return parsed
    return UNPARSABLE_UNIT


### matchers
# go through each of these to parse the amount text
###


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


def parse_amount(m: str) -> t.Optional[t.Tuple[str, int]]:
    """
    Returns the match, and a number indicating the characters
    consumed from the string. The char should be used to
    slice off what was used in the calling function
    """
    matchers = {
        "FRACTION_MATCH": fraction_match,
        "DECIMAL_MATCH": decimal_match,
    }
    for matcher, fn in matchers.items():
        match = fn(m)
        if match:
            log.debug(f"matched on {matcher}")
            return match

    return None


def _format_amount(m: str) -> str:
    """
    attempts to parse the measurement for the `amount` into its decimal form
    """
    m = re.sub("\s+", " ", m.strip())

    leading = "0"

    if " " in m:
        leading, m = m.split(" ")

    if m in FRAC_CHARS_TO_DEC.keys():
        return leading + FRAC_CHARS_TO_DEC[m]

    try:
        float(m)
        return int(leading) + round(float(m), 2)
    except ValueError:
        if "/" in m:
            num, den = m.split("/")
            return int(leading) + round(num / den, 2)


def _convert_frac_chars(m: str) -> str:
    result = m
    for char, dec in FRAC_CHARS_TO_DEC.items():
        result = result.replace(char, str(dec))
    return result
