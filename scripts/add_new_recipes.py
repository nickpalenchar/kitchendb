"""
builds new recipes from the submitted google sheet.

Each new recipe should be its own separate PR. Therefore, it should be ran with
a script that can do said checkout and PR.

**Required**: a text file, `add_new_recipes_since`, containing one line--the iso
date of the last recipe to be added. This script will 
"""
import sys
import csv
from datetime import datetime
from collections import namedtuple
from schema_class import Recipe
import build_recipes
import reciparcer
import logging

reciperow = namedtuple(
    "reciperow",
    [
        "timestamp",
        "name",
        "summary",
        "prep_time",
        "cook_time",
        "ingredients",
        "steps",
        "link_to_photo",
        "submitter_email",
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


def isodate_from_recipe(recipe: reciperow):
    return datetime.strptime(recipe.timestamp, "%m/%d/%Y %H:%M:%S")


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
    print("parsing")
    reciparcer.parse_ingredients(recipe.ingredients)
    logging.info("Successfully imported recipe")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please pass the path to the file to build recipes from.")
        sys.exit(1)
    add_new_recipes(sys.argv[1])
