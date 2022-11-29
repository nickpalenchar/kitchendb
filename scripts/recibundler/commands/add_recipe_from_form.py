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
import typing as t
from datetime import datetime
import logging
from recibundler.schema import reciperow
from recibundler import json_writing

ADD_NEW_RECIPES_SINCE_PATH = "add_new_recipes_since"

T = t.TypeVar("T")

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARN"))


def add_new_recipes(filepath):
    logging.debug(f"filepath is {filepath}")

    with open(filepath, newline="") as fh:
        reader = csv.reader(fh)

        with open(ADD_NEW_RECIPES_SINCE_PATH) as datefh:
            try:
                last_date = datetime.fromisoformat(datefh.read().strip())
            except ValueError:
                logging.warn("starting from beginning of time")
                last_date = datetime(year=2022, month=1, day=28)

        # skip the header
        next(reader)

        for recipe in reader:
            recipe = reciperow.reciperow(*recipe[:17])
            if reciperow.is_recipe_old(recipe, last_date):
                continue
            logging.info(f"the next recipe is {recipe.name}")
            json_writing.write_recipe_to_json(recipe)

            with open(ADD_NEW_RECIPES_SINCE_PATH, mode="w") as datefh:
                datefh.write(str(reciperow.isodate_from_recipe(recipe)))
            return

        logging.error("no new recipes")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please pass the path to the file to build recipes from.")
        sys.exit(1)
    add_new_recipes(sys.argv[1])
