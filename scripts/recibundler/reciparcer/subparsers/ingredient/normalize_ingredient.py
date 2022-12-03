import re
from .alias_ingredient import alias_ingredient


def normalize_ingredient(ing: str) -> str:
    """
    Some final doctoring of the ingredient
    """
    if matches := re.match("([(\[\])].*\d.*[(\[\])])(.*)", ing):
        ing = matches.group(2).strip()

    return alias_ingredient(ing)
