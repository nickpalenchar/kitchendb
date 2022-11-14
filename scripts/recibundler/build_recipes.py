import os
import subprocess
from datetime import datetime
from recibundler.schema.reciperow import isodate_from_recipe
import json
import string
import functools
from jsonschema import validate
import logging as log

log.basicConfig(level=os.environ.get("LOGLEVEL", "WARN"))


PROJECT_ROOT = ".."
RECIPE_DIR = "../data/recipes"
SCHEMA_DIR = "../data/schemas"

HUGO_RECIPE_DIR = "../content/recipes"


def build():
    """
    build takes all json files in data/recipes and builds them into content pages.

    JSON files must all be UpperCammelCase
    """
    clean()

    for file in os.listdir(RECIPE_DIR):
        validate_file_name(file)
        with open(os.path.join(RECIPE_DIR, file)) as fh:
            log.debug(f"Validating schema for {file}...")
            validate_file_schema(fh)
        json_name = file.replace("'", "ʼ")
        mkdown_name = camel_to_snake_case(json_name).replace(".json", ".md")

        log.info(f"building {mkdown_name}...")
        log.debug(f"CMD: hugo new --kind recipes {HUGO_RECIPE_DIR}/{mkdown_name}")
        subprocess.run(
            ["hugo", "new", "--kind", "recipes", f"{HUGO_RECIPE_DIR}/{mkdown_name}"],
            cwd=PROJECT_ROOT,
        )
        post_build_mods(
            os.path.join(RECIPE_DIR, json_name), f"{HUGO_RECIPE_DIR}/{mkdown_name}"
        )


def clean():
    for file in os.listdir(HUGO_RECIPE_DIR):
        os.remove(f"{HUGO_RECIPE_DIR}/{file}")


def validate_file_name(name):
    if not name.endswith(".json"):
        raise Exception("name must be .json extension")
    return name


def validate_file_schema(fh):
    instance = json.loads(fh.read())
    schema = get_recipe_schema()
    validate(instance=instance, schema=schema)


@functools.lru_cache
def get_recipe_schema():
    with open(f"{SCHEMA_DIR}/recipes.json") as fh:
        j = json.loads(fh.read())
    return j


def camel_to_snake_case(name: str) -> str:
    return "".join(
        [name[0].lower()]
        + [
            c
            if (c not in string.ascii_letters or c.islower()) or c in ".()"
            else f"-{c.lower()}"
            for c in name[1:]
        ]
    )


# POST BUILD SCRIPTS #
"""
Because content (content/recipes) is generated from scratch each
time, additional modification to form are required.
"""


def post_build_mods(file: str, mkdown: str) -> None:
    with open(file) as fh:
        recipe = json.loads(fh.read())

    correct_date(recipe, mkdown)
    use_json_name_as_title(recipe, mkdown)
    correct_categories(recipe, mkdown)


def correct_date(recipe: dict, mkdown: str) -> None:
    date = datetime.strptime(recipe["timestamp"], "%m/%d/%Y %H:%M:%S")
    timestamp = date.strftime("%Y-%m-%dT%H:%M:%S-05:00")
    subprocess.run(["sed", "-i", "", f"s#.*\\$DATE\\$$#date: {timestamp}#", mkdown])

def use_json_name_as_title(recipe: dict, mkdown: str) -> None:
    log.debug(f'{__name__}: replacing name with `{recipe["name"]}`')
    subprocess.run(["sed", "-i", "", f"s#.*\\$TITLE\\$$#title: {recipe['name']}#", mkdown])

def correct_categories(recipe: dict, mkdown: str) -> None:
    if "categories" not in recipe:
        return
    categories = recipe["categories"]
    subprocess.run(["sed", "-i", "", f"s#.*\\$CATEGORIES\\$$#categories: {categories}#", mkdown])


if __name__ == "__main__":
    build()
