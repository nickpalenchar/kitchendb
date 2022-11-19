import logging as log
from recibundler.reciparcer.constants import UNPARSABLE_UNIT

def _parse_unit(m: str):
    """
    Attempts to parse a unit of measurement.
    """
    log.debug(f"parsing unit: {m}")
    # NB: These acceptable enums come from the `data/schemase/recipes.json` schema.
    # keep them in sync
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

    alias_units = {
        "tbs": "tbsp",
        "tablespoon": "tbsp",
        "ts": "tsp",
        "teaspoon": "tsp",
        "pound": "lb",
        "gram": "g",
        "mililiter": "ml",
        "milliliter": "ml",
        "pt": "pint",
        "kilogram": "kg",
        "killogram": "kg",
        "gallon": "gal",
        "ounce": "oz",
        "fluid ounces": "fl oz",
    }

    parsed = m.strip().replace(".", "").lower()
    if parsed in valid_units:
        return parsed.lower()
    if parsed in alias_units.keys():
        return alias_units[parsed]
    if parsed.endswith("s"):
        return _parse_unit(parsed[:-1])
    return UNPARSABLE_UNIT
