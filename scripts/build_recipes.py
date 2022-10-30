import os
import subprocess
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

        mkdown_name = camel_to_snake_case(file).replace(".json", ".md")

        log.debug(f"building {mkdown_name}...")
        log.debug(f"CMD: hugo new --kind recipes {HUGO_RECIPE_DIR}/{mkdown_name}")
        subprocess.run(
            ["hugo", "new", "--kind", "recipes", f"{HUGO_RECIPE_DIR}/{mkdown_name}"],
            cwd=PROJECT_ROOT,
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
            if (c not in string.ascii_letters or c.islower()) or c == "."
            else f"-{c.lower()}"
            for c in name[1:]
        ]
    )


if __name__ == "__main__":
    build()
