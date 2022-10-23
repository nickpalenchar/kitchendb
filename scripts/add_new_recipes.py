"""
ASSUMES YOUR WORKING DIRECTORY IS scripts/

builds new recipes from the submitted google sheet.

Each new recipe should be its own separate PR. Therefore, it should be ran with
a script that can do said checkout and PR.

**Required**: a text file, `add_new_recipes_since`, containing one line--the iso
date of the last recipe to be added. This script will 
"""
import sys
import os
import csv
import json
import typing as t
from collections import namedtuple
from schema_class import Recipe
from datetime import datetime
import build_recipes
import reciparcer
import logging
from os import path

T = t.TypeVar("T")

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARN"))

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


def add_new_recipes(filepath):
    logging.debug(f"filepath is {filepath}")

    with open(filepath, newline="") as fh:
        reader = csv.reader(fh)

        with open("add_new_recipes_since") as datefh:
            try:
                last_date = datetime.fromisoformat(datefh.read().strip())
            except ValueError:
                logging.warn("starting from beginning of time")
                last_date = datetime(year=2022, month=1, day=28)

        # skip the header
        next(reader)

        for recipe in reader:
            recipe = reciperow(*recipe)
            if is_recipe_old(recipe, last_date):
                continue
            logging.info(f"the next recipe is {recipe.name}")
            write_recipe_to_json(recipe)

            with open("add_new_recipes_since", mode="w") as datefh:
                datefh.write(str(isodate_from_recipe(recipe)))
            return

        logging.info("no new recipes")


def isodate_from_recipe(recipe: reciperow) -> datetime:
    return datetime.strptime(recipe.timestamp, "%m/%d/%Y %H:%M:%S")


def get_recipe_filename(recipe: reciperow) -> str:
    return f'{isodate_from_recipe(recipe).isoformat()[:10]}_{recipe.name.replace(" ", "-").lower()}.json'


def is_recipe_old(recipe: reciperow, since) -> bool:
    """
    Parses the date from the "google" submission date and
    simply compares the date delta with `since`. If True, this is
    the next recipe to use
    """
    recipe_date = datetime.strptime(recipe.timestamp, "%m/%d/%Y %H:%M:%S")
    return recipe_date <= since


def write_recipe_to_json(recipe: reciperow):
    # TODO parse the recipe and add it to the json file
    attrs = {
        "version": "1",
        "name": recipe.name,
        "summary": recipe.summary,
        "steps": reciparcer.parse_steps(recipe.steps),
        "ingredients": reciparcer.parse_ingredients(recipe.ingredients),
        "timestamp": recipe.timestamp,
    }
    optional_attrs = {
        "yields": None,  # TODO
        "yieldsUnit": None,  # TODO
        "prep_time": optional(recipe.prep_time),
        "cook_time": optional(recipe.cook_time),
    }

    logging.debug("parsing")
    logging.debug(f"csv row: {recipe}")
    name: str = recipe.name
    summary: str = optional(recipe.summary) or ""
    yields: t.Optional[int] = optional(4)
    yieldsUnit = None  # TODO
    prep_time: t.Optional[int] = optional(recipe.prep_time)
    cook_time: t.Optional[int] = optional(recipe.cook_time)
    ingredients = reciparcer.parse_ingredients(recipe.ingredients)
    steps: t.Lest = reciparcer.parse_steps(recipe.steps)
    link_to_photo: t.Optional[str] = optional(recipe.link_to_photo)
    logging.info("Successfully imported recipe")
    recipe = Recipe(**attrs)

    filename = get_recipe_filename(recipe)
    logging.debug(f"Recipe will be named {filename}")

    with open(path.join("..", "data", "recipes", filename), "a") as fh:
        fh.write(json.dumps(recipe, indent=2))


def optional(value: t.Generic[T]) -> t.Optional[T]:
    return value if value else None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please pass the path to the file to build recipes from.")
        sys.exit(1)
    add_new_recipes(sys.argv[1])
