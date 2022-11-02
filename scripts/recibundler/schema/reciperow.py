import typing as t
from datetime import datetime

reciperow = t.NamedTuple(
    "reciperow",
    [
        ("timestamp", str),
        ("name", str),
        ("summary", t.Optional[str]),
        ("prep_time", t.Optional[int]),
        ("cook_time", t.Optional[str]),
        ("ingredients", t.Any),
        ("steps", t.List[str]),
        ("link_to_photo", t.Optional[str]),
        ("submitter_email", t.Optional[str]),
    ],
)

def is_recipe_old(recipe: reciperow, since) -> bool:
    """
    Parses the date from the "google" submission date and
    simply compares the date delta with `since`. If True, this is
    the next recipe to use
    """
    recipe_date = datetime.strptime(recipe.timestamp, "%m/%d/%Y %H:%M:%S")
    return recipe_date <= since

def isodate_from_recipe(recipe: reciperow) -> datetime:
    return datetime.strptime(recipe.timestamp, "%m/%d/%Y %H:%M:%S")