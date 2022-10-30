from parser import expr
import re
from collections import OrderedDict
import logging as log
import typing as t
from .constants import UNPARSABLE_INGREDIENT, UNPARSABLE_UNIT, FRAC_CHARS_TO_DEC
from .matchers import fraction_match, decimal_match, number_match


def parse_ingredients(s: str):

    result = []
    section = {"sectionTitle": "", "ingredients": []}
    for line in s.split("\n"):
        ing = parse_ingredient(line)
        if ing == UNPARSABLE_INGREDIENT:
            continue
        section["ingredients"].append(ing)

    result.append(section)
    from pprint import pprint

    pprint(result)
    return result

def parse_section(m: str) -> t.Optional[str]:
    m = m.strip()
    if m.startswith('(') and m.endswith(')'):
        return m[1:-1].strip()

def parse_ingredient(m: str):
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
        # there is probably no unit and the first word was part of the ingredients.
        # i.e. "1 Granny Smith Apple"
        result["customUnit"] = ""
        rest[0] = possible_unit + " " + rest[0]
    else:
        result["unit"] = unit
    ingredient, *modifier = rest[0].split(",", 1)
    result["ingredient"] = ingredient
    if modifier:
        result["modifier"] = modifier[0].strip()

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


def _parse_custom_unit(m: str) -> t.Optional[t.Tuple[str, int]]:
    if match := re.match('"(.*)"', m):
        return (match.group(1), len(match.group(1) + 2))
    first, _ = m.split(" ", 1)
    return (first, len(first))


def parse_amount(m: str) -> t.Optional[t.Tuple[str, int]]:
    """
    Returns the match, and a number indicating the characters
    consumed from the string. The char should be used to
    slice off what was used in the calling function
    """
    matchers = OrderedDict(
        (
            ("NUMBER_MATCH", number_match),
            ("FRACTION_MATCH", fraction_match),
            ("DECIMAL_MATCH", decimal_match),
        )
    )
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


if __name__ == "__main__":
    parse_ingredients(" ¼ cup dark rum or cognac (optional)")
