from parser import expr
import re
from collections import OrderedDict
import logging as log
import typing as t
from .constants import UNPARSABLE_INGREDIENT, UNPARSABLE_UNIT, FRAC_CHARS_TO_DEC
from recibundler.reciparcer.subparsers.amount import (
    parse_amount,
    _parse_unit,
    _format_amount,
)
from recibundler.reciparcer.subparsers.ingredient import normalize_ingredient


def parse_ingredients(s: str):

    result = []
    section = {"sectionTitle": "", "ingredients": []}
    for line in s.split("\n"):
        if not line:
            continue
        if section_title := parse_section(line):
            if not section["sectionTitle"]:
                section["sectionTitle"] = section_title
            else:
                result.append(section)
                section = {"sectionTitle": section_title, "ingredients": []}
            continue
        ing = parse_ingredient(line)
        if ing == UNPARSABLE_INGREDIENT:
            continue
        section["ingredients"].append(ing)  # type: ignore

    result.append(section)
    return result


def parse_section(m: str) -> t.Optional[str]:
    m = m.strip()
    if m.startswith("(") and m.endswith(")"):
        return m[1:-1].strip()
    return None


def parse_ingredient(m: str) -> t.Union[dict, object]:
    log.debug(f"parsing ingredient: {m}")
    result = {}
    m = _convert_frac_chars(m).strip()
    try:
        parsed = parse_amount(m)
        if parsed is None:
            return {"ingredient": m}
        amount_parsed, slicepoint = parsed
        amount = _format_amount([str(a) for a in amount_parsed])
        slice_rest = m[slicepoint:]
        log.debug(f"parsed amount: {amount}")
        result["amount"] = [float(a) for a in amount]
    except:
        log.warn(f"Unparsable Ingredient: {m}")
        return UNPARSABLE_INGREDIENT
    possible_unit, *rest = slice_rest.strip().split(" ", 1)
    if not rest:
        # there is only one word so it must be an ingredient with no unit
        result["customUnit"] = ""  # type: ignore
        result["ingredient"] = possible_unit  # type: ignore
        return result

    unit = _parse_unit(possible_unit)
    if unit == UNPARSABLE_UNIT:
        # there is probably no unit and the first word was part of the ingredients.
        # i.e. "1 Granny Smith Apple"
        result["customUnit"] = ""  # type: ignore
        rest[0] = possible_unit + " " + rest[0]
    else:
        result["unit"] = unit
    ingredient, *modifier = rest[0].split(",", 1)
    result["ingredient"] = normalize_ingredient(ingredient)  # type: ignore
    if modifier:
        result["modifier"] = modifier[0].strip()  # type: ignore

    log.debug(result)
    return result


def _convert_frac_chars(m: str) -> str:
    result = m
    for char, dec in FRAC_CHARS_TO_DEC.items():
        result = result.replace(char, str(dec))
    return result


if __name__ == "__main__":
    parse_ingredients(" ¼ cup dark rum or cognac (optional)")
