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
        ("categories", str),
        ("ingredients", t.Any),
        ("steps", str),
        ("link_to_photo", t.Optional[str]),
        ("link_to_instruction_video", t.Optional[str]),
        ("external_recipe_links", t.Optional[str]),
        ("null", t.Any),
        ("submitter_email", t.Optional[str]),
        ("author_name", t.Optional[str]),
        ("social_links", t.Optional[str]),
        ("book_merch_links", t.Optional[str]),
        ("difficulty", t.Optional[int]),
        ("cuisine", t.Optional[str]),
        ("diet", t.Optional[str])
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